# Analysing Pharmaceutical Sales Data

Explore six years of daily pharmaceutical sales in Pandas and Matplotlib. The dataset contains daily totals for eight ATC drug categories.

**Roadmap project:** <https://roadmap.sh/projects/pharmaceutical-sales-data>

## Questions covered

- Total sales quantities for each ATC category
- Highest selling categories overall and in January 2015, July 2016, and September 2017
- The category with the highest total in 2017
- Average daily sales by category
- Whether respiratory category R03 has a monthly pattern

The source data is aggregated to ATC categories; it does not contain individual brand names. The notebook documents that limitation and reports category-level rankings where a requirement asks for individual drugs or brands.

## Results from the included daily data

- `N02BE` has the highest total sales overall and the highest total in 2017.
- `N02BE` also has the highest average daily sales.
- Among the available category-level results, `N02BE` ranks first in January 2015, July 2016, and September 2017.
- The average daily `R03` sales peak in December in this dataset.

The period rankings and monthly pattern are generated from the data when you run the analysis; they are not brand-level results.

## Run the project

Python 3.10 or later is recommended.

```bash
python -m venv .venv
```

Activate the environment, install dependencies, then run the script:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
# source .venv/bin/activate

python -m pip install -r requirements.txt
python analyze_sales.py
```

To explore each question in the notebook:

```bash
jupyter notebook pharmaceutical_sales_analysis.ipynb
```

The script writes category totals, date-period rankings, average daily sales, monthly R03 averages, and charts to `outputs/`.

## Dataset and attribution

The `data/salesdaily.csv` file is the daily view of **Pharma Sales Data** by Milan Zdravković, available from [Kaggle](https://www.kaggle.com/datasets/milanzdravkovic/pharma-sales-data). A copy of the source data and its license notice are available in [mcallara/pharma-sales-data](https://github.com/mcallara/pharma-sales-data). The dataset is shared under the [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/). It is included here with attribution; the dataset's license applies to the data file, not the project code.

