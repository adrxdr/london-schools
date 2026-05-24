#!/usr/bin/env python3

import csv
import datetime as dt
import json
import math
import re
import statistics
import subprocess
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"

PERFORMANCE_CSV = DATA_DIR / "ks2_school_performance_2025.csv"
INFO_CSV = DATA_DIR / "ks2_school_info_2025.csv"
WORKFORCE_CSV = DATA_DIR / "school_workforce_school_level.csv"
GEOCODE_CACHE = DATA_DIR / "postcode_geocode_cache.json"
PRICE_POSTCODE_CACHE = DATA_DIR / "price_postcode_geocode_cache.json"
CRIME_CACHE = DATA_DIR / "school_crime_cache.json"
IMD_CSV = DATA_DIR / "iod2019_all.csv"
IMD_POSTCODE_CACHE = DATA_DIR / "imd_postcode_cache.json"

ALL_RANKED_CSV = OUTPUT_DIR / "london_ks2_2025_ranked.csv"
TOP_300_CSV = OUTPUT_DIR / "london_ks2_2025_top300.csv"
TOP_300_JSON = OUTPUT_DIR / "london_ks2_2025_top300.json"
MAP_HTML = OUTPUT_DIR / "london_ks2_2025_top300_map.html"

POSTCODE_RE = re.compile(r"([A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2})$")
MISSING = {"", "z", "x", "SUPP"}
TOP_N = 500
TERRACE_PRICE_START_DATE = dt.date(2024, 5, 16)
TERRACE_PRICE_YEARS = [2024, 2025, 2026]
TERRACE_PRICE_RADIUS_MILES = 0.5
TERRACE_PRICE_RADIUS_KM = TERRACE_PRICE_RADIUS_MILES * 1.609344
PRICE_PAID_URL_TEMPLATE = "https://price-paid-data.publicdata.landregistry.gov.uk/pp-{year}.csv"
POLICE_LAST_UPDATED_URL = "https://data.police.uk/api/crime-last-updated"
POLICE_STREET_CRIME_URL = "https://data.police.uk/api/crimes-street/all-crime"
IMD_CSV_URL = "https://assets.publishing.service.gov.uk/media/5dc407b440f0b6379a7acc8d/File_7_-_All_IoD2019_Scores__Ranks__Deciles_and_Population_Denominators_3.csv"
IMD_POSTCODE_LOOKUP_ORIGIN = "https://imd-by-postcode.opendatacommunities.org"
IMD_POSTCODE_LOOKUP_BASE = f"{IMD_POSTCODE_LOOKUP_ORIGIN}/imd/2019"
FAMILY_CRIME_WEIGHTS = {
    "violent-crime": 2.0,
    "robbery": 1.8,
    "possession-of-weapons": 1.8,
    "burglary": 1.5,
    "drugs": 1.4,
    "public-order": 1.2,
    "anti-social-behaviour": 1.0,
    "criminal-damage-arson": 1.0,
    "vehicle-crime": 0.7,
    "bicycle-theft": 0.6,
    "theft-from-the-person": 0.6,
    "other-theft": 0.5,
    "shoplifting": 0.3,
}
LONDON_BOROUGHS = {
    "BARKING AND DAGENHAM",
    "BARNET",
    "BEXLEY",
    "BRENT",
    "BROMLEY",
    "CAMDEN",
    "CITY OF LONDON",
    "CROYDON",
    "EALING",
    "ENFIELD",
    "GREENWICH",
    "HACKNEY",
    "HAMMERSMITH AND FULHAM",
    "HARINGEY",
    "HARROW",
    "HAVERING",
    "HILLINGDON",
    "HOUNSLOW",
    "ISLINGTON",
    "KENSINGTON AND CHELSEA",
    "KINGSTON UPON THAMES",
    "LAMBETH",
    "LEWISHAM",
    "MERTON",
    "NEWHAM",
    "REDBRIDGE",
    "RICHMOND UPON THAMES",
    "SOUTHWARK",
    "SUTTON",
    "TOWER HAMLETS",
    "WALTHAM FOREST",
    "WANDSWORTH",
    "WESTMINSTER",
}

WANDSWORTH_CATCHMENT_SOURCE = {
    "name": "Wandsworth Council reception allocations",
    "year": 2026,
    "url": "https://www.wandsworth.gov.uk/media/4q2f3jqt/how_places_were_allocated_for_primary_schools_2026.pdf",
}

HARINGEY_CATCHMENT_SOURCE = {
    "name": "Haringey Council primary cutoff distances",
    "year": 2025,
    "url": "https://haringey.gov.uk/schools-learning/schools/school-admissions/how-school-place-offers-were-made/cutoff-distance-school-last-child-offered-place/primary-schools-distance-school-last-child-offered-place-national-offer-day",
}

HACKNEY_CATCHMENT_SOURCE = {
    "name": "Hackney Education reception applications and offers",
    "year": 2026,
    "url": "https://education.hackney.gov.uk/sites/default/files/document/Applications%20and%20Offers%20at%20Hackney%20Primary%20Schools%202018-26.pdf",
}

BARNET_CATCHMENT_SOURCE = {
    "name": "Barnet Council primary school allocations",
    "year": 2026,
    "url": "https://www.barnet.gov.uk/sites/default/files/how_primary_school_places_were_allocated_on_16_april_2026.pdf",
}


def miles_catchment(miles):
    return {
        "radius_m": round(miles * 1609.344),
        "note": f"Distance of last child offered under distance criterion ({miles:g} miles)",
    }


def metres_catchment(metres, criterion="published allocation criterion"):
    return {
        "radius_m": round(metres),
        "note": f"Distance of last child offered under {criterion} ({metres:g} metres)",
    }


def km_catchment(km):
    return {
        "radius_m": round(km * 1000),
        "note": f"Distance of last child offered under distance criterion ({km:g} km)",
    }


def criterion_miles_catchment(miles, criterion):
    return {
        "radius_m": round(miles * 1609.344),
        "note": f"Distance of last child offered under {criterion} ({miles:g} miles)",
    }


def no_distance_catchment(note="No final-distance cut-off published in the latest source"):
    return {"note": note}


def all_offered_catchment(note="All on-time applicants offered"):
    return {"note": note}


def demand_met_catchment(note="Demand met"):
    return {"note": note}


WANDSWORTH_2026_CATCHMENTS = {
    "all saints ce primary school": {"note": "All applicants offered"},
    "belleville primary school": {
        "radius_m": 1210,
        "note": "Furthest distance offered under proximity criterion",
    },
    "brandlehow primary school": {
        "radius_m": 645,
        "note": "Furthest distance offered under proximity criterion",
    },
    "holy ghost catholic primary school": {
        "radius_m": 838,
        "note": "Furthest distance offered in the listed Catholic category",
    },
    "honeywell infant school": {
        "radius_m": 1071,
        "note": "Furthest distance offered under proximity criterion",
    },
    "john burns primary school": {"note": "All applicants offered"},
    "ronald ross primary school": {
        "radius_m": 301,
        "note": "Furthest distance offered under proximity criterion",
    },
    "roehampton church forest school": {"note": "All applicants offered"},
    "rutherford house primary school": {
        "radius_m": 777,
        "note": "Furthest distance offered under proximity criterion",
    },
    "sheringdale primary school": {
        "radius_m": 354,
        "note": "Furthest distance offered under proximity criterion",
    },
    "st anselm's catholic primary school": {
        "radius_m": 987,
        "note": "Furthest distance offered in the listed Catholic category",
    },
    "st mary's ce primary school putney": {
        "radius_m": 311,
        "note": "Furthest distance offered for open places",
    },
    "st michael's ce primary school": {
        "radius_m": 412,
        "note": "Furthest distance offered for open places",
    },
    "trinity st mary's primary school": {"note": "All applicants offered"},
}

HARINGEY_2025_CATCHMENTS = {
    "alexandra primary school": {"note": "All applicants offered"},
    "belmont infant school": miles_catchment(0.1808),
    "bounds green infant school": miles_catchment(0.5317),
    "bruce grove primary school": {"note": "All applicants offered"},
    "campsbourne infant school": miles_catchment(0.7065),
    "chestnuts primary school": miles_catchment(0.2729),
    "coldfall primary school": miles_catchment(0.8358),
    "coleridge primary school": miles_catchment(0.4913),
    "crowland primary school": {"note": "All applicants offered"},
    "devonshire hill primary school": {"note": "All applicants offered"},
    "earlham primary school": miles_catchment(0.7918),
    "earlsmead primary school": {"note": "All applicants offered"},
    "ferry lane primary school": {"note": "All applicants offered"},
    "harris academy tottenham": miles_catchment(0.3668),
    "harris primary academy coleraine park": {"note": "All applicants offered"},
    "harris primary academy philip lane": miles_catchment(0.3807),
    "highgate primary school": miles_catchment(1.0265),
    "lancasterian primary school": miles_catchment(0.7961),
    "lea valley primary school": {"note": "All applicants offered"},
    "lordship lane primary school": {"note": "All applicants offered"},
    "mulberry primary school": miles_catchment(0.522),
    "muswell hill primary school": miles_catchment(0.5338),
    "noel park primary school": miles_catchment(0.6743),
    "north harringay primary school": miles_catchment(0.287),
    "rhodes avenue primary school": miles_catchment(0.3808),
    "risley avenue primary school": {"note": "All applicants offered"},
    "rokesly infant school": miles_catchment(0.4557),
    "south harringay infant school": miles_catchment(0.1884),
    "st aidan's voluntary controlled primary school": miles_catchment(0.2178),
    "stroud green primary school": miles_catchment(0.3593),
    "tetherdown primary school": {"note": "All applicants offered"},
    "the willow primary school": miles_catchment(0.3234),
    "trinity primary academy": miles_catchment(0.4733),
    "welbourne primary school": {"note": "All applicants offered"},
    "west green primary school": miles_catchment(0.2863),
    "weston park primary school": miles_catchment(0.2345),
}

HACKNEY_2026_CATCHMENTS = {
    "benthal primary school": miles_catchment(0.833),
    "berger primary school": miles_catchment(9.719),
    "betty layward primary school": miles_catchment(0.245),
    "daubeney primary school": miles_catchment(5.829),
    "gainsborough primary school": miles_catchment(3.31),
    "gayhurst community school": miles_catchment(0.344),
    "grasmere primary school": miles_catchment(0.197),
    "grazebrook primary school": miles_catchment(0.51),
    "harrington hill primary school": miles_catchment(0.321),
    "holmleigh primary school": miles_catchment(7.416),
    "hoxton garden primary school": {
        "radius_m": 350,
        "note": "Source lists max distance as 350.333 under the miles column; treated as metres due implausible mile value",
    },
    "jubilee primary school": miles_catchment(1.294),
    "kingsmead primary school": miles_catchment(0.568),
    "lauriston primary school": miles_catchment(0.463),
    "london fields primary school": miles_catchment(1.179),
    "mandeville primary school": miles_catchment(1.668),
    "millfields community school": miles_catchment(1.65),
    "morningside primary school": miles_catchment(0.835),
    "nightingale primary school": miles_catchment(0.699),
    "orchard primary school": miles_catchment(2.443),
    "parkwood primary school": miles_catchment(1.5),
    "princess may primary school": miles_catchment(5.127),
    "queensbridge primary school": miles_catchment(3.517),
    "rushmore primary school": miles_catchment(0.447),
    "sebright school": miles_catchment(0.434),
    "shacklewell primary school": miles_catchment(0.277),
    "shoreditch park primary school": miles_catchment(0.419),
    "southwold primary school": miles_catchment(0.796),
    "springfield community primary school": miles_catchment(0.979),
    "thomas fairchild community school": miles_catchment(1.993),
    "william patten primary school": miles_catchment(0.466),
    "woodberry down community primary school": miles_catchment(2.795),
}

