extends Node3D
@onready var label: Label = $"../Item_taken"
var value:int=0
func _ready() -> void:
	update_value(0)
func update_value(added: int):
	value=value+added
	label.text="Oggetti presi : %d" %[value]
