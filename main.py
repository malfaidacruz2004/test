import pandas as pan
import hashlib
import requests
import time
import sqlite3 


def obtener_datos():
    url = "https://restcountries.com/v3.1/all?fields=name,flags,languages"
    response= requests.get(url)
    if response.status_code == 200:
        print("Se obtuvieron los datos deseados")
        return response.json()

    else:
        print("Fallo, no se obtuvieron los datos")
        return None

def encriptarIdioma(idioma):
    lengua = idioma
    idiomaEncrip = hashlib.sha1(lengua.encode('utf-8'))
    return idiomaEncrip.hexdigest()
    

def generarTabla():
    datos= obtener_datos()
    nombre= []
    idiomas= []
    idiomasEncriptados = []
    tiempos= []
    
    for dato in datos:
        inicio = time.perf_counter()
        nombre.append(dato.get('name', {}).get('official'))
        idioma = str(dato.get('languages',{}))
        idioma_Encriptado = encriptarIdioma(idioma)
        idiomas.append(idioma)
        idiomasEncriptados.append(idioma_Encriptado)
        fin = time.perf_counter()
        tiempo= fin-inicio
        tiempos.append(tiempo)



    df= pan.DataFrame((zip(nombre,idiomas,idiomasEncriptados,tiempos)), columns =['Nombre','Idioma', 'Idioma Encriptado','Time'])
    print(df)
    tiempo_Total= df['Time'].sum()
    print('Tiempo total:',tiempo_Total)
    tiempo_Promedio= df['Time'].mean()
    print('Tiempo promedio:',tiempo_Promedio)
    tiempo_Minimo= df['Time'].min()
    print('Tiempo minimo:',tiempo_Minimo)
    tiempo_Maximo= df['Time'].max()
    print('Tiempo maximo:',tiempo_Maximo)

    con = sqlite3.connect('datos.bd')
    df.to_sql('datos',con, if_exists='replace', index=False)
    print('Datos enviados a la Base de datos Sqlite')

    df.to_json('data.json', orient= 'split')
    print('Archivo data.json creado')


if __name__ == "__main__":
    generarTabla()