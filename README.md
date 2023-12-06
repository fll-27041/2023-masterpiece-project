# 2023-masterpiece-project
Team Thought Process group project

## Overview

This is the team project for FIRST Lego League team #27041 "Thought Process" for the 2023 "Masterpiece".  This year the team decided to learn about programming a video game in Python, building a custom PCB chip, and writing the code to interface the software and hardware.

This repository is intended to be run on a rasperry pi that the team built.  The program simulates a 2023 FLL robot game board.  Players can drive a virtual lego robot around the board.

To help learn how to program a lego robot using python, the program will show the python code similar to the moves the robot is making on screen.

Special keys:

* g       - Toggle grid display
space   - begin recording moves or stop recording
w,a,s,d - drive robot around

The program uses the bottom six pins of the 40-pin GPIO connector on a raspberry pi 4 to control a custom printed circuit board.  When the player clicks on grids on the board, the corresponding square on an 8x4 grid of LEDs will be lit up.
