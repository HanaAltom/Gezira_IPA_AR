import logging
from os.path import join
from json import load
from PIL import Image

import streamlit as st
import pandas as pd
import numpy as np
import xarray as xr
import rasterio
import altair as alt

from content.languages import arabic, english

# Configure the logging settings
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

logger = logging
#######################
# dfm.columns = [x.replace('_', ' ') for x in dfm.columns]
logo_wide = join("data", "logo_wide.png")
logo_small = join("data", "logo_small.png")


def indicator_title(indicator, stat_dict):
    # stat_dict = {'std':'Standard deviation', 'min':'Minimum', 'max':'Maximum', 'mean':'Average', 'median':'Median'}
    lst = indicator.split('_')
    t1 = ' '.join(lst[1:])
    t2 = f"{[k for k, v in stat_dict.items() if v == lst[0]][0]} {t1}" 
    return t1,t2


# @st.cache_data(ttl=300)
def load_image(image_name: str) -> Image.Image:
    """Displays an image.

    Parameters
    ----------
    image_name : str
        Local path of the image.

    Returns
    -------
    Image
        Image to be displayed.
    """
    return Image.open(image_name)


def logos_and_language() -> None:
    img_wide = load_image(logo_wide)
    img_small = load_image(logo_small)

    st.logo(img_wide, size="large", link="https://www.un-ihe.org/", icon_image=img_small)
    arabic_button, english_button = st.columns((1, 1))

    with arabic_button:
        if st.button("العربية"):
            st.session_state.language = arabic
            st.rerun()
    with english_button:
        if st.button("English"):
            st.session_state.language = english
            st.rerun()


# Load data
@st.cache_data(ttl=300)
def read_df_and_geo(selected_crop) -> tuple[pd.DataFrame, dict]:
    dfm = pd.read_csv(join("data", f"Gezira_IPA_statistic_{selected_crop}.csv"))
    with open(join("data", "Gezira_IR.json")) as response:
        geo = load(response)

    return dfm, geo



def format_number(num):
    return f"{num:.2f}"


# Calculation season-over-season difference in metrix
def calculate_indicator_difference(input_df, indicator, input_season):
  selected_season_data = input_df[input_df['season'] == input_season].reset_index()
  previous_season_data = input_df[input_df['season'] == input_season - 1].reset_index()
  selected_season_data['indicator_difference'] = selected_season_data[indicator].sub(previous_season_data[indicator], fill_value=0)
  return pd.concat([selected_season_data['division'], selected_season_data[indicator], selected_season_data.indicator_difference], axis=1).sort_values(by="indicator_difference", ascending=False)


def history_df(df1, df2, idx_col, selected_indicator):
    d2 = df1.pivot(index=idx_col, columns='season', values=selected_indicator).reset_index()
    d3 = df2.groupby(idx_col).agg({selected_indicator:'mean'}).reset_index()
    d4 = d3.merge(d2, on=idx_col, how = 'inner')
    d4[d4.columns[2:]]= d4[d4.columns[2:]].round(2)
    d4['history'] = d4[d4.columns[2:]].values.tolist()
    d4 = d4.drop(columns = d4.columns[2:-1])
    return d4.round(2)


select = alt.selection_point(name="select", on="click")
highlight = alt.selection_point(name="highlight", on="pointerover", empty=False)

stroke_width = (
    alt.when(select).then(alt.value(2, empty=False))
    .when(highlight).then(alt.value(1))
    .otherwise(alt.value(0))
)



@st.cache_data
def read_dataset(ds_path):
    # chunks = {'season': 1, 'latitude': 2000, 'longitude': 2000}
    # with xr.open_dataset(ds_path, chunks=chunks) as dataset:  
    with xr.open_dataset(ds_path) as dataset:  
        # data = dataset.beneficial_fraction[0].values
        dataset = dataset.transpose('season', 'lat', 'lon')  # change axis order
        transform = dataset.rio.transform()
        crs = dataset.rio.crs
        nodata = -9999 #dataset.nodata
        bd = dataset.rio.bounds()
        bounds = rasterio.coords.BoundingBox(bd[0], bd[1], bd[2], bd[3])

    return dataset, transform, crs, nodata, bounds


@st.cache_data
def _get_stats(_data):
      # Compute spatial statistics
    _data = _data.where(_data>0, np.nan)
    stats = {
        'min': _data.min(dim=['lat', 'lon']),
        'max': _data.max(dim=['lat', 'lon']),
        'mean': _data.mean(dim=['lat', 'lon']),
        'median': _data.median(dim=['lat', 'lon']),
        'std': _data.std(dim=['lat', 'lon']),
        "25_q": _data.quantile(0.25, dim=['lat', 'lon'], method='linear')
                        .drop_vars('quantile'),
        "75_q": _data.quantile(0.75, dim=['lat', 'lon'], method='linear')
                        .drop_vars('quantile'),
    }
    return stats


def get_stats_english(data):
    stats_dict = _get_stats(data)
    stats = {
        'Minimum': stats_dict['min'],
        'Maximum': stats_dict['max'],
        'Mean': stats_dict['mean'],
        'Median': stats_dict['median'],
        'St. deviation': stats_dict['std'],
        "25% quantile": stats_dict['25_q'],
        "75% quantile": stats_dict['75_q'],
    }

    # pd.DataFrame.from_dict(d)
    df_stat = pd.DataFrame.from_dict({k: v.values.item() for k, v in stats.items()}, 
                                    orient='index', columns = ['Values']).round(2)
    df_stat.index.names = ['Stats']
    return df_stat


def get_stats_arabic(data):
    stats_dict = _get_stats(data)
    stats = {
        'الحد لاأدنى': stats_dict['min'],
        'الحد الأقصى': stats_dict['max'],
        'المتوسط': stats_dict['mean'],
        'الوسيط': stats_dict['median'],
        'الانحراف المعياري': stats_dict['std'],
        "25% نقطة تجزيء": stats_dict['25_q'],
        "75% نقطة تجزيء": stats_dict['75_q'],
    }

    # pd.DataFrame.from_dict(d)
    df_stat = pd.DataFrame.from_dict({k: v.values.item() for k, v in stats.items()}, 
                                    orient='index', columns = ['القيمة']).round(2)
    df_stat.index.names = ['الاحصائية']
    return df_stat


# This function is not used
def extract_time_series(da, locations):
    """Function to extract time series in a vectorized way"""
    lats, lons = zip(*locations)
    ts = da.sel(lat=list(lats), lon=list(lons), method="nearest")
    return ts.to_dataframe().reset_index()

