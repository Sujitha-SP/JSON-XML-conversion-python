'''
DONE ON ASSESSMENT DAY AFTER RECHANGING --NEXT DAY
'''

import sys  # for CLI commands
import json # for JSON reads
import xml.etree.ElementTree as ET # for constructing the XML tree


# Getting the path from arguments
def json_path(paths):
    return paths[1]

def xml_path(paths):
    return paths[2]


# Function to read from JSON file:
def read_json_file(path):
    try:
        with open(path, 'r') as file:
            data = json.load(file)
            return data
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None


# Get field names based on the value type
def get_field_name(value):
    if isinstance(value, list):
        return 'array'
    elif isinstance(value, str):
        return 'string'
    elif isinstance(value, bool):
        return 'boolean'
    elif isinstance(value, (int, float)):
        return 'number'
    elif value is None:
        return 'null'
    elif isinstance(value, dict):
        return 'object'
    return 'unknown'


# Handle array values
def put_array_values(content, value, key_name=''):
    if key_name:
        content += f'<array name="{key_name}">'
    else:
        content += '<array>'
    
    for val in value:
        field_name = get_field_name(val)
        if isinstance(val, dict):
            content = put_dict_values(content, val)
        elif isinstance(val, list):
            content = put_array_values(content, val)
        else:
            content += f'<{field_name}>{val}</{field_name}>'
    
    content += '</array>'
    return content


# Handle dictionary/object values
def put_dict_values(content, data):
    for key, value in data.items():
        field_name = get_field_name(value)
        if field_name == 'object':
            content += f'<object name="{key}">'
            content = put_dict_values(content, value)
            content += '</object>'
        elif field_name == 'array':
            content = put_array_values(content, value, key)
        elif field_name == 'null':
            content += f'<null name="{key}"/>'
        else:
            content += f'<{field_name} name="{key}">{value}</{field_name}>'
    return content


# Main function to create the XML content
def make_object(content, data, root_name):
    if root_name:
        content += f'<object name="{root_name}">'
    else:
        content += '<object>'
    
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                content = put_dict_values(content, item)
            elif isinstance(item, list):
                content = put_array_values(content, item)
    else:
        content = put_dict_values(content, data)
    
    content += '</object>'
    return content


# MAIN FUNCTION
if __name__ == "__main__":
    paths = sys.argv

    jpath = json_path(paths)
    xpath = xml_path(paths)

    data = read_json_file(jpath)
    if data is None:
        sys.exit("Failed to read JSON data")

    # Convert the objects one by one and create the XML file
    content = make_object('', data, '')

    tree = ET.ElementTree(ET.fromstring(content))
    with open(xpath, "wb") as f:
        tree.write(f)

    with open(xpath, 'r') as f:
        data = f.read()
    print("\nHERE IS THE CONVERTED XML DATA:\n\n", data)
    print("\n\nSUCCESSFUL\n")
