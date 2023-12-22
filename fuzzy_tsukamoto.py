from classes import FuzzyData

class TsukamotoFuzzyLogic:

    def __init__(self):
        self.age_range = [25, 30]
        self.location_range = [0, 1]
        self.experience_range = [0, 12]
        self.skill_range = [0, 3]
        self.ipk_threshold = 3.0
        self.org_range = [0, 1]
    
    # init singleton
    def __new__(cls):
      if not hasattr(cls, 'instance'):
        cls.instance = super(TsukamotoFuzzyLogic, cls).__new__(cls)
      return cls.instance

    def age(self, age):
        if age == 3:
            return 3
        elif age == 2:
            return 2
        elif age == 1:
            return 1

    def fuzzify_location(self, location):
        if location == self.location_range[0]:
            return 0
        elif location == self.location_range[1]:
            return 1

    def fuzzify_experience(self, experience):
        if experience == 1:
            return 1
        elif experience == 2:
            return 2
        elif experience == 3:
            return 3

    def fuzzify_skill(self, skill):
        if skill == 1:
            return 1
        elif skill == 2:
            return 2
        elif skill == 3:
            return 3

    def fuzzify_ipk(self, ipk):
        if org_exp == self.ipk_threshold[0]:
            return 0
        elif org_exp == self.ipk_threshold[1]:
            return 1

    def fuzzify_organizational_exp(self, org_exp):
        if org_exp == self.org_range[0]:
            return 0
        elif org_exp == self.org_range[1]:
            return 1

    def apply_rules(self,fuzzy_data:FuzzyData):
        rule1 = round(fuzzy_data.location)
        rule2 = round(fuzzy_data.age)
        rule3 = round(fuzzy_data.experience)
        rule4 = round(fuzzy_data.skill)
        rule5 = round(fuzzy_data.ipk)
        rule6 = round(fuzzy_data.org_exp)

        # Weighted average for overall suitability with higher weights for specified criteria
        suitability = (((rule1 * 0.1) + (rule2 * 0.05) + (rule3 * 0.3) + (rule4 * 0.25) + (rule5 * 0.1) + (rule6 * 0.2)) / (0.1 + 0.05 + 0.3 + 0.25 + 0.1 + 0.2))
        return round(suitability,2),rule1,rule2,rule3,rule4,rule5,rule6

# Contoh penggunaan:
# age = 20        # Umur di bawah 25 ; 3
# location = 1    # Lokasi di malang(1) : 1
# experience = 0  # Experience di atas 12 : 3
# skill = 4       # Skill di atas 5 : 3
# ipk = 3.50      # IPK > 3 : 1
# org_exp = 1     # Punya organisasi : 1

# tsukamoto = TsukamotoFuzzyLogic()
# hasil = ((tsukamoto.apply_rules(age, location, experience, skill, ipk, org_exp))/2.2)
# rounded_res = round(hasil * 100, 2)
# print(f"Kesesuaian keseluruhan berdasarkan logika fuzzy adalah: {rounded_res}%")
