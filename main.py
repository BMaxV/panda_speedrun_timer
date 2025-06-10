import os
import time

import panda3d
from direct.showbase import ShowBase
from panda3d.core import WindowProperties

from panda_interface_glue import panda_interface_glue as pig


class SimpleSpeedrunTimer:
    def __init__(self, showbase):
        self.b = showbase

        self.zero_values()
        self.load_names()

        self.build_buttons()

        self.z_spacing = 0.18

        pos = (-0.5, 0, -0.4)
        self.main_time = pig.create_textline(f"0", pos)
        self.main_time.setScale(0.15)
        
    def main(self, *args):
        """this just updates the main clock"""
        diff = time.time() - self.start_time
        if self.start_time == 0:
            my_text = "not started"
        else:
            my_text = self.get_time_text(diff)
        self.main_time.node().set_text(my_text)

    def build_buttons(self):
        self.reset_button = pig.create_button(
            "reset", (-0.6, 0, -0.8), 0.05, self.reset, [])
        self.start_button = pig.create_button(
            "start", (-0.0, 0, -0.8), 0.05, self.start, [])
        self.split_button = pig.create_button(
            "split", (0.6, 0, -0.8), 0.05, self.split, [])
        self.split_button = pig.create_button(
            "save", (-0.6, 0, -0.9), 0.05, self.save, [])

    def load_names(self):
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

        self.timing_list = []
        self.start_time = 0
        self.timing_UI = []
        self.split_c = 0

    def save(self, *args):
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

        with open("timings.csv", "w") as f:
            f.write(s)
        
    def start(self, *args):
        self.start_time = time.time()

    def reset(self, *args):
        self.timing_list = []
        for node in self.timing_UI:
            node.removeNode()
        self.timing_UI = []
        self.start_time = 0  # time.time()
        self.split_c = 0

    def get_time_text(self, my_seconds):
        """
        somehow **formatting time** for a stopwatch is a difficult,
        unsolved problem in python
        
        so this converts seconds into hours, minutes, seconds.
        not days, because I built this as a speedrun clock, but
        adding that is trivial if you want.
        """
        hours = int(my_seconds.__floordiv__(60*60))
        hours = str(hours)
        hours = hours.rjust(2, "0")

        minutes = int(my_seconds.__floordiv__(60))
        minutes = str(minutes)
        minutes = minutes.rjust(2, "0")

        seconds = my_seconds % 60
        seconds = (str(round(seconds, 2)))
        seconds = seconds.rjust(5, "0")
        my_text = f"{hours}:{minutes}:{seconds}"

        return my_text

    def delete_adjust(self):

        if len(self.timing_UI) > 5:
            old = self.timing_UI.pop(0)
            old.removeNode()
            for x in self.timing_UI:
                pos = x.getPos()
                x.setPos((pos[0], 0, pos[2]+self.z_spacing))

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
        diff = time.time() - self.start_time
        self.timing_list.append(diff)

        m = len(self.timing_UI)
        pos = (0.5, 0, 0.8-m*self.z_spacing)
        text = self.get_text()
        time_text = self.get_time_text(diff)

        full_text = f"{text} {time_text}"
        #full_text = full_text.ljust(50, " ")
        new_element = pig.create_textline(full_text, pos)
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


def main():
    W = Wrapper()

    while True:
        delta_t = globalClock.dt
        W.SimpleSpeedrunTimer.main(delta_t)

        W.b.taskMgr.step()


if __name__ == "__main__":
    main()
