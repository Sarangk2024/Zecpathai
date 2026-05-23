# technical_ai/experience_logic.py

def get_experience_level(years):
    if years <= 2:
        return "0-2"
    elif years <= 5:
        return "3-5"
    return "5+"
