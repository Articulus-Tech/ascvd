
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

    def compute_ten_year_score(self):
        if self.age < 40 or self.age > 79:
            return 0


        self.calculate_base()

        s010_ret = 0.0
        mnxb_ret = 0.0
        predict_ret = 0.0

        if self.is_aa and not self.is_male:
            mnxb_ret, predict_ret, s010_ret = self.is_aa_female()
        elif not self.is_aa and not self.is_male:
            mnxb_ret, predict_ret, s010_ret = self.not_aa_female()
        elif self.is_aa and self.is_male:
            mnxb_ret, predict_ret, s010_ret = self.is_aa_male()
        else:
            mnxb_ret, predict_ret, s010_ret = self.is_not_aa_male()

        pct = (1 - (s010_ret ** exp(predict_ret - mnxb_ret)))
        return round((pct * 100), 1)

    def is_not_aa_male(self):
        s010_ret = 0.91436
        mnxb_ret = 61.1816
        predict_ret = ((12.344 * self.log_age)
                      + 11.853 * self.log_total_chol
                      + -2.664 * self.age_total_chol
                      + -7.99 * self.log_hdl
                      + 1.769 * self.age_hdl
                      + 1.797 * self.trlnsbp
                      + 1.764 * self.ntlnsbp
                      + 7.837 * int(self.smoker)
                      + -1.795 * self.age_smoke
                      + 0.658 * int(self.diabetic)
                      )
        return mnxb_ret, predict_ret, s010_ret

    def is_aa_male(self):
        s010_ret = 0.89536
        mnxb_ret = 19.5425
        predict_ret = ((2.469 * self.log_age)
                      + (0.302 * self.log_total_chol)
                      + (-0.307 * self.log_hdl)
                      + (1.916 * self.trlnsbp)
                      + (1.809 * self.ntlnsbp)
                      + (0.549 * int(self.smoker))
                      + (0.645 * int(self.diabetic))
                      )
        return mnxb_ret, predict_ret, s010_ret

    def is_aa_female(self):
        s010_ret = 0.95334
        mnxb_ret = 86.6081
        predict_ret = (
                (17.1141 * self.log_age)
                + (0.9396 * self.log_total_chol)
                + (-18.9196 * self.log_hdl)
                + (4.4748 * self.age_hdl)
                + (29.2907 * self.trlnsbp)
                + (-6.4321 * self.age_tsbp)
                + (27.8197 * self.ntlnsbp)
                + (-6.0873 * self.age_ntsbp)
                + (0.6908 * int(self.smoker))
                + (0.8738 * int(self.diabetic))
        )
        return mnxb_ret, predict_ret, s010_ret

    def not_aa_female(self):
        s010_ret = 0.96652
        mnxb_ret = -29.1817
        predict_ret = ((-29.799 * self.log_age)
                      + (4.884 * (self.log_age ** 2))
                      + (13.54 * self.log_total_chol)
                      + (-3.114 * self.age_total_chol)
                      + (-13.578 * self.log_hdl)
                      + (3.149 * self.age_hdl)
                      + (2.019 * self.trlnsbp)
                      + (1.957 * self.ntlnsbp)
                      + (7.574 * int(self.smoker))
                      + (-1.665 * self.age_smoke)
                      + (0.661 * int(self.diabetic))
                      )
        return mnxb_ret, predict_ret, s010_ret


    def compute_lifetime_risk(self):
        if self.age < 20 or self.age > 59: return 0

        ascvd_risk = 0.0
        all_optimal = 0
        not_optimal = 0.0
        elevated = 0

        major = (int(self.total_cholesterol >= 240)
                 + int(self.systolic >= 160)
                 + int(self.hypertensive)
                 + int(self.smoker)
                 + int(self.diabetic)
                 )

        if major != 1:
            elevated = (
                    int(self.total_cholesterol >= 200 and self.total_cholesterol < 240)
                    + int(self.systolic >= 140 and self.systolic < 160 and not self.hypertensive)
            )

            # todo this is far from optimal!
            all_optimal = (
                int(
                    (int(self.total_cholesterol < 180) + (int(self.systolic < 120) * int(not self.hypertensive)) == 2)
                ))

            if not elevated:
                not_optimal = int(
                    int(self.total_cholesterol >= 180 and self.total_cholesterol < 200)
                    or (int(self.systolic >= 120 and self.systolic < 140 and not self.hypertensive))
                )

        ascvd_risk = self.get_ascvd_risk(all_optimal, ascvd_risk, elevated, major, not_optimal)

        return ascvd_risk


    def get_ascvd_risk(self, all_optimal, ascvd_risk, elevated, major, not_optimal):
        params = self.set_params()

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


    def set_params(self):
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
        return params

    def calculate_base(self):
        self.log_age = log(self.age)
        self.log_total_chol = log(self.total_cholesterol)
        self.log_hdl = log(self.hdl)
        self.trlnsbp = log(self.systolic) if self.hypertensive else 0.0
        self.ntlnsbp = 0.0 if self.hypertensive else log(self.systolic)
        self.age_total_chol = self.log_age * self.log_total_chol
        self.age_hdl = self.log_age * self.log_hdl
        self.age_tsbp = self.log_age * self.trlnsbp
        self.age_ntsbp = self.log_age * self.ntlnsbp
        self.age_smoke = self.log_age if self.smoker else 0
        self.is_aa = self.race == 'aa'
        self.is_male = self.gender == 'male'



