import sys
import numpy as np
from interbotix_xs_modules.arm import InterbotixManipulatorXS

def popcorn(bot):
    """
    Executes the coffee-serving sequence for the WX250 robot arm.
    """
    # Move end-effector to an initial position
    bot.arm.set_ee_pose_components(x=0.2, z=0.3)  # Move to (X=0.2m, Z=0.3m)

    # Rotate the waist joint **clockwise (CW)**
    bot.arm.set_single_joint_position("waist", np.pi/4.0)  # Rotate waist **45° CW**

    # Perform a small forward-downward motion
    bot.arm.set_ee_cartesian_trajectory(x=0.1, z=-0.2)  # Move forward (X+0.1m) and down (Z-0.2m)

    # Perform an up/down wrist pitching motion
    bot.arm.set_ee_cartesian_trajectory(pitch=1.0)  # Tilt the end-effector forward  
    bot.arm.set_ee_cartesian_trajectory(x=0.05, z=-0.1)
    bot.arm.set_ee_cartesian_trajectory(pitch=-1.0)
    bot.arm.set_ee_cartesian_trajectory(x=0.1, z=0.1)
    # Reverse the previous motion
    bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.16)  # Move back (X-0.1m) and up (Z+0.16m)

    # Rotate the waist joint **counterclockwise (CCW)**
    bot.arm.set_single_joint_position("waist", 0)  # Rotate waist **-90° CCW**
    bot.arm.set_ee_cartesian_trajectory(x=0.1, z=-0.1)
    bot.arm.set_ee_cartesian_trajectory(pitch=0.5)
    # Return arm to home and sleep position
    bot.arm.go_to_home_pose()  # Move to default home pose  
    bot.arm.go_to_sleep_pose()  # Move to rest/sleep position  

def main():
    """
    Initializes the WX250 robot and runs the coffee function.
    """
    bot = InterbotixManipulatorXS("wx250", "arm", "gripper")

    if bot.arm.group_info.num_joints < 5:
        sys.exit()

    # Call the coffee-serving function
    popcorn(bot)

if __name__ == '__main__':
    main()
