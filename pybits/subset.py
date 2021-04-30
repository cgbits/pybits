from fnmatch import fnmatch

from typing import Dict, List, Any

from pybits.exceptions import (
    ComparisonBaseError,
    ComparisonError,
    ComparisonErrorInfo,
)
from pybits.trim import trim_dict, trim_list


def dict_assert_is_subset(
    subset: Dict[str, Any], superset: Dict[str, Any], depth: int = 0
) -> bool:
    # compare all keys
    try:
        for key, value in subset.items():
            if isinstance(value, dict):
                dict_value: Dict[str, Any] = value
                # compare value recursive with assert_is_subset
                # if value is an instance of dict
                superset_value_dict: Dict[str, Any] = superset.get(key, {})

                dict_assert_is_subset(
                    dict_value, superset_value_dict, depth + 1
                )
            elif isinstance(value, list):
                list_value: List[Any] = value
                # compare value recursive with listbits.assert_is_subset
                # if value is an instance of list
                superset_value_list: List[Any] = superset.get(key, [])

                list_assert_is_subset(
                    list_value, superset_value_list, depth + 1
                )
            elif isinstance(value, str):
                # compare value
                # if value is neither dict or list
                superset_value_str: str = superset.get(key, "")

                if not fnmatch(superset_value_str, value):
                    raise ComparisonError(
                        f"Excpected '{value}' to match '{superset_value_str}'",
                        depth,
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
            f"{trim_dict(subset)} is no subset of {trim_dict(superset)}: {e}",
            depth,
        )

    # all compared keys must return true
    # for the input to be a subset of superset
    return True


def dict_is_subset(subset: Dict[str, Any], superset: Dict[str, Any]) -> bool:
    try:
        return dict_assert_is_subset(subset, superset)
    except ComparisonBaseError:
        return False


def list_assert_is_subset(
    subset: List[Any], superset: List[Any], depth: int = 0
) -> bool:
    try:
        for item in subset:
            if isinstance(item, dict):
                dict_item: Dict[str, Any] = item

                # compare value recursive with dictbits.assert_is_subset
                # if value is an instance of dict
                matches = False
                local_exceptions: List[ComparisonBaseError] = []

                for superset_item in superset:
                    # compare every value of superset with item
                    try:
                        dict_assert_is_subset(
                            dict_item, superset_item, depth + 1
                        )

                        matches = True

                        break
                    except ComparisonBaseError as e:
                        local_exceptions.append(e)

                if not matches and local_exceptions:
                    # raise error from likeliest path
                    raise sorted(local_exceptions, key=lambda x: x.depth).pop()

            elif isinstance(item, list):
                list_item: List[Any] = item
                # compare value recursive with assert_is_subset
                # if value is an instance of list
                matches = False
                local_exceptions = []

                for superset_item in superset:
                    # compare every value of superset with item
                    try:
                        list_assert_is_subset(
                            list_item, superset_item, depth + 1
                        )

                        matches = True

                        break
                    except ComparisonBaseError as e:
                        local_exceptions.append(e)

                if not matches and local_exceptions:
                    # raise error from likeliest path
                    raise sorted(local_exceptions, key=lambda x: x.depth).pop()
            elif isinstance(item, str):
                # compare value
                # if value is neither dict or list
                if not any([fnmatch(x, item) for x in superset]):
                    raise ComparisonError(
                        f"Expected '{item}' to be contained in '{trim_list(superset)}'",
                        depth,
                    )
            else:
                # compare every value of superset with item
                # if value is neither dict or list
                if not any([item in x for x in superset]):
                    # raise exceptions.ComparisonError
                    # if no value from superset equals item
                    raise ComparisonError(
                        f"Expected '{item}' to be contained in '{trim_list(superset)}'",
                        depth,
                    )
    except ComparisonError as e:
        raise ComparisonErrorInfo(
            f"{trim_list(subset)} is no subset of {trim_list(superset)}: {e}",
            depth,
        )

    return True


def list_is_subset(subset: List[Any], superset: List[Any]) -> bool:
    try:
        return list_assert_is_subset(subset, superset)
    except ComparisonBaseError:
        return False
