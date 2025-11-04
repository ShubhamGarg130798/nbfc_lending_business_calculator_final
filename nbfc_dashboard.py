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
    # Enhanced login page
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 40px;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.85) 100%);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    .login-header {
        text-align: center;
        margin-bottom: 30px;
    }
    .login-icon {
        font-size: 60px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="login-container">
        <div class="login-header">
            <div class="login-icon">🏦</div>
            <h1 style="color: #2c3e50; margin: 0;">NBFC Analytics</h1>
            <p style="color: #7f8c8d; margin-top: 10px;">Secure Access Portal</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    password = st.text_input("Enter password to access dashboard:", type="password")
    if password == PASSWORD:
        st.session_state.authenticated = True
        st.success("✅ Access granted. Welcome!")
        st.rerun()
    elif password:
        st.error("❌ Incorrect password")
    st.stop()

# Set page config
st.set_page_config(
    page_title="NBFC Lending Business Calculator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with modern design
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Global Styles */
* {
    font-family: 'Inter', sans-serif;
}

/* Main container background */
.main {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    background-attachment: fixed;
}

/* Main header with glassmorphism */
.main-header {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.85) 100%);
    backdrop-filter: blur(20px);
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    border: 1px solid rgba(255, 255, 255, 0.3);
    margin-bottom: 30px;
    text-align: center;
}

.main-header h1 {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.2rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.5px;
}

.main-header p {
    color: #7f8c8d;
    font-size: 1rem;
    margin-top: 8px;
    font-weight: 500;
}

/* Custom Metrics with gradient backgrounds */
.custom-metric {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.85) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 1.8rem;
    border-radius: 20px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    margin: 0.5rem 0;
    text-align: center;
    height: 140px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    position: relative;
    overflow: hidden;
}

.custom-metric::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
    transform: scaleX(0);
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    transform-origin: left;
}

.custom-metric:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}

.custom-metric:hover::before {
    transform: scaleX(1);
}

.metric-icon {
    font-size: 2rem;
    margin-bottom: 0.3rem;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
}

.metric-label {
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #5a6c7d;
}

.metric-value {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: -0.3px;
    color: #2c3e50;
}

/* Individual metric colors with CSS variables - more professional palette */
.metric-capital {
    --gradient-start: #5a6c7d;
    --gradient-end: #475666;
}

.metric-roi {
    --gradient-start: #5a6c7d;
    --gradient-end: #475666;
}

.metric-disbursed {
    --gradient-start: #5a6c7d;
    --gradient-end: #475666;
}

.metric-profit {
    --gradient-start: #5a6c7d;
    --gradient-end: #475666;
}

.metric-aum {
    --gradient-start: #5a6c7d;
    --gradient-end: #475666;
}

/* Chart containers */
.chart-container {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.85) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 1.5rem;
    border-radius: 20px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    margin: 1rem 0;
}

/* Section headers */
.section-header {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.85) 100%);
    backdrop-filter: blur(20px);
    padding: 1.5rem;
    border-radius: 15px;
    margin: 2rem 0 1rem 0;
    border: 1px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

.section-header h2 {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 1.4rem;
    font-weight: 600;
    margin: 0;
    letter-spacing: -0.3px;
}

/* Sidebar styling */
.css-1d391kg, [data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(44, 62, 80, 0.98) 0%, rgba(52, 73, 94, 0.98) 100%);
    backdrop-filter: blur(20px);
}

.css-1d391kg .stMarkdown, [data-testid="stSidebar"] .stMarkdown {
    background: transparent;
}

/* Sidebar headers */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ecf0f1 !important;
    font-weight: 600;
    font-size: 0.95rem;
    margin: 1.2rem 0 0.8rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(149, 165, 166, 0.3);
    letter-spacing: 0.3px;
}

/* Expander styling */
.streamlit-expanderHeader {
    background: rgba(52, 73, 94, 0.6) !important;
    border-radius: 8px !important;
    padding: 0.7rem !important;
    margin: 0.5rem 0 !important;
    border: 1px solid rgba(149, 165, 166, 0.2) !important;
    color: #ecf0f1 !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    transition: all 0.3s ease !important;
}

