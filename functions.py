from variables import *
from urls import *
import requests
import xlsxwriter

def get_severe_rent_burden():
  severe_burden = {}
  values = requests.get(url=SEVERE_RENT_ALL_COUNTIES + API_KEY).json()

  for i in range(1, len(values)):
    severe_burden[values[i][2]] = int(values[i][0])

  return severe_burden


def get_sum_severe_rent_burden():
  sum_rent_burden = {}
  values = requests.get(url=SUM_SEVERE_RENT_BURDEN + API_KEY).json()

  for i in range(1, len(values)):
    sum_rent_burden[values[i][4]] = int(
      values[i][0]) + int(values[i][1]) + int(values[i][2])
  
  return sum_rent_burden


def get_sum_burden_in_oregon():
  county_population_burdened = {}
  values = requests.get(url=TOTAL_POPULATION_BURDENED_OREGON + API_KEY).json()

  for i in range(1, len(values)):
    county_population_burdened[values[i][2]] = int(values[i][0])
  
  return county_population_burdened

def get_household_incomes():
  household_incomes = {}
  for values in COUNTY_CODES.values():
    household_incomes[values] = []

  NUM_HOUSEHOLD_INCOME_VARIABLES = 17
  
  for i in range(2, NUM_HOUSEHOLD_INCOME_VARIABLES + 1):
    # B19001_00 + i + E is a range of income variables in the acs5
    FINAL_URL = BASE_URL \
        + GET + ('B19001_00' if i < 10 else 'B19001_0') + str(i) + 'E' \
        + FOR + COUNTY + "*" \
        + IN + STATE + OREGON

    values = requests.get(url=FINAL_URL + API_KEY).json()

    # get number of individuals in ith bracket and match with respective key
    for i in range(1, len(values)):
        household_incomes[COUNTY_CODES[values[i][2]]].append(int(values[i][0]))

  return household_incomes


def get_rent_burden_trends():
  trends = {
    "Crook": [],
    "Deschutes": [], 
    "Jefferson":[]
  }

    
# ==========TRENDS IN RENT AND SEVERE BURDENING FROM 2011 to 2018==========================================
  for i in range(2011,2019):
    FINAL_URL =  URL + str(i) + '/' + DATA_SET\
    + GET + TOTAL_POPULATION_BURDENED + COMMA + GROSS_RENT_PERCENT_INCOME_50_PLUS + COMMA\
    + GROSS_RENT_PERCENT_INCOME_30_34 + COMMA + GROSS_RENT_PERCENT_INCOME_35_39 + COMMA + GROSS_RENT_PERCENT_INCOME_40_49\
    + COMMA + MED_GROSS_RENT\
    + FOR + COUNTY + CROOK + COMMA + DESCHUTES + COMMA + JEFFERSON \
    + IN + STATE + OREGON

    values = requests.get(url=FINAL_URL + API_KEY).json()

    for i in range(1, len(values)):
      severe = round(100 * (int(values[i][1])/int(values[i][0])), 2)
      non_severe = round(100 * ((int(values[i][2])) + (int(values[i][3])) + (int(values[i][4])))/int(values[i][0]), 2)

      trends[COUNTY_CODES[values[i][7]]].append(severe)
      trends[COUNTY_CODES[values[i][7]]].append(non_severe)
      trends[COUNTY_CODES[values[i][7]]].append(int(values[i][5]))

  return trends

def create_rent_burdening(workbook, population, rent_burdened_by_pop, severe_rent_burdened_by_pop):
  
  worksheet = workbook.add_worksheet('rent_burdening')
  row = 0
  col = 0
  col_names = ['county', 'population', '"%"rent burdened','"%" severely rent burdened']

  worksheet.set_column(0,1,10)
  worksheet.set_column(2,2,15)
  worksheet.set_column(3,3,24)
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
    worksheet.write(row, col, round(rent_burdened_by_pop[i], 2))
    col += 1
    worksheet.write(row, col, round(severe_rent_burdened_by_pop[i], 2))
    row += 1
    col = 0

def create_household_incomes(workbook, household_incomes):
  worksheet = workbook.add_worksheet('household incomes')
  row = 0
  col = 0
  # write header to sheet
  worksheet.write(row, col, 'county')
  worksheet.set_column(0,len(income_brackets),15)
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

def create_historical_data(workbook,trends):
  worksheet = workbook.add_worksheet('historic data')
  row = 0
  col = 0
  columns = ['county',"Year", '"%"severe rent burdening', '"%"rent burdening', 'median gross income']

  worksheet.set_column(0,1,10)
  worksheet.set_column(2,5,22)
  # write header to sheet
  for i in columns:
    worksheet.write(row, col, i)
    col += 1

  # write counties and years (2011 - 2018) to xls
  row = 1
  county_col = 0
  year_col = 1
  start_year = 2011
  end_year = 2018
  for key in trends:
    for i in range(start_year, end_year + 1):
        worksheet.write(row,county_col, key )
        worksheet.write(row, year_col, str(i))
        row += 1

  row = 1
  col = 2
  # this goes through the sheet and adds count+year then three data columns (severe, burdened, median gross income)
  # then it drops a row and starts the process over starting at column 0
  for key in trends:
    for i in trends[key]:
        if (col > 4):
            col = 2
            row += 1
        worksheet.write(row, col, i)
        col += 1
