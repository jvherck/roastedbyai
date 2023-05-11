# MIT License
#
# Copyright (c) 2023 jvherck (on GitHub)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import html

from .errors import MessageLimitExceeded, CharacterLimitExceeded


__all__ = ("Conversation",)


# Create a new object of this class for every simultaneous conversation you want to have
class Conversation:
    """
    An object of this class represents a conversation with the AI.
    Make a new object if this conversation reached its message limit.
    """
    def __init__(self):
        """
        Creates an object of this class that represents a conversation with the AI.
        Make a new object if this conversation reached its message limit.
        """
        # Initialising variables, do NOT change these!
        # Private variables start with _
        self._aimessages: list = []
        self._usermessages: list = []
        self._alive: bool = True
        self._selnumber: int = 1
        self._selector: str = '/html/body/div/div/div[2]/div[2]/div[2]/div/div[{}]/div'
        self._cooldown: int = 10

        # Opening browser and waiting until initial message is shown
        self._driver = webdriver.Chrome()
        self._driver.get('https://roastedby.ai')
        WebDriverWait(self._driver, self._cooldown).until(
            EC.presence_of_element_located(
                (By.XPATH, self._selector.format(self._selnumber))
            )
        )

        # Locating input box
        WebDriverWait(self._driver, self._cooldown).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, 'inputBox')
            )
        )
        self._input_box = self._driver.find_element(by=By.CLASS_NAME, value='inputBox')


    @property
    def aimessages(self):
        return self._aimessages

    @property
    def usermessages(self):
        return self._usermessages

    @property
    def alive(self):
        return self._alive


    def _scrollToBottom(self):
        self._driver.execute_script(
            """
            var elem = document.getElementsByClassName("chatMessages")[0];
            elem.scrollTo(0, elem.scrollHeight);
            """
        )


    def send(self, message: str) -> str:
        """
        Sends the user input to the AI and the AI returns a roast as output.

        :param message: the user input for the AI
        :type message: str
        :return: returns a string containing the AI's (roast) response to the user's input
        """
        # Checking if message limit isn't reached yet
        if self.alive is False:
            raise MessageLimitExceeded('Message limit is exceeded, create a new object of this class to continue again.')

        # Checking for max character length
        if len(message) > 250:
            raise CharacterLimitExceeded('Character limit is exceeded: maximum allowed number of characters is 250!')

        # Removing all unsupported characters
        for char in message:
            if ord(char) > 65535:
                message = message.replace(char, '￿')

        # Insert user input to input box
        self._input_box.send_keys(message)
        self._input_box.send_keys(Keys.RETURN)

        # Increase selector number by 2 to get the next AI message
        # (every odd number is an AI's message, note that the initial value is 1)
        self._selnumber += 2

        # Wait for the AI to respond (as soon as the 3 loading symbols disappear, the AI's response is shown)
        ie = (NoSuchElementException, StaleElementReferenceException,)
        WebDriverWait(self._driver, self._cooldown, ignored_exceptions=ie).until_not(
            EC.text_to_be_present_in_element_attribute(
                (By.XPATH, self._selector.format(self._selnumber)),
                'innerHTML',
                # Note that the following string is ONE string on two separate lines! (readability)
                '<span class="circle animate-loader"></span><span class="circle animate-loader animation-delay-200">'
                '</span><span class="circle animate-loader animation-delay-400"></span>'
            )
        )

        # Scroll to bottom of chat window
        self._scrollToBottom()

        # Get AI's response
        result = self._driver.find_element(by=By.XPATH, value=self._selector.format(self._selnumber)) \
            .get_attribute('innerHTML')
        result = html.unescape(result)

        # Storing messages
        self._aimessages.append(result)
        self._usermessages.append(message)

        # Checking if message limit is reached
        if result == 'Too many messages. Thanks for playing!':
            self._alive = False
            self.quit()
        elif result == 'Can you calm down?! You exceeded the rate limit. Please try again later.':
            self._alive = False
            self.quit()

        return result


    def quit(self) -> None:
        """
        Quit and close the conversation.
        User and AI messages are still available using `.usermessages` and `.aimessages`
        """
        self._alive = False
        self._driver.quit()
