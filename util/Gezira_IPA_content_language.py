sidebar_title = {
    "a": "مؤشرات أداء الري في مشروع الجزيرة",
    "e": "Gezira Irrigation Performance Indicators",
}

crop_lst = {
    "label": {
        "a": "إختر نوع المحصول",
        "e": "Select crop type",
    },
    "values": {
        "index": [0, 1, 2],
        "e": ["wheats", "sorgums", "cottons"],
        "a": ["القمح", "الذرة", "القطن"],
    },
}

crop_calendar = {
    "a": {'wheats': 'نوفمبر لمارس', 'sorgums':'يونيو لديسمبر', 'cottons':'يونيو لمارس'},
    "e": {'wheats': 'November to March', 'sorgums':'June to December', 'cottons':'June to March'}
}
def crop_calendar_txt(selected_crop_index, lang) -> str:
    selected_crop = crop_lst["values"][lang][selected_crop_index]
    selected_crop_calendar = crop_calendar[lang][crop_lst["values"]["e"][selected_crop_index]]
    if lang == "a":
        return f':blue[موسم] :blue[{selected_crop}] من :blue[{selected_crop_calendar}].'
    elif lang == "e":
        return f'The :blue[season] for :blue[{selected_crop}] runs from months of :blue[{selected_crop_calendar}].'
    else:
        raise NotImplementedError("language not supported")


select_season = {
    "label": {
        "a": "إختر موسماً",
        "e": "Select a season",
    },
    "help": {
        "a": "اختر الموسم الذي تود عرضه",
        "e": "Choose the Year/Season to visualize",
    },
}

indicator_map = {
    "a": "خريطة المؤشّر",
    "e": "Indicator Map",
}


e_a_indicator = {
    "crop water productivity": "انتاجية المياه",
    "crop water deficit": "شح االمياه",
    "quantile": "النسب",
    "relative water deficit": "شح المياه النسبي",
    "seasonal yield": "الانتاج الموسمي",
    "total seasonal biomass production": "الانتاج العضوي الموسمي",
    "beneficial fraction": "نسبة الاستفادة",
}


def indicator_lst(df_columns) -> dict:
    indicators = [" ".join(col.split("_")[1:]) for col in df_columns]
    indicators = list(set(indicators))
    indicators = [x for x in indicators if x not in ["a", "b", "quantile"]]
    indicator_dict = {
        "label": {
            "a": "اختر مؤشّر",
            "e": "Select an indicator",
        },
        "values": {
            "index": list(range(len(indicators))),
            "e": indicators,
            "a": [e_a_indicator[indicator] for indicator in indicators],
        },
        "help": {
            "a": "اختر مؤشر لعرضه",
            "e": "Choose the IPA indicator type to visualize"
        },
    }
    return indicator_dict


e_a_stats = {
    "Standard deviation": "الانحراف المعياري",
    "Minimum": "اقل قيمة",
    "Maximum": "اقصى قيمة",
    "Average": "المتوسّط",
    "Median": "الوسيط",
}


def stats_lst(stats_keys: list[str]) -> dict:
    indicator_dict = {
        "label": {
            "a": "اختر الاحصائيات",
            "e": "Select a statistics",
        },
        "values": {
            "index": list(range(len(stats_keys))),
            "e": stats_keys,
            "a": [e_a_stats[stat] for stat in stats_keys],
        },
        "help": {
            "a": "اختر الاحصائية لعرضها لعرضه",
            "e": "Choose the statistics to visualize"
        },
    }
    return indicator_dict


about_the_map = {
    "label": {"a": "ℹ️ عن خرائط المؤشرات", "e": "ℹ️ About the Indicator Map"},
    "markdown": {
        "a": """
        تُتيح خريطة المؤشرات عرض مؤشرات أداء الري (IPA) لمشروع ري الجزيرة.
        - تُحسب مؤشرات أداء الري باستخدام بيانات من: [بيانات WaPOR لمنظمة الأغذية والزراعة](https://www.fao.org/in-action/remote-sensing-for-water-productivity/wapor-data/en).
        - :orange[**خريطة المؤشرات**]: تُظهر قيم أقسام أو كتل مشاريع الري للمؤشر والإحصاءات المُختارة.
        - يُمكن اختيار السنة/الموسم ونوع المؤشر ونوع الإحصاءات لعرض المؤشر المُختار حسب السنة/الموسم ونوع الإحصاءات.
        - 📊 :orange[**مخطط شريطي**]: يُظهر على الجانب الأيمن مؤشر السنة المُختارة للقسم، بناءً على طريقة العرض على خريطة المؤشرات، مُرتّبًا حسب المؤشر المُختار.
        - 📈 :orange[**مخطط خطي**]: أو مخطط السلسلة الزمنية أسفل الخريطة يوضح الاتجاه على مر السنين (المواسم) للمؤشر المحدد.
        """,
        "e": """
        This Indicator Map provides view of the Irrigation Performance Indicators (IPA) for Gezira Irrigation Scheme.
        - IPAs are calculated using data from: [FAO WaPOR data](https://www.fao.org/in-action/remote-sensing-for-water-productivity/wapor-data/en).
        - :orange[**Indicator Map**]: Shows the irrigation schemes section or blocks values for the selected indicator and selected statistics.
        - Year/Season, and indicator type and statistic type can be selected to view the indicator selected by year/season and by statistics type.
        - 📊 :orange[**Bar Chart**]: on the right side shows the indicator for the selected year for the section or the block depending on which view is on the indicator map sorted by the selected indicator.
        - 📈 :orange[**Line Chart**]: or the timeseries plot below the map shows the trend over the years (seasons) for the selected indicator.
        """,
    },
}

raster_viewer_title = {
    "a": "عرض صور المؤشرات بمشروع الجزيرة",
    "e": "Gezira IPA Raster Viewer",
}
