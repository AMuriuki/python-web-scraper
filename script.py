import sys

from urllib.request import urlopen


def open_page(argv):
    page = urlopen(sys.argv[1])
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    print(type(html))
    find_title(html)


def find_title(html):
    title_tag_start_index = html.find("<title>")
    title_text_start_index = title_tag_start_index + len("<title>")
    title_text_end_index = html.find("</title>")
    title = html[title_text_start_index:title_text_end_index]
    print(title)


if __name__ == "__main__":
    open_page(sys.argv[1])
