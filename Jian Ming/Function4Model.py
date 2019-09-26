"""
This module contains functions for Function 4 GUI and some extra stuff.
"""

import csv


def extract_csv_data(csv_file_path):
    """
    Extract csv data from a file.

    :param str csv_file_path: csv file path to extract the data from.
    :return: An iterable list of dictionary in this format: {'category': 'value'}
    :exception IOError: Raised when the file cannot be open.
    """
    # Open a csv file with read binary mode.
    with open(csv_file_path, "rb") as csv_file:
        reader = csv.DictReader(csv_file)

        """
        Generate an iterable list of dictionary.
        {'category': 'value'}
        This is more memory efficient as there will not be memory overflow if dataset is too big.
        """
        for readerRow in reader:
            yield readerRow


def get_registered_contractors(contractors_file_path):
    """
    Get all the registered contractors.

    :param contractors_file_path: File path to the registered contractors dataset.
    :rtype: list[str]
    :return: A list of registered contractors
    """
    try:
        registered_contractors = []

        contractors_generator = extract_csv_data(contractors_file_path)

        for row in contractors_generator:
            company_name = row["company_name"]

            # Insert contractors into the list if it does not exist in the list.
            if company_name not in registered_contractors:
                registered_contractors.append(company_name)

        return registered_contractors
    except IOError:
        return []


def get_registered_contractors_awarded(procurement_file_path, contractors_file_path):
    """
    Get all the registered contractors that have secured at least one procurement.

    :param str procurement_file_path: File path to the government procurement dataset.
    :param str contractors_file_path: File path to the registered contractors dataset.
    :rtype: list[str]
    :return: A list of registered contractors that have secured at least one procurement.
    """
    try:
        awarded_contractors = []
        registered_contractors_awarded = []

        procurement_generator = extract_csv_data(procurement_file_path)
        contractors_generator = extract_csv_data(contractors_file_path)

        for row in procurement_generator:
            supplier_name = row["supplier_name"]

            # Insert awarded vendors into the list if it does not exist in the list.
            if supplier_name != "na" and supplier_name not in awarded_contractors:
                awarded_contractors.append(supplier_name)

        for row in contractors_generator:
            company_name = row["company_name"]

            # Insert registered contractor that was awarded into the list if it does not exist in the list.
            if company_name in awarded_contractors and company_name not in registered_contractors_awarded:
                registered_contractors_awarded.append(company_name)

        return registered_contractors_awarded
    except IOError:
        return []


def get_contractors_information(contractors_file_path, search_by, search_data):
    """
    Get the contractors information by company name or uen number.

    :param str contractors_file_path: File path to the registered contractors dataset.
    :param str search_by: Search the information by company_name or uen_no.
    :param str search_data: Search data.
    :rtype: list[dict[str, str]]
    :return: A list of contractors information in a dictionary.
    """
    if not str.lower(search_by) == "company_name" and not str.lower(search_by) == "uen_no":
        return []

    try:
        contractors_information = []

        contractors_generator = extract_csv_data(contractors_file_path)

        for row in contractors_generator:
            column_data = row[search_by]

            # If the search matches, add them into the list.
            if str.lower(column_data) == str.lower(search_data):
                contractors_information.append(row)

        return contractors_information
    except IOError:
        return []


def get_registered_contractors_search_suggestions(contractors_file_path, search_data):
    """
    Get the top 5 entries that starts with search_data.

    :param str contractors_file_path: File path to the registered contractors dataset.
    :param str search_data: What to search.
    :rtype: list[str]
    :return: The top 5 list of entries that matches the search_data.
    """
    try:
        top_5_search = []

        contractors_generator = extract_csv_data(contractors_file_path)

        for row in contractors_generator:
            company_name = row["company_name"]
            uen_no = row["uen_no"]

            if str.startswith(str.lower(company_name), str.lower(search_data)) and company_name not in top_5_search:
                top_5_search.append(company_name)
            elif str.startswith(str.lower(uen_no), str.lower(search_data)) and uen_no not in top_5_search:
                top_5_search.append(uen_no)

            if len(top_5_search) == 5:
                break

        return top_5_search
    except IOError:
        return []


