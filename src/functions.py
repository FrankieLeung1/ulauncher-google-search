import json
import urllib.parse
import urllib.request


DEFAULT_ENGINE = 'google'


def _parse_opensearch_suggestions(data):
    return data[1]


def _parse_bing_suggestions(data):
    results = data.get('AS', {}).get('Results', [])
    return [item['Txt'] for group in results for item in group.get('Suggests', []) if 'Txt' in item]


SEARCH_ENGINES = {
    'google': {
        'name': 'Google',
        'home_url': 'https://www.google.com/',
        'suggest_url': 'https://www.google.com/complete/search?client=firefox&',
        'search_url': 'https://www.google.com/search?',
    },
    'bing': {
        'name': 'Bing',
        'home_url': 'https://www.bing.com/',
        'suggest_url': 'https://api.bing.com/qsonhs.aspx?',
        'search_url': 'https://www.bing.com/search?',
        'parser': _parse_bing_suggestions,
    },
    'duckduckgo': {
        'name': 'DuckDuckGo',
        'home_url': 'https://duckduckgo.com/',
        'suggest_url': 'https://duckduckgo.com/ac/?type=list&',
        'search_url': 'https://duckduckgo.com/?',
    },
    'startpage': {
        'name': 'Startpage',
        'home_url': 'https://www.startpage.com/',
        'suggest_url': 'https://www.startpage.com/osuggestions?',
        'search_url': 'https://www.startpage.com/do/search?',
    },
    'ecosia': {
        'name': 'Ecosia',
        'home_url': 'https://www.ecosia.org/',
        'suggest_url': 'https://ac.ecosia.org/autocomplete?type=list&',
        'search_url': 'https://www.ecosia.org/search?',
    },
}

GOOGLE_HOME_URL = SEARCH_ENGINES['google']['home_url']
GOOGLE_SUGGESTION_URL = SEARCH_ENGINES['google']['suggest_url']
GOOGLE_SEARCH_URL = SEARCH_ENGINES['google']['search_url']


def get_engine_config(engine=None):
    return SEARCH_ENGINES.get(engine, SEARCH_ENGINES[DEFAULT_ENGINE])


def generate_url(url, search):
    return url + urllib.parse.urlencode({'q': search})


def search_suggestions(search, engine=DEFAULT_ENGINE):
    config = get_engine_config(engine)
    parser = config.get('parser', _parse_opensearch_suggestions)
    request = urllib.request.Request(
        generate_url(config['suggest_url'], search),
        headers={'User-Agent': 'Mozilla/5.0'},
    )
    try:
        with urllib.request.urlopen(request, timeout=5) as req:
            data = req.read()
            encoding = req.info().get_content_charset('utf-8')
        return parser(json.loads(data.decode(encoding)))
    except Exception:
        return []


def search_from_google(search):
    return search_suggestions(search, 'google')
