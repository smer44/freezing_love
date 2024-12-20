
default calender_entry_width = config.screen_width //9
default calender_entry_short_height = config.screen_height //9
default calender_entry_full_height = int(config.screen_width /3.5)
default highest_cell_ypos = config.screen_height - calender_entry_full_height

screen calender_entry_short(texts,xy):
    default k = 12
    frame:
        xysize (calender_entry_width, calender_entry_short_height)
        imagebutton:
            idle Solid("#000",xsize=calender_entry_width-k, ysize=calender_entry_short_height-k)
            hover Solid("#0af",xsize=calender_entry_width-k, ysize=calender_entry_short_height-k)
            action ToggleScreen("calender_entry_long",None, texts,xy)
        #pos xy 
        vbox:            
            for text in texts:
                text "[text]" 


screen calender_entry_long(texts,xy):

    frame:
        xysize (calender_entry_width, calender_entry_full_height)
        pos xy 
        vbox:
            
            for text in texts:
                text "[text]" 



screen calender_entry_empty(xy):
    frame:
        style "empty"
        xysize (calender_entry_width, calender_entry_short_height)
        #pos xy 


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
    frame:
        #align 0.5,0.5
        pos config.screen_width//9, config.screen_height //9 
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
            grid 7 cal_obj.gui_rows_amount():
                    #use calender_entry_short((day_of_week_name,), (0,0))
                for day_nr in range(0,cal_obj.first_day_of_week):
                    use calender_entry_empty((0,0))
                for day_nr in range(1, cal_obj.days_amount+1):
                    use calender_entry_short((day_nr,), cal_obj.gui_cell_xy_pos(day_nr,calender_entry_width, calender_entry_short_height, highest_cell_ypos))
                



init -999 python:

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


        def reset(self,year,month):
            assert month in CalenderMonth.month_day_of_week_marker, "CalenderMonth : wrong month :" + str(month)
            self.year = int(year)
            assert self.year > 1752 
            self.month = month
            
            self.is_leap_year = self.calc_leap_year()
            self.days_amount = self.calc_days_of_month()
            self.first_day_of_week = self.calc_months_first_day_of_week()


        
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




label test_calender_entry_short():
    #show screen calender_entry_short(("one","two", "three"), (200,200))
    show screen calender(calenderMonth)
    hide window  
    label .loop:
        pause 
    jump .loop 
    return 

        