def get_tendering_limits(workhead, grade):
    """
    Get the tendering limits of the workhead based on their grades.

    :param str workhead: Type of workhead
    :param str grade: Workhead grades.
    :return: The tendering limits in SGD million.
    """
    construction_workhead = {"A1": "Unlimited", "A2": "85", "B1": "40", "B2": "13", "C1": "4", "C2": "1.3",
                             "C3": "0.65"}

    specialist_workhead = {"Single Grade": "Unlimited", "L6": "Unlimited", "L5": "13", "L4": "6.5", "L3": "4",
                           "L2": "1.3", "L1": "0.65"}

    if str.lower(workhead) == "cw01" or str.lower(workhead) == "cw02":
        # Construction Workheads (CW01 and CW02)
        return construction_workhead[grade]
    else:
        # Specialist Workheads (CR, ME MW and SY)
        return specialist_workhead[grade]


def get_workhead_description(workhead):
    """
    Get the workhead description.

    :param str workhead: Type of workhead.
    :return: The workhead description.
    """
    workhead_type = {
        "CW01": "General Building",
        "CW02": "Civil Engineering",
        "CR01": "Minor Construction Work",
        "CR02": "Corrosion Protection",
        "CR03": "Demolition",
        "CR04": "Fencing & Ironworks",
        "CR05": "Concrete Repairs",
        "CR06": "Interior Decoration & Finishing Works",
        "CR07": "Cable / Pipe Laying & Road Reinstatement",
        "CR08": "Piling Works",
        "CR09": "Repairs & Redecoration",
        "CR10": "Pre-cast Concrete Works",
        "CR11": "Signcraft Installation",
        "CR12": "Ground Support & Stabilisation Works",
        "CR13": "Waterproofing Installation",
        "CR14": "Asphalt Works & Road Marking",
        "CR15": "Site Investigation Works",
        "CR16": "Curtain Walls",
        "CR17": "Windows",
        "CR18": "Doors",
        "MW02": "Housekeeping, Cleansing, Desilting & Conservancy Service",
        "MW03": "Landscaping",
        "MW04": "Pest Control",
        "ME01": "Air-Conditioning, Refrigeration & Ventilation Works",
        "ME02": "Building Automation, Industrial & Process Control Systems",
        "ME03": "Solar PV System Integration",
        "ME04": "Communication & Security Systems",
        "ME05": "Electrical Engineering",
        "ME06": "Fire Prevention & Protection Systems",
        "ME07": "High & Low Tension Overhead Line Installation",
        "ME08": "Internal Telephone Wiring for Telecommunications",
        "ME09": "Lift & Escalator Installation",
        "ME10": "Line Plant Cabling / Wiring for Telecommunications",
        "ME11": "Mechanical Engineering",
        "ME12": "Plumbing & Sanitary Works",
        "ME13": "Traffic Light Systems",
        "ME14": "Underground Pipleline for Telecommunications",
        "ME15": "Integrated Building Services",
        "RW01": "Window Contractors",
        "RW02": "Lift Contractors",
        "RW03": "Escalator Contractors",
        "SY01A": "Essential Construction Materials",
        "SY01B": "Ready-Mixed Concrete",
        "SY01C": "Other Basic Construction Materials",
        "SY02": "Chemicals",
        "SY04": "Electrical Equipment",
        "SY05": "Electrical & Electronic Materials, Products & Components",
        "SY06": "Finishing & Building Products",
        "SY07": "Gases",
        "SY08": "Mechanical Equipment, Plant & Machinery",
        "SY09": "Mechanical Materials Products & Components",
        "SY10": "Metal & Timber Structures",
        "SY11": "Petroleum Products",
        "SY12": "Pipes",
        "SY14": "Sanitary Products",
        "TR01": "Formwork",
        "TR02": "Steel Reinforcement Work",
        "TR03": "Concreting Work",
        "TR04": "Drywall Installation",
        "TR05": "Pre-case Installation",
        "TR06": "Ceiling Work",
        "TR07": "Tile/Marble/Stone Work",
        "TR08": "Timber, Vinyl and Laminate Flooring Works",
        "TR09": "Plastering/Skimming",
        "TR10": "Ironmongery & Metalwork"
    }

    if str.upper(workhead) in workhead_type:
        return workhead_type[str.upper(workhead)]
    else:
        return "No description"
