"""
IFC Compliance Checker — Space and Storey naming check.
"""

import ifcopenshell


def check_spaces(model: ifcopenshell.file, **kwargs) -> list[dict]:
    """
    Check that all IfcSpace elements have a name.

    Args:
        model: An ifcopenshell.file object representing the IFC model
        **kwargs: Additional parameters (unused)

    Returns:
        List of result dicts following the required schema
    """
    results = []
    spaces = model.by_type("IfcSpace")

    for space in spaces:
        name = space.Name
        has_name = bool(name)
        long_name = getattr(space, "LongName", None)
        results.append({
            "element_id": space.GlobalId,
            "element_type": "IfcSpace",
            "element_name": name or f"Space #{space.id()}",
            "element_name_long": long_name if isinstance(long_name, str) else None,
            "check_status": "pass" if has_name else "fail",
            "actual_value": name if has_name else "No name",
            "required_value": "Named space",
            "comment": None if has_name else "IfcSpace must have a Name for identification",
            "log": None,
        })

    unnamed = sum(1 for r in results if r["check_status"] == "fail")
    results.append({
        "element_id": None,
        "element_type": "Summary",
        "element_name": "Space Name Check",
        "element_name_long": None,
        "check_status": "pass" if unnamed == 0 else "fail",
        "actual_value": str(len(spaces)),
        "required_value": "All spaces named",
        "comment": f"Found {len(spaces)} space(s); {unnamed} unnamed",
        "log": None,
    })

    return results
