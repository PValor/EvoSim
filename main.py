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

    joint_2.apply_force(0, 30)

    time.sleep(3)

    joint_4.apply_force(-30, -20)

kill_event = threading.Event()

joint_1 = Joint(0, 0)
joint_2 = Joint(50, 0)
joint_3 = Joint(100, 0)
joint_4 = Joint(100, 50)

arm_1 = Arm(f_joint1=joint_1, f_joint2=joint_2)
arm_2 = Arm(f_joint1=joint_2, f_joint2=joint_3)
arm_3 = Arm(f_joint1=joint_3, f_joint2=joint_4)

test_obj = Object([joint_1,joint_2, joint_3, joint_4], [arm_1, arm_2, arm_3])

data = ObjectData(kill_event, [test_obj], f_timestep=params.TIME_RESOLUTION)

graph_app = App(f_data=data, f_kill_event=kill_event, f_timestep=params.TIME_RESOLUTION)

threading.Thread(target=forces_scenario).start()

graph_app.protocol("WM_DELETE_WINDOW", on_closing)
graph_app.mainloop()

