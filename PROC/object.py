import math

class Joint:
    def __init__(self, f_x, f_y):
        self.x = f_x
        self.y = f_y

        self.prev_x = f_x
        self.prev_y = f_y

        self.velocity_x = 0
        self.velocity_y = 0

    def apply_force(self, f_force_x, f_force_y):
        self.velocity_x += f_force_x
        self.velocity_y += f_force_y

    def update_position(self):

        self.prev_x = self.x
        self.prev_y = self.y

        self.x += self.velocity_x
        self.y += self.velocity_y

        self.velocity_x *= 0.99
        self.velocity_y *= 0.99


class Arm:
    def __init__(self, f_joint1, f_joint2):
        self.joint1 = f_joint1
        self.joint2 = f_joint2

        self.length = math.sqrt((self.joint1.x-self.joint2.x)**2+(self.joint1.y-self.joint2.y)**2)

    def transmit_force(self):
        self.length = math.sqrt((self.joint1.x-self.joint2.x)**2+(self.joint1.y-self.joint2.y)**2)
        print(f"Length = {self.length}")

        if self.length < 48 or self.length > 52:
            compression_force = abs(50 - self.length)

            force_x = compression_force*50/self.length #cos alpha FAUX

            force_y = compression_force*math.sqrt(1-(50/self.length)*(50/self.length)) #sin alpha FAUX
            print(f"Force x = {force_y}")

            # Si plus on soustrait si plus grand on ajoute
            self.joint1.apply_force(force_x, force_y)
            self.joint2.apply_force(-force_x, -force_y)





class Object:
    def __init__(self, f_joint_list=None, f_arm_list=None):
        if f_joint_list is None:
            self.joint_list = []
        else:
            self.joint_list = f_joint_list

        if f_arm_list is None:
            self.arm_list = []
        else:
            self.arm_list = f_arm_list
