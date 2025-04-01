'''
THIS IS THE CODE FOR POPBOT, THE POPCORN AND SNACKS SERVING ROBOT OF THE SNAKBOT EXHIBIT.

WARNING: THIS CODE IS MEANT ONLY FOR POPBOT AND SHOULD NOT BE TESTED ON BREWBOT. 
THIS CODE CONTAINS -Z COORDINATES AND MUST BE RUN AT SLOW SPEEDS DURING TESTING TO AVOID BREAKING THE ARM DUE TO COLLISION.


'''

import time
from interbotix_xs_modules.arm import InterbotixManipulatorXS

def main():

    # Initialize the arm 
    bot = InterbotixManipulatorXS("wx250", moving_time=1.0, accel_time=1.0)
    #go to home position
    bot.arm.set_ee_pose_components(x=0.2, y=0.0, z=0.2, pitch=0.0)


    # takecup()
    # coffee()
    # placecup()
    # time.sleep(5)
    # takecup()
    # juice()
    # takecup()
    # coffee()



def takecup():
    bot = InterbotixManipulatorXS("wx250", moving_time=1.5, accel_time=1.5)
    #go to coffee cup holder and open gripper
    bot.arm.set_ee_pose_components(x=0.1, y=0.32, z=0.4, pitch=0.0)
    bot.gripper.open()
    #move upwards and grasp cup closing gripper
    bot.arm.set_ee_pose_components(x=0.1, y=0.32, z=0.49, pitch=0.0)
    bot.gripper.set_pressure(1.5)
    bot.gripper.close(1)
    #move down to pull cup out
    bot.arm.set_ee_cartesian_trajectory(x=0.01, z=-0.22)


def placecup():
    bot = InterbotixManipulatorXS("wx250", moving_time=4, accel_time=1.5)
    bot.arm.set_ee_pose_components(x=0.33, y=0.22, z=0.1, pitch=0.0)
    bot.arm.set_ee_cartesian_trajectory(x=-0.0, z=-0.01)
    bot.gripper.open()
    #wait and move arm backwards
    time.sleep(2)
    bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=0.0)
    time.sleep(1)
    #endcode sleep
    bot.arm.go_to_sleep_pose()


def coffee():
    bot = InterbotixManipulatorXS("wx250", moving_time=1.5, accel_time=1.5)
    #head to coffee machine
    bot.arm.set_ee_pose_components(x=-0.1, y=-0.32, z=0.1, pitch=0.0)
    #place cup in machine
    bot.arm.set_ee_pose_components(x=-0.1, y=-0.32, z=0.15, pitch=0.0)
    bot = InterbotixManipulatorXS("wx250", moving_time=3, accel_time=1.5)
    bot.arm.set_ee_pose_components(x=-0.13, y=-0.35, z=0.05, pitch=0.0)
    bot.gripper.open()
    bot = InterbotixManipulatorXS("wx250", moving_time=1.5, accel_time=1.5)
    bot.arm.set_ee_pose_components(x=-0.10, y=-0.32, z=0.1, pitch=0.0)
    bot.arm.set_ee_cartesian_trajectory(pitch=1.5)
    bot.arm.set_ee_cartesian_trajectory(x=0.03, z=0.03)
    bot.arm.set_ee_cartesian_trajectory(x=0.01, z=0.0)
    bot.arm.set_ee_cartesian_trajectory(x=-0.05, z=0.0)
    #coffe makeer make coffee
    time.sleep(5)
    bot = InterbotixManipulatorXS("wx250", moving_time=2, accel_time=1.5)
    bot.arm.set_ee_pose_components(x=-0.1, y=-0.32, z=0.1, pitch=0.0)
    bot.arm.set_ee_pose_components(x=-0.13, y=-0.35, z=0.05, pitch=0.0)
    bot.gripper.close()

    #move to serving area and place cup gently
    bot = InterbotixManipulatorXS("wx250", moving_time=4, accel_time=1.5)
    bot.arm.set_ee_cartesian_trajectory(x=-0.05, z=0.0)
    bot.arm.set_ee_pose_components(x=-0.10, y=-0.32, z=0.1, pitch=0.0)
    placecup()



def juice():
    bot = InterbotixManipulatorXS("wx250", moving_time=1.5, accel_time=1.5)
    #head to juice dispenser
    choice = input("Enter choice: ")    
    
    if choice == '1':
        bot.arm.set_ee_pose_components(x=-0.19, y=0.19, z=0.1, pitch=0.0)
    elif choice == '2':
        bot.arm.set_ee_pose_components(x=-0.33, y=0.15, z=0.11, pitch=0.0)
    elif choice == '3':
        bot.arm.set_ee_pose_components(x=-0.33, y=0.0, z=0.11, pitch=0.0)

    bot.arm.set_ee_cartesian_trajectory(x=0.1, z=0.1) 
    #juice is filled
    time.sleep(5)   
    bot = InterbotixManipulatorXS("wx250", moving_time=4, accel_time=1.5)

    bot.arm.set_ee_cartesian_trajectory(x=-0.1, z=-0.1) 

    #move to serving area and place cup gently
    bot = InterbotixManipulatorXS("wx250", moving_time=5, accel_time=4)
    placecup()



if __name__=='__main__':

    main()
  
