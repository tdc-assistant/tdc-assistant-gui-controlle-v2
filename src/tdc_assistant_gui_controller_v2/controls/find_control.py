from typing import Any, Callable


from .enums import ControlPropertyKey, ControlPropertyValue


def find_control_by_property(
    control: Any,
    prop_key: ControlPropertyKey,
    prop_value: ControlPropertyValue,
    f: Callable[[Any], Any],
):
    if control is None:
        return

    props = control.get_properties()
    if props.get(prop_key.value) == prop_value.value:
        return f(props)

    for d in control.descendants():
        found = find_control_by_property(d, prop_key, prop_value, f)
        if found:
            return found

    return None
