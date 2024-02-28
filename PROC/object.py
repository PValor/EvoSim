import math
import params


class Joint:
    def __init__(self, f_x, f_y, color):
        self.x = f_x
        self.y = f_y

        self.prev_x = f_x
        self.prev_y = f_y

        self.velocity_x = 0
        self.velocity_y = 0

        self.co_joints = []

        self.color = color

    def add_co_joint(self, f_joint):
        self.co_joints.append(f_joint)

    def apply_force(self, f_force_x, f_force_y):
        self.velocity_x += f_force_x/10
        self.velocity_y += f_force_y/10

        for joint in self.co_joints:
            joint.apply_transmitted_force(-f_force_x, -f_force_y)

    def apply_transmitted_force(self, f_force_x, f_force_y):
        self.velocity_x += f_force_x/10
        self.velocity_y += f_force_y/10

    def update_position(self):

        self.prev_x = self.x
        self.prev_y = self.y

        self.x += self.velocity_x
        self.y += self.velocity_y

        self.velocity_x *= params.FRICTION_COEFF
        self.velocity_y *= params.FRICTION_COEFF

class Articulation():
    def __init__(self, f_pivot_joint:Joint, f_joint1:Joint, f_joint2:Joint):
        self.pivot = f_pivot_joint
        self.joint1 = f_joint1
        self.joint2 = f_joint2

        self.angle_command = math.pi/2
        self.integrated_err = 0
        self.previous_err = 0

    def start_angle_command(self, f_angle):
        if f_angle != self.angle_command:
            self.integrated_err = 0
            self.previous_err = 0
            self.angle_command = f_angle

    def update_angle(self):
        if self.joint1.x == self.pivot.x:
            a_p1 = 10000
        else:
            a_p1 = (self.joint1.y - self.pivot.y)/(self.joint1.x - self.pivot.x)
        if self.joint2.x == self.pivot.x:
            a_p2 = 10000
        else:
            a_p2 = (self.joint2.y - self.pivot.y)/(self.joint2.x - self.pivot.x)

        if a_p1*a_p2 == -1:
            current_angle = math.copysign(math.pi/2, a_p2)
        else :
            current_angle = math.atan((a_p2 - a_p1)/(1+a_p1*a_p2))

        err = current_angle - self.angle_command

        if abs(err) > 0.1 :

            print(current_angle, err)

            self.integrated_err += err

            # Proportionnal
            corrective_force = params.KP * err
            # Integrative
            corrective_force += params.KI * self.integrated_err/params.DT
            # Derivative
            corrective_force += params.KD * (self.previous_err - err)/params.DT

            corrective_force /= 2

            if a_p1 == 0 :
                a_cf_1 = 10000
            else :
                a_cf_1 = -1/a_p1

            if a_p2 == 0 :
                a_cf_2 = 10000
            else :
                a_cf_2 = -1/a_p2

            cf1_x = math.sqrt(abs(corrective_force)/(1+(a_cf_1**2)))*math.copysign(1, a_cf_1)*math.copysign(1,corrective_force)
            cf1_y = math.sqrt(abs(corrective_force)/(1+(1/(a_cf_1**2))))*math.copysign(1,a_cf_1)*math.copysign(1,corrective_force)

            cf2_x = math.sqrt(abs(corrective_force)/(1+(a_cf_2**2)))*math.copysign(1,a_cf_2)*math.copysign(1,corrective_force)
            cf2_y = math.sqrt(abs(corrective_force)/(1+(1/(a_cf_2**2))))*math.copysign(1,a_cf_2)*math.copysign(1,corrective_force)


            print("cf1_x = ", cf1_x)
            print("cf1_y = ", cf1_y)
            print("cf2_x = ", cf2_x)
            print("cf2_y = ", cf2_y)

            self.joint1.apply_force(cf1_x, cf1_y)
            self.joint2.apply_force(cf2_x, cf2_y)


class Arm:
    def __init__(self, f_joint1, f_joint2):
        self.joint1 = f_joint1
        self.joint2 = f_joint2

        self.joint1.add_co_joint(self.joint2)
        self.joint2.add_co_joint(self.joint1)

        self.length = math.sqrt((self.joint1.x-self.joint2.x)**2+(self.joint1.y-self.joint2.y)**2)

    def transmit_force(self):
        self.length = math.sqrt((self.joint1.x-self.joint2.x)**2+(self.joint1.y-self.joint2.y)**2)

        if self.length != params.ARM_LENGTH:
            compression_force = (params.ARM_LENGTH - self.length)/2

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
    def __init__(self, f_joint_list=None, f_arm_list=None, f_articulation_list=None):
        if f_joint_list is None:
            self.joint_list = []
        else:
            self.joint_list = f_joint_list

        if f_arm_list is None:
            self.arm_list = []
        else:
            self.arm_list = f_arm_list

        if f_articulation_list is None:
            self.articulation_list = []
        else:
            self.articulation_list = f_articulation_list