BARNET_2026_CATCHMENTS = {
    "akiva school": criterion_miles_catchment(0.565, "top faith priority"),
    "all saints' ce school n20": demand_met_catchment(),
    "all saints' ce school nw2": demand_met_catchment(),
    "alma primary": demand_met_catchment(),
    "annunciation catholic infant": demand_met_catchment(),
    "ashmole primary school": criterion_miles_catchment(0.496, "Straight-line distance"),
    "beis yaakov jewish": no_distance_catchment("Other Orthodox Jewish girls (lottery)"),
    "beit shvidler jewish": criterion_miles_catchment(
        0.428, "Orthodox Jewish attending another synagogue"
    ),
    "blessed dominic catholic": criterion_miles_catchment(0.159, "Other Faiths"),
    "brookland infant": demand_met_catchment(),
    "brunswick park primary": demand_met_catchment(),
    "brunswick park primary and nursery school": demand_met_catchment(),
    "brunswick park primary school": demand_met_catchment(),
    "chalgrove primary school": criterion_miles_catchment(
        0.46, "children living in defined area"
    ),
    "childs hill": demand_met_catchment(),
    "christ church ce school": demand_met_catchment(),
    "christ church primary school": demand_met_catchment(),
    "claremont primary school": demand_met_catchment(),
    "colindale primary": criterion_miles_catchment(
        0.976, "children living outside defined area"
    ),
    "courtland primary": criterion_miles_catchment(
        0.794, "children living outside defined area"
    ),
    "courtland school": criterion_miles_catchment(
        0.794, "children living outside defined area"
    ),
    "deansbrook infant": demand_met_catchment(),
    "dollis": demand_met_catchment(),
    "etz chaim jewish primary": demand_met_catchment(),
    "foulds primary": criterion_miles_catchment(
        0.448, "children living outside defined area"
    ),
    "foulds school": criterion_miles_catchment(
        0.448, "children living outside defined area"
    ),
    "goldbeaters primary school": criterion_miles_catchment(
        0.663, "children living in defined area"
    ),
    "hasmonean primary school": demand_met_catchment(),
    "hollickwood school": demand_met_catchment(),
    "holy trinity ce": demand_met_catchment(),
    "holy trinity ce primary school": demand_met_catchment(),
    "independent jewish day": no_distance_catchment("Certificate of religious practice (lottery)"),
    "independent jewish day school": no_distance_catchment(
        "Certificate of religious practice (lottery)"
    ),
    "livingstone primary": criterion_miles_catchment(
        0.408, "children living in defined area"
    ),
    "livingstone primary and nursery school": criterion_miles_catchment(
        0.408, "children living in defined area"
    ),
    "livingstone primary school": criterion_miles_catchment(
        0.408, "children living in defined area"
    ),
    "london academy": criterion_miles_catchment(0.165, "Geographical Distance"),
    "mathilda marks kennedy": demand_met_catchment(),
    "menorah foundation jewish": no_distance_catchment(
        "Others who do not meet the religious criteria (lottery)"
    ),
    "menorah foundation school": no_distance_catchment(
        "Others who do not meet the religious criteria (lottery)"
    ),
    "menorah primary boys": no_distance_catchment(
        "Orthodox Jewish who are first children (lottery)"
    ),
    "menorah primary school for boys": no_distance_catchment(
        "Orthodox Jewish who are first children (lottery)"
    ),
    "menorah primary girls": no_distance_catchment("Other Orthodox Jewish children (lottery)"),
    "menorah primary school for girls": no_distance_catchment(
        "Other Orthodox Jewish children (lottery)"
    ),
    "monken hadley ce": no_distance_catchment(
        "Children within 2 miles and worship at a Holy Trinity church; no final straight-line cut-off published"
    ),
    "monken hadley ce primary school": no_distance_catchment(
        "Children within 2 miles and worship at a Holy Trinity church; no final straight-line cut-off published"
    ),
    "monkfrith primary": criterion_miles_catchment(
        1.019, "children living outside defined area"
    ),
    "monkfrith primary school": criterion_miles_catchment(
        1.019, "children living outside defined area"
    ),
    "moss hall infant": criterion_miles_catchment(
        0.463, "children living outside defined area"
    ),
    "osidge": demand_met_catchment(),
    "our lady of lourdes rc": demand_met_catchment(),
    "pardes house jewish": criterion_miles_catchment(
        1.353, "Other Orthodox Jewish children within 2.5 miles"
    ),
    "parkfield primary": demand_met_catchment(),
    "rimon jewish": criterion_miles_catchment(
        0.49, "Faith Band: GG Synagogue Attendance Level 1"
    ),
    "rimon jewish primary school": criterion_miles_catchment(
        0.49, "Faith Band: GG Synagogue Attendance Level 1"
    ),
    "rosh pinah jewish": demand_met_catchment(),
    "rosh pinah primary school": demand_met_catchment(),
    "sacks morasha jewish": no_distance_catchment(
        "Priority children attending Orthodox synagogue in catchment (lottery)"
    ),
    "sacks morasha jewish primary school": no_distance_catchment(
        "Priority children attending Orthodox synagogue in catchment (lottery)"
    ),
    "sacred heart rc": demand_met_catchment(),
    "sacred heart roman catholic primary school": demand_met_catchment(),
    "st agnes' rc": criterion_miles_catchment(0.45, "Any Other Children"),
    "st agnes' catholic primary school": criterion_miles_catchment(
        0.45, "Any Other Children"
    ),
    "st andrew's ce": criterion_miles_catchment(0.639, "All Others Living in the Parish"),
    "st andrew's ce voluntary aided primary school totteridge": criterion_miles_catchment(
        0.639, "All Others Living in the Parish"
    ),
    "st catherine's catholic": criterion_miles_catchment(0.321, "Any other applicant"),
    "st catherine's rc school": criterion_miles_catchment(0.321, "Any other applicant"),
    "st john's ce n20": criterion_miles_catchment(
        0.456, "Faith Band: worship at other Christian church"
    ),
    "st john's ce primary school": criterion_miles_catchment(
        0.456, "Faith Band: worship at other Christian church"
    ),
    "st john's ce primary school and": criterion_miles_catchment(
        0.456, "Faith Band: worship at other Christian church"
    ),
    "st john's ce primary and school": criterion_miles_catchment(
        0.456, "Faith Band: worship at other Christian church"
    ),
    "st john's ce primary and nursery school": criterion_miles_catchment(
        0.456, "Faith Band: worship at other Christian church"
    ),
    "st mary's ce en4": criterion_miles_catchment(
        0.332, "resident of the four eligible parishes"
    ),
    "st mary's ce primary school east barnet": criterion_miles_catchment(
        0.332, "resident of the four eligible parishes"
    ),
    "st mary's ce n3": criterion_miles_catchment(
        0.884, "Any other applicant geographically"
    ),
    "st mary's ce primary school": criterion_miles_catchment(
        0.884, "Any other applicant geographically"
    ),
    "st paul's ce nw7": demand_met_catchment(),
    "st paul's ce primary school nw7": demand_met_catchment(),
    "sunnyfields primary": criterion_miles_catchment(
        0.472, "children living outside defined area"
    ),
    "sunnyfields primary school": criterion_miles_catchment(
        0.472, "children living outside defined area"
    ),
    "the hyde": criterion_miles_catchment(0.511, "Inside catchment area"),
    "the hyde school": criterion_miles_catchment(0.511, "Inside catchment area"),
    "the orion primary": criterion_miles_catchment(
        0.946, "children living outside defined area"
    ),
    "the orion primary school": criterion_miles_catchment(
        0.946, "children living outside defined area"
    ),
    "whitings hill primary": criterion_miles_catchment(
        0.768, "children living outside defined area"
    ),
    "whitings hill primary school": criterion_miles_catchment(
        0.768, "children living outside defined area"
    ),
}

EALING_CATCHMENT_SOURCE = {
    "name": "Ealing Council primary allocations by distance and criteria",
    "year": 2026,
    "url": "https://www.ealing.gov.uk/download/downloads/id/8668/primary_allocations_by_distance_and_criteria",
}

EALING_2026_CATCHMENTS = {
    "ark priory primary academy": criterion_miles_catchment(0.448, "Distance (criterion e)"),
    "ark priory primary school": criterion_miles_catchment(0.448, "Distance (criterion e)"),
    "brentside primary academy": criterion_miles_catchment(0.138, "Distance (criterion 7)"),
    "christ the saviour ce primary school": criterion_miles_catchment(
        4.93, "Other Christian weekly attendance (criterion 5)"
    ),
    "dairy meadow primary school": criterion_miles_catchment(0.505, "Distance (criterion 9)"),
    "durdans park primary school": criterion_miles_catchment(1.082, "Distance (criterion 9)"),
    "fielding primary school": criterion_miles_catchment(0.364, "Priority area (criterion 5)"),
    "holy family catholic primary school": criterion_miles_catchment(
        0.302, "Other applicants (criterion 12)"
    ),
    "little ealing primary school": criterion_miles_catchment(0.363, "Priority area (criterion 5)"),
    "montpelier primary school": criterion_miles_catchment(0.661, "Priority area (criterion 5)"),
    "mount carmel catholic primary school": criterion_miles_catchment(
        0.767, "Practising Catholic living in named parish (criterion 4)"
    ),
    "selborne primary school": criterion_miles_catchment(2.47, "Distance (criterion 9)"),
    "southfield primary school": criterion_miles_catchment(3.941, "Sibling (criterion 6)"),
    "st gregory's catholic primary school": criterion_miles_catchment(
        0.739, "Practising Catholic living outside parish (criterion 3)"
    ),
    "stanhope primary school": criterion_miles_catchment(7.1, "Distance (criterion 9)"),
    "tudor primary school": criterion_miles_catchment(0.871, "Distance (criterion 9)"),
}

HARROW_CATCHMENT_SOURCE = {
    "name": "Harrow Council primary school place allocations",
    "year": 2026,
    "url": "https://www.harrow.gov.uk/downloads/file/33701/primary-school-allocations-2026-27",
}

HARROW_2026_CATCHMENTS = {
    "avanti house primary school": criterion_miles_catchment(1.313, "distance criterion"),
    "cannon lane primary school": criterion_miles_catchment(0.851, "distance criterion"),
    "grimsdyke school": criterion_miles_catchment(1.498, "distance criterion"),
    "krishna avanti primary school": criterion_miles_catchment(0.683, "distance criterion"),
    "krishna avanti school": criterion_miles_catchment(0.683, "distance criterion"),
    "newton farm nursery infant and junior school": criterion_miles_catchment(
        0.359, "distance criterion"
    ),
    "pinner wood school": criterion_miles_catchment(0.778, "distance criterion"),
    "priestmead primary school and nursery": criterion_miles_catchment(0.823, "distance criterion"),
    "priestmead primary school": criterion_miles_catchment(0.823, "distance criterion"),
    "stanburn primary school": criterion_miles_catchment(1.253, "distance criterion"),
    "vaughan primary school": criterion_miles_catchment(0.396, "distance criterion"),
    "west lodge primary school": criterion_miles_catchment(0.663, "distance criterion"),
    "st anselm's catholic primary school": no_distance_catchment(
        "Breakdown not published by Harrow; source says contact the school directly"
    ),
    "st bernadette's catholic primary school": no_distance_catchment(
        "Breakdown not published by Harrow; source says contact the school directly"
    ),
    "st john fisher catholic primary school": no_distance_catchment(
        "Breakdown not published by Harrow; source says contact the school directly"
    ),
    "st joseph's catholic primary school": no_distance_catchment(
        "Breakdown not published by Harrow; source says contact the school directly"
    ),
    "whitchurch primary school and nursery": no_distance_catchment(
        "No final-distance cut-off published in the latest Harrow source"
    ),
}

REDBRIDGE_CATCHMENT_SOURCE = {
    "name": "Redbridge Council primary offer day last allocated distances",
    "year": 2026,
    "url": "https://www.redbridge.gov.uk/media/ldbowne5/primary-offer-day-16-april-2026-last-allocated.pdf",
}

REDBRIDGE_2026_CATCHMENTS = {
    "al noor voluntary aided muslim primary school": criterion_miles_catchment(
        0.361, "Non-Muslim distance"
    ),
    "al noor primary school": criterion_miles_catchment(0.361, "Non-Muslim distance"),
    "aldborough primary school": all_offered_catchment(),
    "aldersbrook primary school": all_offered_catchment(),
    "avanti court primary school": criterion_miles_catchment(
        2.929, "Band 3 Hindu faith distance"
    ),
    "christchurch primary school": all_offered_catchment(),
    "churchfields junior school": criterion_miles_catchment(
        0.471, "junior transfer distance"
    ),
    "cleveland road primary school": criterion_miles_catchment(0.617, "distance"),
    "fullwood primary school": criterion_miles_catchment(0.904, "distance"),
    "gearies primary school": criterion_miles_catchment(0.847, "distance"),
    "gordon primary school": all_offered_catchment(),
    "grove primary school": criterion_miles_catchment(1.51, "distance"),
    "highlands primary school": criterion_miles_catchment(0.669, "distance"),
    "nightingale primary school": criterion_miles_catchment(1.821, "distance"),
    "our lady of lourdes rc primary school": criterion_miles_catchment(
        0.188, "Any other applicant"
    ),
    "parkhill junior school": all_offered_catchment(),
    "ss peter and paul's catholic primary school": all_offered_catchment(),
    "st antony's catholic primary school": all_offered_catchment(),
    "st bede's catholic primary school": all_offered_catchment(),
    "wanstead church school": criterion_miles_catchment(1.286, "distance to school"),
    "wells primary school": criterion_miles_catchment(0.714, "distance"),
}

HAVERING_CATCHMENT_SOURCE = {
    "name": "Havering Council infant and primary school statistics",
    "year": 2026,
    "url": "https://www.havering.gov.uk/downloads/file/7395/infant-and-primary-school-statistics-2026",
}

HAVERING_2026_CATCHMENTS = {
    "ardleigh green infants": km_catchment(0.746),
    "ardleigh green junior school": km_catchment(0.746),
    "concordia academy": km_catchment(1.115),
    "hacton primary school": km_catchment(2.348),
    "nelmes primary school": km_catchment(1.081),
    "scotts primary school": km_catchment(0.989),
    "suttons primary school": no_distance_catchment(),
    "upminster infants": km_catchment(1.911),
    "upminster junior school": km_catchment(1.911),
}

NEWHAM_CATCHMENT_SOURCE = {
    "name": "Newham Council Starting School in Newham",
    "year": 2026,
    "url": "https://www.newham.gov.uk/downloads/file/9671/starting-school-in-newham-2026-",
}

