import sys
import math 
sys.path.append("../../")
from lib.ComunicationSystem.dds_sys import *

class position_calculator:
    
    def __init__(self):
        self.pos_list = {
                0:  [0,0],
                1:  [5, 0],
                2:  [0, -5],
                3:  [-5, 0],
                4:  [0, 4],
                5:  [5, -4.5],
                6:  [3.5, 3],
                7:  [-4, 5],
                8:  [-3, 1.5],
                9:  [-2, -6.5],
                10: [-3, -3],
                11: [4, 8],
                12: [8, -7],
                13: [8.5, 0],
                14: [7.5, 5],
                15: [-8, 8],
                16: [-8, -4],
                17: [-6.5, -8],
                18: [2.5, -7],
                19: [-4, 9],
                20: [9, 9]
                }

    def convert_in_coordinates(self,target_ID):

        if target_ID is None:
            return None
        
        return self.pos_list[target_ID]

    def euclidean_distance(self,point_a,point_b):

        a=self.convert_in_coordinates(point_a)
        b=self.convert_in_coordinates(point_b)

        if a is None or b is None:
            return 0
        
        return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

    def set_target(self, drone, target):

        coordinates=self.convert_in_coordinates(target)

        if coordinates is None:
            return None
        drone.x_target=coordinates[0]
        drone.y_target=coordinates[1]
        return target
    