.streamlit-expanderHeader:hover {
    background: rgba(52, 73, 94, 0.8) !important;
    transform: translateX(3px);
}

/* Sidebar labels */
[data-testid="stSidebar"] label {
    color: #bdc3c7 !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    margin-bottom: 0.5rem !important;
}

/* Sidebar number inputs */
[data-testid="stSidebar"] input[type="number"] {
    background: rgba(52, 73, 94, 0.9) !important;
    border: 1px solid rgba(149, 165, 166, 0.3) !important;
    color: #ecf0f1 !important;
    border-radius: 8px !important;
    padding: 0.5rem !important;
    font-weight: 500 !important;
}

[data-testid="stSidebar"] input[type="number"]:focus {
    border-color: #3498db !important;
    box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.3) !important;
    outline: none !important;
}

/* Dataframe styling */
.stDataFrame {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.85) 100%);
    backdrop-filter: blur(20px);
    border-radius: 15px;
    padding: 1rem;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    border: 1px solid rgba(255, 255, 255, 0.3);
}

/* Summary box */
.summary-box {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.85) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    margin: 1rem 0;
}

.summary-box h3 {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
    margin-bottom: 1.5rem;
}

.summary-item {
    display: flex;
    justify-content: space-between;
    padding: 0.8rem 0;
    border-bottom: 1px solid rgba(0,0,0,0.05);
    font-size: 1.05rem;
}

.summary-item:last-child {
    border-bottom: none;
}

.summary-label {
    font-weight: 600;
    color: #2c3e50;
}

.summary-value {
    font-weight: 700;
    color: #667eea;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(0,0,0,0.1);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
}

