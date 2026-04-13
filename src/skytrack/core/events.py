"""Lightweight synchronous event bus for cross-service communication.

Intentionally decoupled from Qt signals so it remains testable without a QApplication.
"""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

EventHandler = Callable[[Any], None]


@dataclass(slots=True)
class EventBus:
    """Publish–subscribe event bus. Topics are plain strings."""

    _subscribers: dict[str, list[EventHandler]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def subscribe(self, topic: str, handler: EventHandler) -> None:
        """Register *handler* to receive payloads published to *topic*."""
        self._subscribers[topic].append(handler)

    def unsubscribe(self, topic: str, handler: EventHandler) -> None:
        """Remove *handler* from *topic*. Silent no-op if not registered."""
        self._subscribers[topic] = [
            h for h in self._subscribers[topic] if h is not handler
        ]

    def publish(self, topic: str, payload: Any = None) -> None:
        """Call every handler registered under *topic* with *payload*."""
        for handler in list(self._subscribers.get(topic, [])):
            handler(payload)
