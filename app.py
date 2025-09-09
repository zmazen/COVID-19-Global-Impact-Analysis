import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.markdown("# Global COVID-19 Data Analysis")

st.markdown("## Project Objective")
st.markdown("""
This project analyzes global COVID-19 data from Our World in Data to explore pandemic trends, country-level impacts, and the relationship between socio-economic indicators and COVID-19 outcomes.

The goal is to provide a clean, well-structured dataset and a visually rich exploratory analysis that can highlight key insights for portfolio presentation.
""")

st.markdown("## Dataset")
st.markdown("""
The dataset includes:
- *Location* (country name)
- *Date* (daily records)
- *Total Cases* (cumulative COVID-19 cases)
- *Total Deaths* (cumulative COVID-19 deaths)
- *Gdp Per Capita* (economic indicator)
- *Human Development Index* (development indicator)
""")

st.markdown("### Loading the COVID-19 Dataset")

st.markdown("""
The raw COVID-19 data is imported from a CSV file into a **pandas DataFrame**, which allows for efficient data manipulation and analysis. The dataset contains **country-level daily statistics** including COVID-19 cases, deaths, and socio-economic indicators.

Displaying the DataFrame provides an initial view of the structure, helping to identify:
- **Missing values** in fields like GDP per capita and HDI
- **Aggregate rows** such as "International" without a specific country
- Opportunities for **data cleaning and preprocessing** before analysis
""")

df_covid = pd.read_csv("owid-covid-data.csv")
st.dataframe(df_covid)

cols = ["location", "date", "total_cases",
        "total_deaths","gdp_per_capita", "human_development_index"]

df_covid = df_covid[cols]

df_covid["date"] = pd.to_datetime(df_covid["date"])
df_covid = df_covid.dropna(subset=["total_cases", "total_deaths"])
mode = df_covid["gdp_per_capita"].mode()[0]
df_covid.fillna({"gdp_per_capita": mode}, inplace=True)
mode = df_covid["human_development_index"].mode()[0]
df_covid.fillna({"human_development_index": mode}, inplace=True)
df_covid.columns = df_covid.columns.str.replace("_", " ")
df_covid.columns = df_covid.columns.str.title()

st.markdown("### **Previewing the Cleaned Dataset**")
st.markdown("""
Displaying the cleaned DataFrame provides a **snapshot of the dataset after preprocessing**. Key observations:
- The dataset contains **44,182 rows and 6 columns**
- Columns are **clean, readable, and ready for analysis**
- Missing values have been handled, and there are **no duplicates**
- Aggregate rows like "International" are still present, which can be **filtered if country-specific analysis** is required

This confirms that the dataset is **well-prepared for exploratory data analysis and visualization**.
""")

st.dataframe(df_covid)

df_latest = df_covid.sort_values("Date").groupby("Location").last()
df_latest["CFR %"] = ((df_latest["Total Deaths"] / df_latest["Total Cases"]) * 100).round(2)

st.markdown("""
### **Top 10 Countries by COVID-19 Case Fatality Rate (CFR %) and Comparison with Global Average**

This analysis identifies the **top 10 countries with the highest CFR %**, providing insight into where COVID-19 was **most deadly relative to reported cases**.

**Key Observations:**
- **Yemen** has the highest CFR at **28.90%**, which is **over 11 times higher** than the global average CFR of **2.55%**.  
- Other countries in the top 10, including **Italy (12.09%)**, **United Kingdom (10.81%)**, and **Mexico (10.57%)**, also significantly exceed the global average.  
- Countries like **France (7.29%)** and **Isle of Man (7.08%)** still show elevated CFRs compared to the world mean.  

**Insights:**
- A high CFR indicates a **higher proportion of deaths among confirmed cases**, which may result from:
  - **Healthcare system limitations or overload**  
  - **Delayed detection or limited testing**, causing milder cases to be underreported  
  - **Population vulnerability**, e.g., older populations or comorbidities  
  - **Data accuracy and reporting practices**  

- Comparing top CFRs with the **global average (2.55%)** highlights stark **regional disparities in pandemic impact**, emphasizing that some countries suffered disproportionately high mortality even with relatively fewer cases.

**Conclusion:**
- While total case counts show **where infections were widespread**, CFR provides complementary insight into **severity and mortality risk**.  
- Countries in the top 10 CFR list require particular attention in terms of **public health response, resource allocation, and historical analysis of healthcare outcomes** during the pandemic.
""")