/* Plotly chart backgrounds */
.js-plotly-plot .plotly .main-svg {
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# Title with enhanced styling
st.markdown("""
<div class="main-header">
    <h1>💰 NBFC Lending Analytics</h1>
    <p>Comprehensive Business Intelligence Dashboard</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for all inputs with collapsible sections
st.sidebar.markdown("# 🎛️ Configuration Panel")

# Projection Period - Expandable Section
with st.sidebar.expander("📅 PROJECTION PERIOD", expanded=True):
    num_months = st.number_input("Number of Months", min_value=1, max_value=48, value=12, step=1)

# Capital Deployment Parameters - Expandable Section
with st.sidebar.expander("💰 CAPITAL DEPLOYMENT (₹ Crores)", expanded=False):
    # Create dynamic capital inputs based on number of months
    capital_values = []
    if num_months <= 12:
        # Two columns for 12 or fewer months
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
        # Single column for more than 12 months
        for i in range(num_months):
            month_num = i + 1
            if month_num <= 5:
                default_val = [5.0, 4.0, 4.0, 4.0, 3.0][i]
            else:
                default_val = 0.0
            val = st.number_input(f"Month {month_num}", min_value=0.0, max_value=20.0, value=default_val, step=0.5, key=f"cap_{month_num}")
            capital_values.append(val)

# Create individual variables for backward compatibility
for i in range(48):  # Create all possible month variables
    if i < len(capital_values):
        globals()[f"month{i+1}_capital"] = capital_values[i]
    else:
        globals()[f"month{i+1}_capital"] = 0.0

total_capital = sum(capital_values)

# Business Parameters - Expandable Section
with st.sidebar.expander("📈 REVENUE PARAMETERS", expanded=False):
    processing_fees = st.number_input("Processing Fees (%)", min_value=0.0, max_value=25.0, value=11.8, step=0.1) / 100
    monthly_interest_rate = st.number_input("Monthly Interest Rate (%)", min_value=0.0, max_value=50.0, value=30.0, step=0.5) / 100
    marketing_rate = st.number_input("Marketing Expenses (%)", min_value=0.0, max_value=10.0, value=2.0, step=0.1) / 100
    cost_of_funds_rate = st.number_input("Cost of Funds (% monthly)", min_value=0.0, max_value=10.0, value=1.5, step=0.1) / 100

# Operational expense rates - Expandable Section
with st.sidebar.expander("🏢 OPERATIONAL EXPENSES (%)", expanded=False):
    opex_month1_value = st.number_input("Month 1 OpEx (₹)", 0, 5000000, 1500000, 50000)
    opex_month1 = opex_month1_value / 1e7  # Convert to crores for consistency

    # Create dynamic OPEX inputs based on number of months (starting from month 2)
    opex_values = [opex_month1]  # Month 1 is already handled above
    for i in range(1, num_months):  # Start from month 2
        month_num = i + 1
        if month_num <= 3:
            default_val = 10.0
        elif month_num <= 6:
            default_val = 5.0
        else:
            default_val = 4.0
        val = st.number_input(f"Month {month_num} OpEx Rate (%)", min_value=0.0, max_value=30.0, value=default_val, step=0.5, key=f"opex_{month_num}") / 100
        opex_values.append(val)

# Create individual variables for backward compatibility
for i in range(48):  # Create all possible month variables
    if i < len(opex_values):
        globals()[f"opex_month{i+1}"] = opex_values[i]
    else:
        globals()[f"opex_month{i+1}"] = 0.04  # Default 4%

# Loan parameters - Expandable Section
with st.sidebar.expander("🎯 LOAN PARAMETERS", expanded=False):
    avg_ticket_size = st.number_input("Average Loan Ticket (₹)", 10000, 50000, 22000, 1000)

# Collection parameters - Expandable Section
with st.sidebar.expander("📊 COLLECTION PARAMETERS", expanded=False):
    t0_collection = st.number_input("T+0 Collection Rate (%)", min_value=0, max_value=100, value=80, step=1) / 100
    t30_collection = st.number_input("T+30 Collection Rate (%)", min_value=0, max_value=100, value=5, step=1) / 100
    t60_collection = st.number_input("T+60 Collection Rate (%)", min_value=0, max_value=100, value=5, step=1) / 100
    t90_collection = st.number_input("T+90 Collection Rate (%)", min_value=0, max_value=100, value=3, step=1) / 100

    # Validation for collection rates
    total_collection_rate_percent = (t0_collection + t30_collection + t60_collection + t90_collection) * 100
    if total_collection_rate_percent > 100:
        st.error(f"⚠️ Total collection rate is {total_collection_rate_percent:.1f}% - should not exceed 100%")
    else:
        st.success(f"✅ Total collection rate: {total_collection_rate_percent:.1f}%")

    # API costs
    api_cost_80_percent = st.number_input("API Cost (Per Lead Not Converted) ₹", 0, 100, 35, 5)
    api_cost_20_percent = st.number_input("API Cost (Per Converted Customers) ₹", 0, 150, 95, 5)

# Fixed costs - Expandable Section
with st.sidebar.expander("💳 MONTHLY PRINCIPAL RETURN (₹ Crores)", expanded=False):
    # Create dynamic principal return inputs based on number of months
    principal_values = []
    if num_months <= 12:
        # Two columns for 12 or fewer months
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
        # Single column for more than 12 months
        for i in range(num_months):
            month_num = i + 1
            val = st.number_input(f"Month {month_num} PR", min_value=0.0, value=0.0, step=0.1, key=f"prin_{month_num}")
            principal_values.append(val)

# Create individual variables for backward compatibility
for i in range(48):  # Create all possible month variables
    if i < len(principal_values):
        globals()[f"month{i+1}_principal"] = principal_values[i]
    else:
        globals()[f"month{i+1}_principal"] = 0.0

# EXACT calculation function using your formulas
def calculate_with_exact_formulas():
    months = num_months  # Use dynamic number of months
    
    # Capital deployment schedule - use actual number of months
    capital_invested = [capital_values[i] * 1e7 if i < len(capital_values) else 0 for i in range(months)]
    
    # OPEX rates array - use actual number of months
    opex_rates = [opex_values[i] if i < len(opex_values) else 0.04 for i in range(months)]
    
    # Principal return array - use actual number of months (convert from crores to rupees)
    principal_returns = [principal_values[i] * 1e7 if i < len(principal_values) else 0 for i in range(months)]
    
    # Initialize arrays to store all calculations
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
        # Amount Invested
        amount_invested.append(capital_invested[month])
        
        # Amount Available for Disbursal
        if month == 0:
            available = capital_invested[month]
        else:
            prev_profit = profit_loss[month-1]
            available = amount_available[month-1] + prev_profit + capital_invested[month]
        
        amount_available.append(available)
        
        # Amount Actually Disbursed = Amount Available / (1 - Processing Fees)
        disbursed = available / (1 - processing_fees)
        amount_disbursed.append(disbursed)
        
        # Number of Customers
        num_customers = int(disbursed / avg_ticket_size)
        customers.append(num_customers)
        
        # Operational Expenses
        if month == 0:
            op_expense = opex_month1_value  # Use editable value for month 1
        else:
            prev_aum = aum[month-1]
            op_expense = prev_aum * opex_rates[month]
        
        opex.append(op_expense)
        
        # API Cost
        api_cost = (num_customers * 2 * api_cost_20_percent) + (num_customers * 8 * api_cost_80_percent)
        api_expense.append(api_cost)
        
        # Marketing Expense
        marketing_exp = disbursed * marketing_rate
        marketing_expense.append(marketing_exp)
        
        # Cost of Funds (quarterly calculation - adapted for variable months)
        cost_of_funds_expense = 0
        # Calculate cost of funds for quarters that are complete within the selected months
        if month == 2 and months >= 3:  # Month 3 (Q1) - if we have at least 3 months
            cost_q1_m1 = capital_invested[0] * cost_of_funds_rate
            cost_q1_m2 = sum(capital_invested[:2]) * cost_of_funds_rate  
            cost_q1_m3 = sum(capital_invested[:3]) * cost_of_funds_rate
            cost_of_funds_expense = cost_q1_m1 + cost_q1_m2 + cost_q1_m3
        elif month == 5 and months >= 6:  # Month 6 (Q2) - if we have at least 6 months
            cost_q2_m4 = sum(capital_invested[:4]) * cost_of_funds_rate
            cost_q2_m5 = sum(capital_invested[:5]) * cost_of_funds_rate
            cost_q2_m6 = sum(capital_invested[:6]) * cost_of_funds_rate
            cost_of_funds_expense = cost_q2_m4 + cost_q2_m5 + cost_q2_m6
        elif month == 8 and months >= 9:  # Month 9 (Q3) - if we have at least 9 months
            cost_q3_m7 = sum(capital_invested[:7]) * cost_of_funds_rate
            cost_q3_m8 = sum(capital_invested[:8]) * cost_of_funds_rate
            cost_q3_m9 = sum(capital_invested[:9]) * cost_of_funds_rate
            cost_of_funds_expense = cost_q3_m7 + cost_q3_m8 + cost_q3_m9
        elif month == 11 and months >= 12:  # Month 12 (Q4) - if we have at least 12 months
            cost_q4_m10 = sum(capital_invested[:10]) * cost_of_funds_rate
            cost_q4_m11 = sum(capital_invested[:11]) * cost_of_funds_rate
            cost_q4_m12 = sum(capital_invested[:12]) * cost_of_funds_rate
            cost_of_funds_expense = cost_q4_m10 + cost_q4_m11 + cost_q4_m12
        # Add additional quarters for periods longer than 12 months
        elif month == 14 and months >= 15:  # Month 15 (Q5)
            cost_q5_m13 = sum(capital_invested[:13]) * cost_of_funds_rate
            cost_q5_m14 = sum(capital_invested[:14]) * cost_of_funds_rate
            cost_q5_m15 = sum(capital_invested[:15]) * cost_of_funds_rate
            cost_of_funds_expense = cost_q5_m13 + cost_q5_m14 + cost_q5_m15
        elif month == 17 and months >= 18:  # Month 18 (Q6)
            cost_q6_m16 = sum(capital_invested[:16]) * cost_of_funds_rate
            cost_q6_m17 = sum(capital_invested[:17]) * cost_of_funds_rate
            cost_q6_m18 = sum(capital_invested[:18]) * cost_of_funds_rate
            cost_of_funds_expense = cost_q6_m16 + cost_q6_m17 + cost_q6_m18
        # Continue pattern for longer periods - every 3rd month starting from month 3
        elif (month + 1) % 3 == 0 and month >= 2 and months > month:  # General quarterly calculation
            quarter_start = month - 2
            cost_q_m1 = sum(capital_invested[:quarter_start+1]) * cost_of_funds_rate
            cost_q_m2 = sum(capital_invested[:quarter_start+2]) * cost_of_funds_rate
            cost_q_m3 = sum(capital_invested[:quarter_start+3]) * cost_of_funds_rate
            cost_of_funds_expense = cost_q_m1 + cost_q_m2 + cost_q_m3
        
        cost_of_funds.append(cost_of_funds_expense)
        
        # Interest calculation (split across two months)
        if month == 0:
            interest = (disbursed * monthly_interest_rate) / 2
        else:
            current_month_interest = (disbursed * monthly_interest_rate) / 2
            prev_month_interest = (amount_disbursed[month-1] * monthly_interest_rate) / 2
            interest = current_month_interest + prev_month_interest
        
        interest_revenue.append(interest)
        
        # Bad Debt Default = (Amount Disbursed + Interest) × (1 - T+0 Collection Rate)
        bad_debt = (disbursed + interest) * (1 - t0_collection)
        bad_debt_default.append(bad_debt)
        
        # Recovery of Bad Debt
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
        
        # Processing Fees
        pf = disbursed * processing_fees
        processing_fees_revenue.append(pf)
        
        # GST
        gst_amount = pf * (18/118)
        gst.append(gst_amount)
        
        # Fixed costs
        monthly_salary = 0  # Fixed at 0 since removed from inputs
        salary.append(monthly_salary)
        principal_return.append(principal_returns[month])
        
        # Profit/Loss
        profit = (interest + recovery + pf) - (op_expense + api_cost + marketing_exp + cost_of_funds_expense + bad_debt + gst_amount + monthly_salary + principal_returns[month])
        profit_loss.append(profit)
        
        # AUM = Current month + Previous months with weightings
        # Handle edge cases for months that don't exist (use 0 values)
        current_disbursed_interest = disbursed + interest
        
        # Previous month (i-1) with 15% weighting
        if month >= 1:
            prev_disbursed_interest = amount_disbursed[month-1] + interest_revenue[month-1]
        else:
            prev_disbursed_interest = 0
            
        # Two months ago (i-2) with 10% weighting  
        if month >= 2:
            prev2_disbursed_interest = amount_disbursed[month-2] + interest_revenue[month-2]
        else:
            prev2_disbursed_interest = 0
            
        # Three months ago (i-3) with 3% weighting
        if month >= 3:
            prev3_disbursed_interest = amount_disbursed[month-3] + interest_revenue[month-3]
        else:
            prev3_disbursed_interest = 0
            
        # Calculate AUM with new formula
        aum_value = (current_disbursed_interest + 
                    prev_disbursed_interest * 0.15 + 
                    prev2_disbursed_interest * 0.10 + 
                    prev3_disbursed_interest * 0.03)
        aum.append(aum_value)
    
    # Create DataFrame with dynamic number of months
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

# Calculate derived metrics
# Time-weighted investment calculation for variable months
sum_annual_investment = 0
for i, capital in enumerate(capital_values):
    months_remaining = num_months - i
    weight = months_remaining / num_months
    sum_annual_investment += capital * weight

# Calculate projections first to get final month values
df = calculate_with_exact_formulas()

# Calculate Actual Period ROI (not annualized)
final_month_aum = df['aum'].iloc[-1]
if sum_annual_investment > 0:
    period_roi = ((final_month_aum - sum_annual_investment) / sum_annual_investment) * 100
else:
    period_roi = 0

# Key Performance Indicators with enhanced styling
st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="custom-metric metric-capital">
        <div class="metric-icon">💰</div>
        <div class="metric-label">Capital Invested</div>
        <div class="metric-value">₹{total_capital:.1f} Cr</div>
    </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown(f"""
    <div class="custom-metric metric-roi">
        <div class="metric-icon">📈</div>
        <div class="metric-label">Period ROI</div>
        <div class="metric-value">{period_roi:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)
    
with col3:
    final_month_disbursed = df['amount_disbursed'].iloc[-1]
    st.markdown(f"""
    <div class="custom-metric metric-disbursed">
        <div class="metric-icon">📊</div>
        <div class="metric-label">M{num_months} Disbursed</div>
        <div class="metric-value">₹{final_month_disbursed:.2f} Cr</div>
    </div>
    """, unsafe_allow_html=True)
    
with col4:
    final_month_profit = df['profit_loss'].iloc[-1]
    st.markdown(f"""
    <div class="custom-metric metric-profit">
        <div class="metric-icon">🎯</div>
        <div class="metric-label">M{num_months} Profit</div>
        <div class="metric-value">₹{final_month_profit:.2f} Cr</div>
    </div>
    """, unsafe_allow_html=True)
    
with col5:
    final_month_aum = df['aum'].iloc[-1]
    st.markdown(f"""
    <div class="custom-metric metric-aum">
        <div class="metric-icon">🏆</div>
        <div class="metric-label">M{num_months} AUM</div>
        <div class="metric-value">₹{final_month_aum:.2f} Cr</div>
    </div>
    """, unsafe_allow_html=True)

# Charts section with enhanced styling
st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <h2>📊 Business Analytics & Insights</h2>
</div>
""", unsafe_allow_html=True)

# Row 1: AUM Chart and Monthly Revenue vs Cost Analysis (side by side)
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # 1. AUM Growth Analysis
    fig_aum_growth = px.area(
        df,
        x='month',
        y='aum',
        title="Assets Under Management (AUM) Growth",
        color_discrete_sequence=['#667eea']
    )
    fig_aum_growth.update_layout(
        xaxis_title="Month",
        yaxis_title="AUM (₹ Crores)",
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", color="#2c3e50"),
        title_font=dict(size=18, color="#2c3e50", family="Inter, sans-serif")
    )
    fig_aum_growth.update_xaxes(dtick=1, showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    fig_aum_growth.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    fig_aum_growth.update_traces(hovertemplate='Month %{x}<br>AUM: ₹%{y:.2f} Cr<extra></extra>')
    st.plotly_chart(fig_aum_growth, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # 2. Revenue vs Costs
    fig_revenue_costs = go.Figure()

    # Calculate revenue and costs
    total_revenue = df['interest_revenue'] + df['processing_fees_revenue'] + df['bad_debt_recovery']
    total_costs = (df['opex'] + df['api_expense'] + df['marketing_expense'] + 
                   df['cost_of_funds'] + df['bad_debt_default'] + df['gst'] + 
                   df['salary'] + df['principal_return'])

    fig_revenue_costs.add_trace(go.Bar(
        x=df['month'],
        y=total_revenue,
        name='Total Revenue',
        marker_color='#27ae60',
        hovertemplate='Month %{x}<br>Revenue: ₹%{y:.2f} Cr<extra></extra>'
    ))

    fig_revenue_costs.add_trace(go.Bar(
        x=df['month'],
        y=total_costs,
        name='Total Costs',
        marker_color='#e74c3c',
        hovertemplate='Month %{x}<br>Costs: ₹%{y:.2f} Cr<extra></extra>'
    ))

    fig_revenue_costs.add_trace(go.Scatter(
        x=df['month'],
        y=df['profit_loss'],
        mode='lines+markers',
        name='Net Profit',
        line=dict(color='#f39c12', width=4),
        marker=dict(size=10),
        hovertemplate='Month %{x}<br>Profit: ₹%{y:.2f} Cr<extra></extra>'
    ))

    fig_revenue_costs.update_layout(
        title="Monthly Revenue vs Costs Analysis",
        xaxis_title="Month",
        yaxis_title="Amount (₹ Crores)",
        hovermode='x unified',
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", color="#2c3e50"),
        title_font=dict(size=18, color="#2c3e50", family="Inter, sans-serif")
    )
    fig_revenue_costs.update_xaxes(dtick=1, showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    fig_revenue_costs.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')

    st.plotly_chart(fig_revenue_costs, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Row 2: Monthly Profit/Loss Analysis (full width)
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
# 3. Profit/Loss Analysis
fig_profit = px.bar(
    df,
    x='month',
    y='profit_loss',
    title="Monthly Profit/Loss Analysis",
    color='profit_loss',
    color_continuous_scale=['#e74c3c', '#f39c12', '#27ae60']
)
fig_profit.update_layout(
    xaxis_title="Month",
    yaxis_title="Profit/Loss (₹ Crores)",
    height=400,
    showlegend=False,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Inter, sans-serif", color="#2c3e50"),
    title_font=dict(size=18, color="#2c3e50", family="Inter, sans-serif")
)
fig_profit.update_xaxes(dtick=1, showgrid=True, gridcolor='rgba(0,0,0,0.05)')
fig_profit.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
fig_profit.update_traces(hovertemplate='Month %{x}<br>Profit/Loss: ₹%{y:.2f} Cr<extra></extra>')
st.plotly_chart(fig_profit, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Row 3: Amount Invested vs Available and Amount Disbursed (side by side)
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # 4. Amount Invested vs Available for Disbursal - Both as bars
    fig_invested_vs_available = go.Figure()

    fig_invested_vs_available.add_trace(go.Bar(
        x=df['month'],
        y=df['amount_invested'],
        name='Amount Invested',
        marker_color='#3498db',
        hovertemplate='Month %{x}<br>Invested: ₹%{y:.2f} Cr<extra></extra>'
    ))

    fig_invested_vs_available.add_trace(go.Bar(
        x=df['month'],
        y=df['amount_available'],
        name='Available for Disbursal',
        marker_color='#9b59b6',
        hovertemplate='Month %{x}<br>Available: ₹%{y:.2f} Cr<extra></extra>'
    ))

    fig_invested_vs_available.update_layout(
        title="Amount Invested vs Available for Disbursal",
        xaxis_title="Month",
        yaxis_title="Amount (₹ Crores)",
        hovermode='x unified',
        height=400,
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", color="#2c3e50"),
        title_font=dict(size=18, color="#2c3e50", family="Inter, sans-serif")
    )
    fig_invested_vs_available.update_xaxes(dtick=1, showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    fig_invested_vs_available.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')

    st.plotly_chart(fig_invested_vs_available, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # 5. Amount Actually Disbursed vs Month
    fig_disbursed = px.line(
        df,
        x='month',
        y='amount_disbursed',
        title="Amount Actually Disbursed",
        markers=True,
        color_discrete_sequence=['#27ae60']
    )
    fig_disbursed.update_layout(
        xaxis_title="Month",
        yaxis_title="Amount Disbursed (₹ Crores)",
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", color="#2c3e50"),
        title_font=dict(size=18, color="#2c3e50", family="Inter, sans-serif")
    )
    fig_disbursed.update_xaxes(dtick=1, showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    fig_disbursed.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    fig_disbursed.update_traces(
        hovertemplate='Month %{x}<br>Disbursed: ₹%{y:.2f} Cr<extra></extra>',
        line=dict(width=3),
        marker=dict(size=10)
    )
    st.plotly_chart(fig_disbursed, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Row 4: Revenue Breakdown and Customer Acquisition (side by side)
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # 6. Revenue Breakdown
    fig_revenue_breakdown = go.Figure()

    fig_revenue_breakdown.add_trace(go.Bar(
        x=df['month'],
        y=df['interest_revenue'],
        name='Interest Revenue',
        marker_color='#27ae60',
        hovertemplate='Month %{x}<br>Interest: ₹%{y:.2f} Cr<extra></extra>'
    ))

    fig_revenue_breakdown.add_trace(go.Bar(
        x=df['month'],
        y=df['processing_fees_revenue'],
        name='Processing Fees',
        marker_color='#3498db',
        hovertemplate='Month %{x}<br>Processing Fees: ₹%{y:.2f} Cr<extra></extra>'
    ))

    fig_revenue_breakdown.add_trace(go.Bar(
        x=df['month'],
        y=df['bad_debt_recovery'],
        name='Bad Debt Recovery',
        marker_color='#e67e22',
        hovertemplate='Month %{x}<br>Recovery: ₹%{y:.2f} Cr<extra></extra>'
    ))

    fig_revenue_breakdown.update_layout(
        title="Monthly Revenue Breakdown",
        xaxis_title="Month",
        yaxis_title="Amount (₹ Crores)",
        barmode='stack',
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", color="#2c3e50"),
        title_font=dict(size=18, color="#2c3e50", family="Inter, sans-serif")
    )
    fig_revenue_breakdown.update_xaxes(dtick=1, showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    fig_revenue_breakdown.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')

    st.plotly_chart(fig_revenue_breakdown, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # 7. Customer Acquisition
    fig_customers = px.bar(
        df,
        x='month',
        y='customers',
        title="Monthly Customer Acquisition",
        color='customers',
        color_continuous_scale=['#667eea', '#764ba2', '#f093fb']
    )
    fig_customers.update_layout(
        xaxis_title="Month",
        yaxis_title="Number of Customers",
        height=400,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", color="#2c3e50"),
        title_font=dict(size=18, color="#2c3e50", family="Inter, sans-serif")
    )
    fig_customers.update_xaxes(dtick=1, showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    fig_customers.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.05)')
    fig_customers.update_traces(hovertemplate='Month %{x}<br>Customers: %{y:,.0f}<extra></extra>')
    st.plotly_chart(fig_customers, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Complete calculations table
st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <h2>📋 Detailed Monthly Calculations</h2>
</div>
""", unsafe_allow_html=True)

# Round for display
display_df = df.round(3)

# Rename columns for better readability and remove salary
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

# Remove salary column and rename
display_df = display_df.drop('salary', axis=1)
display_df = display_df.rename(columns=column_names)
st.dataframe(display_df, use_container_width=True, hide_index=True, height=400)

# Summary and export
st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)
st.markdown("""
<div class="section-header">
    <h2>📊 Executive Summary</h2>
</div>
""", unsafe_allow_html=True)

