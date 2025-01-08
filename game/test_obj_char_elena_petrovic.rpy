# Ren'Py automatically loads all script files ending with .rpy. To use this
# file, define a label and jump to it from another file.


init -998 python:

    portrait = "mc_normal"#"main_character.png"#"main_character_portrait.png
    
    elena = CharWithFeatures("Elena Petrovik",portrait)

    pd = elena.new_group("personal data")

    pd.new_const("mbti", "ISTJ")
    pd.new_const("nationality", "Serbian")
    pd.new_const("sexuality", "Bisexual")
    pd.new_const("date of birth", "17/01/2001")


    li = elena.new_group("likes")

    li.new_const("skate rolling")
    li.new_const("going to skateparls")
    li.new_const("painting")
    li.new_const("her cat")
    li.new_const("order in house")

    di = elena.new_group("dislikes")

    di.new_const("pineapple pizza")
    di.new_const("valentine's day")
    di.new_const("falling in love")
    di.new_const("dirtiness")

    si = elena.new_group("sins")
    si.new_const("pride")



label display_character_with_features_elena_label():
    show screen toggle_character_screen(elena)
    label .loop:
        pause 
    jump .loop   