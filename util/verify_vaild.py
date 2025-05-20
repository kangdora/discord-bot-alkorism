def is_valid_response(data: dict) -> bool:
    if not data or data.get("count", 0) != 1:
        return False
    items = data.get("items", [])
    if not items or not isinstance(items, list):
        return False
    required_fields = {"handle", "rating", "tier", "solvedCount"}
    return required_fields.issubset(items[0].keys())

def parse_user_info(data: dict):
    item = data["items"][0]
    return {
        "boj_id": item["handle"],
        "rating": item["rating"],
        "tier": item["tier"],
        "solved_count": item["solvedCount"]
    }

def is_valid_id(id:str) -> bool:
    if id.isdigit():
        return False

    return True