from typing import List, Tuple
from warnings import warn


def deprecation_message(
    deprecated_items: List[Tuple[str, str]],
    module_name: str,
    last_effective_version: str,
    recommended_action: str = "",
):

    dep_item_names = list(set([itm for itm, _ in deprecated_items]))
    is_same_item = len(dep_item_names) == 1
    if is_same_item:
        single_item = len(deprecated_items) == 1
        values = (
            deprecated_items[0][1]
            if single_item
            else [val for _, val in deprecated_items]
        )
        dep_msg = f"{dep_item_names[0]}={repr(values)}"
    else:
        dep_msg = ", ".join(
            [
                f"{dep_item}={repr(dep_value)}"
                for dep_item, dep_value in deprecated_items
            ]
        )

    dep_msg += f" of {module_name}"
    dep_msg += f" will be deprecated in version {last_effective_version}."

    if recommended_action:
        dep_msg += " " + recommended_action

    return dep_msg
