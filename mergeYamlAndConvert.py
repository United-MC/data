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
                sub_element.text = xml.sax.saxutils.escape(str(item) if item is not None else '')  # Convert None to empty string
    else:
        element.text = xml.sax.saxutils.escape(str(data) if data is not None else '')  # Convert None to empty string

root = ET.Element('root')
for filename, yaml_data in yaml_objects.items():
    item = ET.SubElement(root, filename.split('.')[0])
    convert_to_xml(item, yaml_data)

# Function to rename tags starting with numbers
def rename_tags_with_numbers(element):
    for child in list(element):
        if child.tag.isdigit():
            index = child.attrib.pop('index', None)
            new_tag = 'item_{}'.format(index) if index is not None else 'item'
            child.tag = new_tag
            rename_tags_with_numbers(child)
        else:
            rename_tags_with_numbers(child)

# Create a new XML tree to perform tag renaming
new_root = ET.Element(root.tag)
new_root.extend(root)
rename_tags_with_numbers(new_root)

# Create an ElementTree object with the new XML tree
tree = ET.ElementTree(new_root)

# Write the XML data to the output XML file with pretty formatting
with open(output_file_xml, 'wb') as file:
    tree.write(file, encoding='utf-8', xml_declaration=True)

# Read the XML data from the file and apply pretty formatting
with open(output_file_xml, 'r', encoding='utf-8') as file:
    xml_data = file.read()
    xml_data = xml_data.replace('><', '>\n<')

# Write the pretty-printed XML data to the output XML file
with open(output_file_xml, 'w', encoding='utf-8') as file:
    file.write(xml_data)