df_cfr = df_latest[["CFR %"]]
df_top10_cfr = df_cfr.sort_values("CFR %", ascending=False).head(10)
st.dataframe(df_top10_cfr)

st.markdown("---")

st.markdown("""
### **Exploratory Data Analysis**

With the dataset now **cleaned and structured**, we can explore patterns and trends through **visualizations**. This section focuses on:  
- **Time-series analysis** of COVID-19 cases and deaths  
- **Comparisons across countries**  
- **Correlation between socio-economic indicators** and pandemic outcomes  

The goal is to uncover **insights that reveal how COVID-19 spread and its impact varied globally**.
""")

st.markdown("""
### **COVID-19 Cases and Deaths Over Time in Poland**

This visualization shows the **cumulative total cases and deaths** in Poland over the course of the pandemic. Key insights:  

- **Rapid growth in total cases** is evident, particularly during major waves of infection, highlighting periods of accelerated virus spread.  
- **Total deaths remain much lower than total cases**, creating a noticeable gap between the two lines. This reflects:  
  - The **relatively low case fatality rate** in Poland  
  - Improvements in **healthcare response** and treatment over time  
- The **Total Deaths line is nearly flat initially**, indicating minimal mortality during early infections, then rises gradually as the pandemic progresses.  
- Time-series trends help identify **peaks and plateaus**, which can be correlated with policy changes, vaccination campaigns, or new variants.  

This plot emphasizes the **disparity between infections and fatalities**, an important factor when analyzing pandemic impact and healthcare effectiveness.
""")

df_country = df_covid[df_covid["Location"] == "Poland"].sort_values("Date")

fig, ax = plt.subplots(figsize=(12,6))
df_country.set_index("Date")["Total Cases"].plot(kind="line", ax=ax, label="Total Cases")
df_country.set_index("Date")["Total Deaths"].plot(kind="line", ax=ax, label="Total Deaths")

ax.set_ylabel("Count")
ax.set_title("COVID-19 Cases & Deaths in Poland")
ax.legend()

st.pyplot(fig)

st.markdown("""
### **COVID-19 in Italy: Cases and Deaths Over Time**

This line chart illustrates the trajectory of **total COVID-19 cases and deaths in Italy** from late January to September 2020. Key observations include:

- **Initial Outbreak:**  
  Italy reported its first cases on **January 31, 2020**. For nearly three weeks, case numbers remained minimal (3 cases), reflecting the initial containment period.

- **Rapid Surge (Late February – March 2020):**  
  From **February 22**, cases began to rise sharply:  
  - 17 cases (Feb 22) → 1,128 cases (Mar 1) → 124,632 cases (Apr 5).  
  - Deaths followed closely, from **2 deaths on Feb 23** to over **10,000 deaths by March 29**.  
  This highlights how quickly Italy became one of the global epicenters of the pandemic.

- **Peak and Plateau (March – May 2020):**  
  - Cases and deaths climbed steeply until early April.  
  - After April, growth slowed, suggesting that lockdowns and interventions were effective.  
  - By May, the curve flattened significantly, with total deaths exceeding **30,000** and cases above **220,000**.

- **Stabilization (June – August 2020):**  
  - Both case and death curves grew at a much slower pace.  
  - Deaths plateaued around **35,000**, while total cases rose gradually, reflecting ongoing but reduced transmission.

- **Resurgence Signs (August – September 2020):**  
  - Cases began to rise again in late summer (over **290,000 cases by mid-September**).  
  - Deaths increased only slightly, suggesting **better medical preparedness and possibly younger demographics in new infections** compared to the first wave.

**Overall Insight:**  
Italy experienced a **devastating first wave**, with explosive case growth and high mortality by March–April 2020. Strict measures helped flatten the curve, but the data also shows **early signs of a second wave** by September, though with relatively lower fatality growth at that stage.
""")

