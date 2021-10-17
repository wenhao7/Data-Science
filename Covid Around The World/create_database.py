# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 14:55:05 2021

@author: wenhao
"""

import psycopg2 as ps
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import Error



"""
# Create database "our_world"
con = ps.connect(user = 'postgres',
                       password = '0000'
                       )

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur = con.cursor()

cur.execute(sql.SQL("CREATE DATABASE {}").format(
    sql.Identifier('our_world')))
"""



"""
# Connect to database
try:
    con = ps.connect(user = 'postgres',
                                  password = '0000',
                                  database = 'our_world'
                                  )
    
    cur = con.cursor()
    
    print("PostgreSQL server information")
    print(con.get_dsn_parameters(), "\n")
    
    

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
    
finally:
    if con:
        cur.close()
        con.close()
        print("PostgreSQL connection is closed")    
 """
   


# Create tables

# Table for Others
con = ps.connect(user = 'postgres',
                 password = '0000',
                 database = 'our_world'
                 )

cur = con.cursor()

try:
    cur.execute("""CREATE TABLE others(
        iso_code text PRIMARY KEY,
    	location text,
    	continent text,
    	population real,
    	population_density real,
    	median_age real,
    	aged_65_older real,
    	aged_70_older real,
    	gdp_per_capita real,
    	extreme_poverty real,
    	cardiovasc_death_rate real,
    	diabetes_prevalence real,
    	female_smokers real,
    	male_smokers real,
    	handwashing_facilities real,
    	hospital_beds_per_thousand real,
    	life_expectancy	real,
        human_development_index real
    )
    """)
    
    with open('others.csv', 'r', encoding='utf-8') as f:
        next(f) # skip header row
        cur.copy_from(f, 'others', sep = ',', null = "")
    
    con.commit()

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
    
    
    
# Table for Cases and Deaths
con = ps.connect(user = 'postgres',
                 password = '0000',
                 database = 'our_world'
                 )

cur = con.cursor()

try:
    cur.execute("""CREATE TABLE cases(
        id integer PRIMARY KEY,
        iso_code text REFERENCES others(iso_code),
        location text,
        date date,
        total_cases real,
        new_cases real,
        new_cases_smoothed real,	
        total_deaths real,
        new_deaths	real,
        new_deaths_smoothed real,	
        total_cases_per_million real,
        new_cases_per_million real,
        new_cases_smoothed_per_million real,
        total_deaths_per_million real,
        new_deaths_per_million real,
        new_deaths_smoothed_per_million real
        )
    """)
    
    cur = con.cursor()
    with open('cases.csv', 'r', encoding='utf-8') as f:
        next(f) # skip header row
        cur.copy_from(f, 'cases', sep = ',', null = "")
    
    con.commit()
    
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)



# Table for Excess Mortality
con = ps.connect(user = 'postgres',
                 password = '0000',
                 database = 'our_world'
                 )

cur = con.cursor()

try:
    cur.execute("""CREATE TABLE excess_mortality(
        id integer PRIMARY KEY REFERENCES cases(id),
        iso_code text REFERENCES others(iso_code),
    	location text,
    	date date,
    	excess_mortality_cumulative_absolute real,
    	excess_mortality_cumulative real,
        excess_mortality real,
    	excess_mortality_cumulative_per_million real
    )
    """)
    
    with open('excess_mortality.csv', 'r', encoding='utf-8') as f:
        next(f) # skip header row
        cur.copy_from(f, 'excess_mortality', sep = ',', null = "")
    
    con.commit()
    
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)



# Table for Hospitalisation
con = ps.connect(user = 'postgres',
                 password = '0000',
                 database = 'our_world'
                 )

cur = con.cursor()

try:
    cur.execute("""CREATE TABLE hospitalisation(
        id integer PRIMARY KEY REFERENCES cases(id),
        iso_code text REFERENCES others(iso_code),
    	location text,
    	date date,
    	icu_patients real,
    	icu_patients_per_million real,
    	hosp_patients real,
    	hosp_patients_per_million real,
    	weekly_icu_admissions real,
    	weekly_icu_admissions_per_million real,
    	weekly_hosp_admissions real,
    	weekly_hosp_admissions_per_million real
    )
    """)
    
    with open('hospitalisation.csv', 'r', encoding='utf-8') as f:
        next(f) # skip header row
        cur.copy_from(f, 'hospitalisation', sep = ',', null = "")
    
    con.commit()
    
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)



# Table for Reproduction Rate
con = ps.connect(user = 'postgres',
                 password = '0000',
                 database = 'our_world'
                 )

cur = con.cursor()

try:
    cur.execute("""CREATE TABLE reproduction(
        id integer PRIMARY KEY REFERENCES cases(id),
        iso_code text REFERENCES others(iso_code),
        location text,
        date date,
        reproduction_rate real
    )
    """)
    
    with open('reproduction.csv', 'r', encoding='utf-8') as f:
        next(f) # skip header row
        cur.copy_from(f, 'reproduction', sep = ',', null = "")
    
    con.commit()

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
    
    

# Table for Stringency
con = ps.connect(user = 'postgres',
                 password = '0000',
                 database = 'our_world'
                 )

cur = con.cursor()

try:
    cur.execute("""CREATE TABLE stringency(
        id integer PRIMARY KEY REFERENCES cases(id),
        iso_code text REFERENCES others(iso_code),
        location text,
        date date,
        stringency_index real
    )
    """)
    
    with open('stringency.csv', 'r', encoding='utf-8') as f:
        next(f) # skip header row
        cur.copy_from(f, 'stringency', sep = ',', null = "")
    
    con.commit()
    
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
    


# Table for Tests
con = ps.connect(user = 'postgres',
                 password = '0000',
                 database = 'our_world'
                 )

cur = con.cursor()

try:
    cur.execute("""CREATE TABLE tests(
        id integer PRIMARY KEY REFERENCES cases(id),
        iso_code text REFERENCES others(iso_code),
    	location text,
    	date date,
    	new_tests real,
    	total_tests real,
    	total_tests_per_thousand real,
    	new_tests_per_thousand real,
    	new_tests_smoothed real, 
    	new_tests_smoothed_per_thousand real,
    	positive_rate real,
    	tests_per_case real,
    	tests_units text
    )
    """)
    
    with open('tests.csv', 'r', encoding='utf-8') as f:
        next(f) # skip header row
        cur.copy_from(f, 'tests', sep = ',', null = "")
    
    con.commit()

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
    


# Table for Vaccinations
con = ps.connect(user = 'postgres',
                 password = '0000',
                 database = 'our_world'
                 )

cur = con.cursor()

try:
    cur.execute("""CREATE TABLE vaccinations(
        id integer PRIMARY KEY REFERENCES cases(id),
        iso_code text REFERENCES others(iso_code),
    	location text,
    	date date,
    	total_vaccinations real,
    	people_vaccinated real,
    	people_fully_vaccinated real,
    	total_boosters real,
    	new_vaccinations real,
    	new_vaccinations_smoothed real,
    	total_vaccinations_per_hundred real,
    	people_vaccinated_per_hundred real,
    	people_fully_vaccinated_per_hundred real,
    	total_boosters_per_hundred real,
    	new_vaccinations_smoothed_per_million real
    )
    """)
    
    with open('vaccinations.csv', 'r', encoding='utf-8') as f:
        next(f) # skip header row
        cur.copy_from(f, 'vaccinations', sep = ',', null = "")
    
    con.commit()

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
    
    


    
    

