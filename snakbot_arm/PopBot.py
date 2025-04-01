'''
THIS IS THE CODE FOR BREWBOT, THE JUICE AND COFFEE SERVING ROBOT OF THE SNAKBOT EXHIBIT.

    WARNING: coffee() and juice() have placecup alreay added in the end of function..no need to call


'''
import time
from interbotix_xs_modules.arm import InterbotixManipulatorXS
import numpy as np

def popcorn():
    #SET SPEED    
    bot = InterbotixManipulatorXS("wx250", moving_time=2.0, accel_time=1.0)

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

    # Initialize the arm 
    bot = InterbotixManipulatorXS("wx250", moving_time=1.0, accel_time=1.0)
    #go to home position
    bot.arm.set_ee_pose_components(x=0.2, y=0.0, z=0.2, pitch=0.0)

    popcorn()    

if __name__=='__main__':

    main()
  