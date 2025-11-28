from content.languages import arabic, english


page_title = {
    arabic: "مؤشرات أداء الري",
    english: "Irrigation Performance Indicators",
}


indicator_map = {
    arabic: "خريطة المؤشّر",
    english: "Indicator Map",
}


select_crop_type = {
    "label": {
        arabic: "إختر نوع المحصول",
        english: "Select crop type",
    },
    "values": {
        "index": (0, 1, 2),
        english: ["wheats", "sorgums", "cottons"],
        arabic: ["القمح", "الذرة", "القطن"],
    },
}


_crop_calendar = {
    arabic: {
        "wheats": "نوفمبر لمارس",
        "sorgums": "يونيو لديسمبر",
        "cottons": "يونيو لمارس",
    },
    english: {
        "wheats": "November to March",
        "sorgums": "June to December",
        "cottons": "June to March",
    },
}


reset_map_label = {
    arabic: "🔄 إرجاع الخريطة",
    english: "🔄 Reset Map",
}


def crop_calendar_txt(selected_crop_index, lang) -> str:
    selected_crop = select_crop_type["values"][lang][selected_crop_index]
    selected_crop_calendar = _crop_calendar[lang][
        select_crop_type["values"][english][selected_crop_index]
    ]
    if lang == arabic:
        return f":blue[موسم] :blue[{selected_crop}] من :blue[{selected_crop_calendar}]."
    elif lang == english:
        return f"The :blue[season] for :blue[{selected_crop}] runs from months of :blue[{selected_crop_calendar}]."
    else:
        raise NotImplementedError("language not supported")


about_the_map = {
    "label": {
        arabic: "ℹ️ عن خرائط المؤشرات",
        english: "ℹ️ About the Indicator Map",
    },
    "markdown": {
        arabic: """
        تُتيح خريطة المؤشرات عرض مؤشرات أداء الري (IPA) لمشروع ري الجزيرة.
        - تُحسب مؤشرات أداء الري باستخدام بيانات من: [بيانات WaPOR لمنظمة الأغذية والزراعة](https://www.fao.org/in-action/remote-sensing-for-water-productivity/wapor-data/en).
        - :orange[**خريطة المؤشرات**]: تُظهر قيم أقسام أو كتل مشاريع الري للمؤشر والإحصاءات المُختارة.
        - يُمكن اختيار السنة/الموسم ونوع المؤشر ونوع الإحصاءات لعرض المؤشر المُختار حسب السنة/الموسم ونوع الإحصاءات.
        - 📊 :orange[**مخطط شريطي**]: يُظهر على الجانب الأيمن مؤشر السنة المُختارة للقسم، بناءً على طريقة العرض على خريطة المؤشرات، مُرتّبًا حسب المؤشر المُختار.
        - 📈 :orange[**مخطط خطي**]: أو مخطط السلسلة الزمنية أسفل الخريطة يوضح الاتجاه على مر السنين (المواسم) للمؤشر المحدد.
        """,
        english: """
        This Indicator Map provides view of the Irrigation Performance Indicators (IPA) for Gezira Irrigation Scheme.
        - IPAs are calculated using data from: [FAO WaPOR data](https://www.fao.org/in-action/remote-sensing-for-water-productivity/wapor-data/en).
        - :orange[**Indicator Map**]: Shows the irrigation schemes section or blocks values for the selected indicator and selected statistics.
        - Year/Season, and indicator type and statistic type can be selected to view the indicator selected by year/season and by statistics type.
        - 📊 :orange[**Bar Chart**]: on the right side shows the indicator for the selected year for the section or the block depending on which view is on the indicator map sorted by the selected indicator.
        - 📈 :orange[**Line Chart**]: or the timeseries plot below the map shows the trend over the years (seasons) for the selected indicator.
        """,
    },
}


