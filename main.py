import math
import threading
import time
from VIEW.window import App
from PROC.data import ObjectData
from PROC.object import Object, Arm, Joint, Articulation
import params


def on_closing():
    kill_event.set()


def forces_scenario():
    time.sleep(2)

    print("launch command")
    pivot.start_angle_command(math.pi/2.2)


kill_event = threading.Event()

joint_pivot = Joint(f_x=0,
                    f_y=0,
                    color="blue")

joint_1 = Joint(f_x=0,
                f_y=100,
                color="green")

joint_2 = Joint(f_x=0,
                f_y=100,
                color="red")

pivot = Articulation(joint_pivot, joint_1, joint_2)

joint_list = [joint_pivot, joint_1, joint_2]
arm_list = [Arm(joint_pivot, joint_1), Arm(joint_pivot, joint_2)]
articulation_list = [pivot]

test_obj = Object(f_joint_list=joint_list, f_arm_list=arm_list, f_articulation_list=articulation_list)


data = ObjectData(kill_event, [test_obj])

graph_app = App(f_data=data, f_kill_event=kill_event)

threading.Thread(target=forces_scenario).start()

graph_app.protocol("WM_DELETE_WINDOW", on_closing)

graph_app.mainloop()
