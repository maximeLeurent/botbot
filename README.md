This software is a Interface that can control players of a online multiplayer game in a semi automatic way (bots).
The goal is to make them boring but necessary jobs and keep the inteligence of work to do.
It's is mostly use to sell/build/buy items of the game.

The players answer to order like : buying items, building new items with a list of ingredient, control the price in a place of selling given by other players, selling my items at a clever price...

The project is compose of :
-A Database :
    that memorizes all the items of the game and their list of ingredient, the previous prices encounter, the time used to sell them etc.
    It's made with the librairy "sqlalchemy"
- a GUI:
    Provide a usefull interface to think and take rapidly good decision, and send orders to players. It's display information from the database, from the game and previous note made by myself.
    It's made with the librairy "PyQt5"    
- a Control command system:
    Receive order from the GUI and dispachs them to one player. Controls the players in the game by simulatic a human normal behaviour (click, typing etc). Analyse image of the game to ride up information to GUI and the database.
    It's made with the lirairy "multhreading" and ..
