from collections import namedtuple
import os, jinja2
import pandas as pd

datafrombd = pd.read_csv('./data_from_bd.csv').replace(float("nan"), None)
df2 = pd.read_csv('./countries.csv').replace(float("nan"), None)
dataset = df2.reset_index()
datasetfrombd = datafrombd.reset_index()

# print(datasetfrombd)

def addZero(num):
    if len(num)==1:
        return str("00"+num)
    elif len(num)==2:
        return str("0"+num)
    else:
        return num

lista_final = []
for i, item in datafrombd.iterrows():
    # print(datafrombd.loc[i, 'pais'])
    # print(item['pais'])
    # print('------------')
    for i2, item2 in dataset.iterrows():
        pais1 = item2['es']
        pais2 = item['pais']
        if item2['es']==item['pais']:
            # print("FOUND - " + item2['es'] +' - '+ item['pais'])
            lista_final.append({
                'codigo_nacimiento': item['codigo_nacimiento']
                , 'iso_3166_1': addZero(str(item2['id']))
            })

lista_final.append({
    'codigo_nacimiento': 'TAI'
    , 'iso_3166_1': '158'
})
lista_final.append({
    'codigo_nacimiento': 'KOR'
    , 'iso_3166_1': '410'
})
lista_final.append({
    'codigo_nacimiento': 'ING'
    , 'iso_3166_1': '826'
})
lista_final.append({
    'codigo_nacimiento': 'OTR'
    , 'iso_3166_1': None
})
# print(lista_final)
# print(len(lista_final))

# To template
templateLoader = jinja2.FileSystemLoader( searchpath="/" )
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = f"{os.path.abspath(os.getcwd())}/super_update.sql.tmp"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render({'lista_final':lista_final})
text_file = open(f"{os.path.abspath(os.getcwd())}/super_update.sql", "w")
n = text_file.write(outputText)
text_file.close()