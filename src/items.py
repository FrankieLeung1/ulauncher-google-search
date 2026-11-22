from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction

from src.functions import generate_url, GOOGLE_HOME_URL, GOOGLE_SEARCH_URL


ICON_FILE = 'images/icon.png'

def no_input_item(engine_name='Google', home_url=GOOGLE_HOME_URL):
    return [
        ExtensionResultItem(
            icon=ICON_FILE,
            name=f'Search on {engine_name}',
            on_enter=ExtensionCustomAction(home_url)
        )
    ]

def show_suggestion_items(suggestions, search_url=GOOGLE_SEARCH_URL):
    return [
        ExtensionResultItem(
            icon=ICON_FILE,
            name=suggestion,
            on_enter=ExtensionCustomAction(generate_url(search_url, suggestion))
        )
    for suggestion in suggestions]