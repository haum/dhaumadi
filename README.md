# dhaumadi
Code of dHaumadi project

The dhaumadi project is a Simon Says game engineered to be set up in a wooden geodesic
dome. The game is designed to force collaboration between players to replay the sequence
by using a human-sized dome that nobody can master alone.

## Installing & Running

To setup a new instance:

1. Install Python 3.6+
2. Install Fluidsynth and a soundfont
3. Install pySerial
4. Clone this repo

	$ git clone https://github.com/haum/dhaumadi.git
	$ cd dhaumadi
	$ git submodule init
	$ git submodule update

To run the game:

1. Start fluidsynth in server mode:

	$ fluidsynth --server -a alsa /usr/share/sounds/sf2/FluidR3_GM.sf2

2. Start the serial bridge and pipe its output to the game script:

	$ ./dhaumadi.py | ./game/game.py


More info (fr) : https://pad.aumbox.fr/p/20170802_Teriaki2017

