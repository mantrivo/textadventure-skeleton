import re


class CommandFailedException(Exception):
    """Condition for command execution not valid"""
    pass


class command:
    """Command Base Class. Only use clid classes."""
    def __init__(self, player) -> None:
        self.player = player
        self.action = []
        self.action_regex = []
        self.filler = []

        t = player.translation["commands"][type(self).__name__]
        if "action" in t:
            self.action = t["action"]
        if "action_regex" in t:
            self.action_regex = t["action_regex"]
        if "filler" in t:
            self.filler = t["filler"]
    
    def parse(self, text):
        """Parse the text input. Returns True if successfull."""
        text = text.lower()
        split = self._remove_filler(text).split()
        if len(split) == 0:
            # incomplete/ invalid
            return False
        elif split[0] in self.action:
            # action-word and optional arguments
            return self.execute(text, args=split[1:])
        for expression in self.action_regex:
            # parsing regular expressions with optional arguments
            match = re.match(expression, text)
            if match:
                return self.execute(text, args=match.groups())
        return False
    
    def execute(self, text, **args):
        return False

    def _remove_all(self, text, remove):
        #if not " " in text:
        #    return text
        
        split = text.split()
        for r in remove:
            if r in split: split.remove(r)
        return " ".join(split)
    
    def _remove_filler(self, text):
        return self._remove_all(text, self.filler)


class go(command):
    def __init__(self, player) -> None:
        super().__init__(player)

        self.directions = player.translation["commands"]["go"]["directions"]
        
    
    def parse(self, text: str):

        text = text.lower()
        player = self.player
        game = player.game
        text = self._remove_filler(text)
        split = text.split()
        #match
        if split[0] in self.action:
            #validate
            if not split[1]:
                raise CommandFailedException("where?")
        elif text in self.directions:
            pass
        else:
            return False
        
        #execute
        if text in self.directions:
            direction = self.directions[text]
        elif split[1] in self.directions:
            direction = self.directions[split[1]]
        else:
            raise CommandFailedException("no direction")
            
        return self.go(direction)
        
    
    def go(self, direction):
        player = self.player
        game = player.game
        success = False
        for con in player.game.connections:
            if con["_dockStart"] == player.room["id"] and \
                con["_startDir"] == direction:
                    player.room = game.get_room(con["_dockEnd"])
                    success = True
                    break
            elif con["_dockEnd"] == player.room["id"] and \
                con["_endDir"] == direction and \
                not con["_oneWay"]:
                    player.room = game.get_room(con["_dockStart"])
                    success = True
                    break
        if not success:
            raise CommandFailedException("no way")
        
        if con["_name"] != "":
            print(con["_name"])
        
        look.describe_room(player)
        return success


class look(command):
    def execute(self, text: str, args=[]):
        if len(args) == 0:
            self.describe_room(self.player)
        else:
            object_found = False
            for object in self.player.room["objects"]:
                if args[0] == object["_name"].lower():
                    print(object["_description"])
                    object_found = True
                    break
            if not object_found:
                raise CommandFailedException("Object not found")
        
        return True

    @staticmethod
    def describe_room(player):
        room = player.room
        if room["_description"]: 
                print(room["_description"])
        else:
            print(player.translate(room["_name"]))
        
        if room["objects"]:
            print("\n" + player.translate("There is"))
            for object in room["objects"]:
                print(player.translate(object["_name"]))


class take(command):
    def execute(self, text: str, args=[]):
        if len(args) == 0:
            raise CommandFailedException("What?")
        object_found = False
        if args[0] in self.player.translate("all"):
            #take all
            for object in list(self.player.room["objects"]):
                self.player.inventory.append(object)
                self.player.room["objects"].remove(object)
            return True

        for object in self.player.room["objects"]:
            if args[0] == object["_name"].lower():
                #take item
                self.player.inventory.append(object)
                self.player.room["objects"].remove(object)
                object_found = True
                break
        if not object_found:
            raise CommandFailedException("Object not found")
        return object_found


class drop(command):
    def execute(self, text: str, args=[]):
        if len(args) == 0:
            raise CommandFailedException("What?")
        #execute
        object_found = False
        for object in self.player.inventory:
            if args[0] == object["_name"].lower():
                self.player.room["objects"].append(object)
                self.player.inventory.remove(object)
                object_found = True
                break
        if not object_found:
            raise CommandFailedException("Object not found")
        return object_found


class inventory(command):
    def execute(self, text: str, args=[]):
        if not len(self.player.inventory):
            print(self.player.translate("You have nothing in your pockets."))
            return True
        
        print(self.player.translate("You have the following in your pockets:"))
        for object in self.player.inventory:
            print(self.player.translate(object["_name"]))
        
        return True