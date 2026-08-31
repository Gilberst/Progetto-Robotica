import sys
import time
sys.path.append("../../")
import math
from movement.drone import *
from lib.ComunicationSystem.dds_sys import *
from path_planner.path_planner import *
from path_planner.position_calculator import *
from lib.dataplotter import *

def main():
    #inizializzazione
    targets=startDDS()
    drone = Drone()
    p_planner=planner()
    pos_setter=position_calculator()
    plotter=data_plot()
    drone.z_target=5.0
    delta_t=0.01
    # variabile di gestione fase comunicazione
    set_aline=0
    
    path_list=[]
    return_list=[]

    target=0
    i=0

    plotter.map_plot(targets)
    plotter.plot_drone_path()
    plotter.graph_plot(p_planner,pos_setter)
    while True:

        target=targets[i]
        print("current_target: ",target)
        (path_list,return_list)=p_planner.Shortest_path(0,target)     
        i=i+1

        movment_loop(path_list,pos_setter,delta_t,drone,plotter)
        drone.x_target=drone.x
        drone.y_target=drone.y
        drone.z_target=drone.z_target-4.0#oggetti sono circa 1m*1m*1m

        #loop movimento discesa #1
        move_drone(delta_t,drone,plotter)
        time.sleep(delta_t)

        while abs(drone.z-drone.z_target)>0.1:
            move_drone(delta_t,drone,plotter)
            time.sleep(delta_t)

        sentDDS('action',1,dds.DDS_TYPE_INT)
        set_aline=dds.read('aline')
        
        while set_aline is None or set_aline!=1:
            move_drone(delta_t,drone,plotter)#impedisce al drone di cadere
            set_aline=dds.read('aline')
            time.sleep(delta_t)

        sentDDS("action",2,dds.DDS_TYPE_INT)
        set_aline=dds.read('aline')

        while set_aline is None or set_aline!=2:
            move_drone(delta_t,drone,plotter)
            set_aline=dds.read('aline')
            time.sleep(delta_t)

        drone.z_target=5.0
        
        while abs(drone.z-drone.z_target)>0.2:
            #evito di far partire il movimento orizontale fino a quasi completamento movimento verticale
            move_drone(delta_t,drone,plotter)
            time.sleep(delta_t)
        sentDDS("return",0,dds.DDS_TYPE_INT)
        movment_loop(return_list,pos_setter,delta_t,drone,plotter)
        sentDDS("return",1,dds.DDS_TYPE_INT)
        sentDDS("action",3,dds.DDS_TYPE_INT)
        set_aline=dds.read('aline')

        while set_aline is None or set_aline!=3:
            move_drone(delta_t,drone,plotter)
            set_aline=dds.read('aline')
            time.sleep(delta_t)

        sentDDS("action",4,dds.DDS_TYPE_INT)
        drone.z_target=0

        while abs(drone.z-drone.z_target)>1.05:
            #distanza terreno-base decollo circa 1 metro
            move_drone(delta_t,drone,plotter)
            time.sleep(delta_t)

        reset_values(drone)
        time.sleep(delta_t*100)
        set_aline=None

        if i+1 >len(targets):
            plotter.plot_drone_values(drone)
            plotter.save_drone_path()
            sys.exit(0)#il programma ha finito


def movment_loop(path_list,pos_set,d_t,drone,plot):   

    next=False
    while path_list:
        if not next:
            pos_set.set_target(drone, path_list[0])
            next = True
        (x,y,z)=move_drone(d_t,drone,plot)
        if abs(x-drone.x_target)<0.1 and abs(y-drone.y_target)<0.1:
            plot.update(x,y,True)
            path_list.pop(0)
            next=False
            time.sleep(d_t)
            continue
        else:
            plot.update(x,y,False)
            time.sleep(d_t)
            continue


def startDDS():
    global dds 
    dds= DDS()
    dds.start('127.0.0.1', 4444)
    dds.subscribe(['X','Y','Z','X_Ang','Y_Ang','Z_Ang','X_vel','Y_vel','Z_vel','X_VAng','Y_VAng','Z_VAng', 'tick', \
                   'aline','item_position_1', 'item_position_2', 'item_position_3', 'item_position_4', 'item_position_5'])
    dds.wait('tick')
    return target_set(5)
    


def sentDDS(name: str, value, type):
    dds.publish(name, value, type)


def readDDS():
    x=dds.read('X')
    y=dds.read('Y')
    z=dds.read('Z')
    xv=dds.read('X_vel')
    yv=dds.read('Y_vel')
    zv=dds.read('Z_vel')
    roll=dds.read('X_Ang')
    rollRate=dds.read('X_VAng')
    pitch=dds.read('Y_Ang')
    pitchRate=dds.read('Y_VAng')
    return (x,y,z,xv,yv,zv,roll,rollRate,pitch,pitchRate)


def reset_values(drone):
    sentDDS('f1',0.0,dds.DDS_TYPE_FLOAT)
    sentDDS('f2',0.0,dds.DDS_TYPE_FLOAT)
    sentDDS('f3',0.0,dds.DDS_TYPE_FLOAT)
    sentDDS('f4',0.0,dds.DDS_TYPE_FLOAT)
    sentDDS('action',0,dds.DDS_TYPE_INT)
    drone.z_target=5.0

#riceve le posizioni degli oggetti el conserva in una lista
def target_set(value):
    targets=[]

    for i in range(1,value+1):
        var=dds.read('item_position_'+str(i))
        while var is None:
                time.sleep(0.01)
                var=dds.read('item_position_'+str(i))
        targets.append(var)

    return targets

#fa muovere il drone, restituisce le coordinate del drone
def move_drone(delta_t, drone,plot):
    (x,y,z,vx,vy,vz,roll,r_rate,pitch,p_rate)=readDDS()
    while x is None or y is None:
        time.sleep(delta_t)
        (x,y,z,vx,vy,vz,roll,r_rate,pitch,p_rate)=readDDS()
    (f1,f2,f3,f4)=drone.evaluate(delta_t,z,vz,x,vx,y,vy,roll,r_rate,pitch,p_rate)
    sentDDS('f1',f1,dds.DDS_TYPE_FLOAT)
    sentDDS('f2',f2,dds.DDS_TYPE_FLOAT)
    sentDDS('f3',f3,dds.DDS_TYPE_FLOAT)
    sentDDS('f4',f4,dds.DDS_TYPE_FLOAT)
    plot.save_drone_data(vz,vx,vy,roll,pitch)
    return x,y,z

if __name__ == "__main__":
    main()