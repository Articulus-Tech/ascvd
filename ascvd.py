from math import *


class ASCVD:

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, val):
        if val < 40 or val > 79:
            raise ValueError('Invalid age: ' + str(val) + ' - Age must be between 40 and 79')
        self.__age = val

    @property
    def total_cholesterol(self):
        return self.__total_chol

    @total_cholesterol.setter
    def total_cholesterol(self, val):
        if val < 130 or val > 320:
            raise ValueError('Invalid value: ' + str(val) + ' - Total Cholesterol must be between 130 and 320')
        self.__total_chol = val

    @property
    def hdl(self):
        return self.__hdl

    @hdl.setter
    def hdl(self, val):
        if val < 20 or val > 100:
            raise ValueError("Invalid value: " + str(val) + ' - HDL must be between 20 and 100')
        self.__hdl = val

    @property
    def hypertensive(self):
        return self.__hypertensive

    @hypertensive.setter
    def hypertensive(self, val):
        self.__hypertensive = val

    @property
    def systolic(self):
        return self.__systolic

    @systolic.setter
    def systolic(self, val):
        if val < 90 or val > 200:
            raise ValueError("Invalid value: " + str(val) + ' - Systolic must be between 90 and 200')
        self.__systolic = val

    @property
    def smoker(self):
        return self.__smoker

    @smoker.setter
    def smoker(self, val):
        self.__smoker = val

    @property
    def race(self):
        return self.__race

    @race.setter
    def race(self, val):
        self.__race = val

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, val):
        self.__gender = val

    @property
    def diabetic(self):
        return self.__diabetic

    @diabetic.setter
    def diabetic(self, val):
        self.__diabetic = val

    # is_male, is_aa
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
        'aa_female': {  ## todo why different from paper
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
        if self.age < 40 or self.age > 79:
            return 0

        who = self.who()

        predict_ret = self.sum_of_calcs()
        pct = (1 - (self.baseline_survival[who] ** exp(predict_ret - self.mnxb[who])))
        return round((pct * 100), 1)

    # Table A calculations
    def sum_of_calcs(self):
        cof = self.coefficients()

        v = round(
            self.calc_age_value(cof)
            + self.calc_age_squared_value(cof)
            + self.calc_cholesterol_value(cof)
            + self.calc_cholesterol_age_value(cof)
            + self.calc_hdl_value(cof)
            + self.calc_hdl_age_value(cof)
            + self.calc_treated_systolic_value(cof)
            + self.calc_treated_systolic_age_value(cof)
            + self.calc_untreated_systolic_value(cof)
            + self.calc_untreated_systolic_age_value(cof)
            + self.calc_smoker_value(cof)
            + self.calc_smoker_age_value(cof)
            + self.calc_diabetic_value(cof)
            , 2)
        return v

    def calc_diabetic_value(self, cof):
        return round(cof['diabetic_co'] * int(self.diabetic), 2)

    def calc_smoker_age_value(self, cof):
        return round(cof['smoker_age_co'] * log(self.age) * int(self.smoker), 2)

    def calc_smoker_value(self, cof):
        return round(cof['smoker_co'] * int(self.smoker), 2)

    def calc_untreated_systolic_age_value(self, cof):
        return round(cof['untreated_systolic_age_co'] * log(self.age) * log(self.systolic) * int(not self.hypertensive), 2)

    def calc_untreated_systolic_value(self, cof):
        return round(cof['untreated_systolic_co'] * log(self.systolic) * int(not self.hypertensive), 2)

    def calc_treated_systolic_age_value(self, cof):
        return round(
            cof['treated_systolic_age_co'] * log(self.age) * log(self.systolic)  * int(self.hypertensive), 2)

    def calc_treated_systolic_value(self, cof):
        return round(cof['treated_systolic_co'] * log(self.systolic) * int(self.hypertensive), 2)

    def calc_hdl_age_value(self, cof):
        return round(cof['hdl_age_co'] * log(self.age) * log(self.hdl), 2)

    def calc_hdl_value(self, cof):
        return round(cof['hdl_co'] * log(self.hdl), 2)

    def calc_cholesterol_age_value(self, cof):
        return round(cof['chol_age_co'] * log(self.age) * log(self.total_cholesterol), 2)

    def calc_cholesterol_value(self, cof):
        return round(cof['chol_co'] * log(self.total_cholesterol), 2)

    def calc_age_squared_value(self, cof):
        return round(cof['age2_co'] * (log(self.age) ** 2), 2)

    def calc_age_value(self, cof):
        return round(cof['age_co'] * log(self.age), 2)

    def compute_lifetime_risk(self):
        if self.age < 20 or self.age > 59: return 0

        major = (int(self.total_cholesterol >= 240)
                 + int(self.systolic >= 160)
                 + int(self.hypertensive)
                 + int(self.smoker)
                 + int(self.diabetic)
                 )

        elevated = (
                int(self.total_cholesterol >= 200 and self.total_cholesterol < 240)
                + int(self.systolic >= 140 and self.systolic < 160 and not self.hypertensive)
        )


        all_optimal = (
                          int(
                              (int(self.total_cholesterol < 180)
                               + (int(self.systolic < 120) * int(not self.hypertensive)) == 2)
                          )) * 1 if (major == 0) else 0

        not_optimal = int(
            int(self.total_cholesterol >= 180 and self.total_cholesterol < 200)
            + (int(self.systolic >= 120 and self.systolic < 140 and not self.hypertensive))
            * int(int(elevated == 0) * int(major == 0)) >= 1)

        ascvd_risk = self.get_ascvd_risk(all_optimal, elevated, major, not_optimal)

        return ascvd_risk


    def get_ascvd_risk(self, all_optimal, elevated, major, not_optimal):
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


    def who(self):
        return self.whom[self.race == 'aa'][self.gender == 'male']

    def coefficients(self):
        return self.coefficient_table[self.who()]


a = ASCVD()
a.age = 58
a.diabetic = False
a.smoker = False
a.hypertensive = True
a.systolic = 129
a.gender = 'female'
a.hdl = 80
a.total_cholesterol = 160
a.race = "aa"

v =  a.compute_lifetime_risk() # table is .69
ten = a.compute_ten_year_score()
print(v)
print(ten)