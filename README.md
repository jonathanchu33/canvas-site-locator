# Canvas Site Locator
A web app that Harvard students can use to quickly search for, save, and download files from Canvas sites for courses of interest. Users must own a Harvard-affiliated Canvas account; search results may depend on Canvas user privileges.

## Requirements & Tools
This web app is built on Flask. It uses the Python modules bs4 (Beautiful Soup), cs50 (created by Harvard's CS50), and canvasapi (Python wrapper for the Canvas REST API). The front-end is stylized with Boostrap, with HTML and CSS adopted from Harvard CS50x distribution code.

### Installation
```bash
pip install cs50
pip install bs4
pip install canvasapi
```

Flask installation instructions may be found [here](http://flask.pocoo.org/docs/1.0/installation/). 

## API Token Set-up
Sign into your Canvas account. Under Settings > Approved Integrations, click on "New Access Token" and choose a reasonable expiration date. Copy the token and paste it in app.py:

```python
API_KEY = "Your_API_Token_Here"
```

You are now ready to use the app! Simply launch from terminal using the command ```flask run```.
