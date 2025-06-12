import os
import time
import datetime

from contextlib import contextmanager

import panda3d
from direct.showbase import ShowBase
from panda3d.core import WindowProperties

from panda_interface_glue import panda_interface_glue as pig

#def fake_exit():
    #print("yo fake exit")

class SimpleSpeedrunTimer:
    """
    uh... i somehow got around the concept of a running clock? hm.
    
    """
    def __init__(self, showbase):
        self.b = showbase

        self.zero_values()
        self.load_names()

        self.build_buttons()

        self.z_spacing = 0.18

        pos = (-0.5, 0, -0.4)
        
        self.font = self.b.loader.loadFont("FreeMono.ttf")
        
        #path = pig.create_textline(my_text,(-1.2,0,0),card_color=(0.4,0.4,0.4,1),panda_font=font
        self.main_time = pig.create_textline(f"0", pos,panda_font = self.font,card_color=(1,1,1,0),outline_color=(0.1,0.1,0.1,1),outline_geom=(0.5,0))
        self.main_time.setScale(0.15)
        
        self.decimals = 0
        
        self.font_name = "FreeMono.ttf"
        
        self.try_auto_load()
        
        # other option to do some auto save thing.
        # base.exitFunc = fake_exit
        
    def try_auto_load(self):
        # maybe there is a config?
        
        names = os.listdir()
        new_names = []
        for name in names:
            if name.startswith("auto"):
                new_names.append(name)
        
        new_names.sort()
        print(new_names)
        fn=new_names[-1]
        
        # if this crashes, only because you messed with it.
        #try:
        self.load(fn)
    
        #except:
        #    pri
        
        
        
    def main(self, *args):
        """this just updates the main clock"""
        # that is not accurate.
        # that doesn't work.
        diff = time.time() - self.start_time
        
        if self.clock_started == False:
            my_text = "not started"
        else:
            print(diff)
            my_text = self.get_time_text(diff,decimals = self.decimals)
            self.main_time.node().set_text(my_text)

    def build_buttons(self):
        self.reset_button = pig.create_button(
            "reset", (-0.6, 0, -0.8), 0.05, self.reset, [])
        self.start_button = pig.create_button(
            "start/resume", (-0.6, 0, -0.7), 0.05, self.start_resume, [])
        self.split_button = pig.create_button(
            "split", (0.0, 0, -0.7), 0.05, self.split, [])
        self.split_button = pig.create_button(
            "save", (-0.6, 0, -0.9), 0.05, self.save, [])
        self.enter_button = pig.create_button(
            "enter time", (0, 0, -0.9), 0.05, self.start_entering_time, [])
        self.enter_button = pig.create_button(
            "pause", (0.6, 0, -0.7), 0.05, self.pause, [])
        self.enter_button = pig.create_button(
            "load options", (0.6, 0, -0.9), 0.05, self.show_load_options, [])
        
        # this should not work and not be called, but if it is...
        # idk, it gets a none error, not a... somethinng.
        self.new_text_entry = None
        self.confirm_button = None
        
    def start_entering_time(self,*args):
        #p_dict = {"scale": (0.05, 0.05, 0.05)}

        self.new_text_entry = pig.old_create_text_entry((-0.8,0,-0.7),0.05)
        #self.new_text_entry.setPos(0,0,0.2)
        self.confirm_button = pig.create_button(
            "confirm", (0, 0, 0), 0.05, self.confirm_entering, [])
        
    def confirm_entering(self,*args):
        my_text = self.new_text_entry.get()
        my_time,success = self.time_enter_function(my_text)
        #print(my_time)
        if not success:
            #self.main_time.set_text("entry failed")
            self.main_time.node().set_text("entry failed")
            
        if success:
            self.new_text_entry.destroy()
            self.confirm_button.destroy()
            self.new_text_entry = None
            self.confirm_button = None
            
            time_text = self.get_time_text(my_time)
            print(time_text)
            self.main_time.node().set_text(time_text)
            
            self.clock_timing_touched = True
            
        self.start_time_diff = my_time
        
        
            
    def start_resume(self, *args):
        
        if self.temp_stopped_clock_value == None:
            
            self.start_time = time.time() - self.start_time_diff
        else:
            self.start_time = time.time() - self.temp_stopped_clock_value
            
        self.clock_started = True
        self.clock_timing_touched = True
        
    def load_names(self,*args):
        if "splitnamelist.txt" in os.listdir():
            with open("splitnamelist.txt", "r") as f:
                t = f.read()

                t = t.split("\n")
                while "" in t:
                    t.remove("")
                self.name_list = t
        else:
            self.name_list = ["make", "splitnamelist.txt", "in", "folder"]

    def zero_values(self):
        
        self.clock_started = False
        
        self.timing_list = []
        self.start_time = 0
        self.timing_UI = []
        self.split_c = 0
        self.start_time_diff = 0

        # this is for...
        self.clock_timing_touched = False
        
        self.temp_stopped_clock_value = None
        
    def save(self, fn_prefix="",*args):
        """save timings to textfile"""
        s = ""
        c = 0
        m = len(self.timing_list)

        while c < m:
            if c < len(self.name_list):
                name = self.name_list[c]
            else:
                name = "unnamed"
            s += f"{name};{self.timing_list[c]}\n"
            c += 1
        s += f"save_marker_automatic;{time.time()-self.start_time}\n"
        
        time_string = datetime.datetime.now().isoformat()
        print(time_string)
        with open(fn_prefix+time_string+"timings.csv", "w") as f:
            f.write(s)
    
    def pause(self,*args):
        if self.clock_started:
            stopped_clock_value = time.time() - self.start_time 
            self.temp_stopped_clock_value = stopped_clock_value
            self.clock_started = False
    
    def show_load_options(self,*args):
        names = os.listdir()
        new_names = []
        for name in names:
            if name.startswith("auto"):
                new_names.append(name)
        new_names.sort(reverse=True)
        
        c=0
        self.temp_buttons = []
        for name in new_names :
            b = pig.create_button(name, (-0.0, 0, 0.8-c*self.z_spacing), 0.05, self.load_close, [name])
            self.temp_buttons.append(b)
            if c>10:
                break
            c+=1
        b = pig.create_button("abort loading", (-0.0, 0, 0.8-c*self.z_spacing), 0.05, self.load_close, [name])
        self.temp_buttons.append(b)
        
        fn=new_names[-1]
        
    def load_close(self,fn=None,*args):
        if fn!=None:
            self.load(fn)
        for x in self.temp_buttons:
            x.destroy()
        self.temp_buttons=[]        

    def load(self,fn):
        
        self.reset()
        
        with open(fn,"r") as f:
            t= f.read()
            t = t.split("\n")
        while "" in t:
            t.remove("")
        lines = t
        
        #self.timings = 
        for line in lines:
            line = line.split(";")
            name, time=line
            print(time)
            time=float(time)
            
            if name == "save_marker_automatic":
                # is this correct?
                self.start_time_diff = time
                
            else:
                
                self.timing_list.append(time)
                self.make_timesplit_UI_element(time)
        
    def reset(self, *args):
        self.timing_list = []
        for node in self.timing_UI:
            node.removeNode()
        my_text = self.get_time_text(0,decimals = self.decimals)
        self.main_time.node().set_text(my_text)
        self.timing_UI = []
        self.start_time = 0  # time.time()
        self.start_time_diff = 0
        self.split_c = 0
        self.clock_started = False

    def get_time_text(self, my_seconds,decimals = 2):
        """
        somehow **formatting time** for a stopwatch is a difficult,
        unsolved problem in python
        
        so this converts seconds into hours, minutes, seconds.
        not days, because I built this as a speedrun clock, but
        adding that is trivial if you want.
        """
        hours = int(my_seconds.__floordiv__(60*60))
        hours = hours % 24
        hours = str(hours)
        
        hours = hours.rjust(2, "0")

        minutes = int(my_seconds.__floordiv__(60))
        minutes = minutes % 60
        minutes = str(minutes)
        minutes = minutes.rjust(2, "0")

        seconds = my_seconds % 60 # huh?
        seconds = (str(round(seconds, decimals)))
        number = max(3+decimals,4) #eh, 0.0 and 60.0 happens otherwise
        seconds = seconds.rjust(number, "0")
        
        my_text = f"{hours}:{minutes}:{seconds}"

        return my_text
    
    def manually_enter(self):
        """set the time to go from e.g. a save and a set time."""
        self.asdf=1
    
    def delete_adjust(self):

        if len(self.timing_UI) > 5:
            old = self.timing_UI.pop(0)
            old.removeNode()
            for x in self.timing_UI:
                pos = x.getPos()
                x.setPos((pos[0], 0, pos[2]+self.z_spacing))
    
    def time_enter_function(self,my_time):
        # it would be best if this would land me in a "paused" mode.
        #try:
        if True:
            r = my_time.split(":")
            assert len(r) == 3
            #I'm assuming this is length 3, and
            hours, minutes, seconds=r
            
            hours = int(hours)
            minutes = int(minutes)
            seconds = float(seconds)
            print(hours, minutes, seconds)
            min_totl = 60*hours+minutes
            #minutes 
            seconds += 60*min_totl#minutes
            print(seconds)
            print(self.get_time_text(seconds))
            print("61",self.get_time_text(61))
            print("61 minutes", self.get_time_text(60*61))
            converted=self.get_time_text(seconds)
            print([my_time,converted])
        
        #except:
            #print('something went wrong')
            #return 0, False 
        return seconds, True
        
    
    def get_text(self):
        if self.split_c < len(self.name_list):
            text = self.name_list[self.split_c]
        else:
            text = f"split {self.split_c}"
        return text

    def split(self, *args):
        
        # if too full...
        self.delete_adjust()

        if self.start_time == 0:
            self.start_time = time.time()
            
        if self.clock_started:
            diff = time.time() - self.start_time
            
            
            # ok, so I am only recording the difference.
            self.timing_list.append(diff)
            self.make_timesplit_UI_element(diff)
            self.clock_timing_touched = True
        
    def make_timesplit_UI_element(self, diff):

        m = len(self.timing_UI)
        pos = (0.5, 0, 0.8-m*self.z_spacing)
        text = self.get_text()
        time_text = self.get_time_text(diff)

        full_text = f"{text} {time_text}"
        #full_text = full_text.ljust(50, " ")
        new_element = pig.create_textline(full_text, pos,panda_font = self.font,card_color=(1,1,1,0),outline_color=(0.1,0.1,0.1,1),outline_geom=(0.5,0))
        #main.py:23: self.timer = pig.create_textline(my_text,(-1.2,0,-0.5),card_color=(0.4,0.4,0.4,1),panda_font=font,outline_color=(0.1,0.1,0.1,1),outline_geom=(0.5,0))
        new_element.node().set_align(1)

        new_element.setScale(0.10)
        self.timing_UI.append(new_element)

        self.split_c += 1


class Wrapper:
    def __init__(self):

        self.b = ShowBase.ShowBase()

        props = WindowProperties()
        props.setTitle('My timer')
        self.b.win.requestProperties(props)
        base.setBackgroundColor(0, 1, 0, 1)

        self.SimpleSpeedrunTimer = SimpleSpeedrunTimer(self.b)

# this is for autosave on quit.
class MyContext:
    
    def __init__(self,GameControlObject,*args):
        
        self.gamecontrol=GameControlObject
        
    def __enter__(self):
        return self
        
    def __exit__(self,*args):
        if self.gamecontrol.clock_timing_touched:
            self.gamecontrol.save(fn_prefix="auto")
        # if you didn't do anything, don't make save.
        return


def main():
    W = Wrapper()
    with MyContext(W.SimpleSpeedrunTimer):
        while True:
            delta_t = globalClock.dt
            W.SimpleSpeedrunTimer.main(delta_t)

            W.b.taskMgr.step()


if __name__ == "__main__":
    main()
