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

LINKED_CATCHMENT_SCHOOL_ALIASES = {
    "honeywell junior school": {
        "catchment_key": "honeywell infant school",
        "source_school_name": "Honeywell Infant School",
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
    aliases = {
        "all saints ce primary school putney": "all saints ce primary school",
        "st mary's ce primary school": "st mary's ce primary school putney",
        "st mary's ce primary school putney": "st mary's ce primary school putney",
        "st michael's ce primary school": "st michael's ce primary school",
        "roehampton church forest primary school": "roehampton church forest school",
        "rutherford house school": "rutherford house primary school",
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

        if row.get("borough") != "Wandsworth":
            continue

        catchment = WANDSWORTH_2026_CATCHMENTS.get(catchment_lookup_key(row))
        if not catchment:
            continue

        row["catchment_radius_m"] = catchment.get("radius_m")
        row["catchment_source_year"] = WANDSWORTH_CATCHMENT_SOURCE["year"]
        row["catchment_source_name"] = WANDSWORTH_CATCHMENT_SOURCE["name"]
        row["catchment_source_url"] = WANDSWORTH_CATCHMENT_SOURCE["url"]
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


def build_map_html(rows, ranked_count=None):
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
    .commute-tool {{
      display: grid;
      gap: 10px;
      margin: 0 0 18px;
      padding: 14px;
      border: 1px solid var(--border);
      border-radius: 14px;
      background: rgba(255,255,255,0.74);
    }}
    .commute-title {{
      font-weight: 700;
      font-size: 0.98rem;
    }}
    .commute-grid {{
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
    .commute-status {{
      color: var(--muted);
      font-size: 0.86rem;
      line-height: 1.35;
    }}
    .commute-note {{
      color: var(--muted);
      font-size: 0.78rem;
      line-height: 1.35;
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
    .commute-time {{
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
    .leaflet-popup-content-wrapper {{
      border-radius: 14px;
    }}
    .popup h3 {{
      margin: 0 0 6px;
      font-size: 1rem;
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
    }}
  </style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <h1>Top 500 London Primary-Age Schools</h1>
      <p class="subhead">2025 KS2 results, ranked from official DfE school-level attainment data and mapped by school postcode.</p>
      <p class="subhead"><strong>Tip:</strong> click a school marker for details; click empty map space to set a commute starting point.</p>
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
          <li><strong>Commute filter:</strong> rough distance-based estimates only, intended for shortlisting before checking live routes.</li>
          <li><strong>Catchment circles:</strong> shown only where the latest source-backed allocation distance is available. Wandsworth uses its 2026 reception allocation PDF; schools marked "all applicants offered" do not get a radius because no cut-off distance was needed.</li>
        </ul>
      </div>
      <div class="commute-tool">
        <div class="commute-title">Find schools near a commute point</div>
        <div class="commute-grid">
          <label>
            Minutes
            <input id="commuteMinutes" type="number" min="5" max="90" step="5" value="30">
          </label>
          <label>
            Mode
            <select id="commuteMode">
              <option value="transit">Transit estimate</option>
              <option value="cycle">Cycle</option>
              <option value="walk">Walk</option>
              <option value="drive">Drive</option>
            </select>
          </label>
        </div>
        <button id="clearCommute" class="secondary" type="button">Show all schools</button>
        <div id="commuteStatus" class="commute-status">Map clicks set commute points; marker clicks open school details.</div>
        <div class="commute-note">Times are approximate map-distance estimates, useful for shortlisting before checking live TfL or route details.</div>
        <div class="commute-title">Filter by nearby terraced-house sold prices</div>
        <div class="commute-grid">
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
        <div id="priceStatus" class="commute-status">Uses terraced sales within 0.5 miles in the last 2 years.</div>
        <div class="commute-note">Source: HM Land Registry Price Paid Data. Small samples can be lumpy, so each popup includes the sale count.</div>
        <div class="commute-title">Filter by family area rating</div>
        <label>
          <span class="range-label"><span>Minimum family area rating</span><strong id="familyAreaMinValue">50</strong></span>
          <input id="familyAreaMin" type="range" min="0" max="100" step="1" value="50">
        </label>
        <button id="clearFamilyArea" class="secondary" type="button">Clear area filter</button>
        <div id="familyAreaStatus" class="commute-status">Family area rating blends safety and lower deprivation, weighted equally.</div>
        <div class="commute-note">Safety uses recent data.police.uk street-level crimes within 1 mile. Deprivation uses the official English Index of Multiple Deprivation 2019 for the school postcode LSOA.</div>
        <div class="commute-title">Filter by school type and free school meals (FSM)</div>
        <div class="commute-grid">
          <label>
            Faith status
            <select id="faithFilter">
              <option value="all">Faith and non-faith</option>
              <option value="faith">Faith schools only</option>
              <option value="nonfaith">Non-faith schools only</option>
            </select>
          </label>
          <label>
            <span class="range-label"><span>Max free school meals eligibility</span><strong id="fsmMaxValue">100%</strong></span>
            <input id="fsmMax" type="range" min="0" max="100" step="1" value="100">
          </label>
        </div>
        <button id="clearSchoolFilters" class="secondary" type="button">Clear school filters</button>
        <div id="schoolFilterStatus" class="commute-status">Showing faith and non-faith schools at any free-school-meals level.</div>
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
    <main id="map"></main>
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
    const commuteMinutesEl = document.getElementById("commuteMinutes");
    const commuteModeEl = document.getElementById("commuteMode");
    const clearCommuteEl = document.getElementById("clearCommute");
    const commuteStatusEl = document.getElementById("commuteStatus");
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
    const commuteState = {{
      active: false,
      origin: null,
      originMarker: null,
      rangeCircle: null
    }};
    const commuteModes = {{
      transit: {{ label: "transit estimate", speedKmh: 18, routeFactor: 1.35, fixedMinutes: 8 }},
      cycle: {{ label: "cycle", speedKmh: 14, routeFactor: 1.25, fixedMinutes: 3 }},
      walk: {{ label: "walk", speedKmh: 4.8, routeFactor: 1.2, fixedMinutes: 1 }},
      drive: {{ label: "drive", speedKmh: 22, routeFactor: 1.35, fixedMinutes: 6 }}
    }};
    const priceState = {{
      active: false,
      maxPrice: null,
      metric: "median"
    }};
    const filterState = {{
      faith: "all",
      fsmMax: 100,
      familyAreaMin: 50
    }};

    function markerColor(rank) {{
      const t = (rank - {min_rank}) / {rank_span};
      const hue = 148 - (t * 110);
      return `hsl(${{hue}}, 68%, 44%)`;
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

    function popupHtml(school) {{
      const fsmFlag = school.fsm_percent > 25 ? '<span class="flag" title="More than 25% eligible for free school meals">!</span>' : '';
      const ratioFlag = school.anomalous_low_ptr ? '<span class="flag flag-ratio" title="Best 5% pupil-to-teacher ratio in London">T</span>' : '';
      const faithFlag = school.is_faith_school
        ? '<span class="flag flag-faith" title="Faith school">F</span>'
        : '<span class="flag flag-nonfaith" title="Non-faith school">N</span>';
      const nonFaithRankLine = !school.is_faith_school && school.non_faith_rank
        ? `<p><strong>Non-faith rank:</strong> #${{school.non_faith_rank}}</p>`
        : '';
      const faithTypeLabel = school.is_faith_school
        ? `Faith (${{school.religious_denomination}})`
        : 'Non-faith';
      const commuteLine = commuteState.active && Number.isFinite(school.commute_minutes)
        ? `<p>Estimated commute: <strong>${{school.commute_minutes.toFixed(0)}} min</strong></p>`
        : '';
      const terraceCount = school.terrace_sales_count_2y_0_5mi || 0;
      const terraceLine = terraceCount
        ? `<p>Nearby terraced sold prices: median <strong>${{formatCurrency(school.terrace_median_price_2y_0_5mi)}}</strong>, average <strong>${{formatCurrency(school.terrace_avg_price_2y_0_5mi)}}</strong> <span class="minor">(${{terraceCount}} sales, 0.5 mi, last 2y)</span></p>`
        : '<p>Nearby terraced sold prices: <strong>n/a</strong> <span class="minor">(no matching sales within 0.5 mi in the last 2y)</span></p>';
      const familyAreaLine = Number.isFinite(school.family_area_rating)
        ? `<p>Family area rating: <strong>${{school.family_area_rating.toFixed(1)}}/100</strong> <span class="minor">(safety ${{school.area_safety_percentile ?? "n/a"}}, lower deprivation ${{school.imd_lower_deprivation_percentile ?? "n/a"}}; IMD decile ${{school.imd_decile ?? "n/a"}}, local weighted crime ${{school.recent_family_crime_weighted_count_1mi ?? "n/a"}} in ${{school.recent_crime_month ?? "latest month"}})</span></p>`
        : '<p>Family area rating: <strong>n/a</strong></p>';
      const catchmentRadius = Number(school.catchment_radius_m);
      const catchmentLine = Number.isFinite(catchmentRadius) && catchmentRadius > 0
        ? `<p>Catchment distance: <strong>${{catchmentRadius.toLocaleString()}} m</strong> <span class="minor">(${{school.catchment_note}}, ${{school.catchment_source_year}}; source: <a href="${{school.catchment_source_url}}" target="_blank" rel="noopener noreferrer">${{school.catchment_source_name}}</a>)</span></p>`
        : school.catchment_note
          ? `<p>Catchment distance: <strong>No cut-off distance</strong> <span class="minor">(${{school.catchment_note}}, ${{school.catchment_source_year}}; source: <a href="${{school.catchment_source_url}}" target="_blank" rel="noopener noreferrer">${{school.catchment_source_name}}</a>)</span></p>`
          : '<p>Catchment distance: <strong>n/a</strong> <span class="minor">(no latest source-backed distance loaded yet)</span></p>';
      return `
        <div class="popup">
          <h3>#${{school.rank}} ${{school.school_name}} ${{faithFlag}} ${{fsmFlag}} ${{ratioFlag}}</h3>
          <p><strong>London rank:</strong> #${{school.rank}} · <strong>${{school.borough}} rank:</strong> #${{school.borough_rank}}</p>
          ${{nonFaithRankLine}}
          ${{commuteLine}}
          <p>School type: <strong>${{faithTypeLabel}}</strong></p>
          <p><strong>${{school.borough}}</strong> · ${{school.age_range}} · Eligible pupils: ${{school.eligible_pupils}}</p>
          <p>Free school meals eligible: <strong>${{school.fsm_percent}}%</strong></p>
          <p>Pupils per teacher: <strong>${{school.pupils_per_teacher ? school.pupils_per_teacher.toFixed(1) : "n/a"}}</strong> <span class="minor">(blue T = best 5% in London)</span></p>
          ${{familyAreaLine}}
          ${{catchmentLine}}
          ${{terraceLine}}
          <p>Composite: <strong>${{school.composite_score.toFixed(2)}}</strong></p>
          <p>Expected standard (RWM): <strong>${{school.expected_rwm}}%</strong></p>
          <p>Higher standard (RWM): <strong>${{school.higher_rwm}}%</strong></p>
          <p>Scaled scores: Reading <strong>${{school.reading_score}}</strong>, Maths <strong>${{school.maths_score}}</strong>, GPS <strong>${{school.gps_score}}</strong></p>
          <p class="minor">${{school.full_address}}</p>
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

    function estimateMinutes(origin, school) {{
      const mode = commuteModes[commuteModeEl.value] || commuteModes.transit;
      const km = distanceKm(origin, {{ lat: school.latitude, lng: school.longitude }}) * mode.routeFactor;
      return (km / mode.speedKmh * 60) + mode.fixedMinutes;
    }}

    function setLayerDimmed(school, dimmed) {{
      const layers = schoolLayers.get(school.rank);
      if (!layers) return;
      layers.marker.setStyle({{
        opacity: dimmed ? 0.28 : 0.95,
        fillOpacity: dimmed ? 0.18 : 0.92
      }});
      layers.overlays.forEach((overlay) => overlay.setOpacity(dimmed ? 0.22 : 1));
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
        const fsmFlag = school.fsm_percent > 25 ? '<span class="flag" title="More than 25% eligible for free school meals">!</span>' : '';
        const ratioFlag = school.anomalous_low_ptr ? '<span class="flag flag-ratio" title="Best 5% pupil-to-teacher ratio in London">T</span>' : '';
        const faithFlag = school.is_faith_school
          ? '<span class="flag flag-faith" title="Faith school">F</span>'
          : '<span class="flag flag-nonfaith" title="Non-faith school">N</span>';
        const commuteText = commuteState.active && Number.isFinite(school.commute_minutes)
          ? `<div class="commute-time">${{school.commute_minutes.toFixed(0)}} min estimated commute</div>`
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
            ${{commuteText}}
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

    function updateCommuteSearch(origin = commuteState.origin) {{
      if (!origin) return;
      commuteState.active = true;
      commuteState.origin = origin;

      const minutes = Math.max(5, Math.min(90, Number(commuteMinutesEl.value) || 30));
      commuteMinutesEl.value = minutes;
      const mode = commuteModes[commuteModeEl.value] || commuteModes.transit;

      schools.forEach((school) => {{
        school.commute_minutes = estimateMinutes(origin, school);
      }});

      if (commuteState.originMarker) commuteState.originMarker.setLatLng(origin);
      else {{
        const originIcon = L.divIcon({{
          className: "",
          html: '<div class="origin-dot" title="Commute starting point"></div>',
          iconSize: [20, 20],
          iconAnchor: [10, 10]
        }});
        commuteState.originMarker = L.marker(origin, {{ icon: originIcon, keyboard: false }}).addTo(map);
      }}

      const rangeMeters = (minutes - mode.fixedMinutes) / 60 * mode.speedKmh / mode.routeFactor * 1000;
      if (commuteState.rangeCircle) {{
        commuteState.rangeCircle.setLatLng(origin);
        commuteState.rangeCircle.setRadius(Math.max(0, rangeMeters));
      }} else {{
        commuteState.rangeCircle = L.circle(origin, {{
          radius: Math.max(0, rangeMeters),
          color: "#045d56",
          weight: 1.5,
          fillColor: "#045d56",
          fillOpacity: 0.08,
          interactive: false
        }}).addTo(map);
      }}

      applyFilters();
    }}

    function clearCommuteSearch() {{
      commuteState.active = false;
      commuteState.origin = null;
      schools.forEach((school) => {{
        delete school.commute_minutes;
        setLayerDimmed(school, false);
      }});
      if (commuteState.originMarker) {{
        map.removeLayer(commuteState.originMarker);
        commuteState.originMarker = null;
      }}
      if (commuteState.rangeCircle) {{
        map.removeLayer(commuteState.rangeCircle);
        commuteState.rangeCircle = null;
      }}
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
      const commuteMinutes = Math.max(5, Math.min(90, Number(commuteMinutesEl.value) || 30));
      const commuteMode = commuteModes[commuteModeEl.value] || commuteModes.transit;
      const matches = schools
        .filter((school) => {{
          const commuteOk = !commuteState.active || school.commute_minutes <= commuteMinutes;
          const selectedPrice = priceValue(school);
          const priceOk = !priceState.active || (Number.isFinite(selectedPrice) && selectedPrice <= priceState.maxPrice);
          const familyAreaOk = !filterState.familyAreaMin || (Number.isFinite(school.family_area_rating) && school.family_area_rating >= filterState.familyAreaMin);
          const faithOk =
            filterState.faith === "all" ||
            (filterState.faith === "faith" && school.is_faith_school) ||
            (filterState.faith === "nonfaith" && !school.is_faith_school);
          const fsmOk = Number.isFinite(school.fsm_percent) && school.fsm_percent <= filterState.fsmMax;
          return commuteOk && priceOk && familyAreaOk && faithOk && fsmOk;
        }})
        .sort((a, b) => a.rank - b.rank);

      const matchRanks = new Set(matches.map((school) => school.rank));
      schools.forEach((school) => setLayerDimmed(school, !matchRanks.has(school.rank)));
      renderRows(matches);

      commuteStatusEl.textContent = commuteState.active
        ? `${{matches.filter((school) => school.commute_minutes <= commuteMinutes).length}} matching schools within ${{commuteMinutes}} min by ${{commuteMode.label}}.`
        : "Map clicks set commute points; marker clicks open school details.";
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
      const {{ center = false }} = options;
      rowByRank.forEach((row, key) => row.classList.toggle("active", key === rank));
      const marker = markerByRank.get(rank);
      const school = schools.find((item) => item.rank === rank);
      if (school) updateCatchmentCircle(school);
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
      const fsmFlag = school.fsm_percent > 25 ? '<span class="flag" title="More than 25% eligible for free school meals">!</span>' : '';
      const ratioFlag = school.anomalous_low_ptr ? '<span class="flag flag-ratio" title="Best 5% pupil-to-teacher ratio in London">T</span>' : '';
      const faithFlag = school.is_faith_school
        ? '<span class="flag flag-faith" title="Faith school">F</span>'
        : '<span class="flag flag-nonfaith" title="Non-faith school">N</span>';
      const marker = L.circleMarker([school.latitude, school.longitude], {{
        radius: 7.5,
        weight: 2.75,
        color: "#182126",
        opacity: 0.95,
        fillColor: markerColor(school.rank),
        fillOpacity: 0.92,
        bubblingMouseEvents: false
      }});
      marker.bindPopup(() => popupHtml(school));
      marker.on("click", () => activate(school.rank));
      marker.addTo(map);
      markerByRank.set(school.rank, marker);
      schoolLayers.set(school.rank, {{ marker, overlays: [] }});
      bounds.push([school.latitude, school.longitude]);

      if (school.fsm_percent > 25) {{
        const flagIcon = L.divIcon({{
          className: "",
          html: '<div class="map-flag" title="More than 25% eligible for free school meals">!</div>',
          iconSize: [18, 18],
          iconAnchor: [-1, 17]
        }});
        const flagOverlay = L.marker([school.latitude, school.longitude], {{
          icon: flagIcon,
          keyboard: false,
          bubblingMouseEvents: false
        }});
        flagOverlay.on("click", () => activate(school.rank));
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
        ratioOverlay.on("click", () => activate(school.rank));
        ratioOverlay.addTo(map);
        schoolLayers.get(school.rank).overlays.push(ratioOverlay);
      }}
    }});

    applyFilters();
    map.on("click", (event) => updateCommuteSearch(event.latlng));
    commuteMinutesEl.addEventListener("change", () => updateCommuteSearch());
    commuteModeEl.addEventListener("change", () => updateCommuteSearch());
    clearCommuteEl.addEventListener("click", clearCommuteSearch);
    priceMaxEl.addEventListener("input", updatePriceFilter);
    priceMetricEl.addEventListener("change", updatePriceFilter);
    clearPriceEl.addEventListener("click", clearPriceFilter);
    familyAreaMinEl.addEventListener("input", updateFamilyAreaFilter);
    clearFamilyAreaEl.addEventListener("click", clearFamilyAreaFilter);
    faithFilterEl.addEventListener("change", updateSchoolFilters);
    fsmMaxEl.addEventListener("input", updateSchoolFilters);
    clearSchoolFiltersEl.addEventListener("click", clearSchoolFilters);
    map.fitBounds(bounds, {{ padding: [26, 26] }});
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