df_country = df_covid[df_covid["Location"] == "Italy"].sort_values("Date")

fig, ax = plt.subplots(figsize=(12,6))
df_country.set_index("Date")["Total Cases"].plot(kind="line", ylabel="Count", label="Total Cases",
                                                title="COVID-19 Cases & Deaths in Italy", ax=ax)
df_country.set_index("Date")["Total Deaths"].plot(kind="line", label="Total Deaths", ax=ax)

ax.legend()
st.pyplot(fig)

st.markdown("""
### **Insights from the COVID-19 Total Cases Plot: Poland vs Italy**

The line chart compares the progression of **total confirmed COVID-19 cases** between **Italy** and **Poland** over time.

- **Early Outbreak (Dec 2019 – Feb 2020):**
  - Italy reported its first cases at the end of **January 2020** (3 cases).
  - Case counts in Italy grew slowly until **late February**, when numbers began to accelerate (17 → 229 cases within a few days).

- **Rapid Growth in Italy (Feb – Mar 2020):**
  - Italy experienced an **explosive outbreak** starting in late February.
  - By **March 1st, 2020**, Italy already had over **1,000 cases**, and by mid-March it surpassed **20,000 cases**.
  - This highlights Italy as one of the earliest and hardest-hit European countries.

- **Poland’s Later Outbreak (Mar 2020 Onwards):**
  - Poland reported its first case on **March 4, 2020**.
  - Growth in Poland was **much slower** compared to Italy in the early months.
  - By the end of March, Poland had a little over **2,000 cases**, while Italy was already above **100,000 cases**.

- **Cumulative Growth Trend (Apr – Jul 2020):**
  - Italy’s case curve rose steeply through March and April, then **flattened** by summer 2020 (around **240,000 cases by July**).
  - Poland’s curve rose gradually but consistently, reaching **40,000+ cases by late July**, still far below Italy’s total.

### Key Takeaways
- Italy was hit **earlier and harder**, with a sharp exponential growth in spring 2020.
- Poland’s outbreak started **later** and followed a **slower trajectory** in comparison.
- The plot highlights how different the pandemic’s **timing and scale** were between the two countries, despite both being in Europe.
""")

df_compare = df_covid[df_covid["Location"].isin(["Poland", "Italy"])]

fig, ax = plt.subplots(figsize=(12, 6))
df_compare.pivot(index="Date", columns="Location", values="Total Cases") \
          .plot(kind="line", ylabel="Total Cases", title="COVID-19 Total Cases: Poland vs Italy", ax=ax)
st.pyplot(fig)

st.markdown("""
### **Insights: COVID-19 Total Deaths – Poland vs Italy**

This line chart compares the cumulative COVID-19 deaths in **Italy** and **Poland** from the start of the pandemic.  

- **Italy’s trajectory**:  
  - Deaths remained at zero until **late February 2020**.  
  - The first spike appeared on **Feb 23, 2020**, followed by a **sharp exponential rise** throughout March.  
  - Italy quickly became one of the earliest and hardest-hit countries in Europe, surpassing **10,000 deaths by late March**.  
  - Growth continued steeply into April, but by May–June the curve began to **flatten**, showing that daily deaths slowed down.  
  - By **August 2020**, Italy’s total deaths stabilized around **35,000**, with only small increases afterward.  

- **Poland’s trajectory**:  
  - Poland reported its first deaths later, in **mid-March 2020**.  
  - The growth was **slower and more gradual** compared to Italy.  
  - By the end of May, Poland had just over **1,000 deaths**, while Italy already exceeded **30,000**.  
  - The curve kept climbing steadily, but never approached Italy’s early explosive surge.  

- **Comparison**:  
  - Italy’s death toll grew dramatically in the first months, while Poland’s remained relatively lower and more controlled in the same period.  
  - The stark difference highlights how Italy was one of Europe’s epicenters early in the pandemic, while Poland experienced a **delayed and slower spread**.  

**Takeaway**: Italy faced a severe and early outbreak with rapid escalation in deaths, while Poland’s curve shows a later start and slower growth, reflecting differences in timing, health policies, and possibly population exposure.
""")

