
import pandas as pd
import geopandas as gpd
import shapely
import matplotlib.pyplot as plt
from shapely.geometry import LineString

#https://maps.princeton.edu/catalog/stanford-kk544xm4197 --> shapefile españa
#https://maps.princeton.edu/catalog/stanford-gy612dn2324--> shapefile portugal
#todos los archivos de españa hay que guardarlos es carpeta spain y los de portugal en portugal

#descargar shape de españa, grafico de poligono y frontera
shapefile = gpd.read_file(r"fuentesExternas\spain\kk544xm4197.shp")
spain_polygon = shapefile.unary_union
spain_gdf = gpd.GeoDataFrame(geometry=[spain_polygon])
spain_gdf.plot()
plt.title('Polygon of Spain')
plt.show()
spain_boundary = spain_gdf.boundary
spain_boundary.plot()
plt.title('Boundary of Spain')
plt.show()  
#descargar shape de portugal, grafico de poligono y frontera
shapefile2 = gpd.read_file(r"fuentesExternas\portugal\PRT_adm1.shp")
portugal_polygon = shapefile2.unary_union
portugal_gdf = gpd.GeoDataFrame(geometry=[portugal_polygon])
portugal_gdf.plot()
plt.title('Polygon of portugal')
plt.show()
portugal_boundary = portugal_gdf.boundary
portugal_boundary.plot()
plt.title('Boundary of portugal')
plt.show() 
#juntar los dos y graficos del conjunto 
iberia=pd.concat([spain_gdf,portugal_gdf])
iberia_polygon = iberia.unary_union
iberia_gdf = gpd.GeoDataFrame(geometry=[iberia_polygon])
iberia_gdf.plot()
plt.title('Polygon of iberia')
plt.show()
iberia_boundary = iberia_gdf.boundary
iberia_boundary.plot()
plt.title('Boundary of iberia')
plt.show() 

#creo dos puntos para pruebas, aprox es donde están Madrid y Barcelona
puntoMadrid=shapely.geometry.Point((-3.9,40.2))
puntoBarcelona=shapely.geometry.Point((2.4,41.5))

#distancia de Barcelona a la frontera
print(iberia_boundary.distance(puntoBarcelona))

#accedo a la serie de LineStrings de la frontera
exploded = iberia_boundary.explode()          
 
#creo una lista para quitar la linea de peninsula y dejar solo las islas   
lista=[]
for i in range(0,1040):    
    if i in [935,1027,1028,1029,1030,1031,1032,1033,1034]:
        lista.append(False)
    else:
        lista.append(True)
filtered_lines = exploded[lista]
filtro_gdf = gpd.GeoDataFrame(geometry=filtered_lines)
filtro_gdf.plot()
plt.title('Polygon of filtro')
plt.show()

#de linea de peninsula quito el trozo que es frontera con Francia porque lo que quiero es linea de costa
lista1=[]
lista2=[]
e=exploded.iloc[935]
f=e.coords    
print(f)
#de la linea de iberia, creo dos lineas quitando la frontera con francia
for h,g in enumerate(f):  
    if h<94731:
        lista1.append(g)
    if h>96363:
        lista2.append(g)
#las convierto en LineString
line1 = LineString(lista1)
line2 = LineString(lista2)

# convierto linestrings a geoseries
new_lines = gpd.GeoSeries([line1, line2])

# concateno con las islas
filtered_lines = filtered_lines.append(new_lines)
filtro_gdf = gpd.GeoDataFrame(geometry=filtered_lines)
filtro_gdf.plot()
plt.title('Polygon of costa')
plt.show()      
costa = filtro_gdf.unary_union
costa_gdf = gpd.GeoDataFrame(geometry=[costa])
#esta es la linea de costa que podre usar para medir distancia de un punto en españa a la costa
print(costa_gdf.distance(puntoBarcelona))
print(costa_gdf.distance(puntoMadrid))   

#por si necesito ver la primera coordenada de cada linea
lista=[]
for i in exploded:    
    f=i.coords
    c=f[0]
    lista.append(c)
   
# l=pd.DataFrame(lista)
# l.to_excel("lista.xlsx")




