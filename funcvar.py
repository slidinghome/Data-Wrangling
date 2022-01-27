# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import os
import re


"""
This section contains helper functions to process the OSM files. 
"""

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """
    Yield element if it is the right type of tag
    """
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

def get_element_count(osm_file):
    """
    Get the count of node, relation, and way. 
    Args: 
        osm_file
    Returns:
        the count of node, relation, and way in a dictionary 
    """
    elements = {'node': 0, 'relation': 0, 'way': 0}
    for elem in get_element(osm_file):
        if elem.tag == 'node':
            elements['node'] += 1
        elif elem.tag == 'relation':
            elements['relation'] += 1
        else:
            elements['way'] +=1
    return elements

def get_file_size(file):
    """
    Get a file size in KB, rounded to 1 decimal place
    Args:
        file
    Returns:
        file size in KB
    """
    return round(float(os.path.getsize(file))/1000,1)
            
def get_map_bounds(osm_file):
    """
    Get osm map boundaries
    Args:
        osm_file
    Returns:
        minimum and maximum latitude and minimum and maximum longitude in a dictionary
    """
    boundaries = None
    for event, elem in ET.iterparse(OSM_PATH):
        if elem.tag == "bounds":
            boundaries= {'Latitude': [elem.attrib['minlat'], elem.attrib['maxlat']], 
                         'Longitude': [elem.attrib['minlon'], elem.attrib['maxlon']]}            
        break # we're done
    return boundaries

def is_street_name(elem):
    """Check whether an element consist of street address"""
    return (elem.attrib['k'] == "addr:street")

def is_zipcode(elem):
    """Check whether an element consist of a zip code"""
    return (elem.attrib['k'] == "addr:postcode")

def is_city_name(elem):
    """Check whether an element consist of city name"""
    return (elem.attrib['k'] == "addr:city")
	
"""
This section consists of file paths, regular expressions, mapping rules, and 
expected values used in th Open Street Data Wrangling project
"""


#          Files Paths                

# The osm file
OSM_PATH = 'burlesonsample.osm'
# The database file
DB_PATH = 'burlesonsample.db'
# The csv files
NODES_PATH = 'nodes.csv'
NODE_TAGS_PATH = 'nodes_tags.csv'
RELATIONS_PATH = 'relations.csv'
RELATION_NODES_PATH = 'relations_nodes.csv'
RELATION_RELATIONS_PATH = 'relations_relations.csv'
RELATION_TAGS_PATH = 'relations_tags.csv'
RELATION_WAYS_PATH = 'relations_ways.csv'
WAYS_PATH = 'ways.csv'
WAY_NODES_PATH = 'ways_nodes.csv'
WAY_TAGS_PATH = 'ways_tags.csv'
csv_files = [NODES_PATH, NODE_TAGS_PATH, RELATIONS_PATH, RELATION_NODES_PATH,
             RELATION_RELATIONS_PATH, RELATION_TAGS_PATH,RELATION_WAYS_PATH,
             WAYS_PATH, WAY_NODES_PATH, WAY_TAGS_PATH]

# The fields order in the csvs base on the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
RELATION_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
RELATION_NODES_FIELDS = ['id', 'node_id', 'position', 'role']
RELATION_RELATIONS_FIELDS = ['id', 'relation_id', 'position', 'role']
RELATION_TAGS_FIELDS = ['id', 'key', 'value', 'type']
RELATION_WAYS_FIELDS = ['id', 'way_id', 'position', 'role']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']


#           Regular Expressions                   

audit_point = re.compile(r'(^|\s)([SWNE]|SE|SW|NW|NE)\.?(\s|$)', re.IGNORECASE)
building_no_phrase_re = re.compile(r'\s(ste\s|suite\s|building\s|#\s?)\w+\-?\d*', re.IGNORECASE)
building_no_type_re = re.compile(r'\s(ste\s|suite\s|building\s|#\s?|no\.)', re.IGNORECASE)
##end_point_re = re.compile(r'\s([SWNE]|SE|SW|NW|NE)*\.?$', re.IGNORECASE)
ending_word_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
highway_re = re.compile(r'(\s|\-)\d+\w?(\s|$)', re.IGNORECASE)
LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
ordinal_number_re = re.compile(r'(^|\s)\d+(st|nd|rd|th)\.?(\s|$)', re.IGNORECASE)
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
##start_point_re = re.compile(r'^([SWNE]|SE|SW|NW|NE)(\.|\s)', re.IGNORECASE)
starting_word_re = re.compile(r'^\b\S+\.?', re.IGNORECASE)
street_number_re = re.compile(r'^\d+\w?\s',re.IGNORECASE)
zip_re = re.compile(r'7[5-6]\d{3}') # Regex to find Dallas Zipcodes


