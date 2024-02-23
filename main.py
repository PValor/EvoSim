import threading
from VIEW.window import App
from PROC.data import ObjectData
from PROC.object import *

step = 1

kill_event = threading.Event()

joint_1 = Joint(0, 0)
joint_2 = Joint(0, 50)

arm = Arm(f_joint1=joint_1, f_joint2=joint_2)

test_obj = Object([joint_1, joint_2], [arm])

data = ObjectData(kill_event, [test_obj], f_timestep=step)

joint_2.apply_force(0, 1)

graph_app = App(f_data=data, f_kill_event=kill_event, f_timestep=step)
