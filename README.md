# StudentHack2025
END_VALUE = 10
BEGINNING_VALUE = 100

statement1 = "Grant Lopez is 47 years old and has a budget of $2716 per year. He started investing on June 16th, 2023 and ended on October 22nd, 2023. His hobbies are painting and he avoids Crypto Assets."

T0 = 0
T1 = 1

class portfolioVariables(__init__)
    def find_budget(statement):    
        budget_position_beg = statement.find("budget of $") 
        if budget_position_beg == -1:
            budget_position_beg = statement.find("budget is $") 
            if budget_position_beg == -1:
                budget_position_beg = statement.find("investment of $") 
                if budget_position_beg == -1:
                    return None
        
        start_index = budget_position_beg + len("budget of $")
        budget = ""
        
        for character in statement[start_index:]:
            if character.isdigit():
                budget += character
            else:
                return budget
        return budget

    def find_times(statement):
        
        return T0, T1

def inflationRisk(END_VALUE, BEGINNING_VALUE, T0, T1):
    # The inflation rate at time 0 must be greater than the investment return
    # at time 1 for positive real returns
    
    # Calculate rate of return
    nominalStockReturn = (END_VALUE - BEGINNING_VALUE)/BEGINNING_VALUE
    
    # Consumer Price Index (CPI) data set to measure US stock inflationary risk
    endCPI = 
    beginningCPI =
    
    inflationRate = (endCPI - beginningCPI) / beginningCPI
        
    # Definition returns an index of whether or not the inflation risk is good
    # Add a function that will compare stocks real returns to one another.
    if nominalStockReturn > inflationRate:
        return 1
    else:
        return 0
    
    for character in statement[start_index:]:
        if character.isdigit():
            budget += character
        else:
            return budget
    return budget


