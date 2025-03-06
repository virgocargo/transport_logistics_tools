# Transport & Logistics Tools  

This repo contains essential apps for trucking professionals in logistics:  

1. **Load Calculator App** – A GUI tool for evaluating potential loads based on distance, expenses, and profit.  
2. **Load Profitability Analyzer** – A data-driven web app for analyzing load profitability using data visualizations.  

These tools aim to help logistics professionals, fleet managers, and owner-operators** make data-driven decisions for better profitability and efficiency.

## **Create Virtual Environment**
Before running any python script, to avoid dependency conflicts, set up a virtual environment (you only need to create it once):

*Note: You can name the virtual environment anything you want. If you work with multiple virtual environments in a common development folder, consider adding a date or project name (e.g., venv_030524 or loadcalc_venv). However, for projects that keep one virtual environment per folder, simply using venv is fine.*

For Windows (in CMD or PowerShell):
```sh
python -m venv venv
venv\Scripts\activate
```

For macOS & Linux (in Terminal):
```sh
python3 -m venv venv
source venv/bin/activate
```
Once activated, your terminal prompt should show *(venv)*.

## Pre-Reqs:
For this script to work properly, please ensure you have Python *3.12.3* installed or higher. 

## **Clone Repo**
```sh
git clone https://github.com/virgocargo/transport_logistics_tools.git
```

## 1. Load Calculator App 

This Python GUI app helps truck operators and logistics professionals evaluate potential loads by calculating total miles, rate per mile, expenses, and net profit.

### Features:
- **Load Entry Form**: Input *origin, destination, load pay, and deadhead miles*.
- **Automated Calculations**:
  - Determines *total distance*, including deadhead miles.
  - Calculates *rate per mile, fuel costs, dispatcher fees, maintenance, tolls, and net profit*.
- **Dynamic Distance Handling**:
  - Uses a built-in distance dictionary for common routes.
  - Allows manual distance input for unknown routes.
- **Data Management**:
  - Keeps track of *loads under consideration*.
  - Supports booking confirmed loads.
- **User-Friendly Interface**:
  - Built with Tkinter for an intuitive experience.
  - Uses message boxes for results and errors instead of cluttered windows.

### **Run**
```sh
python load_calculator.py
```

## 2. Load Profitability Analyzer 

This is a web tool that helps trucking businesses analyze load profitability, providing insights into total revenue, costs, fuel efficiency, driver pay, and profit per mile, along with data visualization for better decision-making.

### Features:
- Upload and analyze files containing load data.
- Calculate profit per mile, fuel costs, driver pay, and operational expenses.
- Visualize profitability trends with bar charts and expense breakdowns.
- Identify profitable vs. non-profitable loads to optimize future routes.
- Export processed data (in CSV or Excel format).

### **Run**
```sh
streamlit run load_profitability_analyzer.py
```



