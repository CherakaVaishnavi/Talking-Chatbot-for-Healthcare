import json

# Detailed advice mapping for the most common/critical diseases in your JSON
detailed_advice = {
    "Dengue": " Dengue is a mosquito-borne illness. Measures: 1) Drink plenty of water and ORS to prevent dehydration. 2) Take Paracetamol for fever (Strictly avoid Aspirin or Ibuprofen). 3) Get complete bed rest. Visit a hospital if you experience severe abdominal pain or bleeding.",
    "Flu": " The flu is a contagious respiratory illness. Measures: 1) Get plenty of rest and sleep. 2) Stay warm and hydrated. 3) Take over-the-counter fever reducers if needed. See a doctor if symptoms last more than a week.",
    "Migraine": " Migraines are severe, throbbing headaches. Measures: 1) Rest in a quiet, dark room. 2) Apply a cold compress to your forehead. 3) Stay hydrated and try caffeine in small amounts.",
    "Diabetes": " Diabetes affects how your body uses blood sugar. Measures: 1) Monitor your blood sugar levels regularly. 2) Maintain a strict, low-sugar diet. 3) Exercise daily. Please consult an endocrinologist for a proper treatment plan.",
    "Hypertension": " Hypertension means your blood pressure is physically too high. Measures: 1) Reduce salt (sodium) intake immediately. 2) Avoid stress and practice deep breathing. 3) Monitor your blood pressure and consult a doctor for medication.",
    "Asthma": " Asthma narrows your airways. Measures: 1) Sit upright to breathe easier. 2) Take long, deep breaths. 3) Use your prescribed inhaler. Seek emergency care if your lips turn blue or breathing becomes extremely difficult.",
    "Food Poisoning": " This is caused by eating contaminated food. Measures: 1) Stop eating solid foods until vomiting stops. 2) Drink ORS or clear fluids to replace lost water. 3) Rest. See a doctor if symptoms last more than 48 hours or you see blood.",
    "COVID-19": " COVID-19 is a highly infectious respiratory disease. Measures: 1) Isolate yourself immediately. 2) Wear a mask around others. 3) Monitor your oxygen levels daily using an oximeter, and consult a doctor if the level drops below 94%.",
    "Tuberculosis": " TB is a serious bacterial infection of the lungs. Measures: 1) Cover your mouth when coughing. 2) Isolate yourself. 3) This requires a strict 6-month antibiotic course—visit a pulmonologist urgently.",
    "Heart Attack": " A heart attack is a severe medical emergency where blood flow to the heart is blocked. Measures: 1) Call an ambulance immediately. 2) Do not attempt to drive yourself. 3) Chew an aspirin if you are not allergic while waiting for help.",
    "Kidney Stones": " Hard deposits of minerals and acid salts. Measures: 1) Drink extreme amounts of water (2-3 liters) to help flush the stone out. 2) Take prescribed pain relievers. 3) Visit a urologist if the pain is unbearable.",
    "Typhoid": " Typhoid is a bacterial infection from contaminated food/water. Measures: 1) Stay extremely hydrated. 2) Eat bland, easy-to-digest food. 3) Visit a doctor immediately for a blood test and antibiotics."
}

# Generic advice for all other 100+ diseases
generic_advice = " Measures: 1) Ensure you are well-rested and extremely hydrated. 2) Monitor your symptoms closely over the next 24 hours. 3) Please consult a certified medical professional for a proper diagnosis and treatment plan."

print("Loading intents.json...")
try:
    with open('intents.json', 'r') as file:
        data = json.load(file)

    updates_made = 0
    for intent in data['intents']:
        tag = intent['tag']
        base_response = intent['responses'][0]
        
        # Prevent double-updating if they run the script twice
        if "Measures:" not in base_response:
            if tag in detailed_advice:
                new_response = base_response + detailed_advice[tag]
            else:
                new_response = base_response + generic_advice
                
            intent['responses'] = [new_response]
            updates_made += 1

    with open('intents.json', 'w') as file:
        json.dump(data, file, indent=4)
        
    print(f"Success! Updated {updates_made} diseases with deep explanations and medical measures.")
except Exception as e:
    print(f"Error: {e}")
