# Global COVID-19 Data Analysis

## Project Overview
This project explores global COVID-19 data from **Our World in Data (OWID)** to understand pandemic trends, country-level impacts, and the relationship between socio-economic indicators and COVID-19 outcomes. The goal is to provide a **clean dataset** and **insightful visualizations** suitable for portfolio presentation.

## Tools
Python, Pandas, Plotly Express

## Dataset
The dataset includes:
- **Location** – country name
- **Date** – daily record
- **Total Cases** – cumulative COVID-19 cases
- **Total Deaths** – cumulative COVID-19 deaths
- **GDP per Capita** – economic indicator
- **Human Development Index (HDI)** – development indicator

## Data Cleaning & Preprocessing
- Selected 6 key columns from 41 to simplify analysis.
- Converted `date` column to **datetime** format for time-series analysis.
- Handled missing values:
  - Dropped rows with missing `total_cases` or `total_deaths`.
  - Imputed `gdp_per_capita` and `human_development_index` with mode.
- Checked for duplicates – none found.
- Renamed columns for **readability** (e.g., `total_cases` → `Total Cases`).

## Analysis Highlights
### Case Fatality Rate (CFR)
- Calculated CFR for each country: `(Total Deaths / Total Cases) * 100`.
- **Top 10 countries by CFR** include Yemen (28.9%), Italy (12.1%), UK (10.8%).
- **Global average CFR**: 2.55%.

### Time-Series Insights
- **Poland:** slower initial outbreak; gap between cases and deaths; second surge visible by September 2020.
- **Italy:** early explosive outbreak; high first-wave mortality; curve flattened by May 2020.
- Comparative analysis shows **timing and scale differences** between countries.

### Global Impact
- **Top 5 countries by cases:** US, India, Brazil, Russia, Peru.
- **Top 5 countries by deaths:** US, Brazil, India, Mexico, UK.
- CFR vs total cases shows **mortality varies independently of case counts**.

### Socio-Economic Correlations
- **GDP per Capita vs Total Cases:** correlation ≈ 0.015 → almost no linear relationship.
- **HDI vs Total Deaths:** correlation ≈ 0.061 → very weak linear relationship.
- Insights: economic or development indicators alone **cannot explain pandemic outcomes**; other factors like population, healthcare quality, testing, and government response matter.

## Visualizations
- Line charts: cases & deaths over time (Poland vs Italy)
- Bar charts: top countries by cases, deaths, and CFR
- Scatter plots: GDP/HDI vs cases/deaths

## Key Learnings
- Pandemic impact is **uneven across countries**.
- Socio-economic indicators are **not sole predictors** of outcomes.
- Visualizations reveal patterns and outliers not obvious in raw data.
- Data-driven analysis can inform **public health strategies and policy**.

## Conclusion
COVID-19 outcomes are shaped by a **combination of epidemiological, socio-economic, and healthcare factors**. This project demonstrates the importance of **data cleaning, visualization, and interpretation** in understanding global health crises.
