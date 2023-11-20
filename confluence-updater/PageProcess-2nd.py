import requests
import pandas as pd
from bs4 import BeautifulSoup
from collections import OrderedDict

class ConfluenceAPI:
    def __init__(self, url, username, password):
        self.base_url = f"{url}/rest/api/content"
        self.auth = (username, password)

    def get_page_content(self, page_id):
        response = requests.get(f"{self.base_url}/{page_id}?expand=body.storage", auth=self.auth)
        response.raise_for_status()
        return response.json()['body']['storage']['value']

    def update_page(self, page_id, new_content, current_version):
        payload = {
            "version": {"number": current_version + 1},
            "title": "Updated Page Title",
            "type": "page",
            "body": {"storage": {"value": new_content, "representation": "storage"}}
        }
        response = requests.put(f"{self.base_url}/{page_id}", json=payload, auth=self.auth)
        response.raise_for_status()
        return response.status_code

class ContentProcessor:
    def __init__(self, identifier):
        self.identifier = identifier
        self.has_update = False

    def mark_updated(self):
        self.has_update = True

class TableProcessor(ContentProcessor):
    def __init__(self, identifier, html_table):
        super().__init__(identifier)
        self.table = pd.read_html(html_table)[0]

    def update_table(self, updates):
        self.table.update(pd.DataFrame(updates))
        self.mark_updated()

    def to_html(self):
        return self.table.to_html(index=False, border=0)

class TextContentProcessor(ContentProcessor):
    def __init__(self, identifier, text):
        super().__init__(identifier)
        self.text = text

    def update_text(self, new_text):
        self.text = new_text
        self.mark_updated()

    def to_html(self):
        return f'<p id="{self.identifier}">{self.text}</p>'

class ImageProcessor(ContentProcessor):
    def __init__(self, identifier, image_url):
        super().__init__(identifier)
        self.image_url = image_url

    def update_image_url(self, new_url):
        self.image_url = new_url
        self.mark_updated()

    def to_html(self):
        return f'<img src="{self.image_url}" alt="Image">'

class HeadingProcessor(ContentProcessor):
    def __init__(self, identifier, level, text):
        super().__init__(identifier)
        self.level = level
        self.text = text

    def update_text(self, new_text):
        self.text = new_text
        self.mark_updated()

    def to_html(self):
        return f'<h{self.level} id="{self.identifier}">{self.text}</h{self.level}>'

class ListProcessor(ContentProcessor):
    def __init__(self, identifier, html_list):
        super().__init__(identifier)
        self.html_list = html_list

    def update_list(self, new_html):
        self.html_list = new_html
        self.mark_updated()

    def to_html(self):
        return self.html_list

class LinkProcessor(ContentProcessor):
    def __init__(self, identifier, href, text):
        super().__init__(identifier)
        self.href = href
        self.text = text

    def update_link(self, new_href, new_text):
        self.href = new_href
        self.text = new_text
        self.mark_updated()

    def to_html(self):
        return f'<a id="{self.identifier}" href="{self.href}">{self.text}</a>'

class PageProcess:
    def __init__(self, url, username, password, page_id):
        self.api = ConfluenceAPI(url, username, password)
        self.page_id = page_id
        self.content_processors = OrderedDict()
        self.original_html = None
        self.element_positions = {}
        self.current_version = 0

    def fetch_page_content(self):
        self.original_html = self.api.get_page_content(self.page_id)
        soup = BeautifulSoup(self.original_html, 'html.parser')

        for index, table in enumerate(soup.find_all('table')):
            identifier = table.get('id') or f'table_{index}'
            self.element_positions[identifier] = str(table)
            self.content_processors[identifier] = TableProcessor(identifier, str(table.extract()))

        for index, p in enumerate(soup.find_all('p')):
            identifier = p.get('id') or f'text_{index}'
            self.element_positions[identifier] = str(p)
            self.content_processors[identifier] = TextContentProcessor(identifier, p.get_text())

        for index, img in enumerate(soup.find_all('img')):
            identifier = img.get('id') or f'image_{index}'
            self.element_positions[identifier] = str(img)
            self.content_processors[identifier] = ImageProcessor(identifier, img['src'])

        for index, heading in enumerate(soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])):
            identifier = heading.get('id') or f'heading_{index}'
            level = heading.name[-1]
            self.element_positions[identifier] = str(heading)
            self.content_processors[identifier] = HeadingProcessor(identifier, level, heading.get_text())

        for index, lst in enumerate(soup.find_all(['ul', 'ol'])):
            identifier = lst.get('id') or f'list_{index}'
            self.element_positions[identifier] = str(lst)
            self.content_processors[identifier] = ListProcessor(identifier, str(lst))

        for index, link in enumerate(soup.find_all('a')):
            identifier = link.get('id') or f'link_{index}'
            self.element_positions[identifier] = str(link)
            self.content_processors[identifier] = LinkProcessor(identifier, link['href'], link.get_text())

        self.current_version = self.get_current_version()

    def get_current_version(self):
        response = requests.get(f"{self.api.base_url}/{self.page_id}", auth=self.api.auth)
        response.raise_for_status()
        return response.json()['version']['number']

    def update_contents(self):
        updated_html = self.original_html
        for identifier, processor in self.content_processors.items():
            if processor.has_update:
                updated_part = processor.to_html()
                updated_html = updated_html.replace(self.element_positions[identifier], updated_part)

        return updated_html

    def push_update(self):
        new_content = self.update_contents()
        return self.api.update_page(self.page_id, new_content, self.current_version)

# 使用示例
page_processor = PageProcess('http://your-confluence-url', 'username', 'password', 'page_id')
page_processor.fetch_page_content()
# 进行内容更新
page_processor.content_processors['text_0'].update_text("This is updated text")
page_processor.content_processors['image_0'].update_image_url("http://newimageurl.com/image.jpg")
# 推送更新
page_processor.push_update()
