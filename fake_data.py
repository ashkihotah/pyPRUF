import pandas as pd
import random
from faker import Faker

fake = Faker()
Faker.seed(0)

# Helper function to calculate age from birthday
def calculate_age(birthdate):
    today = pd.Timestamp.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

# Generate a list of 1000 fake people
def get_fake_people_df(n: int):
    people = []
    for _ in range(n):
        name = fake.first_name()
        surname = fake.last_name()
        birthday = fake.date_of_birth(minimum_age=18, maximum_age=90)
        age = calculate_age(birthday)
        city = fake.city()
        gender = random.choice(["Male", "Female"])
        height_cm = random.randint(150, 200)
        weight_kg = random.randint(50, 100)
        
        people.append({
            "Names": name,
            "Surnames": surname,
            "Birthdays": birthday,
            "Ages": age,
            "Cities": city,
            "Genders": gender,
            "Heights_cm": height_cm,
            "Weights_kg": weight_kg
        })

    # Create a DataFrame from the list
    df = pd.DataFrame(people)
    return df
