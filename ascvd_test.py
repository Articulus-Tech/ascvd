import pytest

from ascvd import *

# test_data source - http://tools.acc.org/ASCVD-Risk-Estimator-Plus/#!/calculate/estimate/

test_data = [
    # white female
    [58, False, False, False, 90, 'female', 100, 130, 'white', 0.6, 8],
    [58, False, False, False, 129, 'female', 80, 160, 'white', 1.7, 27],
    [58, True, False, False, 129, 'female', 80, 160, 'white', 3.2, 39],
    [58, False, True, False, 129, 'female', 80, 160, 'white', 3.7, 39],
    [58, False, False, True, 129, 'female', 80, 160, 'white', 2.2, 39],
    [58, True, True, False, 129, 'female', 80, 160, 'white', 7.0, 50],  # source report 7.1?
    [58, False, True, True, 129, 'female', 80, 160, 'white', 5.0, 50],
    [58, True, False, True, 129, 'female', 80, 160, 'white', 4.3, 50],
    [58, True, True, True, 129, 'female', 80, 160, 'white', 9.4, 50],

    # white male
    [58, False, False, False, 90, 'male', 100, 130, 'white', 1.5, 5],
    [58, False, False, False, 129, 'male', 80, 160, 'white', 4.1, 36],
    [58, True, False, False, 129, 'male', 80, 160, 'white', 7.8, 50],  # 7.7?
    [58, False, True, False, 129, 'male', 80, 160, 'white', 7.0, 50],
    [58, False, False, True, 129, 'male', 80, 160, 'white', 4.8, 50],

    # black female
    [58, False, False, False, 90, 'female', 100, 130, 'aa', 0.6, 8],
    [58, False, False, False, 129, 'female', 80, 160, 'aa', 2.7, 27],
    [58, True, False, False, 129, 'female', 80, 160, 'aa', 6.3, 39],
    [58, False, True, False, 129, 'female', 80, 160, 'aa', 5.3, 39],
    [58, False, False, True, 129, 'female', 80, 160, 'aa', 3.8, 39],

    # black male
    [58, False, False, False, 90, 'male', 100, 130, 'aa', 2.9, 5],
    [58, False, False, False, 129, 'male', 80, 160, 'aa', 6.2, 36],
    [58, True, False, False, 129, 'male', 80, 160, 'aa', 11.6, 50],
    [58, False, True, False, 129, 'male', 80, 160, 'aa', 10.5, 50],  # 10.6?
    [58, False, False, True, 129, 'male', 80, 160, 'aa', 10.2, 50],  # 10.3?
]


@pytest.mark.parametrize("d", test_data)
def test_valueset(d):
    a = ASCVD(
        age=d[0],
        diabetic=d[1],
        smoker=d[2],
        hypertensive=d[3],
        systolic=d[4],
        gender=d[5],
        hdl=d[6],
        total_cholesterol=d[7],
        race=d[8]
    )

    assert d[9] == a.compute_ten_year_score()
    assert d[10] == a.compute_lifetime_risk()

    if (d[2]):
        a.compute_ten_year_risk_reduction(quit_smoking=True)


def test_calc_table_a_1():
    a = ASCVD(
        age=55,
        diabetic=False,
        smoker=False,
        hypertensive=False,
        systolic=120,
        gender='female',
        hdl=50,
        total_cholesterol=213,
        race="white"
    )

    is_calc_correct(a, a._calc_age_value, -119.41)
    is_calc_correct(a, a._calc_age_squared_value, 78.43)  # Table has .44
    is_calc_correct(a, a._calc_cholesterol_value, 72.59)
    is_calc_correct(a, a._calc_cholesterol_age_value, -66.90)  # Table has .91
    is_calc_correct(a, a._calc_hdl_value, -53.12)
    is_calc_correct(a, a._calc_hdl_age_value, 49.37)
    is_calc_correct(a, a._calc_treated_systolic_value, 0.0)
    is_calc_correct(a, a._calc_treated_systolic_age_value, 0.0)
    is_calc_correct(a, a._calc_untreated_systolic_value, 9.37)
    is_calc_correct(a, a._calc_untreated_systolic_age_value, 0.0)
    is_calc_correct(a, a._calc_smoker_value, 0.0)
    is_calc_correct(a, a._calc_smoker_age_value, 0.0)
    is_calc_correct(a, a._calc_diabetic_value, 0.0)

    assert a._sum_of_calcs() == -29.67


