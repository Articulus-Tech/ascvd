

# Atherosclerotic cardiovascular disease (ASCVD) Risk Calculator+

ASCVD+ implementation in python 3.

##Usage:

 

    from ascvd import *
    
    ascvd = ASCVD(
        age=55,
        diabetic=False,
        smoker=False,
        hypertensive=False,
        systolic=120,
        gender='female',
        hdl=50,
        total_cholesterol=213,
        race='aa',
    )
    
    ascvd.compute_ten_year_score()
    ascvd.compute_lifetime_risk()
    ascvd.compute_optimal_lifetime()
    ascvd.compute_ten_year_risk_reduction(quit_smoking=True, 
                                          statin_therapy=True)
    

References:

https://tools.acc.org/ASCVD-Risk-Estimator-Plus/#!/content/clinician-split-layout/reference_external_links


