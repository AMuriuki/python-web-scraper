import sys

from urllib.request import urlopen


def open_page(argv):
    page = urlopen(sys.argv[1])
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    print(html)
    find_title_index(html)


def find_title_index(html):
    title_index = html.find("<title>")
    print (title_index)


if __name__ == "__main__":
    open_page(sys.argv[1])
