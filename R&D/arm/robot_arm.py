import rospy
import numpy as np
from interbotix_xs_modules.arm import InterbotixManipulatorXS

class RobotArm:
    def __init__(self):
        if not rospy.core.is_initialized():
            rospy.init_node('robot_arm_node', anonymous=True)
        self.bot = InterbotixManipulatorXS("wx250", "arm", "gripper")
    
    def coffee(self):
        self.bot.arm.set_ee_pose_components(x=0.2, z=0.3)
        self.bot.arm.set_single_joint_position("waist", np.pi/4.0)
        self.bot.arm.set_ee_cartesian_trajectory(x=0.1, z=-0.2)
        self.bot.arm.set_ee_cartesian_trajectory(pitch=1.5)
        self.bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.16)
        self.bot.arm.set_single_joint_position("waist", -np.pi/2.0)
        self.bot.arm.go_to_home_pose()
        self.bot.arm.go_to_sleep_pose()

    def popcorn(self):
        self.bot.arm.set_ee_pose_components(x=0.2, z=0.3)
        self.bot.arm.set_single_joint_position("waist", np.pi/4.0)
        self.bot.arm.set_ee_cartesian_trajectory(x=0.1, z=-0.2)
        self.bot.arm.set_ee_cartesian_trajectory(pitch=1.0)
        self.bot.arm.set_ee_cartesian_trajectory(x=0.05, z=-0.1)
        self.bot.arm.set_ee_cartesian_trajectory(pitch=-1.0)
        self.bot.arm.set_ee_cartesian_trajectory(x=0.1, z=0.1)
        self.bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.16)
        self.bot.arm.set_single_joint_position("waist", 0)
        self.bot.arm.set_ee_cartesian_trajectory(x=0.1, z=-0.1)
        self.bot.arm.set_ee_cartesian_trajectory(pitch=0.5)
        self.bot.arm.go_to_home_pose()
        self.bot.arm.go_to_sleep_pose()