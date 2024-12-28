# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Elena",who_color = "#f0f")

image bg_rainy_street = "bg/rainy_street.png"
image bg_raindrops = Transform("bg/raindrops.png", blend = "multiply")
image mc_normal = "main_character2.png"

#The default blend modes this supports are "normal", "add", "multiply", "min", and "max".

transform multiply:
    blend "multiply"

transform slightleft:
    xalign 0.33
    yalign 1.0

#methods with images : image , show, scene, hide 

#layers : master transient screens overlay

# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg_rainy_street
    #show bg_raindrops at multiply onlayer screens
    show bg_raindrops onlayer screens
    show screen toggle_character_screen()

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show mc_normal at slightleft

    # These display lines of dialogue.

    e "You've created a new Ren'Py game."

    e "Once you add a story, pictures, and music, you can release it to the world!"

    # This ends the game.

    return
