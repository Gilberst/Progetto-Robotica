import sys
sys.path.append("../../")
import logging
from lib.lib_funct import *
from lib.math_funct import *
class Drone:

    def __init__(self):
        self.z_vel_control=PID_Controller(4.5, 8.35, 0.025, 6.4)
        self.z_control=PID_Controller(6, 0.0, 0.0, 5)  

        self.y_vel_control=PID_Controller(0.7, 0.0, 0.3415, math.radians(30),True)
        self.y_control=PID_Controller(0.9, 0.0, 0.0, 1,True)

        self.x_vel_control=PID_Controller(0.7, 0.0, 0.3415, math.radians(30),True)
        self.x_control=PID_Controller(0.9, 0.0, 0.0, 1,True)
        
        self.w_roll_control=PID_Controller(0.5, 0.2, 0.005, 2)
        self.roll_control=PID_Controller(1.0, 0.0, 0.0, 4) 

        self.w_pitch_control=PID_Controller(0.5, 0.2, 0.005, 2)
        self.pitch_control=PID_Controller(1.0, 0.0, 0.0, 4)
                
        self.z_target = 0.0
        self.x_target = 0.0
        self.y_target = 0.0
        #dati per taratura
        self.z_target_data=[]
        self.z_data=[]
        self.z_error_data=[]

        self.x_target_data=[]
        self.x_data=[]
        self.x_error_data=[]

        self.y_target_data=[]
        self.y_data=[]
        self.y_error_data=[]

        self.vz_target_data=[]
        self.vz_data=[]
        self.vz_error_data=[]

        self.vx_target_data=[]
        self.vx_data=[]
        self.vx_error_data=[]

        self.vy_target_data=[]
        self.vy_data=[]
        self.vy_error_data=[]

        

    def evaluate(self, delta_t, z, zV, x, xV, y, yV, roll, roll_rate, pitch, pitch_rate):
        
        self.x = x
        self.y = y
        self.z = z
        
        # propeller order = quello visto a lezione
        #
        #  3     4
        #
        #  2     1
        #

        #controllo sulle z
        self.vz_target = self.z_control.evaluate(delta_t, self.z_target - z)
        force = self.z_vel_control.evaluate(delta_t, self.vz_target - zV)
        #dati z
        self.z_target_data.append(self.z_target)
        self.z_data.append(z)
        self.vz_target_data.append(self.vz_target)
        self.vz_data.append(zV)
        self.z_error_data.append(self.z_target - z)
        self.vz_error_data.append(self.vz_target - zV)
        #controllo sulle x
        self.vx_target = self.x_control.evaluate(delta_t, self.x_target - x,x)
        self.pitch_target = self.x_vel_control.evaluate(delta_t, self.vx_target - xV,xV)
        #dati x
        self.x_target_data.append(self.x_target)
        self.x_data.append(x)
        self.vx_target_data.append(self.vx_target)
        self.vx_data.append(xV)
        self.x_error_data.append(self.x_target - x)
        self.vx_error_data.append(self.vx_target - xV)    
        #controllo sulle y
        self.vy_target = self.y_control.evaluate(delta_t, self.y_target - y,y)
        self.roll_target = - self.y_vel_control.evaluate(delta_t, self.vy_target - yV,yV)
        #dati y
        self.y_target_data.append(self.y_target)
        self.y_data.append(y)
        self.vy_target_data.append(self.vy_target)
        self.vy_data.append(yV)
        self.y_error_data.append(self.y_target - y)
        self.vy_error_data.append(self.vy_target - yV)
        
        #controllo roll
        self.roll_rate_target = self.roll_control.evaluate(delta_t, self.roll_target - roll)
        _roll = self.w_roll_control.evaluate(delta_t, self.roll_rate_target - roll_rate)
        
        #controllo pitch
        self.pitch_rate_target = self.pitch_control.evaluate(delta_t, self.pitch_target - pitch)
        _pitch = self.w_pitch_control.evaluate(delta_t, self.pitch_rate_target - pitch_rate)

        return force + _roll - _pitch, force - _roll - _pitch,\
        force - _roll+ _pitch, force + _roll + _pitch