total_revenue_sum = total_revenue.sum()
total_costs_sum = total_costs.sum()
net_profit_sum = df['profit_loss'].sum()
final_aum = df['aum'].iloc[-1]
final_month_available = df['amount_available'].iloc[-1]
total_customers_sum = df['customers'].sum()
final_month_aum_summary = df['aum'].iloc[-1]

st.markdown(f"""
<div class="summary-box">
    <h3>💼 {num_months}-Month Financial Overview</h3>
    <div class="summary-item">
        <span class="summary-label">💰 Capital Invested</span>
        <span class="summary-value">₹{total_capital:.2f} Cr</span>
    </div>
    <div class="summary-item">
        <span class="summary-label">📊 Month {num_months} Available for Disbursal</span>
        <span class="summary-value">₹{final_month_available:.2f} Cr</span>
    </div>
    <div class="summary-item">
        <span class="summary-label">🏆 Month {num_months} AUM</span>
        <span class="summary-value">₹{final_month_aum_summary:.2f} Cr</span>
    </div>
    <div class="summary-item">
        <span class="summary-label">🎯 Total Profit/Loss ({num_months} months)</span>
        <span class="summary-value">₹{net_profit_sum:.2f} Cr</span>
    </div>
    <div class="summary-item">
        <span class="summary-label">👥 Total Customers</span>
        <span class="summary-value">{total_customers_sum:,}</span>
    </div>
    <div class="summary-item">
        <span class="summary-label">💵 Total Revenue</span>
        <span class="summary-value">₹{total_revenue_sum:.2f} Cr</span>
    </div>
    <div class="summary-item">
        <span class="summary-label">💸 Total Costs</span>
        <span class="summary-value">₹{total_costs_sum:.2f} Cr</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.6); font-size: 0.9rem; padding: 2rem;">
    <p>NBFC Lending Analytics Dashboard | Powered by Advanced Financial Modeling</p>
</div>
""", unsafe_allow_html=True)
