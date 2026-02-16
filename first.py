import marimo

__generated_with = "0.19.7"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Módulo 1: Extracción de datos

    ## -- Shapefiles --

    ### Objetivo

    - Entender qué contiene un SHP así como conceptos básicos de estos archivos.
      - Aprender la importancia de los CRS y cómo ésto nos puede ayudar a cuadrar mapas.
    - Visualizar mapas a partir de una serie de puntos, líneas y polígonos.
    - Graficar características del AMG (Área Metropolitana de Guadalajara).

    ### Actividades

    #### Actividad de clase

    - A partir de los archivos provistos de tren ligero del AMG y caminos, dibuje las líneas del tren así como el de los caminos del estado (gráficos separados).

    #### Actividad de tarea

    - Tome el archivo de colonias, lea y grafique coloreando por municipio.
      - El object type es `colonias`, estos files no tienen subcarpetas como los del tren.
    - Sobre el archivo de colonias agregue lo ya hecho de líneas del tren ligero.
      - El objetivo de este punto es replicar la gráfica que ya existe de estaciones con nombres MÁS el plot de colonias.
      - Para que te sea más fácil pregúntate, ¿necesitas modificar algo del `for` para que esto funcione? Solo ten cuidado con que todo tenga el mismo `CRS` (El `CRS` indicado a utilizar es el `"EPSG:4326"`)
      - Recuerda que para modificar el `CRS` de algo que ya sea un mapa (o sea que ya cuente con un `CRS`) debes usar el `to_crs`.

    Una excelente referencia: https://www.earthdatascience.org/workshops/gis-open-source-python/intro-vector-data-python/
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Los archivos shapefile albergan vectores de información geoespacial generalmente utilizado en GIS (Geographic Information System).

    ## Tipos de información

    - Puntos: Coordenadas x,y.
    - Líneas: Conexiones de 2+ puntos.
    - Polígonos: 3+ puntos que se conectan **y se cierran**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Estructura

    - `.shp`: Contiene geometría para todos los features.
    - `.shx`: Contiene los índices para toda la geometría.
    - `.dbf`: Guarda metadatos en forma tabular.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Metadata espacial

    Los metadatos son _los datos de los datos_. Si yo descargo un archivo .csv, el peso del archivo es un metadato.

    - `CRS`: Proyección de la data. Coordinate Reference System. Nos ayuda a proyectar una serie de coordenadas de manera que tengan sentido en un mapa. Ver: https://geopandas.org/projections.html
    - `Extent`: Espacio geográfico que cubre todos los objetos dentro del archivo shapefile.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Creando puntos, líneas y polígonos

    Importante antes contar con la paquetería `shapely`, `geopandas` y `descartes` instaladas.
    """)
    return


@app.cell
def _():
    # Importamos los 3 objetos básicos
    from shapely.geometry import Point, Polygon, LineString
    return LineString, Point, Polygon


@app.cell
def _(Point):
    # Definiendo un punto
    _point1 = Point(0, 1)
    _point1
    return


@app.cell
def _(LineString):
    # Definiendo una línea
    _point1 = [0, 1]
    _point2 = [2, 3]
    linea = LineString([_point1, _point2])
    # Línea
    linea
    return


@app.cell
def _(Polygon):
    # Definiendo un polígono
    _point1 = [0, 0]
    _point2 = [1, 0]
    point3 = [1, 1]
    puntos_juntos = [_point1, _point2, point3]
    poligono = Polygon(puntos_juntos)
    poligono
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Leyendo shapefiles (.shp)

    ### Actividad de clase:

    - A partir de los archivos provistos de tren ligero del AMG y caminos, dibuje las líneas del tren así como el de los caminos del estado (gráficos separados).
    """)
    return


@app.cell
def _():
    import os
    import geopandas as gpd
    import pandas as pd
    import matplotlib.pyplot as plt

    plt.style.use('ggplot')
    # '%matplotlib inline' command supported automatically in marimo
    return gpd, os, plt


@app.cell
def _():
    # supdir =  Reemplaza con el directorio donde vayas a trabajar. Aquí debe de estar un subdirectorio llamado "tren-ligero"
    supdir = '.'
    return (supdir,)


