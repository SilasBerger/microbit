import music

# Note representation: "c4:3" represents the note C4, played
# for 3 time units.

def play_hit_sound():
    tones = ['f#4:1', 'e5:1', ':4', 'f#4:1', 'e5:1', ':4', 'f#4:1', 'e5:1', ':4']
    music.set_tempo(bpm=480)
    music.play(tones)

def play_death_sound():
    tones = ['b3:1', 'f4:1', ':1', 'f4:1', 'f4:1', 'e4:1', 'd4:1', 'c4:3']
    music.set_tempo(bpm=120)
    music.play(tones)
