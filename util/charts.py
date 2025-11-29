import pandas as pd
import altair as alt
import plotly.express as px

from util.common2 import indicator_title
from content.ipa_content import line_chart_content, area_id_translation
from content.languages import arabic, english
from content.shared_content import STATS


def move_rows_to_top(df, column, value):
    """Reorder DataFrame rows to bring specified column value to the top."""
    df_top = df[df[column] == value]  # Rows with the specified value
    df_rest = df[df[column] != value]  # All other rows
    return pd.concat([df_top, df_rest], ignore_index=True)  # Merge and reset index


def make_alt_chart(df,indicator):
    """histogram plot"""

    ylable, text = indicator_title(indicator, STATS)
    title = alt.TitleParams(f'Yearly {text} by section', anchor='middle')
    barchart = alt.Chart(df, title=title).mark_bar().encode(
        x=alt.X('division:N', axis=None),
        y=alt.Y(f'{indicator}:Q', title=ylable),
        color='division:N',
        column='season:N'
    ).properties(width=80, height=120).configure_legend(
        orient='bottom'
    )
    return barchart


def alt_bar_chart(df, indicator, indicator_name, stat_name, col_name, season, language):
    plot_title = f"{indicator_name.title()} - {stat_name} - {str(season)}"
    area_id = area_id_translation[col_name][language]
    df = df.round(2)
    row_count = len(df)
    pixel_size = 60 - 2* (row_count-5)
    height = row_count * pixel_size  # 30 pixels per row

    select = alt.selection_point(name="select", on="click")
    highlight = alt.selection_point(name="highlight", on="pointerover", empty=False)

    stroke_width = (
        alt.when(select).then(alt.value(2, empty=False))
        .when(highlight).then(alt.value(1))
        .otherwise(alt.value(0))
    )

    chart = alt.Chart(df).mark_bar().encode(
        y=alt.Y(f'{col_name}_{language}:N', sort=alt.EncodingSortField(field="indicator", op="count", order='descending'),title=area_id),  # Rename Y-axis
        x=alt.X(f'{indicator}:Q', title=indicator_name),  # Rename X-axis
        color=alt.Color(f'{indicator}:N', legend=None),  # Remove the legend
        fillOpacity=alt.when(select).then(alt.value(1)).otherwise(alt.value(0.3)),
        strokeWidth=stroke_width,

        tooltip=[
            alt.Tooltip(f'{col_name}_{language}:N', title=area_id),
            alt.Tooltip(f'{indicator}:Q', title=indicator_name, format='.2f'),  # Format Value as decimal with 2 digits
        ],
    ).properties(
        height=height, #title=plot_title
        ).configure_view(
            continuousWidth=600,  # Default width to avoid shrinking
            continuousHeight=300
        ).configure(
            autosize="fit"  # Ensures it resizes correctly
        ).add_params(select, highlight)

    return chart, plot_title


def make_alt_linechart(
    df, indicator, indicator_name, stat_name, unit, col_name, selected_section, language
):
    df["year"] = df["season"].str.split("-").str[1]
    df=df.assign(year= pd.to_datetime(df["year"], format="%Y")).round(2)

    min_value = df[indicator].min()
    max_value = df[indicator].max()
    area_id = area_id_translation[col_name][language]

    plot_title, x_title, y_title = line_chart_content(
        indicator_name, stat_name, area_id, unit, language
    )

    if selected_section is not None:
        df = move_rows_to_top(df, "section", selected_section).iloc[::-1]
    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('year:T', title=x_title, axis=alt.Axis(tickCount="year",
                        labelExpr='(parseInt(timeFormat(datum.value, \'%Y\')) - 1) + "–" + timeFormat(datum.value, \'%Y\')')),  
        y=alt.Y(f'{indicator}:Q',title=y_title, scale=alt.Scale(domain=[min_value, max_value])),
        color=alt.Color(f'{col_name}_{language}:N', title=area_id,  legend=alt.Legend(orient="top")),

        tooltip=[
            alt.Tooltip(f'{col_name}_{language}:N', title=area_id),
            alt.Tooltip('year:T', title=x_title,format='%Y'),
            alt.Tooltip(f'{indicator}:Q', title=indicator, format='.2f'),  # Format Value as decimal with 2 digits
        ]
    ).properties(
        height=300,
        bounds="flush",  # Ensures title does not affect chart size
    ).configure_view(
        continuousWidth=600,  # Default width to avoid shrinking
        continuousHeight=300,
    ).configure(
        autosize="fit",  # Ensures it resizes correctly
    )

    return chart, plot_title


def alt_line_chart(df, indicator, indicator_name, unit):
    # df2=df.assign(time= pd.to_datetime(df['time']).dt.season).dropna(axis=1, how='all').round(2)

    df2=df.assign(season = pd.to_datetime(df['season'],format='%Y')).dropna(axis=1, how='all').round(2)
    indicator_name = indicator.replace("_"," ")
    plot_title = f'{indicator_name.title()} for the pixels over the seasons'
    y_title = f'{indicator_name.title()} [{unit}]'
    data = df2.melt('season')
    minv = data['value'].min()
    maxv = data['value'].max()
    chart = alt.Chart(data).mark_line().encode(
            x=alt.X('season:T',title='Year', axis=alt.Axis(tickCount="year")),  
            y=alt.Y("value:Q", title=y_title, scale=alt.Scale(domain=[minv*0.9, maxv*1.1])),
            color=alt.Color("variable:N",  title='Point', legend=alt.Legend(orient="right")),

            tooltip=[
                # alt.Tooltip(f'{col_name}:N', title=area_id),
                alt.Tooltip('season:T', title='season',format='%Y'),    
                alt.Tooltip(f'{indicator}:Q', title=indicator, format='.2f'),  # Format Value as decimal with 2 digits
            ]
        ).properties(
            # title=plot_title,
            height=300, 
            bounds="flush",  # Ensures title does not affect chart size
        ).configure_view(
            continuousWidth=600,  # Default width to avoid shrinking
            continuousHeight=300
        ).configure(
            autosize="fit",  # Ensures it resizes correctly
        )

    return chart, plot_title


def plotly_pie_chart(dfca, name, year, language):
    land_use_type_ar = {
        "uncultivated": "غير مزروع",
        "wheat": "قمح",
        "sorgum": "ذرة",
        "cotton": "قطن",
        "others": "اخرى",
    }

    df = dfca.melt(
        value_vars=[col for col in dfca.columns if "_pct" in col],
        var_name="landuse_type",
        value_name="percentage",
    )

    # Clean up the landuse_type column for better labels
    df["landuse_type"] = df["landuse_type"].str.replace("_pct", "")
    if language == arabic:
        df["landuse_type"] = [land_use_type_ar[lt] for lt in df["landuse_type"]]

    fig = px.pie(df, values="percentage", names="landuse_type")
    # Set a general hoverlabel style (one for all slices)
    fig.update_traces(
        hoverlabel=dict(
            bgcolor="rgba(0,0,0,0.7)",  # or pick a neutral color like gray or black
            font=dict(color="white"),
        )
    )

    fig.update_traces(
        hole=0.3, textposition="inside", textinfo="percent", textfont_size=16
    )

    if language == arabic:
        title = f"استخدامات الأراضي الشاغلة للغطاء الأرضي: {name} - {year}"
    elif language == english:
        title = f"Area covered by each landuse class for: {name} - {year}"
    else:
        raise NotImplementedError(f"This language is not supported yet {language}")

    return fig, title
