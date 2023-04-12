from bs4 import BeautifulSoup as bs
import pandas as pd
import codecs
import sys
#Lectura de cada archivo 

meses = ["01","02","03","04","05","06","07","08","09","10","11","12"]
años = ["2018"]
df = pd.DataFrame(columns = ["Empresa","Central","Unidad","MW","Fecha","Hora"])
pos = 0
#%%
for año in años:
    for mes in meses:
        f = codecs.open("htmls/html"+mes+"_"+año+".html", 'r',encoding='utf-8')
        html = f.read()
        f.close()
        #Usamos BS 
        soup = bs(html,'html.parser')
        # Identificamos el div que contiene la tabla que queremos extraer 
        main_div = soup.find('div',class_='dataTables_scroll')
        # Identificamos la fecha que ocurrió la máxima potencia
        fecha = soup.find(id = "reporteMaxDemanda").find_all('td')[0].get_text()
        # Identificamos la hora que ocurrió la máxima potencia
        hora = soup.find(id = "reporteMaxDemanda").find_all('td')[1].get_text()
        #%% Extraemos los datos
        rows = main_div.find_all('tr')
        for row in rows[2:]:
            lrow = []
            for data in row:
                if data.get_text() != '\n':
                    lrow.append(data.get_text().strip())
            lrow.append(fecha)
            lrow.append(hora)
            df.loc[pos] = lrow
            pos = pos + 1
#%% TRANSFORMACIÓN DE LOS DATOS
def cambiar_formato(fech):
    fech_split = fech.split("/")
    return fech_split[2]+"/"+fech_split[1]+"/"+fech_split[0]

def con_to_float(num):
    num = num.replace(",",".")
    return(float(num))

df["Fecha"] = df["Fecha"].apply(cambiar_formato)    
df["MW"] = df["MW"].apply(con_to_float) #Le quitamos la coma a los datos

df["Fecha_Hora"] = df["Fecha"] + " " + df["Hora"]

df.drop(['Fecha','Hora'],axis = 1,inplace = True)
            #%%
df.to_csv("Tabular_Data/Final_Data.csv",index = False,sep = ";")
#%%
sys.modules[__name__].__dict__.clear()