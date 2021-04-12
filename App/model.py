"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import time 
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as slc
from DISClib.Algorithms.Sorting import mergesort as mg 
from DISClib.Algorithms.Sorting import quicksort as qc
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog(est_datos):
    """ 
    Inicializa el catálogo que se va a usar para almacenar los datos del CSV
    """
    if est_datos == 1:
        x = 'ARRAY_LIST'
    else:
        x = 'SINGLE_LINKED'
    catalog = {'videos': None,   
               'category': None,
               'VideosByCategory': None,
               'VideosByCountry': None}
    
    catalog['videos'] = lt.newList(x, cmpfunction = cmpVideos)

    catalog['category'] = mp.newMap(32 ,maptype= 'PROBING', loadfactor= 0.5 , comparefunction=cmpVideosByCategory)
    
    catalog['VideosByCategory'] = mp.newMap(44, maptype='PROBING', loadfactor=0.5, comparefunction=cmpVideosByCategory)

    catalog['VideosByCountry'] = mp.newMap(10, maptype= 'PROBING', loadfactor= 0.5, comparefunction= cmpVideosByCountry)
    return catalog

# Funciones para agregar informacion al catalogo
def addVideo(catalog, video):
    lt.addLast(catalog['videos'], video)
    return None

def addCategory(catalog, category):
    """
    Crea un mapa para los indices de cada categoria y además crea un mapa por ids de categoria
    donde en cada entrada guarda un nuevo mapa
    """
    cat = newCategory(category['name'], category['id'])
    nuevo_mapa = mp.newMap(10, maptype='PROBING', loadfactor= 0.5, comparefunction=cmpVideosByCategory)
    mp.put(catalog['category'], cat['cat_name'], cat["cat_id"])
    mp.put(catalog['VideosByCategory'], int(cat['cat_id']), nuevo_mapa)
    return None

def addVideoByCategory(catalog, video):
    """
    Añade el video al mapa de mapas, en el primer mapa busca la categoria del video y dentro de este mapa
    busca el pais para guardar el video en una lista dentro del mapa de paises que está dentro del mapa de categorías
    """
    pais = video['country']
    category_id = int(video['category_id'])
    entry = mp.get(catalog['VideosByCategory'], category_id)
    mapa = me.getValue(entry)

    if mp.contains(mapa, pais):
        entry = mp.get(mapa, pais)
        videos = me.getValue(entry)
        lt.addFirst(videos, video)
        mp.put(mapa, pais, videos)
    else:
        lista = lt.newList('SINGLE_LINKED', cmpfunction=cmpVideosByLikes)
        lt.addFirst(lista, video)
        mp.put(mapa, pais, lista)

    return None

def addVideoByCountry(catalog, video):
    """
    Añada cada video a  la lista guardada en en cada pareja llave valor, es decir, en cada llave (país) se 'guarda' 
    una lista con los videos que tienen como característica común el país.
    """
    country = video['country']
    mapa = catalog['VideosByCountry']
    if mp.contains(mapa, country):
        entry = mp.get(mapa, country)
        videos = me.getValue(entry)
        lt.addFirst(videos, video)
        mp.put(mapa, country, videos)
    else:
        videos = lt.newList('SINGLE_LIKED', cmpfunction= cmpVideos)
        lt.addFirst(videos, video)
        mp.put(mapa, country, videos)
        
    return None
# Funciones para creacion de datos

def newCategory(name, ide):
    category = {'cat_name': name,
                'cat_id': ide}
    return category

# Funciones de consulta
def getFirstVideo(catalog):
    return lt.firstElement(catalog['videos'])
    
def getCategory_id(catalog, category):

    cat_id= mp.get(catalog['category'], category)
    if cat_id:
        return me.getValue(cat_id)
    return None

def get_all_elements(catalog):
    resultado = list()
    for i in lt.iterator(catalog):
        pos = 1
        resultado.append(lt.getElement(catalog, pos))
        pos += 1
    return resultado

def mostTrendingVideo(catalog, attribute, indicator):
    lista_trabajo = lt.newList('SINGLE_LINKED', cmpVideos)

    if indicator == 0:
        key = attribute
        entry = mp.get(catalog['VideosByCountry'], key)
        videos = me.getValue(entry)
        for video in lt.iterator(videos):
            pos = lt.isPresent(lista_trabajo, video)
            if pos == 0:
                lt.addFirst(lista_trabajo, video)
                lt.firstElement(lista_trabajo)['trending_days'] = 1
            else:
                lt.getElement(lista_trabajo, pos)['trending_days'] += 1



    else: 
        for video in lt.iterator(catalog['videos']):
            if lt.isPresent(lista_trabajo, video) != 0:
                pos = lt.isPresent(lista_trabajo, video)
                lt.getElement(lista_trabajo, pos)['trending_days'] += 1

            elif video['category_id'] == attribute:
                lt.addFirst(lista_trabajo, video)
                lt.firstElement(lista_trabajo)['trending_days'] = 1

    sorted_list = mg.sort(lista_trabajo, cmpVideosByTrend)
       
    return  lt.firstElement(sorted_list)

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpVideosByCategory(keyname, category):
    catentry = me.getKey(category)
    if keyname == catentry:
        return 0
    elif keyname > catentry:
        return 1
    else:
        return -1 

def cmpVideosByViews(video_1, video_2):
    if int(video_1['views'])>int(video_2['views']):
        valor = True
    else:
        valor = False
    return valor

def cmpVideos(video_1, video_2):
    if video_1['video_id']>video_2['video_id']:
        return 1
    elif video_1['video_id'] == video_2['video_id']:
        return 0
    else:
        return -1

def cmpVideosByTrend(video_1, video_2):
    if video_1['trending_days'] > video_2['trending_days']:
        valor = True
    else:
        valor = False
    return valor

def cmpVideosByLikes(video_1, video_2):
    if int(video_1['likes']) > int(video_2['likes']):
        valor = True
    else:
        valor = False
    return valor

def cmpVideosByCountry(keyname, pair):
    country = me.getKey(pair)
    if keyname == country:
        return 0
    elif keyname > country:
        return 1
    else:
        return 0

# Funciones de ordenamiento

def sort_sublist(catalog, numlen, category, country, tag, indicator):
    """
    Se usan los índices del doble mapa (categoría y país) para obtener de forma directa los datos que se necesitan ordenar
    """

    lista_trabajo = lt.newList('SINGLE_LINKED')

    if indicator == 1:
        function = cmpVideosByViews
        mapa_categoria = catalog['VideosByCategory']
        entry_1 = mp.get(mapa_categoria, int(category))
        mapa_pais = me.getValue(entry_1)
        entry_2 = mp.get(mapa_pais, country)
        lista_trabajo = me.getValue(entry_2)
    
    else:
        function = cmpVideosByLikes
        for i in lt.iterator(catalog['videos']):
            if i['country'] == country and (tag in i['tags']):
                lt.addFirst(lista_trabajo, i)


    sorted_list = mg.sort(lista_trabajo, function)
    try:
        resultado = lt.subList(sorted_list,1,numlen)
    except:
        resultado = 'No existen tantos videos, intente con un número más pequeño...'
    return resultado
## Final