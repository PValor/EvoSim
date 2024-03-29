import time
import params
import threading


class ObjectData:
    def __init__(self, f_kill_event, f_object_list=None):
        if f_object_list is None:
            self.object_list = []
        else:
            self.object_list = f_object_list

        self.kill_event = f_kill_event

        self.update_object_thread = threading.Thread(target=lambda: self.update_object_data())

        self.update_object_thread.start()

    def add_objects(self, f_new_objects):
        for obj in f_new_objects:
            self.object_list.append(obj)

    def update_object_data(self):
        while not self.kill_event.isSet():
            for obj in self.object_list:
                for arm in obj.arm_list:
                    arm.transmit_force()
                for articulation in obj.articulation_list:
                    articulation.update_angle()
                for joint in obj.joint_list:
                    joint.update_position()

            time.sleep(params.DT)
        print("Data exit")