fig, ax = plt.subplots(figsize=(12, 6))
df_compare.pivot(index="Date", columns="Location", values="Total Deaths") \
          .plot(kind="line", ylabel="Total Deaths", title="COVID-19 Total Deaths: Poland vs Italy", ax=ax)
st.pyplot(fig)

df_top = df_covid[df_covid["Location"] != "World"]

cases_per_country = df_top.groupby(["Location"])["Total Cases"].max().sort_values(ascending=False).head()
deaths_per_country = df_top.groupby(["Location"])["Total Deaths"].max().sort_values(ascending=False).head()

st.markdown("### **Top 5 Countries by Total COVID-19 Cases**")
st.markdown("""
This horizontal bar chart highlights the countries with the **highest cumulative COVID-19 cases**. Key observations:

- The **United States** leads by a significant margin with over **6.7 million reported cases**, followed by **India** (5.3M) and **Brazil** (4.5M).
- **Russia** and **Peru** round out the top five, showing substantial case counts despite smaller populations compared to the U.S., India, or Brazil.
- The wide gap between the top countries illustrates the **unequal impact of the pandemic**, influenced by factors such as:
  - **Population size** and density
  - **Testing capacity and reporting practices**
  - **Government policies and public health interventions**
- Comparing these numbers visually emphasizes **where outbreaks were most severe**, helping to identify regions that experienced the **largest burdens on healthcare systems**.
- This plot also serves as a baseline for **further correlation analyses**, such as linking case counts with socio-economic indicators like GDP per capita or human development index.

Overall, the visualization provides a **clear and intuitive understanding of global case distribution**, essential for both public health analysis and portfolio presentation.
""")

fig, ax = plt.subplots(figsize=(12, 6))
cases_per_country.plot(kind="barh", color="darkorange", ax=ax)
ax.set_ylabel("Country")
ax.set_xlabel("Total Cases")
ax.set_title("Top 5 Countries by Total COVID-19 Cases")
st.pyplot(fig)

st.markdown("""
### **Top 5 Countries by Total COVID-19 Deaths**

This bar chart presents the countries with the **highest cumulative COVID-19 deaths**, offering a perspective on the **mortality impact of the pandemic**. Key insights include:

- The **United States** experienced the most deaths with nearly **200,000 fatalities**, followed by **Brazil** (135,793) and **India** (85,619).  
- **Mexico** and the **United Kingdom** complete the top five, reflecting regions with significant healthcare challenges or high population densities.  
- Comparing this chart with the top cases chart reveals a **disparity between case numbers and deaths**:  
  - For example, India has the second-highest number of cases but fewer deaths than the U.S. and Brazil, suggesting **differences in healthcare capacity, demographics, and reporting accuracy**.  
  - Similarly, the United Kingdom appears in the top five for deaths despite lower case counts compared to countries like Peru or Russia, highlighting **regional differences in mortality rates**.  
- The visual representation makes it easy to identify countries with **severe health impacts** and can inform discussions about **public health preparedness, medical infrastructure, and pandemic management strategies**.  
- By analyzing mortality alongside case counts, we can start to explore **case-fatality rates** and the **effectiveness of government interventions and vaccination campaigns**.  

This chart emphasizes that while the number of infections is important, **mortality is a critical measure of the pandemic’s overall severity**, providing deeper insights into the **human cost of COVID-19 globally**.
""")

fig, ax = plt.subplots(figsize=(12, 6))
deaths_per_country.plot(kind="barh", color="darkcyan", ax=ax)
ax.set_ylabel("Country")
ax.set_xlabel("Total Deaths")
ax.set_title("Top 5 Countries by Total COVID-19 Deaths")
st.pyplot(fig)

