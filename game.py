import json
import commands

class game:
    all_commands = []
    languages = {
        "en": "english",
        "de": "deutsch"
    }
    translations = {}

    def __init__(self, file="rooms.json"):
        """Init a new game and load a map file from https://www.trizbort.io"""
        self.config = {}
        self.rooms = []
        self.connections = []
        self.elements = []
        self.players = []

        game.all_commands = commands.command.__subclasses__()

        # open a map generated with https://www.trizbort.io
        f = open(file)
        self.config = json.load(f)
        f.close()
        self.load_translations()
        config = self.config

        self.elements = config["elements"]
        for e in config["elements"]:
            if e["_type"] == "Connector":
                self.connections.append(e)
            elif e["_type"] == "Room":
                self.rooms.append(e)
    
    def load_translations(self):
        for lang in self.languages:
            f = open(f"{lang}.json")
            self.translations[lang] = json.load(f)
            f.close()

    def add_player(self, player):
        self.players.append(player)
        if self.config["startRoom"] == 0:
            player.room = self.get_first_room()
        else:
            player.room = self.get_room(self.config["startRoom"])

    def get_first_room(self):
        if len(self.rooms) > 0:
            return self.rooms[0]
        raise Exception("Map does not contain a room")
    
    def get_room(self, id):
        for room in self.rooms:
            if room["id"] == id:
                return room
        raise Exception("Room ID not found")
    
    def get_connection(self, id):
        for connection in self.connections:
            if connection["id"] == id:
                return connection
        raise Exception("Connection ID not found")


class player:
    def __init__(self, game, language="en") -> None:
        self.game = game
        self.inventory = []
        self.room = {}
        game.add_player(self)
        self.language = language
        self.translation = game.translations[self.language]

    
    def play(self):
        commands.look.describe_room(self)
        while True:
            text = input("> ")
            parsed = False
            for cmd_class in self.game.all_commands:
                #instatiate command class
                cmd = cmd_class(self)
                try:
                    #try parsing the command
                    if cmd.parse(text):
                        parsed = True
                        break
                except commands.CommandFailedException as ex:
                    print(self.translate(str(ex)))
                    parsed = True
                    break
                except Exception as ex:
                    print("Oops! An Error occured:")
                    print(f"Command: {type(cmd).__name__}")
                    print(ex)
                    parsed = True
                    break
            if not parsed:
                print(self.translate("Hu?"))

    def translate(self, text: str):
        """Translates the text"""
        if text in self.translation:
            return self.translation[text]
        elif text in self.game.translations["en"]:
            # use English as Fallback
            return self.game.translations["en"][text]
        else:
            # use given text, if nothing matches
            return text