import tkinter as tk
import threading
import time
import params


class Display(tk.Frame):
    def __init__(self, f_root, f_ref_data, f_kill_event):
        super().__init__(f_root)

        self.root = f_root

        self.drawing_zone_cnvs = tk.Canvas(self,
                                           width=params.DISPLAY_WIDTH,
                                           height=params.DISPLAY_HEIGHT)
        self.drawing_zone_cnvs.grid(sticky="nwes")

        self.data = f_ref_data
        self.kill_event = f_kill_event

        self.bind("<<ThreadFinished>>", lambda _: self.destroy_window())

        self.update_thread = threading.Thread(target=lambda: self.update_display())

        self.timestep = params.TIME_RESOLUTION

        self.pack()
        self.update_thread.start()

    def update_display(self):
        while not self.kill_event.is_set():
            self.drawing_zone_cnvs.delete('all')
            self.draw_objects()
            time.sleep(self.timestep)
        self.event_generate("<<ThreadFinished>>")
        print("Display exit")

    def destroy_window(self):
        self.root.destroy()

    def draw_objects(self):
        for obj in self.data.object_list:
            for arm in obj.arm_list:
                self.drawing_zone_cnvs.create_polygon(
                    params.DISPLAY_X_CENTER + arm.joint1.x-((arm.joint1.y-arm.joint2.y)*params.ARM_WIDTH)/arm.length,
                    params.DISPLAY_Y_CENTER - arm.joint1.y+((arm.joint2.x-arm.joint1.x)*params.ARM_WIDTH)/arm.length,
                    params.DISPLAY_X_CENTER + arm.joint1.x+((arm.joint1.y-arm.joint2.y)*params.ARM_WIDTH)/arm.length,
                    params.DISPLAY_Y_CENTER - arm.joint1.y-((arm.joint2.x-arm.joint1.x)*params.ARM_WIDTH)/arm.length,
                    params.DISPLAY_X_CENTER + arm.joint2.x+((arm.joint1.y-arm.joint2.y)*params.ARM_WIDTH)/arm.length,
                    params.DISPLAY_Y_CENTER - arm.joint2.y-((arm.joint2.x-arm.joint1.x)*params.ARM_WIDTH)/arm.length,
                    params.DISPLAY_X_CENTER + arm.joint2.x-((arm.joint1.y-arm.joint2.y)*params.ARM_WIDTH)/arm.length,
                    params.DISPLAY_Y_CENTER - arm.joint2.y+((arm.joint2.x-arm.joint1.x)*params.ARM_WIDTH)/arm.length,
                    fill="#DBC886")
            for joint in obj.joint_list:
                self.drawing_zone_cnvs.create_oval(params.DISPLAY_X_CENTER-params.JOINT_RADIUS + joint.x,
                                                   params.DISPLAY_Y_CENTER-params.JOINT_RADIUS - joint.y,
                                                   params.DISPLAY_X_CENTER+params.JOINT_RADIUS + joint.x,
                                                   params.DISPLAY_Y_CENTER+params.JOINT_RADIUS - joint.y,
                                                   fill=joint.color)
