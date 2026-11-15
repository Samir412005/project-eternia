extends Node3D
## PlayerAnimationController — procedural animation for the PROTOTYPE mesh.
## No imported animations exist yet (see ASSET LIMITATIONS in README).
## Walk/run swing the primitive limbs; idle breathes; jump tucks.
var player: CharacterBody3D = null
var body: MeshInstance3D = null
var arm_l: MeshInstance3D = null
var arm_r: MeshInstance3D = null
var leg_l: MeshInstance3D = null
var leg_r: MeshInstance3D = null
var anim_time: float = 0.0

func _ready() -> void:
    player = get_parent() as CharacterBody3D
    body = get_node_or_null("Body") as MeshInstance3D
    arm_l = get_node_or_null("ArmL") as MeshInstance3D
    arm_r = get_node_or_null("ArmR") as MeshInstance3D
    leg_l = get_node_or_null("LegL") as MeshInstance3D
    leg_r = get_node_or_null("LegR") as MeshInstance3D

func _process(delta: float) -> void:
    if player == null:
        return
    var speed: float = Vector2(player.velocity.x, player.velocity.z).length()
    anim_time += delta * (2.0 + speed * 1.6)
    var swing: float = sin(anim_time * 3.0) * clampf(speed / 8.0, 0.0, 1.0) * 0.7
    if leg_l: leg_l.rotation.x = swing
    if leg_r: leg_r.rotation.x = -swing
    if arm_l: arm_l.rotation.x = -swing * 0.8
    if arm_r: arm_r.rotation.x = swing * 0.8
    if body:
        var bob: float = absf(sin(anim_time * 3.0)) * 0.05 * clampf(speed / 8.0, 0.0, 1.0)
        body.position.y = 0.95 + bob
        if not player.is_on_floor():
            body.position.y = 1.0
