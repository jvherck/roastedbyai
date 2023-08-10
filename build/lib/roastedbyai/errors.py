# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License (jvherck on GitHub)

__all__ = ("MessageLimitExceeded", "CharacterLimitExceeded",)

class MessageLimitExceeded(Exception):
    def __init__(self, _):
        super().__init__(_)

class CharacterLimitExceeded(Exception):
    def __init__(self, _):
        super().__init__(_)