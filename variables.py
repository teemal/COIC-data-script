import config

COUNTY_CODES = {
    "001": "Baker",
    "003": "Benton",
    "005": "Clackamas",
    "007": "Clatsop",
    "009": "Columbia",
    "011": "Coos",
    "013": "Crook",
    "015": "Curry",
    "017": "Deschutes",
    "019": "Douglas",
    "021": "Gilliam",
    "023": "Grant",
    "025": "Harney",
    "027": "Hood River",
    "029": "Jackson",
    "031": "Jefferson",
    "033": "Josephine",
    "035": "Klamath",
    "037": "Lake",
    "039": "Lane",
    "041": "Lincoln",
    "043": "Linn",
    "045": "Malheur",
    "047": "Marion",
    "049": "Morrow",
    "051": "Multnomah",
    "053": "Polk",
    "055": "Sherman",
    "057": "Tillamook",
    "059": "Umatilla",
    "061": "Union",
    "063": "Wallowa",
    "065": "Wasco",
    "067": "Washington",
    "069": "Wheeler",
    "071": "Yamhill"
}

# API setup and variables

API_KEY = config.CENSUS_API_KEY
URL = 'https://api.census.gov/data/'
YEAR = '2018/'
DATA_SET = 'acs/acs5'
BASE_URL = URL + YEAR + DATA_SET
GET = '?get='
MED_GROSS_RENT = 'B25064_001E'
GROSS_RENT_TOTAL = 'B25063_001E'
GROSS_RENT_PERCENT_INCOME_30_34 = 'B25070_007E'
GROSS_RENT_PERCENT_INCOME_35_39 = 'B25070_008E'
GROSS_RENT_PERCENT_INCOME_40_49 = 'B25070_009E'
GROSS_RENT_PERCENT_INCOME_50_PLUS = 'B25070_010E'
TOTAL_POPULATION_BURDENED = 'B25070_001E'

COMMA = ','
FOR = '&for='
IN = '&in='
PLUS = '+'
STATE = 'state:'
ALL_STATES = 'state:*'
COUNTY = 'county:'
OREGON = '41'
DESCHUTES = '017'
CROOK = '013'
JEFFERSON = '031'

income_brackets = [
"< $10k",
"$10k - $14.9k",
"$15k - $19.9k",
"$20k - $24.9k",
"$25k - $29.9k",
"$30k - $34.9k",
"$35k - $39.9k",
"$40k - $44.9k",
"$45k - $49.9k",
"$50k - $59.9k",
"$60k - $74.9k",
"$75k - $99.9k",
"$100k - $124.9k",
"$125k - $149.9k",
"$150k - $199.9k",
"$200k +"
]
