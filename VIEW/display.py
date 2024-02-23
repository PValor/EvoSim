import tkinter as tk
import threading
import time
import math

DISPLAY_HEIGHT = 800
DISPLAY_WIDTH  = 800

DISPLAY_X_CENTER = 400
DISPLAY_Y_CENTER = 400


class Display(tk.Frame):
    def __init__(self, f_root, f_ref_data, f_kill_event, f_timestep):
        super().__init__(f_root)

        self.drawing_zone_cnvs = tk.Canvas(self, width=800, height=800)
        self.drawing_zone_cnvs.grid(sticky="nwes")

        self.data = f_ref_data
        self.kill_event = f_kill_event

        self.pack()

        self.update_thread = threading.Thread(target=lambda: self.update_display())
        self.update_thread.start()

        self.timestep = f_timestep

    def update_display(self):
        while not self.kill_event.isSet():
            self.drawing_zone_cnvs.delete('all')
            self.draw_objects()
            time.sleep(self.timestep)

    def draw_objects(self):
        for obj in self.data.object_list:
            for arm in obj.arm_list:
                self.drawing_zone_cnvs.create_polygon(
                    DISPLAY_X_CENTER + arm.joint1.x-((arm.joint1.y-arm.joint2.y)*2)/arm.length,
                    DISPLAY_Y_CENTER - arm.joint1.y+((arm.joint2.x-arm.joint1.x)*2)/arm.length,
                    DISPLAY_X_CENTER + arm.joint1.x+((arm.joint1.y-arm.joint2.y)*2)/arm.length,
                    DISPLAY_Y_CENTER - arm.joint1.y-((arm.joint2.x-arm.joint1.x)*2)/arm.length,
                    DISPLAY_X_CENTER + arm.joint2.x+((arm.joint1.y-arm.joint2.y)*2)/arm.length,
                    DISPLAY_Y_CENTER - arm.joint2.y-((arm.joint2.x-arm.joint1.x)*2)/arm.length,
                    DISPLAY_X_CENTER + arm.joint2.x-((arm.joint1.y-arm.joint2.y)*2)/arm.length,
                    DISPLAY_Y_CENTER - arm.joint2.y+((arm.joint2.x-arm.joint1.x)*2)/arm.length,
                    fill="#DBC886")
            for joint in obj.joint_list:
                self.drawing_zone_cnvs.create_oval(DISPLAY_X_CENTER-4 + joint.x,
                                                   DISPLAY_Y_CENTER-4 - joint.y,
                                                   DISPLAY_X_CENTER+4 + joint.x,
                                                   DISPLAY_Y_CENTER+4 - joint.y,
                                                   fill="red")


