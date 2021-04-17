import fnmatch

from typing import Dict, List, Optional

from pybits import listbits, exceptions


def trim(item: Dict) -> Dict:
    result = {}

    for key, value in item.items():
        if isinstance(value, dict):
            result[key] = "{...}"
        elif isinstance(value, list):
            result[key] = "[...]"
        else:
            result[key] = value

    return result


def assert_is_equal(subset: Dict, superset: Dict, depth: int = 0) -> bool:
    try:
        if len(list(superset.keys())) != len(list(subset.keys())):
            # early return false
            # if length of superset keys and subset keys ar not equal
            raise exceptions.ComparisonError(
                f"Excpected length of keys to be equal"
            )

        # compare all keys
        results = []
        compare_exceptions = []

        for key, value in subset.items():
            if isinstance(value, dict):
                # compare value recursive with assert_is_equal
                # if value is an instance of dict
                superset_value_dict: Dict = superset.get(key, {})

                assert_is_equal(value, superset_value_dict, depth + 1)
            elif isinstance(value, list):
                # compare value recursive with listbits.assert_is_equal
                # if value is an instance of list
                superset_value_list: List = superset.get(key, [])

                listbits.assert_is_equal(value, superset_value_list, depth + 1)
            # elif isinstance(value, str):
            #     # compare value
            #     # if value is neither dict or list
            #     superset_value_str: str = superset.get(key, "")

            #     if not fnmatch.fnmatch(superset_value_str, value):
            #         raise exceptions.ComparisonError(
            #             f"Excpected '{value}' to match '{superset_value_str}'",
            #             depth,
            #         )
            else:
                # compare value
                # if value is neither dict or list
                superset_value = superset.get(key)

                if value != superset_value:
                    raise exceptions.ComparisonError(
                        f"Excpected '{value}' to be equal to '{superset_value}'",
                        depth,
                    )
    except exceptions.ComparisonError as e:
        raise exceptions.ComparisonErrorInfo(
            f"{trim(subset)} is not equal to {trim(superset)}: {e}", depth
        )

    # all compared keys must return true
    # for the input to be a subset of superset
    return True


def is_equal(subset: Dict, superset: Dict) -> bool:
    try:
        return assert_is_equal(subset, superset)
    except exceptions.ComparisonBaseError:
        return False


def assert_is_subset(subset: Dict, superset: Dict, depth: int = 0) -> bool:
    # compare all keys
    try:
        for key, value in subset.items():
            if isinstance(value, dict):
                # compare value recursive with assert_is_subset
                # if value is an instance of dict
                superset_value_dict: Dict = superset.get(key, {})

                assert_is_subset(value, superset_value_dict, depth + 1)
            elif isinstance(value, list):
                # compare value recursive with listbits.assert_is_subset
                # if value is an instance of list
                superset_value_list: List = superset.get(key, [])

                listbits.assert_is_subset(
                    value, superset_value_list, depth + 1
                )
            elif isinstance(value, str):
                # compare value
                # if value is neither dict or list
                superset_value_str: str = superset.get(key, "")

                if not fnmatch.fnmatch(superset_value_str, value):
                    raise exceptions.ComparisonError(
                        f"Excpected '{value}' to match '{superset_value_str}'",
                        depth,
                    )
            else:
                # compare value
                # if value is neither dict or list
                superset_value = superset.get(key)

                if value != superset_value:
                    raise exceptions.ComparisonError(
                        f"Excpected '{value}' to be equal to '{superset_value}'",
                        depth,
                    )
    except exceptions.ComparisonError as e:
        raise exceptions.ComparisonErrorInfo(
            f"{trim(subset)} is no subset of {trim(superset)}: {e}", depth
        )

    # all compared keys must return true
    # for the input to be a subset of superset
    return True


def is_subset(subset: Dict, superset: Dict) -> bool:
    try:
        return assert_is_subset(subset, superset)
    except exceptions.ComparisonBaseError:
        return False


def pick(
    item: Dict,
    include: Optional[List[str]] = None,
    exclude: Optional[List[str]] = None,
    childrens_attribute_name: str = "children",
    recursive: bool = True,
    depth: int = -1,
    path: str = "*",
    path_attribute_name: str = "",
) -> Dict:
    if include is None:
        include = list(item.keys())

    if exclude is None:
        exclude = []

    # list of item keys
    item_keys = list(item.keys())

    # remove childrens attribute name from include list
    if childrens_attribute_name in include:
        include.remove(childrens_attribute_name)

    result = {}

    # add included attributes
    for attribute_name in include:
        matches = [fnmatch.fnmatch(x, attribute_name) for x in item_keys]

        if any(matches):
            match_index = matches.index(True)
            matched_attribute_name = item_keys[match_index]

            result[matched_attribute_name] = item[matched_attribute_name]

    # remove excluded attributes
    for attribute_name in exclude:
        matches = [fnmatch.fnmatch(x, attribute_name) for x in result.keys()]

        if any(matches):
            match_index = matches.index(True)
            matched_attribute_name = item_keys[match_index]

            del result[matched_attribute_name]

    # add children
    if recursive:
        # make sure childrens attribute name exists in item keys
        if childrens_attribute_name in item_keys:
            children = []

            # make sure depth is either infinite or larger 0
            if depth == -1 or depth > 0:
                # decrease depth per recursive step
                if depth > 0:
                    depth -= 1

                children = item[childrens_attribute_name]

                if path != "*" or "/" in path:
                    if not path_attribute_name:
                        raise ValueError(
                            "path_attribute_name must not be empty"
                        )

                    # filter children by path
                    parts = path.split("/")

                    if len(parts) > 0:
                        first_part = parts[0]

                        def children_filter(child: Dict) -> bool:
                            if path_attribute_name in child.keys():
                                return fnmatch.fnmatch(
                                    child[path_attribute_name], first_part
                                )
                            else:
                                return False

                        children = filter(children_filter, children)

                        # override path for next recursive step
                        path = "/".join(parts[1:])

            result[childrens_attribute_name] = [
                pick(
                    x,
                    include=include,
                    childrens_attribute_name=childrens_attribute_name,
                    recursive=recursive,
                    depth=depth,
                    path=path,
                    path_attribute_name=path_attribute_name,
                )
                for x in children
            ]

    return result
