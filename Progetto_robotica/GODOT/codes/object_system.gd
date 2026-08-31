extends Node3D
@export var objectScene: PackedScene
@onready var spawnPoints = $points
@onready var container = $objectContainer
@onready var deposit=  $"../deposito"
var timing=5.0#do 5 secondi di comunicazione
const maxObj=5
var phase:int=0
var obj
var release_pos:Vector3=Vector3(0.0,4.0,0.0)
var positions:Array[int]=[0,0,0,0,0]

func _ready():
	generate_object()
	dds.subscribe("action")

func _process(delta: float) -> void:
	if timing>=0:
		publish_positions()
		timing-=delta
	var tmp=dds.read("action")
	if phase==0:
		if tmp==1:
			obj=container.get_child(0)
			obj.take()
			phase=1
			dds.publish("aline",dds.DDS_TYPE_INT,1)
	elif phase==1:
		if tmp==2:
			dds.publish("aline",dds.DDS_TYPE_INT,2)
			phase=2
	elif phase==2:
		if tmp==3:
			obj.release(release_pos)
			phase=3
	elif phase==3:
		if tmp==4:
			obj=null
			tmp=0
			phase=0
		
func publish_positions():
	for i in range(5):
		dds.publish("item_position_" + str(i + 1),dds.DDS_TYPE_INT,positions[i])

func generate_object():
	var points=spawnPoints.get_children()
	points.shuffle()
	for i in range(maxObj):
		var item= objectScene.instantiate()
		container.add_child(item)
		item.global_position=points[i].global_position
		positions[i]=points[i].name.to_int()
		
