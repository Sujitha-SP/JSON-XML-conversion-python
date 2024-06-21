'''
METHOD 1 (CLASS)
    USES STRING CONCATENATIONS AND ITERATING THROUGH THE VARIABLES AND SORTING BASED ON THE TYPES 
'''

#IMPORTS 
import sys  #for cli commands 
import json #for json reads
import xml.etree.ElementTree as ET #for constructing the XML tree
from xml.dom import minidom #for parsing


#ONE CLASS FOR THE CONVERSION
class XMLConverter:
    # GET FIELD NAMES
    def get_field_name(self, value_name):
        if value_name is None:
            return 'null'
        
        field_names = {
            list: 'array',
            dict: 'object',
            str: 'string',
            bool: 'boolean',
            int: 'number',
            float: 'number'
        }
        
        return field_names[type(value_name)]
    
    # PUT NULL VALUES
    def put_null_values(self, content, key):
        if key == '':
            content += '<null/>'
        else:
            content += f'<null name="{key}"/>'
        return content

    # PUT ARRAY VALUES
    def put_array_values(self, content, value, key_name=''):
        '''
        Converts all the array elements to <array> tags. If dictionary encountered, it is sent back.
        '''
        if key_name:
            content += f'<array name="{key_name}">'
        else:
            content += '<array>'
        
        for val in value:
            field_name = self.get_field_name(val)
            if field_name == 'object':
                content = self.put_object_values(content, val, '')
            elif field_name == 'array':
                content = self.put_array_values(content, val)
            elif field_name == 'null':
                content += self.put_null_values(content, '')
            else:
                content += f'<{field_name}>{val}</{field_name}>'
        
        content += '</array>'
        return content

    # PUT OBJECT VALUES
    def put_object_values(self, content, values, key_name=''):
        '''
        two ways either there's a json type -> keyword is present 
        or keyword not present cases: inside a list, or as a value
        '''
        if key_name == '':
            content += '<object>'
        else:
            content += f'<object name="{key_name}">'
        if type(values) == dict :
            for key, val in values.items():
                field_name = self.get_field_name(val)
                if field_name == 'null':
                    content = self.put_null_values(content, key)
                elif field_name == 'object':
                    content = self.put_object_values(content, val, key)
                elif field_name == 'array':
                    content = self.put_array_values(content, val, key)
                elif field_name in ['string', 'boolean', 'number']:
                    content += f'<{field_name} name="{key}">{val}</{field_name}>'
        else :
            if type(values) == list :
                content = self.put_array_values(content, values, '')

        content += '</object>'
        return content


#getting the path from argument
def json_path(paths) :
    return paths[1]


#getting the path from argument
def xml_path(paths) :
    return paths[2]


#function to read from json file :
def readJsonFile(path) :
    try:
        with open(path, 'r') as file:
            data = json.load(file)
            formatted_json = json.dumps(data, indent=2)  # Format with indentation
            print(formatted_json)
            return data  
    except :
        print('error')


#WRITE TO XML FILES 
def writeXML(content, xpath) :
    tree = ET.XML(content)
    with open(xpath, "wb") as f:
        f.write(ET.tostring(tree))

#READ FILE
def readXML(xpath) :
    with open(xpath, 'r') as f:
        return f.read()


# parse an xml file by name
def pretty_print_xml(xml_string):
    # Parse the XML string into an ElementTree element
    element = ET.fromstring(xml_string)
    
    # Convert the ElementTree element back into a string with minidom for pretty-printing
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    
    return reparsed.toprettyxml(indent="  ")



'''
MAIN FUNCTIONS 
'''


paths = sys.argv

jpath = json_path(paths)
xpath = xml_path(paths)

print(f"\n\nPATHS GIVEN\n {jpath}\n {xpath}\n\n")

print(f"DATA IN JSON FILE:\n")
json_data = readJsonFile(jpath) # returns as a list 
print("\n\n")


converter = XMLConverter()
# convert the objects one by one and create the xml file
content = ''


if type(json_data) == list and type(json_data[0]) == dict:
    #since the returned values from json file might be a list form 
    for i,data in enumerate(json_data) :
        content = converter.put_object_values(content, data, '')
else :
    content = converter.put_object_values(content, json_data, '')


pretty_xml = pretty_print_xml(content)
writeXML(pretty_xml, xpath)
print("\nCONVERTED XML DATA:\n")
print(readXML(xpath))
print("\n\nSUCCESSFUL\n")



