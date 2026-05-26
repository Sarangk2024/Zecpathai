# ai_core/hiring_fit_calculator.py

def calculate_hiring_fit(score):
    if score >= 85:
        category = "Excellent Fit"
    elif score >= 70:
        category = "Strong Fit"
    elif score >= 55:
        category = "Moderate Fit"
    else:
        category = "Low Fit"
        
    return {
        "hiring_fit_percentage": score,
        "fit_category": category
    }
