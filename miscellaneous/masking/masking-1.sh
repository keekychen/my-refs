#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  mask_logs.sh [--dry-run] [--dir DIR] [--keyword1 STR] [--keyword2 STR] [--mask STR]

Description:
  Recursively scan DIR (default: .) for .log and .txt files (case-insensitive).
  For lines that contain both keyword1 and keyword2, mask the JSON password value
  (e.g., "password" : "secret") to masked_password, printing "filename: <masked line>"
  for each changed line (printed to STDERR so you can see it even when output is redirected).
  Prints per-file and total counts.

Options:
  --dry-run              Show what would change but do NOT modify files
  --dir DIR              Root directory to scan (default: .)
  --keyword1 STR         First keyword to require in a line (default: "KW1")
  --keyword2 STR         Second keyword to require in a line (default: "KW2")
  --mask STR             Replacement for the password value (default: "****masked****")
  -h, --help             Show this help

Examples:
  mask_logs.sh
  mask_logs.sh --dry-run --dir /var/log/myapp
  mask_logs.sh --keyword1 "KW1" --keyword2 "KW2" --mask "****masked****"
EOF
}

# Defaults
ROOT_DIR="."
DRYRUN=0
keyword1="KW1"
keyword2="KW2"
masked_password="****masked****"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRYRUN=1; shift ;;
    --dir) ROOT_DIR="${2:-}"; shift 2 ;;
    --keyword1) keyword1="${2:-}"; shift 2 ;;
    --keyword2) keyword2="${2:-}"; shift 2 ;;
    --mask) masked_password="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "ERROR: Unknown argument: $1" >&2; usage; exit 1 ;;
  esac
done

# Checks
if ! command -v awk >/dev/null 2>&1; then
  echo "ERROR: awk not found." >&2; exit 1
fi
if ! awk --version 2>/dev/null | head -n1 | grep -qi 'GNU Awk'; then
  echo "ERROR: GNU Awk (gawk) is required for gensub()." >&2; exit 1
fi
if [[ ! -d "$ROOT_DIR" ]]; then
  echo "ERROR: Directory not found: $ROOT_DIR" >&2; exit 1
fi

echo "Scanning directory: $ROOT_DIR"
echo "Required keywords: '$keyword1' AND '$keyword2'"
echo "Masked password value: '$masked_password'"
[[ "$DRYRUN" -eq 1 ]] && echo "[DRY-RUN] No file will be modified."

# Summary via temp file
SUMMARY="$(mktemp)"
TOTAL=0
cleanup() { rm -f "$SUMMARY"; }
trap cleanup EXIT

# Find .log / .txt files (case-insensitive)
while IFS= read -r -d '' f; do
  [[ -f "$f" ]] || continue

  tmp_out="$(mktemp)"
  tmp_cnt="$(mktemp)"

  gawk -v FILE="$f" -v CNT="$tmp_cnt" -v K1="$keyword1" -v K2="$keyword2" -v MASK="$masked_password" '
    BEGIN { count = 0 }
    {
      line = $0
      if (index(line, K1) && index(line, K2)) {
        # Allow spaces/tabs after "password", around quotes, and around colon.
        new = gensub(/("password[[:space:]]*"[[:space:]]*:[[:space:]]*")[^"]+(")/,
                     "\\1" MASK "\\2", "g", line)
        if (new != line) {
          count++
          # Print masked line to STDERR so you can see it even when stdout is redirected
          printf("%s: %s\n", FILE, new) > "/dev/stderr"
          line = new
        }
      }
      print line
    }
    END { print count > CNT }
  ' "$f" > "$tmp_out"

  c=$(cat "$tmp_cnt" || echo 0)
  rm -f "$tmp_cnt"

  if [[ "$DRYRUN" -eq 0 ]]; then
    if [[ "$c" -gt 0 ]]; then
      mv "$tmp_out" "$f"
      echo "Updated: $f  ($c lines)"
    else
      rm -f "$tmp_out"
    fi
  else
    rm -f "$tmp_out"
  fi

  if [[ "$c" -gt 0 ]]; then
    echo "$c|$f" >> "$SUMMARY"
    TOTAL=$((TOTAL + c))
  fi
done < <(find "$ROOT_DIR" -type f \( -iname '*.log' -o -iname '*.txt' \) -print0)

echo "----- Summary -----"
if [[ ! -s "$SUMMARY" ]]; then
  echo "No changes were necessary."
else
  awk -F'\\|' '{printf "%s  =>  %d lines\n", $2, $1}' "$SUMMARY" | sort
  echo "-------------------"
  echo "TOTAL masked lines: $TOTAL"
fi
