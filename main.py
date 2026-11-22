import subprocess

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction

from src.functions import DEFAULT_ENGINE, get_engine_config, search_suggestions
from src.items import no_input_item, show_suggestion_items

class GoogleSearchExtension(Extension):
    def __init__(self):
        super(GoogleSearchExtension, self).__init__()

        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or str()
        engine = extension.preferences.get('search_engine', DEFAULT_ENGINE) if extension else DEFAULT_ENGINE
        engine_config = get_engine_config(engine)

        if len(query.strip()) == 0:
            return RenderResultListAction(no_input_item(engine_config['name']))

        suggestions = list(dict.fromkeys([query] + search_suggestions(query, engine)))
        return RenderResultListAction(show_suggestion_items(suggestions, engine_config['search_url']))


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        url = event.get_data()
        subprocess.Popen(
            ['zen-browser', '--blank-window', url],
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


if __name__ == '__main__':
    GoogleSearchExtension().run()
