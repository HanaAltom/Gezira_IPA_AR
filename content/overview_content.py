from os.path import join

import streamlit as st
from arabic_support import support_arabic_text

from content.languages import arabic, english


_IMAGES: dict[str, dict[str, str]] = {
    "error": {
        "link": "",
        arabic: "!الصورة غير موجودة!",
        english: "!image was not found!",
    },
    "satellite_image": {
        "link": "https://upload.wikimedia.org/wikipedia/commons/2/2d/Sudan_Gezira_Plain_1997.jpg",
        arabic: "قنوات الري كما تُرى من الفضاء، 1997",
        english: "The irrigation canals of the Gezira Scheme as seen from space, 1997",
        "source_english": "[source](https://en.wikipedia.org/wiki/Gezira_Scheme)",
        "source_arabic": "[المصدر](https://en.wikipedia.org/wiki/Gezira_Scheme)",
    },
    "gezira_scheme": {
        "link": join("data", "Gezira_Scheme.png"),
        arabic: "أقسام مشروع الجزيرة.",
        english: "Gezira Scheme Divisions",
    }
}


def st_image(image_key: str, lan: str):
    image = _IMAGES.get(image_key, _IMAGES["error"])
    caption = image[lan]
    link = image["link"]

    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.image(
            link,
            caption=caption,
            width=400
        )


