extends CharacterBody2D

@export var player_index = 1
var speed = -1
# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	position.y += speed
		
	if position.y >= 380:
			
		Global.end_round(player_index)
