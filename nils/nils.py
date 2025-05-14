import geopandas
import shapely

df = geopandas.read_file('geometri.geojson')
df = df.to_crs(epsg=25832)

error_index_list = []

for i, feature in df.iterrows():
    if not feature['geometry'].is_simple:
        error_index_list.append(i)
    elif not feature['geometry'].is_valid:
        error_index_list.append(i)
    else:
        for j, other_feature in df.iterrows():
            if (i < j):
                if feature['geometry'].equals(other_feature['geometry']):
                    error_index_list.append(i)
                    error_index_list.append(j)
                elif feature['geometry'].crosses(other_feature['geometry']):
                    error_index_list.append(i)
                    error_index_list.append(j)

error_index_set = set(error_index_list)

name_list = []
geometry_list = []

for i, feature in df.iterrows():
    if i in error_index_set:
        name_list.append(feature['name'])
        geometry_list.append(feature['geometry'])

new_dict = {'col1': name_list, 'geometry': geometry_list}

new_df = geopandas.GeoDataFrame(new_dict, crs="EPSG:25832")

new_df.to_file('nils.geojson', driver='GeoJSON', )
