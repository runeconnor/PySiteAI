"""
Generates list of prompts for generating profile images via generative ai (like Leonardo.ai)
"""

import random

ages = [20, 30, 40, 50]
countries = ["China","India","United States","Germany","Kenya",
             "Sweden","Russia","Japan","Philippines",
             "Congo","Germany","Thailand",
             "United Kingdom","Italy","Scotland",
             "South Korea","Spain"]
professions = ["Doctor","Software Developer","Veterinarian",
               "Mechanical Engineer","Civil Engineer","Financial Advisor","Lawyer",
               "School Teacher","Laboratory Technician",
               "Hairdresser","Bus Driver","Restaurant Cook",
               "Architect","Plumber","Art Director","Auto Mechanic",
               "Receptionist","Sports Coach","Janitor","Electrician","Truck Driver",
               "Carpenter","Security Guard","Construction Worker"]
backgrounds = ["Park","Forest","City","Office","Home","Workshop","Cafe","Mountain","Coast"]

prompts = {
    'f': [],
    'm': []
}
for age in ages:
    for country in countries:
        for profession in professions:
            for background in backgrounds:
                prompt_f = f"{age} year old modern woman from {country}. {profession}. Smiling. {background} background. Realistic."
                prompt_m = f"{age} year old modern man from {country}. {profession}. Smiling. {background} background. Realistic."
                prompts['f'].append(prompt_f)
                prompts['m'].append(prompt_m)

random.shuffle(prompts['f'])
random.shuffle(prompts['m'])

with open('profile_image_prompts_female.txt', 'w', encoding='utf-8') as f:
    for prompt in prompts['f']:
        f.write(prompt + "\n")

with open('profile_image_prompts_male.txt', 'w', encoding='utf-8') as f:
    for prompt in prompts['m']:
        f.write(prompt + "\n")
