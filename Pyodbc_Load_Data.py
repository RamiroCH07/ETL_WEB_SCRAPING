import pyodbc
import pandas as pd
import sys

server = 'LAPTOP-961OQG8P\SQLEXPRESS'
db = 'PRUEBAS'
admin = 'admin'
pswd = '123456'
try:
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+db+';ENCRYPT=no;UID='+admin+';PWD='+ pswd)
    print("Conexion exitosa")
except Exception as ex:
    print(ex)

#%% Objeto cursor
cursor = cnxn.cursor()
#%% Interactuamos con el motor de base de datos y agregamos datos a cierta tabla
#Creamos la tabla en la base de datos
cursor.execute("""
DROP TABLE IF EXISTS Max_Potencia;
CREATE TABLE Max_Potencia (
    UnidadId INT NOT NULL IDENTITY(1,1) PRIMARY KEY,
    Empresa varchar(255),
    Central varchar(255),
    Unidad varchar(255),
    MW float,
    Fecha smalldatetime
    );
               """)
cursor.commit()              
#%%
# Insertamos valores a la base de datos
df = pd.read_csv("Tabular_Data/Final_Data.csv",encoding='latin1',sep = ";")

#Leemos los datos y los pasamos a la base de datos
tam = df.shape[0]
for i in range(tam):
    empresa = df.Empresa[i]
    central = df.Central[i]
    unidad = df.Unidad[i]
    mw = df.MW[i]
    #Cambiar formato fecha a smalldatetime
    fecha_hora = df.Fecha_Hora[i]
    fecha_hora = fecha_hora.split(sep = "/")
    f_h = fecha_hora[0]+fecha_hora[1]+fecha_hora[2]
    cursor.execute("""
    INSERT INTO Max_Potencia (Empresa,Central,Unidad,MW,Fecha)
     VALUES ("""+"'"+empresa+"','"+central+"','"+
             unidad+"','"+str(mw)+"','"+f_h+"'"+""");
                   """)
    cnxn.commit()
                         
#%%
cnxn.close()
sys.modules[__name__].__dict__.clear()