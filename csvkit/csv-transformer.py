#!/usr/bin/env python

"""
Transforma un fichero .csv en otro intercambiando las columnas en funcion de un mapeo definido en un fichero .json

Forma de uso: python csv-transformer.py . test_translator.json
El primer parametro es un directorio. Todos los ficheros csv de ese directorio se transformaran de acuerdo al mapa de
transformacion expresado en el segundo parametro.
"""

import pandas, json
import sys
import os
import utilities.in2csv as in2csv

if len(sys.argv) <= 2:
    print("No se ha proporcionado ruta de ficheros. Fin de procesamiento.")
    sys.exit(0)

path = sys.argv[1]
output_path = path+"/output"

try:
    os.mkdir(output_path)
except OSError:
    pass
else:
    print("Successfully created the directory %s " % output_path)


def new_index(old):
    return int(transform_dict[str(old)]) if str(old) in transform_dict else old


with open(sys.argv[2]) as json_translator:
    transform_dict = json.load(json_translator)

    for file in os.listdir(path):
        if file.endswith('.xlsx') or file.endswith('.xls'):
            in2csv.launch_new_instance()

        if not file.endswith('.csv'):
            continue

        filename = file.split('.')
        name = filename[0]
        suffix = '.' + filename[1]

        df = pandas.read_csv(os.path.join(path, file), sep=',')
        cols = list(df.columns)
        df = df[[cols[new_index(i)] for i in range(len(cols))]]
        df.to_csv(os.path.join(output_path, name+'_translated'+suffix), sep=';', index=False)