def arabic_txt():
    lang = arabic
    support_arabic_text(all=True)
    st.markdown(
"""
# نظرة عامة على لوحة المعلومات
توفر هذه اللوحة تقييماً لأداء الري في مشروع الجزيرة عبر السنوات من 2020 - 2024.

المحاصيل الرئيسية المزروعة هي: 🌾 الذرة الرفيعة، 🌿 القمح، و🌼 القطن.

تُستخدم عدة مؤشرات مع الأخذ في الاعتبار أقسام ودفعات مشروع الجزيرة، وهي:
* العجز المائي.
* الإنتاجية الموسمية.
* إنتاجية المياه.
* إجمالي إنتاج الكتلة الحيوية الموسمية.
* العجز النسبي للمياه
* نسبة الإستفادة.
""", unsafe_allow_html=True)
    st_image("gezira_scheme", lang)
    st.markdown("""
تم الحصول على البيانات المستخدمة في هذا التحليل مثل AETI و RET من موقع الفاو WaPOR
، وتم الحصول على خرائط المحاصيل من منظمة الفاو.

إقرأ المزيد عن مشرع الجزيرة أدناه.....

# مشروع الجزيرة
يقع مشروع الجزيرة الزراعي في وسط السودان بين النيلين الأزرق والأبيض في السهل الطيني الممتد من منطقة سنار إلى جنوب الخرطوم عاصمة السودان. وأنشئ هذا المشروع في عام 1925 لمدّ المصانع البريطانية بحاجتها من خام القطن والذي شكل أيضاً العمود الفقاري لاقتصاد السودان بعد الاستقلال. ويعتبر مشروع الجزيرة أكبر مشروع مروي في أفريقيا وأكبر مزرعة في العالم ذات إدارة واحدة.
""", unsafe_allow_html=True)
    st_image("satellite_image", lang)
    st.markdown( """
# النشأة
بدأ مشروع الجزيرة في عام 1911م، كمزرعة تجريبية لزراعة القطن في مساحة قدرها 250 فدان (بمنطقة طيبة وكركوج) شمال مدينة ود مدني تروى بالطلمبات (مضخات المياه). بعد نجاح التجربة بدأت المساحة في الازدياد عاماً بعد آخر حتى بلغت 22 ألف فدان في عام 1924م. وفي العام الذي تلاه تم افتتاح خزان سنار وإزدادت المساحة المروية حتى بلغت حوالي المليون فدان في عام 1943م. والفترة من 1958 وحتى 1962م تمت إضافة أرض زراعية بمساحة مليون فدان أخرى عرفت باسم امتداد المناقل، لتصبح المساحة الكلية للمشروع اليوم 2,2 مليون فدان.

# أهداف المشروع
* زراعة محاصيل الصادر، كالقطن وزهرة الشمس.
* تحويل المنطقة من الزراعة التقليدية إلى الحديثة.
* رفع المستوى المعيشي والخدمي باستيعاب 15 ألف مزارع، وتوفير السكن والخدمات الصحية والتعليمية لهم.
* تحقيق التكامل الزراعي بإدخال الحيوان في الدورة الزراعية،
* التوسع في زراعة الخضر والفاكهة للاستهلاك المحلي والتصدير.
* استغلال حصة السودان من مياه النيل.

# المساحة
قام مشروع الجزيرة على مساحة تقدر بحوالي (2,200,000 فدان) تمتد شمالاً من حدود الخرطوم الجنوبية وتوزع ملكية الأرض فيها على النحو التالي:
* الحكومة تملك (000 ,300 ,1 فدان) (حسب قانون 1898).
* الملاك الأهالي (000 ,900 فدان). (تقدر الأراضي الملك الحر في مشروع الجزيرة بحوالي (518,000 فدان) و(382,000 فدان) في امتداد المناقل.

# إدارة المشروع
عندما تقرر تأميم المشروع في العام 1950 انتقلت إدارة مشروع الجزيرة إلى مجلس إدارة المشروع الجديد برئاسة المحافظ الإنجليزي للمشروع المستر جنيسكل الذي ظل في خدمة المشروع في الفترة من عام 1923 وحتى 1952 م قبل أن تتم سودنة وظيفة المحافظ. وكان أول محافظ سودانى هو السيد مكي عباس الذي تولى الوظيفة من عام 1955 - 1958 م واستمرت الإدارة الجديدة في سودنة الوظائف عام بعد عام. وبحلول 1956 م، اكتملت سودنة جميع الوظائف.\n
تتكون إدارة المشروع حالياً من مجلس إدارة يرأسه وزير الزراعة الإتحادي و15 عضو منهم مدير عام المشروع ووكيل وزارة الزراعة الإتحادية وممثل لوزارة المالية ونائب محافظ بنك السودان المركزي وممثل لكل من ولاية الجزيرة وشركة الأقطان السودانية وهيئة البحوث الزراعية إلى جانب ممثل للعمال والموظفين بالمشروع وستة ممثلين آخرين للمزارعين.\n
يتولى المدير العام إدارة العمل التنفيذي في المشروع بمساعدة أربع هيئات إدارية هي:
* الإدارة الزراعية.
* الإدارة الهندسية.
* الإدارة المالية.
* إدارة الشؤون الإدارية.
ويتبع لكل هيئة من الهيئآت الأدارية الأربع عددا من الوحدات المتخصصة. وتعتبر الإدارة الزراعية أكبر الإدارت حيث تتولى إدارة العمليات الإنتاجية في المشروع وتنفسم إلى 18 قسم ميداني ولكل قسم لجنة إدارية يتبع لها عدد من وحدات أصغر تعرف بالتفاتيش (المفرد تفتيش) يبلغ عددها الحالي حوالي 113 تفتش. ويضم التفتيش كل تجهيزات ووسائط العمل من مساكن للعاملين ومكاتب ومخازن وورش بالإضافة إلى ى محالج القطن (في بلدات مارنجان والحصاحيصا والباقير القريبة من الخرطوم) كما يشمل التفتيش شبكة النقل الداخلي للإنتاج المتمثلة في خطوط السكة الحديدية الخفيفة التابعة للمشروع. وتوجد محطة أبحاث زراعية في مدينة ود مدني مهمتها دراسة تحسين البذور وغيرها من الأبحاث ذات الصلة بإنتاج القطن.\n
وكان بالمشروع 68 مكتباً لمراقبة الغيط، منها مكتب سابع دليب، ومكتب حمد النيل، ومكتب الغبشان، وغيرها. ويتكون الهيكل الوظيفي لمكتب المراقبة من موظفين (الباشمفتش، والمفتش الأول، والباشغفير، والغفير الأول، والفراش، والمحاسب، والباشمحاسب).\n
مقر رئاسة إدارة المشروع في بلدة بركات بولاية الجزيرة والواقعة على خط السكة الحديدية الذي يربط سنار عبر المشروع بالخرطوم.

# المحاصيل
تتمثل أهم المحاصيل في: القطن، الفول السوداني، الذرة، القمح، والذرة الرفيعة، الذرة، الخضروات، الأعلاف، زهرة الشمس بالإضافة إلى الإنتاج الحيواني. وكان المشروع ينتج أيضاً الأرز قبل أن يتوقف عن ذلك لظروف مناخية، أو ربما تم استبعاده - كما يرى البعض - لمنافسته للقطن الذي كان يعتبر المحصول الاقتصادي الأول وقتئذ، وقد تم نقل زراعة الأرز إلى منطقة النيل الأبيض حيث المياه الفائضة التي تغمر مساحات شاسعة (تقدر بحوالي مليون فدان) خلال الفترة التي يتم فيها أغلاق أبواب سد جبل أولياء في الفترة من سبتمبر / تشرين الأول وحتى مارس / آذار من كل عام.\n

إنتاج الأراضي من المحاصيل في الموسم الزراعي 1992-1993:
* ذرة رفيعة     550,000 فدان
* قمح         530,000 فدان
* فول سوداني    188,000 فدان
* قطن        152,000 فدان
* خضروات     50,000 فدان
* الذرة        5,000 فدان

# نظام الرّي
يعتمد الإنتاج الزراعي في مشروع الجزيرة بصفة أساسية على الرّي الصناعي وكذلك الأمطار في الفترة ما بين شهرى يوليو / تموز – أكتوبر / تشرين الأول) والتي تساهم في ري بعض المحاصيل الصيفية.\n
يتم ريّ المشروع عن طريق ما يعرف بالرّي الانسيابي من سد سنار الذي شُيّد في عام (1925 م). ويتم توزيع المياه بواسطة شبكة من القنوات يبلغ طولها (375,14 كيلومتر) بطاقة تخزينية قدرها 31 مليون متر مكعب، وقد تم تصميم هذا النظام ليعمل بنظام التخزين نهاراً. يتم التحكم في حجم المياه وتوزيعها لمقابلة الاحتياجات المائية لمحاصيل الدورة الزراعية بواسطة عمالاً وأجهزة تشغيل مختلفة موزعة على طول هذه القنوات.\n
يعتمد الرّي الانسيابي، الذي يتميز بانخفاض تكاليفه، علي مدى استواء سطح الأرض وانسيابها من الجنوب نحو الشمال، وذلك من خلال شبكة من القنوات طولها 2300 كيلومتر وتتكون من 1500 قناة صغيرة طولها 8000 كيلومتر وقناتين (ترعتين) رئيسيتين بسعة 345 متر مكعب في الثانية وهما قناة الجزيرة وقناة المناقل.. وتعمل هذه القنوات ابتدء من الترعة الرئيسية على نقل المياه من السد (الذي يعرف لدى المزارعين باسم الخزان) الي الترعة الفرعية ومنها إلى جدوال كبيرة يعرف الواحد منها باسم «أبو عشرين » ومن جدوال أبوعشرين الي جدوال أخرى أصغر حجماً تعرف بجداول «أبوستة» ومن أبو ستة الي الجدول الأصغر داخل المساحة المزروعة (الحواشة).\n
كانت أرض المزارع في السابق مقسمة إلى اربع حواشات، مساحة الواحدة منها تبلغ 5 فدان. ولكن بتغيير الدورة الزراعية الي دورة خماسية أصبحت الحواشات بمساحة اربع افدنة نسبة لتغير التركيبة المحصولية للمزارع.\n
مشاكل المشروعنظام تشغيل المشروع نظام غير معقد ويعود إلى عشرينيات القرن الماضي ونسبة لجودة نوعية الموارد الطبيعية من مياه وتربة فإن المشروع قد استمر يعمل بشكل جيد لفترة طويلة. وقد بدأت المشاكل الحقيقية التي واجهته في سبعينيات القرن الماضي وتفاقمت مع مرور الزمن حتى غدت تشكل تهديداً خطيراً لاستمراره بشكله الحالي. ومن أهم المشاكل نقص الموارد والاعتمادات المالية اللازمة لأعمال صيانة وخصخصة المشروع وبيع ممتلكاته واستبدال الآلات والبنيات القديمة خاصة نظام الاتصالات داخل وحدات المشروع الذي يعتبر ضرورياً في إدارة عمليات الريّ وتعذر إزالة الطمي والحشائش وصيانة شبكات المجاري والقنوات وأنظمة النقل والتخزين.\n
المصدر: [ويكيبيديا](https://ar.wikipedia.org/wiki/%D9%85%D8%B4%D8%B1%D9%88%D8%B9_%D8%A7%D9%84%D8%AC%D8%B2%D9%8A%D8%B1%D8%A9).
""", unsafe_allow_html=True)

    # References
    st.markdown("""
# مراجع

- لوحة معلومات مشروع الجزيرة من [IHE Delft](https://www.un-ihe.org/):
    - [IHE dashboard](https://github.com/SolSeyoum/IPA_Gezira_v3/tree/main).
- مصدر بيانات المؤشرات:
    - [بوابة الوابور](https://www.fao.org/in-action/remote-sensing-for-water-productivity/ar).
- خريطة الأراضي الزراعية المستخدمة:
    - [Geospatial cropland monitoring and crop type mapping of the Gezira irrigation scheme in the Sudan](https://doi.org/10.4060/cd1386en).
""", unsafe_allow_html=True)

