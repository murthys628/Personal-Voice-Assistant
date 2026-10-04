"""Rule-based command matching and safe action dispatch."""

from __future__ import annotations

import platform
import re
import subprocess
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from typing import Callable
from urllib.parse import quote_plus


@dataclass(frozen=True)
class Response:
    text: str
    should_exit: bool = False


def open_application(name: str) -> None:
    """Launch one of the explicitly supported applications."""
    applications = {
        "notepad": {
            "Windows": ["notepad.exe"],
            "Darwin": ["open", "-a", "TextEdit"],
            "Linux": ["gedit"],
        },
        "calculator": {
            "Windows": ["calc.exe"],
            "Darwin": ["open", "-a", "Calculator"],
            "Linux": ["gnome-calculator"],
        },
    }
    command = applications.get(name, {}).get(platform.system())
    if command is None:
        raise ValueError(f"'{name}' is not a supported app on this system")
    subprocess.Popen(command, shell=False)


class CommandRouter:
    """Map recognized phrases to a small set of safe actions."""

    def __init__(
        self,
        *,
        search_web: Callable[[str], object] = webbrowser.open,
        launch_app: Callable[[str], object] = open_application,
        clock: Callable[[], datetime] = datetime.now,
    ) -> None:
        self.search_web = search_web
        self.launch_app = launch_app
        self.clock = clock

    def handle(self, command: str) -> Response:
        phrase = " ".join(command.casefold().split())
        if not phrase:
            return Response("I didn't catch that. Please try again.")

        if phrase in {"quit", "exit", "stop", "goodbye"}:
            return Response("Goodbye!", should_exit=True)
        if phrase in {"help", "commands", "what can you do"}:
            return Response(
                "Try: 'tell me the time', 'search for weather today', "
                "'open notepad', 'open calculator', or 'exit'."
            )
        if phrase in {"time", "what time is it", "tell me the time", "current time"}:
            return Response(f"It is {self.clock().strftime('%I:%M %p').lstrip('0')}.")

        search_match = re.match(r"^(?:search(?: the web)?(?: for)?|google)\s*(.*)$", phrase)
        if search_match:
            query = search_match.group(1).strip()
            if not query:
                return Response("What would you like me to search for?")
            try:
                self.search_web(f"https://www.google.com/search?q={quote_plus(query)}")
            except Exception:
                return Response("I couldn't open a web search. Please check your browser.")
            return Response(f"Searching the web for {query}.")

        app_match = re.match(r"^(?:open(?: the)? app|open|launch)\s+(.+)$", phrase)
        if app_match:
            app_name = app_match.group(1).strip()
            if app_name not in {"notepad", "calculator"}:
                return Response("I can open notepad or calculator on this system.")
            try:
                self.launch_app(app_name)
            except (OSError, ValueError):
                return Response(f"I couldn't open {app_name}. It may not be installed.")
            return Response(f"Opening {app_name}.")

        return Response("I don't know that command yet. Say 'help' for examples.")