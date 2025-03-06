import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Page layout
st.set_page_config(page_title="Load Profitability Analyzer", layout="wide")

def calculate_profitability(df):
    """Calculate financial and operational metrics for each load."""
    df['Total Revenue ($)'] = df['OTR Price ($)']
    df['Total Costs ($)'] = (
        df['Total Fuel Cost ($)'] +
        df['Driver Pay ($)'] +
        df['Dispatcher Fee ($)'] +
        df['Taxes ($)'] +
        df['Tolls ($)'] +
        df['Maintenance Cost ($)']
    )
    
    df['Profit ($)'] = df['Total Revenue ($)'] - df['Total Costs ($)']
    df['Profit per Mile ($)'] = df['Profit ($)'] / df['Total Miles'].replace(0, 1)
    df['Fuel Cost per Mile ($)'] = df['Total Fuel Cost ($)'] / df['Total Miles'].replace(0, 1)
    df['Driver Pay per Mile ($)'] = df['Driver Pay ($)'] / df['Total Miles'].replace(0, 1)
    df['Load Weight per Mile (lbs/mile)'] = df['Load Weight (lbs)'] / df['Total Miles'].replace(0, 1)
    
    return df

def convert_df_to_csv(df):
    """Convert df to csv."""
    return df.to_csv(index=False).encode('utf-8')

def convert_df_to_excel(df):
    """Convert df to Excel."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Profitability Analysis")
    return output.getvalue()

# Sidebar - File upload
st.sidebar.header("Upload Load Data")
uploaded_file = st.sidebar.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    # Read file
    df = pd.read_excel(uploaded_file)

    # Validate required columns
    required_columns = [
        'OTR Price ($)', 'Total Fuel Cost ($)', 'Driver Pay ($)', 'Dispatcher Fee ($)', 'Taxes ($)',
        'Tolls ($)', 'Maintenance Cost ($)', 'Total Miles', 'Load Weight (lbs)'
    ]
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}. Please upload a valid file.")
    else:
        df = calculate_profitability(df)

        # Display Summary of Metrics
        total_revenue = df['Total Revenue ($)'].sum()
        total_costs = df['Total Costs ($)'].sum()
        total_profit = df['Profit ($)'].sum()
        avg_profit_per_mile = df['Profit per Mile ($)'].mean()
        avg_fuel_cost_per_mile = df['Fuel Cost per Mile ($)'].mean()
        avg_driver_pay_per_mile = df['Driver Pay per Mile ($)'].mean()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Revenue", f"${total_revenue:,.2f}")
        col2.metric("Total Costs", f"${total_costs:,.2f}")
        col3.metric("Total Profit", f"${total_profit:,.2f}", delta=f"{(total_profit / total_revenue) * 100:.2f}%")

        col4, col5, col6 = st.columns(3)
        col4.metric("Average Profit per Mile", f"${avg_profit_per_mile:.2f}")
        col5.metric("Average Fuel Cost per Mile", f"${avg_fuel_cost_per_mile:.2f}")
        col6.metric("Average Driver Pay per Mile", f"${avg_driver_pay_per_mile:.2f}")

        # Data Overview
        st.subheader("Load Profitability Analysis")
        st.dataframe(df)

        # Profitable and Non-Profitable Loads
        profitable_loads = df[df['Profit ($)'] > 0]
        non_profitable_loads = df[df['Profit ($)'] <= 0]

        col7, col8 = st.columns(2)
        col7.subheader("Profitable Loads")
        col7.dataframe(profitable_loads)

        col8.subheader("Non-Profitable Loads")
        col8.dataframe(non_profitable_loads)

        # Visualization - Profitability Breakdown
        st.subheader("Profitability Breakdown")
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(df.index, df['Profit ($)'], color=['green' if x > 0 else 'red' for x in df['Profit ($)']])
        ax.set_xlabel("Load Index")
        ax.set_ylabel("Profit ($)")
        ax.set_title("Profitability by Load")
        st.pyplot(fig)

        # Visualization - Expense Breakdown
        st.subheader("Expense Breakdown")
        expense_columns = ['Total Fuel Cost ($)', 'Driver Pay ($)', 'Dispatcher Fee ($)', 'Taxes ($)', 'Tolls ($)', 'Maintenance Cost ($)']
        expense_totals = df[expense_columns].sum()

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.pie(expense_totals, labels=expense_columns, autopct='%1.1f%%', startangle=140)
        ax.set_title("Expense Breakdown")
        st.pyplot(fig)

        # Download Section
        st.subheader("Download Results")
        col9, col10 = st.columns(2)
        col9.download_button("Download as CSV", data=convert_df_to_csv(df), file_name="profitability_analysis.csv", mime="text/csv")
        col10.download_button("Download as Excel", data=convert_df_to_excel(df), file_name="profitability_analysis.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

else:
    st.info("Upload an Excel file to start analysis.")
