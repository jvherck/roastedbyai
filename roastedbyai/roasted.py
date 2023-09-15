# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License (jvherck on GitHub)

import requests
from typing import List

from .errors import MessageLimitExceeded, CharacterLimitExceeded
from .models import Style


__all__ = ("Conversation",)


# Create a new object of this class for every simultaneous conversation you want to have
class Conversation:
    """
    An instance of this class represents a conversation with the AI.
    Create a new instance of this class if this conversation reached its message limit.
    """
    def __init__(self, style: str = Style.default):
        """
        Creates an instance of this class that represents a conversation with the AI.
        Create a new instance if this conversation reached its message limit.

        :param style: The talking style of the AI. Use auxiliary class roastedbyai.models.Style
        :type style: str
        """
        if style not in Style.all:
            raise ValueError(f'"{self.style}" is not a valid style. Check the `Style` class to see possibilities.')
        self.__history: list = [{
            "role": "assistant",
            "content": "Hello there. I'm here to roast you."
        }]
        self.__alive: bool = True
        self.__style: str = style
        self.__url: str = "https://roastedby.ai/api/generate"

    def __str__(self):
        """
        :returns: the content of the last message in `Conversation.history`
        """
        return self.__history[len(self.__history)-1]["content"]

    def __len__(self):
        """
        :returns: the amount of messages in `Conversation.history`
        """
        return len(self.__history)

    @property
    def aimessages(self) -> list:
        """
        Get the list of the AI's messages.

        :returns: list: the list of messages
        """
        aimsgs = []
        for msg in self.__history:
            if msg["role"] == "assistant":
                aimsgs.append(msg["content"])
        return aimsgs

    @property
    def usermessages(self) -> list:
        """
        Get the list of the user's messages.

        :returns: list: the list of messages
        """
        aimsgs = []
        for msg in self.__history:
            if msg["role"] == "user":
                aimsgs.append(msg["content"])
        return aimsgs

    @property
    def history(self) -> List[dict]:
        """
        Return the full history of this Conversation.

        [
        {"role": "assistant","content": "..."},
        {"role": "user","content": "..."},
        ...
        ]

        :returns: list[dict]: the history list which contains dicts
        """
        return self.__history

    @property
    def alive(self) -> bool:
        """
        Whether you are still able to participate in this Conversation.
        If this returns False, you can no longer use the `Conversation.send` function, but you can still access the message history.

        :returns: bool: True if you can still send messages, else False
        """
        return self.__alive

    @property
    def style(self) -> str:
        """
        Returns the talking style of this Conversation.

        :returns: roastedbyai.models.Style: the style
        """
        return self.__style

    def send(self, message: str) -> str:
        """
        Sends the user input to the AI and the AI returns a roast as output.

        :param message: str: the user input for the AI (max character limit of 250)
        :type message: str
        :return: returns a string containing the AI's (roast) response to the user's input
        """
        if self.__alive is False:
            raise MessageLimitExceeded('Message limit exceeded, you can not send any more messages to this Conversation.')

        if len(message) > 250:
            raise CharacterLimitExceeded('Character limit exceeded: maximum allowed number of characters is 250!')

        if self.style not in Style.all:
            raise ValueError(f'"{self.style}" is not a valid style. Check the `Style` class to see possibilities.')

        # Removing non-allowed characters
        for char in message:
            if ord(char) > 65535:
                message = message.replace(char, '￿')

        _json_body = {
            "userMessage": {
                "role": "user",
                "content": message
            },
            "history": self.__history,
            "style": str(self.__style)
        }
        _headers = {
            "Accept": "*/*",
            "Accept-Encoding": "br",
            "Accept-Language": "en-GB,en;q=0.9",
            "Content-Length": str(len(str(_json_body))),
            "Content-Type": "application/json",
            "Origin": "https://roastedby.ai",
            "Referer": "https://roastedby.ai/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        }

        result = requests.post(self.__url, json=_json_body, headers=_headers).json()["content"]

        self.__history.append({
            "role": "user",
            "content": message
        })
        self.__history.append({
            "role": "assistant",
            "content": result
        })

        if result == 'Too many messages. Thanks for playing!':
            self.kill()
        elif result == 'Can you calm down?! You exceeded the rate limit. Please try again later.':
            self.kill()

        return result

    def kill(self) -> None:
        """
        Quit and close the conversation.
        User and AI messages are still available using `Conversation.usermessages` and `Conversation.aimessages`.
        The full conversation is available in `Conversation.history`.
        """
        self.__alive = False
