# dhaumadi
Code of dHaumadi project

Infos ici: https://pad.aumbox.fr/p/20170802_Teriaki2017


dHaumadi est un jeu collaboratif géant.

Sous un dôme en bois, des lumières s’animent et il faut reproduire l’enchaînement sans se tromper : relèverez-vous le défi avec nous ?

C'est un jeu du Simon géant (l'espèce de cylindre plat avec quatre gros boutons colorés et qui t'invite à reproduire la séquence de touches qu'il te montre en l'étoffant de plus en plus) sauf que là, c'est adapté au dHAUM pour être à taille humaine et obliger les joueurs à travailler en équipe.

# installation et utilisation

installer python3.6 (par exemple avec https://github.com/pyenv/pyenv )
installer fluidsynth

$ git clone https://github.com/haum/dhaumadi.git
$ cd dhaumadi
$ git submodule init
$ git submodule update

demarage de fluidsynth en mode serveur 

$ fluidsynth --server -a alsa /usr/share/sounds/sf2/FluidR3_GS.sf2

demarrage du jeu en mode console

$ ./game/game.py