# This dashboard provides an assessment of the irrigation performance of Gezira Scheme over the years {season_list[-1][:4]} - {season_list[0][5:]}.
def english_txt():
    support_arabic_text(all=False)
    lang = english
    st.markdown(
"""
# Dashboard Overview
* This dashboard provides an assessment of the irrigation performance of Gezira Scheme over the years.
* Main cultivated crops are ,🌾 Sorghum, 🌿 Wheat and 🌼 Cotton.
* Different indicators are used considering the sections and divisions of Gezira Scheme which are:
    - Crop water deficit.
    - Seasonal yield.
    - Crop water productivity.
    - Total seasonal biomass production.
    - Relative water deficit.
    - Beneficial fraction.
""", unsafe_allow_html=True)
    st_image("gezira_scheme", lang)
    st.markdown("""
The data used for this analysis, such as AETI and RET, was obtained from [FAO WaPOR](https://data.apps.fao.org/wapor/?lang=en). , and crop maps were obtained from [FAO](https://openknowledge.fao.org/).

# Gezira Scheme
The Gezira Scheme (Arabic: مشروع الجزيرة) is one of the largest irrigation projects in the world. It is centered on the Sudanese state of Gezira, just southeast of the confluence of the Blue and White Nile rivers at the city of Khartoum. The Gezira Scheme was begun by the British while the area was governed as part of Anglo-Egyptian Sudan. Water from the Blue Nile is distributed through canals and ditches to tenant farms lying between the Blue and White Nile.]
The Gezira (which means "island") is particularly suited to irrigation because the soil slopes away from the Blue Nile and water therefore naturally runs through the irrigation canals by gravity. The soil has a high clay content which keeps down losses from seepage. Reginald Wingate, the British governor-general of Sudan, originally envisaged the farmers growing wheat but this was abandoned as the colonial authorities thought that a better cash crop was needed. When it was discovered that Egyptian-type long staple cotton could be grown, this was welcomed as a better choice as it would also provide a raw material for the British textile industry. Cotton was first grown in the area in 1904. After many experiments with irrigation, 24 square kilometres (9.3 sq mi) was put under cultivation in 1914.\n
After the lowest Nile flood for 200 years, the Sennar Dam was constructed on the Blue Nile to provide a reservoir of water. This dam was completed in 1925 and is about 3 kilometres (1.9 mi) long. The Gezira Scheme was initially financed by the Sudan Plantations Syndicate in London and later the British government guaranteed capital to develop it. The Sudan Gezira Board took over from private enterprise in 1950 and was chaired by Arthur Gaitskell.\n
Farmers cooperated with the Sudanese government and the Gezira Board. This network of canals and ditches was 4,300 kilometres (2,700 mi) long, and with the completion in the early 1960s of the Manaqil Extension on the western side of the Gezira Scheme, by 2008 the irrigated area covered 8,800 square kilometres (3,400 sq mi), about half the country's total land under irrigation. The main crop grown in this region was still cotton.\n
source: [wikipedia](https://en.wikipedia.org/wiki/Gezira_Scheme)
""", unsafe_allow_html=True)

    # References
    st.markdown("""
# References

- Original Gezira Scheme dashboard done by [IHE Delft](https://www.un-ihe.org/):
    - [IHE dashboard](https://github.com/SolSeyoum/IPA_Gezira_v3/tree/main).
- Indices data source:
    - [WaPOR portal](https://www.fao.org/in-action/remote-sensing-for-water-productivity/en).
- Crop land map used:
    - [Geospatial cropland monitoring and crop type mapping of the Gezira irrigation scheme in the Sudan](https://doi.org/10.4060/cd1386en).
""", unsafe_allow_html=True)
