
#default calender_entry_width = config.screen_width //9
#default calender_entry_short_height = config.screen_height //9
#default calender_entry_full_height = int(config.screen_width /3.5)

# Do not fuse calender_entry_screen and calender_entry_long together !
screen calender_entry_screen(title=None, texts= None , long_cell_rect = None):

    default k = 12 
    default width = config.screen_width //9
    default height = config.screen_height //9   

    #if both are none, display empty screen:
    if  texts is None:     
        frame:
            #style "empty"
            xysize (width, height)
            add Solid("#111a",xsize=width-k, ysize=height-k)
            if title:
                text "[title]"
    else:
        frame:
            modal True
            xysize (width, height)
            #pos xy 
            imagebutton:
                idle Solid("#111a",xsize=width-k, ysize=height-k)
                hover Solid("#235a",xsize=width-k, ysize=height-k)
                action ToggleScreen("calender_entry_long", None,title,texts,long_cell_rect  )
            vbox:
                text "[title]"
                for day_entry in texts[:2]:
                    text "[day_entry.str_time()] [day_entry]" style  "small_calender_entry_text"
                    #text "[type(day_entry)] [day_entry]"
                if len(texts)>2:
                    text "..." style  "small_calender_entry_text"


style small_calender_entry_text:
    size config.screen_height //50


screen calender_entry_long(title,texts,long_cell_rect):
    $ x,y,w,h = long_cell_rect

    frame:
        imagebutton:
            idle Solid("#000a")
            action Hide("calender_entry_long")
        modal True
        xysize (w,h)
        pos (x,y)
        #ypadding 20
        vbox:
            xalign 0.5
            yoffset 20
            spacing 10
            #style  "small_calender_entry_text"
            #text "[title]"
            for day_entry in texts:
                frame:
                    #xalign 0.5
                    #padding (20,22)
                    vbox:
                        spacing 15
                        #xalign 0.5
                        hbox:
                            xsize w*0.9
                            #xalign 0.5
                            text day_entry.str_time() + " - " + day_entry.str_end() style  "small_calender_entry_text":
                                at transform:
                                    xalign 0.2                    
                            text "[day_entry]" style  "small_calender_entry_text":
                                at transform:
                                    xalign 0.3

                        text day_entry.msg style  "small_calender_entry_text":
                                at transform:
                                    xalign 0.5
                                       
                #text "[text]" style  "small_calender_entry_text"




style calender_header_text:
    size config.screen_height //9
    color "#09f"


style calender_header_textbutton:
    size config.screen_height //9
    color "#777"
    hover_color  "#7bf"
    selected_color "#fff"
    xcenter 0.5


screen calender(cal_obj):
    default calender_entry_width = config.screen_width //9             
    default calender_entry_short_height = config.screen_height //9 
    
    default calender_entry_full_height = int(config.screen_width /3.5)
    default highest_cell_ypos = config.screen_height - calender_entry_full_height
    frame:
        #align 0.5,0.5
        pos calender_entry_width, calender_entry_short_height
        vbox:
            frame:
                style "empty"
                xysize (calender_entry_width*7, calender_entry_short_height)
                textbutton "<":
                    yalign 0.5
                    text_style "calender_header_textbutton"
                    action Function(cal_obj.to_prev_month)
                
                text "[cal_obj.year] [cal_obj.month]":
                    yalign 0.5
                    style "calender_header_text"
                    xalign 0.5
                textbutton ">":
                    yalign 0.5
                    text_style "calender_header_textbutton"
                    xalign 1.0
                    action Function(cal_obj.to_next_month)                     

            hbox:
                for day_of_week_name in cal_obj.day_of_week_names:
                    frame:                        
                        xsize calender_entry_width
                        text day_of_week_name:
                            xalign 0.5
            #text " cells: [7*cal_obj.gui_rows_amount()], first_empty [cal_obj.first_day_of_week] , loop_end: [cal_obj.days_amount]"
            grid 7 cal_obj.gui_rows_amount():
                    #use calender_entry_short((day_of_week_name,), (0,0))
                for day_nr in range(0,cal_obj.first_day_of_week):
                    use calender_entry_screen()
                for day_nr in range(1, cal_obj.days_amount+1):
                    $ cell_entries = cal_obj.get_day_entries(day_nr)
                    #this are coordinates of full size component
                    $ long_cell_xy = cal_obj.gui_cell_xy_pos(day_nr,calender_entry_width, calender_entry_short_height, highest_cell_ypos)
                    $ long_cell_rect = *long_cell_xy,calender_entry_width*2,calender_entry_full_height
                    #if cell_entries:
                    use calender_entry_screen(day_nr, cell_entries,long_cell_rect)
                    #use calender_entry_screen((0,0), cell_title, cell_entries)
                




