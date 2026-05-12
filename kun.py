# ARPA Hellenic Logical Systems
# https://arpacorp.net | https://arpa.systems | input@arpacorp.net
#
# Repository template: replace profile fields with your own data before running.
# See docs/CONFIGURATION.md and kun.example.py for a fuller multi-user example.

import json
import os

_REPO_ROOT = os.path.dirname(os.path.abspath(__file__))


def load_known_user_names():
    """Loads the known_user_names dictionary from the kun.py file."""
    global known_user_names
    current_file = os.path.abspath(__file__)
    with open(current_file, "r", encoding="utf-8") as f:
        content = f.read()
        exec(content)


known_user_names = {
    "Demo Operator": {
        "full_name": "Demo Operator",
        "call_name": "Demo",
        "arpa_id": "R001",
        "public0x": "",
        "db_params": {
            "dbname": "mnemonic_computer",
            "user": "your_postgres_username",
            "password": "your_postgres_password",
            "host": "localhost",
            "port": "5432",
            "options": "-c client_encoding=UTF8",
        },
        "picture": os.path.join(_REPO_ROOT, "assets", "enrollment.jpg"),
        "mail": "you@example.com",
        "soul_sig": [
            "Template soul signature line: adjust preferences here or use /soulsig after login.",
        ],
    },
}


def save_known_user_names():
    """Saves the known_user_names dictionary back to the kun.py file."""
    current_file = os.path.abspath(__file__)
    with open(current_file, "r", encoding="utf-8") as f:
        content = f.readlines()

    start_index = None
    end_index = None

    for i, line in enumerate(content):
        if line.strip().startswith("known_user_names = {"):
            start_index = i
            break

    if start_index is None:
        raise ValueError("known_user_names definition not found in the file.")

    open_braces = 0
    for i in range(start_index, len(content)):
        if "{" in content[i]:
            open_braces += 1
        if "}" in content[i]:
            open_braces -= 1
        if open_braces == 0:
            end_index = i + 1
            break

    if end_index is None:
        raise ValueError("End of known_user_names dictionary not found.")

    new_content = content[:start_index]
    new_content.append("known_user_names = {\n")

    for user, data in known_user_names.items():
        new_content.append(f"    '{user}': {{\n")
        for key, value in data.items():
            if key == "soul_sig":
                new_content.append(f"        '{key}': [\n")
                for item in value:
                    new_content.append(f"            {json.dumps(item, ensure_ascii=False)},\n")
                new_content.append("        ],\n")
            elif key == "db_params":
                db_params_str = ", ".join([f"'{k}': '{v}'" for k, v in value.items()])
                new_content.append(f"        '{key}': {{{db_params_str}}},\n")
            elif key == "picture":
                new_content.append(f"        '{key}': r'{value}',\n")
            else:
                new_content.append(f"        '{key}': '{value}',\n")
        new_content.append("    },\n")
    new_content.append("}\n")
    new_content.extend(content[end_index:])

    with open(current_file, "w", encoding="utf-8") as f:
        f.writelines(new_content)
