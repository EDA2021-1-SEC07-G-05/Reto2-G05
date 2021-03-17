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


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog(est_datos):
    catalog = model.newCatalog(est_datos)
    return catalog

# Funciones para la carga de datos
def loadData(catalog):
    loadVideos(catalog)
    loadCategory(catalog)
    return None

def loadVideos(catalog):
    datos_videos = cf.data_dir + 'videos-5pct.csv'
    input_file = csv.DictReader(open(datos_videos, encoding='utf-8'))
    for video in input_file:
        model.addVideo(catalog,video)
    return None

def loadCategory(catalog):
    datos_category = cf.data_dir + 'category-id.csv'
    input_file = csv.DictReader(open(datos_category, encoding='utf-8'), delimiter='\t')
    for category in input_file:
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
def getFirstVideo(catalog):
    video_dict = model.getFirstVideo(catalog)
    return video_dict

def get_all_elements(catalog):
    return model.get_all_elements(catalog)

def mostTrendingVideo(catalog, attribute, indicator):
    if indicator == 0:
        result = model.mostTrendingVideo(catalog, attribute, indicator)
    else:
        cat_id = str(model.getCategory_id(catalog, attribute))
        result = model.mostTrendingVideo(catalog, cat_id, indicator)
    return result
