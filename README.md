  # 🩺 Healthcare Chatbot for Disease Prediction

A deep learning-powered healthcare assistant designed to help users identify potential medical conditions based on symptom descriptions. Built with **Flask**, **TensorFlow**, and **NLTK**, this chatbot uses natural language processing to understand user input and provide relevant medical guidance.

---

## 🚀 Features

- **Symptom Recognition**: Uses NLP to parse and understand medical symptoms described in plain English.
- **Deep Learning Engine**: Powered by a TensorFlow/Keras model (`.h5`) for high-accuracy intent classification.
- **Dynamic Interaction**: Interactive web interface for seamless diagnostic conversations.
- **Extensible Architecture**: Easy-to-update `intents.json` for adding new diseases and response patterns.

---

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **Machine Learning**: TensorFlow, Keras, NumPy
- **Natural Language Processing**: NLTK (WordNet Lemmatizer, Tokenization)
- **Frontend**: HTML5, CSS3, JavaScript

---

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Amreen-vnrvjiet/Talking-Chatbot-for-Healthcare-using-Deep-Learning.git
   cd Talking-Chatbot-for-Healthcare-using-Deep-Learning
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```
   The app will be available at `http://localhost:5000`.

---

## 📂 Project Structure

- `app.py`: The Main Flask application and API logic.
- `intents.json`: Data source containing symptoms, tags, and responses.
- `chatbot_model.h5`: Pre-trained TensorFlow model for intent prediction.
- `words.pkl` & `classes.pkl`: Serialized data files for model preprocessing.
- `static/`: Frontend assets (CSS, JS).
- `templates/`: HTML templates for the web interface.

---

## ⚠️ Disclaimer

**This chatbot is for educational purposes only.** It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health providers with any questions you may have regarding a medical condition.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