ipa_description = {
    "beneficial fraction": {
        english: ":blue[Beneficial fraction (BF)] is the ratio of the water that is consumed as transpiration\
         compared to overall field water consumption (ETa). ${\\footnotesize BF = T_a/ET_a}$. \
         It is a measure of the efficiency of on farm water and agronomic practices in use of water for crop growth.",
        arabic: "تشير :blue[النسبة المئوية النافعة (BF)] إلى نسبة المياه المستهلكة **كنتح (transpiration)** مقارنةً بإجمالي استهلاك المياه في الحقل (**النتح التبخري الفعلي (ETa)**). $$BF = T_a/ET_a$$ وهي مقياس لكفاءة الممارسات الزراعية واستخدام المياه داخل المزرعة في استخدام المياه لنمو المحصول.",
    },
    "crop water deficit": {
        english: ":blue[crop water deficit (CWD)] is measure of adequacy and calculated as the ration of seasonal\
        evapotranspiration to potential or reference evapotranspiration ${\\footnotesize CWD= ET_a/ET_p}$",
        arabic: "يشير :blue[عجز مياه المحصول (CWD)] إلى مقياس للكفاية ويتم حسابه كنسبة النتح التبخري الموسمي الفعلي إلى النتح التبخري الممكن أو المرجعي. $$CWD= ET_a/ET_p$$",
    },
    "relative water deficit": {
        english: ":blue[relative water deficit (RWD)] is also a measure of adequacy which is 1 minus crop water\
          deficit ${\\footnotesize RWD= 1-ET_a/ET_p}$",
        arabic: "يشير :blue[عجز المياه النسبي (RWD)] إلى مقياس للكفاية، وهو **1 ناقص** عجز مياه المحصول. $$RWD= 1-ET_a/ET_p$$",
    },
    "total seasonal biomass production": {
        english: ":blue[total seasonal biomass production (TBP)] is total biomass produced in tons. \
        ${\\footnotesize TBP = (NPP * 22.222) / 1000}$",
        arabic: "يشير :blue[إجمالي إنتاج الكتلة الحيوية الموسمي (TBP)] إلى إجمالي الكتلة الحيوية المنتجة بالطن. $$TBP = (NPP * 22.222) / 1000$$",
    },
    "seasonal yield": {
        english: ":blue[seasonal yield] is the yield in a season which is crop specific and calculated using \
        the TBP and yield factors such as moisture content, harvest index, light use efficiency correction \
            factor and above ground over total biomass production ratio (AOT) \
                ${\\footnotesize Yiled = TBP*HI*AOT*f_c/(1-MC)}$",
        arabic: "يشير :blue[المحصول الموسمي] إلى المحصول الناتج في موسم معين، وهو خاص بالمحصول ويتم حسابه باستخدام إجمالي إنتاج الكتلة الحيوية الموسمي (**TBP**) وعوامل المحصول مثل **محتوى الرطوبة (MC)**، **مؤشر الحصاد (HI)**، **عامل تصحيح كفاءة استخدام الضوء ($f_c$)**، ونسبة الإنتاج فوق سطح الأرض إلى إجمالي إنتاج الكتلة الحيوية (**AOT**). $$Yield = TBP*HI*AOT*f_c/(1-MC)$$",
    },
    "crop water productivity": {
        english: ":blue[crop water productivity (CWP)] is the seasonal yield per the amount of water \
        consumed in ${kg/m^3}$",
        arabic: "تشير :blue[إنتاجية مياه المحصول (CWP)] إلى المحصول الموسمي لكل كمية المياه المستهلكة بوحدة ${kg/m^3}$",
    },
}


pie_chart_name = {
    arabic: "الجزيرة",
    english: "Gezira",
}


division_alias = {
    arabic: "القسم:", english: "Division:"
}


section_alias = {
    arabic: "الجزء:", english: "Section:"
}


area_id_translation = {
    "division": {arabic: "قسم", english: "division"},
    "section": {arabic: "جزء", english: "section"},
}


def line_chart_content(indicator_name, stat_name, area_id, unit, language):
    if language == arabic:
        chart_title = f"{stat_name} ل{indicator_name} لكل {area_id} للمواسم السابقة"
        x_title = "الموسم"
    elif language == english:
        chart_title = f"{stat_name} {indicator_name.title()} per {area_id} for the past seasons"
        x_title = "Season"
    else:
        raise NotImplementedError("language not supported")
    y_title = f"{indicator_name.title()} [{unit}]"
    return chart_title, x_title, y_title

