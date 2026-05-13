from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle
import json
import random
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
import os

app = Flask(__name__)

# Verify downloads
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

# Initialize ML resources globally
lemmatizer = WordNetLemmatizer()
intents = None
words = None
classes = None
model = None

def load_ml_resources():
    global intents, words, classes, model
    try:
        if os.path.exists("intents.json"):
            intents = json.loads(open("intents.json").read())
            words = pickle.load(open("words.pkl", "rb"))
            classes = pickle.load(open("classes.pkl", "rb"))
            model = load_model("chatbot_model.h5")
            print("INFO: All ML resources loaded successfully.")
    except Exception as e:
        print(f"WARNING: Could not load ML models/files. {e}")

load_ml_resources()

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    if not classes:
        return []
    
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    
    # Lowered threshold to 0.1 handles overlapping symptoms (e.g. "fever" -> dengue, malaria, flu)
    ERROR_THRESHOLD = 0.1 
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    if len(intents_list) == 0:
        return "I'm having trouble diagnosing your exact symptoms. Could you describe them with a bit more detail (e.g. 'high fever and joint pain')?"
        
    tag = intents_list[0]['intent']
    for intent in intents_json['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if model is None:
        return jsonify({'reply': 'The AI model is completely offline or missing. Please ensure all model files (.h5, .pkl) exist in the backend folder.'})
        
    data = request.get_json()
    user_text = data.get('message', '')
    if not user_text:
        return jsonify({'reply': 'Please provide a valid message.'})
    
    try:
        predict = predict_class(user_text)
        reply = get_response(predict, intents)
    except Exception as e:
        reply = "An internal error occurred during prediction."
        print(f"Error making prediction: {e}")
        
    return jsonify({'reply': reply})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
