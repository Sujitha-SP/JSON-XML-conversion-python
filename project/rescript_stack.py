'''
METHOD 2 - 
    CONCEPTS INVLOVED :: RECURSION, STACKS
    DONE USING THE CONCEPT OF STACK WHICH CAN AT MOST STORE ARRAY AND OBJECT. 
        THIS IS SO THAT THE RECURSION IS CONTROLLED TO AN EXTENT
        THIS WAY IT ALSO IS EASIER TO ALLOW CHECKING OF THE ATTRIBUTE 'NAME' TO BE INCLUDED OR NOT
    USES SINGLULAR FUNCTION TO DEAL WITH THE CODE AS IT RUNS RECURSIVELY  
'''
#WORKS - RECHANGED 

#IMPORTS 
import sys  #for cli commands 
import json #for json reads
import xml.etree.ElementTree as ET #for constructing the XML tree
from xml.dom import minidom #for parsing


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


#STACK IMPLEMENTATION AS A CLASS
class Stack:
    def __init__(self):
        self.stack = []

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        else:
            raise IndexError("Peek from an empty stack")

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            raise IndexError("Pop from an empty stack")

    def push(self, item):
        self.stack.append(item)

    def is_empty(self):
        return len(self.stack) == 0


#MAIN FUNCTION TO CONVERT -- RECURSION & STACKS 
def json_to_xml(json_obj):

    #these act as the global variables within the json_to_xml function
    stack = Stack()
    xml_str = ""

    #uses stack to add as needed.
    def start_tag(field_name, key_name=None):
        #appends the type so that it can peek at a later stage
        stack.push(field_name)
        if key_name != None:
            return f'<{field_name} name="{key_name}">'
        else:
            return f"<{field_name}>"

    #uses the stack to get the last included array/object
    def end_tag():
        return f'</{stack.pop()}>'

    #get the names for tags in the values
    def get_field_name(value) :
        if type(value) == str :
            return 'string'
        
        if type(value) == bool :
            return 'boolean'

        if type(value) == int or type(value) == float :
            return 'number'

    #main conversion occurs ; utilizes stack and recursion 
    def convert(value, name=None):

        #call the global variable and keep adding
        nonlocal xml_str

        if type(value) == dict:
            #from stack 
            xml_str += start_tag("object", name)
            #for each value 
            for k, v in value.items():
                convert(v, k)
            #from stack
            xml_str += end_tag()
        
        elif type(value) == list:
            #from stack 
            xml_str += start_tag("array", name)
            #for each value
            for item in value:
                convert(item)
            #from stack
            xml_str += end_tag()
        
        #since null is a special case 
        elif value is None:
            if name != None or stack.peek() == 'array':
                xml_str += f'<null name="{name}"/>'
            else :
                xml_str += f'<null/>'

        #for the other types involved dont include stack
        elif type(value) in [str, int, float, bool] :
            field_name = get_field_name(value)
            if stack.peek() == 'array':
                xml_str = xml_str + start_tag(field_name) + str(value) + end_tag()
                #xml_str += f"<{field_name}>{value}</{field_name}>"
            else :
                xml_str = xml_str + start_tag(field_name, name) + str(value) + end_tag()
                #xml_str += f'<{field_name} name="{name}">{value}</{field_name}>'

        else :
            pass

    convert(json_obj)
    return xml_str


# parse an xml file by name
def pretty_print_xml(xml_string):
    # Parse the XML string into an ElementTree element
    element = ET.fromstring(xml_string)
    
    # Convert the ElementTree element back into a string with minidom for pretty-printing
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    
    return reparsed.toprettyxml(indent="  ")





'''
MAIN FUNCTION 
'''

# JSON object PATHS REAd
paths = sys.argv

jpath = json_path(paths)
xpath = xml_path(paths)


print(f"\n\nPATHS GIVEN\n {jpath}\n {xpath}\n\n")

print(f"DATA IN JSON FILE:\n")
json_data = readJsonFile(jpath) # returns as a list 
print("\n\n")

if type(json_data) == list and type(json_data[0]) == dict:
    #since the returned values from json file is probably in a list form 
    #TWO CASES, dicts within lists
    #Lists is direct. In case 2; send the list of the list
    for i,data in enumerate(json_data) :
        # Convert JSON to XML per element wise 
        xml_output = json_to_xml(data)
else :
    xml_output = json_to_xml(json_data)
    

#convert with indentations ; parsing
pretty_xml = pretty_print_xml(xml_output)
#writing to the file 
writeXML(pretty_xml, xpath)

#displaying on the CLI
print("\nCONVERTED XML DATA:\n")
print(readXML(xpath))
print("\n\nSUCCESSFUL\n")









