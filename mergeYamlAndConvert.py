import glob
import os
import yaml
import xml.etree.ElementTree as ET
import xml.sax.saxutils

# Define the directory where your YAML files are located
data_directory = 'plugins/AreaShop/regions/'

# Initialize an empty dictionary to store the YAML contents
yaml_objects = {}

# Find all YAML files (.yml) in the data directory
yaml_files = glob.glob(data_directory + '*.yml')

# Iterate over the YAML files
for file_path in yaml_files:
    print("Processing file:", file_path)
    with open(file_path, 'r') as file:
        yaml_data = yaml.safe_load(file)
        filename = os.path.basename(file_path)
        yaml_objects[filename] = yaml_data

# Define the path for the output YAML file
output_file_yaml = 'combined.yml'
output_file_xml = 'combined.xml'

# Write the combined YAML objects to the output YAML file
with open(output_file_yaml, 'w') as file:
    yaml.safe_dump(yaml_objects, file)

# Convert the combined YAML objects to XML format
def convert_to_xml(element, data):
    if isinstance(data, dict):
        for key, value in data.items():
            sub_element = ET.SubElement(element, key)
            convert_to_xml(sub_element, value)
    elif isinstance(data, list):
        for i, item in enumerate(data, start=1):
            if isinstance(item, dict):
                sub_element = ET.SubElement(element, 'item', index=str(i))
                convert_to_xml(sub_element, item)
            else:
                sub_element = ET.SubElement(element, 'item', index=str(i))
                sub_element.text = xml.sax.saxutils.escape(str(item))
    else:
        element.text = xml.sax.saxutils.escape(str(data))

root = ET.Element('root')
for filename, yaml_data in yaml_objects.items():
    item = ET.SubElement(root, filename.split('.')[0])
    convert_to_xml(item, yaml_data)

# Function to rename tags starting with numbers
def rename_tags_with_numbers(element):
    for child in list(element):
        if child.tag.isdigit():
            index = child.attrib.pop('index', None)
            item = ET.SubElement(element, 'item', index=index)
            item.extend(list(child))
            element.remove(child)
        else:
            rename_tags_with_numbers(child)

rename_tags_with_numbers(root)

# Create an ElementTree object
tree = ET.ElementTree(root)

# Write the XML data to the output XML file with pretty formatting
tree.write(output_file_xml, encoding='utf-8', xml_declaration=True)

# Read the XML data from the file and apply pretty formatting
with open(output_file_xml, 'r') as file:
    xml_data = file.read()
    xml_data = xml_data.replace('><', '>\n<')

# Write the pretty-printed XML data to the output XML file
with open(output_file_xml, 'w') as file:
    file.write(xml_data)
