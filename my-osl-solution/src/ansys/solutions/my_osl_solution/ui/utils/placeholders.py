# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.


def update_placeholders(ui_values: list, placeholders: dict) -> dict:
    """Information needed."""

    updated_dict = {}
    for row in ui_values[1:]:
        parameter_name = row["props"]["children"][0]["props"]["children"]["props"]["children"]
        input_value = row["props"]["children"][1]["props"]["children"]["props"]["value"]

        placeholder_values = placeholders.get("placeholder_values")
        if parameter_name in placeholder_values:
            updated_dict[parameter_name] = input_value
    return updated_dict
