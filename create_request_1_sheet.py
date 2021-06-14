from pyasn1.type.constraint import WithComponentsConstraint
import requests
import xml.etree.ElementTree as ET

import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe



def create_dataframe(COUNTRY_CODE, API_URL, indicators, rows):
    print(f"Procesando {COUNTRY_CODE}")
    res = requests.get(API_URL)
    #res_string_xml = res.content

    #print(type(res.content))
    root = ET.fromstring(res.content)

    #print(root.tag)
    #print(root.attrib)
    for child in root: #child = fact
        #print(f"tag: {child.tag} | attribute: {child.attrib}")
        row = []
        GHO = child.find('GHO').text if child.find('GHO') is not None else None
        #GHO: nombre de un nodo GHO o fact
        COUNTRY = child.find('COUNTRY').text if child.find('COUNTRY') is not None else None
        SEX = child.find('SEX').text if child.find('SEX') is not None else None
        YEAR = child.find('YEAR').text if child.find('YEAR') is not None else None
        GHECAUSES = child.find('GHECAUSES').text if child.find('GHECAUSES') is not None else None
        AGEGROUP = child.find('AGEGROUP').text  if child.find('AGEGROUP') is not None else None

        DISPLAY = child.find('Display').text if child.find('Display') is not None else None
        DISPLAY = DISPLAY.replace('.', ',') if DISPLAY is not None else None

        NUMERIC = child.find('Numeric').text if child.find('Numeric') is not None else None
        NUMERIC = NUMERIC.replace('.', ',') if NUMERIC is not None else None

        LOW = child.find('Low').text if child.find('Low') is not None else None
        LOW = LOW.replace('.', ',') if LOW is not None else None

        HIGH = child.find('High').text if child.find('High') is not None else None
        HIGH = HIGH.replace('.', ',') if HIGH is not None else None


        if indicators.get(GHO, None) is None:
            indicators[GHO] = len(indicators) + 1
            #input()
            #print(indicators[GHO], GHO)
        indicator_id = indicators[GHO]
        row = [indicator_id, GHO, COUNTRY, SEX, YEAR, GHECAUSES, AGEGROUP, DISPLAY, NUMERIC, LOW, HIGH]
        rows.append(row)
    

    print('-----')





def create_excel_files():
    """Connect spreesheets:"""
    gc = gspread.service_account(filename="client_secret.json")
    sheet = gc.open_by_key('1ld_wPR0HTsN52BWI8C4zVJSvntc7bXTM6oE1GhCbNTo') 

    rows = []
    CODES = ["CHL", "ARG", "BRA", "PER", "COL", "MEX"]
    indicators = {}
    for code in CODES:
        worksheet = sheet.get_worksheet(0)  #hoja numero 0 del excel
        create_dataframe(
            COUNTRY_CODE=code,
            API_URL=f"https://storage.googleapis.com/tarea-4.2021-1.tallerdeintegracion.cl/gho_{code}.xml", 
            indicators=indicators,
            rows=rows)

    df = pd.DataFrame(rows)  # Write in DF
    df.columns = ["indicator_id", "GHO", "COUNTRY", "SEX", "YEAR", "GHECAUSES", "AGEGROUP", "DISPLAY", "NUMERIC", "LOW", "HIGH"]
    print("Escribiendo el spreedsheet")
    set_with_dataframe(worksheet, df)


if __name__ == "__main__":
    create_excel_files()
    