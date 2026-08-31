extends Node3D
@onready var body_self=$scatola
var active=true
func _ready() -> void:
	body_self.contact_monitor = true
	body_self.max_contacts_reported = 10
	body_self.body_entered.connect(_on_body_entered)
func take():
		self.visible=false
		active=false
		body_self.freeze = true
		body_self.sleeping = true
		
func release(pose: Vector3):
		self.global_position=pose
		self.visible=true
		active=true
		body_self.freeze = false
		body_self.sleeping = false
		
func _on_body_entered(body):
	if body.is_in_group("deposit") and active:
		var dep=body.get_parent()
		dep.update_value(1)
		dds.publish("aline",dds.DDS_TYPE_INT,3)
		self.queue_free()
