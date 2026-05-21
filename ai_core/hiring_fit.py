# ai_core/hiring_fit.py

def calculate_hiring_fit(score):
    if score >= 80:
        fit = "Excellent Fit"
    elif score >= 65:
        fit = "Good Fit"
    elif score >= 50:
        fit = "Moderate Fit"
    else:
        fit = "Low Fit"
        
    return {
        "hiring_fit_percentage": score,
        "fit_category": fit
    }
