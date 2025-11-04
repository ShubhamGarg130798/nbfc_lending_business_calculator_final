import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

PASSWORD = "nbfcsecure123"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Enter password to access dashboard:", type="password")
    if password == PASSWORD:
        st.session_state.authenticated = True
        st.success("Access granted. Welcome!")
        st.rerun()
    elif password:
        st.error("Incorrect password")
    st.stop()

# Set page config
st.set_page_config(
    page_title="NBFC Lending Business Calculator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Dashboard CSS
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* Global Styles */
* {
    font-family: 'Inter', sans-serif;
}

/* Main app background */
.stApp {
    background: linear-gradient(135deg, #f8fafc 0%, #edf2f7 100%);
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main content area */
.main .block-container {
    padding: 1.5rem 2.5rem;
    max-width: 1600px;
}

/* Dashboard Header */
.dashboard-header {
    background: linear-gradient(135deg, #2b6cb0 0%, #2c5282 100%);
    padding: 2.5rem 3rem;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(43, 108, 176, 0.2);
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
}

.dashboard-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
    border-radius: 50%;
}

.dashboard-header::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: -5%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 70%);
    border-radius: 50%;
}

.dashboard-title {
    font-size: 2.25rem;
    font-weight: 800;
    color: white;
    margin: 0;
    text-shadow: 0 2px 8px rgba(0,0,0,0.15);
    position: relative;
    z-index: 1;
    letter-spacing: -0.5px;
}

.dashboard-subtitle {
    font-size: 1.125rem;
    color: rgba(255,255,255,0.95);
    margin: 0.75rem 0 0 0;
    font-weight: 500;
    position: relative;
    z-index: 1;
}

/* Section Headers */
.section-header {
    font-size: 1.5rem;
    font-weight: 800;
    color: #1a365d;
    margin: 3rem 0 1.5rem 0;
    padding-bottom: 1rem;
    border-bottom: 3px solid #e2e8f0;
    position: relative;
    letter-spacing: -0.5px;
}

.section-header::before {
    content: '';
    position: absolute;
    bottom: -3px;
    left: 0;
    width: 80px;
    height: 3px;
    background: linear-gradient(90deg, #2b6cb0, #4299e1);
}

/* KPI Card Styles - Modern Dashboard Look */
.kpi-card {
    background: white;
    border-radius: 14px;
    padding: 1.5rem 1.75rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.03);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    height: 100%;
    border-left: 5px solid var(--card-color);
    position: relative;
    border: 1px solid #f7fafc;
}

.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 28px rgba(0,0,0,0.12), 0 4px 8px rgba(0,0,0,0.08);
    border-color: var(--card-color);
}

.kpi-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
}

.kpi-icon {
    width: 42px;
    height: 42px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    background: var(--card-bg);
}

.kpi-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #718096;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.4rem;
}

.kpi-value {
    font-size: 1.75rem;
    font-weight: 800;
    color: var(--card-color);
    margin: 0;
    line-height: 1.2;
}

.kpi-trend {
    font-size: 0.8125rem;
    font-weight: 600;
    color: #48bb78;
    margin-top: 0.4rem;
}

/* Color Variables for KPI Cards */
.kpi-card.blue {
    --card-color: #3182ce;
    --card-bg: rgba(49, 130, 206, 0.1);
}

.kpi-card.green {
    --card-color: #38a169;
    --card-bg: rgba(56, 161, 105, 0.1);
}

.kpi-card.orange {
    --card-color: #dd6b20;
    --card-bg: rgba(221, 107, 32, 0.1);
}

.kpi-card.purple {
    --card-color: #805ad5;
    --card-bg: rgba(128, 90, 213, 0.1);
}

.kpi-card.teal {
    --card-color: #319795;
    --card-bg: rgba(49, 151, 149, 0.1);
}

/* Chart Container */
.chart-container {
    background: white;
    border-radius: 14px;
    padding: 1.75rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.03);
    margin: 1.5rem 0;
    border: 1px solid #f7fafc;
}

.chart-title {
    font-size: 1.125rem;
    font-weight: 700;
    color: #1a365d;
    margin-bottom: 1rem;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2c5282 0%, #2a4365 100%);
    padding: 0;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 1.5rem 1.25rem;
}

