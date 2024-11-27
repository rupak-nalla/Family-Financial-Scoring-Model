from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample financial scoring model function
def calculate_financial_score(income, savings, expenses, loan_payments, credit_card_spending, goals_met):
    # income = data['Income']
    # savings = data['Savings']
    # expenses = data['Monthly Expenses']
    # loan_payments = data['Loan Payments']
    # credit_card_spending = data['Credit Card Spending']
    # financial_goals_met = data['Financial Goals Met (%)']

    if income == 0:
        return 0

    # Scoring components
    savings_score = (savings / income) * 40
    expenses_score = (1 - (expenses / income)) * 20
    loan_score = (1 - (loan_payments / income)) * 15
    credit_card_score = (1 - (credit_card_spending / income)) * 10
    goals_score = (goals_met / 100) * 15

    # Total score
    total_score = savings_score + expenses_score + loan_score + credit_card_score + goals_score
    return max(0, min(100, total_score))

@app.route('/calculate_score', methods=['POST'])
def calculate_score():
    data = request.json
    
    try:
        # Extract input values
        income = data.get("Income", 0)
        savings = data.get("Savings", 0)
        expenses = data.get("Monthly Expenses", 0)
        loan_payments = data.get("Loan Payments", 0)
        credit_card_spending = data.get("Credit Card Spending", 0)
        goals_met = data.get("Financial Goals Met (%)", 0)
        
        # Calculate financial score
        financial_score = calculate_financial_score(
            income, savings, expenses, loan_payments, credit_card_spending, goals_met
        )
        
        return jsonify({
            "Family ID": data.get("Family ID", "N/A"),
            "Financial Score": financial_score
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
