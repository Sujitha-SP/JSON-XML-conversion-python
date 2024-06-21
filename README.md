# ABOUT :
    Creating a simple python program that decodes the json to xml based off the few standards. 

## FOR CLI COMMAND 

- Used sys imported function to read them as functional arguments of second and third arguments 

- Run on windows powershell. A sample is as follows :

- METHOD 1 
```bash
#for the change in dir 
cd C:\Users\Sujitha\OneDrive\Desktop\PYTHON-XML-JSON\project
#for the command METHOD 1 
 python .\rescript.py C:\Users\Sujitha\OneDrive\Desktop\PYTHON-XML-JSON\project\testing\sample1.json C:\Users\Sujitha\OneDrive\Desktop\PYTHON-XML-JSON\project\output\output1.xml
```

- METHOD 2
```bash
#for the change in dir 
cd C:\Users\Sujitha\OneDrive\Desktop\PYTHON-XML-JSON\project
#for the command METHOD 2 
 python .\rescript_stack.py C:\Users\Sujitha\OneDrive\Desktop\PYTHON-XML-JSON\project\testing\sample1.json C:\Users\Sujitha\OneDrive\Desktop\PYTHON-XML-JSON\project\output_stack\output_stack1.xml
```

## FOR JSON READ 

- Used a library called json which allows us to read from a json file like a strinf format 

```bash
pip install json
```

## FOR XML WRITING AND READING

- to convert the string format to an xml format, i have utilized the library xml-python and installed the build using :
```bash
pip install xml-python 
```
- later we write to the file with indents using the module minidom taken from xml.dom

## FUNCTIONS METHOD 1

1. readJsonFile
    takes the path as argument and returns the data in a list format 

2. Class  XMLConvertor
    class which is responsible for converting to xml style. 
    It uses a few supporting functions which are 
        1. get_field_name
        2. put_array_values
        3. put_object_values
        4. put_null_values (since its a special case)
    the fucntion takes a string of currently converted data and then recursively runs it till all the data is iterated and correspondingly changed.

3. put_dict_values 
    helps to deal with data in form of dictionary of key value pairs 

4. get_field_name
    It is responsible for making tags which are part of the xml file by utilizing the type() function and mapping the required values

5. put_array_values
    it iterates all the objects in the dictinary and ensures they form a proper xml tag based on thier data types..

6. put_null_values 
    helps to deal with data in form of null values which may or may not have a key

7. Extras:
    Additional functions are included to read xml files, write to xml files and adding indent to xml data before writing. 

## FUNCTIONS METHOD 2

1. readJsonFile
    takes the path as argument and returns the data in a list format 

2. json_to_xml 
    has two additional functions called start_tag and end_tag to deal with the tags like objects, arrays in the stack datastructure. The rest of them are usually created on the flow so that it doent waste time pushing and popping immediately. 

    Functions which is responsible for converting to xml style. 
    It uses a few supporting functions which are 
        1. get_field_name
        2. convert (all the related data are dealt inside using the help of the stack)
    the fucntion takes a string of currently converted data and then recursively runs it till all the data is iterated and correspondingly changed.

3. get_field_name
    It is responsible for making tags which are part of the xml file by utilizing the type() function and mapping the required values

4. class Stack 
    responsible for keeping track of last tages involved and notcing them

5. Extras
    Additional functions are included to read xml files, write to xml files and adding indent to xml data before writing. 


## TEST FILES USED :

    sample1.json to sample8.json 
    sample1.json to sample6.json taken from given test cases

    [URL of sample7](https://support.oneskyapp.com/hc/en-us/articles/208047697-JSON-sample-files)
    [URL of sample8](https://json.org/example.html)


## OUTPUT FILES 
    - for the method 1 :
        output1.xml to output8.xml
        (parsed using xml-python & then pasted.)

    - for the method 2 :
        output_stack1.xml to output_stack8.xml
        (parsed using xml-python & then pasted.)