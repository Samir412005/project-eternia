extends Node3D
## WorldManager — builds the Phase 1 vertical-slice environment at runtime
## from primitives (ground, platforms, ruins, trees, shrine, torches).
## This is a real 3D environment, not a backdrop: every piece has collision
## where the player can stand on it. World size: 60 x 60 m test valley.
const SIZE := 60.0

func _ready() -> void:
    _build_ground()
    _build_platforms()
    _build_ruins()
    _build_trees()
    _build_shrine()
    _build_torches()

func _mat(color: Color, rough: float = 0.9) -> StandardMaterial3D:
    var m := StandardMaterial3D.new()
    m.albedo_color = color
    m.roughness = rough
    return m

func _box(name: String, pos: Vector3, size: Vector3, mat: Material) -> StaticBody3D:
    var body := StaticBody3D.new()
    body.name = name
    body.position = pos
    var mesh := MeshInstance3D.new()
    var box := BoxMesh.new()
    box.size = size
    box.material = mat
    mesh.mesh = box
    body.add_child(mesh)
    var col := CollisionShape3D.new()
    var shape := BoxShape3D.new()
    shape.size = size
    col.shape = shape
    body.add_child(col)
    add_child(body)
    return body

func _build_ground() -> void:
    var body := StaticBody3D.new()
    body.name = "Ground"
    var mesh := MeshInstance3D.new()
    var plane := PlaneMesh.new()
    plane.size = Vector2(SIZE, SIZE)
    plane.material = _mat(Color(0.23, 0.35, 0.2))
    mesh.mesh = plane
    body.add_child(mesh)
    var col := CollisionShape3D.new()
    var shape := BoxShape3D.new()
    shape.size = Vector3(SIZE, 1.0, SIZE)
    col.shape = shape
    col.position.y = -0.5
    body.add_child(col)
    add_child(body)

func _build_platforms() -> void:
    var stone := _mat(Color(0.45, 0.43, 0.4))
    _box("PlatformNorth", Vector3(0, 0.5, -20), Vector3(12, 1, 8), stone)
    _box("PlatformEast", Vector3(18, 0.75, 6), Vector3(8, 1.5, 8), stone)
    _box("StepNorth", Vector3(0, 0.25, -15), Vector3(4, 0.5, 2), stone)

func _build_ruins() -> void:
    var stone := _mat(Color(0.55, 0.52, 0.48))
    var dark := _mat(Color(0.32, 0.3, 0.28))
    var positions: Array = [
        Vector3(-14, 1.5, -10), Vector3(-14, 1.5, -6), Vector3(-10, 2.0, -12),
        Vector3(12, 1.0, -16), Vector3(16, 1.0, -16),
        Vector3(-18, 1.0, 14), Vector3(14, 1.25, 18),
    ]
    for i in range(positions.size()):
        var h: float = 3.0 if i % 2 == 0 else 2.0
        _box("Pillar%d" % i, positions[i], Vector3(1.2, h, 1.2), stone if i % 2 == 0 else dark)
    _box("BrokenWall", Vector3(-8, 1.0, -18), Vector3(10, 2, 1), dark)

func _build_trees() -> void:
    var trunk_mat := _mat(Color(0.35, 0.25, 0.16))
    var leaf_mat := _mat(Color(0.16, 0.4, 0.18))
    var spots: Array = [
        Vector3(-22, 0, -18), Vector3(-24, 0, 2), Vector3(-20, 0, 20),
        Vector3(22, 0, -8), Vector3(24, 0, 12), Vector3(8, 0, 24),
        Vector3(-6, 0, 24), Vector3(20, 0, -22),
    ]
    for i in range(spots.size()):
        var tree := StaticBody3D.new()
        tree.name = "Tree%d" % i
        tree.position = spots[i]
        var trunk := MeshInstance3D.new()
        var cyl := CylinderMesh.new()
        cyl.top_radius = 0.25
        cyl.bottom_radius = 0.4
        cyl.height = 2.4
        cyl.material = trunk_mat
        trunk.mesh = cyl
        trunk.position.y = 1.2
        tree.add_child(trunk)
        var col := CollisionShape3D.new()
        var shape := CylinderShape3D.new()
        shape.radius = 0.4
        shape.height = 2.4
        col.shape = shape
        col.position.y = 1.2
        tree.add_child(col)
        var leaves := MeshInstance3D.new()
        var cone := CylinderMesh.new()
        cone.top_radius = 0.0
        cone.bottom_radius = 2.0
        cone.height = 3.2
        cone.material = leaf_mat
        leaves.mesh = cone
        leaves.position.y = 3.8
        tree.add_child(leaves)
        add_child(tree)

func _build_shrine() -> void:
    var shrine_script: Script = load("res://scripts/gameplay/shrine.gd")
    var shrine := Area3D.new()
    shrine.name = "AncientShrine"
    shrine.set_script(shrine_script)
    shrine.add_to_group("interactable")
    shrine.position = Vector3(0, 0, -8)
    add_child(shrine)
    var base := MeshInstance3D.new()
    var box := BoxMesh.new()
    box.size = Vector3(2.4, 1.0, 2.4)
    box.material = _mat(Color(0.62, 0.58, 0.5))
    base.mesh = box
    base.position.y = 0.5
    shrine.add_child(base)
    var crystal := MeshInstance3D.new()
    var prism := PrismMesh.new()
    prism.size = Vector3(0.9, 1.6, 0.9)
    var glow := StandardMaterial3D.new()
    glow.albedo_color = Color(0.45, 0.75, 1.0)
    glow.emission_enabled = true
    glow.emission = Color(0.35, 0.6, 1.0)
    glow.emission_energy_multiplier = 1.5
    prism.material = glow
    crystal.mesh = prism
    crystal.position.y = 1.9
    shrine.add_child(crystal)
    var col := CollisionShape3D.new()
    var shape := BoxShape3D.new()
    shape.size = Vector3(3.5, 3.5, 3.5)
    col.shape = shape
    col.position.y = 1.5
    shrine.add_child(col)
    var light := OmniLight3D.new()
    light.position.y = 2.4
    light.light_color = Color(0.5, 0.7, 1.0)
    light.light_energy = 1.2
    light.omni_range = 8.0
    shrine.add_child(light)

func _build_torches() -> void:
    for i in range(2):
        var pos: Vector3 = Vector3(-3 + i * 6, 0, -9.5)
        var torch := Node3D.new()
        torch.name = "Torch%d" % i
        torch.position = pos
        var pole := MeshInstance3D.new()
        var cyl := CylinderMesh.new()
        cyl.top_radius = 0.08
        cyl.bottom_radius = 0.12
        cyl.height = 1.6
        cyl.material = _mat(Color(0.3, 0.22, 0.14))
        pole.mesh = cyl
        pole.position.y = 0.8
        torch.add_child(pole)
        var flame := OmniLight3D.new()
        flame.position.y = 1.8
        flame.light_color = Color(1.0, 0.6, 0.25)
        flame.light_energy = 0.9
        flame.omni_range = 6.0
        torch.add_child(flame)
        add_child(torch)
