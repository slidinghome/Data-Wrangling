# -*- coding: utf-8 -*-
""" 
Audit street names, city names, and postal codes contained in the burlesonsample.osm file. This code will verify characters, abbreviations, street type, or highway name. It will also display the result 
and the time it takes to audit the file.
"""

import pprint
from collections import defaultdict
import time
import funcvar 

problem_chars = defaultdict(set)
problem_building_numbers = defaultdict(set)
problem_points = defaultdict(set)
problem_street_types = defaultdict(set)
problem_highways = defaultdict(set)
problem_cities = defaultdict(set)
problem_zipcodes = defaultdict(set)

def audit_char(s):
    """
    Verify if the street name has the following problem characters: "'S", ",",
    ";", or ordinal number with capital letter. If it does, it will add the street name into
    problem_chars set.
    Args:
        s: street name
    """
    # problem "'S"
    if "'S" in s:
        problem_chars["'S"].add(s)
    # comma in the street name
    if "," in s:
        problem_chars[","].add(s)
    # semicollon in the street name
    if ";" in s:
        problem_chars[";"].add(s)
    # ordinal number with capital letter such as in 5Th
    p = funcvar.ordinal_number_re.search(s)
    if p:
        ordinal = p.group().strip(" ")
        if any(x.isupper() for x in ordinal):
            problem_chars[ordinal].add(s)


def audit_building_number_type(s):
    """
    Verify if the street name has a suite number. If it does, it will add the street 
    name into problem_building_numbers set.
    Args:
        s: street name
    """
    p = funcvar.building_no_type_re.search(s)
    if p:
        bn = p.group().strip(" ").strip(".")
        if bn not in funcvar.EXPECTED_BUILDING_NUMBER_TYPES:
            problem_building_numbers[bn].add(s)

def audit_point(s):
    """
    Verify if the street name has an abbreviation (e.g S, E, N, W). 
    If it does, it will add the street name into problem_points set.
    Args:
        s: street name
    """
    p = funcvar.audit_point.search(s)
    if p:
        point = p.group().strip(" ")
        problem_points[point].add(s)            

def audit_stret_type(s):
    """
    Verify if the street name has an expected name (e.g Street, Road, Lane). 
    If it does not, it will add the street name into problem_street_types set.
    Args:
        s: street name
    """
    if not any(p in s for p in funcvar.EXPECTED_STREET_TYPES):
        street_type = s
        if " " in s:
            street_type = street_type[street_type.rindex(" "):]
        problem_street_types[street_type].add(s)


def audit_highway(s):
    """
    Verify if the street name has a number that could be a highway number 
    (e.g. FM 1187, Interstate 35). If the number is not highway number or 
    the highway name is not consistent with the mapping, it will add the street name into 
    problem_highways set.
    Args:
        s: street name
    """
    p = funcvar.highway_re.search(s)
    if p:
        hwy = p.group().strip(" ").strip(".")
        if hwy not in funcvar.HIGHWAY_MAPPING \
        or funcvar.HIGHWAY_MAPPING[hwy] not in s:
            if "Suite" not in s:
                problem_highways[hwy].add(s)

def audit_street_name(s):
    """
    Audit street name for problematic characters, building number, abbreviations, street name, and highway name/number. 
    """
    audit_char(s)
    audit_building_number_type(s)
    audit_point(s)
    audit_stret_type(s)
    audit_highway(s)
    
def audit_city_name(c):
    """
    Verify if a city name consists of problem characters, or state 
    name (TX or Texas).
    Args:
        z: zipcode value
    """
    # check for city name that includes state name
    if any(x in c.lower() for x in ['tx', 'texas']):
        problem_cities['include state'].add(c)
    # check for city name that include non alphabet character
    elif not all(x.isalpha() for x in c.lower().replace(' ','')):
        problem_cities['non-alphabet'].add(c)
    # check for city with abbreviated name
    for x in funcvar.CITY_MAPPING.keys():
        if x.lower() in c.lower() and funcvar.CITY_MAPPING[x] not in c:
            problem_cities['problem names'].add(c)
			
def audit_zipcode(z):
    """
    Verify if a zip code contains non-digit charachters, the wrong format 
    (not 5 digit), or a non Burleson zip code (Burleson zip codes starts with 76 ).
    Args:
        z: zip code value
    """
    # Check for non-digit value
    if not all(x.isdigit() for x in z):
        problem_zipcodes['non-digit'].add(z) 
    # Check for non 5-digit value
    if len(z) != 5:
        problem_zipcodes['non 5-digit'].add(z)
    # Check for non 75 or 76
    if not z.startswith('76'):
        problem_zipcodes['non Burleson'].add(z)
			
def display_audit_result():
    """
    Display the results of auditing in the osm file.
    """
    print ("Problem Characters:")
    pprint.pprint(dict(problem_chars))
    print ("Problem Building Numbers:")
    pprint.pprint(dict(problem_building_numbers))    
    print ("Problem Points:")
    pprint.pprint(dict(problem_points))    
    print ("Problem Street Types:")
    pprint.pprint(dict(problem_street_types))    
    print ("Problem Highway Name:")
    pprint.pprint(dict(problem_highways))  
    print ("Problem City Names:")
    pprint.pprint(dict(problem_cities)) 
    print ("Problem zip codes:")
    pprint.pprint(dict(problem_zipcodes))
       
    
def auditing():
    """ 
    Audit streets, cities, and zip codes in the osm file, display the results and the time it takes
    to audit the file
    """
    start = time.time()
    print ("Auditing street names in " + funcvar.OSM_PATH)
    for elem in funcvar.get_element(funcvar.OSM_PATH):
        for tag in elem.iter("tag"):
            if funcvar.is_street_name(tag):
                name = tag.attrib['v']
                audit_street_name(name)
    print ("Auditing City Names in " + funcvar.OSM_PATH)
    for elem in funcvar.get_element(funcvar.OSM_PATH):
        for tag in elem.iter("tag"):
            if funcvar.is_city_name(tag):
                name = tag.attrib['v']
                audit_city_name(name)
    print ("Auditing zip codes in " + funcvar.OSM_PATH)
    for elem in funcvar.get_element(funcvar.OSM_PATH):
        for tag in elem.iter("tag"):
            if funcvar.is_zipcode(tag):
                zipcode = tag.attrib['v']
                audit_zipcode(zipcode)
    end = time.time()
    display_audit_result()
    print ("Time elapsed: " + str(end - start) + " seconds")


if __name__ == "__main__":
    auditing()