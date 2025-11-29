import io
import base64
from os.path import join
from PIL import Image

import streamlit as st
import folium
from folium.features import GeoJsonTooltip
from folium.plugins import Fullscreen
from folium.raster_layers import ImageOverlay
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.colors as mcolors
from pyproj import Transformer
from shapely.geometry import shape,mapping, Point
from shapely.ops import unary_union
from branca.colormap import LinearColormap, StepColormap

from util.common2 import indicator_title
from content.shared_content import STATS
from content.languages import arabic, english
from content.ipa_content import division_alias, section_alias


# Add a Reset Button as a Folium Marker
def reset_map():
    """Resets the selected polygon state."""
    st.session_state.selected_division = None
    st.rerun()


@st.cache_data(ttl=300)
def read_crop_area_df() -> pd.DataFrame:
    df = pd.read_csv(join("data", "crop_type_precent.csv"))
    return df


def merge_sections_to_divisions(geo, df_divisions, language):
    divisions = df_divisions.division
    new_features = []
    for i, d_id in enumerate(divisions):
        polygons = []
        division_polygons = [
            f for f in geo["features"] if f["properties"]["division"] == d_id
        ]
        division_name = division_polygons[0]["properties"][f"division_{language}"]

        for d_p in division_polygons:
            geom = shape(d_p["geometry"])
            polygons.append(geom)

        new_geometry = mapping(unary_union(polygons))

        # new_geometry = polygons
        new_feature = {
            "type": "Feature",
            "id": i,
            "properties": {
                "division": d_id,
                f"division_{language}": division_name,
            },
            "geometry": {
                "type": new_geometry["type"],
                "coordinates": new_geometry["coordinates"],
            },
        }

        new_features.append(new_feature)

    divisions = dict(
        type="FeatureCollection",
        crs=dict(type="name", properties=dict(name="urn:ogc:def:crs:OGC:1.3:CRS84")),
        features=new_features,
    )
    return divisions


