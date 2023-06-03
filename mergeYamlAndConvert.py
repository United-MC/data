import glob
import os
import yaml
import xml.etree.ElementTree as ET
import xml.dom.minidom

# Define the directory where your YAML files are located
data_directory = 'plugins/AreaShop/regions'

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
        for item in data:
            if isinstance(item, dict):
                sub_element = ET.SubElement(element, 'item')
                convert_to_xml(sub_element, item)
            else:
                sub_element = ET.SubElement(element, 'item')
                sub_element.text = str(item)
    else:
        element.text = str(data)

root = ET.Element('root')
for filename, yaml_data in yaml_objects.items():
    item = ET.SubElement(root, filename.split('.')[0])
    convert_to_xml(item, yaml_data)

xml_data = ET.tostring(root, encoding='unicode')

# Format the XML data with indentation
dom = xml.dom.minidom.parseString(xml_data)
pretty_xml_data = dom.toprettyxml(indent='  ')

# Write the pretty-printed XML data to the output XML file
with open(output_file_xml, 'w') as file:
    file.write(pretty_xml_data)
