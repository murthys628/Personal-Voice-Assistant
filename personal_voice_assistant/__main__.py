"""Run the personal voice assistant."""

from personal_voice_assistant.commands import CommandRouter
from personal_voice_assistant.speech import SpeechIO, SpeechUnavailable


def main() -> None:
    router = CommandRouter()
    speech = SpeechIO()
    microphone_enabled = True
    speech_output_enabled = True

    print("Personal Voice Assistant. Say 'help' for commands, or type them.")
    while True:
        try:
            if microphone_enabled:
                command = speech.listen()
                if command is None:
                    print("I didn't catch that. Please try again.")
                    continue
                print(f"You: {command}")
            else:
                command = input("You: ")
        except SpeechUnavailable as error:
            print(f"Voice input unavailable ({error}); switching to text input.")
            microphone_enabled = False
            continue
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        response = router.handle(command)
        print(f"Assistant: {response.text}")
        if speech_output_enabled:
            try:
                speech.speak(response.text)
            except SpeechUnavailable as error:
                print(f"Spoken output unavailable ({error}); continuing with text.")
                speech_output_enabled = False
        if response.should_exit:
            break


if __name__ == "__main__":
    main()