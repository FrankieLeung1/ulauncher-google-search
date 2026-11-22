import json
import urllib.parse
import urllib.request


GOOGLE_SUGGESTION_URL = 'https://www.google.com/complete/search?client=firefox&'
GOOGLE_SEARCH_URL = 'https://www.google.com/search?channel=fs&client=ubuntu&'


def generate_url(url, search):
    return url + urllib.parse.urlencode({ 'q': search })


def search_from_google(search):
    with urllib.request.urlopen(generate_url(GOOGLE_SUGGESTION_URL, search), timeout=5) as req:
        data = req.read()
        encoding = req.info().get_content_charset('utf-8')

    return json.loads(data.decode(encoding))[1]
