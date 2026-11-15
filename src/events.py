"""Шина подій. Модулі спілкуються через неї, без прямих імпортів один одного."""

from collections import defaultdict


class EventBus:
    def __init__(self):
        self._handlers = defaultdict(list)

    def subscribe(self, event_name, handler):
        if handler not in self._handlers[event_name]:
            self._handlers[event_name].append(handler)

    def unsubscribe(self, event_name, handler):
        if event_name in self._handlers and handler in self._handlers[event_name]:
            self._handlers[event_name].remove(handler)

    def publish(self, event_name, **data):
        for handler in list(self._handlers.get(event_name, [])):
            handler(**data)