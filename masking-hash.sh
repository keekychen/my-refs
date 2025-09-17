#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  mask_logs.sh [--dry-run] [--dir DIR] [--keyword1 STR] [--keyword2 STR] [--mask STR]

Description:
  Recursively scan DIR (default: .) for .log and .txt files (case-insensitive).
  For lines that contain both keyword1 and keyword2, REPLACE the JSON password value
  with its SHA-256 hex. Prints "filename: <hashed line>" for each changed line
  (printed to STDERR so you can see it even when stdout is redirected).
  Prints per-file and total counts.

Note:
  Requires GNU Awk (gawk). Also requires one of: sha256sum | shasum | openssl.

Options:
  --dry-run              Show what would change but do NOT modify files
  --dir DIR              Root directory to scan (default: .)
  --keyword1 STR         First keyword to require in a line (default: "Request body")
  --keyword2 STR         Second keyword to require in a line (default: "clientIPAddress")
  --mask STR             (Ignored in SHA-256 mode; kept for compatibility)
  -h, --help             Show this help

Examples:
  mask_logs.sh
  mask_logs.sh --dry-run --dir /var/log/myapp
  mask_logs.sh --keyword1 "Request body" --keyword2 "clientIPAddress"
EOF
}

# Defaults
ROOT_DIR="."
DRYRUN=0
keyword1="Request body"
keyword2="clientIPAddress"
masked_password="****masked****"   # kept for CLI compatibility, not used now

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRYRUN=1; shift ;;
    --dir) ROOT_DIR="${2:-}"; shift 2 ;;
    --keyword1) keyword1="${2:-}"; shift 2 ;;
    --keyword2) keyword2="${2:-}"; shift 2 ;;
    --mask) masked_password="${2:-}"; shift 2 ;;   # ignored
    -h|--help) usage; exit 0 ;;
    *) echo "ERROR: Unknown argument: $1" >&2; usage; exit 1 ;;
  esac
done

# Checks
if ! command -v awk >/dev/null 2>&1; then
  echo "ERROR: awk not found." >&2; exit 1
fi
if ! awk --version 2>/dev/null | head -n1 | grep -qi 'GNU Awk'; then
  echo "ERROR: GNU Awk (gawk) is required." >&2; exit 1
fi
if [[ ! -d "$ROOT_DIR" ]]; then
  echo "ERROR: Directory not found: $ROOT_DIR" >&2; exit 1
fi

# Pick a SHA-256 command to use and pass it to gawk
SHA256_CMD=""
if command -v sha256sum >/dev/null 2>&1; then
  SHA256_CMD="sha256sum"
elif command -v shasum >/dev/null 2>&1; then
  SHA256_CMD="shasum -a 256"
elif command -v openssl >/dev/null 2>&1; then
  SHA256_CMD="openssl dgst -sha256 -r"
else
  echo "ERROR: Need one of: sha256sum, shasum, or openssl." >&2
  exit 1
fi

echo "Scanning directory: $ROOT_DIR"
echo "Required keywords: '$keyword1' AND '$keyword2'"
echo "Hashing command: $SHA256_CMD"
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

  gawk -v FILE="$f" -v CNT="$tmp_cnt" -v K1="$keyword1" -v K2="$keyword2" -v SHA256_CMD="$SHA256_CMD" '
    # Compute SHA-256 hex of string s using an external command via a coprocess.
    function sha256(s,    cmd, out) {
      cmd = SHA256_CMD
      # Start coprocess; send s WITHOUT trailing newline
      printf "%s", s |& cmd
      close(cmd, "to")
      cmd |& getline out
      close(cmd)
      # Output formats:
      #  - sha256sum: "<hex>  -"
      #  - shasum:    "<hex>  -"
      #  - openssl -r:"<hex> *stdin"
      split(out, a, /[[:space:]]+/)
      return a[1]
    }

    BEGIN {
      count = 0
      # Regex: capture 3 groups:
      #  1: prefix including "password" + spacing + colon + opening quote
      #  2: the password value (no quotes)
      #  3: the closing quote
      r = /("password[[:space:]]*"[[:space:]]*:[[:space:]]*")([^"]+)(")/
    }

    {
      line = $0
      if (index(line, K1) && index(line, K2)) {
        changed = 0
        # Iteratively replace ALL password values in this line
        while (match(line, r, m)) {
          hashed = sha256(m[2])
          line = substr(line, 1, RSTART-1) m[1] hashed m[3] substr(line, RSTART+RLENGTH)
          changed = 1
          count++
        }
        if (changed) {
          # Print hashed line to STDERR so it shows while stdout is redirected
          printf("%s: %s\n", FILE, line) > "/dev/stderr"
        }
      }
      print line
    }

    END {
      print count > CNT
    }
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
done < <(find "$ROOT_DIR" -type f \( -iname "*.log" -o -iname "*.txt" \) -print0)

echo "----- Summary -----"
if [[ ! -s "$SUMMARY" ]]; then
  echo "No changes were necessary."
else
  awk -F'\\|' '{printf "%s  =>  %d lines\n", $2, $1}' "$SUMMARY" | sort
  echo "-------------------"
  echo "TOTAL updated lines: $TOTAL"
fi

