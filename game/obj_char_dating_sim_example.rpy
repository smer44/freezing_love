# Ren'Py automatically loads all script files ending with .rpy. To use this
# file, define a label and jump to it from another file.

init -998 python:


    portrait = "mc_normal"#"main_character.png"#"main_character_portrait.png

    test_char = CharWithFeatures("Elena Petrovik",portrait)

    cond = test_char.new_group("Conditions")

    cond_names = "Hunger Sleepy Bladder Sadness Tired Hygiene Drunk".split()

    conds = [cond.new_prod(c_name, 0,0,100,n+1) for n, c_name in enumerate(cond_names)]

    influenced_cond = test_char.new_group("Influenced Conditions")


    test_enum =influenced_cond.new_enum("HungerStateStr",conds[0], ("Full",30),( "Hungry a bit", 60), ("VeryHungry",90), ("Starving",95))

    sleep_int = influenced_cond.new_enum("SleepStateInt",conds[1], (0,20),( 1, 50), (2,90))

    influenced_cond.new_enum("DrunkState",conds[6], ("Sober",20),( "Warm", 40), ("CanNotStand",60), ("FullyVasted",80),)

    #How to write complicated influence:
    # lets create complicated formula, like
    #, canStand is influenced as 0 + (Drunk /2 + Hunger/4)*(sleep_int + 0.5)
    #and it must be less then 50 so character can stand.

    # This is described as:


    #aha, is has no children dict because it is a consumer.
    # I need to think how to refactor it

    #canStand = influenced_cond.new_influenced("CanStand",0)

    #canStand.add_influence(conds[6], lambda value,other_value : value + other_value /2)

    #canStand.add_influence(conds[0], lambda value,other_value : value + other_value /4)

    #canStand.add_influence(sleep_int, lambda value,other_value : value * (other_value+ 0.5))



    #test_enum = InfluenceConsumerEnum("HungerState",conds[0], ("Full",30),( "Hungry a bit", 60), ("VeryHungry",90), ("Starving",95))



screen obj_debug_screen(obj):
    text "[obj]"

screen log_screen(lines):
    hbox:
        viewport:
            id "log_mgs"
            draggable True
            mousewheel True xysize (1820, 1080) 
            vbox:
                for line in lines:
                    text "[line]"

        vbar value YScrollValue("log_mgs") align (1.0, 0.5) ysize 1080    
        


label display_character_with_features_test_label():
    show screen toggle_character_screen(test_char,350)
    #show screen obj_debug_screen(test_enum)
    show screen log_screen(log)
    label .loop:
        menu:
            "Time not passed":
                pass 
            "Time passed":
                $test_char.tick(1)
                #update is not caled?
        pause 
    jump .loop   




