# Imports go at the top
from microbit import *
import music

# Code in a 'while True:' loop repeats forever
while True:
    print('Available songs: nyan, blues, funeral')

    # Ask the user for their song choice, store the result in a variable.
    song_choice = input('What song would you like to play? ')

    # Play a song based on their choice...
    if song_choice == 'nyan':
        music.play(music.NYAN)
    elif song_choice == 'blues':
        music.play(music.BLUES)
    elif song_choice == 'funeral':
        music.play(music.FUNERAL)
    else:
        # ...or let them know if it's not available.
        print('Sorry, that song is not available.')

    # Print an empty line to add some space.
    print()
