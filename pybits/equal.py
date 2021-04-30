from typing import Dict, List, Any

from pybits.exceptions import (
    ComparisonBaseError,
    ComparisonError,
    ComparisonErrorInfo,
)
from pybits.trim import trim_dict, trim_list


def list_assert_is_equal(
    subset: List[Any], superset: List[Any], depth: int = 0
) -> bool:
    try:
        if len(superset) != len(subset):
            # early return false
            # if length of superset and subset ar not equal
            raise ComparisonError(f"Excpected length to be equal")

        # compare all items
        for index, item in enumerate(subset):
            if isinstance(item, dict):
                dict_item: Dict[str, Any] = item

                # compare value recursive with dictbits.assert_is_equal
                # if value is an instance of dict
                superset_value_dict: Dict[str, Any] = superset[index]

                dict_assert_is_equal(dict_item, superset_value_dict, depth + 1)
            elif isinstance(item, list):
                list_item: List[Any] = item

                # compare value recursive with assert_is_equal
                # if value is an instance of list
                superset_value_list: List[Any] = superset[index]

                list_assert_is_equal(list_item, superset_value_list, depth + 1)
            else:
                # compare superset at index with item
                # if value is neither dict or list
                superset_value = superset[index]

                if item != superset_value:
                    raise ComparisonError(
                        f"Excpected '{item}' to be equal to '{superset_value}'",
                        depth,
                    )
    except ComparisonError as e:
        raise ComparisonErrorInfo(
            f"{trim_list(subset)} is not equal to {trim_list(superset)}: {e}",
            depth,
        )

    return True


def list_is_equal(subset: List[Any], superset: List[Any]) -> bool:
    try:
        return list_assert_is_equal(subset, superset)
    except ComparisonBaseError:
        return False


def dict_assert_is_equal(
    subset: Dict[str, Any], superset: Dict[str, Any], depth: int = 0
) -> bool:

    try:
        if len(list(superset.keys())) != len(list(subset.keys())):
            # early return false
            # if length of superset keys and subset keys ar not equal
            raise ComparisonError(f"Excpected length of keys to be equal")

        # compare all keys
        for key, value in subset.items():
            if isinstance(value, dict):
                dict_value: Dict[str, Any] = value

                # compare value recursive with assert_is_equal
                # if value is an instance of dict
                superset_value_dict: Dict[str, Any] = superset.get(key, {})

                dict_assert_is_equal(
                    dict_value, superset_value_dict, depth + 1
                )
            elif isinstance(value, list):
                list_value: List[Any] = value

                # compare value recursive with listbits.assert_is_equal
                # if value is an instance of list
                superset_value_list: List[Any] = superset.get(key, [])

                list_assert_is_equal(
                    list_value, superset_value_list, depth + 1
                )
            else:
                # compare value
                # if value is neither dict or list
                superset_value = superset.get(key)

                if value != superset_value:
                    raise ComparisonError(
                        f"Excpected '{value}' to be equal to '{superset_value}'",
                        depth,
                    )
    except ComparisonError as e:
        raise ComparisonErrorInfo(
            f"{trim_dict(subset)} is not equal to {trim_dict(superset)}: {e}",
            depth,
        )

    # all compared keys must return true
    # for the input to be a subset of superset
    return True


def dict_is_equal(subset: Dict[str, Any], superset: Dict[str, Any]) -> bool:
    try:
        return dict_assert_is_equal(subset, superset)
    except ComparisonBaseError:
        return False
