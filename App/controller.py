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
 """

import config as cf
import model
import csv
import time
import tracemalloc as tr


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog(est_datos):
    catalog = model.newCatalog(est_datos)
    return catalog

# Funciones para la carga de datos
def loadData(catalog):
    """
    Carga los datos en el catálogo ya inicializado
    """
    #Modificaciones para medir tiempo y espacio
    delta_time = -1.0
    delta_memory = -1.0

    tr.start()
    star_time = getTime()
    start_memory = getMemory()

    loadCategory(catalog)
    loadVideos(catalog)

    stop_time = getTime()
    stop_memory = getMemory()

    delta_time = stop_time - star_time
    delta_memory= deltaMemory(start_memory, stop_memory)
    tr.stop()

    return delta_time, delta_memory

def loadVideos(catalog):
    """
    Carga los diferentes videos a las diferentes estructuras del catálogo
    """
    datos_videos = cf.data_dir + 'videos-20pct.csv'
    input_file = csv.DictReader(open(datos_videos, encoding='utf-8'))
    for video in input_file:
        video['tags'] = (video['tags'].lower()).split('|')
        model.addVideo(catalog,video)
        model.addVideoByCategory(catalog, video)
        model.addVideoByCountry(catalog, video)
        model.addVideoByCat_id(catalog, video)
    return None

def loadCategory(catalog):
    """
    Edita y prepara los datos de las categorias para luego cargarlos en las diferentes estructuras del catálogo
    """
    datos_category = cf.data_dir + 'category-id.csv'
    input_file = csv.DictReader(open(datos_category, encoding='utf-8'), delimiter='\t')
    for category in input_file:
        category['name'] = category['name'].strip(' ')
        model.addCategory(catalog, category)
    return None
    
# Funciones de ordenamiento

def sort_sublist(catalog, numlen, category, country, tag, indicator):
    if indicator == 1:
        cat_id = model.getCategory_id(catalog, category)
    else:
        cat_id = None
    return model.sort_sublist(catalog,numlen,cat_id, country, tag, indicator)

# Funciones de consulta sobre el catálogo

def mostTrendingVideo(catalog, attribute, indicator):
    if indicator == 0:
        result = model.mostTrendingVideo(catalog, attribute, indicator)
    else:
        cat_id = str(model.getCategory_id(catalog, attribute))
        result = model.mostTrendingVideo(catalog, cat_id, indicator)
    return result

# Funciones ppara medir tiempo y memoria

def getTime():
    """
    Devuelvo un tiempo determinado por el procesador
    """
    return float(time.perf_counter()*1000)

def getMemory():
    """
    Devuelve una 'pantallazo' de la memoria usada
    """
    return tr.take_snapshot()

def deltaMemory(star_memory, stop_memory):
    """
    Devuelve la diferencia entre dos magnitudes de memoria tomadas
    en dos diferentes instantes. Las devuelve en KB
    """
    memory_diff = stop_memory.compare_to(star_memory, 'filename')
    delta_memory = 0.0

    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff

    delta_memory /= 1024.0
    return delta_memory
    