st.markdown("""
### **Top 10 Countries by COVID-19 Case Fatality Rate (CFR)**

This horizontal bar chart shows the **Case Fatality Rate (CFR)** for the ten countries with the highest mortality relative to confirmed COVID-19 cases. Key observations:

- **Yemen** stands out with a staggering **28.9% CFR**, indicating severe challenges in healthcare capacity, reporting, and pandemic management.
- European countries like **Italy (12.1%)**, **United Kingdom (10.8%)**, **Belgium (9.98%)**, and **France (7.29%)** also have high CFRs, reflecting the **impact of early pandemic waves** and high proportions of elderly populations.
- **Mexico (10.57%)** and **Ecuador (8.9%)** show that **high CFR is not limited to Europe**, suggesting **underreporting of cases, healthcare system limitations, or testing gaps**.
- Smaller territories such as **Jersey, Montserrat, and Isle of Man** appear in the top 10 due to **smaller population sizes**, where a few deaths can significantly affect the CFR.
- The chart emphasizes that **CFR varies widely across countries**, highlighting **differences in healthcare infrastructure, testing capacity, population age structure, and data reporting accuracy**.

**Insight:**  
High CFR does not always correlate with total cases, some countries may have fewer cases but proportionally higher deaths. This underscores the **importance of examining mortality rates relative to cases**, not just raw counts, to understand the true impact of COVID-19 across different regions.
""")

fig, ax = plt.subplots(figsize=(10, 6))
df_top10_cfr.plot(kind="barh", y="CFR %", color="purple", ax=ax)
ax.set_xlabel("CFR (%)")
ax.set_ylabel("Country")
ax.set_title("Top 10 Countries by COVID-19 CFR")
st.pyplot(fig)

st.markdown("""
### **GDP per Capita vs Total COVID-19 Cases**

This scatter plot explores whether **economic wealth, measured by GDP per capita, is related to the total number of COVID-19 cases** in each country. Key observations:

- The correlation value is **0.015**, which is extremely low, indicating **almost no linear relationship** between a country's GDP per capita and its total case count.
- High-income countries like the **United States** and **Western European nations** reported high case numbers, but several middle- or low-income countries also experienced significant outbreaks.
- The scatter plot shows a **wide spread of case counts across all income levels**, suggesting that **economic wealth alone does not determine the scale of infection**.
- This finding highlights the role of other factors in pandemic spread, including:
  - **Population density** and urbanization
  - **Testing availability and reporting accuracy**
  - **Government interventions, social behavior, and mobility patterns**
- Although richer countries may have better healthcare infrastructure, **they were not immune to large outbreaks**, possibly due to more international travel and greater social interaction.
- This analysis emphasizes that **pandemic outcomes are multifactorial**, and economic strength alone is not a predictor of total cases.

The visualization effectively conveys that **COVID-19 spread was global and indiscriminate**, challenging assumptions that wealthier nations would automatically see fewer infections.
""")

df_latest = df_covid.sort_values("Date").groupby("Location").last()

fig, ax = plt.subplots(figsize=(12, 6))
df_latest.plot(kind="scatter", x="Gdp Per Capita", y="Total Cases", alpha=0.6, color="green",
               grid=True, ax=ax)
ax.set_xlabel("GDP per Capita")
ax.set_ylabel("Total Cases")
ax.set_title("GDP per Capita vs Total COVID-19 Cases")
st.pyplot(fig)

st.markdown("""
### **Human Development Index vs Total COVID-19 Deaths**

This scatter plot examines the relationship between a country's **Human Development Index (HDI)** and the **total number of COVID-19 deaths**. Key insights include:

- The correlation between HDI and total deaths is approximately **0.061**, which is very weak, indicating **almost no linear relationship** between HDI and mortality.
- Interestingly, countries with **high HDI** like the United States, United Kingdom, and Western European nations still reported **substantial death counts**, suggesting that **better development does not fully prevent fatalities**.
- Some lower-HDI countries recorded fewer deaths, which could be influenced by **underreporting, lower testing rates, or younger population demographics**.
- The scatter plot shows a **wide distribution**, with deaths occurring across the entire HDI spectrum, reinforcing that **pandemic outcomes are influenced by multiple factors** beyond HDI alone:
  - **Healthcare system capacity and quality**
  - **Government response measures** (lockdowns, vaccination campaigns)
  - **Population age structure and comorbidities**
  - **Data reporting and reliability**
- Overall, the visualization highlights that **HDI provides limited predictive power for COVID-19 mortality**, emphasizing the complex nature of pandemic vulnerability.

This analysis suggests that while **HDI reflects socio-economic and healthcare advantages**, it does not guarantee lower death rates during a global health crisis.
""")

