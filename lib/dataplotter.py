from matplotlib import pyplot
from pathlib import Path
import networkx as net
import sys
sys.path.append("../../")
from path_planner.position_calculator import *

class data_plot:
    def __init__(self) -> None:
        self.dir = Path(__file__).resolve().parent
        self.save_dir= self.dir/"plot"
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.delta_t=0.01
        self._plt=pyplot
        self._calc=position_calculator()
        #valori posizione
        self.r_x_data=[]
        self.r_y_data=[]
        self.r_z_data=[]
        self.target_x_data=[]
        self.target_y_data=[]
        self.target_z_data=[]
        #valori velocità
        self.v_z_data=[]
        self.v_x_data=[]
        self.v_y_data=[]
        self.target_v_z_data=[]
        self.target_v_x_data=[]
        self.target_v_y_data=[]
        #roll and pitch
        self.roll_data=[]
        self.pitch_data=[]
        #valori grafico real time
        self.x_data=[]
        self.y_data=[]
        self.point_x_data=[]
        self.point_y_data=[]
        self.figure=None
        self.axes=None
        self.line=None
        self.drone=None
        self.points=None

    def plot_drone_path(self):
        self._plt.ion()

        self.figure,self.axes=self._plt.subplots()
        self.axes.grid(True)
        self.axes.set_xlim(-10,10)
        self.axes.set_xlabel('X')
        self.axes.set_ylim(-10,10)
        self.axes.set_ylabel('Y', rotation=0)

        self.line, =self.axes.plot([],[],linestyle='--')
        self.drone, = self.axes.plot([],[],marker='X')
        self.points, =self.axes.plot([],[],marker='o')
        self.figure.show()

    def update(self,x,y,isPoint):

        if self.figure is None:
            self.plot_drone_path()
        if self.line is not None:
            self.x_data.append(x)
            self.y_data.append(y)
            self.line.set_data(self.x_data, self.y_data)
        if self.drone is not None:
            self.drone.set_data([x],[y])
        if isPoint and self.points is not None:
            self.point_x_data.append(x)
            self.point_y_data.append(y)
            self.points.set_data(self.point_x_data, self.point_y_data)
        if self.axes is not None:
            self.axes.relim()
            self.axes.autoscale_view()
        if self.figure is not None:
            self.figure.canvas.draw_idle()
            self.figure.canvas.flush_events()

    def save_drone_path(self):
        self._plt.ioff()
        self._plt.savefig(self.save_dir/'drone_path.png')
        self._plt.close(self.figure)
    
    def save_drone_data(self,vz,vx,vy,roll,pitch):
        #zv=abs(vz)
        #xv=abs(vx)
        #yv=abs(vy)
        self.v_z_data.append(vz)
        self.v_x_data.append(vx)
        self.v_y_data.append(vy)
        self.roll_data.append(roll)
        self.pitch_data.append(pitch)

    def graph_plot(self,graph,calc):
        grafo=net.Graph()
        for node in graph.grafo_unw:
            grafo.add_node(node)
        for node, adjs in graph.grafo_unw.items():
            for adj in adjs:
                grafo.add_edge(node,adj)
        pos_list={node:calc.convert_in_coordinates(node) for node in graph.grafo_unw}
        figure, axes = self._plt.subplots()

        net.draw(grafo,pos_list,axes,with_labels=True,node_size=600,font_size=15,edge_color="black")
        axes.set_xlabel("X")
        axes.set_ylabel("Y")
        axes.grid(True)
        axes.axis("equal")
        figure.savefig(self.save_dir/"Graph.png")
        self._plt.close(figure)

    def map_plot(self,positions):
        fig,axes=self._plt.subplots()
        axes.grid(True)
        x=[]
        y=[]
        for i in range(len(positions)):
            values=self._calc.convert_in_coordinates(positions[i])
            if values is not None:
                #valori fra Python e Godot sono invertiti di posizione
                x.append(values[1])
                y.append(values[0])
        axes.set_xlim(-10,10)
        axes.set_ylim(-10,10)
        axes.set_xlabel('X')
        axes.set_ylabel('Y', rotation=0)
        self._plt.scatter(0,0,marker='X')
        self._plt.scatter(x, y, marker='s')
        fig.savefig(self.save_dir/'map.png')
        self._plt.close(fig)

    def plot_drone_values(self,drone):
        r_values={
            "roll":self.roll_data,
            "pitch":self.pitch_data,
        }
        self._plotting(drone.z_data,"controllo_z",drone.z_target_data)
        self._plotting(drone.x_data,"controllo_x",drone.x_target_data)
        self._plotting(drone.y_data,"controllo_y",drone.y_target_data)

        self._plotting(self.v_z_data,"controllo_velocità_z",drone.vz_target_data)
        self._plotting(self.v_x_data,"controllo_velocità_x",drone.vx_target_data)
        self._plotting(self.v_y_data,"controllo_velocità_y",drone.vy_target_data)

        self._err_plotting(drone.z_error_data,"errori_z","z")
        self._err_plotting(drone.x_error_data,"errori_x","x")
        self._err_plotting(drone.y_error_data,"errori_y","y")

        self._err_plotting(drone.vz_error_data,"errori_velocità_z","z")
        self._err_plotting(drone.vx_error_data,"errori_velocità_x","x")
        self._err_plotting(drone.vy_error_data,"errori_velocità_y","y")

        for name,val in r_values.items():
            fig,ax=self._plt.subplots()
            time = [i * self.delta_t for i in range(len(val))]
            ax.plot(time,val)
            ax.set_title(name)
            ax.set_xlabel("tempo")
            ax.set_ylabel(f"{name}")
            fig.savefig(self.save_dir/f"{name}.png")
            self._plt.close(fig)

    def _plotting(self,value,name,targets):  
            fig,ax=self._plt.subplots()
            time = [i * self.delta_t for i in range(len(value))]
            ax.plot(time,targets,label="valori target")
            ax.plot(time,value,label="valori real")
            ax.set_title(name)
            ax.set_xlabel("tempo")
            ax.set_ylabel("valore")
            fig.savefig(self.save_dir/f"{name}.png")
            self._plt.close(fig)
    def _err_plotting(self,error,name,dat):
        fig,ax=self._plt.subplots()
        time = [i * self.delta_t for i in range(len(error))]
        ax.plot(time,error,label="errore nel tempo")
        ax.set_title(name)
        ax.set_xlabel("tempo(centesimi di secondo)")
        ax.set_ylabel(f"valore di errore sulle_{dat}")
        fig.savefig(self.save_dir/f"{name}.png")
        self._plt.close(fig)

