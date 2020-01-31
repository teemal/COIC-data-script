import requests
import config
import xlsxwriter


# API setup and variables
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
TOTAL_POPULATION_BURDENED = 'B25070_001E'
POPULATION_IN_POVERTY = 'B17001_002E'
TEST = 'B17003_001E'

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

# one of many query strings
FINAL_URL = BASE_URL \
+ GET + GROSS_RENT_PERCENT_INCOME_50_PLUS \
+ FOR + COUNTY + "*" \
+ IN + STATE + OREGON

r = requests.get(url = FINAL_URL + API_KEY)
values = r.json()
fips_severe_burden = {}

# get population of severe rent burdening by county
for i in range(1,len(values)):
    fips_severe_burden[values[i][2]] = int(values[i][0])

FINAL_URL = BASE_URL \
+ GET + GROSS_RENT_PERCENT_INCOME_30_34 + COMMA +  GROSS_RENT_PERCENT_INCOME_35_39 + COMMA + GROSS_RENT_PERCENT_INCOME_40_49\
+ FOR + COUNTY + "*" \
+ IN + STATE + OREGON

r = requests.get(url = FINAL_URL + API_KEY)
values = r.json()
fips_rent_burden = {}

# get sum population of rent burdening by county
for i in range(1,len(values)):
    fips_rent_burden[values[i][4]] = int(values[i][0]) + int(values[i][1]) + int(values[i][2])

FINAL_URL = BASE_URL \
+ GET + TOTAL_POPULATION_BURDENED \
+ FOR + COUNTY + "*" \
+ IN + STATE + OREGON

r = requests.get(url = FINAL_URL + API_KEY)
values = r.json()
fips_population = {}

# get total population of oregon counties
for i in range(1,len(values)):
    fips_population[values[i][2]] = int(values[i][0])


# TODO  POVERTY RATES
# FINAL_URL = BASE_URL \
# + GET + POPULATION_IN_POVERTY \
# + FOR + COUNTY + "*" \
# + IN + STATE + OREGON

# r = requests.get(url = FINAL_URL + API_KEY)
# values = r.json()
# pop_in_poverty = {}
# print(values)

# FINAL_URL = BASE_URL \
# + GET + TEST \
# + FOR + COUNTY + "*" \
# + IN + STATE + OREGON

# r = requests.get(url = FINAL_URL + API_KEY)
# values = r.json()
# pop_in_poverty = {}
# print(values)

fips_codes = {
"001" : "Baker",
"003" : "Benton",
"005" : "Clackamas",
"007" : "Clatsop",
"009" : "Columbia",
"011" : "Coos",
"013" : "Crook",
"015" : "Curry",
"017" : "Deschutes",
"019" : "Douglas",
"021" : "Gilliam",
"023" : "Grant",
"025" : "Harney",
"027" : "Hood River",
"029" : "Jackson",
"031" : "Jefferson",
"033" : "Josephine",
"035" : "Klamath",
"037" : "Lake",
"039" : "Lane",
"041" : "Lincoln",
"043" : "Linn",
"045" : "Malheur",
"047" : "Marion",
"049" : "Morrow",
"051" : "Multnomah",
"053" : "Polk",
"055" : "Sherman",
"057" : "Tillamook",
"059" : "Umatilla",
"061" : "Union",
"063" : "Wallowa",
"065" : "Wasco",
"067" : "Washington",
"069" : "Wheeler",
"071" : "Yamhill"
}

population = {}
severe_burden_total = {}
rent_burden_total = {}

# make new dicts with key as county name instead of fips
for key in fips_codes:
    if key in fips_population:
        population[fips_codes[key]] = fips_population[key]
        severe_burden_total[fips_codes[key]] = fips_severe_burden[key]
        rent_burden_total[fips_codes[key]] = fips_rent_burden[key]

# print("pop: \n")
# print(population)
# print(" ")
# print("sev burden: \n")
# print(severe_burden_total)
# print(" ")
# print("burden: \n")
# print(rent_burden_total)

severe_rent_burdened_by_pop = {}
rent_burdened_by_pop = {}
# new dicts with rent burden/pop as percent
for key in population:
    if key in rent_burden_total:
        # x100 to shift decimal into percent
        severe_rent_burdened_by_pop[key] = 100 * (severe_burden_total[key] / population[key])
        rent_burdened_by_pop[key] = 100 * (rent_burden_total[key] / population[key])

print("severe rent burdened: ")
print(severe_rent_burdened_by_pop)
print("")
print("rent burdened:")
print(rent_burdened_by_pop)

workbook = xlsxwriter.Workbook('data.xlsx')
worksheet = workbook.add_worksheet()
row = 0
col = 0
col_names = ['county', 'population', 'population rent burdened', 'population severly rent burdened']
for i in col_names:
    worksheet.write(row, col, i)
    col +=1
row = 1
col = 0
# there's probably a really slick way to  do this with a lambda
# but I'm tired and this works
for i in population:
    worksheet.write(row,col,i)
    col += 1
    worksheet.write(row,col,population[i])
    col += 1
    worksheet.write(row,col,rent_burdened_by_pop[i])
    col += 1
    worksheet.write(row,col,severe_rent_burdened_by_pop[i])
    row +=1
    col = 0

workbook.close()

