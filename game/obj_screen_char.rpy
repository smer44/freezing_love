
#Button what toggles display_character_with_features_screen  screen
screen toggle_character_screen(obj, ys = 165):
    #show screen display_character_with_features_screen(mc)
    textbutton "Profile":
        action ToggleScreen("display_character_with_features_screen",None, obj,ys)
        align (0.95, 0.0)


#Shows GroupEntities 
screen features_name_value_screen(features, vi, ys = 165):
    #default ys = 165
    hbox:
        viewport:
            id vi
            draggable True
            mousewheel True xysize (550, ys)

            grid 2 len(features) :
                for feature in features:
                    text "[feature.get_name().capitalize()]"
                    if feature.get_displayed_value() is True:
                        #if it is true, it is a marker of an entity "without" a value - like the entity "just exists".
                        text ""
                    else:
                        text "  [feature.get_displayed_value()]":
                            xalign 1.0

                        
        vbar value YScrollValue(vi) align (1.0, 0.5) ysize ys



#Shows GroupOfGroupEntities and  CharWithFeatures
screen display_character_with_features_screen(char,ys = 165):
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
                for n, group_features in enumerate(char.values()):
                    text "[group_features.get_name().capitalize()]:":
                        xalign 0.5 
                    frame:
                        use features_name_value_screen(group_features.values(), str(n), ys)
            #text "[list(x for x in char.gui_get_feature_groups())]"




