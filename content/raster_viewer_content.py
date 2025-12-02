from content.languages import arabic, english


raster_viewer_title = {
    arabic: "عرض صور المؤشرات بمشروع الجزيرة",
    english: "Gezira IPA Raster Viewer",
}


def stats_table_title(indicator_name, unit, season, language) -> str:
    if language == english:
        title = f"Stats of {indicator_name} [{unit}] - {season}"
    elif language == arabic:
        title = f"احصائيّات {indicator_name} [{unit}] - {season}"
    else:
        raise NotImplementedError("language not supported")

    return title


about_raster_viewer = {
    "label": {
        arabic: "ℹ️ عن عارض الخرائط",
        english: "ℹ️ About the raster viewer",
    },
    "markdown": {
        arabic: """
        هذه العارضة توفر عرضًا نقطيًا (راستر) لمؤشرات أداء الري.

        - يمكن اختيار السنة/الموسم والمؤشرات لعرض الصورة النقطية (الراستر) للسنة/الموسم والمؤشر المختار.
        - 📊 يوفّر الجدول الموجود على الجانب الأيمن إحصائيات الصورة المختارة.
        - 📈 يمكنك النقر على نقاط (بالعدد الذي تحتاجه) على الصورة النقطية (الراستر) وإنشاء مخطط سلسلة زمنية للنقاط.
        """,
        english: """
        This viewer provides raster view of the Irrigation Performance Indicators.

        - Year/Season and indicators can be selected to view the raster for year/season and indicator selected.
        - 📊 The dataframe on the right side provides statistic of the selected raster.
        - 📈 You can click points (as many points as needed) on the raster and generate a time series plot of the points.
        """,
    },
}


generate_time_series_button = {
    arabic: "إنشاء مخطط سلسلة زمنية",
    english: "Generate Time Series",
}


def raster_viewer_line_chart_title(indicator_name, language) -> str:
    if language == english:
        title = f"{indicator_name.title()} for the pixels over the seasons"
    elif language == arabic:
        title = f"{indicator_name} للنقاط خلال المواسم"
    else:
        raise NotImplementedError("language not supported")

    return title


raster_viewer_line_chart_subtitles = {
    "season": {
        arabic: "الموسم",
        english: "Season",
    },
    "year": {
        arabic: "السنة",
        english: "Year",
    },
    "point": {
        arabic: "النقطة",
        english: "Point",
    },
}
