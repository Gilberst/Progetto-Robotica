extends Node3D

@onready var x_label: Label = $"../X_lab"
@onready var y_label: Label = $"../Y_lab"
@onready var z_label: Label = $"../Z_lab"
@onready var rX_lab: Label = $"../X_rot_lab"
@onready var rY_lab: Label = $"../Y_rot_lab"
@onready var rZ_lab: Label = $"../Z_rot_lab"
var body

func _ready():
	body = get_node("body")
	dds.subscribe("f1")
	dds.subscribe("f2")
	dds.subscribe("f3")
	dds.subscribe("f4")

func _process(delta: float) -> void:
	var pose = body.get_pose()
	var vel = body.get_velocity()
	var pos = pose[0]
	var att = pose[1]
	var lin_vel = vel[0]
	var rot_vel = vel[1]
	
	x_label.text = "X : %.3f" % [pos.z]
	y_label.text = "Y : %.3f" % [pos.x]
	z_label.text = "Z : %.3f" % [pos.y]
	
	rX_lab.text = "X_Rotation : %.3f" % [rad_to_deg(att.z)]
	rY_lab.text = "Y_Rotation : %.3f" % [rad_to_deg(att.x)]
	rZ_lab.text = "Z_Rotation : %.3f" % [rad_to_deg(att.y)]
	
	# positions
	dds.publish("X", dds.DDS_TYPE_FLOAT, pos.z)
	dds.publish("Y", dds.DDS_TYPE_FLOAT, pos.x)
	dds.publish("Z", dds.DDS_TYPE_FLOAT, pos.y)
	
	# euler angles
	dds.publish("X_Ang", dds.DDS_TYPE_FLOAT, att.z)
	dds.publish("Y_Ang", dds.DDS_TYPE_FLOAT, att.x)
	dds.publish("Z_Ang", dds.DDS_TYPE_FLOAT, att.y)
	
	# linear speeds
	dds.publish("X_vel", dds.DDS_TYPE_FLOAT, lin_vel.z)
	dds.publish("Y_vel", dds.DDS_TYPE_FLOAT, lin_vel.x)
	dds.publish("Z_vel", dds.DDS_TYPE_FLOAT, lin_vel.y)

	# angular speeds
	dds.publish("X_VAng", dds.DDS_TYPE_FLOAT, rot_vel.z)
	dds.publish("Y_VAng", dds.DDS_TYPE_FLOAT, rot_vel.x)
	dds.publish("Z_VAng", dds.DDS_TYPE_FLOAT, rot_vel.y)
	
	dds.publish("tick", dds.DDS_TYPE_FLOAT, delta)
	var f1 = dds.read("f1")
	var f2 = dds.read("f2")
	var f3 = dds.read("f3")
	var f4 = dds.read("f4")
	body.set_forces(f1,f2,f3,f4)
