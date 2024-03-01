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
    for x in range(10):
        pivot.start_angle_command(math.pi/8)

        time.sleep(1.5)
        pivot.start_angle_command(math.pi/1.2)
        time.sleep(0.5)
    # pivot2.start_angle_command(math.pi/8)


kill_event = threading.Event()

joint_pivot = Joint(f_x=-50,
                    f_y=200,
                    color="blue")

joint_1 = Joint(f_x=-150,
                f_y=201,
                color="green")

joint_2 = Joint(f_x=50,
                f_y=201,
                color="red")

pivot = Articulation(joint_pivot, joint_1, joint_2, 1)

joint_list = [joint_pivot, joint_1, joint_2]
arm_list = [Arm(joint_pivot, joint_1), Arm(joint_pivot, joint_2)]
articulation_list = [pivot]

# joint_pivot2 = Joint(f_x=200,
#                     f_y=0,
#                     color="blue")
#
# joint_12 = Joint(f_x=100,
#                 f_y=1,
#                 color="green")
#
# joint_22 = Joint(f_x=300,
#                 f_y=1,
#                 color="red")
#
# pivot2 = Articulation(joint_pivot2, joint_12, joint_22, 0.4)
#
# joint_list2 = [joint_pivot2, joint_12, joint_22]
# arm_list2 = [Arm(joint_pivot2, joint_12), Arm(joint_pivot2, joint_22)]
# articulation_list2 = [pivot2]

test_obj = Object(f_joint_list=joint_list, f_arm_list=arm_list, f_articulation_list=articulation_list)
# test_obj2 = Object(f_joint_list=joint_list2, f_arm_list=arm_list2, f_articulation_list=articulation_list2)


data = ObjectData(kill_event, [test_obj])
# data = ObjectData(kill_event, [test_obj, test_obj2])

graph_app = App(f_data=data, f_kill_event=kill_event)

threading.Thread(target=forces_scenario).start()

graph_app.protocol("WM_DELETE_WINDOW", on_closing)

graph_app.mainloop()
