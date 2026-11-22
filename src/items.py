from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction

from src.functions import generate_url, GOOGLE_SEARCH_URL


ICON_FILE = 'images/icon.png'

def no_input_item():
    return [
        ExtensionResultItem(
            icon=ICON_FILE,
            name='No input',
            on_enter=DoNothingAction()
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