import requests
import  csv
import config

API_KEY = config.CENSUS_API_KEY
URL = 'https://api.census.gov/data/'
YEAR = '2018/'
DATA_SET = 'acs/acs5'
BASE_URL = URL + YEAR + DATA_SET
GET = '?get='
MED_GROSS_RENT = 'B25064_001E'
MED_GROSS_RENT_DOLLARS = 'B25064_001E'
GROSS_RENT_TOTAL = 'B25063_001E'
GROSS_RENT_PERCENT_INCOME_30_34 = 'B25070_007E'
GROSS_RENT_PERCENT_INCOME_35_39 = 'B25070_008E'
GROSS_RENT_PERCENT_INCOME_40_49 = 'B25070_009E'
GROSS_RENT_PERCENT_INCOME_50_PLUS = 'B25070_010E'

MED_INCOME = 'B06011_001E'
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


FINAL_URL = BASE_URL \
+ GET + GROSS_RENT_PERCENT_INCOME_50_PLUS \
+ FOR + COUNTY + "*" \
+ IN + STATE + OREGON

r = requests.get(url = FINAL_URL + API_KEY)
values = r.json()
severe_burden = {}

# get population of severe rent burdening by county
for i in range(1,len(values)):
    severe_burden[int(values[i][2])] = int(values[i][0])

FINAL_URL = BASE_URL \
+ GET + GROSS_RENT_PERCENT_INCOME_30_34 + COMMA +  GROSS_RENT_PERCENT_INCOME_35_39 + COMMA + GROSS_RENT_PERCENT_INCOME_40_49\
+ FOR + COUNTY + "*" \
+ IN + STATE + OREGON

r = requests.get(url = FINAL_URL + API_KEY)
values = r.json()
rent_burden = {}

# get sum population of rent burdening by county
for i in range(1,len(values)):
    rent_burden[int(values[i][4])] = int(values[i][0]) + int(values[i][1]) + int(values[i][2])
