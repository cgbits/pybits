import fnmatch

from typing import List, Dict

from pybits import dictbits, exceptions


def trim(items: List) -> List:
    result = []

    for item in items:
        if isinstance(item, dict):
            result.append(dictbits.trim(item))
        elif isinstance(item, list):
            result.append("[...]")
        else:
            result.append(item)

    return result


def assert_is_equal(subset: List, superset: List, depth: int = 0) -> bool:
    try:
        if len(superset) != len(subset):
            # early return false
            # if length of superset and subset ar not equal
            raise exceptions.ComparisonError(f"Excpected length to be equal")

        # compare all items
        for index, item in enumerate(subset):
            if isinstance(item, dict):
                # compare value recursive with dictbits.assert_is_equal
                # if value is an instance of dict
                superset_value_dict: Dict = superset[index]

                dictbits.assert_is_equal(item, superset_value_dict, depth + 1)
            elif isinstance(item, list):
                # compare value recursive with assert_is_equal
                # if value is an instance of list
                superset_value_list: List = superset[index]

                assert_is_equal(item, superset_value_list, depth + 1)
            else:
                # compare superset at index with item
                # if value is neither dict or list
                superset_value = superset[index]

                if item != superset_value:
                    raise exceptions.ComparisonError(
                        f"Excpected '{item}' to be equal to '{superset_value}'",
                        depth,
                    )
    except exceptions.ComparisonError as e:
        raise exceptions.ComparisonErrorInfo(
            f"{trim(subset)} is not equal to {trim(superset)}: {e}", depth
        )

    return True


def is_equal(subset: List, superset: List) -> bool:
    try:
        return assert_is_equal(subset, superset)
    except exceptions.ComparisonBaseError:
        return False


def assert_is_subset(subset: List, superset: List, depth: int = 0) -> bool:
    try:
        for item in subset:
            if isinstance(item, dict):
                # compare value recursive with dictbits.assert_is_subset
                # if value is an instance of dict
                matches = False
                local_exceptions = []

                for superset_item in superset:
                    # compare every value of superset with item
                    try:
                        dictbits.assert_is_subset(
                            item, superset_item, depth + 1
                        )

                        matches = True

                        break
                    except exceptions.ComparisonBaseError as e:
                        local_exceptions.append(e)

                if not matches and local_exceptions:
                    # raise error from likeliest path
                    raise sorted(local_exceptions, key=lambda x: x.depth).pop()

            elif isinstance(item, list):
                # compare value recursive with assert_is_subset
                # if value is an instance of list
                matches = False
                local_exceptions = []

                for superset_item in superset:
                    # compare every value of superset with item
                    try:
                        assert_is_subset(item, superset_item, depth + 1)

                        matches = True

                        break
                    except exceptions.ComparisonBaseError as e:
                        local_exceptions.append(e)

                if not matches and local_exceptions:
                    # raise error from likeliest path
                    raise sorted(local_exceptions, key=lambda x: x.depth).pop()
            elif isinstance(item, str):
                # compare value
                # if value is neither dict or list
                if not any([fnmatch.fnmatch(x, item) for x in superset]):
                    raise exceptions.ComparisonError(
                        f"Expected '{item}' to be contained in '{trim(superset)}'",
                        depth,
                    )
            else:
                # compare every value of superset with item
                # if value is neither dict or list
                if not any([item in x for x in superset]):
                    # raise exceptions.ComparisonError
                    # if no value from superset equals item
                    raise exceptions.ComparisonError(
                        f"Expected '{item}' to be contained in '{trim(superset)}'",
                        depth,
                    )
    except exceptions.ComparisonError as e:
        raise exceptions.ComparisonErrorInfo(
            f"{trim(subset)} is no subset of {trim(superset)}: {e}", depth
        )

    return True


def is_subset(subset: List, superset: List) -> bool:
    try:
        return assert_is_subset(subset, superset)
    except exceptions.ComparisonBaseError:
        return False