NEWHAM_2026_CATCHMENTS = {
    "calverton primary school": no_distance_catchment(),
    "central park primary school": no_distance_catchment(),
    "cleves primary school": criterion_miles_catchment(0.33, "All Other"),
    "curwen primary school": criterion_miles_catchment(0.896, "All Other"),
    "earlham primary school": criterion_miles_catchment(0.395, "All Other"),
    "elmhurst primary school": criterion_miles_catchment(0.434, "All Other"),
    "grange primary school": no_distance_catchment(),
    "hallsville primary school": criterion_miles_catchment(0.474, "All Other"),
    "keir hardie primary school": no_distance_catchment(),
    "new city primary school": no_distance_catchment(),
    "ranelagh primary school": no_distance_catchment(),
    "ravenscroft primary school": no_distance_catchment(),
    "roman road primary school": no_distance_catchment(),
    "rosetta primary school": no_distance_catchment(),
    "salisbury primary school": no_distance_catchment(),
    "scott wilkie primary school": no_distance_catchment(),
    "shaftesbury primary school": no_distance_catchment(),
    "southern road primary school": no_distance_catchment(),
    "st stephen's primary school": criterion_miles_catchment(0.369, "All Other"),
    "tollgate primary school": no_distance_catchment(),
    "vicarage primary school": no_distance_catchment(),
}

BRENT_CATCHMENT_SOURCE = {
    "name": "Brent Council how places were offered at schools",
    "year": 2026,
    "url": "https://www.brent.gov.uk/education-schools-and-learning/school-admissions/how-school-places-were-offered",
}

BRENT_2026_CATCHMENTS = {
    "ark franklin primary academy": metres_catchment(671.53, "Distance"),
    "east lane primary school": metres_catchment(1294.11, "Distance"),
    "mount stewart junior school": metres_catchment(4415.19, "Any Other Applicant"),
    "our lady of grace catholic junior school": metres_catchment(7232.49, "Other Applicants"),
    "princess frederica ce primary school": metres_catchment(
        814.03, "Any Other Child who live in parish"
    ),
    "sinai jewish primary school": metres_catchment(
        8987.12, "Other children with completed and valid CRP"
    ),
    "st joseph's catholic junior school": metres_catchment(
        1553.38, "Baptised Catholic with certificate of Catholic practice, in parish"
    ),
    "st joseph's roman catholic primary school": metres_catchment(
        1678.52, "Other Christian children"
    ),
    "sudbury primary school": metres_catchment(3284.16, "Distance"),
}

TOWER_HAMLETS_CATCHMENT_SOURCE = {
    "name": "Tower Hamlets Council reception places offered",
    "year": 2026,
    "url": "https://www.towerhamlets.gov.uk/lgnl/education_and_learning/schools/school_admissions/primary_school_admissions.aspx",
}

TOWER_HAMLETS_2026_CATCHMENTS = {
    "bigland green primary school": metres_catchment(537, "tie-break cut off"),
    "mayflower primary school": metres_catchment(515, "tie-break cut off"),
}

SUTTON_CATCHMENT_SOURCE = {
    "name": "Sutton Council primary school allocation information",
    "year": 2026,
    "url": "https://www.sutton.gov.uk/w/primary-school-allocation-information",
}

SUTTON_2026_CATCHMENTS = {
    "all saints carshalton ce primary school": no_distance_catchment(
        "Voluntary-aided school; Sutton source says contact the school direct"
    ),
    "all saints carshalton church of england primary school": no_distance_catchment(
        "Voluntary-aided school; Sutton source says contact the school direct"
    ),
    "barrow hedges primary school": metres_catchment(1171.54, "furthest distance"),
    "brookfield primary academy": all_offered_catchment(),
    "cheam common infants": metres_catchment(1006.55, "furthest distance"),
    "cheam common junior academy": metres_catchment(1006.55, "linked infant allocation"),
    "cheam fields primary academy": metres_catchment(1214.74, "furthest distance"),
    "cheam park farm primary academy": metres_catchment(3317.13, "furthest distance"),
    "manor park primary academy": metres_catchment(464.02, "furthest distance"),
    "robin hood infants": all_offered_catchment(),
    "robin hood junior school": all_offered_catchment("Linked infant school: all applicants offered"),
    "st cecilia's catholic primary school": no_distance_catchment(
        "Voluntary-aided school; Sutton source says contact the school direct"
    ),
    "st elphege's rc infants": all_offered_catchment(),
    "st elphege's rc junior school": all_offered_catchment(
        "Linked infant school: all applicants offered"
    ),
    "westbourne primary school": metres_catchment(2416.15, "furthest distance"),
}

CATCHMENT_SOURCES_BY_BOROUGH = {
    "Barnet": BARNET_CATCHMENT_SOURCE,
    "Wandsworth": WANDSWORTH_CATCHMENT_SOURCE,
    "Haringey": HARINGEY_CATCHMENT_SOURCE,
    "Hackney": HACKNEY_CATCHMENT_SOURCE,
    "Ealing": EALING_CATCHMENT_SOURCE,
    "Harrow": HARROW_CATCHMENT_SOURCE,
    "Redbridge": REDBRIDGE_CATCHMENT_SOURCE,
    "Havering": HAVERING_CATCHMENT_SOURCE,
    "Newham": NEWHAM_CATCHMENT_SOURCE,
    "Brent": BRENT_CATCHMENT_SOURCE,
    "Tower Hamlets": TOWER_HAMLETS_CATCHMENT_SOURCE,
    "Sutton": SUTTON_CATCHMENT_SOURCE,
}

CATCHMENTS_BY_BOROUGH = {
    "Barnet": BARNET_2026_CATCHMENTS,
    "Wandsworth": WANDSWORTH_2026_CATCHMENTS,
    "Haringey": HARINGEY_2025_CATCHMENTS,
    "Hackney": HACKNEY_2026_CATCHMENTS,
    "Ealing": EALING_2026_CATCHMENTS,
    "Harrow": HARROW_2026_CATCHMENTS,
    "Redbridge": REDBRIDGE_2026_CATCHMENTS,
    "Havering": HAVERING_2026_CATCHMENTS,
    "Newham": NEWHAM_2026_CATCHMENTS,
    "Brent": BRENT_2026_CATCHMENTS,
    "Tower Hamlets": TOWER_HAMLETS_2026_CATCHMENTS,
    "Sutton": SUTTON_2026_CATCHMENTS,
}

LINKED_CATCHMENT_SCHOOL_ALIASES = {
    "honeywell junior school": {
        "catchment_key": "honeywell infant school",
        "source_school_name": "Honeywell Infant School",
        "reason": "Reception admissions are published for the linked infant school",
    },
    "rokesly junior school": {
        "catchment_key": "rokesly infant school",
        "source_school_name": "Rokesly Infant School",
        "reason": "Reception admissions are published for the linked infant school",
    },
    "south harringay junior school": {
        "catchment_key": "south harringay infant school",
        "source_school_name": "South Harringay Infant School",
        "reason": "Reception admissions are published for the linked infant school",
    },
    "deansbrook junior school": {
        "catchment_key": "deansbrook infant",
        "source_school_name": "Deansbrook Infant",
        "reason": "Reception admissions are published for the linked infant school",
    },
    "moss hall junior school": {
        "catchment_key": "moss hall infant",
        "source_school_name": "Moss Hall Infant",
        "reason": "Reception admissions are published for the linked infant school",
    },
    "brookland junior school": {
        "catchment_key": "brookland infant",
        "source_school_name": "Brookland Infant",
        "reason": "Reception admissions are published for the linked infant school",
    },
    "the annunciation rc junior school": {
        "catchment_key": "annunciation catholic infant",
        "source_school_name": "Annunciation Catholic Infant",
        "reason": "Reception admissions are published for the linked infant school",
    },
}


