# Canvas Site Locator
A web app that Harvard students can use to quickly search for, save, and download files from Canvas sites for courses of interest. Users must own a Harvard-affiliated Canvas account; search results may depend on Canvas user privileges.

## Prerequisites
For best performance, use Python 3. This web app is built on Flask. It uses cs50, a Python package developed by Harvard's CS50, and canvasapi, a Python wrapper for the Canvas REST API). The front-end is stylized with Boostrap, with HTML and CSS adopted from Harvard CS50x distribution code.

### Installation
First, activate a virtual environment (if desired). Then, simply perform
```bash
pip install -r requirements-to-freeze.txt --upgrade
```
to install all required Python dependencies.

Flask installation instructions may be found [here](http://flask.pocoo.org/docs/1.0/installation/). 

## API Token Set-up
Sign into your Canvas account. Under Settings > Approved Integrations, click on "New Access Token" and choose a reasonable expiration date. Copy the token and paste it in app.py:

```python
API_KEY = "Your_API_Token_Here"
```

## Deployment
You are now ready to use the app! Simply launch from terminal using ```flask run```.
Save updated Python dependencies (upon successful app launch) with
```bash
pip freeze > requirements.txt
```
