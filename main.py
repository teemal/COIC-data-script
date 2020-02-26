import requests
import config
import xlsxwriter

from variables import *
from urls import *
from functions import *

# one of many query strings. Below is an example of the string directly below it
# FINAL_URL = https://api.census.gov/data/2018/acs/acs5?get=B25070_010E&for=county:*&in=state:41
# this string will get the population of individuals that pay 50% or more of their income
# in rent for all counties in oregon.
# It returns a list of lists. The first list containing meta data and the following lists containing the requested info.
# i.e. one list being ['5690', '41', '047'], meaning 5690 people spend 50% or more of their income in the county 047 (FIPS code for Marion county) in the state 41 (FIPS code for Oregon)


# ==========get population of severe rent burdening by county============================
severe_burden_population = get_severe_rent_burden()

# ==========get sum population of rent burdening by county==================================
sum_severe_burden = get_sum_severe_rent_burden()

# get total population rent burdened in oregon counties
county_population_burdened = get_sum_burden_in_oregon()

# ========HOUSEHOLD  INCOME FOR  ALL BRACKETS IN ALL COUNTIES=================================
# household_income is a dict of lists to store all income brackets ($10,000 to $14,999, $15,000 to $19,999,...$200,000+)
household_incomes = get_household_incomes()

# ==========TRENDS IN RENT AND SEVERE BURDENING FROM 2011 to 2018==========================================
trends = get_rent_burden_trends()

# ============make new dicts with key as county name instead of fips=====================
population = {}
severe_burden_total = {}
rent_burden_total = {}

for key in COUNTY_CODES:
    if key in county_population_burdened:
        population[COUNTY_CODES[key]] = county_population_burdened[key]
        severe_burden_total[COUNTY_CODES[key]] = severe_burden_population[key]
        rent_burden_total[COUNTY_CODES[key]] = sum_severe_burden[key]


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


# ===========================XLS STUFF=====================================================
workbook = xlsxwriter.Workbook('data2.xlsx')

create_rent_burdening(workbook, population, rent_burdened_by_pop, severe_rent_burdened_by_pop)

create_household_incomes(workbook, household_incomes)

create_historical_data(workbook,trends)

workbook.close()
print("done")
