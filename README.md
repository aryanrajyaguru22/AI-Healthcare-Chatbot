# 🩺 AI Healthcare Chatbot

- A simple yet powerful healthcare chatbot built with Python and Streamlit. 
- This application leverages the Google Gemini API to provide AI-powered symptom analysis and helps users find doctors in major Indian cities.

### Features

__AI Symptom Analysis__: Users can describe their symptoms in natural language to get preliminary information about possible conditions.

__Medicine Suggestions__: The chatbot suggests common over-the-counter remedies based on the provided symptoms.

__Doctor Locator__: Helps users find a list of doctors by selecting a city from a dropdown menu.

__User-Friendly Interface__: A clean and simple UI built with Streamlit for easy interaction.

### Tech Stack
__Backend__: *Python*

__Frontend__: *Streamlit*

__AI Model__: *Google Gemini API (google-generativeai)*

## Setup and Installation
> Follow these steps to set up and run the project on your local machine.

1. Prerequisites
Make sure you have `Python 3.8` or newer installed on your system. 
You can download it from `python.org`.

2. Clone the Repository
First, clone this project's repository to your local machine.

Bash

`git clone https://github.com/aryanrajyaguru22/AI-Healthcare-Chatbot`
`cd AI-Healthcare-chatbot`

3. Create a Virtual Environment
It's highly recommended to create a virtual environment to manage project dependencies.

__*For Windows:*__

Bash

`python -m venv venv`
`venv\Scripts\activate`

__*For macOS/Linux:*__

Bash

`python3 -m venv venv`
`source venv/bin/activate`

4. Install Dependencies
Install all the necessary Python libraries listed in the `requirements.txt` file.

Bash

`pip install -r requirements.txt`

The main dependencies are:

`streamlit`

`google-generativeai`

`python-dotenv`

5. Set Up Your API Key
The application requires a Google Gemini API key to function.

Get your API key from Google AI Studio.

In the project's root directory, create a file named .env.

Open the .env file and add your API key in the following format:

GOOGLE_API_KEY="YOUR_API_KEY_HERE"
Replace "YOUR_API_KEY_HERE" with the key you obtained.

## Note: If you are using the version of the code where the API key is hardcoded, you can skip this step.

## How to Run the Project 

Once the setup is complete, you can run the application with a single command:

Bash

`streamlit run app.py`
Your web browser will automatically open a new tab with the AI Healthcare Chatbot running locally.

File Structure
The project directory is structured as follows:

├── app.py              # The main Streamlit application script
├── requirements.txt    # Lists all Python dependencies
├── .env                # Stores the Google API key (optional, if not hardcoded)
└── README.md           # This readme file


## ⚠️ Disclaimer
## This application is for informational and educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified healthcare provider with any questions you may have regarding a medical condition.