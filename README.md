# 🔧 Reducing CO Emissions in Turbine Output

This consulting project analyzes turbine sensor data to recommend engineering adjustments that reduce carbon monoxide (CO) emissions in a Turkish power plant. Using a mix of linear and non-linear modeling, we identify the most impactful controllable variables and provide actionable engineering guidance.

## 📌 Project Scope

- **Client**: Man Fung Leung
- **Course**: STAT 443 – Statistical Consulting
- **Goal**: Recommend optimal settings for turbine parameters to minimize CO emissions
- **Data**: 7,158 observations of ambient and internal turbine sensor readings from UCI repository

## ⚙️ Methods Used
- Linear Regression
- LASSO Regression (with Bootstrap CI)
- Decision Trees
- Random Forest (best performer)
- Train-test split (80:20)
- Model evaluation using RMSE, MAE, R²

## 🛠 Controllable Variables
- AFDP: Air Filter Difference Pressure  
- GTEP: Gas Turbine Exhaust Pressure  
- TIT: Turbine Inlet Temperature  
- TAT: Turbine After Temperature  
- CDP: Compressor Discharge Pressure  

Ambient variables like AT, AP, AH, and TEY were considered but not manipulated in recommendations.

## 📊 Key Results

| Model           | RMSE (Overall) | R² (Overall) | MAE (Overall) |
|----------------|----------------|--------------|----------------|
| Linear         | 0.721          | 0.618        | 0.493          |
| LASSO          | 0.719          | 0.619        | 0.491          |
| Decision Tree  | 0.603          | 0.732        | 0.374          |
| **Random Forest** | **0.504**  | **0.813**    | **0.313**      |

Random forest consistently outperformed other models in overall, medium, and high energy load subsets.

## 🧠 Final Recommendations

**Overall Load**:
- Keep **CDP > 12 mbar**
- Keep **TIT > 1085°C**

**Medium Load (TEY 130–136)**:
- **AFDP ≤ 3.6 mbar**
- **TIT > 1088°C**
- **GTEP ≈ 25 mbar**

**High Load (TEY > 160)**:
- **AFDP ≈ 4.4 mbar**
- **GTEP ≈ 33.5 mbar**

## 📁 Repository Contents
- `Group7ConsultingProjectReport.pdf`: Full consulting report
- `STAT443_Project.Rmd`: All modeling workflows in R
- `Stat443BootstrapLasso.Rmd`: LASSO with bootstrapping
- `OutlierSearching.Rmd`: Influence diagnostics
- `stat443_consulting_project_introductory_analysis.py`: Initial EDA and RF models

## 👥 Contributors
- Kashyap Ava  
- Mitchell Cappel  
- Christopher Cebra  
- Kris Png

---

*Project completed as part of UIUC's STAT 443 Statistical Consulting course.*
