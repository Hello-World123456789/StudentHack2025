def calculate_risk_tolerance_score(age, salary, budget):
    """
    Calculate the Risk Tolerance Score (RTS) for an investor.
    
    Args:
        age (int): Investor's age
        salary (float): Annual salary
        budget (float): Investment budget
    
    Returns:
        float: Risk Tolerance Score between 0 (conservative) and 1 (aggressive)
    """
    # Calculate components
    age_factor = 1 - (age / 100)
    salary_factor = min(salary / 200000, 1)
    budget_factor = min(budget / 50000, 1)
    
    # Calculate RTS with weighted components
    rts = (0.4 * age_factor) + (0.3 * salary_factor) + (0.3 * budget_factor)
    
    return rts

def interpret_risk_score(rts):
    """
    Interpret the Risk Tolerance Score into a risk category.
    
    Args:
        rts (float): Risk Tolerance Score
    
    Returns:
        str: Risk category description
    """
    if rts < 0.3:
        return "Conservative (e.g., dividend stocks, low-volatility sectors)"
    elif 0.3 <= rts < 0.6:
        return "Moderate (e.g., blended growth/value stocks)"
    else:
        return "Aggressive (e.g., tech/growth stocks, higher beta)"

# Example usage
investor_data = {
    "age": 45,
    "salary": 86378,
    "budget": 13814
}

# Calculate RTS
rts = calculate_risk_tolerance_score(
    age=investor_data["age"],
    salary=investor_data["salary"],
    budget=investor_data["budget"]
)

# Interpret the score
risk_category = interpret_risk_score(rts)
print(risk_category)
