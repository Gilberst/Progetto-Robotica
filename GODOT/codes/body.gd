extends RigidBody3D

@onready var body_mesh = $Body_mesh
@onready var L = body_mesh.get_size()
@onready var p1 = Vector3(L.x/2.0,0,L.z/2.0)
@onready var p2 = Vector3(-L.x/2.0,0,L.z/2.0)
@onready var p3 = Vector3(-L.x/2.0,0,-L.z/2.0)
@onready var p4 = Vector3(L.x/2.0,0,-L.z/2.0)
var f1 = Vector3(0,0,0)
var f2 = Vector3(0,0,0)
var f3 = Vector3(0,0,0)
var f4 = Vector3(0,0,0)

var initial_position
var initial_rotation
var initial_velocity
var initial_angular_velocity
var perform_reset : bool = false

# Called when the node enters the scene tree for the first time.
func _ready():
	initial_position = global_position
	initial_rotation = global_rotation
	initial_velocity = linear_velocity
	initial_angular_velocity = angular_velocity

func _physics_process(delta: float) -> void:
	self.apply_local_force(f1, p1)
	self.apply_local_force(f2, p2)
	self.apply_local_force(f3, p3)
	self.apply_local_force(f4, p4)

func apply_local_force(force: Vector3, pos: Vector3):
	var global_force = global_transform.basis * force
	var global_pos = global_transform * pos
	var offset = global_pos - global_position
	apply_force(global_force, offset)

func set_forces(_f1,_f2,_f3,_f4):
	f1 = Vector3(0,_f1,0)
	f2 = Vector3(0,_f2,0)
	f3 = Vector3(0,_f3,0)
	f4 = Vector3(0,_f4,0)

func get_pose():
	return [global_position, global_rotation]

func get_velocity():
	return [linear_velocity, angular_velocity]
