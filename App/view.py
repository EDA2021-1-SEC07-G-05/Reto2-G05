"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
assert cf

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

default_limit = 1000
sys.setrecursionlimit(default_limit*10)

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print('2- n-Videos con más views según categoría')
    print("3- Video con más tendencias según país")
    print("4- Video con más tendencias según categoría")
    print("5- n-Videos con mas likes según país y tag")
    print("0- Salir")


def initCatalog(est_datos):
    return controller.initCatalog(est_datos)

def loadData(catalog):
    controller.loadData(catalog)
    return None

def getFirstVideo(catalog):
    return controller.getFirstVideo(catalog)

def sort_sublist(catalog, numlen, category, country, tag, indicator):
    return controller.sort_sublist(catalog, numlen, category, country, tag, indicator)

def get_all_elements(catalog):
    return controller.get_all_elements(catalog)

def mostTrendingVideo(catalog, attribute, indicator):
    return controller.mostTrendingVideo(catalog, attribute, indicator)

def view_req2(diccionario):
    title = diccionario['title']
    cannel_title = diccionario['channel_title']
    country = diccionario['country']
    days = diccionario['trending_days']
    return title, cannel_title, country, days

def view_req1(diccionario):
    title = diccionario['title']
    cannel_title = diccionario['channel_title']
    publish_time = diccionario['publish_time']
    views = diccionario['views']
    likes = diccionario['likes']
    dislikes = diccionario['dislikes']
    tags = diccionario['tags']
    return title, cannel_title, publish_time, views, likes, dislikes, tags

def primerVideo(diccionario):
    title = diccionario['title']
    cannel_title = diccionario['channel_title']
    trending_date = diccionario['trending_date']
    country = diccionario['country']
    views = diccionario['views']
    likes = diccionario['likes']
    dislikes = diccionario['dislikes']

    return title, cannel_title, trending_date, country, views, likes, dislikes

def view_req3(diccionario):
    title = diccionario['title']
    cannel_title = diccionario['channel_title']
    category_id= diccionario['category_id']
    days = diccionario['trending_days']

    return title, cannel_title, category_id, days 

def view_req4(diccionario):
    title= diccionario['title']
    cannel_title = diccionario['channel_title']
    publish_time = diccionario['publish_time']
    views = diccionario['views']
    likes = diccionario['likes']
    dislikes = diccionario['dislikes']
    tags = diccionario['tags']

    return title, cannel_title, publish_time, views, likes, dislikes, tags

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        est_datos = 1
        print("Cargando información de los archivos ....")
        catalog = initCatalog(est_datos)
        loadData(catalog)
        print('Videos cargados: ' + str(lt.size(catalog['videos'])))
        print('Categorias cargadas: ' + str (mp.size(catalog['category'])))
        
    elif int(inputs[0]) == 2:
        indicator = 1
        numlen = int(input('Digite la cantidad de videos con más likes que desea consultar:\n'))
        category = input('Digite la categoria que desea consultar:\n')
        result = sort_sublist(catalog, numlen, category, None, None, indicator)

        try:
            pos = 1
            for i in lt.iterator(result):
                print(f'Video número {pos}')
                print(view_req1(i))
                print('\n')
                pos += 1
        except:
            print(result)
        
    elif int(inputs[0]) == 3:
        indicator = 0
        country = input('Registre el país sobre el cual desea hacer la consulta:\n')
        print('Estamos trabajando duro para entregarte los resultados, por favor espera unos segundos...')
        result = mostTrendingVideo(catalog, country, indicator)
        print(view_req2(result))
    
    elif int(inputs[0]) == 4: 
        indicator = 1
        category_name = input('Registre la categoría sobre la cual desea hacer la consulta:\n')
        print('Estamos trabajando duro para entregarte los resultados, por favor espera unos segundos...')
        result = mostTrendingVideo(catalog, category_name, indicator)
        print (view_req3(result))
    
    elif int(inputs[0]) == 5:
        indicator = 0
        tag = input('Registre el tag sobre el cual desea hacer la consulta:\n')
        country = input('Registre el país sobre el cual desea hacer la consulta:\n')
        numlen = int(input('Registre la cantidad de videos con más views que desea consultar:\n'))
        print('Estamos trabajando duro para entregarte los resultados, por favor espera unos segundos...')
        result = sort_sublist(catalog, numlen, 'no aplica', country, tag, indicator)
        
        try:
            pos = 1
            for i in lt.iterator(result):
                print(f'Video número {pos}')
                print(view_req4(i))
                print('\n')
                pos += 1
        except:
            print(result)

    else:
        sys.exit(0)
sys.exit(0)