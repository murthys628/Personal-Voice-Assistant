from datetime import datetime
import unittest

from personal_voice_assistant.commands import CommandRouter


class CommandRouterTests(unittest.TestCase):
    def test_time_command_uses_injected_clock(self) -> None:
        router = CommandRouter(clock=lambda: datetime(2026, 10, 4, 9, 5))

        self.assertEqual(router.handle("tell me the time").text, "It is 9:05 AM.")

    def test_search_command_encodes_query_and_opens_browser(self) -> None:
        opened_urls: list[str] = []
        router = CommandRouter(search_web=opened_urls.append)

        response = router.handle("search for cats and dogs")

        self.assertEqual(opened_urls, ["https://www.google.com/search?q=cats+and+dogs"])
        self.assertEqual(response.text, "Searching the web for cats and dogs.")

    def test_open_app_only_launches_allowlisted_app(self) -> None:
        opened_apps: list[str] = []
        router = CommandRouter(launch_app=opened_apps.append)

        response = router.handle("open app calculator")

        self.assertEqual(opened_apps, ["calculator"])
        self.assertEqual(response.text, "Opening calculator.")

    def test_unrecognized_app_is_not_launched(self) -> None:
        opened_apps: list[str] = []
        router = CommandRouter(launch_app=opened_apps.append)

        response = router.handle("open powershell")

        self.assertEqual(opened_apps, [])
        self.assertIn("notepad or calculator", response.text)

    def test_exit_command_requests_shutdown(self) -> None:
        response = CommandRouter().handle("goodbye")

        self.assertTrue(response.should_exit)


if __name__ == "__main__":
    unittest.main()