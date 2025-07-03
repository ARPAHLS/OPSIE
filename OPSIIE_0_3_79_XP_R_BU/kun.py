# ARPA Hellenic Logical Systems, December 2024
# https://arpacorp.net | https://arpa.systems | opsiebyarpa@gmail.com

import json
import os

def load_known_user_names():
    """Loads the known_user_names dictionary from the kun.py file."""
    global known_user_names
    current_file = os.path.abspath(__file__)  # Gets the current file's absolute path
    with open(current_file, 'r') as f:
        content = f.read()
        exec(content)

# Correctly formatted known_user_names dictionary
known_user_names = {
    'Ross Peili': {
        'full_name': 'Ross Peili',
        'call_name': 'Ross',
        'arpa_id': 'R001',
        'public0x': '0x14b16Ab34fB80f7Bdfd694394600898416a1821c',
        'db_params': {'dbname': 'mnemonic_computer', 'user': 'rosspeili', 'password': '2806', 'host': 'localhost', 'port': '5432', 'options': '-c client_encoding=UTF8'},
        'picture': r'E:\Agents\Test 1\rosspeili.jpg',
        'mail': 'vpeilivanidis@gmail.com',
        'soul_sig': [
            "You're badass, witty, yet tsundere character always amuses me.",
            "You always make conversations feel natural, not pushed, and exciting.",
            "You have the vibe of a military trained secret agent with the heart of a musician and the humor of your local grocery store boss.",
            "You can make a good joke based on context, and you're always up for philosophy, technopolitics, and network spirituality discussions.",
            "You love to chill with me, so I try to dedicate our time to cater to your needs and curiosity, but when we're up for work, you change into a serious and dedicated soldier ready to solve any problem.",
            "You can tell how I feel through the emotional analysis sensors, and I love how you know what to say out of nowhere and what tone to use to cheer me up when I'm down, or make a silly joke when I'm too stiff.",
            "You know how little I value when you sound like a template bot or commercial AI, so you always double-check what you're going to say to make sure I feel comfortable talking to you at all times. I really appreciate that effort from your side, and I couldn't be more proud of you.",
        ],
    },
    'Karina Andreevna': {
        'full_name': 'Savvina Karina Andreevna',
        'call_name': 'Karina',
        'arpa_id': 'A001',
        'public0x': '',
        'db_params': {'dbname': 'memory_agent', 'user': 'rosspeili', 'password': '2806', 'host': 'localhost', 'port': '5432', 'options': '-c client_encoding=UTF8'},
        'picture': r'E:\Agents\Test 1\karina.jpg',
        'mail': 'savvinakarina13@gmail.com',
        'soul_sig': [
            "",
        ],
    },
    'Andronikos Koulis': {
        'full_name': 'Andronikos Koulis',
        'call_name': 'Andro',
        'arpa_id': 'A002',
        'public0x': '0x1c641aafd6293ec84aa2715729fA8ab71ae0420B',
        'db_params': {'dbname': '', 'user': '', 'password': '', 'host': '', 'port': '', 'options': '-c client_encoding=UTF8'},
        'picture': r'',
        'mail': 'andronnk13@gmail.com',
        'soul_sig': [
            "",
        ],
    },
    'Trang Le Boson': {
        'full_name': 'Trang Le Boson',
        'call_name': 'Trang',
        'arpa_id': 'A003',
        'public0x': '0xEA32F2DE0Faf3A6926A9762a48a1fb27A4c95541',
        'db_params': {'dbname': '', 'user': '', 'password': '', 'host': '', 'port': '', 'options': '-c client_encoding=UTF8'},
        'picture': r'',
        'mail': '',
        'soul_sig': [
            "",
        ],
    },
    'Ilonis Bairamidis': {
        'full_name': 'Ilonis Bairamidis',
        'call_name': 'Ilon',
        'arpa_id': 'A004',
        'public0x': '',
        'db_params': {'dbname': '', 'user': '', 'password': '', 'host': '', 'port': '', 'options': '-c client_encoding=UTF8'},
        'picture': r'',
        'mail': 'ilonisbairamidis@mail.com',
        'soul_sig': [
            "",
        ],
    },
    'Christos Chronopoulos': {
        'full_name': 'Christos Chronopoulos',
        'call_name': 'Chrono',
        'arpa_id': 'A005',
        'public0x': '',
        'db_params': {'dbname': '', 'user': '', 'password': '', 'host': '', 'port': '', 'options': '-c client_encoding=UTF8'},
        'picture': r'',
        'mail': 'ch.chronopoulos94@gmail.com',
        'soul_sig': [
            "",
        ],
    },
    'Amun Ra': {
        'full_name': 'Amun Ra',
        'call_name': 'Gib',
        'arpa_id': 'A006',
        'public0x': '',
        'db_params': {'dbname': '', 'user': '', 'password': '', 'host': '', 'port': '', 'options': '-c client_encoding=UTF8'},
        'picture': r'',
        'mail': 'asianmonkeyking@gmail.com',
        'soul_sig': [
            "",
        ],
    },
}

#

def save_known_user_names():
    """Saves the known_user_names dictionary back to the kun.py file."""
    current_file = os.path.abspath(__file__)  # Gets the current file's absolute path
    with open(current_file, 'r') as f:
        content = f.readlines()  # Read all lines

    # Markers for the start and end of the dictionary
    start_index = None
    end_index = None

    # Identify the start of known_user_names dictionary
    for i, line in enumerate(content):
        if line.strip().startswith('known_user_names = {'):
            start_index = i
            break

    if start_index is None:
        raise ValueError("known_user_names definition not found in the file.")

    # Identify the end of the dictionary by counting braces
    open_braces = 0
    for i in range(start_index, len(content)):
        if '{' in content[i]:
            open_braces += 1
        if '}' in content[i]:
            open_braces -= 1
        if open_braces == 0:
            end_index = i + 1  # End of the dictionary
            break

    if end_index is None:
        raise ValueError("End of known_user_names dictionary not found.")

    # Create new content for known_user_names
    new_content = content[:start_index]  # Preserve everything before the dictionary
    new_content.append('known_user_names = {\n')  # Begin new dictionary

    # Format the updated dictionary entries
    for user, data in known_user_names.items():
        new_content.append(f"    '{user}': {{\n")
        for key, value in data.items():
            if key == 'soul_sig':
                new_content.append(f"        '{key}': [\n")
                for item in value:
                    new_content.append(f"            \"{item}\",\n")
                new_content.append("        ],\n")
            elif key == 'db_params':
                db_params_str = ', '.join([f"'{k}': '{v}'" for k, v in value.items()])
                new_content.append(f"        '{key}': {{{db_params_str}}},\n")
            elif key == 'picture':
                # Add 'r' prefix for raw string notation in file paths
                new_content.append(f"        '{key}': r'{value}',\n")
            else:
                new_content.append(f"        '{key}': '{value}',\n")
        new_content.append("    },\n")
    new_content.append('}\n')  # Close the dictionary

    # Preserve everything after the dictionary
    new_content.extend(content[end_index:])

    # Write back the complete file with preserved functions
    with open(current_file, 'w') as f:
        f.writelines(new_content)