@app.cell
def _(gpd, os, supdir):
    basedir = os.path.join(supdir, 'tren-ligero','tren_ligero-gdl')
    directorio = os.path.join(basedir, 'lineas', 'c_tren_l1.shp')


    mi_sh = gpd.read_file(directorio)
    mi_sh.head()
    return (basedir,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Dada la forma en la que tenemos organizada la información (carpetas), crearemos una función para leer. El ejemplo es de las líneas del tren ligero.
    """)
    return


@app.cell
def _(gpd, os):
    def get_shp_files(basedir, object_type, file_type='.shp'):
        """ Lectura de archivos SHP anidados

        Este método nos permitirá leer archivos SHP que se encuetran en subcarpetas.

        Parámetros

        basedir: Directorio base en el cual se encuentran nuestras subcarpetas con archivos shp.
        object_type: Tipo de mapa a leer (las carpetas que descargamos traen muchos tipos dentro).
        file_type: Constante para solo leer archivos .shp
        """
        # Empezamos con el código diciéndonos qué rayos está leyendo
        print(f'--> Initiating with {file_type} file reading over {object_type} type of files.')

        # Juntamos el directorio original con el tipo de mapa a leer.
        final_dir = os.path.join(basedir, object_type)

        # Juntando todos los archivos del directorio
        existing_files = os.listdir(final_dir)

        # Variable respuesta, aquí tendremos todos los archivos
        returning_files = {}

        # Recorriendo archivo por archivo
        for existing_file in existing_files:

            # Condicional: ¿El archivo en cuestión es de los que nos interesan?
            if file_type in existing_file:

                # En efecto lo es, quítale la extensión ".shp"
                file_name = existing_file.strip(file_type)

                print(f'--> Found file {file_type}: {file_name}.')

                # Nuevo path: El específico para el archivo shp
                path_to_specific_file = os.path.join(final_dir, existing_file)

                # Leyéndolo con geopandas
                returning_files[file_name] = gpd.read_file(path_to_specific_file)

        # Listo
        print(f'Done with file seek over {object_type}.')
        return returning_files
    return (get_shp_files,)


@app.cell
def _(basedir, get_shp_files):
    # Pongamos a prueba la función.

    lineas = get_shp_files(basedir = basedir, object_type='lineas')
    # estaciones_tren_ligero = get_shp_files(basedir, 'estaciones
    # Leyendo el mapa de líneas del tren ligero


    # Leyendo el mapa de estaciones del tren ligero
    estaciones = get_shp_files(basedir= basedir, object_type= 'estaciones')
    return estaciones, lineas


@app.cell
def _():
    from IPython.display import display
    return (display,)


@app.cell
def _(display, lineas):
    # Veamos qué tenemos
    display(lineas['c_tren_l1'])
    display(lineas['c_tren_l2'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Parece que tenemos un ligero cochinero, pero accedamos al mismo archivo que leímos hace rato:
    """)
    return


@app.cell
def _(estaciones, lineas):
    # Línea 1
    estaciones_l1 = estaciones['c_est_tren_l1']
    linea1 = lineas['c_tren_l1']
    estaciones_l1
    return estaciones_l1, linea1


@app.cell
def _():
    # Línea 2
    return


@app.cell
def _():
    # Ojo con como vienen los metadatos de la línea 3
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Es exactamente lo mismo, solo nos ayudamos de la función para tener todo más organizado.

    Sabemos que tenemos un diccionario de la forma:

    ```
    dict = {nombre_archivo: geopandas con coordenadas}
    ```

    Grafiquemos un solo set usando `geopandas`:
    """)
    return


@app.cell
def _():
    # Viendo como acceder a estaciones

    # ¿Cómo se ven las estaciones?
    return


@app.cell
def _():
    # Graficando estaciones línea 1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notamos que el CRS está raro (el estándar es 4326)
    """)
    return


@app.cell
def _(estaciones_l1, linea1):
    # Setteando CRS a algo típico
    estaciones_l10 = estaciones_l1.to_crs("EPSG:4326")
    linea10 = linea1.to_crs("EPSG:4326")
    estaciones_l10
    return


@app.cell
def _(estaciones_l1, linea1, plt):
    # Ahora sí grafiquemos
    fig, ax = plt.subplots(figsize=(20, 10))

    linea1.plot(color="blue", ax=ax, alpha=0.4)

    nombre_estaciones = estaciones_l1["NOMBRE"].tolist()

    estaciones_l1.plot(
        categorical=True,
        column="NOMBRE",
        categories=nombre_estaciones,
        cmap="Blues",
        edgecolor="black",
        legend_kwds={'bbox_to_anchor': (1.3, 1)},
        legend=True,
        ax=ax
    )

    fig.tight_layout()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ¿Qué tal si de una graficamos todo?
    """)
    return


@app.cell
def _(plt):
    # Definiendo el espacio de graficado
    fig, ax = plt.subplots(figsize=(30, 10))

    # linea1.plot(color="blue", ax=ax, alpha=0.4)

    # Constante para la fuente
    fontsize = 7

    # Diccionario de colores: Uno para cada línea
    colors = {0: 'blue', 1: 'red', 2: 'yellow'}
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Leyendo shapefiles (.shp) : Caminos en el AMG (2012)
    """)
    return


@app.cell
def _():
    # Reciclamos la función, ahora para caminos
    return


@app.cell
def _():
    # Gráfica simple para esta magia
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Actividad autónoma

    - Tome el archivo de colonias, lea y grafique coloreando por municipio.
      - El object type es `colonias`, estos files no tienen subcarpetas como los del tren.
    - Sobre el archivo de colonias agregue lo ya hecho de líneas del tren ligero.
      - El objetivo de este punto es replicar la gráfica que ya existe de estaciones con nombres MÁS el plot de colonias.
      - Para que te sea más fácil pregúntate, ¿necesitas modificar algo del `for` para que esto funcione? Solo ten cuidado con que todo tenga el mismo `CRS` (El `CRS` indicado a utilizar es el `"EPSG:4326"`)
      - Recuerda que para modificar el `CRS` de algo que ya sea un mapa (o sea que ya cuente con un `CRS`) debes usar el `to_crs`.
    """)
    return


if __name__ == "__main__":
    app.run()
