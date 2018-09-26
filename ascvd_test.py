import pytest

from ascvd import ASCVD

# A - http://tools.acc.org/ASCVD-Risk-Estimator-Plus/#!/calculate/estimate/

def setup():
    return [
        # white female
        [58, False, False, False, 129, 'female', 80, 160, 'white', 1.7, 27],
        [58, True, False, False, 129, 'female', 80, 160, 'white', 3.2, 39],
        [58, False, True, False, 129, 'female', 80, 160, 'white', 3.7, 39],
        [58, False, False, True, 129, 'female', 80, 160, 'white', 2.3, 39], # A reports 2.2
        [58, True, True, False, 129, 'female', 80, 160, 'white', 7.1, 27],  # A reports 50
        [58, False, True, True, 129, 'female', 80, 160, 'white', 5.0, 50],
        [58, True, False, True, 129, 'female', 80, 160, 'white', 4.3, 50],
        [58, True, True, True, 129, 'female', 80, 160, 'white', 9.5, 50],   # A reports 9.4

        # white male
        [58, False, False, False, 129, 'male', 80, 160, 'white', 4.1, 36],
        [58, True, False, False, 129, 'male', 80, 160, 'white', 7.7, 50],
        [58, False, True, False, 129, 'male', 80, 160, 'white', 7.0, 50],
        [58, False, False, True, 129, 'male', 80, 160, 'white', 4.8, 50],

        # black female
        [58, False, False, False, 129, 'female', 80, 160, 'aa', 2.7, 27],
        [58, True, False, False, 129, 'female', 80, 160, 'aa', 6.3, 39],
        [58, False, True, False, 129, 'female', 80, 160, 'aa', 5.3, 39],
        [58, False, False, True, 129, 'female', 80, 160, 'aa', 3.8, 39],

        # black male
        [58, False, False, False, 129, 'male', 80, 160, 'aa', 6.2, 36],
        [58, True, False, False, 129, 'male', 80, 160, 'aa', 11.6, 50],
        [58, False, True, False, 129, 'male', 80, 160, 'aa', 10.6, 50],
        [58, False, False, True, 129, 'male', 80, 160, 'aa', 10.3, 50],
    ]


def test_it():
    for d in setup():
        a = ASCVD()
        a.age = d[0]
        a.diabetic = d[1]
        a.smoker = d[2]
        a.hypertensive = d[3]
        a.systolic = d[4]
        a.gender = d[5]
        a.hdl = d[6]
        a.total_cholesterol = d[7]
        a.race = d[8]

        #assert a.compute_ten_year_score() == d[9]
        assert a.compute_lifetime_risk() == d[10]


def test_too_old():
    with pytest.raises(ValueError) as excinfo:
        a = ASCVD()
        a.age = 80
    assert 'Invalid age:' in str(excinfo.value)


def test_too_young():
    with pytest.raises(ValueError) as e:
        a = ASCVD()
        a.age = 39
    assert 'Invalid age:' in str(e.value)


def test_valid_ages():
    i_am_of_age = True

    a = ASCVD()

    for i in range(40, 60):
        a.age = i
    # an invalid age would raise ValueError and the assert below would never be hit.
    assert i_am_of_age
