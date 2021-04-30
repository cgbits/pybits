from __future__ import annotations

from typing import Dict, Any, List


def trim_dict(item: Dict[str, Any]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}

    for key, value in item.items():
        if isinstance(value, dict):
            result[key] = "{...}"
        elif isinstance(value, list):
            result[key] = "[...]"
        else:
            result[key] = value

    return result


def trim_list(items: List[Any]) -> List[Any]:
    result: List[Any] = []

    for item in items:
        if isinstance(item, dict):
            dict_item: Dict[str, Any] = item

            result.append(trim_dict(dict_item))
        elif isinstance(item, list):
            result.append("[...]")
        else:
            result.append(item)

    return result