/* Sidebar Title */
[data-testid="stSidebar"] h1 {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 1.125rem !important;
    margin-bottom: 1.5rem !important;
    padding: 1rem !important;
    background: rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    text-align: center !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

/* Sidebar Text */
[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* Sidebar Expanders */
[data-testid="stSidebar"] details summary {
    background: rgba(255, 255, 255, 0.12) !important;
    border-radius: 10px !important;
    padding: 0.875rem 1rem !important;
    margin: 0.5rem 0 !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    font-weight: 600 !important;
    font-size: 0.9375rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}

[data-testid="stSidebar"] details summary:hover {
    background: rgba(255, 255, 255, 0.18) !important;
    border-color: rgba(255, 255, 255, 0.25) !important;
}

[data-testid="stSidebar"] details[open] {
    background: rgba(255, 255, 255, 0.05) !important;
    border-radius: 10px !important;
    padding: 0.5rem !important;
    margin: 0.5rem 0 !important;
}

/* Sidebar Labels */
[data-testid="stSidebar"] label {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    margin-bottom: 0.5rem !important;
}

/* Sidebar Inputs */
[data-testid="stSidebar"] input[type="number"] {
    background: rgba(255, 255, 255, 0.95) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    color: #2d3748 !important;
    border-radius: 8px !important;
    padding: 0.625rem !important;
    font-weight: 600 !important;
    font-size: 0.9375rem !important;
}

[data-testid="stSidebar"] input[type="number"]:focus {
    border-color: #4299e1 !important;
    box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2) !important;
    background: rgba(255, 255, 255, 1) !important;
}

/* Sidebar Buttons */
[data-testid="stSidebar"] button {
    background: rgba(66, 153, 225, 0.2) !important;
    color: #ffffff !important;
    border-radius: 6px !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

[data-testid="stSidebar"] button:hover {
    background: rgba(66, 153, 225, 0.3) !important;
}

/* Success/Error Messages */
[data-testid="stSidebar"] .stSuccess {
    background: rgba(72, 187, 120, 0.15) !important;
    border-left: 4px solid #48bb78 !important;
    border-radius: 8px !important;
    padding: 0.75rem !important;
    color: #c6f6d5 !important;
}

[data-testid="stSidebar"] .stError {
    background: rgba(245, 101, 101, 0.15) !important;
    border-left: 4px solid #f56565 !important;
    border-radius: 8px !important;
    padding: 0.75rem !important;
    color: #fed7d7 !important;
}

/* Table Styling */
[data-testid="stDataFrame"] {
    background: white !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.03) !important;
    overflow: hidden !important;
    border: 1px solid #f7fafc !important;
}

[data-testid="stDataFrame"] thead tr th {
    background: linear-gradient(135deg, #2b6cb0 0%, #2c5282 100%) !important;
    color: white !important;
    font-weight: 700 !important;
    padding: 1.125rem !important;
    font-size: 0.875rem !important;
    border: none !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

[data-testid="stDataFrame"] tbody tr:hover {
    background: #f7fafc !important;
}

[data-testid="stDataFrame"] tbody td {
    color: #4a5568 !important;
    padding: 0.875rem !important;
    border-bottom: 1px solid #e2e8f0 !important;
    font-size: 0.875rem !important;
}

/* Plotly Charts */
[data-testid="stPlotlyChart"] {
    background: white !important;
    border-radius: 14px !important;
    padding: 1.5rem !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.03) !important;
    border: 1px solid #f7fafc !important;
}

/* Summary Section */
.summary-box {
    background: linear-gradient(135deg, #ffffff 0%, #fafbfc 100%);
    border-radius: 14px;
    padding: 2rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.03);
    margin: 1.5rem 0;
    border: 1px solid #e2e8f0;
}

.summary-title {
    font-size: 1.5rem;
    font-weight: 800;
    color: #1a365d;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 3px solid #e2e8f0;
    letter-spacing: -0.5px;
    position: relative;
}

.summary-title::before {
    content: '';
    position: absolute;
    bottom: -3px;
    left: 0;
    width: 80px;
    height: 3px;
    background: linear-gradient(90deg, #2b6cb0, #4299e1);
}

/* Summary Metric Cards */
.summary-metric-card {
    background: white;
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
    border: 1px solid #f7fafc;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.summary-metric-card:hover {
    transform: translateX(4px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.summary-metric-icon {
    width: 48px;
    height: 48px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    flex-shrink: 0;
}

.summary-metric-label {
    font-size: 0.8125rem;
    font-weight: 600;
    color: #718096;
    margin-bottom: 0.25rem;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}

.summary-metric-value {
    font-size: 1.5rem;
    font-weight: 800;
    line-height: 1.2;
}

.stMarkdown p {
    color: #4a5568 !important;
    font-size: 0.9375rem !important;
    line-height: 1.75 !important;
}

.stMarkdown strong {
    color: #2d3748 !important;
    font-weight: 700 !important;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .dashboard-header {
        padding: 1.5rem 1.25rem;
    }
    
    .dashboard-title {
        font-size: 1.5rem;
    }
    
    .kpi-card {
        margin-bottom: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)

# Dashboard Header
st.markdown("""
<div class="dashboard-header">
    <div class="dashboard-title">💰 NBFC Lending Business Calculator</div>
    <div class="dashboard-subtitle">Real-time financial projections and business insights • Investor Presentation</div>
</div>
""", unsafe_allow_html=True)

# Sidebar for all inputs with collapsible sections
st.sidebar.markdown("# 🎛️ Input Parameters")

# Projection Period
with st.sidebar.expander("📅 Projection Period", expanded=True):
    num_months = st.number_input("Number of Months", min_value=1, max_value=48, value=12, step=1)

# Capital Deployment Parameters
with st.sidebar.expander("💰 Capital Deployment (₹ Crores)", expanded=False):
    capital_values = []
    if num_months <= 12:
        cap_col1, cap_col2 = st.columns(2)
        for i in range(num_months):
            month_num = i + 1
            if month_num <= 5:
                default_val = [5.0, 4.0, 4.0, 4.0, 3.0][i] if month_num <= 5 else 0.0
            else:
                default_val = 0.0
                
            if i % 2 == 0:
                with cap_col1:
                    val = st.number_input(f"Month {month_num}", min_value=0.0, max_value=20.0, value=default_val, step=0.5, key=f"cap_{month_num}")
            else:
                with cap_col2:
                    val = st.number_input(f"Month {month_num}", min_value=0.0, max_value=20.0, value=default_val, step=0.5, key=f"cap_{month_num}")
            capital_values.append(val)
    else:
        for i in range(num_months):
            month_num = i + 1
            if month_num <= 5:
                default_val = [5.0, 4.0, 4.0, 4.0, 3.0][i]
            else:
                default_val = 0.0
            val = st.number_input(f"Month {month_num}", min_value=0.0, max_value=20.0, value=default_val, step=0.5, key=f"cap_{month_num}")
            capital_values.append(val)

for i in range(48):
    if i < len(capital_values):
        globals()[f"month{i+1}_capital"] = capital_values[i]
    else:
        globals()[f"month{i+1}_capital"] = 0.0

total_capital = sum(capital_values)

# Business Parameters
with st.sidebar.expander("📈 Revenue Parameters", expanded=False):
    processing_fees = st.number_input("Processing Fees (%)", min_value=0.0, max_value=25.0, value=11.8, step=0.1) / 100
    monthly_interest_rate = st.number_input("Monthly Interest Rate (%)", min_value=0.0, max_value=50.0, value=30.0, step=0.5) / 100
    marketing_rate = st.number_input("Marketing Expenses (%)", min_value=0.0, max_value=10.0, value=2.0, step=0.1) / 100
    cost_of_funds_rate = st.number_input("Cost of Funds (% monthly)", min_value=0.0, max_value=10.0, value=1.5, step=0.1) / 100

# Operational expense rates
with st.sidebar.expander("🏢 Operational Expenses (%)", expanded=False):
    opex_month1_value = st.number_input("Month 1 OpEx (₹)", 0, 5000000, 1500000, 50000)
    opex_month1 = opex_month1_value / 1e7

    opex_values = [opex_month1]
    for i in range(1, num_months):
        month_num = i + 1
        if month_num <= 3:
            default_val = 10.0
        elif month_num <= 6:
            default_val = 5.0
        else:
            default_val = 4.0
        val = st.number_input(f"Month {month_num} OpEx Rate (%)", min_value=0.0, max_value=30.0, value=default_val, step=0.5, key=f"opex_{month_num}") / 100
        opex_values.append(val)

for i in range(48):
    if i < len(opex_values):
        globals()[f"opex_month{i+1}"] = opex_values[i]
    else:
        globals()[f"opex_month{i+1}"] = 0.04

# Loan parameters
with st.sidebar.expander("🎯 Loan Parameters", expanded=False):
    avg_ticket_size = st.number_input("Average Loan Ticket (₹)", 10000, 50000, 22000, 1000)

# Collection parameters
with st.sidebar.expander("📊 Collection Parameters", expanded=False):
    t0_collection = st.number_input("T+0 Collection Rate (%)", min_value=0, max_value=100, value=80, step=1) / 100
    t30_collection = st.number_input("T+30 Collection Rate (%)", min_value=0, max_value=100, value=5, step=1) / 100
    t60_collection = st.number_input("T+60 Collection Rate (%)", min_value=0, max_value=100, value=5, step=1) / 100
    t90_collection = st.number_input("T+90 Collection Rate (%)", min_value=0, max_value=100, value=3, step=1) / 100

    total_collection_rate_percent = (t0_collection + t30_collection + t60_collection + t90_collection) * 100
    if total_collection_rate_percent > 100:
        st.error(f"⚠️ Total collection rate is {total_collection_rate_percent:.1f}% - should not exceed 100%")
    else:
        st.success(f"✅ Total collection rate: {total_collection_rate_percent:.1f}%")

    api_cost_80_percent = st.number_input("API Cost (Per Lead Not Converted) ₹", 0, 100, 35, 5)
    api_cost_20_percent = st.number_input("API Cost (Per Converted Customers) ₹", 0, 150, 95, 5)

# Principal Return
with st.sidebar.expander("💳 Monthly Principal Return (₹ Crores)", expanded=False):
    principal_values = []
    if num_months <= 12:
        prin_col1, prin_col2 = st.columns(2)
        for i in range(num_months):
            month_num = i + 1
            if i % 2 == 0:
                with prin_col1:
                    val = st.number_input(f"Month {month_num} PR", min_value=0.0, value=0.0, step=0.1, key=f"prin_{month_num}")
            else:
                with prin_col2:
                    val = st.number_input(f"Month {month_num} PR", min_value=0.0, value=0.0, step=0.1, key=f"prin_{month_num}")
            principal_values.append(val)
    else:
        for i in range(num_months):
            month_num = i + 1
            val = st.number_input(f"Month {month_num} PR", min_value=0.0, value=0.0, step=0.1, key=f"prin_{month_num}")
            principal_values.append(val)

for i in range(48):
    if i < len(principal_values):
        globals()[f"month{i+1}_principal"] = principal_values[i]
    else:
        globals()[f"month{i+1}_principal"] = 0.0

# Calculation function
def calculate_with_exact_formulas():
    months = num_months
    capital_invested = [capital_values[i] * 1e7 if i < len(capital_values) else 0 for i in range(months)]
    opex_rates = [opex_values[i] if i < len(opex_values) else 0.04 for i in range(months)]
    principal_returns = [principal_values[i] * 1e7 if i < len(principal_values) else 0 for i in range(months)]
    
    amount_invested = []
    amount_available = []
    amount_disbursed = []
    customers = []
    opex = []
    api_expense = []
    marketing_expense = []
    cost_of_funds = []
    bad_debt_default = []
    gst = []
    salary = []
    principal_return = []
    interest_revenue = []
    bad_debt_recovery = []
    processing_fees_revenue = []
    profit_loss = []
    aum = []
    
    for month in range(months):
        amount_invested.append(capital_invested[month])
        
        if month == 0:
            available = capital_invested[month]
        else:
            prev_profit = profit_loss[month-1]
            available = amount_available[month-1] + prev_profit + capital_invested[month]
        
        amount_available.append(available)
        disbursed = available / (1 - processing_fees)
        amount_disbursed.append(disbursed)
        
        num_customers = int(disbursed / avg_ticket_size)
        customers.append(num_customers)
        
        if month == 0:
            op_expense = opex_month1_value
        else:
            prev_aum = aum[month-1]
            op_expense = prev_aum * opex_rates[month]
        
        opex.append(op_expense)
        
        api_cost = (num_customers * 2 * api_cost_20_percent) + (num_customers * 8 * api_cost_80_percent)
        api_expense.append(api_cost)
        
        marketing_exp = disbursed * marketing_rate
        marketing_expense.append(marketing_exp)
        
        cost_of_funds_expense = 0
        if month == 2 and months >= 3:
            cost_q1_m1 = capital_invested[0] * cost_of_funds_rate
            cost_q1_m2 = sum(capital_invested[:2]) * cost_of_funds_rate  
            cost_q1_m3 = sum(capital_invested[:3]) * cost_of_funds_rate
            cost_of_funds_expense = cost_q1_m1 + cost_q1_m2 + cost_q1_m3
        elif month == 5 and months >= 6:
            cost_q2_m4 = sum(capital_invested[:4]) * cost_of_funds_rate
            cost_q2_m5 = sum(capital_invested[:5]) * cost_of_funds_rate
            cost_q2_m6 = sum(capital_invested[:6]) * cost_of_funds_rate
            cost_of_funds_expense = cost_q2_m4 + cost_q2_m5 + cost_q2_m6
        elif month == 8 and months >= 9:
            cost_q3_m7 = sum(capital_invested[:7]) * cost_of_funds_rate
            cost_q3_m8 = sum(capital_invested[:8]) * cost_of_funds_rate
            cost_q3_m9 = sum(capital_invested[:9]) * cost_of_funds_rate
            cost_of_funds_expense = cost_q3_m7 + cost_q3_m8 + cost_q3_m9
        elif month == 11 and months >= 12:
            cost_q4_m10 = sum(capital_invested[:10]) * cost_of_funds_rate
            cost_q4_m11 = sum(capital_invested[:11]) * cost_of_funds_rate
            cost_q4_m12 = sum(capital_invested[:12]) * cost_of_funds_rate
            cost_of_funds_expense = cost_q4_m10 + cost_q4_m11 + cost_q4_m12
        elif (month + 1) % 3 == 0 and month >= 2 and months > month:
            quarter_start = month - 2
            cost_q_m1 = sum(capital_invested[:quarter_start+1]) * cost_of_funds_rate
            cost_q_m2 = sum(capital_invested[:quarter_start+2]) * cost_of_funds_rate
            cost_q_m3 = sum(capital_invested[:quarter_start+3]) * cost_of_funds_rate
            cost_of_funds_expense = cost_q_m1 + cost_q_m2 + cost_q_m3
        
        cost_of_funds.append(cost_of_funds_expense)
        
        if month == 0:
            interest = (disbursed * monthly_interest_rate) / 2
        else:
            current_month_interest = (disbursed * monthly_interest_rate) / 2
            prev_month_interest = (amount_disbursed[month-1] * monthly_interest_rate) / 2
            interest = current_month_interest + prev_month_interest
        
        interest_revenue.append(interest)
        
        bad_debt = (disbursed + interest) * (1 - t0_collection)
        bad_debt_default.append(bad_debt)
        
        recovery = 0
        if month >= 1:
            prev_disbursed_plus_interest = amount_disbursed[month-1] + interest_revenue[month-1]
            recovery += prev_disbursed_plus_interest * t30_collection
        if month >= 2:
            prev2_disbursed_plus_interest = amount_disbursed[month-2] + interest_revenue[month-2]
            recovery += prev2_disbursed_plus_interest * t60_collection
        if month >= 3:
            prev3_disbursed_plus_interest = amount_disbursed[month-3] + interest_revenue[month-3]
            recovery += prev3_disbursed_plus_interest * t90_collection
        
        bad_debt_recovery.append(recovery)
        
        pf = disbursed * processing_fees
        processing_fees_revenue.append(pf)
        
        gst_amount = pf * (18/118)
        gst.append(gst_amount)
        
        monthly_salary = 0
        salary.append(monthly_salary)
        principal_return.append(principal_returns[month])
        
        profit = (interest + recovery + pf) - (op_expense + api_cost + marketing_exp + cost_of_funds_expense + bad_debt + gst_amount + monthly_salary + principal_returns[month])
        profit_loss.append(profit)
        
        current_disbursed_interest = disbursed + interest
        
        if month >= 1:
            prev_disbursed_interest = amount_disbursed[month-1] + interest_revenue[month-1]
        else:
            prev_disbursed_interest = 0
            
        if month >= 2:
            prev2_disbursed_interest = amount_disbursed[month-2] + interest_revenue[month-2]
        else:
            prev2_disbursed_interest = 0
            
        if month >= 3:
            prev3_disbursed_interest = amount_disbursed[month-3] + interest_revenue[month-3]
        else:
            prev3_disbursed_interest = 0
            
        aum_value = (current_disbursed_interest + 
                    prev_disbursed_interest * 0.15 + 
                    prev2_disbursed_interest * 0.10 + 
                    prev3_disbursed_interest * 0.03)
        aum.append(aum_value)
    
    df = pd.DataFrame({
        'month': range(1, months + 1),
        'amount_invested': [x/1e7 for x in amount_invested],
        'amount_available': [x/1e7 for x in amount_available],
        'amount_disbursed': [x/1e7 for x in amount_disbursed],
        'customers': customers,
        'opex': [x/1e7 for x in opex],
        'api_expense': [x/1e7 for x in api_expense],
        'marketing_expense': [x/1e7 for x in marketing_expense],
        'cost_of_funds': [x/1e7 for x in cost_of_funds],
        'bad_debt_default': [x/1e7 for x in bad_debt_default],
        'gst': [x/1e7 for x in gst],
        'salary': [x/1e7 for x in salary],
        'principal_return': [x/1e7 for x in principal_return],
        'interest_revenue': [x/1e7 for x in interest_revenue],
        'bad_debt_recovery': [x/1e7 for x in bad_debt_recovery],
        'processing_fees_revenue': [x/1e7 for x in processing_fees_revenue],
        'profit_loss': [x/1e7 for x in profit_loss],
        'aum': [x/1e7 for x in aum]
    })
    
    return df

# Calculate metrics
sum_annual_investment = 0
for i, capital in enumerate(capital_values):
    months_remaining = num_months - i
    weight = months_remaining / num_months
    sum_annual_investment += capital * weight

df = calculate_with_exact_formulas()

final_month_aum = df['aum'].iloc[-1]
if sum_annual_investment > 0:
    period_roi = ((final_month_aum - sum_annual_investment) / sum_annual_investment) * 100
else:
    period_roi = 0

# Key Performance Indicators
st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card blue">
        <div class="kpi-header">
            <div>
                <div class="kpi-label">Capital Invested</div>
            </div>
            <div class="kpi-icon">💰</div>
        </div>
        <div class="kpi-value">₹{total_capital:.1f} Cr</div>
        <div class="kpi-trend">Total deployment</div>
    </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown(f"""
    <div class="kpi-card green">
        <div class="kpi-header">
            <div>
                <div class="kpi-label">Period ROI</div>
            </div>
            <div class="kpi-icon">📈</div>
        </div>
        <div class="kpi-value">{period_roi:.1f}%</div>
        <div class="kpi-trend">{num_months} months</div>
    </div>
    """, unsafe_allow_html=True)
    
with col3:
    final_month_disbursed = df['amount_disbursed'].iloc[-1]
    st.markdown(f"""
    <div class="kpi-card purple">
        <div class="kpi-header">
            <div>
                <div class="kpi-label">Month {num_months} Disbursed</div>
            </div>
            <div class="kpi-icon">📊</div>
        </div>
        <div class="kpi-value">₹{final_month_disbursed:.2f} Cr</div>
        <div class="kpi-trend">Latest month</div>
    </div>
    """, unsafe_allow_html=True)
    
with col4:
    total_profit_loss = df['profit_loss'].sum()
    st.markdown(f"""
    <div class="kpi-card orange">
        <div class="kpi-header">
            <div>
                <div class="kpi-label">Total Profit/Loss</div>
            </div>
            <div class="kpi-icon">🎯</div>
        </div>
        <div class="kpi-value">₹{total_profit_loss:.2f} Cr</div>
        <div class="kpi-trend">{num_months} months cumulative</div>
    </div>
    """, unsafe_allow_html=True)
    
with col5:
    final_month_aum = df['aum'].iloc[-1]
    st.markdown(f"""
    <div class="kpi-card teal">
        <div class="kpi-header">
            <div>
                <div class="kpi-label">Month {num_months} AUM</div>
            </div>
            <div class="kpi-icon">🏆</div>
        </div>
        <div class="kpi-value">₹{final_month_aum:.2f} Cr</div>
        <div class="kpi-trend">Assets under management</div>
    </div>
    """, unsafe_allow_html=True)

# Charts Section
st.markdown('<div class="section-header">Business Analysis Charts</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig_aum_growth = px.area(
        df, x='month', y='aum',
        title="Assets Under Management (AUM) Growth",
        color_discrete_sequence=['#4299e1']
    )
    fig_aum_growth.update_layout(
        xaxis_title="Month", yaxis_title="AUM (₹ Crores)",
        height=400, template="plotly_white",
        title_font=dict(size=16, color='#2d3748', family='Inter'),
        font=dict(family='Inter', size=12)
    )
    fig_aum_growth.update_xaxes(dtick=1)
    st.plotly_chart(fig_aum_growth, use_container_width=True)

with col2:
    fig_revenue_costs = go.Figure()
    total_revenue = df['interest_revenue'] + df['processing_fees_revenue'] + df['bad_debt_recovery']
    total_costs = (df['opex'] + df['api_expense'] + df['marketing_expense'] + 
                   df['cost_of_funds'] + df['bad_debt_default'] + df['gst'] + 
                   df['salary'] + df['principal_return'])

    fig_revenue_costs.add_trace(go.Bar(
        x=df['month'], y=total_revenue, name='Total Revenue',
        marker_color='#38a169'
    ))
    fig_revenue_costs.add_trace(go.Bar(
        x=df['month'], y=total_costs, name='Total Costs',
        marker_color='#f56565'
    ))
    fig_revenue_costs.add_trace(go.Scatter(
        x=df['month'], y=df['profit_loss'], mode='lines+markers',
        name='Net Profit', line=dict(color='#dd6b20', width=3),
        marker=dict(size=8)
    ))

    fig_revenue_costs.update_layout(
        title="Monthly Revenue vs Costs Analysis",
        xaxis_title="Month", yaxis_title="Amount (₹ Crores)",
        height=400, template="plotly_white",
        title_font=dict(size=16, color='#2d3748', family='Inter'),
        font=dict(family='Inter', size=12)
    )
    fig_revenue_costs.update_xaxes(dtick=1)
    st.plotly_chart(fig_revenue_costs, use_container_width=True)

# Profit/Loss Analysis
fig_profit = px.bar(
    df, x='month', y='profit_loss',
    title="Monthly Profit/Loss Analysis",
    color='profit_loss',
    color_continuous_scale=['#f56565', '#fbd38d', '#38a169']
)
fig_profit.update_layout(
    xaxis_title="Month", yaxis_title="Profit/Loss (₹ Crores)",
    height=400, showlegend=False, template="plotly_white",
    title_font=dict(size=16, color='#2d3748', family='Inter'),
    font=dict(family='Inter', size=12)
)
fig_profit.update_xaxes(dtick=1)
st.plotly_chart(fig_profit, use_container_width=True)

# More Charts
col1, col2 = st.columns(2)

with col1:
    fig_invested_vs_available = go.Figure()
    fig_invested_vs_available.add_trace(go.Bar(
        x=df['month'], y=df['amount_invested'],
        name='Amount Invested', marker_color='#4299e1'
    ))
    fig_invested_vs_available.add_trace(go.Bar(
        x=df['month'], y=df['amount_available'],
        name='Available for Disbursal', marker_color='#38a169'
    ))
    fig_invested_vs_available.update_layout(
        title="Amount Invested vs Available for Disbursal",
        xaxis_title="Month", yaxis_title="Amount (₹ Crores)",
        height=400, barmode='group', template="plotly_white",
        title_font=dict(size=16, color='#2d3748', family='Inter'),
        font=dict(family='Inter', size=12)
    )
    fig_invested_vs_available.update_xaxes(dtick=1)
    st.plotly_chart(fig_invested_vs_available, use_container_width=True)

with col2:
    fig_disbursed = px.line(
        df, x='month', y='amount_disbursed',
        title="Amount Actually Disbursed",
        markers=True, color_discrete_sequence=['#38a169']
    )
    fig_disbursed.update_layout(
        xaxis_title="Month", yaxis_title="Amount Disbursed (₹ Crores)",
        height=400, template="plotly_white",
        title_font=dict(size=16, color='#2d3748', family='Inter'),
        font=dict(family='Inter', size=12)
    )
    fig_disbursed.update_xaxes(dtick=1)
    st.plotly_chart(fig_disbursed, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    fig_revenue_breakdown = go.Figure()
    fig_revenue_breakdown.add_trace(go.Bar(
        x=df['month'], y=df['interest_revenue'],
        name='Interest Revenue', marker_color='#38a169'
    ))
    fig_revenue_breakdown.add_trace(go.Bar(
        x=df['month'], y=df['processing_fees_revenue'],
        name='Processing Fees', marker_color='#4299e1'
    ))
    fig_revenue_breakdown.add_trace(go.Bar(
        x=df['month'], y=df['bad_debt_recovery'],
        name='Bad Debt Recovery', marker_color='#dd6b20'
    ))
    fig_revenue_breakdown.update_layout(
        title="Monthly Revenue Breakdown",
        xaxis_title="Month", yaxis_title="Amount (₹ Crores)",
        barmode='stack', height=400, template="plotly_white",
        title_font=dict(size=16, color='#2d3748', family='Inter'),
        font=dict(family='Inter', size=12)
    )
    fig_revenue_breakdown.update_xaxes(dtick=1)
    st.plotly_chart(fig_revenue_breakdown, use_container_width=True)

with col2:
    fig_customers = px.bar(
        df, x='month', y='customers',
        title="Monthly Customer Acquisition",
        color='customers', color_continuous_scale='Blues'
    )
    fig_customers.update_layout(
        xaxis_title="Month", yaxis_title="Number of Customers",
        height=400, showlegend=False, template="plotly_white",
        title_font=dict(size=16, color='#2d3748', family='Inter'),
        font=dict(family='Inter', size=12)
    )
    fig_customers.update_xaxes(dtick=1)
    st.plotly_chart(fig_customers, use_container_width=True)

# Complete calculations table
st.markdown('<div class="section-header">Complete Monthly Calculations</div>', unsafe_allow_html=True)

display_df = df.round(3)
column_names = {
    'month': 'Month',
    'amount_invested': 'Invested (₹Cr)',
    'amount_available': 'Available (₹Cr)',
    'amount_disbursed': 'Disbursed (₹Cr)',
    'customers': 'Customers',
    'opex': 'OpEx (₹Cr)',
    'api_expense': 'API (₹Cr)',
    'marketing_expense': 'Marketing (₹Cr)',
    'cost_of_funds': 'Cost of Funds (₹Cr)',
    'bad_debt_default': 'Bad Debt (₹Cr)',
    'gst': 'GST (₹Cr)',
    'interest_revenue': 'Interest (₹Cr)',
    'bad_debt_recovery': 'Recovery (₹Cr)',
    'processing_fees_revenue': 'PF (₹Cr)',
    'principal_return': 'Principal Return (₹Cr)',
    'profit_loss': 'Profit (₹Cr)',
    'aum': 'AUM (₹Cr)'
}

display_df = display_df.drop('salary', axis=1)
display_df = display_df.rename(columns=column_names)
st.dataframe(display_df, use_container_width=True, hide_index=True, height=400)

# Financial Summary
st.markdown('<div class="section-header">Financial Summary</div>', unsafe_allow_html=True)

total_revenue_sum = total_revenue.sum()
total_costs_sum = total_costs.sum()
net_profit_sum = df['profit_loss'].sum()
final_month_available = df['amount_available'].iloc[-1]
total_customers_sum = df['customers'].sum()
final_month_aum_summary = df['aum'].iloc[-1]

# Create a professional summary grid
summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    st.markdown(f"""
    <div class="summary-metric-card">
        <div class="summary-metric-icon" style="background: rgba(49, 130, 206, 0.1); color: #3182ce;">💰</div>
        <div class="summary-metric-label">Capital Invested</div>
        <div class="summary-metric-value" style="color: #3182ce;">₹{total_capital:.2f} Cr</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="summary-metric-card">
        <div class="summary-metric-icon" style="background: rgba(56, 161, 105, 0.1); color: #38a169;">📊</div>
        <div class="summary-metric-label">Month {num_months} Available</div>
        <div class="summary-metric-value" style="color: #38a169;">₹{final_month_available:.2f} Cr</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="summary-metric-card">
        <div class="summary-metric-icon" style="background: rgba(49, 151, 149, 0.1); color: #319795;">📈</div>
        <div class="summary-metric-label">Total Revenue</div>
        <div class="summary-metric-value" style="color: #319795;">₹{total_revenue_sum:.2f} Cr</div>
    </div>
    """, unsafe_allow_html=True)

with summary_col2:
    st.markdown(f"""
    <div class="summary-metric-card">
        <div class="summary-metric-icon" style="background: rgba(245, 101, 101, 0.1); color: #e53e3e;">💳</div>
        <div class="summary-metric-label">Total Costs</div>
        <div class="summary-metric-value" style="color: #e53e3e;">₹{total_costs_sum:.2f} Cr</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="summary-metric-card">
        <div class="summary-metric-icon" style="background: rgba(221, 107, 32, 0.1); color: #dd6b20;">🎯</div>
        <div class="summary-metric-label">Net Profit/Loss</div>
        <div class="summary-metric-value" style="color: #dd6b20;">₹{net_profit_sum:.2f} Cr</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="summary-metric-card">
        <div class="summary-metric-icon" style="background: rgba(128, 90, 213, 0.1); color: #805ad5;">👥</div>
        <div class="summary-metric-label">Total Customers</div>
        <div class="summary-metric-value" style="color: #805ad5;">{total_customers_sum:,}</div>
    </div>
    """, unsafe_allow_html=True)

with summary_col3:
    st.markdown(f"""
    <div class="summary-metric-card">
        <div class="summary-metric-icon" style="background: rgba(49, 151, 149, 0.1); color: #319795;">🏆</div>
        <div class="summary-metric-label">Month {num_months} AUM</div>
        <div class="summary-metric-value" style="color: #319795;">₹{final_month_aum_summary:.2f} Cr</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="summary-metric-card">
        <div class="summary-metric-icon" style="background: rgba(56, 161, 105, 0.1); color: #38a169;">📊</div>
        <div class="summary-metric-label">Period ROI</div>
        <div class="summary-metric-value" style="color: #38a169;">{period_roi:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="summary-metric-card">
        <div class="summary-metric-icon" style="background: rgba(49, 130, 206, 0.1); color: #3182ce;">📅</div>
        <div class="summary-metric-label">Projection Period</div>
        <div class="summary-metric-value" style="color: #3182ce;">{num_months} months</div>
    </div>
    """, unsafe_allow_html=True)
