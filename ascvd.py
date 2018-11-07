from math import *


class ASCVD:

    def __init__(self, age, gender, race, total_cholesterol, hdl, systolic,
                 hypertensive=False, smoker=False, diabetic=False):

        if age < 40 or age > 79:
            raise ValueError('Invalid age: ', age, ' - Age must be between 40 and 79')

        if total_cholesterol < 130 or total_cholesterol > 320:
            raise ValueError('Invalid value: ', total_cholesterol, ' - Total Cholesterol must be between 130 and 320')

        if hdl < 20 or hdl > 100:
            raise ValueError("Invalid value: ", hdl, ' - HDL must be between 20 and 100')

        if systolic < 90 or systolic > 200:
            raise ValueError("Invalid value: ", systolic, ' - Systolic must be between 90 and 200')

        self.age = age
        self.gender = gender
        self.race = race
        self.total_cholesterol = total_cholesterol
        self.hdl = hdl
        self.systolic = systolic
        self.hypertensive = hypertensive
        self.smoker = smoker
        self.diabetic = diabetic

    whom = {
        True: {
            True: 'aa_male',
            False: 'aa_female'
        },
        False: {
            True: 'male',
            False: 'female'
        }
    }

    baseline_survival = {
        'aa_male': 0.89536,
        'aa_female': 0.95334,
        'male': 0.91436,
        'female': 0.96652
    }

    mnxb = {
        'aa_male': 19.5425,
        'aa_female': 86.6081,
        'male': 61.1816,
        'female': -29.1817
    }

    params = {
        'male': {
            'major2': 69,
            'major1': 50,
            'elevated': 46,
            'notOptimal': 36,
            'allOptimal': 5,
        },
        'female': {
            'major2': 50,
            'major1': 39,
            'elevated': 39,
            'notOptimal': 27,
            'allOptimal': 8,
        },
    }

    # Table A. coefficients
    coefficient_table = {
        'aa_male': {
            'age_co': 2.469,
            'age2_co': 0,
            'chol_co': 0.302,
            'chol_age_co': 0,
            'hdl_co': -0.307,
            'hdl_age_co': 0,
            'treated_systolic_co': 1.916,
            'treated_systolic_age_co': 0,
            'untreated_systolic_co': 1.809,
            'untreated_systolic_age_co': 0,
            'smoker_co': 0.549,
            'smoker_age_co': 0,
            'diabetic_co': 0.645
        },
        'aa_female': {  # todo why different from paper
            'age_co': 17.1141,
            'age2_co': 0,
            'chol_co': 0.9396,
            'chol_age_co': 0,
            'hdl_co': -18.9196,
            'hdl_age_co': 4.4748,
            'treated_systolic_co': 29.2907,
            'treated_systolic_age_co': -6.4321,
            'untreated_systolic_co': 27.8197,
            'untreated_systolic_age_co': -6.0873,
            'smoker_co': 0.6908,
            'smoker_age_co': 0,
            'diabetic_co': 0.8738
        },
        'male': {
            'age_co': 12.344,
            'age2_co': 0,
            'chol_co': 11.853,
            'chol_age_co': -2.664,
            'hdl_co': -7.990,
            'hdl_age_co': 1.769,
            'treated_systolic_co': 1.797,
            'treated_systolic_age_co': 0,
            'untreated_systolic_co': 1.764,
            'untreated_systolic_age_co': 0,
            'smoker_co': 7.837,
            'smoker_age_co': -1.795,
            'diabetic_co': 0.658
        },
        'female': {
            'age_co': -29.799,
            'age2_co': 4.884,
            'chol_co': 13.540,
            'chol_age_co': -3.114,
            'hdl_co': -13.578,
            'hdl_age_co': 3.149,
            'treated_systolic_co': 2.019,
            'treated_systolic_age_co': 0,
            'untreated_systolic_co': 1.957,
            'untreated_systolic_age_co': 0,
            'smoker_co': 7.574,
            'smoker_age_co': -1.665,
            'diabetic_co': 0.661
        }
    }

    def compute_ten_year_score(self):
        predict_ret = self._sum_of_calcs()
        pct = (1 - (self.baseline_survival[self.__who()] ** exp(predict_ret - self.mnxb[self.__who()])))
        return round((pct * 100), 1)

    def compute_lifetime_risk(self):
        if self.age < 20 or self.age > 59:
            return 0

        major = (int(self.total_cholesterol >= 240)
                 + int(self.systolic >= 160)
                 + int(self.hypertensive)
                 + int(self.smoker)
                 + int(self.diabetic))

        elevated = (int(200 <= self.total_cholesterol < 240)
                    + int(140 <= self.systolic < 160 and not self.hypertensive))

        all_optimal = (int(
            (int(self.total_cholesterol < 180)
             + (int(self.systolic < 120) * int(not self.hypertensive)) == 2)
        )) * 1 if (major == 0) else 0

        not_optimal = int(
            int(180 <= self.total_cholesterol < 200)
            + (int(120 <= self.systolic < 140 and not self.hypertensive))
            * int(int(elevated == 0) * int(major == 0)) >= 1)

        ascvd_risk = self.__get_ascvd_risk(all_optimal, elevated, major, not_optimal)

        return ascvd_risk

    def compute_ten_year_risk_reduction(
            self, quit_smoking = False, statin_therapy= False, systolic_improvement = 0, aspirin = False):
        base_score = self.compute_ten_year_score()
        optimal_score = self.compute_optimal_ten_year()
        total_reduced_score = 0

        if (quit_smoking):
            total_reduced_score +=  (base_score * 0.15)

        if (statin_therapy):
            total_reduced_score +=  base_score * 0.25

        if (systolic_improvement > 0):
            total_reduced_score += base_score - (base_score * (0.7 ** ((self.systolic - 140) / 10)))

        if (aspirin):
            total_reduced_score +=  base_score * 0.1

        if (round(base_score - total_reduced_score) <= optimal_score):
            return round (base_score - total_reduced_score)

        return total_reduced_score


    def compute_optimal_ten_year(self):
        return self.__compute_optimal(self.compute_ten_year_score)

    def compute_optimal_lifetime(self):
        return self.__compute_optimal(self.compute_lifetime_risk)

    def __compute_optimal(self, fn):
        t_systolic = self.systolic
        t_total_cholesterol = self.total_cholesterol
        t_hdl = self.hdl
        t_smoker = self.smoker
        t_diabetic = self.diabetic
        t_hypertensive = self.hypertensive

        self.systolic = 90
        self.total_cholesterol = 130
        self.hdl = 100
        self.smoker = False
        self.diabetic = False
        self.hypertensive = False

        predict = fn()

        self.systolic = t_systolic
        self.total_cholesterol = t_total_cholesterol
        self.hdl = t_hdl
        self.smoker = t_smoker
        self.diabetic = t_diabetic
        self.hypertensive = t_hypertensive

        return predict

    # Table A (from 2013 paper) calculations
    def _sum_of_calcs(self):
        cof = self._coefficients()

        return round(
            self._calc_age_value(cof)
            + self._calc_age_squared_value(cof)
            + self._calc_cholesterol_value(cof)
            + self._calc_cholesterol_age_value(cof)
            + self._calc_hdl_value(cof)
            + self._calc_hdl_age_value(cof)
            + self._calc_treated_systolic_value(cof)
            + self._calc_treated_systolic_age_value(cof)
            + self._calc_untreated_systolic_value(cof)
            + self._calc_untreated_systolic_age_value(cof)
            + self._calc_smoker_value(cof)
            + self._calc_smoker_age_value(cof)
            + self._calc_diabetic_value(cof), 2)

    # The following methods could all be embedded in the above. They were separated for testing individual values
    # and matched with values from Table A in the paper
    def _calc_diabetic_value(self, cof):
        return round(cof['diabetic_co'] * int(self.diabetic), 2)

    def _calc_smoker_age_value(self, cof):
        return round(cof['smoker_age_co'] * log(self.age) * int(self.smoker), 2)

    def _calc_smoker_value(self, cof):
        return round(cof['smoker_co'] * int(self.smoker), 2)

    def _calc_untreated_systolic_age_value(self, cof):
        return round(cof['untreated_systolic_age_co']
                     * log(self.age) * log(self.systolic) * int(not self.hypertensive), 2)

    def _calc_untreated_systolic_value(self, cof):
        return round(cof['untreated_systolic_co'] * log(self.systolic) * int(not self.hypertensive), 2)

    def _calc_treated_systolic_age_value(self, cof):
        return round(
            cof['treated_systolic_age_co'] * log(self.age) * log(self.systolic) * int(self.hypertensive), 2)

    def _calc_treated_systolic_value(self, cof):
        return round(cof['treated_systolic_co'] * log(self.systolic) * int(self.hypertensive), 2)

    def _calc_hdl_age_value(self, cof):
        return round(cof['hdl_age_co'] * log(self.age) * log(self.hdl), 2)

    def _calc_hdl_value(self, cof):
        return round(cof['hdl_co'] * log(self.hdl), 2)

    def _calc_cholesterol_age_value(self, cof):
        return round(cof['chol_age_co'] * log(self.age) * log(self.total_cholesterol), 2)

    def _calc_cholesterol_value(self, cof):
        return round(cof['chol_co'] * log(self.total_cholesterol), 2)

    def _calc_age_squared_value(self, cof):
        return round(cof['age2_co'] * (log(self.age) ** 2), 2)

    def _calc_age_value(self, cof):
        return round(cof['age_co'] * log(self.age), 2)

    def __get_ascvd_risk(self, all_optimal, elevated, major, not_optimal):
        params = self.params
        ascvd_risk = 0
        if major > 1:
            ascvd_risk = params[self.gender]['major2']
        if major == 1:
            ascvd_risk = params[self.gender]['major1']
        if elevated == 1:
            ascvd_risk = params[self.gender]['elevated']
        if not_optimal == 1:
            ascvd_risk = params[self.gender]['notOptimal']
        if all_optimal == 1:
            ascvd_risk = params[self.gender]['allOptimal']
        return ascvd_risk

    def __who(self):
        return self.whom[self.race == 'aa'][self.gender == 'male']

    def _coefficients(self):
        return self.coefficient_table[self.__who()]