init -999 python:

    class CalenderDay:

        def __init__(self,*entries):
            self.entries = []
            self.add(*entries)

        def add(self,*entries):
            self.entries.extend(entries)
            self.entries.sort()

        def get_entries(self):
            return self.entries

        def __iter__(self):
            return iter(self.entries)

        def __getitem__(self,n):
            return self.entries[n]

        def __len__(self):
            return len(self.entries)




    def add_minutes(h,m,am):
        m = m + h*60 + am 
        d = m//1440 
        h = m//60 
        m = m%60 
        return d,h,m 

    class DayTimeMinutesEntry:

        def __init__(self,name,msg, hour,minute, duration_minutes):
            assert isinstance(name, str) and isinstance(msg,str) , "DayTimeMinutesEntry.__init__ : wrong {name=} or {msg=}"
            self.name = name 
            self.msg = msg 
            self.hour = hour
            self.minute = minute
            self.daytime = hour * 60 + minute
            self.duration_minutes = duration_minutes


        def str_end(self):
            d,h,m = add_minutes(self.hour,self.minute,self.duration_minutes)
            return f"{h}:{m}"

        def str_time(self):
            return f"{self.hour}:{self.minute}"


        def __str__(self):
            return self.name

        def __gt__(self,other):
            return self.daytime.__gt__(other.daytime)

        def __lt__(self,other):
            return self.daytime.__lt__(other.daytime)        

        def __ge__(self,other):
            return self.daytime.__ge__(other.daytime)

        def __le__(self,other):
            return self.daytime.__le__(other.daytime)  





    class CalenderMonth:

        day_of_week_names = "Sunday Monday Tuesday  Wednesday Thursday Friday Saturday".split()
        month_with_30_days = {"April", "June", "September", "November"} 
        month_day_of_week_marker = {"January" :1,
                                    "February":4,
                                    "March":4,
                                    "April":0,
                                    "May":2,
                                    "June":5,
                                    "July":0,
                                    "August":3,
                                    "September":6,
                                    "October":1,
                                    "November":4,
                                    "December":6
                                    }
        month_number               = {"January" :1,
                                    "February":2,
                                    "March":3,
                                    "April":4,
                                    "May":5,
                                    "June":6,
                                    "July":7,
                                    "August":8,
                                    "September":9,
                                    "October":10,
                                    "November":11,
                                    "December":12
                                    }
        month_names_from_number = {v:k for k,v in month_number.items() }

        sakamoto_table = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]


        def __init__(self,year,month):
            self.reset(year,month)
            self.days = dict()


        def reset(self,year,month):
            assert month in CalenderMonth.month_day_of_week_marker, "CalenderMonth : wrong month :" + str(month)
            self.year = int(year)
            assert self.year > 1752 
            self.month = month
            
            self.is_leap_year = self.calc_leap_year()
            self.days_amount = self.calc_days_of_month()
            self.first_day_of_week = self.calc_months_first_day_of_week()

        def add_day(self,number,calenderDay):
            self.days[number] = calenderDay

        def get_day_entries(self,day_number):
            return self.days.get(int(day_number),None)
        
        def calc_leap_year(self):
            year = self.year
            return (year % 100 != 0 and year % 4 == 0 ) or (year % 400 == 0)


        def calc_days_of_month_alt(self):
            year = self.year#
            month = self.month
            if month in CalenderMonth.month_with_30_days:
                return 30 
            elif month == "February":
                if  self.is_leap_year:
                    return 29 
                else :
                    return 28 
            else:
                return 31 

        def calc_days_of_month(self):
            m = self.month_number[self.month]
            if m == 2:
                return 28+self.is_leap_year
            return 30 + (m+ (m > 7)) %2


        def calc_months_first_day_of_week_alt(self):
            #as in https://www.almanac.com/how-find-day-week
            #but works wrong
            last_two_digits_of_year_div_4 = (self.year % 100) //4 
            day_of_week = last_two_digits_of_year_div_4 + CalenderMonth.month_day_of_week_marker[self.month]
            if self.is_leap_year and self.month in {"January" , "February"}:
                day_of_week-=1
            if self.year >= 2000:
                day_of_week-=1
            else :
                if self.year < 1900:
                    day_of_week +=2 
                if self.year < 1800:
                    day_of_week +=2



            return day_of_week % 7 

        def calc_months_first_day_of_week(self):
            # as in https://en.wikipedia.org/wiki/Determination_of_the_day_of_the_week
            #Sakamoto's method
            d = 1 
            m = CalenderMonth.month_number[self.month]
            y = self.year
            t = self.sakamoto_table
            if m < 3:
                y-=1 
            return (y+y//4-y//100+y//400+t[m-1]+d)%7

        def to_next_month(self):
            m = CalenderMonth.month_number[self.month]+1
            y = self.year
            if m == 13:
                m = 1
                y+=1 
            m = self.month_names_from_number[m]
            self.reset(y,m)

        def to_prev_month(self):
            m = CalenderMonth.month_number[self.month]-1
            y = self.year
            if m == 0:
                m = 12
                y-=1             
            m = self.month_names_from_number[m]
            self.reset(y,m)           

        def gui_rows_amount(self):
            days_amount = self.days_amount + self.first_day_of_week
            rows_amount = days_amount//7 

            if days_amount % 7:
                rows_amount += 1             
            return rows_amount


        def gui_cell_xy_pos(self,day_nr, cell_width,cell_height,highest_cell_ypos):
            cell_nr = self.first_day_of_week+day_nr-1
            
            #cell pos:
            ypos = cell_nr//7
            xpos = cell_nr%7

            #pixel pos:
            xpos = (xpos+1)*cell_width+6
            ypos = (ypos+2)*cell_height+56
            if ypos > highest_cell_ypos:
                ypos = ypos -highest_cell_ypos + cell_height-13
            return xpos,ypos



            








        
    calenderMonth =CalenderMonth(1998, "April")
    calenderMonth =CalenderMonth(1998, "February")
    calenderMonth =CalenderMonth(2024, "December")
    #calenderMonth =CalenderMonth(2025, "March")
    #calenderMonth =CalenderMonth(2025, "January")
    #calenderMonth =CalenderMonth(2000, "January")
    #calenderMonth =CalenderMonth(2000, "February")
    #calenderMonth =CalenderMonth(2001, "January")

    daytime = DayTimeMinutesEntry("lunch", " Just eat lunch in peace ", 16, 15,20 )

    math_lesson = DayTimeMinutesEntry("math ","Linear equasions ",  9, 15,90, )
    physicks_lesson = DayTimeMinutesEntry("Physicks", "Shroedinger equsions,", 11,15,90 )
    info_lesson = DayTimeMinutesEntry( "IT" ,"informaticks lesson", 13, 15,90 )
    sport_lesson = DayTimeMinutesEntry( "sports", "very long lesson long long entry", 15,15,60)


    calenderDay = CalenderDay(math_lesson, info_lesson, sport_lesson, physicks_lesson)
    calenderMonth.add_day(15,calenderDay)





label test_calender_entry_short():
    #show screen calender_entry_short(("one","two", "three"), (200,200))
    show screen calender(calenderMonth)
    hide window  
    label .loop:
        #"Say : [daytime]"
        pause 
    jump .loop 
    return 

        