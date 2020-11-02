# A Practical Introduction to Web Scraping in Python
## Introduction
Let's start by describing what **web scraping** is. If you are a student, researcher, data scientist or if you would want to traverse through large amounts of data on a website or websites then web scraping would solve the challenge of manually browsing each website to get the data you are looking for. Scraping is the process where a program automatically collects data from websites. In this post I'll be looking at how to:

* Automatically break up content that's on a website into separate components.

## Scrape and Parse Text From Websites
What do we mean by *parsing text from a website*? First, let's get to understand how data on a webpage is structured.  

A web page (or webpage) is a document that's written using HTML (Hyper Text Markup Language). Below is an example of a simple HTML document

```
<!DOCTYPE html>
<html lang="en">

<meta charset="utf-8">
<title>Page Title</title>

<body>
   <h1>This is a Heading</h1>
   <p>This is a paragraph.</p>
   <p>This is another paragraph.</p>
</body>

</html>
```
The above piece of HTML will render the below page.

```
This is a Heading
This is a paragraph.

This is a another paragraph.
```

If you would like to learn more about HTML take a look at [What is HTML?](https://www.w3schools.com/whatis/whatis_html.asp)

Parsing involves grabbing all the HTML code in a web page and extracting the text based content while leaving out the HTML code.

### Our very first web scraper
We'll be using the [Python](https://www.python.org/) programming language to build our web scraper. Python is an easy to learn language and has a number of useful in-built packages and dependencies (3rd party programs) to help in  building a web scraper.

One useful package we have for web scraping in Python is `urllib`, which contains tools for working with URLS. To open a url in python we would use the `urllib.request` module which contains a function called `urlopen()`.    

Here is a simple program that uses `urlopen()`

***script.py***
```
import sys

from urllib.request import urlopen

def open_page(argv):    
    page = urlopen(sys.argv[1])
    print(page)

    
if __name__ == "__main__":
    open_page(sys.argv[1])
```

When we run the above script on a terminal (we are passing "http://olympus.realpython.org/profiles/aphrodite" as the url to open) 

```
$ python script.py "http://olympus.realpython.org/profiles/aphrodite"
$ <http.client.HTTPResponse object at 0x7f9b03a9ab70>
```
A `HTTPResponse` object is printed out on the terminal:

`<http.client.HTTPResponse object at 0x7f9b03a9ab70>`

This object is not useful to use until we are able to extract the HTML from the page. We'll now use the `read()` method, which will return a sequence of bytes. To decode it to a [UTF-8](https://realpython.com/python-encodings-guide/#unicode-vs-utf-8) string we use `.decode`

Here is the update script.py file:

```
import sys

from urllib.request import urlopen


def open_page(argv):
    page = urlopen(sys.argv[1])
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    print(html)


if __name__ == "__main__":
    open_page(sys.argv[1])
```

This will now print out:

```
<html>
   <head>
      <title>Profile: Aphrodite</title>
   </head>
   <body bgcolor="yellow">
      <center>
         <br><br>
         <h2>Name: Aphrodite</h2>
         <br><br>
         Favorite animal: Dove
         <br><br>
         Favorite color: Red
         <br><br>
         Hometown: Mount Olympus
      </center>
   </body>
</html>
```

Which is rendered by a browser as such:

<html>
   <head>
      <title>Profile: Aphrodite</title>
   </head>
   <body bgcolor="yellow">
      <center>
         <br><br>
         <h2>Name: Aphrodite</h2>
         <br><br>
         Favorite animal: Dove
         <br><br>
         Favorite color: Red
         <br><br>
         Hometown: Mount Olympus
      </center>
   </body>
</html>

<br>
Now we have our HTML, so how then do we extract text from it.
<br><br>

## Extract text from HTML with string methods
Another set of built in tools that will come in handy are python's string methods. These are methods that manipulate string values. For example:

* capitalize() - Converts the first character of a string to upper case
* casefold() - Converts a string into lower case
* center() - Returns a centered string.

There are a number of string methods. You can learn of them all here [String Methods](https://docs.python.org/2.5/lib/string-methods.html)

For our case, let's say we want to extract the title of the page which from our example is `Profile: Aphrodite`, we will first determine the index of the first character of the opening `<title>` tag of the page and the first character of the closing `</title>` tag, then use string slicing to extract the title.

`.find()` method returns the index of the first occurrence of a substring, we'll use it to get the index of the opening `<title>` tag by passing the `"<title>"` to `.find()`:

```
>>> title_tag_start_index = html.find("<title>")
>>> title_tag_start_index
14
```

We don't want the index of the `<title>` tag instead what we want is the index of the title itself. To get that (index of the first letter in the title), we add the length of the string `"<title>"` to the value of title_tag_start_index:

```
>>> title_text_start_index = title_tag_start_index + len("<title>")
>>> title_text_start_index
21
```

Next, let's get the index of the closing `</title>` tag by passing the string `"</title>"` to `.find()`:

```
>>> title_text_end_index = html.find("</title>")
>>> title_text_end_index
39
```

Finally, we can now extract the title by slicing the `html` string:
```
>>> title = html[title_text_start_index:title_text_end_index]
>>> title
'Profile: Aphrodite'
```
Below i have updated script.py with the above commands:

```
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
```

After extracting the html from the given url the `open_page(argv)` method calls the `find_title(html)` method and pass the html object to it. Which then prints out the index of the starting character of the `<title>` tag.