def normalize_school_name_for_catchment(name):
    normalized = (name or "").lower()
    normalized = normalized.replace("&", "and")
    normalized = normalized.replace("’", "'")
    normalized = normalized.replace(",", " ")
    normalized = re.sub(r"\bnursery and\b", "", normalized)
    normalized = re.sub(r"\bcofe\b", "ce", normalized)
    normalized = re.sub(r"\bchurch of england\b", "ce", normalized)
    normalized = re.sub(r"\bprimary academy\b", "primary school", normalized)
    normalized = re.sub(r"\bschool putney\b", "school putney", normalized)
    normalized = re.sub(r"[^a-z0-9']+", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def catchment_lookup_key(row):
    name = normalize_school_name_for_catchment(row.get("school_name"))
    if row.get("borough") == "Barnet" and name == "st mary's ce primary school":
        return name
    aliases = {
        "all saints ce primary school putney": "all saints ce primary school",
        "st mary's ce primary school": "st mary's ce primary school putney",
        "st mary's ce primary school putney": "st mary's ce primary school putney",
        "st michael's ce primary school": "st michael's ce primary school",
        "roehampton church forest primary school": "roehampton church forest school",
        "rutherford house school": "rutherford house primary school",
        "lift trinity": "trinity primary academy",
        "lift noel park": "noel park primary school",
        "hoxton garden primary": "hoxton garden primary school",
    }
    if name in LINKED_CATCHMENT_SCHOOL_ALIASES:
        return LINKED_CATCHMENT_SCHOOL_ALIASES[name]["catchment_key"]
    return aliases.get(name, name)


def catchment_alias_note(row):
    name = normalize_school_name_for_catchment(row.get("school_name"))
    alias = LINKED_CATCHMENT_SCHOOL_ALIASES.get(name)
    if not alias:
        return None
    return f"{alias['reason']} ({alias['source_school_name']})"


def add_catchment_metadata(rows):
    for row in rows:
        row["catchment_radius_m"] = None
        row["catchment_source_year"] = None
        row["catchment_source_name"] = None
        row["catchment_source_url"] = None
        row["catchment_note"] = None

        borough = row.get("borough")
        catchments = CATCHMENTS_BY_BOROUGH.get(borough)
        source = CATCHMENT_SOURCES_BY_BOROUGH.get(borough)
        if not catchments or not source:
            continue

        catchment = catchments.get(catchment_lookup_key(row))
        if not catchment:
            continue

        row["catchment_radius_m"] = catchment.get("radius_m")
        row["catchment_source_year"] = source["year"]
        row["catchment_source_name"] = source["name"]
        row["catchment_source_url"] = source["url"]
        note = catchment["note"]
        alias_note = catchment_alias_note(row)
        if alias_note:
            note = f"{note}; {alias_note}"
        row["catchment_note"] = note


def parse_number(value):
    if value in MISSING:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_age_upper(age_range):
    match = re.match(r"^(\d+) to (\d+)$", age_range or "")
    if not match:
        return None
    return int(match.group(2))


def extract_postcode(address):
    address = (address or "").replace(", z", "").strip()
    match = POSTCODE_RE.search(address.upper())
    if not match:
        return None
    postcode = re.sub(r"\s+", "", match.group(1))
    return f"{postcode[:-3]} {postcode[-3:]}"


def load_school_info():
    schools = {}
    with INFO_CSV.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if not row["new_la_code"].startswith("E090"):
                continue
            if row["iclose"] != "0":
                continue

            age_upper = parse_age_upper(row["agerange"])
            if age_upper is None or age_upper > 11:
                continue

            schools[row["school_urn"]] = {
                "school_urn": row["school_urn"],
                "school_name": row["school_name"],
                "borough": row["la_name"],
                "age_range": row["agerange"],
                "eligible_pupils": parse_int(row["telig"]),
                "total_pupils": parse_float(row["totpups"]),
                "fsm_percent": parse_number(row["ptfsm6cla1a"]),
                "religious_denomination": row["reldenom"],
                "school_type_code": row["nftype"],
                "full_address": row["full_address"].replace(", z", ""),
                "postcode": extract_postcode(row["full_address"]),
            }
    return schools


def load_workforce_metrics():
    metrics = {}
    if not WORKFORCE_CSV.exists():
        return metrics

    with WORKFORCE_CSV.open(newline="", encoding="latin1") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if row["time_period"] != "202425":
                continue
            teachers = parse_float(row["fte_all_teachers"])
            if not row["school_urn"] or teachers is None or teachers <= 0:
                continue
            metrics[row["school_urn"]] = {
                "fte_all_teachers": teachers,
            }
    return metrics


def load_performance(schools):
    subject_map = {
        "Reading, writing and maths": ("expected_rwm", "higher_rwm"),
        "Reading": ("reading_score",),
        "Maths": ("maths_score",),
        "Grammar, punctuation and spelling": ("gps_score",),
    }

    metrics = defaultdict(dict)
    with PERFORMANCE_CSV.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if row["time_period"] != "202425":
                continue
            if row["school_urn"] not in schools:
                continue
            if row["breakdown_topic"] != "All pupils" or row["breakdown"] != "Total":
                continue
            if row["subject"] not in subject_map:
                continue

            school_metrics = metrics[row["school_urn"]]
            if row["subject"] == "Reading, writing and maths":
                school_metrics["expected_rwm"] = parse_number(
                    row["expected_standard_pupil_percent"]
                )
                school_metrics["higher_rwm"] = parse_number(
                    row["higher_standard_pupil_percent"]
                )
            elif row["subject"] == "Reading":
                school_metrics["reading_score"] = parse_number(
                    row["average_scaled_score"]
                )
            elif row["subject"] == "Maths":
                school_metrics["maths_score"] = parse_number(row["average_scaled_score"])
            elif row["subject"] == "Grammar, punctuation and spelling":
                school_metrics["gps_score"] = parse_number(row["average_scaled_score"])

    ranked_rows = []
    for urn, school in schools.items():
        school_metrics = metrics.get(urn, {})
        needed = [
            "expected_rwm",
            "higher_rwm",
            "reading_score",
            "maths_score",
            "gps_score",
        ]
        if any(school_metrics.get(key) is None for key in needed):
            continue
        if not school["eligible_pupils"] or school["eligible_pupils"] < 11:
            continue

        row = dict(school)
        row.update(school_metrics)
        row["mean_scaled_score"] = statistics.mean(
            [row["reading_score"], row["maths_score"], row["gps_score"]]
        )
        ranked_rows.append(row)

    return ranked_rows


def add_percentiles(rows, metric_keys):
    for metric in metric_keys:
        ordered = sorted(row[metric] for row in rows)
        percentile_by_value = {}
        total = len(ordered)
        idx = 0
        while idx < total:
            end = idx + 1
            while end < total and ordered[end] == ordered[idx]:
                end += 1
            average_rank = ((idx + 1) + end) / 2
            percentile_by_value[ordered[idx]] = average_rank / total
            idx = end

        for row in rows:
            row[f"{metric}_percentile"] = percentile_by_value[row[metric]]


def percentile_lookup(values):
    ordered = sorted(value for value in values if value is not None)
    if not ordered:
        return {}
    percentile_by_value = {}
    total = len(ordered)
    idx = 0
    while idx < total:
        end = idx + 1
        while end < total and ordered[end] == ordered[idx]:
            end += 1
        average_rank = ((idx + 1) + end) / 2
        percentile_by_value[ordered[idx]] = average_rank / total
        idx = end
    return percentile_by_value


def geocode_postcodes(postcodes):
    if GEOCODE_CACHE.exists():
        cache = json.loads(GEOCODE_CACHE.read_text(encoding="utf-8"))
    else:
        cache = {}

    uncached = [
        postcode
        for postcode in sorted(set(postcodes))
        if postcode and (postcode not in cache or "lsoa_code" not in cache[postcode])
    ]
    for start in range(0, len(uncached), 100):
        batch = uncached[start : start + 100]
        request = urllib.request.Request(
            "https://api.postcodes.io/postcodes",
            data=json.dumps({"postcodes": batch}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request) as response:
            payload = json.load(response)
        for item in payload["result"]:
            result = item["result"]
            cache[item["query"]] = {
                "latitude": None if result is None else result["latitude"],
                "longitude": None if result is None else result["longitude"],
                "lsoa_code": None if result is None else result.get("codes", {}).get("lsoa"),
                "lsoa_name": None if result is None else result.get("lsoa"),
            }

    GEOCODE_CACHE.write_text(json.dumps(cache, indent=2, sort_keys=True), encoding="utf-8")
    return cache


def bulk_geocode_postcodes(postcodes, cache_path):
    if cache_path.exists():
        cache = json.loads(cache_path.read_text(encoding="utf-8"))
    else:
        cache = {}

    uncached = [
        postcode
        for postcode in sorted(set(postcodes))
        if postcode and postcode not in cache
    ]
    total_batches = math.ceil(len(uncached) / 100) if uncached else 0
    for start in range(0, len(uncached), 100):
        batch = uncached[start : start + 100]
        batch_number = (start // 100) + 1
        print(f"Geocoding postcode batch {batch_number}/{total_batches}")
        request = urllib.request.Request(
            "https://api.postcodes.io/postcodes",
            data=json.dumps({"postcodes": batch}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
        for item in payload["result"]:
            result = item["result"]
            cache[item["query"]] = {
                "latitude": None if result is None else result["latitude"],
                "longitude": None if result is None else result["longitude"],
                "lsoa_code": None if result is None else result.get("codes", {}).get("lsoa"),
                "lsoa_name": None if result is None else result.get("lsoa"),
            }
        cache_path.write_text(json.dumps(cache, indent=2, sort_keys=True), encoding="utf-8")

    cache_path.write_text(json.dumps(cache, indent=2, sort_keys=True), encoding="utf-8")
    return cache


def geocode_address(address):
    url = (
        "https://nominatim.openstreetmap.org/search?"
        + urllib.parse.urlencode({"q": address, "format": "jsonv2", "limit": 1})
    )
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "codex-school-map/1.0"},
    )
    with urllib.request.urlopen(request) as response:
        payload = json.load(response)
    if not payload:
        return {"latitude": None, "longitude": None, "lsoa_code": None, "lsoa_name": None}
    return {
        "latitude": float(payload[0]["lat"]),
        "longitude": float(payload[0]["lon"]),
        "lsoa_code": None,
        "lsoa_name": None,
    }


def ensure_price_paid_files():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    paths = []
    for year in TERRACE_PRICE_YEARS:
        path = DATA_DIR / f"pp-{year}.csv"
        paths.append(path)
        if path.exists() and path.stat().st_size > 1_000_000:
            continue
        url = PRICE_PAID_URL_TEMPLATE.format(year=year)
        print(f"Downloading {url}")
        with urllib.request.urlopen(url) as response, path.open("wb") as handle:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                handle.write(chunk)
    return paths


def normalize_postcode(postcode):
    postcode = re.sub(r"\s+", "", (postcode or "").upper())
    if len(postcode) < 5:
        return None
    return f"{postcode[:-3]} {postcode[-3:]}"


def load_london_terrace_sales():
    sales = []
    for path in ensure_price_paid_files():
        with path.open(newline="", encoding="latin1") as handle:
            reader = csv.reader(handle)
            for row in reader:
                if len(row) < 14:
                    continue
                if row[4] != "T":
                    continue
                try:
                    sale_date = dt.datetime.strptime(row[2][:10], "%Y-%m-%d").date()
                except ValueError:
                    continue
                if sale_date < TERRACE_PRICE_START_DATE:
                    continue
                district = row[12].strip().upper()
                county = row[13].strip().upper()
                if district not in LONDON_BOROUGHS and county != "GREATER LONDON":
                    continue
                postcode = normalize_postcode(row[3])
                if not postcode:
                    continue
                try:
                    price = int(row[1])
                except ValueError:
                    continue
                sales.append({"postcode": postcode, "price": price})
    return sales


def distance_km(lat1, lon1, lat2, lon2):
    earth_km = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    h = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )
    return 2 * earth_km * math.asin(math.sqrt(h))


def add_terrace_price_metrics(rows):
    sales = load_london_terrace_sales()
    print(f"Loaded {len(sales)} recent London terraced sales")
    geocodes = bulk_geocode_postcodes(
        (sale["postcode"] for sale in sales),
        PRICE_POSTCODE_CACHE,
    )

    geocoded_sales = []
    for sale in sales:
        geocode = geocodes.get(sale["postcode"], {})
        lat = geocode.get("latitude")
        lon = geocode.get("longitude")
        if lat is None or lon is None:
            continue
        geocoded_sales.append({
            "latitude": lat,
            "longitude": lon,
            "price": sale["price"],
        })
    print(f"Geocoded {len(geocoded_sales)} recent London terraced sales")

    for row in rows:
        lat_window = TERRACE_PRICE_RADIUS_KM / 111
        lon_window = TERRACE_PRICE_RADIUS_KM / (111 * max(0.2, math.cos(math.radians(row["latitude"]))))
        prices = [
            sale["price"]
            for sale in geocoded_sales
            if abs(sale["latitude"] - row["latitude"]) <= lat_window
            and abs(sale["longitude"] - row["longitude"]) <= lon_window
            if distance_km(
                row["latitude"],
                row["longitude"],
                sale["latitude"],
                sale["longitude"],
            )
            <= TERRACE_PRICE_RADIUS_KM
        ]
        row["terrace_sales_count_2y_0_5mi"] = len(prices)
        if prices:
            row["terrace_avg_price_2y_0_5mi"] = round(statistics.mean(prices))
            row["terrace_median_price_2y_0_5mi"] = round(statistics.median(prices))
        else:
            row["terrace_avg_price_2y_0_5mi"] = None
            row["terrace_median_price_2y_0_5mi"] = None


def latest_crime_month():
    try:
        with urllib.request.urlopen(POLICE_LAST_UPDATED_URL, timeout=30) as response:
            payload = json.load(response)
        return payload["date"][:7]
    except Exception:
        return "2026-03"


def load_crime_cache():
    if CRIME_CACHE.exists():
        return json.loads(CRIME_CACHE.read_text(encoding="utf-8"))
    return {}


def save_crime_cache(cache):
    CRIME_CACHE.write_text(json.dumps(cache, indent=2, sort_keys=True), encoding="utf-8")


def fetch_family_crime_count(lat, lon, month):
    query = urllib.parse.urlencode({
        "lat": f"{lat:.6f}",
        "lng": f"{lon:.6f}",
        "date": month,
    })
    # data.police.uk currently rejects the older TLS stack in the system Python
    # on this Mac, while curl negotiates the endpoint correctly.
    response = subprocess.run(
        [
            "curl",
            "-fsSL",
            "--max-time",
            "45",
            "-A",
            "codex-school-map/1.0",
            f"{POLICE_STREET_CRIME_URL}?{query}",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    crimes = json.loads(response.stdout)

    weighted_count = 0.0
    category_counts = defaultdict(int)
    for crime in crimes:
        category = crime.get("category", "other-crime")
        category_counts[category] += 1
        weighted_count += FAMILY_CRIME_WEIGHTS.get(category, 0.8)

    return {
        "month": month,
        "weighted_count": round(weighted_count, 1),
        "total_count": len(crimes),
        "category_counts": dict(category_counts),
    }


def ensure_imd_file():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if IMD_CSV.exists() and IMD_CSV.stat().st_size > 1_000_000:
        return IMD_CSV
    print(f"Downloading {IMD_CSV_URL}")
    with urllib.request.urlopen(IMD_CSV_URL, timeout=60) as response, IMD_CSV.open("wb") as handle:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            handle.write(chunk)
    return IMD_CSV


def load_imd_metrics():
    path = ensure_imd_file()
    metrics = {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            lsoa_code = row["LSOA code (2011)"]
            rank = parse_int(row["Index of Multiple Deprivation (IMD) Rank (where 1 is most deprived)"])
            decile = parse_int(row["Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOAs)"])
            score = parse_float(row["Index of Multiple Deprivation (IMD) Score"])
            if not lsoa_code or rank is None:
                continue
            metrics[lsoa_code] = {
                "imd_rank": rank,
                "imd_decile": decile,
                "imd_score": score,
                "imd_lsoa_name": row["LSOA name (2011)"],
                "imd_local_authority": row["Local Authority District name (2019)"],
            }
    return metrics


def imd_row_to_metrics(row):
    return {
        "imd_rank": parse_int(row["Index of Multiple Deprivation Rank"]),
        "imd_decile": parse_int(row["Index of Multiple Deprivation Decile"]),
        "imd_score": None,
        "imd_lsoa_name": row["LSOA Name"],
        "imd_local_authority": None,
        "lsoa_code": row["LSOA code"],
        "lsoa_name": row["LSOA Name"],
    }


def load_imd_postcode_cache():
    if IMD_POSTCODE_CACHE.exists():
        return json.loads(IMD_POSTCODE_CACHE.read_text(encoding="utf-8"))
    return {}


def save_imd_postcode_cache(cache):
    IMD_POSTCODE_CACHE.write_text(json.dumps(cache, indent=2, sort_keys=True), encoding="utf-8")


def fetch_imd_postcode_metrics(postcodes):
    postcodes = [postcode for postcode in postcodes if postcode]
    if not postcodes:
        return {}

    cache = load_imd_postcode_cache()
    missing = [postcode for postcode in postcodes if postcode not in cache]
    if missing:
        postcode_payload = "\n".join(missing)
        response = subprocess.run(
            [
                "curl",
                "-fsSL",
                "-X",
                "POST",
                "-F",
                f"postcodes={postcode_payload}",
                f"{IMD_POSTCODE_LOOKUP_BASE}/ajax/upload",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        upload = json.loads(response.stdout)
        poll_path = upload["poll-path"]
        files = None
        for _ in range(30):
            poll = subprocess.run(
                ["curl", "-fsSL", f"{IMD_POSTCODE_LOOKUP_ORIGIN}{poll_path}"],
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(poll.stdout)
            if payload.get("completed"):
                files = payload["files"]
                break
        if files is None:
            raise RuntimeError("Timed out waiting for IMD postcode lookup")

        csv_response = subprocess.run(
            ["curl", "-fsSL", f"{IMD_POSTCODE_LOOKUP_ORIGIN}{files['csv']}"],
            check=True,
            capture_output=True,
            text=True,
        )
        for row in csv.DictReader(csv_response.stdout.splitlines()):
            postcode = normalize_postcode(row["Postcode"])
            cache[postcode] = imd_row_to_metrics(row)
        save_imd_postcode_cache(cache)

    return {postcode: cache.get(postcode) for postcode in postcodes}


def add_family_area_metrics(rows):
    month = latest_crime_month()
    cache = load_crime_cache()
    imd_metrics = load_imd_metrics()
    print(f"Using police street-crime month: {month}")

    unmatched_postcodes = [
        row["postcode"]
        for row in rows
        if row.get("lsoa_code") not in imd_metrics
    ]
    postcode_imd_metrics = fetch_imd_postcode_metrics(unmatched_postcodes)

    for index, row in enumerate(rows, start=1):
        key = f"{row['school_urn']}:{month}:{row['latitude']:.5f}:{row['longitude']:.5f}"
        if key not in cache:
            print(f"Fetching local crime {index}/{len(rows)}: {row['school_name']}")
            try:
                cache[key] = fetch_family_crime_count(row["latitude"], row["longitude"], month)
            except Exception as exc:
                cache[key] = {
                    "month": month,
                    "weighted_count": None,
                    "total_count": None,
                    "category_counts": {},
                    "error": str(exc),
                }
            save_crime_cache(cache)

        crime = cache[key]
        row["recent_crime_month"] = crime.get("month", month)
        row["recent_family_crime_weighted_count_1mi"] = crime.get("weighted_count")
        row["recent_crime_total_count_1mi"] = crime.get("total_count")
        imd = imd_metrics.get(row.get("lsoa_code")) or postcode_imd_metrics.get(row.get("postcode"))
        if imd:
            row.update(imd)
        else:
            row["imd_rank"] = None
            row["imd_decile"] = None
            row["imd_score"] = None
            row["imd_lsoa_name"] = None
            row["imd_local_authority"] = None

    crime_lookup = percentile_lookup(
        row.get("recent_family_crime_weighted_count_1mi") for row in rows
    )
    max_imd_rank = max((metric["imd_rank"] for metric in imd_metrics.values()), default=None)

    for row in rows:
        crime_count = row.get("recent_family_crime_weighted_count_1mi")

        safety = None if crime_count is None else 1 - crime_lookup.get(crime_count, 0)
        lower_deprivation = None
        if row.get("imd_rank") is not None and max_imd_rank:
            lower_deprivation = row["imd_rank"] / max_imd_rank

        row["area_safety_percentile"] = None if safety is None else round(safety * 100, 1)
        row["imd_lower_deprivation_percentile"] = (
            None if lower_deprivation is None else round(lower_deprivation * 100, 1)
        )

        components = [
            (safety, 0.50),
            (lower_deprivation, 0.50),
        ]
        available = [(value, weight) for value, weight in components if value is not None]
        if available:
            weight_total = sum(weight for _, weight in available)
            row["family_area_rating"] = round(
                100 * sum(value * weight for value, weight in available) / weight_total,
                1,
            )
        else:
            row["family_area_rating"] = None


def slugify_school_name_for_performance_url(name):
    normalized = (name or "").lower()
    normalized = normalized.replace("&", " and ")
    normalized = normalized.replace("’", "")
    normalized = normalized.replace("'", "")
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    return re.sub(r"^-+|-+$", "", normalized)


def school_performance_url(row):
    urn = row.get("school_urn")
    slug = slugify_school_name_for_performance_url(row.get("school_name"))
    if not urn or not slug:
        return None
    return f"https://www.compare-school-performance.service.gov.uk/school/{urn}/{slug}/primary"


def add_performance_urls(rows):
    for row in rows:
        row["performance_url"] = school_performance_url(row)


def build_map_html(rows, ranked_count=None):
    rows = [dict(row) for row in rows]
    add_performance_urls(rows)
    ranked_count_label = f"{ranked_count:,}" if ranked_count is not None else "n/a"
    rows_json = json.dumps(rows, ensure_ascii=False)
    rank_values = [row["rank"] for row in rows]
    min_rank = min(rank_values)
    max_rank = max(rank_values)
    rank_span = max_rank - min_rank or 1

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Top 500 London KS2 Schools (2025)</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="">
  <style>
    :root {{
      --bg: #f5efe4;
      --panel: rgba(255, 252, 246, 0.96);
      --ink: #182126;
      --muted: #5c6770;
      --accent: #045d56;
      --accent-2: #b8432f;
      --border: rgba(24, 33, 38, 0.12);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Avenir Next", "Segoe UI", sans-serif;
      color: var(--ink);
      overflow: hidden;
      background:
        radial-gradient(circle at top left, rgba(4, 93, 86, 0.16), transparent 38%),
        radial-gradient(circle at bottom right, rgba(184, 67, 47, 0.16), transparent 36%),
        var(--bg);
    }}
    .layout {{
      display: grid;
      grid-template-columns: minmax(320px, 430px) 1fr;
      height: 100vh;
      overflow: hidden;
    }}
    .sidebar {{
      padding: 24px 20px 20px;
      background: var(--panel);
      backdrop-filter: blur(12px);
      border-right: 1px solid var(--border);
      overflow: auto;
      min-height: 0;
    }}
    h1 {{
      margin: 0 0 10px;
      font-size: 1.9rem;
      line-height: 1.05;
      letter-spacing: -0.03em;
    }}
    .subhead {{
      margin: 0 0 18px;
      color: var(--muted);
      font-size: 0.98rem;
      line-height: 1.4;
    }}
    .meta {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
      margin-bottom: 18px;
    }}
    .card {{
      padding: 12px 14px;
      border: 1px solid var(--border);
      border-radius: 14px;
      background: rgba(255,255,255,0.68);
    }}
    .card strong {{
      display: block;
      font-size: 1.15rem;
    }}
    .card span {{
      color: var(--muted);
      font-size: 0.86rem;
    }}
    .method {{
      margin: 0 0 18px;
      padding: 14px;
      border-left: 4px solid var(--accent);
      background: rgba(4, 93, 86, 0.08);
      border-radius: 10px;
      font-size: 0.93rem;
      line-height: 1.45;
    }}
    .method h2 {{
      margin: 0 0 8px;
      font-size: 0.98rem;
      letter-spacing: -0.01em;
    }}
    .method p {{
      margin: 0 0 8px;
    }}
    .method ul {{
      margin: 0;
      padding-left: 18px;
    }}
    .method li {{
      margin: 5px 0;
    }}
    .filter-tool {{
      display: grid;
      gap: 10px;
      margin: 0 0 18px;
      padding: 14px;
      border: 1px solid var(--border);
      border-radius: 14px;
      background: rgba(255,255,255,0.74);
    }}
    .filter-title {{
      font-weight: 700;
      font-size: 0.98rem;
    }}
    .filter-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }}
    .range-label {{
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: baseline;
    }}
    input[type="range"] {{
      accent-color: var(--accent);
    }}
    label {{
      display: grid;
      gap: 5px;
      color: var(--muted);
      font-size: 0.78rem;
    }}
    select,
    input,
    button {{
      width: 100%;
      border: 1px solid rgba(24, 33, 38, 0.22);
      border-radius: 8px;
      background: #fffdf8;
      color: var(--ink);
      font: inherit;
      min-height: 34px;
      padding: 7px 9px;
    }}
    button {{
      cursor: pointer;
      font-weight: 700;
      background: #182126;
      color: #fffdf8;
    }}
    button.secondary {{
      background: #fffdf8;
      color: var(--ink);
    }}
    .filter-status {{
      color: var(--muted);
      font-size: 0.86rem;
      line-height: 1.35;
    }}
    .filter-note {{
      color: var(--muted);
      font-size: 0.78rem;
      line-height: 1.35;
    }}
    .map-panel {{
      position: relative;
      min-height: 100vh;
    }}
    .floating-filter-widget {{
      position: absolute;
      top: 16px;
      right: 16px;
      z-index: 700;
      width: min(360px, calc(100% - 32px));
      max-height: calc(100vh - 32px);
      margin: 0;
      gap: 8px;
      padding: 12px;
      overflow: auto;
      background: rgba(255, 252, 246, 0.94);
      border-color: rgba(24, 33, 38, 0.16);
      box-shadow: 0 22px 60px rgba(24, 33, 38, 0.22);
    }}
    .floating-filter-widget .filter-title {{
      font-size: 0.86rem;
    }}
    .floating-filter-widget .filter-status,
    .floating-filter-widget .filter-note {{
      font-size: 0.72rem;
    }}
    .floating-filter-widget label {{
      font-size: 0.72rem;
    }}
    .floating-filter-widget select,
    .floating-filter-widget input,
    .floating-filter-widget button {{
      min-height: 30px;
      padding: 5px 8px;
      font-size: 0.82rem;
    }}
    .table-wrap {{
      border: 1px solid var(--border);
      border-radius: 16px;
      overflow: hidden;
      background: rgba(255,255,255,0.72);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
    }}
    thead {{
      position: sticky;
      top: 0;
      background: #fff8ef;
      z-index: 1;
    }}
    th, td {{
      padding: 10px 12px;
      text-align: left;
      border-bottom: 1px solid var(--border);
      vertical-align: top;
    }}
    tbody tr {{
      cursor: pointer;
    }}
    tbody tr:hover,
    tbody tr.active {{
      background: rgba(4, 93, 86, 0.1);
    }}
    .rank {{
      font-variant-numeric: tabular-nums;
      font-weight: 700;
      color: var(--accent-2);
    }}
    .school {{
      font-weight: 650;
      margin-bottom: 2px;
    }}
    .borough {{
      color: var(--muted);
      font-size: 0.82rem;
    }}
    .catchment-match {{
      color: var(--accent);
      font-size: 0.82rem;
      font-weight: 650;
    }}
    .price-line {{
      color: var(--muted);
      font-size: 0.82rem;
    }}
    .area-line {{
      color: var(--accent-2);
      font-size: 0.82rem;
      font-weight: 650;
    }}
    #map {{
      height: 100vh;
    }}
    .catchment-halo {{
      filter: drop-shadow(0 0 6px rgba(184, 67, 47, 0.48));
    }}
    .school-rank-marker {{
      display: grid;
      place-items: center;
      width: 28px;
      height: 28px;
      border: 2.5px solid #182126;
      border-radius: 999px;
      background: var(--marker-color);
      color: #fffdf8;
      font-size: 0.62rem;
      font-weight: 850;
      line-height: 1;
      letter-spacing: -0.04em;
      box-shadow: 0 5px 14px rgba(24, 33, 38, 0.26);
    }}
    .leaflet-popup-content-wrapper {{
      border-radius: 14px;
    }}
    .popup h3 {{
      margin: 0 0 6px;
      font-size: 1rem;
    }}
    .popup-subtitle {{
      margin: -2px 0 8px;
      color: var(--muted);
      font-size: 0.82rem;
      line-height: 1.35;
    }}
    .popup-section {{
      margin-top: 9px;
      padding-top: 8px;
      border-top: 1px solid var(--border);
    }}
    .popup-section h4 {{
      margin: 0 0 6px;
      color: var(--accent);
      font-size: 0.72rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}
    .popup-metric-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 6px;
    }}
    .popup-metric {{
      padding: 7px 8px;
      border: 1px solid var(--border);
      border-radius: 10px;
      background: rgba(255, 252, 246, 0.76);
    }}
    .popup-metric strong {{
      display: block;
      font-size: 0.88rem;
      line-height: 1.1;
    }}
    .popup-metric span {{
      display: block;
      margin-top: 3px;
      color: var(--muted);
      font-size: 0.68rem;
      line-height: 1.1;
    }}
    .popup-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.8rem;
    }}
    .popup-table th,
    .popup-table td {{
      padding: 5px 0;
      border-bottom: 1px solid rgba(24, 33, 38, 0.08);
      vertical-align: top;
    }}
    .popup-table th {{
      width: 45%;
      color: var(--muted);
      font-weight: 650;
      text-align: left;
    }}
    .popup-table td {{
      color: var(--ink);
      font-weight: 650;
      text-align: right;
    }}
    .popup-section-note {{
      margin: 6px 0 0;
      color: var(--muted);
      font-size: 0.76rem;
      line-height: 1.35;
    }}
    .popup-section-note a {{
      color: var(--accent);
      font-weight: 750;
      text-decoration: none;
    }}
    .popup-section-note a:hover {{
      text-decoration: underline;
    }}
    .popup-address {{
      margin-top: 8px;
      padding-top: 7px;
      border-top: 1px solid rgba(24, 33, 38, 0.08);
      color: var(--muted);
      font-size: 0.76rem;
      line-height: 1.35;
    }}
    .flag {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 1rem;
      height: 1rem;
      margin-left: 0.35rem;
      border-radius: 999px;
      background: #c53a2f;
      color: #fff;
      font-size: 0.68rem;
      line-height: 1;
      vertical-align: middle;
      box-shadow: 0 4px 10px rgba(197, 58, 47, 0.25);
    }}
    .flag-ratio {{
      background: #225ea8;
      box-shadow: 0 4px 10px rgba(34, 94, 168, 0.25);
    }}
    .flag-faith {{
      background: #9a6700;
      box-shadow: 0 4px 10px rgba(154, 103, 0, 0.25);
    }}
    .flag-nonfaith {{
      background: #45556c;
      box-shadow: 0 4px 10px rgba(69, 85, 108, 0.25);
    }}
    .popup p {{
      margin: 4px 0;
      font-size: 0.9rem;
    }}
    .popup .minor {{
      color: var(--muted);
    }}
    .map-flag {{
      display: flex;
      align-items: center;
      justify-content: center;
      width: 14px;
      height: 14px;
      border-radius: 999px;
      background: #c53a2f;
      color: #fff;
      border: 1.5px solid #fff8ef;
      font-size: 9px;
      font-weight: 700;
      line-height: 1;
      box-shadow: 0 3px 10px rgba(197, 58, 47, 0.35);
    }}
    .map-flag-ratio {{
      background: #225ea8;
      box-shadow: 0 3px 10px rgba(34, 94, 168, 0.35);
    }}
    .map-flag-all {{
      width: 24px;
      border-radius: 999px;
      background: #2f7d4f;
      font-size: 8px;
      letter-spacing: 0.02em;
      box-shadow: 0 3px 10px rgba(47, 125, 79, 0.35);
    }}
    .origin-dot {{
      display: grid;
      place-items: center;
      width: 20px;
      height: 20px;
      border-radius: 999px;
      background: #182126;
      border: 3px solid #fff8ef;
      box-shadow: 0 8px 18px rgba(24, 33, 38, 0.35);
    }}
    .origin-dot::after {{
      content: "";
      width: 6px;
      height: 6px;
      border-radius: 999px;
      background: #fff8ef;
    }}
    .connector-distance-label {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 3px 6px;
      border-radius: 999px;
      border: 1px solid rgba(4, 93, 86, 0.28);
      background: rgba(255, 252, 246, 0.94);
      color: #045d56;
      font-size: 0.72rem;
      font-weight: 750;
      line-height: 1;
      white-space: nowrap;
      box-shadow: 0 4px 12px rgba(24, 33, 38, 0.18);
    }}
    .share-row {{
      display: flex;
      gap: 8px;
      align-items: center;
      margin-top: 10px;
      padding-top: 8px;
      border-top: 1px solid var(--border);
    }}
    .share-row button,
    .share-row a {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 30px;
      width: auto;
      padding: 6px 9px;
      border-radius: 8px;
      font-size: 0.78rem;
      font-weight: 750;
      text-decoration: none;
    }}
    .share-row a {{
      border: 1px solid rgba(24, 33, 38, 0.18);
      background: #fffdf8;
      color: var(--ink);
    }}
    @media (max-width: 980px) {{
      body {{
        overflow: auto;
      }}
      .layout {{
        grid-template-columns: 1fr;
        height: auto;
        overflow: visible;
      }}
      .sidebar {{
        max-height: 42vh;
      }}
      #map {{
        min-height: 64vh;
        height: 64vh;
      }}
      .map-panel {{
        min-height: 64vh;
      }}
      .floating-filter-widget {{
        position: sticky;
        top: 10px;
        right: auto;
        width: calc(100% - 20px);
        max-height: none;
        margin: 10px;
      }}
    }}
  </style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <h1>Top 500 London Primary-Age Schools</h1>
      <p class="subhead">2025 KS2 results, ranked from official DfE school-level attainment data and mapped by school postcode.</p>
      <p class="subhead"><strong>Tip:</strong> click a school marker for details; click empty map space to find schools whose source-backed catchment contains that point.</p>
      <div class="meta">
        <div class="card"><strong>{len(rows)}</strong><span>Schools on the map</span></div>
        <div class="card"><strong>{ranked_count_label}</strong><span>London schools ranked</span></div>
        <div class="card"><strong>5 metrics</strong><span>Used in the composite</span></div>
        <div class="card"><strong>11+</strong><span>Minimum eligible pupils</span></div>
      </div>
      <div class="method">
        <h2>Methodology</h2>
        <p><strong>Top 500:</strong> all London primary-age schools with 2025 KS2 results are scored first; the 500 highest composite scores are mapped.</p>
        <ul>
          <li><strong>Academic score:</strong> average percentile across five DfE measures: Reading, Maths and GPS scaled scores, plus Reading/Writing/Maths at expected and higher standards. Higher is better.</li>
          <li><strong>Eligibility:</strong> excludes closed schools, schools outside London, schools above primary age, and cohorts below 11 eligible pupils.</li>
          <li><strong>Location:</strong> school postcodes are geocoded, so markers are approximate postcode-level locations.</li>
          <li><strong>House-price filter:</strong> median/average sold price for terraced houses within 0.5 miles, using HM Land Registry Price Paid Data since 16 May 2024. Popups show sale counts because small samples can be noisy.</li>
          <li><strong>Family area rating:</strong> 0-100 proxy, split 50/50 between recent local safety and lower deprivation. Safety uses weighted data.police.uk street-level crimes within 1 mile; deprivation uses the English Index of Multiple Deprivation 2019 for the school postcode LSOA.</li>
          <li><strong>Catchment-point search:</strong> clicking the map highlights schools whose latest source-backed numeric catchment radius contains that point. Schools marked ALL are still source-backed, but have no cut-off radius to test against.</li>
          <li><strong>Catchment circles:</strong> shown only where the latest official allocation source gives a distance or explicit no-distance outcome. Sources now include Barnet 2026, Brent 2026, Ealing 2026, Hackney 2026, Haringey 2025, Harrow 2026, Havering 2026, Newham 2026, Redbridge 2026, Sutton 2026, Tower Hamlets 2026, and Wandsworth 2026. Source-backed schools have an amber halo before you click. A green ALL badge means all applicants were offered or demand was met, so no cut-off radius was needed. No estimated catchment distances are used.</li>
        </ul>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Rank</th>
              <th>School</th>
              <th>Comp.</th>
            </tr>
          </thead>
          <tbody id="rankings"></tbody>
        </table>
      </div>
    </aside>
    <main class="map-panel">
      <div id="map"></div>
      <div id="floatingFilters" class="filter-tool floating-filter-widget">
        <div class="filter-title">Filters</div>
        <div class="filter-title">Catchment point</div>
        <button id="clearCatchmentSearch" class="secondary" type="button">Clear catchment point</button>
        <div id="catchmentSearchStatus" class="filter-status">Map clicks find source-backed catchment circles containing that point.</div>
        <div class="filter-note">Only schools with numeric catchment radii can be matched. ALL/no-radius entries remain visible as source-backed catchments, but cannot contain a point mathematically.</div>
        <div class="filter-title">Nearby terraced-house sold prices</div>
        <div class="filter-grid">
          <label>
            Max price
            <input id="priceMax" type="number" min="0" step="25000" placeholder="e.g. 900000">
          </label>
          <label>
            Price measure
            <select id="priceMetric">
              <option value="median">Median sold price</option>
              <option value="average">Average sold price</option>
            </select>
          </label>
        </div>
        <button id="clearPrice" class="secondary" type="button">Clear price filter</button>
        <div id="priceStatus" class="filter-status">Uses terraced sales within 0.5 miles in the last 2 years.</div>
        <div class="filter-note">Source: HM Land Registry Price Paid Data. Small samples can be lumpy, so each popup includes the sale count.</div>
        <div class="filter-title">Family area rating</div>
        <label>
          <span class="range-label"><span>Minimum family area rating</span><strong id="familyAreaMinValue">50</strong></span>
          <input id="familyAreaMin" type="range" min="0" max="100" step="1" value="50">
        </label>
        <button id="clearFamilyArea" class="secondary" type="button">Clear area filter</button>
        <div id="familyAreaStatus" class="filter-status">Family area rating blends safety and lower deprivation, weighted equally.</div>
        <div class="filter-note">Safety uses recent data.police.uk street-level crimes within 1 mile. Deprivation uses the official English Index of Multiple Deprivation 2019 for the school postcode LSOA.</div>
        <div class="filter-title">School type and free school meals (FSM)</div>
        <div class="filter-grid">
          <label>
            Faith status
            <select id="faithFilter">
              <option value="all">Faith and non-faith</option>
              <option value="faith">Faith schools only</option>
              <option value="nonfaith" selected>Non-faith schools only</option>
            </select>
          </label>
          <label>
            <span class="range-label"><span>Max free school meals eligibility</span><strong id="fsmMaxValue">100%</strong></span>
            <input id="fsmMax" type="range" min="0" max="100" step="1" value="100">
          </label>
        </div>
        <button id="clearSchoolFilters" class="secondary" type="button">Clear school filters</button>
        <div id="schoolFilterStatus" class="filter-status">Showing non-faith schools at any free-school-meals level.</div>
      </div>
    </main>
  </div>

  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  <script>
    const schools = {rows_json};
    const map = L.map("map", {{ zoomControl: true }});
    L.tileLayer("https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png", {{
      maxZoom: 18,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }}).addTo(map);

    const rowsEl = document.getElementById("rankings");
    const filterToolEl = document.getElementById("floatingFilters");
    const clearCatchmentSearchEl = document.getElementById("clearCatchmentSearch");
    const catchmentSearchStatusEl = document.getElementById("catchmentSearchStatus");
    const priceMaxEl = document.getElementById("priceMax");
    const priceMetricEl = document.getElementById("priceMetric");
    const clearPriceEl = document.getElementById("clearPrice");
    const priceStatusEl = document.getElementById("priceStatus");
    const familyAreaMinEl = document.getElementById("familyAreaMin");
    const familyAreaMinValueEl = document.getElementById("familyAreaMinValue");
    const clearFamilyAreaEl = document.getElementById("clearFamilyArea");
    const familyAreaStatusEl = document.getElementById("familyAreaStatus");
    const faithFilterEl = document.getElementById("faithFilter");
    const fsmMaxEl = document.getElementById("fsmMax");
    const fsmMaxValueEl = document.getElementById("fsmMaxValue");
    const clearSchoolFiltersEl = document.getElementById("clearSchoolFilters");
    const schoolFilterStatusEl = document.getElementById("schoolFilterStatus");
    const markerByRank = new Map();
    const schoolLayers = new Map();
    const rowByRank = new Map();
    const catchmentState = {{
      circle: null
    }};
    const catchmentSearchState = {{
      active: false,
      origin: null,
      originMarker: null,
      connectorLines: []
    }};
    const priceState = {{
      active: false,
      maxPrice: null,
      metric: "median"
    }};
    const filterState = {{
      faith: "nonfaith",
      fsmMax: 100,
      familyAreaMin: 50
    }};

    L.DomEvent.disableClickPropagation(filterToolEl);
    L.DomEvent.disableScrollPropagation(filterToolEl);

    function markerColor(rank) {{
      const t = (rank - {min_rank}) / {rank_span};
      const hue = 148 - (t * 110);
      return `hsl(${{hue}}, 68%, 44%)`;
    }}

    function schoolMarkerHtml(school) {{
      return `<div class="school-rank-marker" style="--marker-color: ${{markerColor(school.rank)}}" title="#${{school.rank}} ${{school.school_name}}">${{school.rank}}</div>`;
    }}

    function formatCurrency(value) {{
      if (!Number.isFinite(value)) return "n/a";
      if (value >= 1000000) return `£${{(value / 1000000).toFixed(value >= 10000000 ? 0 : 1)}}m`;
      return `£${{Math.round(value / 1000)}}k`;
    }}

    function priceValue(school) {{
      return priceState.metric === "average"
        ? school.terrace_avg_price_2y_0_5mi
        : school.terrace_median_price_2y_0_5mi;
    }}

    function slugifySchoolName(name) {{
      return String(name || "")
        .toLowerCase()
        .replace(/&/g, " and ")
        .replace(/['’]/g, "")
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/^-+|-+$/g, "");
    }}

    function schoolPerformanceUrl(school) {{
      return school.performance_url || `https://www.compare-school-performance.service.gov.uk/school/${{school.school_urn}}/${{slugifySchoolName(school.school_name)}}/primary`;
    }}

    function schoolShareUrl(school) {{
      const url = new URL(window.location.href);
      url.searchParams.set("school", school.rank);
      url.hash = `school-${{school.rank}}`;
      return url.toString();
    }}

    function selectedSchoolRankFromUrl() {{
      const params = new URLSearchParams(window.location.search);
      const queryRank = Number(params.get("school"));
      if (Number.isFinite(queryRank) && queryRank > 0) return queryRank;
      const hashMatch = window.location.hash.match(/^#school-(\\d+)$/);
      return hashMatch ? Number(hashMatch[1]) : null;
    }}

    function writeSelectedSchoolUrl(school) {{
      if (!window.history || !window.history.replaceState) return;
      history.replaceState(null, "", schoolShareUrl(school));
    }}

    function copySchoolLink(rank) {{
      const school = schools.find((item) => item.rank === rank);
      if (!school) return;
      const shareUrl = schoolShareUrl(school);
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(shareUrl);
      }}
    }}
    window.copySchoolLink = copySchoolLink;

    function popupHtml(school) {{
      const shareUrl = schoolShareUrl(school);
      const performanceUrl = schoolPerformanceUrl(school);
      const fsmFlag = school.fsm_percent > 35 ? '<span class="flag" title="More than 35% eligible for free school meals">!</span>' : '';
      const ratioFlag = school.anomalous_low_ptr ? '<span class="flag flag-ratio" title="Best 5% pupil-to-teacher ratio in London">T</span>' : '';
      const faithFlag = school.is_faith_school
        ? '<span class="flag flag-faith" title="Faith school">F</span>'
        : '<span class="flag flag-nonfaith" title="Non-faith school">N</span>';
      const nonFaithRankRow = !school.is_faith_school && school.non_faith_rank
        ? `<tr><th>Non-faith rank</th><td>#${{school.non_faith_rank}}</td></tr>`
        : '';
      const faithTypeLabel = school.is_faith_school
        ? `Faith (${{school.religious_denomination}})`
        : 'Non-faith';
      const catchmentMatchLine = catchmentSearchState.active && school.contains_catchment_point
        ? '<p class="popup-section-note"><strong>This school catchment contains the selected map point.</strong></p>'
        : '';
      const terraceCount = school.terrace_sales_count_2y_0_5mi || 0;
      const terraceRows = terraceCount
        ? `
            <tr><th>Median terrace</th><td>${{formatCurrency(school.terrace_median_price_2y_0_5mi)}}</td></tr>
            <tr><th>Average terrace</th><td>${{formatCurrency(school.terrace_avg_price_2y_0_5mi)}}</td></tr>
            <tr><th>Sales sample</th><td>${{terraceCount}} sales</td></tr>
          `
        : '<tr><th>Terraced sales</th><td>n/a</td></tr>';
      const familyAreaText = Number.isFinite(school.family_area_rating)
        ? `${{school.family_area_rating.toFixed(1)}}/100`
        : 'n/a';
      const safetyText = Number.isFinite(school.area_safety_percentile)
        ? school.area_safety_percentile
        : 'n/a';
      const deprivationText = Number.isFinite(school.imd_lower_deprivation_percentile)
        ? school.imd_lower_deprivation_percentile
        : 'n/a';
      const ptrText = school.pupils_per_teacher ? school.pupils_per_teacher.toFixed(1) : "n/a";
      const catchmentRadius = Number(school.catchment_radius_m);
      const catchmentLine = Number.isFinite(catchmentRadius) && catchmentRadius > 0
        ? `
            <table class="popup-table">
              <tr><th>Catchment distance</th><td>${{catchmentRadius.toLocaleString()}} m</td></tr>
              <tr><th>Published note</th><td>${{school.catchment_note}}</td></tr>
              <tr><th>Year</th><td>${{school.catchment_source_year}}</td></tr>
            </table>
            <p class="popup-section-note">Source: <a href="${{school.catchment_source_url}}" target="_blank" rel="noopener noreferrer">${{school.catchment_source_name}}</a></p>
          `
        : school.catchment_note
          ? `
              <table class="popup-table">
                <tr><th>Catchment distance</th><td>No cut-off distance</td></tr>
                <tr><th>Published note</th><td>${{school.catchment_note}}</td></tr>
                <tr><th>Year</th><td>${{school.catchment_source_year}}</td></tr>
              </table>
              <p class="popup-section-note">Source: <a href="${{school.catchment_source_url}}" target="_blank" rel="noopener noreferrer">${{school.catchment_source_name}}</a></p>
            `
          : `
              <table class="popup-table">
                <tr><th>Catchment distance</th><td>n/a</td></tr>
              </table>
              <p class="popup-section-note">No latest source-backed distance loaded yet.</p>
            `;
      return `
        <div class="popup">
          <h3>#${{school.rank}} ${{school.school_name}} ${{faithFlag}} ${{fsmFlag}} ${{ratioFlag}}</h3>
          <p class="popup-subtitle">${{school.borough}} · ${{school.age_range}} · ${{faithTypeLabel}}</p>
          ${{catchmentMatchLine}}

          <section class="popup-section popup-ranks">
            <h4>Rankings</h4>
            <div class="popup-metric-grid">
              <div class="popup-metric"><strong>#${{school.rank}}</strong><span>London</span></div>
              <div class="popup-metric"><strong>#${{school.borough_rank}}</strong><span>${{school.borough}}</span></div>
              <div class="popup-metric"><strong>${{school.composite_score.toFixed(1)}}</strong><span>Composite</span></div>
            </div>
            <table class="popup-table">
              ${{nonFaithRankRow}}
              <tr><th>Eligible pupils</th><td>${{school.eligible_pupils}}</td></tr>
              <tr><th>FSM eligible</th><td>${{school.fsm_percent}}%</td></tr>
              <tr><th>Pupils / teacher</th><td>${{ptrText}}</td></tr>
            </table>
          </section>

          <section class="popup-section">
            <h4>KS2 Results</h4>
            <table class="popup-table">
              <tr><th>Achieving expected standard</th><td>${{school.expected_rwm}}%</td></tr>
              <tr><th>Achieving higher standard</th><td>${{school.higher_rwm}}%</td></tr>
              <tr><th>Reading score</th><td>${{school.reading_score}}</td></tr>
              <tr><th>Maths score</th><td>${{school.maths_score}}</td></tr>
              <tr><th>GPS score</th><td>${{school.gps_score}}</td></tr>
            </table>
            <p class="popup-section-note"><a href="${{performanceUrl}}" target="_blank" rel="noopener noreferrer">DfE performance page</a></p>
          </section>

          <section class="popup-section">
            <h4>Area & Admissions</h4>
            <table class="popup-table">
              <tr><th>Family area rating</th><td>${{familyAreaText}}</td></tr>
              <tr><th>Safety percentile</th><td>${{safetyText}}</td></tr>
              <tr><th>Lower deprivation</th><td>${{deprivationText}}</td></tr>
              ${{terraceRows}}
            </table>
            <p class="popup-section-note">Terraced sales use 0.5 miles and the last 2 years.</p>
          </section>

          <section class="popup-section">
            <h4>Catchment</h4>
            ${{catchmentLine}}
          </section>

          <p class="popup-address">${{school.full_address}}</p>
          <div class="share-row">
            <button type="button" onclick="copySchoolLink(${{school.rank}})">Copy link</button>
            <a href="${{shareUrl}}" target="_blank" rel="noopener noreferrer">Direct link</a>
          </div>
        </div>
      `;
    }}

    function distanceKm(a, b) {{
      const earthKm = 6371;
      const toRad = (degrees) => degrees * Math.PI / 180;
      const dLat = toRad(b.lat - a.lat);
      const dLng = toRad(b.lng - a.lng);
      const lat1 = toRad(a.lat);
      const lat2 = toRad(b.lat);
      const h = Math.sin(dLat / 2) ** 2 + Math.cos(lat1) * Math.cos(lat2) * Math.sin(dLng / 2) ** 2;
      return 2 * earthKm * Math.asin(Math.sqrt(h));
    }}

    function setLayerDimmed(school, dimmed) {{
      const layers = schoolLayers.get(school.rank);
      if (!layers) return;
      if (typeof layers.marker.setStyle === "function") {{
        layers.marker.setStyle({{
          opacity: dimmed ? 0.28 : 0.95,
          fillOpacity: dimmed ? 0.18 : 0.92
        }});
      }} else if (typeof layers.marker.setOpacity === "function") {{
        layers.marker.setOpacity(dimmed ? 0.28 : 1);
      }}
      layers.overlays.forEach((overlay) => {{
        if (typeof overlay.setOpacity === "function") {{
          overlay.setOpacity(dimmed ? 0.22 : 1);
        }} else if (typeof overlay.setStyle === "function") {{
          overlay.setStyle({{ opacity: dimmed ? 0.22 : 0.95 }});
        }}
      }});
    }}

    function stopMapClick(event) {{
      if (event.originalEvent) L.DomEvent.stopPropagation(event.originalEvent);
    }}

    function updateCatchmentCircle(school) {{
      const radius = Number(school.catchment_radius_m);
      if (!Number.isFinite(radius) || radius <= 0) {{
        if (catchmentState.circle) {{
          map.removeLayer(catchmentState.circle);
          catchmentState.circle = null;
        }}
        return;
      }}

      const center = [school.latitude, school.longitude];
      if (catchmentState.circle) {{
        catchmentState.circle.setLatLng(center);
        catchmentState.circle.setRadius(radius);
      }} else {{
        catchmentState.circle = L.circle(center, {{
          radius,
          color: "#b8432f",
          weight: 2.25,
          dashArray: "8 6",
          fillColor: "#b8432f",
          fillOpacity: 0.08,
          interactive: false
        }}).addTo(map);
      }}
      catchmentState.circle.bringToBack();
    }}

    function renderRows(rows) {{
      rowsEl.innerHTML = "";
      rowByRank.clear();
      rows.forEach((school) => {{
        const fsmFlag = school.fsm_percent > 35 ? '<span class="flag" title="More than 35% eligible for free school meals">!</span>' : '';
        const ratioFlag = school.anomalous_low_ptr ? '<span class="flag flag-ratio" title="Best 5% pupil-to-teacher ratio in London">T</span>' : '';
        const faithFlag = school.is_faith_school
          ? '<span class="flag flag-faith" title="Faith school">F</span>'
          : '<span class="flag flag-nonfaith" title="Non-faith school">N</span>';
        const catchmentMatchText = catchmentSearchState.active && school.contains_catchment_point
          ? '<div class="catchment-match">Contains selected map point</div>'
          : '';
        const selectedPrice = priceValue(school);
        const priceText = Number.isFinite(selectedPrice)
          ? `<div class="price-line">${{priceState.metric === "average" ? "Avg" : "Median"}} terrace: ${{formatCurrency(selectedPrice)}} (${{school.terrace_sales_count_2y_0_5mi}} sales)</div>`
          : '<div class="price-line">Terrace price: n/a</div>';
        const familyAreaText = Number.isFinite(school.family_area_rating)
          ? `<div class="area-line">Family area: ${{school.family_area_rating.toFixed(0)}}/100</div>`
          : '<div class="area-line">Family area: n/a</div>';
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td class="rank">${{school.rank}}</td>
          <td>
            <div class="school">${{school.school_name}} ${{faithFlag}} ${{fsmFlag}} ${{ratioFlag}}</div>
            <div class="borough">${{school.borough}}</div>
            ${{catchmentMatchText}}
            ${{familyAreaText}}
            ${{priceText}}
          </td>
          <td>${{school.composite_score.toFixed(1)}}</td>
        `;
        tr.addEventListener("click", () => activate(school.rank, {{ center: true }}));
        rowsEl.appendChild(tr);
        rowByRank.set(school.rank, tr);
      }});
    }}

    function clearCatchmentConnectorLines() {{
      catchmentSearchState.connectorLines.forEach((line) => map.removeLayer(line));
      catchmentSearchState.connectorLines = [];
    }}

    function drawCatchmentConnectorLines(origin) {{
      clearCatchmentConnectorLines();
      schools
        .filter((school) => school.contains_catchment_point)
        .forEach((school) => {{
          const schoolLatLng = L.latLng(school.latitude, school.longitude);
          const lineDistanceMetres = Math.round(distanceKm(origin, schoolLatLng) * 1000);
          const line = L.polyline([origin, [school.latitude, school.longitude]], {{
            color: "#045d56",
            weight: 2,
            opacity: 0.78,
            dashArray: "5 7",
            interactive: false
          }}).addTo(map);
          const labelLatLng = L.latLng(
            (origin.lat + school.latitude) / 2,
            (origin.lng + school.longitude) / 2
          );
          const label = L.marker(labelLatLng, {{
            icon: L.divIcon({{
              className: "",
              html: `<div class="connector-distance-label">${{lineDistanceMetres.toLocaleString()}} m</div>`,
              iconSize: [1, 1],
              iconAnchor: [0, 0]
            }}),
            keyboard: false,
            interactive: false
          }}).addTo(map);
          line.bringToBack();
          catchmentSearchState.connectorLines.push(line, label);
        }});
    }}

    function updateCatchmentSearch(origin) {{
      if (!origin) return;
      catchmentSearchState.active = true;
      catchmentSearchState.origin = origin;

      schools.forEach((school) => {{
        const radius = Number(school.catchment_radius_m);
        school.contains_catchment_point = Number.isFinite(radius) &&
          radius > 0 &&
          distanceKm(origin, {{ lat: school.latitude, lng: school.longitude }}) * 1000 <= radius;
      }});

      if (catchmentSearchState.originMarker) catchmentSearchState.originMarker.setLatLng(origin);
      else {{
        const originIcon = L.divIcon({{
          className: "",
          html: '<div class="origin-dot" title="Selected catchment point"></div>',
          iconSize: [20, 20],
          iconAnchor: [10, 10]
        }});
        catchmentSearchState.originMarker = L.marker(origin, {{ icon: originIcon, keyboard: false }}).addTo(map);
      }}

      drawCatchmentConnectorLines(origin);
      applyFilters();
    }}

    function clearCatchmentSearch() {{
      catchmentSearchState.active = false;
      catchmentSearchState.origin = null;
      schools.forEach((school) => {{
        delete school.contains_catchment_point;
        setLayerDimmed(school, false);
      }});
      if (catchmentSearchState.originMarker) {{
        map.removeLayer(catchmentSearchState.originMarker);
        catchmentSearchState.originMarker = null;
      }}
      clearCatchmentConnectorLines();
      applyFilters();
    }}

    function updatePriceFilter() {{
      const maxPrice = Number(priceMaxEl.value);
      priceState.metric = priceMetricEl.value;
      priceState.active = Number.isFinite(maxPrice) && maxPrice > 0;
      priceState.maxPrice = priceState.active ? maxPrice : null;
      applyFilters();
    }}

    function clearPriceFilter() {{
      priceState.active = false;
      priceState.maxPrice = null;
      priceMaxEl.value = "";
      applyFilters();
    }}

    function updateFamilyAreaFilter() {{
      filterState.familyAreaMin = Math.max(0, Math.min(100, Number(familyAreaMinEl.value) || 0));
      familyAreaMinEl.value = filterState.familyAreaMin;
      familyAreaMinValueEl.textContent = filterState.familyAreaMin;
      applyFilters();
    }}

    function clearFamilyAreaFilter() {{
      filterState.familyAreaMin = 0;
      familyAreaMinEl.value = "0";
      familyAreaMinValueEl.textContent = "0";
      applyFilters();
    }}

    function updateSchoolFilters() {{
      filterState.faith = faithFilterEl.value;
      filterState.fsmMax = Math.max(0, Math.min(100, Number(fsmMaxEl.value) || 0));
      fsmMaxEl.value = filterState.fsmMax;
      fsmMaxValueEl.textContent = `${{filterState.fsmMax}}%`;
      applyFilters();
    }}

    function clearSchoolFilters() {{
      filterState.faith = "all";
      filterState.fsmMax = 100;
      faithFilterEl.value = filterState.faith;
      fsmMaxEl.value = filterState.fsmMax;
      fsmMaxValueEl.textContent = "100%";
      applyFilters();
    }}

    function applyFilters() {{
      const matches = schools
        .filter((school) => {{
          const catchmentOk = !catchmentSearchState.active || school.contains_catchment_point;
          const selectedPrice = priceValue(school);
          const priceOk = !priceState.active || (Number.isFinite(selectedPrice) && selectedPrice <= priceState.maxPrice);
          const familyAreaOk = !filterState.familyAreaMin || (Number.isFinite(school.family_area_rating) && school.family_area_rating >= filterState.familyAreaMin);
          const faithOk =
            filterState.faith === "all" ||
            (filterState.faith === "faith" && school.is_faith_school) ||
            (filterState.faith === "nonfaith" && !school.is_faith_school);
          const fsmOk = Number.isFinite(school.fsm_percent) && school.fsm_percent <= filterState.fsmMax;
          return catchmentOk && priceOk && familyAreaOk && faithOk && fsmOk;
        }})
        .sort((a, b) => a.rank - b.rank);

      const matchRanks = new Set(matches.map((school) => school.rank));
      schools.forEach((school) => setLayerDimmed(school, !matchRanks.has(school.rank)));
      renderRows(matches);

      catchmentSearchStatusEl.textContent = catchmentSearchState.active
        ? `${{matches.length}} schools match all active filters and contain the selected point in their catchment.`
        : "Map clicks find source-backed catchment circles containing that point.";
      priceStatusEl.textContent = priceState.active
        ? `${{matches.length}} schools match all active filters. Price filter uses ${{priceState.metric}} <= ${{formatCurrency(priceState.maxPrice)}}.`
        : "Uses terraced sales within 0.5 miles in the last 2 years.";
      familyAreaStatusEl.textContent = filterState.familyAreaMin
        ? `${{matches.length}} schools match all active filters. Family area rating >= ${{filterState.familyAreaMin}}.`
        : "Family area rating blends safety and lower deprivation, weighted equally.";
      const faithLabel = filterState.faith === "faith"
        ? "faith schools"
        : filterState.faith === "nonfaith"
          ? "non-faith schools"
          : "faith and non-faith schools";
      schoolFilterStatusEl.textContent = `${{matches.length}} schools match all active filters. Showing ${{faithLabel}} with free school meals eligibility <= ${{filterState.fsmMax}}%.`;
    }}

    function activate(rank, options = {{}}) {{
      const {{ center = false, updateUrl = true }} = options;
      rowByRank.forEach((row, key) => row.classList.toggle("active", key === rank));
      const marker = markerByRank.get(rank);
      const school = schools.find((item) => item.rank === rank);
      if (school) {{
        updateCatchmentCircle(school);
        if (updateUrl) writeSelectedSchoolUrl(school);
      }}
      if (marker) {{
        marker.openPopup();
        if (center) {{
          map.flyTo(marker.getLatLng(), Math.max(map.getZoom(), 12), {{
            animate: true,
            duration: 0.45
          }});
        }}
      }}
    }}

    const bounds = [];
    schools.forEach((school) => {{
      const fsmFlag = school.fsm_percent > 35 ? '<span class="flag" title="More than 35% eligible for free school meals">!</span>' : '';
      const ratioFlag = school.anomalous_low_ptr ? '<span class="flag flag-ratio" title="Best 5% pupil-to-teacher ratio in London">T</span>' : '';
      const faithFlag = school.is_faith_school
        ? '<span class="flag flag-faith" title="Faith school">F</span>'
        : '<span class="flag flag-nonfaith" title="Non-faith school">N</span>';
      const markerIcon = L.divIcon({{
        className: "",
        html: schoolMarkerHtml(school),
        iconSize: [28, 28],
        iconAnchor: [14, 14],
        popupAnchor: [0, -14]
      }});
      const marker = L.marker([school.latitude, school.longitude], {{
        icon: markerIcon,
        keyboard: false,
        bubblingMouseEvents: false
      }});
      marker.bindPopup(() => popupHtml(school));
      marker.on("click", (event) => {{
        stopMapClick(event);
        activate(school.rank);
      }});

      const overlays = [];
      if (school.catchment_note) {{
        const catchmentHalo = L.circleMarker([school.latitude, school.longitude], {{
          radius: 13,
          weight: 3.5,
          color: "#b8432f",
          opacity: 0.95,
          fill: false,
          interactive: false,
          className: "catchment-halo"
        }});
        catchmentHalo.addTo(map);
        overlays.push(catchmentHalo);
      }}

      marker.addTo(map);
      markerByRank.set(school.rank, marker);
      schoolLayers.set(school.rank, {{ marker, overlays }});
      bounds.push([school.latitude, school.longitude]);

      const catchmentNoteLower = (school.catchment_note || "").toLowerCase();
      if (catchmentNoteLower.includes("all applicants offered") || catchmentNoteLower === "demand met") {{
        const allApplicantsIcon = L.divIcon({{
          className: "",
          html: '<div class="map-flag map-flag-all" title="All applicants were offered a place, or demand was met">ALL</div>',
          iconSize: [24, 16],
          iconAnchor: [12, -3]
        }});
        const allApplicantsOverlay = L.marker([school.latitude, school.longitude], {{
          icon: allApplicantsIcon,
          keyboard: false,
          bubblingMouseEvents: false
        }});
        allApplicantsOverlay.on("click", (event) => {{
          stopMapClick(event);
          activate(school.rank);
        }});
        allApplicantsOverlay.addTo(map);
        schoolLayers.get(school.rank).overlays.push(allApplicantsOverlay);
      }}

      if (school.fsm_percent > 35) {{
        const flagIcon = L.divIcon({{
          className: "",
          html: '<div class="map-flag" title="More than 35% eligible for free school meals">!</div>',
          iconSize: [18, 18],
          iconAnchor: [-1, 17]
        }});
        const flagOverlay = L.marker([school.latitude, school.longitude], {{
          icon: flagIcon,
          keyboard: false,
          bubblingMouseEvents: false
        }});
        flagOverlay.on("click", (event) => {{
          stopMapClick(event);
          activate(school.rank);
        }});
        flagOverlay.addTo(map);
        schoolLayers.get(school.rank).overlays.push(flagOverlay);
      }}

      if (school.anomalous_low_ptr) {{
        const ratioIcon = L.divIcon({{
          className: "",
          html: '<div class="map-flag map-flag-ratio" title="Best 5% pupil-to-teacher ratio in London">T</div>',
          iconSize: [18, 18],
          iconAnchor: [19, 1]
        }});
        const ratioOverlay = L.marker([school.latitude, school.longitude], {{
          icon: ratioIcon,
          keyboard: false,
          bubblingMouseEvents: false
        }});
        ratioOverlay.on("click", (event) => {{
          stopMapClick(event);
          activate(school.rank);
        }});
        ratioOverlay.addTo(map);
        schoolLayers.get(school.rank).overlays.push(ratioOverlay);
      }}
    }});

    applyFilters();
    map.on("click", (event) => updateCatchmentSearch(event.latlng));
    clearCatchmentSearchEl.addEventListener("click", clearCatchmentSearch);
    priceMaxEl.addEventListener("input", updatePriceFilter);
    priceMetricEl.addEventListener("change", updatePriceFilter);
    clearPriceEl.addEventListener("click", clearPriceFilter);
    familyAreaMinEl.addEventListener("input", updateFamilyAreaFilter);
    clearFamilyAreaEl.addEventListener("click", clearFamilyAreaFilter);
    faithFilterEl.addEventListener("change", updateSchoolFilters);
    fsmMaxEl.addEventListener("input", updateSchoolFilters);
    clearSchoolFiltersEl.addEventListener("click", clearSchoolFilters);
    map.fitBounds(bounds, {{ padding: [26, 26] }});
    const initialSelectedRank = selectedSchoolRankFromUrl();
    if (initialSelectedRank) {{
      activate(initialSelectedRank, {{ center: true, updateUrl: false }});
    }}
  </script>
</body>
</html>
"""


def write_csv(path, rows):
    fieldnames = [
        "rank",
        "borough_rank",
        "school_name",
        "borough",
        "school_urn",
        "performance_url",
        "age_range",
        "eligible_pupils",
        "total_pupils",
        "fsm_percent",
        "religious_denomination",
        "is_faith_school",
        "non_faith_rank",
        "fte_all_teachers",
        "pupils_per_teacher",
        "anomalous_low_ptr",
        "composite_score",
        "expected_rwm",
        "higher_rwm",
        "reading_score",
        "maths_score",
        "gps_score",
        "mean_scaled_score",
        "postcode",
        "latitude",
        "longitude",
        "lsoa_code",
        "lsoa_name",
        "terrace_sales_count_2y_0_5mi",
        "terrace_avg_price_2y_0_5mi",
        "terrace_median_price_2y_0_5mi",
        "family_area_rating",
        "area_safety_percentile",
        "imd_lower_deprivation_percentile",
        "imd_rank",
        "imd_decile",
        "imd_score",
        "imd_lsoa_name",
        "imd_local_authority",
        "recent_family_crime_weighted_count_1mi",
        "recent_crime_total_count_1mi",
        "recent_crime_month",
        "catchment_radius_m",
        "catchment_source_year",
        "catchment_source_name",
        "catchment_source_url",
        "catchment_note",
        "full_address",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key) for key in fieldnames})


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    schools = load_school_info()
    ranked_rows = load_performance(schools)
    workforce_metrics = load_workforce_metrics()

    metric_keys = [
        "reading_score",
        "maths_score",
        "gps_score",
        "expected_rwm",
        "higher_rwm",
    ]
    add_percentiles(ranked_rows, metric_keys)

    for row in ranked_rows:
        row["composite_score"] = 100 * statistics.mean(
            [row[f"{metric}_percentile"] for metric in metric_keys]
        )

    ranked_rows.sort(
        key=lambda row: (
            row["composite_score"],
            row["higher_rwm"],
            row["expected_rwm"],
            row["mean_scaled_score"],
        ),
        reverse=True,
    )

    for index, row in enumerate(ranked_rows, start=1):
        row["rank"] = index

    borough_rank_counters = defaultdict(int)
    for row in ranked_rows:
        borough_rank_counters[row["borough"]] += 1
        row["borough_rank"] = borough_rank_counters[row["borough"]]

    non_faith_counter = 0
    non_faith_values = {"Does not apply", "None", "Unknown", ""}
    for row in ranked_rows:
        row["is_faith_school"] = row["religious_denomination"] not in non_faith_values
        if row["is_faith_school"]:
            row["non_faith_rank"] = None
        else:
            non_faith_counter += 1
            row["non_faith_rank"] = non_faith_counter

    ptr_rows = []
    for row in ranked_rows:
        workforce = workforce_metrics.get(row["school_urn"])
        total_pupils = row.get("total_pupils")
        if workforce and total_pupils is not None and total_pupils > 0:
            row["fte_all_teachers"] = workforce["fte_all_teachers"]
            row["pupils_per_teacher"] = total_pupils / workforce["fte_all_teachers"]
            ptr_rows.append(row["pupils_per_teacher"])
        else:
            row["fte_all_teachers"] = None
            row["pupils_per_teacher"] = None

    ptr_rows.sort()
    if ptr_rows:
        ptr_threshold = ptr_rows[int((len(ptr_rows) - 1) * 0.05)]
    else:
        ptr_threshold = None

    for row in ranked_rows:
        row["anomalous_low_ptr"] = (
            ptr_threshold is not None
            and row["pupils_per_teacher"] is not None
            and row["pupils_per_teacher"] <= ptr_threshold
        )

    add_catchment_metadata(ranked_rows)
    add_performance_urls(ranked_rows)
    write_csv(ALL_RANKED_CSV, ranked_rows)

    top_rows = [dict(row) for row in ranked_rows[:TOP_N]]
    geocodes = geocode_postcodes(row["postcode"] for row in top_rows)

    mapped_rows = []
    for row in top_rows:
        geocode = geocodes.get(row["postcode"], {})
        if not geocode or geocode["latitude"] is None or geocode["longitude"] is None:
            geocode = geocode_address(row["full_address"])
        if geocode["latitude"] is None or geocode["longitude"] is None:
            continue
        row["latitude"] = geocode["latitude"]
        row["longitude"] = geocode["longitude"]
        row["lsoa_code"] = geocode.get("lsoa_code")
        row["lsoa_name"] = geocode.get("lsoa_name")
        mapped_rows.append(row)

    add_terrace_price_metrics(mapped_rows)
    add_family_area_metrics(mapped_rows)
    write_csv(TOP_300_CSV, mapped_rows)
    TOP_300_JSON.write_text(json.dumps(mapped_rows, indent=2, ensure_ascii=False), encoding="utf-8")
    MAP_HTML.write_text(build_map_html(mapped_rows, len(ranked_rows)), encoding="utf-8")

    print(f"Ranked London schools: {len(ranked_rows)}")
    print(f"Mapped top schools: {len(mapped_rows)}")
    print(f"Top ranked school: {ranked_rows[0]['school_name']} ({ranked_rows[0]['borough']})")
    print(f"Map written to: {MAP_HTML}")


if __name__ == "__main__":
    main()
