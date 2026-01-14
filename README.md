# Gezira Irrigation Scheme Dashboard

A Streamlit-based dashboard for monitoring and analyzing irrigation performance indicators in the Gezira Irrigation Scheme. This interactive application provides bilingual support (English/Arabic) and visualizes agricultural water management data through multiple pages including overview, performance indicators, and raster map viewing.

## Access
**Try the live dashboard**: [https://gezira-ipa-ar.streamlit.app/](https://gezira-ipa-ar.streamlit.app/)

## Features

- **Multi-page Application**: Overview, Irrigation Performance Indicators, and Raster Viewer pages.
- **Bilingual Support**: Full English and Arabic language interface.
- **Interactive Visualizations**: Charts, maps, and performance metrics.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Gezira_IPA_AR
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run Gezira_scheme.py
   ```

The dashboard will open in your default web browser at `http://localhost:8501`

## Project Structure

```
ipa_gezira_dashboard/
├── Gezira_scheme.py          # Main application entry point
├── requirements.txt          # Python dependencies
├── pages/                    # Streamlit multi-page components
│   ├── overview.py          # Overview page
│   ├── ipa.py               # Irrigation Performance Indicators page
│   └── raster_viewer.py     # Raster map viewer page
├── content/                  # Page content and text
│   ├── overview_content.py
│   ├── ipa_content.py
│   ├── raster_viewer_content.py
│   ├── shared_content.py
│   └── languages.py         # Bilingual text definitions
├── util/                     # Utility functions
│   ├── maps.py              # Mapping utilities
│   ├── charts.py            # Chart creation functions
│   └── common2.py           # Shared utilities
└── data/                     # Data files (gitignored)
    ├── Gezira_ipa_results.nc    # Main NetCDF data
    ├── Gezira_IR.json           # Vector data
    ├── Gezira_IPA_statistic_*.csv # Crop statistics
    └── *.png                    # Logos and images
```

## Navigation

The dashboard features three main pages accessible through the sidebar:

1. **Overview/ملخّص**: General overview of the dashboard and scheme information.
2. **Irrigation Performance Indicators/مؤشّرات أداء الري**: IPA metrics and analysis.
3. **Raster Viewer/عارض الخرائط**: Map visualization.

## References

- Original Gezira Scheme dashboard done by [IHE Delft](https://www.un-ihe.org/):
    - [IHE dashboard](https://github.com/SolSeyoum/IPA_Gezira_v3/tree/main).
- Overview page, Gezira Scheme information:
    - [wikipedia](https://ar.wikipedia.org/wiki/%D9%85%D8%B4%D8%B1%D9%88%D8%B9_%D8%A7%D9%84%D8%AC%D8%B2%D9%8A%D8%B1%D8%A9) (Arabic version).
    - [wikipedia](https://en.wikipedia.org/wiki/Gezira_Scheme) (English version).
- Indices data source:
    - [WaPOR portal](https://www.fao.org/in-action/remote-sensing-for-water-productivity/en).
- Crop land map used:
    - [Geospatial cropland monitoring and crop type mapping of the Gezira irrigation scheme in the Sudan](https://doi.org/10.4060/cd1386en).
