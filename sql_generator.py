from collections import namedtuple
import os, jinja2
import pandas as pd


df2 = pd.read_csv('./dataset.csv').replace(float("nan"), None)
dataset = df2[:78].reset_index()


def addZero(num):
    if len(num) == 1:
        return str("0"+num)
    return str(num)

def validateNone(field):
    if type(field) == float:
        return addZero(str(int(field))) if field else ''
    return field if field else ''

# Generar el codigo servidor
prefijo = "S"
cuentanro = ""
cnt = ""
lista_codigos = []
for nro in range(len(dataset)):
    cnt = str(nro)
    while len(cnt) < 6:
        cnt = "0" + cnt
        
    cuentanro = prefijo + cuentanro + cnt
    lista_codigos.append(cuentanro)
    cnt = ""
    cuentanro=""

# Armar el diccionario
lista_servers = []
for index, item in dataset.iterrows():
    lista_servers.append({
        'index': index
        , 'codigoservidor': lista_codigos[index]
        , 'servername': validateNone(dataset.loc[index, 'server_name'])
        , 'sshuser': validateNone(dataset.loc[index, 'ssh_user'])
        , 'sshpass': validateNone(dataset.loc[index, 'ssh_pass'])
        , 'sshport': validateNone(dataset.loc[index, 'ssh_port'])
        , 'dbuser': validateNone(dataset.loc[index, 'db_user'])
        , 'dbpass': validateNone(dataset.loc[index, 'db_pass'])
        , 'hisdbname': validateNone(dataset.loc[index, 'his_db_name'])
        , 'hisuser': validateNone(dataset.loc[index, 'his_user'])
        , 'hispass': validateNone(dataset.loc[index, 'his_pass'])
        , 'hisdomainname': str(dataset.loc[index, 'his_domain_name']).split('https://')[1] if dataset.loc[index, 'his_domain_name'] else ''
        , 'codigodepartamento': validateNone(dataset.loc[index, 'codigo_departamento'])
        , 'isambulatoria': dataset.loc[index, 'is_ambulatoria']
        , 'isinternacion': dataset.loc[index, 'is_internacion']
    })

# To template
templateLoader = jinja2.FileSystemLoader( searchpath="/" )
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = f"{os.path.abspath(os.getcwd())}/super_insert.sql.tmp"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render({'lista_servers':lista_servers})
text_file = open(f"{os.path.abspath(os.getcwd())}/super_insert.sql", "w")
n = text_file.write(outputText)
text_file.close()