#!/usr/bin/env python3

from strfabric import StrFabric
from strategy import Worker

strFabric = StrFabric()
worker = Worker(strFabric.getFunction('FileInput'))

def interactiveConsole():
    while True:
        user_input = input(f"Input strategy name (-s {strFabric.availableFunctionsNames()}) or command. Input exit or quit for exit\n").strip()

        if user_input.lower() in ("exit", "quit"):
            break

        tokens = user_input.split(maxsplit=1)

        if len(tokens) == 2 and tokens[0] == '-s':
            name = tokens[1]
            if name in strFabric.availableFunctionsNames():
                print(f"set strategy name in {name}\n")
                worker.setStrategy(strFabric.getFunction(name))
            else:
                print(f"there is no strategy name: {name}\n")

        else:
        	worker.exec(user_input)

interactiveConsole()
