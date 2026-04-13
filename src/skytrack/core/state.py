"""Central application state store.

Only AppStateStore.update() or AppStateStore.append_message() mutates state.
All UI components subscribe to state changes via subscribe().
"""
from __future__ import annotations

from dataclasses import replace
from typing import Callable

from skytrack.core.models import AppState, MessageEntry

StateListener = Callable[[AppState], None]


class AppStateStore:
    """Single source of truth for all mutable application state."""

    def __init__(self, initial: AppState | None = None) -> None:
        self._state: AppState = initial or AppState()
        self._listeners: list[StateListener] = []

    @property
    def state(self) -> AppState:
        """Current state snapshot (read-only)."""
        return self._state

    def subscribe(self, listener: StateListener) -> None:
        """Register *listener*; immediately called with current state."""
        self._listeners.append(listener)
        listener(self._state)

    def unsubscribe(self, listener: StateListener) -> None:
        self._listeners = [l for l in self._listeners if l is not listener]

    def update(self, **changes: object) -> None:
        """Replace top-level fields and notify all listeners."""
        self._state = replace(self._state, **changes)  # type: ignore[arg-type]
        self._emit()

    def append_message(self, message: MessageEntry) -> None:
        """Append a log message and notify listeners."""
        self._state.messages.append(message)
        self._emit()

    def _emit(self) -> None:
        for listener in list(self._listeners):
            listener(self._state)
