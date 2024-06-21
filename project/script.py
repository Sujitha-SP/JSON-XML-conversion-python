'''
GET THE PATH, READ THE JSON FILE, CONVERT TO LIST.
ITERATE THROGH THE VARIABLES ND WRITE CODE FOR XML LINE BY LINE REFERNCEING TO DATATYPE.
STORE THE DATA AS A STRING AND WRITE INTO GIVEN PATH.
'''

import sys  #for cli commands 
import json #for json reads
import xml.etree.ElementTree as ET #for constructing the XML tree


#getting the path from argument
def json_path(paths) :
    return paths[1]

def xml_path(paths) :
    return paths[2]


#function to read from json file :
def readJsonFile(path) :
    try:
        with open(path, 'r') as file:
            data = json.load(file)
            return data  
    except :
        print('error')

#GET FIELD NAMES
def get_field_name(value_name) :
    field_name = type(value_name)
    if field_name == list :
        field_name = 'array'
    elif field_name == str :
        field_name = 'string'
    elif value_name == True or value_name == False :
        field_name = 'boolean'
    elif field_name == int or field_name == float :
        field_name = 'number'
    elif value_name == None :
        field_name = 'null'
    else :
        if field_name == dict :
            field_name = 'object'
    
    return field_name


#PUT DEAL WITH ARRAY VALUES 
def put_array_values(content, value_name, key_name='') :
    for i,val in enumerate(value_name) :
        print(val, type(val))
        if type(val) == dict :
            content = makeObject(content, val, val.keys())
        elif type(val) == list :
            content = put_array_values(content, value_name)
        else :
            field_name = get_field_name(val)
            content = content+'<'+str(field_name)+'>'+str(val)+'</'+str(field_name)+'>'

            if (i==len(value_name)-1) :
                content += "</array>"
            elif (i==0) :
                if key_name!='' :
                    content += '<array name="' + str(key_name) + '">'
                else :
                    content += '<array>'
    return content
    

#TO DEAL WITH THE DICT / OBJECT VALUES
def put_dict_values(content, data) :
    for key_name, value_name in data.items() :
        #if in form of dict call the function.
        if (type(value_name)==dict) :
            content = put_dict_values(content, value_name)
        else : 
            #get the value_name type :
            field_name = get_field_name(value_name)
            if field_name == 'array':
                content = put_array_values(content, value_name, key_name)
            elif field_name == 'null' :
                content = content + '<null name="'+str(key_name)+'"/>'  
            else :
                content = content+'<'+str(field_name)+' '+'name='+'"'+str(key_name)+'"'+'>'+str(value_name)+'</'+str(field_name)+'>'
    return content


#TO DEAL WITH THE FILE IN ITSELF
def makeObject(content, data, root_name) :
    
    #for the top level; main part
    if root_name == '' :
        content = content+'<object>'
    #for the smaller nested elements
    else :
        #get for the nest subtree parts
        content = content+ '<object name="' + str(root_name) + '">'
     
    #create subelemenets for each values in the list :
    if type(data) == list :
        print(data)
        for d in data :
            if type(d) == dict :
                content = put_dict_values(content, d)
            elif type(d) == list :
                 content = put_array_values(content, d)
    else :
        print(data)
        content = put_dict_values(content, data)
    
    content = content+"</object>"

    #returning the root of the tree and current object where it is being nested in 
    return content



#MAIN FUNCTION 
paths = sys.argv

jpath = json_path(paths)
xpath = xml_path(paths)


data = readJsonFile(jpath) # returns as a list 

# convert the objects one by one and create the xml file
content = makeObject('', data, '')

tree = ET.XML(content)
with open(xpath, "wb") as f:
    f.write(ET.tostring(tree))

with open(xpath, 'r') as f:
    data = f.read()
print("\nHERE IS THE CONVERTED XML DATA:\n\n", data)

print("\n\nSUCCESSFUL\n")