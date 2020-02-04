import requests
import config
import xlsxwriter

fips_codes = {
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
MED_GROSS_RENT_DOLLARS = 'B25064_001E'
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

# one of many query strings. Below is an example of the string directly below it
# FINAL_URL = https://api.census.gov/data/2018/acs/acs5?get=B25070_010E&for=county:*&in=state:41
# this string will get the population of individuals that pay 50% or more of their income
# in rent for all counties in oregon.
# It returns a list of lists. The first list containing meta data and the following lists containing the requested info.
# i.e. one list being ['5690', '41', '047'], meaning 5690 people spend 50% or more of their income in the county 047 (FIPS code for Marion county) in the state 41 (FIPS code for Oregon)
FINAL_URL = BASE_URL \
    + GET + GROSS_RENT_PERCENT_INCOME_50_PLUS \
    + FOR + COUNTY + "*" \
    + IN + STATE + OREGON

r = requests.get(url=FINAL_URL + API_KEY)
# values is the return value from the census  API
values = r.json()
fips_severe_burden = {}

# ==========get population of severe rent burdening by county============================
for i in range(1, len(values)):
    fips_severe_burden[values[i][2]] = int(values[i][0])

FINAL_URL = BASE_URL \
    + GET + GROSS_RENT_PERCENT_INCOME_30_34 + COMMA + GROSS_RENT_PERCENT_INCOME_35_39 + COMMA + GROSS_RENT_PERCENT_INCOME_40_49\
    + FOR + COUNTY + "*" \
    + IN + STATE + OREGON

r = requests.get(url=FINAL_URL + API_KEY)
values = r.json()
fips_rent_burden = {}

# ==========get sum population of rent burdening by county==================================
for i in range(1, len(values)):
    fips_rent_burden[values[i][4]] = int(
        values[i][0]) + int(values[i][1]) + int(values[i][2])

FINAL_URL = BASE_URL \
    + GET + TOTAL_POPULATION_BURDENED \
    + FOR + COUNTY + "*" \
    + IN + STATE + OREGON

r = requests.get(url=FINAL_URL + API_KEY)
values = r.json()
fips_population = {}

# get total population of oregon counties
for i in range(1, len(values)):
    fips_population[values[i][2]] = int(values[i][0])


# ========HOUSEHOLD  INCOME FOR  ALL BRACKETS IN ALL COUNTIES=================================
# household_income is a dict of lists to store all income brackets ($10,000 to $14,999, $15,000 to $19,999,...$200,000+)
household_incomes = {}
for values in fips_codes.values():
    household_incomes[values] = []

NUM_HOUSEHOLD_INCOME_VARIABLES = 17
for i in range(2, NUM_HOUSEHOLD_INCOME_VARIABLES + 1):
    # B19001_00 + i + E is a range of income variables in the acs5
    FINAL_URL = BASE_URL \
        + GET + ('B19001_00' if i < 10 else 'B19001_0') + str(i) + 'E' \
        + FOR + COUNTY + "*" \
        + IN + STATE + OREGON

    r = requests.get(url=FINAL_URL + API_KEY)
    values = r.json()
    # get number of individuals in ith bracket and match with respective key
    for i in range(1, len(values)):
        # add to household_income the value which matches the fips value which matches the key in fips_codes
        # household_incomes[fips_codes[values[i][2]]].append(int(values[i][0]))
        # fips_codes[047] = Marion
        # int(values[1][0]) = 5690
        # household_incomes[Marion].append(int(5690)
        # household_incom = {Marion: [5690]}
        household_incomes[fips_codes[values[i][2]]].append(int(values[i][0]))

trends = {}
for values in fips_codes.values():
    trends[values] = []
# ==========TRENDS IN RENT AND SEVERE BURDENING FROM 2011 to 2018==========================================
for i in range(2011,2019):
    FINAL_URL =  URL + str(i) + '/' + DATA_SET\
    + GET + TOTAL_POPULATION_BURDENED + COMMA + GROSS_RENT_PERCENT_INCOME_50_PLUS + COMMA\
    + GROSS_RENT_PERCENT_INCOME_30_34 + COMMA + GROSS_RENT_PERCENT_INCOME_35_39 + COMMA + GROSS_RENT_PERCENT_INCOME_40_49\
    + COMMA + MED_GROSS_RENT_DOLLARS\
    + FOR + COUNTY + "*" \
    + IN + STATE + OREGON

    r = requests.get(url=FINAL_URL + API_KEY)
    values = r.json()
    for i in range(1, len(values)):
        trends[fips_codes[values[i][7]]].append(100 * (int(values[i][1])/int(values[i][0])))
        trends[fips_codes[values[i][7]]].append(100 * ((int(values[i][2])) + (int(values[i][3])) + (int(values[i][4])))/int(values[i][0]))
        trends[fips_codes[values[i][7]]].append(int(values[i][5]))

print(trends)

# print(household_incomes)
# ============make new dicts with key as county name instead of fips=====================
population = {}
severe_burden_total = {}
rent_burden_total = {}

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
# ===============new dicts with rent burden/pop as percent=============================
for key in population:
    if key in rent_burden_total:
        # x100 to shift decimal into percent
        severe_rent_burdened_by_pop[key] = 100 * \
            (severe_burden_total[key] / population[key])
        rent_burdened_by_pop[key] = 100 * \
            (rent_burden_total[key] / population[key])

# print("severe rent burdened: ")
# print(severe_rent_burdened_by_pop)
# print("")
# print("rent burdened:")
# print(rent_burdened_by_pop)


# ===========================XLS STUFF=====================================================
workbook = xlsxwriter.Workbook('data.xlsx')
worksheet = workbook.add_worksheet('rent_burdening')
row = 0
col = 0
col_names = ['county', 'population', 'population rent burdened',
             'population severly rent burdened']
for i in col_names:
    worksheet.write(row, col, i)
    col += 1
row = 1
col = 0
# there's probably a really slick way to  do this with a lambda
# but I'm tired and this works
for i in population:
    worksheet.write(row, col, i)
    col += 1
    worksheet.write(row, col, population[i])
    col += 1
    worksheet.write(row, col, rent_burdened_by_pop[i])
    col += 1
    worksheet.write(row, col, severe_rent_burdened_by_pop[i])
    row += 1
    col = 0


income_brackets = [
"Less than $10,000",
"$10,000 to $14,999",
"$15,000 to $19,999",
"$20,000 to $24,999",
"$25,000 to $29,999",
"$30,000 to $34,999",
"$35,000 to $39,999",
"$40,000 to $44,999",
"$45,000 to $49,999",
"$50,000 to $59,999",
"$60,000 to $74,999",
"$75,000 to $99,999",
"$100,000 to $124,999",
"$125,000 to $149,999",
"$150,000 to $199,999",
"$200,000 or more"
]

# new sheet
worksheet = workbook.add_worksheet('household incomes')
row = 0
col = 0
# write header to sheet
worksheet.write(row, col, 'county')
for i in income_brackets:
    col += 1
    worksheet.write(row, col, i)

# write incomes per county by brackets to sheet
row = 1
col = 0
for key in household_incomes:
    worksheet.write(row,col,key)
    for i in household_incomes[key]:
        col += 1
        worksheet.write(row,col,i)
    col = 0
    row += 1
workbook.close()