#       Expected Values               

EXPECTED_BUILDING_NUMBER_TYPES = ['Suite', 'No', 'Building']
EXPECTED_POINTS = ['North', 
                   'Northwest',
                   'West',
                   'Southwest',
                   'South',
                   'Southeast',
                   'East',
                   'North']
EXPECTED_STREET_TYPES = ['Alley', 
                      'Avenue', 
                      'Bay',
                      'Boulevard',
                      'Central',  
                      'Circle',
                      'Court', 
                      'Cove',  
                      'Crest', 
                      'Crossing', 
                      'Drive', 
                      'Expressway', 
                      'Extension',
                      'Freeway', 
                      'Glen',
                      'Highway',
                      'Inlet', 
                      'Landing',
                      'Lane', 
                      'Loop', 
                      'Mews', 
                      'Park',  
                      'Parkway', 
                      'Pass', 
                      'Path',
                      'Place',
                      'Plaza', 
                      'Point',
                      'Ridge',  
                      'Road', 
                      'Row', 
                      'Run',    
                      'Street',
                      'Square',
                      'Terrace',  
                      'Tollway',
                      'Trace', 
                      'Trail',
                      'Vista',
                      'Way',  
                      'Walk']


#          Value Mappings             

CITY_MAPPING = {'Burleson': 'Crowley',
                'Dfw': 'Fort Worth',
                'Ft': 'Fort',
                'Joshua': 'Alvarado'}

CR_road = 'County Road'
FM_road = 'FM Road'
Inter_road = 'Interstate Highway' 
TX_road = 'TX Highway'
US_road = 'US Highway'

HIGHWAY_MAPPING = {'1043': CR_road,
                   '1138': FM_road,
                   '114': TX_road,
                   '1187': FM_road,
                   '12': TX_road + ' Loop',
                   '121': TX_road,
                   '1382': FM_road,
                   '1565': FM_road,
                   '157': FM_road,
                   '1603': FM_road,
                   '161': TX_road,
                   '175': US_road,
                   '183': TX_road,
                   '1902': FM_road,
                   '199': TX_road,                   
                   '20': Inter_road,
                   '206': CR_road,
                   '2181': FM_road,
                   '23': CR_road,
                   '234': CR_road,
                   '26': TX_road,
                   '287': US_road,
                   '288': TX_road + ' Loop',
                   '30': Inter_road,
                   '3040': FM_road,
                   '34': TX_road,
                   '342': TX_road,
                   '35': Inter_road,
                   '356': TX_road,
                   '360': TX_road,
                   '376': CR_road,
                   '377': US_road,
                   '380': US_road,
                   '407': FM_road,
                   '408': TX_road + ' Spur',
                   '423': FM_road,
                   '45': Inter_road,
                   '526': CR_road,
                   '549': CR_road,
                   '544': FM_road,
                   '615': CR_road,
                   '664': FM_road,
                   '66': TX_road,
                   '67': US_road,
                   '707': CR_road,
                   '730': FM_road,
                   '741': FM_road,
                   '77': US_road,
                   '78': TX_road,
                   '80': US_road,
                   '81': US_road,
                   '820': TX_road + ' Loop',
                   '983': FM_road}

POINT_MAPPING = {'s': 'South',
                 'se': 'Southeast',
                 'e': 'East',
                 'ne': 'Northeast',
                 'n': 'North',
                 'nw': 'Northwest',
                 'w': 'West',
                 'sw': 'Southwest'}

TYPE_MAPPING = {'56th': '56th Street',
                'av': 'Avenue',
                'ave': 'Avenue',
                'expy': 'Expressway',
                'expessway': 'Expressway',
                'exressway': 'Expressway',
                'trl': 'Trail',
                'blvd': 'Boulevard',
                'bus': 'Business',
                'cir': 'Cirle',
                'ct': 'Court',
                'dr': 'Drive',
                'ln': 'Lane',
                'frontage': 'Frontage Road',
                'fwy': 'Freeway',
                'hwy': 'Highway',
                'pkwy': 'Parkway',
                'rd': 'Road',
                'st': 'Street',
                'pkwy': 'Parkway'}