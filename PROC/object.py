import math
import params


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

        self.velocity_x *= params.FRICTION_COEFF
        self.velocity_y *= params.FRICTION_COEFF


class Arm:
    def __init__(self, f_joint1, f_joint2):
        self.joint1 = f_joint1
        self.joint2 = f_joint2

        self.length = math.sqrt((self.joint1.x-self.joint2.x)**2+(self.joint1.y-self.joint2.y)**2)

    def transmit_force(self):
        self.length = math.sqrt((self.joint1.x-self.joint2.x)**2+(self.joint1.y-self.joint2.y)**2)

        if self.length != params.ARM_LENGTH:
            compression_force = (params.ARM_LENGTH - self.length)

            force_x = 0
            force_y = 0

            if self.joint2.x-self.joint1.x == 0:
                force_y = compression_force
            elif self.joint2.y-self.joint1.y == 0:
                force_x = compression_force
            else:
                slope = (self.joint2.y-self.joint1.y)/(self.joint2.x-self.joint1.x)
                force_x = compression_force/math.sqrt(1+abs(slope))
                force_y = compression_force/math.sqrt(1+abs(1/slope))

            if self.joint2.x > self.joint1.x:
                j1_f_x = -force_x
                j2_f_x = force_x
            else:
                j1_f_x = force_x
                j2_f_x = -force_x
            if self.joint2.y > self.joint1.y:
                j1_f_y = -force_y
                j2_f_y = force_y
            else:
                j1_f_y = force_y
                j2_f_y = -force_y

            self.joint1.apply_force(j1_f_x, j1_f_y)
            self.joint2.apply_force(j2_f_x, j2_f_y)


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
