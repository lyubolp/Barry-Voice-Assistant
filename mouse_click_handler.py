import subprocess

from pymouse import PyMouseEvent


class VoiceAssistantEvent(PyMouseEvent):
    def __init__(self):
        PyMouseEvent.__init__(self)

    def click(self, x, y, button, press):
        # Call voice assistant when mouse is pressed
        if button == 1:
            if press:
                subprocess.run(['python3', './voice_assistant.py'])


if __name__ == '__main__':
    assistant = VoiceAssistantEvent()
    assistant.run()
