""" Properati Metadata
This script reads the estates description and generate new features 
Also splits the full location into places

Copyright (C) 2017  Ramiro Savoie ramiro.savoie@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import numpy as np
import pandas as pd
import csv

# TODO Arreglar el nombre del Datasets
df = pd.read_csv('data/properatti.csv')

# Pasamos todos los datos a minusculas pra facilitar la comparacion.
df['description'] = df['description'].transform(lambda x: str(x).lower())

def extract_ambients(description):
    "Extrae la cantidad de ambientes de la descripción"

    print("\nReading description:", description[:200])
    # Mapping entre números como dígitos y como palabras.
    numbers_as_strings = {
        'un': 1,
        'dos': 2,
        'tres': 3,
        'cuatro': 4,
        'cinco': 5,
        'seis': 6
    }
  
    # Con esta regex extraemos los ambientes contemplando los casos de texto y de números.
    result = pd.Series([description]).str.extract("(\d|un|dos|tres|cuatro|cinco|seis)(\s+)(amb)",expand=False)
    # Retorna un Dataframe con el resultado de la extracción, lo obtenemos con sus indices.
    matched_value = result[0][0]
    
    ambients = 'NA'
    try:
        # No encontramos la cantidad de ambientes en la descripción
        if np.isnan(result[0][0]):
            ambients = 'NA'
    except TypeError:
        try:
            # Lo encontramos, intentamos parsearlo como entero.
            ambients = int(matched_value)
        # Lo encontramos como string, lo mapeamos con un diccionario.
        except ValueError:
            ambients = numbers_as_strings[matched_value]

    print("Ambients:", ambients)        
    return ambients        

def extract_ammenities(description):
    "Extrae los ammenities de la descripción"

    print("\nReading description:", description[:200])

    ammenities_to_extract = ['lavadero', 'pileta_piscina', 'terraza','nuevo', 'refaccionado', 'AC', 'living_comedor', 'cocina_comedor', 'cocina_integrada', 'parrilla','balcon', 'subte', 'cochera_fija', 'baulera']

    lavadero = (0, 1)['lavadero' in description] # reemplaza el if else statement 
    pileta_piscina = (0, 1)['pileta' in description or 'piscina' in description ]
    terraza = (0, 1)['terraza' in description]
    nuevo = (0, 1)['nuevo' in description]
    refaccionado = (0, 1)['refaccionado' in description]
    AC = (0, 1)['aire acondicionado' in description or 'AC' in description or 'AA' in description ]
    living_comedor = (0, 1)['living comedor' in description ]
    cocina_comedor = (0, 1)['cocina comedor' in description ]
    cocina_integrada = (0, 1)['cocina integrada' in description ]
    parrilla = (0, 1)['parrilla' in description ]
    balcon = (0, 1)['balcã³n' in description or 'balcon' in description ]
    subte =(0, 1)['subte' in description or 'metro' in description ]
    cochera_fija = (0, 1)['cochera fija' in description or 'cochera' in description ]
    baulera = (0, 1)['baulera' in description ]

    extracted_ammenities = pd.Series([lavadero,pileta_piscina, terraza,nuevo, refaccionado, AC, living_comedor, cocina_comedor, cocina_integrada, parrilla,balcon, subte, cochera_fija, baulera])
    print("Extracted ammenities:", list(zip(ammenities_to_extract, extracted_ammenities)))
    return extracted_ammenities

def split_place_with_parent_names(place_with_parent_names):

    print("\nReading place_with_parent_names:", place_with_parent_names)

    splitted_location = place_with_parent_names.split('|')
    padding_left = splitted_location[0]
    country_name_extracted = splitted_location[1]
    state_name_extracted = splitted_location[2]
    place_name_extracted = splitted_location[3]

    print("Extracted place_name:", country_name_extracted, state_name_extracted, place_name_extracted)

    return pd.Series([country_name_extracted, state_name_extracted, place_name_extracted])

# Main execution

# We reduce the dataframe for testing
df = df.iloc[:10]

# We create a Dataframe for the output with the same Index
output_dataframe = pd.DataFrame(index=df.index)
output_dataframe['ambients'] = df['description'].apply(extract_ambients)

ammenities_columns = ['lavadero','pileta_piscina', 'terraza','nuevo', 'refaccionado', 'AC', 'living_comedor', 'cocina_comedor', 'cocina_integrada','parrilla','balcon','subte','cochera fija','baulera']
output_dataframe[ammenities_columns] = df['description'].apply(extract_ammenities)

place_columns = ['country_name_extracted', 'state_name_extracted', 'place_name_extracted']
output_dataframe[place_columns] = df['place_with_parent_names'].apply(split_place_with_parent_names)

print("\nOutput dataframe:")
output_dataframe.info()

print("\nWriten dataframe in data/properati-metadata.csv")
output_dataframe.to_csv('data/properati-metadata.csv')