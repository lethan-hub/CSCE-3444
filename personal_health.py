class PersonalHealth:
  def __init__(self,name,age,gender,height_cm,weight_kg):
    self.name = name
    self.age = age
    self.gender = gender
    self.height_cm = height_cm
    self.weight_kg = weight_kg
    self.bmi = self.calculate_bmi()
    self.status = self.health_status()

  def calculate_bmi(self):
    height_m = self.height_cm / 100
    return round(self.weight_kg / (height_m ** 2), 2)
  
  def health_status(self):
    bmi = self.bmi
    if bmi < 18.5:
      return "Underweight"
    elif 18.5 <= bmi < 24.9:
      return "Normal weight"
    elif 25<= bmi < 29.9:
      return "Overweight"
    else:
      return "Obese"

    def update_weight(self, new_weight_kg):
      self.weight_kg = new_weight_kg
      self.bmi = self.calculate_bmi()
      self.status = self.health_status()

    def profile(self):
      return {
          "Name" : self.name,
          "Age" : self.age,
          "Gender" : self.gender,
          "Height (cm)" : self.height_cm,
          "Weight (kg)" : self.weight_kg,
          "BMI" : self.bmi,
          "Health Status" : self.status
      }
