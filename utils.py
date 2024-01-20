def object_to_dict(obj: object) -> dict:
    if hasattr(obj, "__dict__"):
        obj_dict = obj.__dict__
        for key, val in obj_dict.items():
            if isinstance(val, list):
                obj_dict[key] = [object_to_dict(v) for v in val]
            else:
                obj_dict[key] = object_to_dict(val)
        return obj_dict
    else:
        return obj