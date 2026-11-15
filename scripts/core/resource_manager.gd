extends Node
## ResourceManager — tiny load cache so scenes/scripts are loaded once.
var _cache: Dictionary = {}

func load_resource(path: String) -> Resource:
    if _cache.has(path):
        return _cache[path]
    var res: Resource = load(path)
    if res != null:
        _cache[path] = res
    else:
        push_error("ResourceManager: cannot load " + path)
    return res

func preload_scene(path: String) -> PackedScene:
    return load_resource(path) as PackedScene

func clear_cache() -> void:
    _cache.clear()

func cached_count() -> int:
    return _cache.size()
