from content.languages import arabic, english


STATS = {
    "Standard deviation": "std",
    "Minimum": "min",
    "Maximum": "max",
    "Average": "mean",
    "Median": "meadian",
}


sidebar_title = {
    arabic: "مؤشرات أداء الري في مشروع الجزيرة",
    english: "Gezira Irrigation Performance Indicators",
}


select_season = {
    "label": {
        arabic: "إختر موسماً",
        english: "Select a season",
    },
    "help": {
        arabic: "اختر الموسم الذي تود عرضه",
        english: "Choose the Year/Season to visualize",
    },
}


select_indicator = {
    "label": {
        arabic: "اختر مؤشّر",
        english: "Select an indicator",
    },
    "values": {
        "index": (0, 1, 2, 3, 4, 5),
        english: (
            "crop water productivity",
            "crop water deficit",
            "relative water deficit",
            "seasonal yield",
            "total seasonal biomass production",
            "beneficial fraction",
        ),
        arabic: (
            "انتاجية المياه",
            "شح االمياه",
            "شح المياه النسبي",
            "الانتاج الموسمي",
            "الانتاج العضوي الموسمي",
            "نسبة الاستفادة",
        ),
    },
    "help": {
        arabic: "اختر مؤشر لعرضه",
        english: "Choose the IPA indicator type to visualize",
    },
    "units": {
        english: (
            "kg/m³",
            "-",
            "-",
            "ton/ha",
            "ton",
            "-",
        ),
        arabic: (
            "كج/م³",
            "-",
            "-",
            "طن/هيكتار",
            "طن",
            "-",

        ),
    },
}


select_stat = {
    "label": {
        arabic: "اختر الاحصائيات",
        english: "Select a statistics",
    },
    "values": {
        "index": (0, 1, 2, 3, 4),
        english: ("Standard deviation", "Minimum", "Maximum", "Average", "Median"),
        arabic: ("الانحراف المعياري", "اقل قيمة", "اقصى قيمة", "المتوسّط", "الوسيط"),
    },
    "help": {
        arabic: "اختر الاحصائية لعرضها لعرضه",
        english: "Choose the statistics to visualize",
    },
}