init -999 python:

    class GameEntity:
        """
        Basic class of any model entity in game, what has its name and value 
        """

        def __init__(self,name, value = True):
            self.name = name
            self.value = value 
            

        def __hash__(self):
            return hash(self.name)

        def get_name(self):
            return self.name 

        def get_value(self):
            return self.value

        def get_displayed_value(self):
            return self.get_value()

        def tick(self,ticks):
            #Do not change with time
            msg = f"GameEntity {self.name} tick SKIPPED"
            log.append(msg)
            pass 

        def __str__(self):
            if self.value is not None:
                return f"{self.name} : {self.value}"
            else:
                return f"{self.name}"

        def __repr__(self):
            return f"{self.name} : {self.value}"

    
    class InfluencedEntity(GameEntity):
        '''
        BAsic class of an entity, what is influenced from 
        another entity, so its modified value must be recalculated.
        Also this entity influences on its children.
        The influence function fn(value, other_value)
        takes 2 args - value of current function and other_value and returns resulting 
        value, what is set into modified value
        Currently, influence modifies the value.
        So as this entity is updated, the update function for all its children is called.
        '''
        def __init__(self,name, value):
            super().__init__(name,  value)
            self.modified_value = value 
            self.influences_list = []
            self.influences_dict = dict()
            self.children_dict = dict()


        def get_value(self):
            return self.modified_value

        def add_influence(self, other, fn):
            assert other.get_name() not in self.influences_dict
            assert self.get_name() not in other.children_dict

            self.influences_list.append((other,fn))
            self.influences_dict[other.get_name()]= (other, fn)
            other.children_dict[self.get_name()] = self

        
        def update_value(self):
            value = self.value 
            for other, fn in self.influences_dict.items():
                value = fn(value, other.get_value())
            self.modified_value = value 
            self.__update_children__()

        def __update_children__(self):
            for child_name, child in self.children_dict.items():
                child.update_value()







    class InfluenceConsumerBySingleEntity(GameEntity):
        '''
        Entity, what gets influence by some game entity, 
        but do not influence on any other entities.
        '''    

        def __init__(self,name, value, influence, fn):
            super().__init__(name,  value)
            assert isinstance(influence,GameEntity), f"{self}: __init__ with wrong {influence=} "
            self.modified_value = value 

            self.set_influence(influence,fn)



        def get_value(self):
            return self.modified_value
        
        def set_influence(self,other, fn):
            self.influence = other
            self.fn = fn
            assert self.get_name() not in other.children_dict
            other.children_dict[self.get_name()] = self
            self.update_value()
        
        def update_value(self):
            self.modified_value = self.fn(self.value, self.influence.get_value())
            #log.append(f"InfluenceConsumerBySingleEntity {self.name} : after update_value : {self.modified_value}")



    log = []

    class InfluenceConsumerEnum(InfluenceConsumerBySingleEntity):

        def __init__(self,name,influence, *names_and_numbers):
            super().__init__(name,  names_and_numbers,influence,ranges_to_name)




    def ranges_to_name(names_and_ranges, value):
        first_name, prev_number = names_and_ranges[0] 
        if value < prev_number:
            return first_name

        for name, number in names_and_ranges[1:]:
            if prev_number <= value < number:

                return name

        return names_and_ranges[-1][0]



        #def __str__(self):
        #    return "f{self.name} : {self.get_displayed_value() }"

        #def __repr__(self):
        #    return "f{self.name} : {self.get_displayed_value() }"


    class DynamicEntity(GameEntity):

        def __init__(self,name,  value, minValue, maxValue, changePerTick):
            super().__init__(name,  value)
            self.minValue = minValue
            self.maxValue = maxValue
            self.changePerTick = changePerTick            

        def tick(self,ticks):
            change = self.changePerTick           
            
            self.set_value(self.value+change*ticks)
            #msg = f"DynamicEntity {self.name} tick with value after set_value : {self.get_displayed_value()}"
            #log.append(msg)
            

        def set_value(self,value):
            log.append(f"DynamicEntity set_value called")
            self.value = max(self.minValue, min(value,self.maxValue))

        def get_name_debug(self):
            return f"{self.value} ,{self.minValue} ,{self.maxValue}"


    class InfluenceProducerEntity(DynamicEntity):
        '''
        Dynamic entity (has is sence to have static entity here?, what influences on something
        but not experience influence from other entities
        '''

        def __init__(self,name, value, minValue, maxValue, changePerTime):
            super().__init__(name,  value, minValue, maxValue, changePerTime)
            self.children_dict = dict()

        def set_value(self,value):
            
            self.value = max(self.minValue, min(value,self.maxValue))
            
            self.__update_children__()
            #log.append(f"InfluenceProducerEntity set_value called after __update_children__")


        def __update_children__(self):
            #children_dict is empty 
            msg = f"InfluenceProducerEntity __update_children__ for {self.children_dict.items()}"
            log.append(msg)
            for child_name, child in self.children_dict.items():
                msg = f"InfluenceProducerEntity update value called for {child}"
                child.update_value()



            






    class GroupEntities(GameEntity):
        '''
        Represents group of entities.
        Is a container of value what is ordered dict with entities.
        For now, GroupEntities should be not dynamic entity itself,
        instead make reference with 
        '''

        def __init__(self,name):
            super().__init__(name,  OrderedDict())


        def append(self,feature):
            self.value.append(feature)

        
        def values(self):
            return self.value.values()


        def new_const(self,name, value = True, order = None):
            f = GameEntity(name, value)
            if order is not None:
                self.add(f, order)
            else:
                self.append(f)
            return f

        def new_prod(self,name,  value, minValue, maxValue, changePerTime, order = None):
            f = InfluenceProducerEntity(name,  value, minValue, maxValue, changePerTime)
            if order is not None:
                self.add(f, order)
            else:
                self.append(f)
            return f


        def new_enum(self,name,influence,*names_and_numbers):
            f = InfluenceConsumerEnum(name,influence,*names_and_numbers)
            self.append(f)
            return f

        def new_influenced(self,name,value):
            f = InfluencedEntity(name, value)
            self.append(f)
            return f


        def new_dynamic(self,name,  value, minValue, maxValue, changePerTime, order = None):
            f = DynamicEntity(name,  value, minValue, maxValue, changePerTime)
            if order is not None:
                self.add(f, order)
            else:
                self.append(f)
            return f

        def tick(self,ticks):
            msg = f"GroupEntities {self.name} tick called "
            #msg = f"GroupEntities {self.name} tick called for values = {self.values()}"
            #ERROR IS IN self.values()
            log.append(msg)
            for entity in self.values():
                log.append(f"- - - {entity=}")

                entity.tick(ticks)

    

    class GroupOfGroupEntities(GroupEntities):

        def __init__(self,name):
            super().__init__(name)

        def new_group(self,group_name):
            g = GroupEntities(group_name)
            self.append(g)
            return g




    class CharWithFeatures(GroupOfGroupEntities):

        def __init__(self, name, portrait):

            super().__init__(name)
            self.portrait = portrait 

        def __str__(self):
            return self.name 


        def get_portrait(self):
            return self.portrait

    





