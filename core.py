"""
Global imports
"""
# from PyOpenGL import *
import matplotlib.pyplot as plt
import numpy as np


class DataFetcher:
    """
    This is a skeleton class is for getting overall sensor data from all universal motors
    """
    def __init__(self, *args):
        pass

    def mtr1_voltage(self):
        """
        Get the analog value from the Arduino ADC as raw values and display them on the analog gauges
        on the main manual screen
        This applies for all the voltage functions functions
        :return: real time motor voltage
        """
        pass

    def mtr2_voltage(self):
        pass

    def mtr3_voltage(self):
        pass

    def mtr4_voltage(self):
        pass

    def mtr5_voltage(self):
        pass

    def mtr6_voltage(self):
        pass

    def gripper_force(self):
        pass


    # todo: implement classes to calculate current


class Simulator:
    """
    This class simulates the kinematic movement of the arm's joints
    Implemented using OpenGL
    """
    def __init__(self, *args):
        pass

