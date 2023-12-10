from microbit import *

# Define the possible health levels. Level 5 means
# full health (show full heart), level 0 means death
# (show blank screen).
class HealthLevel:
    FULL = 5
    DMG_80 = 4
    DMG_60 = 3
    DMG_40 = 2
    DMG_20 = 1
    DEAD = 0

# Define the pixel graphic of the full heart, line by
# line. LEDs are all set to brightness level 7 out of 9.
_heart = [
    '07070',
    '77777',
    '77777',
    '07770',
    '00700'
]

# Define a function that creates the health indicator image
# based on a given health level. Assemble the image top to
# bottom.
def _create_health_indicator(health):
    # We have no lines yet.
    lines = []

    # How many blank lines do we need to draw at the top, before
    # we start drawing lines of the heart image? That depends: for
    # health level 5, we need all five heart lines, so no blanks.
    # For health level 3, we need three heart lines at the bottom,
    # which means two blanks at the top. And so on, and so forth.
    # There are five lines in total. The number of heart lines is
    # equal to the health level. So, the number of blanks is 5 minus
    # the health level.
    number_of_blank_lines = 5 - health

    for i in range(0, 5): # We need to draw 5 lines, 0 to 4.
        # i goes through values 0 to 4. If, for example,
        # number_of_blank_lines is 2, that means we should draw a
        # blank line for i=0 and i=1 (so we have two blank lines).
        # Once i reaches 2, we can start drawing heart lines.
        should_draw_blank_line = i < number_of_blank_lines

        # Draw a blank line ('00000') or a heart line, depending on
        # our decision from before.
        lines.append('00000' if should_draw_blank_line else _heart[i])

    # Right now, our image is a list of lines. However, the Image()
    # function wants it to be a single string, with lines separated
    # by a ':'. So, ':'.join(lines) takes our list of lines, puts
    # all entries into a single string, and separates the entries
    # with a ':'. We can then pass that string into the Image()
    # function, which results in something that we can display on
    # our screen.
    return Image(':'.join(lines))

# Define a function that prints the health indicator to the screen.
def show_health(health):
    # Create the health indicator and print it to the screen.
    display.show(_create_health_indicator(health))
