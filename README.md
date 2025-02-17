# dmxPong
Play Pong on movie lights with Python and OLA!
<b>dmxPong Readme</b>

Thanks for checking out dmxPong! This code still needs some work, mainly around edge cases where the framerate drops so much the ball flies out of bounds, but as long as your hardware can maintain a good framerate it seems to work without issue.

<b>Setup</b>

This script requires Python (and pyGame and numPy, which normally comes with Python. Install them if you need to) as well as OLA to handle the dmx output. OLA works on Mac and Linux, if you have Windows, spin up a virtual Linux box.

https://www.openlighting.org/ola/getting-started/downloads/

Once OLA is installed, it will begin serving a webpage at yourip:9090 . You can use this page to configure OLA. To begin, click add universe. Here you can set the number of the universe just like a console and label it. After that, select the type of protocol you'd like to use. This will probably be ArtNet or E1.31(sACN) but you can also output to a physical dmx dongle if you have that configured. Click add universe.

OLA is now set up to start sending data over your preferred protocol to your transmitter.

<b>Settings in the Script</b>

Before you run the script for the first time, you need to edit the variable "universe" on line 55 to reflect the universe you just configured in OLA. It defaults to 2 because that's what I was using for testing.

While you're in the script you can also change the size of your pixel array with the "pxlWidth"(number of fixtures) and "pxlHeight"(pixels per fixture) on lines 41 and 42. I've started an 8x16 grid with a box of Titans in RGB 16px mode as the default setup, but the game should scale to any array with 170 pixels or less(width*height) (1 universe of dmx).

You can also ajust the following variables to effect gameplay:

ballSpeed on line 31 controls the speed of the ball
paddleVel on line 33 controls the speed of the player's paddles
AILVL on line 53 controls the difficulty of the computer player in 1 player mode. This should be a number from 1-100 where 1 will lose every game and 100 is unbeatable. Season to taste

You can add custom colors by adding new variables under line 21. These should be r,g,b values from 0-255. AKA your color from the console.

Once you've added colors or not, you can choose which colors are applied to which objects when we build the dmx packet from line 200-225. There are 3 types of rendered objects, 1 is Player 1's paddle, 2 is Player 2's paddle, and 3 is the ball. You can set the colors by changing what dmx color they reference in this section. All other possibilities will render black as they're used for internal calculation, not displayed to the player.

<b>Playing the Game</b>

After configuring you can run the script. A window with the game's menu will appear and the script will start outputting dmx. 

Once it's running, select 1 or 2 player mode using the Left and Right arrow keys and press Return to select the mode which will start the game.

When the game starts, or after a point, press Space to serve the ball and start the next point.

Player 1's paddle is controlled with the Up and Down arrow keys, and Player 2's paddle is controlled with W and S.

The numbers control the intensity of your lights with 1 being 10% and 0 being full.

Escape quits the game.

I have yet to enable any kind of winning or losing conditions, so play to whatever score you want. I also haven't put in a way to loop back to the menu so if you want to change from 1 player to 2 player or restart the game you need to restart the whole program.

That's about it. If you have any questions feel free to dm me. Have fun playing! 
