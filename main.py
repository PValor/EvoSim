import threading
import time
from VIEW.window import App
from PROC.data import ObjectData
from PROC.object import Object, Arm, Joint
import params


def on_closing():
    kill_event.set()


def forces_scenario():

    time.sleep(2)

    joint_2.apply_force(8, -6)
    joint_3.apply_force(8, 6)


kill_event = threading.Event()

joint_2 = Joint(f_x=0,   f_y=80,  color="blue")
joint_1 = Joint(f_x=-60, f_y=0,   color="red")
joint_3 = Joint(f_x=0,   f_y=-80, color="magenta")

arm_1 = Arm(f_joint1=joint_1, f_joint2=joint_2)
arm_2 = Arm(f_joint1=joint_1, f_joint2=joint_3)

test_obj = Object([joint_1, joint_2, joint_3], [arm_1, arm_2])

data = ObjectData(kill_event, [test_obj], f_timestep=params.TIME_RESOLUTION)

graph_app = App(f_data=data, f_kill_event=kill_event, f_timestep=params.TIME_RESOLUTION)

threading.Thread(target=forces_scenario).start()

graph_app.protocol("WM_DELETE_WINDOW", on_closing)
graph_app.mainloop()

