import streamlit as st
import nltk
from transformers import pipeline
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

chatbot = pipeline("text-generation",model='distilgpt2')

def healthcare_chatbot(user_input):
    if "symptom" in user_input:
        return "Please consult doctor"
    elif "appointment" in user_input:
        return "Would you like to schedule your appointment?"
    elif "meditation" in user_input:
        return "It's important to take prescribe medicines regulary."
    else:
        response = chatbot(user_input,max_length = 300,num_return_sequences=1)
        return response[0]['generated_text']
    return ""

def main():
    st.title("AI Healthcare Chatbot")
    user_input = st.text_input("How can i assit you today?")
    if st.button("Submit"):
        if user_input:
            st.write("User:",user_input)
            with st.spinner("Processiong your query.... plz wait"):
                response=healthcare_chatbot(user_input)
            st.write("Healthcare Assistant :" , response)

        else:
            st.write("Please enter message to get response.")    


if __name__=="__main__":
    main()