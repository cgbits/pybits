from fnmatch import fnmatch

from typing import Dict, List, Any, Optional


def pick_list(
    items: List[Any],
    include: Optional[List[str]] = None,
    exclude: Optional[List[str]] = None,
    childrens_attribute_name: str = "children",
    recursive: bool = True,
    depth: int = -1,
    path: str = "*",
    path_attribute_name: str = "",
) -> List[Any]:
    result: List[Any] = []

    for item in items:
        if isinstance(item, dict):
            item_dict: Dict[str, Any] = item

            result.append(
                pick(
                    item_dict,
                    include,
                    exclude,
                    childrens_attribute_name,
                    recursive,
                    depth,
                    path,
                    path_attribute_name,
                )
            )
        elif isinstance(item, list):
            item_list: List[Any] = item

            result.append(
                pick_list(
                    item_list,
                    include,
                    exclude,
                    childrens_attribute_name,
                    recursive,
                    depth,
                    path,
                    path_attribute_name,
                )
            )
        elif isinstance(item, (str, int, float)):
            result.append(item)

    return result


def pick(
    item: Dict[str, Any],
    include: Optional[List[str]] = None,
    exclude: Optional[List[str]] = None,
    childrens_attribute_name: str = "children",
    recursive: bool = True,
    depth: int = -1,
    path: str = "*",
    path_attribute_name: str = "",
) -> Dict[str, Any]:
    if include is None:
        include = list(item.keys())

    if exclude is None:
        exclude = []

    # list of item keys
    item_keys = list(item.keys())

    # remove childrens attribute name from include list
    if childrens_attribute_name in include:
        include.remove(childrens_attribute_name)

    result: Dict[str, Any] = {}

    # remove excluded attributes
    for attribute_name in exclude:
        matches = [fnmatch(x, attribute_name) for x in include]

        # print(include, attribute_name)

        if any(matches):
            match_index = matches.index(True)

            include.remove(include[match_index])

    # add included attributes
    for attribute_name in include:
        matches = [fnmatch(x, attribute_name) for x in item_keys]

        if any(matches):
            match_index = matches.index(True)
            matched_attribute_name = item_keys[match_index]

            value = item[matched_attribute_name]

            if isinstance(value, dict):
                value_dict: Dict[str, Any] = value
                value = pick(
                    value_dict,
                    include,
                    exclude,
                    childrens_attribute_name,
                    recursive,
                    depth,
                    path,
                    path_attribute_name,
                )
            elif isinstance(value, list):
                value_list: List[Dict[str, Any]] = value

                value = pick_list(
                    value_list,
                    include,
                    exclude,
                    childrens_attribute_name,
                    recursive,
                    depth,
                    path,
                    path_attribute_name,
                )
            elif not isinstance(value, (str, float, int)):
                raise Exception(f"{type(value)} is not supported")

            result[matched_attribute_name] = value

    # add children
    if recursive:
        # make sure childrens attribute name exists in item keys
        if childrens_attribute_name in item_keys:
            children: List[Dict[str, Any]] = []

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

                        def children_filter(child: Dict[str, Any]) -> bool:
                            if path_attribute_name in child.keys():
                                return fnmatch(
                                    child[path_attribute_name], first_part
                                )
                            else:
                                return False

                        children = list(filter(children_filter, children))

                        # override path for next recursive step
                        path = "/".join(parts[1:])

            result[childrens_attribute_name] = [
                pick(
                    x,
                    include=include,
                    exclude=exclude,
                    childrens_attribute_name=childrens_attribute_name,
                    recursive=recursive,
                    depth=depth,
                    path=path,
                    path_attribute_name=path_attribute_name,
                )
                for x in children
            ]

    return result
