# Automated-API-Data-Pipelines-World-Indicators-Analysis-using-PowerBI
I built an automated pipeline using a Python script to ingest macroeconomic data from the World Bank REST API, transform it, and model it in Power BI. I used advanced DAX to calculate historical percentage changes dynamically and integrated Python scripts for correlation matrix heatmaps and health expenditure regression analysis.

![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![DAX](https://img.shields.io/badge/DAX-Data_Analysis_Expressions-blue?style=for-the-badge)
![REST API](https://img.shields.io/badge/REST_API-World_Bank-0071C5?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)

An end-to-end macroeconomic and public health intelligence solution that ingests data from the **World Bank REST API**, processes time-series metrics via an automated ETL pipeline, and delivers interactive exploratory analytics using **Power BI**, **DAX**, and **embedded Python data visualizations**.

---

# 📌 Executive Summary & Dashboard Preview

The **World Indicators Dashboard** translates global development indicators (GDP, health expenditure, internet penetration, poverty rates, and mortality metrics) into actionable policy and economic insights.

It answers **9 core business & policy questions** to identify underperforming regions, measure digital connectivity impact, and evaluate public health ROI.

![World Indicators Dashboard Overview](.github/screenshots/dashboard_overview.png)

---

# 🛠️ Architecture & Data Pipeline Flow

The platform utilizes a hybrid pipeline combining automated API extraction, Power Query transformation, dynamic DAX modeling, and custom Python statistical rendering.

```text
┌──────────────────────────────────────────────┐
│          World Bank REST API                 │
│   (Endpoints: /countries, /indicators)       │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│          Python ETL Pipeline                 │
│ Fetches JSON, handles nulls, normalizes data │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│         Power Query & Data Model             │
│ Star Schema, Relationships, Date Dimension   │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────┐
│          Power BI Dashboard                  │
│ DAX Measures + Python Visualizations         │
└──────────────────────────────────────────────┘
```

---

# 💡 Key Questions Answered & Business Value

| # | Analytical Question | Visual Solution | Primary Insight / Value |
|---|---------------------|-----------------|-------------------------|
| **1** | **Overall Economic & Social Landscape** | Executive KPI Cards | Baseline metrics: Avg GDP per Capita ($18.62K), Trade Value ($1.49T), Health Spend (6.21% of GDP), GDP Growth (3.68%). |
| **2** | **Regional Health Spending Patterns** | Custom Bar Chart | Compares health spending (% of GDP) across global regions to highlight regional investment disparities. |
| **3** | **Socio-Economic Indicator Trends** | Multi-Line Time Series | Tracks historical changes (1990–2024) across forest area, mobile/internet subscriptions, GDP, and energy usage. |
| **4** | **Internet Access vs. Immunization** | Dual-Line Trend Analysis | Evaluates whether digital connectivity correlates with increased public health engagement and immunization. |
| **5** | **Internet Access vs. Unemployment** | Animated Play-Axis Scatter Plot | Explores whether expanding internet penetration lowers unemployment rates over time across nations. |
| **6** | **Bottom 10 Countries in Poverty Reduction** | Dynamic Top/Bottom DAX Table | Identifies countries showing the least progress (or increase) in national poverty headcount ratio. |
| **7** | **Top 10 Countries in Poverty Reduction** | Dynamic Top/Bottom DAX Table | Highlights high-performing success stories in poverty alleviation (e.g., China -100%, Vietnam -93%). |
| **8** | **Interrelationships Among Health Metrics** | Python Seaborn Heatmap | Statistical correlation matrix measuring ties between health spend, life expectancy, mortality, and disease burden. |
| **9** | **Government Spend vs. Life Expectancy** | Python Matplotlib Regression | Linear regression trend line assessing if higher government health spending directly extends life expectancy. |

---

# 🧮 Technical Deep Dive: DAX & Python Engineering

## 1. Dynamic Poverty Reduction Percentage (DAX)

To measure historical poverty reduction regardless of missing survey years per country, a custom DAX measure calculates the relative change between the earliest and latest available observations.

```dax
Poverty Change % =
VAR _Indicator = "Poverty headcount ratio at national poverty lines (% of population)"

VAR _ValidTable =
    FILTER(
        'poverty',
        'poverty'[indicator_name] = _Indicator
            && NOT ISBLANK('poverty'[value])
            && 'poverty'[value] <> 0
    )

VAR _MinDate =
    CALCULATE(
        MIN('poverty'[date]),
        _ValidTable
    )

VAR _MaxDate =
    CALCULATE(
        MAX('poverty'[date]),
        _ValidTable
    )

VAR _MinValue =
    CALCULATE(
        AVERAGE('poverty'[value]),
        _ValidTable,
        'poverty'[date] = _MinDate
    )

VAR _MaxValue =
    CALCULATE(
        AVERAGE('poverty'[value]),
        _ValidTable,
        'poverty'[date] = _MaxDate
    )

RETURN
    DIVIDE(_MaxValue - _MinValue, _MinValue) * 100
```

---

## 2. Embedded Python Statistical Graphics

### A. Correlation Matrix Heatmap (Seaborn)

Executed directly inside Power BI to compute feature correlations across health indicators.

```python
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(8, 6))

correlation_matrix = dataset.corr()

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5
)

plt.title("Correlation Between Health Indicators")
plt.show()
```
<img width="2726" height="2344" alt="Heatmap" src="https://github.com/user-attachments/assets/cecb1400-450a-490f-89c1-06bb1ceaf36a" />

---

### B. Linear Regression Model (Health Spend vs. Life Expectancy)

Evaluates structural returns on public health investment using a fitted regression line.

```python
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(7, 5))

sns.regplot(
    x='Current health expenditure (% of GDP)',
    y='Life expectancy at birth, total (years)',
    data=dataset,
    color='#3182bd',
    line_kws={'color': 'red'}
)

plt.xlabel("Current Health Expenditure (% of GDP)")
plt.ylabel("Life Expectancy at Birth (Years)")
plt.title("Government Health Expenditure vs. Life Expectancy")

plt.grid(True, linestyle='--', alpha=0.5)

plt.show()
```

---

# 📊 Key Insights & Analytical Findings

### 1. Health Spending vs. Life Expectancy ROI

Regression analysis indicates a positive relationship up to approximately **8–10% of GDP**. Beyond this threshold, additional health expenditure provides diminishing improvements in life expectancy unless accompanied by strong sanitation, education, and healthcare infrastructure.
<img width="730" height="827" alt="Screenshot 2026-08-07 171719" src="https://github.com/user-attachments/assets/8acbe70d-58b2-4a72-9b71-2f5cf76a39ba" />
<img width="747" height="821" alt="Screenshot 2026-08-07 171654" src="https://github.com/user-attachments/assets/83435a7c-ed5d-4f32-bec4-338e23240605" />
<img width="731" height="812" alt="Screenshot 2026-08-07 171637" src="https://github.com/user-attachments/assets/9d52280d-2c6c-4618-8ed5-a8219c61bea6" />
Unexpectedly, Our regression analysis reveals that government health expenditure (% of GDP) exhibits diminishing returns and, in some regions, a negative correlation with life expectancy. This proves that policy interventions should focus on healthcare system efficiency and preventative care rather than simply inflating public health budgets as a percentage of GDP."

### 2. Poverty Reduction Success

Asian economies such as **China**, **Vietnam**, and **Thailand** achieved more than **90% poverty reduction** during the evaluated period, driven by industrialization, sustained economic growth, and digital expansion.
<img width="273" height="617" alt="image" src="https://github.com/user-attachments/assets/d38b61c2-9f68-479a-bf97-3b10b2d7e847" />

### 3. Digital Divide & Immunization

Countries experiencing rapid internet adoption (>60% penetration) generally exhibited improvements in childhood immunization coverage, suggesting that digital connectivity supports healthcare awareness and outreach.
<img width="943" height="335" alt="image" src="https://github.com/user-attachments/assets/8ceab095-8bff-4813-a54f-c9f493798bbb" />

### 4. Socio Economic Trends Over time
Time-series analysis from 1990 to 2024 reveals a stark contrast between technological adoption and environmental policy: while mobile subscriptions surged from <1% to >115% saturation and internet usage reached ~70% globally, environmental metrics (forest area and renewable energy share) remained stagnant at ~30%. Additionally, the GDP growth trend clearly isolates the severe economic contraction of the 2020 global pandemic
<img width="1108" height="501" alt="image" src="https://github.com/user-attachments/assets/d47aa8cf-77d2-47d0-8373-9d188df80dfb" />

---

# 🚀 How to Run & Reproduce Locally

## Prerequisites

- Power BI Desktop (Latest Version)
- Python 3.9+
- pandas
- requests
- matplotlib
- seaborn

---

## Step 1 — Clone the Repository

```bash
git clone https://github.com/your-username/world-indicators-analytics.git

cd world-indicators-analytics
```

---

## Step 2 — Configure Python in Power BI

1. Open **Power BI Desktop**
2. Navigate to:

```
File
 └── Options and settings
      └── Options
           └── Python scripting
```

3. Select your Python installation (e.g. `C:\Python39` or your Conda environment).

4. Install the required libraries:

```bash
pip install pandas matplotlib seaborn requests
```

---

## Step 3 — Open the Dashboard

Navigate to the **pbix/** folder and open:

```
World_Indicators_Analysis.pbix
```

---

# 📁 Repository Structure

```
world-indicators-analytics/
│
├── data/
│   ├──indicators.csv
│
├── script/
│   ├── fetch_worldbank_api.py
│
├── pbix/
│   └── World_Indicators_Analysis.pbix
│
├── .github/
│   └── screenshots/
│       └── dashboard_overview.png
        ├──analysis_with_slicer_filtering.gif
        ├──Heatmap.png
        ├──Regression plot.png

│
├── README.md
```

---

# 🛠️ Technology Stack

- **Power BI Desktop**
- **Power Query**
- **DAX**
- **Python**
- **Pandas**
- **Matplotlib**
- **Seaborn**
- **REST API**
- **World Bank Open Data API**

---

# 📫 Contact & Author

**Developer:** Suraj Bhandari

**Email:** surajbhandari6731@gmail.com

---

## ⭐ Support

If you found this project useful or insightful, consider giving it a ⭐ on GitHub!
