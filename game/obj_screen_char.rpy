# Ren'Py automatically loads all script files ending with .rpy. To use this
# file, define a label and jump to it from another file.


screen toggle_character_screen():
    #show screen display_character_with_features_screen(mc)
    textbutton "Profile":
        action ToggleScreen("display_character_with_features_screen",None, mc)
        align (0.95, 0.0)


screen features_name_value_screen(features, vi):
    default ys = 165
    hbox:
        viewport:
            id vi
            draggable True
            mousewheel True xysize (550, ys)

            grid 2 len(features) :
                for feature in features:
                    text "[feature.get_name().capitalize()]"
                    if feature.value is not True:
                        text "  [feature.value]":
                            xalign 1.0
                    else:
                        text ""
                         


        vbar value YScrollValue(vi) align (1.0, 0.5) ysize ys




screen display_character_with_features_screen(char):
    style_prefix "default"

    frame:
        align(0.5,0.5)        
        hbox:
            vbox:
                frame:
                    vbox:
                        text "[char.get_name()]"
                            #yalign  0.5
                        add "[char.get_portrait()]"

            vbox:
                for n, group_features in enumerate(char.gui_items()):
                    text "[group_features.get_name().capitalize()]:":
                        xalign 0.5 
                    frame:
                        use features_name_value_screen(group_features.gui_items(), str(n))
            #text "[list(x for x in char.gui_get_feature_groups())]"




init -999 python:

    class ConstFeature:

        def __init__(self,name, value = True):
            self.name = name 
            #self.group = group
            self.value = value 

        def __hash__(self):
            return hash(self.name)

        def get_name(self):
            return self.name 

        def __str__(self):
            if self.value is not None:
                return "{} : {}".format(self.name, self.value )
            else:
                return "{}".format(self.name )

        def __repr__(self):
            return "{} {}".format(self.name, self.value )


    class DynamicFeature(ConstFeature):

        def __init__(self,name,  value, minValue, maxValue, changePerTime):
            super().__init__(name,  value)
            self.minValue = minValue
            self.maxValue = maxValue
            self.changePerHour = changePerHour            

        def pass_time(self,hours):
            change = self.changePerHour
            if change:
                set_value(self.value+change*hours)

        def set_value(self,value):
            self.value = max(self.minValue, min(value,self.maxValue))


    class GroupFeatures(ConstFeature):

        def __init__(self,name):
            super().__init__(name,  True)
            self.unordered = set()
            self.ordered = list()

        def add(self,feature, order = None):
            assert feature not in self.unordered
            self.unordered.add(feature)
            if order is None:                    
                self.ordered.append((feature, len(self.ordered)))
            else:
                self.ordered.append((feature, order))
                self.ordered.sort(key = lambda t: t[1])
        
        def gui_items(self):
            return [t[0] for t in self.ordered]


        def new_const_feature(self,name, value = True, order = None):
            f = ConstFeature(name, value)
            self.add(f, order)
            return f

        def new_dynamic_feature(self,name,  value, minValue, maxValue, changePerTime, order = None):
            f = DynamicFeature(name,  value, minValue, maxValue, changePerTime)
            self.add(f, order)
            return f

    

    class GroupOfGroupFeatures(GroupFeatures):

        def __init__(self,name):
            super().__init__(name)

        def new_group(self,group_name, order = None):
            g = GroupFeatures(group_name)
            self.add(g,order)
            return g






    class GroupsFeatures_Alt:

        def __init__(self):
            self.feature_group_sets = dict()
            self.features_groups_order = list()

        def add_feature_group(self,name,order):
            assert name not in self.feature_group_sets 
            ordered_row = list()
            self.features_groups_order.append((name,order,ordered_row))
            self.features_groups_order.sort(key = lambda t: t[1])
            self.feature_group_sets[name] = set(), ordered_row

        def add_feature(self,feature, order= None):
 
            name = feature.name 
            group = feature.group
            assert group in self.feature_group_sets
            row, ordered_row = self.feature_group_sets[group]  
            assert name not in row 
            row.add(name)

            if order is None:
                order = len(ordered_row)

            ordered_row.append((feature,order))
            ordered_row.sort(key = lambda t: t[1])

        def add_features(self,*features):
            for f in features:
                self.add_feature(f)

        def gui_get_feature_groups(self):
            for name,order,ordered_row in self.features_groups_order:
                yield name.capitalize(), ordered_row


    class CharWithFeatures(GroupOfGroupFeatures):

        def __init__(self, name, portrait):

            super().__init__(name)
            self.portrait = portrait 

        def __str__(self):
            return self.name 


        def get_portrait(self):
            return self.portrait

    
    portrait = "mc_normal"#"main_character.png"#"main_character_portrait.png
    
    mc = CharWithFeatures("Elena Petrovik",portrait)

    pd = mc.new_group("personal data",0)

    pd.new_const_feature("mbti", "ISTJ")
    pd.new_const_feature("nationality", "Serbian")
    pd.new_const_feature("sexuality", "Bisexual")
    pd.new_const_feature("date of birth", "17/01/2001")


    li = mc.new_group("likes",1)

    li.new_const_feature("skate rolling")
    li.new_const_feature("going to skateparls")
    li.new_const_feature("painting")
    li.new_const_feature("her cat")
    li.new_const_feature("order in house")

    di = mc.new_group("dislikes",2)

    di.new_const_feature("pineapple pizza")
    di.new_const_feature("valentine's day")
    di.new_const_feature("falling in love")
    di.new_const_feature("dirtiness")

    si = mc.new_group("sins",3)
    si.new_const_feature("pride")







    #mc.add_feature_group("personal data", 0)

    #mbti = ConstFeature("mbti","personal data", "ISTJ")
    #nationality = ConstFeature("nationality","personal data", "Serbian")
    #sexuality = ConstFeature("sexuality","personal data", "Bisexual")
    #dateOfBirth = ConstFeature("date of birth","personal data", "17/01/2001")

    #mc.add_features(mbti,nationality,sexuality,dateOfBirth)


    #mc.add_feature_group("likes", 1)

    #skate = ConstFeature("skate rolling","likes")
    #skate_going = ConstFeature("going to skateparls","likes")
    #paint = ConstFeature("painting","likes")
    #cat = ConstFeature("her cat","likes")
    #order = ConstFeature("order in house","likes")

    #mc.add_features(skate,skate_going,cat,order)

    #mc.add_feature_group("dislikes", 2)

    #pizza =  ConstFeature("pineapple pizza","dislikes")
    #vale_day =  ConstFeature("valentine's day","dislikes")
    #love = ConstFeature("falling in love","dislikes")
    #dirty = ConstFeature("dirtiness","dislikes")

    #mc.add_features(pizza,vale_day,love,dirty)

    #mc.add_feature_group("sins", 3)

    #pride = ConstFeature("pride","sins")

    #mc.add_features(pride)



label display_character_with_features_label():
    show screen toggle_character_screen()
    label .loop:
        pause 
    jump .loop   




