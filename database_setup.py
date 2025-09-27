# import sqlite3

# # Connect / create database
# conn = sqlite3.connect("health.db")
# cursor = conn.cursor()

# # -------------------------------
# # Create tables
# # -------------------------------
# # Table for health data
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS health_data (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     symptoms TEXT NOT NULL,
#     disease TEXT NOT NULL,
#     advice TEXT NOT NULL
# )
# """)

# # # For login 

# # cursor.execute("""
# # CREATE TABLE IF NOT EXISTS users (
# #     id INTEGER PRIMARY KEY AUTOINCREMENT,
# #     username TEXT UNIQUE NOT NULL,
# #     password TEXT NOT NULL
# # )
# # """)
# # conn.commit()

# # Table for admin users
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS admin_users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     username TEXT UNIQUE NOT NULL,
#     password TEXT NOT NULL
# )
# """)

# # -------------------------------
# # Insert sample health data
# # -------------------------------
# # Clear existing data to avoid duplicates on re-run
# cursor.execute("DELETE FROM health_data")

# sample_data = [
#     ("fever, cough, tiredness", "Flu", "Take rest, drink fluids, and consult a doctor if severe."),
#     ("chest pain, shortness of breath", "Heart Disease", "Seek immediate medical help immediately."),
#     ("frequent urination, increased thirst", "Diabetes", "Monitor blood sugar and consult a doctor."),
#     ("sneezing, itchy eyes, runny nose", "Allergy", "Avoid allergens and take antihistamines."),
#     ("headache, nausea, light sensitivity", "Migraine", "Rest in a dark room, take prescribed medicine."),
#     ("fever, body pain, weakness", "Dengue", "Stay hydrated, rest, and consult a doctor for blood tests."),
#     ("sore throat, cough, runny nose", "Cold", "Rest, drink warm fluids, and take cough medicine if necessary."),
#     ("vomiting, stomach pain, diarrhea", "Food Poisoning", "Drink plenty of water, eat light food, consult a doctor if severe."),
#     ("joint pain, fatigue, rash", "Chikungunya", "Rest, drink fluids, and take prescribed pain relievers."),
#     ("fever, rash, red eyes", "Measles", "Isolate, drink fluids, and consult a doctor."),
#     ("yellow skin, fatigue, dark urine", "Jaundice", "Consult a doctor for liver function tests and follow their advice on diet and rest."),
#     ("persistent cough, chest pain, weight loss", "Tuberculosis", "Seek medical attention immediately for proper diagnosis and treatment with antibiotics."),
#     ("high fever, headache, stomach pain", "Typhoid", "Consult a doctor for diagnosis. Requires antibiotic treatment and proper hydration.")
# ]

# cursor.executemany("INSERT INTO health_data (symptoms, disease, advice) VALUES (?, ?, ?)", sample_data)

# # -------------------------------
# # Insert default admin
# # -------------------------------
# # Using INSERT OR IGNORE to prevent an error if the admin already exists
# cursor.execute("INSERT OR IGNORE INTO admin_users (username, password) VALUES (?, ?)", ("admin", "admin123"))

# # -------------------------------
# # Commit and close
# # -------------------------------
# conn.commit()
# conn.close()

# print("✅ Database setup complete! Admin -> (username=admin, password=admin123)")




#--------------------------------------------------------------------------------------------




import sqlite3

# Connect / create database
conn = sqlite3.connect("health.db")
cursor = conn.cursor()

# -------------------------------
# Create tables
# -------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS health_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symptoms TEXT NOT NULL,
    disease TEXT NOT NULL,
    advice TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS admin_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# -------------------------------
# Insert a much larger set of health data
# -------------------------------
# Clear existing data to avoid duplicates on re-run
cursor.execute("DELETE FROM health_data")

# New, greatly expanded list of diseases and symptoms
comprehensive_data = [
    # Infections & Viruses
    ("fever, cough, tiredness, body aches", "Flu (Influenza)", "Rest, drink plenty of fluids, and consider over-the-counter pain relievers."),
    ("sore throat, runny nose, sneezing, mild cough", "Common Cold", "Stay hydrated, use saline nasal sprays, and get plenty of rest."),
    ("high fever, headache, rash, muscle and joint pains", "Dengue Fever", "Seek medical advice. Rest and fluid intake are crucial. Avoid aspirin."),
    ("fever, sore throat, swollen lymph nodes, extreme fatigue", "Mononucleosis (Glandular Fever)", "Rest is key. Avoid strenuous activities. Gargle with salt water for sore throat."),
    ("fever, itchy rash with blisters, headache", "Chickenpox", "Avoid scratching. Use calamine lotion and take oatmeal baths to soothe itching."),
    ("cough with phlegm, fever, chills, difficulty breathing", "Pneumonia", "See a doctor immediately. Antibiotics are likely needed. Rest and fluids are important."),
    ("painful urination, frequent urge to urinate, cloudy urine", "Urinary Tract Infection (UTI)", "Drink lots of water to flush bacteria. See a doctor for antibiotics."),
    ("diarrhea, vomiting, stomach cramps, nausea", "Gastroenteritis (Stomach Flu)", "Stay hydrated with clear liquids (water, broth). Gradually reintroduce bland foods (BRAT diet)."),
    ("red, itchy, watery eyes, discharge", "Conjunctivitis (Pink Eye)", "Wash hands frequently. Use a clean, warm compress. See a doctor for antibiotic eye drops if bacterial."),
    ("fever, cough, shortness of breath, loss of taste or smell", "COVID-19", "Isolate to prevent spread. Monitor symptoms. Consult a doctor for treatment options."),

    # Chronic Conditions
    ("frequent urination, increased thirst, unexplained weight loss, fatigue", "Type 1 Diabetes", "Requires medical diagnosis and insulin therapy. Monitor blood sugar levels closely."),
    ("increased thirst, frequent urination, hunger, fatigue, blurred vision", "Type 2 Diabetes", "Consult a doctor for management plan, which may include diet, exercise, and medication."),
    ("high blood pressure reading, often no symptoms, sometimes headache or dizziness", "Hypertension (High Blood Pressure)", "Regularly monitor blood pressure. Adopt a low-salt diet, exercise, and take prescribed medication."),
    ("wheezing, shortness of breath, chest tightness, coughing", "Asthma", "Use prescribed inhalers. Identify and avoid triggers. Have an action plan for attacks."),
    ("joint pain, stiffness, swelling, especially in the morning", "Rheumatoid Arthritis", "Consult a rheumatologist. Treatment involves medication and physical therapy."),
    ("fatigue, pale skin, weakness, shortness of breath, cold hands and feet", "Anemia (Iron Deficiency)", "Increase iron-rich foods in diet (red meat, spinach). A doctor may prescribe iron supplements."),
    ("abdominal pain, bloating, diarrhea, constipation", "Irritable Bowel Syndrome (IBS)", "Manage diet to identify and avoid trigger foods. Manage stress."),

    # Skin Conditions
    ("red, itchy, inflamed skin, dry patches", "Eczema (Atopic Dermatitis)", "Moisturize skin regularly. Avoid harsh soaps and irritants. A doctor may prescribe steroid creams."),
    ("red patches of skin with thick, silvery scales, itching, burning", "Psoriasis", "Consult a dermatologist. Treatments include topical creams, light therapy, and medications."),
    ("facial redness, flushing, visible blood vessels, bumps", "Rosacea", "Identify and avoid triggers (sun, spicy food). Use gentle skincare. A doctor may prescribe topical medications."),
    ("widespread muscle pain and tenderness, fatigue, sleep problems", "Fibromyalgia", "Management includes a combination of exercise, stress management, and medication. See a doctor."),

    # Neurological & Mental Health
    ("severe throbbing headache, nausea, sensitivity to light and sound", "Migraine", "Rest in a dark, quiet room. Use over-the-counter or prescription medication as advised by a doctor."),
    ("persistent sadness, loss of interest, changes in sleep or appetite, fatigue", "Depression", "Seek help from a mental health professional. Therapy and/or medication can be very effective."),
    ("excessive worry, restlessness, feeling on-edge, difficulty concentrating", "Generalized Anxiety Disorder", "Therapy, mindfulness techniques, and sometimes medication can help manage symptoms. Consult a professional."),
    ("difficulty falling asleep, waking up often during the night, feeling tired upon waking", "Insomnia", "Practice good sleep hygiene: regular schedule, dark room, no screens before bed. Consult a doctor if persistent.")
]

cursor.executemany("INSERT INTO health_data (symptoms, disease, advice) VALUES (?, ?, ?)", comprehensive_data)

# -------------------------------
# Insert default admin
# -------------------------------
cursor.execute("INSERT OR IGNORE INTO admin_users (username, password) VALUES (?, ?)", ("admin", "admin123"))

# -------------------------------
# Commit and close
# -------------------------------
conn.commit()
conn.close()

print("✅ Database setup complete with a greatly expanded dataset! Admin -> (username=admin, password=admin123)")