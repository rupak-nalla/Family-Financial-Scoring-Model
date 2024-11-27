import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Scoring function
def calculate_financial_score(data):
    income = data['Income']
    savings = data['Savings']
    expenses = data['Monthly Expenses']
    loan_payments = data['Loan Payments']
    credit_card_spending = data['Credit Card Spending']
    financial_goals_met = data['Financial Goals Met (%)']

    if income == 0:
        return 0

    # Scoring components
    savings_score = (savings / income) * 40
    expenses_score = (1 - (expenses / income)) * 20
    loan_score = (1 - (loan_payments / income)) * 15
    credit_card_score = (1 - (credit_card_spending / income)) * 10
    goals_score = (financial_goals_met / 100) * 15

    # Total score
    total_score = savings_score + expenses_score + loan_score + credit_card_score + goals_score
    return max(0, min(100, total_score))

# Recommendations
def generate_recommendations(data, score):
    recommendations = []
    if data['Savings'] / data['Income'] < 0.2:
        recommendations.append("Increase savings to at least 20% of income.")
    if data['Monthly Expenses'] / data['Income'] > 0.5:
        recommendations.append("Reduce monthly expenses to less than 50% of income.")
    if data['Loan Payments'] / data['Income'] > 0.3:
        recommendations.append("Reduce loan payments to less than 30% of income.")
    if score < 50:
        recommendations.append("Focus on meeting financial goals to improve the score.")
    return recommendations

# Streamlit UI
st.title("Financial Insights Dashboard")

st.sidebar.header("Input Family Data")
family_data = {
    "Income": st.sidebar.number_input("Monthly Income", min_value=0, value=10000),
    "Savings": st.sidebar.number_input("Savings", min_value=0, value=5000),
    "Monthly Expenses": st.sidebar.number_input("Monthly Expenses", min_value=0, value=2000),
    "Loan Payments": st.sidebar.number_input("Loan Payments", min_value=0, value=1000),
    "Credit Card Spending": st.sidebar.number_input("Credit Card Spending", min_value=0, value=500),
    "Financial Goals Met (%)": st.sidebar.slider("Financial Goals Met (%)", 0, 100, 80),
}

# Calculate score
score = calculate_financial_score(family_data)
st.metric("Financial Score", f"{score:.2f}/100")

# Recommendations
st.header("Recommendations")
recommendations = generate_recommendations(family_data, score)
if recommendations:
    for rec in recommendations:
        st.write(f"- {rec}")
else:
    st.write("Your financial health looks great!")

# Visualizations
st.header("Visualizations")
data = pd.DataFrame([family_data])

# Spending breakdown
st.subheader("Spending Breakdown")
spending_data = pd.DataFrame({
    "Category": ["Savings", "Expenses", "Loan Payments", "Credit Card Spending"],
    "Amount": [
        family_data["Savings"],
        family_data["Monthly Expenses"],
        family_data["Loan Payments"],
        family_data["Credit Card Spending"]
    ]
})
fig, ax = plt.subplots()
sns.barplot(x="Category", y="Amount", data=spending_data, ax=ax)
st.pyplot(fig)
