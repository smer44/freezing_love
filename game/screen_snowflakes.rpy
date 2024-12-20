# Ren'Py automatically loads all script files ending with .rpy. To use this
# file, define a label and jump to it from another file.

default snowflakes = ["sfx/snowflake.png", "sfx/snowflake2.png", "sfx/snowflake3.png"]

        

transform snowflake_ani(xya):
    #$ypos = renpy.random.random()
    align xya
    
    easein 5.0*(1.1-xya[1]) align ( xya[0] + (renpy.random.random()-0.5)*0.3, 1.1)
    yalign -0.1 
    block:
        easein 5.0*(1.2) align ( xya[0] + (renpy.random.random()-0.5)*0.3, 1.1)
        yalign -0.1
        repeat 





screen snowflakes(amount):
    default xya = tuple((renpy.random.random(),renpy.random.random()) for _ in range(amount))

    fixed:
        for n in range(amount):
            add snowflakes[n %len(snowflakes)]:
                at snowflake_ani(xya[n])
                size 40,40
            



label test_snowflakes():
    show screen snowflakes(100)
    "woho"
    "second"
