from inputs import get_gamepad
from threading import Thread
import json


class Listener:
    def __init__(self, code2key):
        self.code2key = code2key
        self.actions = {}

    @classmethod
    def load_code2key_json(cls, fp):
        return cls(json.load(fp)["code2key"])

    def action(self, key):
        def decorator(function):
            self.actions[key] = function
        return decorator

    def run(self):
        t = Thread(target=self.__run)
        t.start()

    def __run(self):
        while True:
            events = get_gamepad()
            for i in events:
                if i.code != "SYN_REPORT":   # SYN_REPORT doesn't relate to a specific keypress
                    if i.code not in self.code2key:
                        raise Exception("Pressed a key ({}) that is not in the codes dictionary.".format(i.code))
                    elif self.code2key[i.code] not in self.actions:
                        if self.actions.get("other"):
                            self.actions["other"]()
                        else:
                            raise Exception("Action for this keypress ({}) was not found.".format(self.code2key[i.code]))
                    else:
                        self.actions[self.code2key[i.code]](i.state)

