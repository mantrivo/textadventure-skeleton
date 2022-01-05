# Textadventure sceleton written in python

Use with a map file generated on https://www.trizbort.io

Use the following Sockets for walking directions:
```
 nw         n   up    ne
    x---0---x---x---x
    0               0
  w x               x e
    0               0
    x---0---x---x---x
 sw         s  down   se
```
0: Socket not in use. You can still use one of these to enter a room, but it is not possible to exit the room via this socket. However it is recommanded to mark the connector as oneway for readability.

Execute the file `play.py` to start a game.

## Command Parsing
The Command parsing is handled in a Command Base Class. The action words are taken from the translation file. It is also possible to provide regex parsing or even overwriting the parsing in a command child class.

Every command is a child of the Base Class. If the player enters a command, all command classes try to parse the input. The first command wich successfully parses the textinput will be executed.

By now, the parser supports the following commands:
- go
- look
- take
- drop
- inventory

## Localisation
The localisation is provided in a json file. It needs to have the following directory mapping:
- "generic_fills": list of articles
- "commands": dictionary of commands
    - "-command class name-": directory of command values
        - "action": list of action words of the command
        - "action_regex": (optional) list of regex parsing
        - "filler": (optinal) list of fillers of the command
        - more command specific values. (eg. direction mapping for the go command)
- "all": list of words translating to all
- "-your text-": your translation

Example:
```
{
    "generic_fills": [
        "the",
        "this",
        "a"
    ],
    "commands": {
        "go": {
            "action": [
                "go",
                "goto"
            ],
            "filler": [
                "to"
            ],
            "directions": {
                "n": 0,
                "north": 0,
                "ne": 2,
                "northeast": 2,
                "...": 4
            }
        }
    },
    "all": ["all", "everything"],
    "no way": "There is no way in this direction"
}
```