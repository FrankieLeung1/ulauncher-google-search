import json
import urllib.parse
import urllib.request


DEFAULT_ENGINE = 'google'

SEARCH_ENGINES = {
    'google': {
        'suggest_url': 'https://www.google.com/complete/search?client=firefox&',
        'search_url': 'https://www.google.com/search?channel=fs&client=ubuntu&',
    },
    'duckduckgo': {
        'suggest_url': 'https://duckduckgo.com/ac/?type=list&',
        'search_url': 'https://duckduckgo.com/?',
    },
    'startpage': {
        'suggest_url': 'https://www.startpage.com/osuggestions?',
        'search_url': 'https://www.startpage.com/do/search?',
    },
    'ecosia': {
        'suggest_url': 'https://ac.ecosia.org/autocomplete?type=list&',
        'search_url': 'https://www.ecosia.org/search?',
    },
}

GOOGLE_SUGGESTION_URL = SEARCH_ENGINES['google']['suggest_url']
GOOGLE_SEARCH_URL = SEARCH_ENGINES['google']['search_url']


def get_engine_config(engine=None):
    return SEARCH_ENGINES.get(engine, SEARCH_ENGINES[DEFAULT_ENGINE])


def generate_url(url, search):
    return url + urllib.parse.urlencode({'q': search})


def search_suggestions(search, engine=DEFAULT_ENGINE):
    suggest_url = get_engine_config(engine)['suggest_url']
    request = urllib.request.Request(
        generate_url(suggest_url, search),
        headers={'User-Agent': 'Mozilla/5.0'},
    )
    try:
        with urllib.request.urlopen(request, timeout=5) as req:
            data = req.read()
            encoding = req.info().get_content_charset('utf-8')
        return json.loads(data.decode(encoding))[1]
    except Exception:
        return []


def search_from_google(search):
    return search_suggestions(search, 'google')