def test_calc_table_a_2():
    a = ASCVD(
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

    is_calc_correct(a, a._calc_age_value, 68.58)
    is_calc_correct(a, a._calc_age_squared_value, 0.0)
    is_calc_correct(a, a._calc_cholesterol_value, 5.04)
    is_calc_correct(a, a._calc_cholesterol_age_value, 0.0)
    is_calc_correct(a, a._calc_hdl_value, -74.01)
    is_calc_correct(a, a._calc_hdl_age_value, 70.15)
    is_calc_correct(a, a._calc_treated_systolic_value, 0.0)
    is_calc_correct(a, a._calc_treated_systolic_age_value, 0.0)
    is_calc_correct(a, a._calc_untreated_systolic_value, 133.19)
    is_calc_correct(a, a._calc_untreated_systolic_age_value, -116.79)
    is_calc_correct(a, a._calc_smoker_value, 0.0)
    is_calc_correct(a, a._calc_smoker_age_value, 0.0)
    is_calc_correct(a, a._calc_diabetic_value, 0.0)

    assert a._sum_of_calcs() == round(86.16, 2)


def test_calc_table_a_3():
    a = ASCVD(
        age=55,
        diabetic=False,
        smoker=False,
        hypertensive=False,
        systolic=120,
        gender='male',
        hdl=50,
        total_cholesterol=213,
        race="white"
    )

    is_calc_correct(a, a._calc_age_value, 49.47)
    is_calc_correct(a, a._calc_age_squared_value, 0.0)
    is_calc_correct(a, a._calc_cholesterol_value, 63.55)
    is_calc_correct(a, a._calc_cholesterol_age_value, -57.23)  # Table is .24
    is_calc_correct(a, a._calc_hdl_value, -31.26)
    is_calc_correct(a, a._calc_hdl_age_value, 27.73)
    is_calc_correct(a, a._calc_treated_systolic_value, 0.0)
    is_calc_correct(a, a._calc_treated_systolic_age_value, 0.0)
    is_calc_correct(a, a._calc_untreated_systolic_value, 8.45)
    is_calc_correct(a, a._calc_untreated_systolic_age_value, 0.0)
    is_calc_correct(a, a._calc_smoker_value, 0.0)
    is_calc_correct(a, a._calc_smoker_age_value, 0.0)
    is_calc_correct(a, a._calc_diabetic_value, 0.0)

    assert a._sum_of_calcs() == round(60.71, 2)  # table is .69


def test_calc_table_a_4():
    a = ASCVD(
        age=55,
        diabetic=False,
        smoker=False,
        hypertensive=False,
        systolic=120,
        gender='male',
        hdl=50,
        total_cholesterol=213,
        race='aa'
    )

    is_calc_correct(a, a._calc_age_value, 9.89)
    is_calc_correct(a, a._calc_age_squared_value, 0.0)
    is_calc_correct(a, a._calc_cholesterol_value, 1.62)
    is_calc_correct(a, a._calc_cholesterol_age_value, 0.0)
    is_calc_correct(a, a._calc_hdl_value, -1.20)
    is_calc_correct(a, a._calc_hdl_age_value, 0.0)
    is_calc_correct(a, a._calc_treated_systolic_value, 0.0)
    is_calc_correct(a, a._calc_treated_systolic_age_value, 0.0)
    is_calc_correct(a, a._calc_untreated_systolic_value, 8.66)
    is_calc_correct(a, a._calc_untreated_systolic_age_value, 0.0)
    is_calc_correct(a, a._calc_smoker_value, 0.0)
    is_calc_correct(a, a._calc_smoker_age_value, 0.0)
    is_calc_correct(a, a._calc_diabetic_value, 0.0)

    assert a._sum_of_calcs() == round(18.97, 2)

def is_calc_correct(a, fn, val):
    assert round(val, 2) == fn(a._coefficients())


def test_too_old():
    with pytest.raises(ValueError) as excinfo:
        ASCVD(
            age=80,
            diabetic=False,
            smoker=False,
            hypertensive=False,
            systolic=120,
            gender='male',
            hdl=50,
            total_cholesterol=213,
            race='aa'
        )
    assert 'Invalid age:' in str(excinfo.value)


def test_too_young():
    with pytest.raises(ValueError) as e:
        ASCVD(
            age=39,
            diabetic=False,
            smoker=False,
            hypertensive=False,
            systolic=120,
            gender='male',
            hdl=50,
            total_cholesterol=213,
            race='aa'
        )
    assert 'Invalid age:' in str(e.value)


def test_valid_ages():
    i_am_of_age = True


    for i in range(40, 60):
        ASCVD(
            age=i,
            diabetic=False,
            smoker=False,
            hypertensive=False,
            systolic=120,
            gender='male',
            hdl=50,
            total_cholesterol=213,
            race='aa'
        )
    # an invalid age would raise ValueError and the assert below would never be hit.
    assert i_am_of_age