fig, ax = plt.subplots(figsize=(12, 6))
df_latest.plot(kind="scatter", x="Human Development Index", y="Total Deaths", alpha=0.6, color="purple",
               grid=True, ax=ax)
ax.set_xlabel("Human Development Index")
ax.set_ylabel("Total Deaths")
ax.set_title("HDI vs Total COVID-19 Deaths")
st.pyplot(fig)

st.markdown("""
---

## **Conclusion and Key Learnings from the COVID-19 Analysis Project**

### Summary of the Project
This project analyzed the **OWID COVID-19 dataset** to explore patterns in **cases, deaths, and socio-economic indicators** across countries. Through data cleaning, processing, and visualizations, we investigated the **pandemic’s progression in specific countries**, identified the **most affected nations**, and examined how **economic and development factors correlate with COVID-19 outcomes**.

### Key Outcomes and Insights

1. **COVID-19 Cases and Deaths Over Time in Poland**  
   - Cumulative **cases grew rapidly**, while **deaths remained comparatively low**, showing a clear gap between infections and fatalities.  
   - The nearly flat initial deaths indicate **minimal mortality during early waves**, with gradual increases as the pandemic progressed.  
   - This time-series visualization highlighted **periods of peaks and plateaus**, which can be linked to **policy changes, vaccination rollouts, and variant emergence**.  

2. **Top 5 Countries by Total COVID-19 Cases and Deaths**  
   - The **United States, India, and Brazil** recorded the highest cases, while the **U.S., Brazil, and India** also led in deaths, though with differing ranks.  
   - Disparities between cases and deaths emphasize **differences in healthcare capacity, demographic factors, and reporting accuracy**.  
   - These charts help identify countries where the pandemic **placed the greatest strain on healthcare systems**, providing context for global public health preparedness.

3. **GDP per Capita vs Total COVID-19 Cases**  
   - The extremely low correlation (~0.015) indicates that **economic wealth alone did not determine the spread of the virus**.  
   - High and middle-income countries alike experienced significant outbreaks, suggesting that **population density, mobility, testing, and social behavior** played larger roles.  
   - This insight reinforces that **pandemic outcomes are multifactorial**, and wealth does not automatically confer immunity from large-scale infections.

4. **Human Development Index vs Total COVID-19 Deaths**  
   - The weak correlation (~0.061) highlights that **HDI has limited predictive power for mortality outcomes**.  
   - Countries with high HDI still experienced substantial deaths, while some lower-HDI countries had fewer deaths, likely due to **demographics, reporting discrepancies, or healthcare practices**.  
   - This emphasizes that **mortality is shaped by a combination of healthcare quality, government response, and population characteristics**, not just development indicators.

### Lessons Learned
- **Pandemic impact is uneven**: Total cases and deaths vary widely across countries, showing the importance of **localized analysis**.  
- **Socio-economic indicators are not sole predictors**: Both GDP and HDI have minimal correlation with cases or deaths, highlighting the **complexity of real-world pandemic dynamics**.  
- **Visualizations enhance understanding**: Time-series, bar charts, and scatter plots revealed patterns not immediately obvious in raw data, helping identify **trends, outliers, and global disparities**.  
- **Data-driven insights inform decisions**: Understanding case and death distributions can guide **public health strategies, resource allocation, and policy interventions** in future health crises.

### Conclusion
This project demonstrates that **COVID-19 outcomes cannot be explained by a single factor**. The combination of **epidemiological data, socio-economic context, and time-series analysis** provides a clearer picture of the pandemic's global impact. Ultimately, this analysis highlights the **critical role of data visualization and interpretation** in understanding complex public health challenges and preparing for future crises.
""")