def make_folium_choropleth(geo, indicator, indicator_name, df, col_name, language):
    df = df.round(2)

    # Convert DataFrame to dictionary for mapping
    data_df = df.set_index(col_name)[indicator]

    # Convert DataFrame to dictionary for fast lookup
    data_dict = data_df.to_dict()

    # Add ESRI aerial imagery tile layer
    esri = folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Aerial Imagery",
        overlay=False,
        control=True
    )

    m = folium.Map(
        location=[14.429, 33.01],
        zoom_start=12,
        height=300,
        width="100%",
        tiles=esri,  # Add ESRI arial imagery as default tile layer
    )

    # Add OSM map
    folium.TileLayer("OpenStreetMap", name="OSM", control=True).add_to(m)
    minv = df[indicator].min()
    maxv = df[indicator].max()

    # Define a custom color scale
    colormap = StepColormap(
        ["#ff0000", "#ff4500", "#ff7f50", "#ffb347", "#ffdd44", 
        "#ccff33", "#99ff33", "#66ff33", "#33cc33", "#009933"], 
        vmin=minv, vmax=maxv, caption="colormap"
    )
    # Update geojson for tooltip
    for feature in geo["features"]:
        region_id = feature["properties"].get(col_name)  # Get region ID from GeoJSON
        if region_id in data_dict:  # Check if ID exists in CSV
            feature["properties"][indicator] = data_dict[region_id]
        else:
            feature["properties"][indicator] = None  # Assign None if not found

    if col_name == "section":
        fields = [f"division_{language}", f"section_{language}", indicator]
        aliases = [division_alias[language], section_alias[language], f"{indicator_name}:"]
        geo["ch_name"] = "Gezira Sections"
    else:
        fields = [f"division_{language}", indicator]
        aliases = [division_alias[language], f"{indicator_name}:"]
        geo["ch_name"] = "Gezira Divisions"

    # Add Choropleth layer
    tooltip=folium.GeoJsonTooltip(
            fields=fields,
            aliases=aliases,
            localize=True,
            sticky=False,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 1px solid black;
                border-radius: 3px;
                box-shadow: 3px;
                font-size: 12px;
                font-weight: normal;
                # max-width: 400px; 
                # white-space: normal; 
            """,
            # max_width=200,
            html=True  # Enables HTML in the tooltip
        )

    choropleth = folium.GeoJson(
        geo,
        name=geo["ch_name"],
        tooltip=tooltip,
        style_function=lambda feature: {
            "fillColor": colormap(data_dict[feature["properties"].get(col_name)]),
            "color": "black",
            "weight": 0.5,
            "fillOpacity": 0.7
        },
    ).add_to(m)

    # Add Click event
    click_marker = folium.Marker(
        location=[0, 0],  # Default position (hidden initially)
        popup="Click on the map",
        icon=folium.Icon(color="red")
    )
    m.add_child(click_marker)

    folium.LayerControl().add_to(m)
    folium.plugins.Fullscreen().add_to(m)   
    bounds = choropleth.get_bounds()  # Automatically calculates min/max lat/lon

    # Fit map to bounds
    m.fit_bounds(bounds)
    return m


@st.cache_data(ttl=300)
def create_base_map(center_lat, center_lon, zoom):
    """Create base map with satellite/aerial imagery as default and fullscreen control"""    
    # Add Satellite/Aerial imagery as default base layer
       # Add ESRI aerial imagery tile layer
    esri = folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Aerial Imagery",
        overlay=False,
        control=True
    )#.add_to(m))

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        tiles=esri,
        control_scale=True
    )
    # Add OpenStreetMap as an alternative base layer
    folium.TileLayer("OpenStreetMap", name="OSM", control=True).add_to(m)

    # Add Fullscreen control
    Fullscreen(
        position='topleft',
        title='Fullscreen mode',
        title_cancel='Exit fullscreen mode',
        force_separate_button=True
    ).add_to(m)

    return m




def get_value_at_point(da, lat, lon, variable):
    ts = da.sel(lat=lat, lon=lon, method="nearest")
    ts = ts.to_dataframe().loc[:,variable] 
    return ts



def extraxt_ts(da, locations):
    # Extract time series for each location
    time_series = {}
    for idx, (lat, lon) in enumerate(locations):
        ts = da.sel(lat=lat, lon=lon, method="nearest")  # Nearest neighbor selection
        time_series[f'point_{idx+1}'] = ts.to_pandas()  # Convert to Pandas Series for easy manipulation

    # Convert to a DataFrame for better analysis
    df = pd.DataFrame(time_series).reset_index()
    return df




@st.cache_data
def get_gdf_from_json(geo):
     return gpd.GeoDataFrame.from_features(geo['features'])

def filter_points_within_polygon(points, polygon):
    """Filter points that lie within the given polygon."""
    # Create GeoSeries for points
    points = [Point(lon, lat) for lat, lon in points]
    points_in = [x for x in points if polygon.contains(x).any()]

    return [(lambda point: (point.y, point.x))(point) for point in points_in]

def get_image_from_ds(data, minv, maxv, nodata, colors):
    """Efficient function to get image data for overlay"""

    try:
        data = np.nan_to_num(data, nan=nodata)
        data = np.flip(data, 0).astype(float)

        # Normalize and apply colormap
        norm = mcolors.Normalize(vmin=minv, vmax=maxv)
        cmap = mcolors.LinearSegmentedColormap.from_list("custom", colors, N=100)
        colored_data = cmap(norm(data))

        # Set alpha channel for no-data values
        colored_data[..., 3] = np.where(data == nodata, 0, 0.9)

        # Convert to PIL image and then to base64
        img = Image.fromarray((colored_data * 255).astype(np.uint8))
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return base64.b64encode(img_bytes.getvalue()).decode()

    except Exception as e:
        st.error(f"Error processing data: {str(e)}")

def transform_bounds(bounds, crs):
    """Transform bounds to EPSG:4326."""
    left, bottom, right, top = bounds
    transformer = Transformer.from_crs(crs, "EPSG:4326", always_xy=True)
    return transformer.transform(left, bottom), transformer.transform(right, top)




def create_colormap(data, colors, variable, folium_map):

    """Create and add a colormap legend to the map."""
    colormap = LinearColormap(colors=colors, vmin=data.min(), vmax=data.max())
    colormap.caption = f"{variable} Values"
    colormap.add_to(folium_map)
    return colormap



def add_image_overlay(data, bounds, colors, variable, folium_map):
    """Generate an image overlay for the map."""
    img_base64 = get_image_from_ds(data, data.min(), data.max(), -9999, colors)
    ImageOverlay(
        name=f"{variable.replace('_', ' ')}".title(),
        image=f"data:image/png;base64,{img_base64}",
        bounds=bounds,
        opacity=0.9,
    ).add_to(folium_map)


def add_geojson_layer(geo, folium_map, lang):
    """Add a GeoJSON layer with tooltips to the map."""
    if lang == arabic:
        fields = ["division_a", "section_a"]
        aliases = ["القسم: ", "الجزء: "]
    elif lang == english:
        fields = ["division_e", "section_e"]
        aliases = ["Division: ", "Section: "]
    else:
        raise NotImplementedError(f"This language is not supported yet {lang}")

    geo_layer = folium.GeoJson(
        geo,
        name="irrigation divisions",
        style_function=lambda _: {
            'fillColor': '#00000000', 
            'color': 'black',
            "weight": 0.5,
        },
    ).add_to(folium_map)

    tooltip = GeoJsonTooltip(
        fields=fields,
        aliases=aliases,
        localize=True,
        sticky=False,
        labels=True,
        smooth_factor=0,
        style="""
            background-color: #F0EFEF;
            border: 1px solid black;
            border-radius: 3px;
            box-shadow: 3px;
            font-size: 12px;
            font-weight: normal;
        """,
        max_width=750,
    )
    geo_layer.add_child(tooltip)
    return geo_layer

def add_click_markers(folium_map, clicked_locations):
    """Add markers for clicked locations."""
    for idx, (lat, lon) in enumerate(clicked_locations):
        folium.Marker(
            [lat, lon],
            popup=f"Point {idx + 1}: lat: {lat:.4f}, lon: {lon:.4f}", 
            icon=folium.Icon(color="blue")
        ).add_to(folium_map)

        folium.Marker(
            location=[lat, lon],
            icon=folium.DivIcon(
                icon_size=(50, 50),
                icon_anchor=(3, 17),
                html=f'<div style="font-size: 24ptpx;font-weight: bold; color: white;">{idx + 1}</div>'
            ),
            zIndexOffset=1000
        ).add_to(folium_map)


def create_folium_map(data, geo, bounds, crs, variable, language):
    """Main function to create the folium map."""
    (left, bottom), (right, top) = transform_bounds(bounds, crs)

    folium_map = create_base_map((bottom + top) / 2, (left + right) / 2, 12)

    colors = ['red', 'yellow', 'green']
    create_colormap(data, colors, variable, folium_map)
    add_image_overlay(data, [[bottom, left], [top, right]], colors, variable, folium_map)

    geo_layer = add_geojson_layer(geo, folium_map, language)
    folium_map.fit_bounds(geo_layer.get_bounds())

    click_marker = folium.Marker(
        location=[0, 0],
        popup="Click on the map",
        icon=folium.Icon(color="red")
    )
    folium_map.add_child(click_marker)
    folium_map.add_child(folium.LatLngPopup())

    add_click_markers(folium_map, st.session_state.clicked_locations)

    folium.LayerControl().add_to(folium_map)

    return folium_map
