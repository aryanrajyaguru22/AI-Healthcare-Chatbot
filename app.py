import streamlit as st
import os
import google.generativeai as genai

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI HealthCare Chatbot",
    page_icon="🩺",
    layout="wide"
)

# --- API CONFIGURATION ---
# The API key is hardcoded. In a production environment, use environment variables.
API_KEY = "AIzaSyBiyu0WGMRtcPBuTZaGdmziMn1FWHfz1R0"

# Configure the generative AI model
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Could not initialize the AI model: {e}", icon="🚨")
    model = None

# --- HARDCODED DOCTOR DATABASE ---
doctors_db = {
    "ahmedabad": [
        # General Physicians
        {"name": "Dr. Aarav Patel", "specialty": "General Physician", "address": "123, C.G. Road, Navrangpura"},
        {"name": "Dr. Meena Shah", "specialty": "General Physician", "address": "24, Sunrise Park, Bodakdev"},
        {"name": "Dr. Rajesh Verma", "specialty": "General Physician", "address": "Opp. Town Hall, Ellisbridge"},
        {"name": "Dr. Sunita Rao", "specialty": "General Physician", "address": "A-101, Galaxy Tower, Vastrapur"},
        {"name": "Dr. Anil Kumar", "specialty": "General Physician", "address": "Near ISKCON Temple, S.G. Highway"},
        # Cardiologists
        {"name": "Dr. Priya Sharma", "specialty": "Cardiologist", "address": "45, Sterling Hospital, Memnagar"},
        {"name": "Dr. Mohan Joshi", "specialty": "Cardiologist", "address": "CIMS Hospital, Science City Road"},
        {"name": "Dr. Kavita Nair", "specialty": "Cardiologist", "address": "UN Mehta Institute of Cardiology, Civil Hospital Campus"},
        # Dermatologists
        {"name": "Dr. Rohan Mehta", "specialty": "Dermatologist", "address": "78, Apollo Hospital, Bhat"},
        {"name": "Dr. Alpa Trivedi", "specialty": "Dermatologist", "address": "SkinFirst Clinic, Prahlad Nagar"},
        {"name": "Dr. Jignesh Kothari", "specialty": "Dermatologist", "address": "305, Shivalik Yash, Naranpura"},
        # Pediatricians
        {"name": "Dr. Sneha Desai", "specialty": "Pediatrician", "address": "9, Anand Complex, Satellite"},
        {"name": "Dr. Rakesh Patel", "specialty": "Pediatrician", "address": "Sunshine Global Hospitals, Maninagar"},
        {"name": "Dr. Falguni Shah", "specialty": "Pediatrician", "address": "Apple Children Hospital, Navrangpura"},
        # Neurologists
        {"name": "Dr. Sudhir Shah", "specialty": "Neurologist", "address": "Zydus Hospital, Thaltej"},
        {"name": "Dr. Keyur Panchal", "specialty": "Neurologist", "address": "Global Hospital, Ambawadi"},
        # Orthopedic Surgeons
        {"name": "Dr. Hitesh Modi", "specialty": "Orthopedic Surgeon", "address": "Shalby Hospitals, S.G. Highway"},
        {"name": "Dr. Tushar Shah", "specialty": "Orthopedic Surgeon", "address": "GCS Medical College, Naroda Road"},
        # Oncologists
        {"name": "Dr. Pankaj Shah", "specialty": "Oncologist", "address": "Gujarat Cancer & Research Institute, Asarwa"},
        {"name": "Dr. Shilin Shukla", "specialty": "Oncologist", "address": "HCG Cancer Centre, Mithakhali"},
        # Gynecologists
        {"name": "Dr. Usha Mehta", "specialty": "Gynecologist", "address": "Bodyline Hospital, Paldi"},
        {"name": "Dr. Vineet Mishra", "specialty": "Gynecologist", "address": "Institute of Kidney Diseases & Research Centre, Civil Hospital"},
        # ENT Specialists
        {"name": "Dr. Kalpesh Patel", "specialty": "ENT Specialist", "address": "Vedanta ENT Hospital, Usmanpura"},
        {"name": "Dr. Deven Shah", "specialty": "ENT Specialist", "address": "Anand Surgical Hospital, Bapunagar"},
        # Psychiatrists
        {"name": "Dr. Himanshu Desai", "specialty": "Psychiatrist", "address": "VIMHANS, Paldi"},
    ],
    "mumbai": [
        # General Physicians
        {"name": "Dr. Vikram Singh", "specialty": "General Physician", "address": "101, Marine Drive, Churchgate"},
        {"name": "Dr. Leena D'souza", "specialty": "General Physician", "address": "Breach Candy Hospital, Breach Candy"},
        {"name": "Dr. Ashok Kumar", "specialty": "General Physician", "address": "Hiranandani Hospital, Powai"},
        {"name": "Dr. Fatima Khan", "specialty": "General Physician", "address": "Global Hospital, Parel"},
        {"name": "Dr. Suresh Menon", "specialty": "General Physician", "address": "Wockhardt Hospital, Mumbai Central"},
        # Neurologists
        {"name": "Dr. Ananya Rao", "specialty": "Neurologist", "address": "22, Kokilaben Hospital, Andheri West"},
        {"name": "Dr. P. N. Renjen", "specialty": "Neurologist", "address": "Indraprastha Apollo Hospitals, Sarita Vihar"},
        {"name": "Dr. Mohit Bhatt", "specialty": "Neurologist", "address": "Jaslok Hospital, Peddar Road"},
        # Orthopedic Surgeons
        {"name": "Dr. Sameer Joshi", "specialty": "Orthopedic Surgeon", "address": "56, Lilavati Hospital, Bandra"},
        {"name": "Dr. Sanjay Agarwala", "specialty": "Orthopedic Surgeon", "address": "P. D. Hinduja Hospital, Mahim"},
        {"name": "Dr. Ram Chaddha", "specialty": "Orthopedic Surgeon", "address": "Nanavati Super Speciality Hospital, Vile Parle"},
        # Cardiologists
        {"name": "Dr. Ashwin Mehta", "specialty": "Cardiologist", "address": "Jaslok Hospital, Peddar Road"},
        {"name": "Dr. Ramakanta Panda", "specialty": "Cardiologist", "address": "Asian Heart Institute, Bandra Kurla Complex"},
        {"name": "Dr. S. K. Sinha", "specialty": "Cardiologist", "address": "Fortis Hospital, Mulund"},
        # Dermatologists
        {"name": "Dr. Madhuri Agarwal", "specialty": "Dermatologist", "address": "Yavana Aesthetics Clinic, Juhu"},
        {"name": "Dr. Jaishree Sharad", "specialty": "Dermatologist", "address": "Skinfiniti Aesthetic Skin & Laser Clinic, Bandra"},
        # Pediatricians
        {"name": "Dr. Mukesh Sanklecha", "specialty": "Pediatrician", "address": "Bombay Hospital, Marine Lines"},
        {"name": "Dr. Fazal Nabi", "specialty": "Pediatrician", "address": "Jaslok Hospital, Peddar Road"},
        # Oncologists
        {"name": "Dr. Suresh Advani", "specialty": "Oncologist", "address": "S. L. Raheja Hospital, Mahim"},
        {"name": "Dr. Boman Dhabhar", "specialty": "Oncologist", "address": "Fortis Hospital, Mulund"},
        # Gynecologists
        {"name": "Dr. Firuza Parikh", "specialty": "Gynecologist", "address": "Jaslok Hospital, Peddar Road"},
        {"name": "Dr. Rishma Pai", "specialty": "Gynecologist", "address": "Lilavati Hospital, Bandra"},
        # Gastroenterologists
        {"name": "Dr. Amit Maydeo", "specialty": "Gastroenterologist", "address": "Global Hospital, Parel"},
        {"name": "Dr. Devendra Desai", "specialty": "Gastroenterologist", "address": "P. D. Hinduja Hospital, Mahim"},
        # Pulmonologists
        {"name": "Dr. Zarir Udwadia", "specialty": "Pulmonologist", "address": "P. D. Hinduja Hospital, Mahim"},
    ],
    "delhi": [
        # General Physicians
        {"name": "Dr. Ishaan Gupta", "specialty": "General Physician", "address": "A-1, Connaught Place"},
        {"name": "Dr. Randeep Guleria", "specialty": "General Physician", "address": "AIIMS, Ansari Nagar"},
        {"name": "Dr. Anupam Sibal", "specialty": "General Physician", "address": "Indraprastha Apollo Hospitals, Sarita Vihar"},
        {"name": "Dr. Sandeep Budhiraja", "specialty": "General Physician", "address": "Max Healthcare, Saket"},
        {"name": "Dr. Vivek Nangia", "specialty": "General Physician", "address": "Fortis Flt. Lt. Rajan Dhall Hospital, Vasant Kunj"},
        # Endocrinologists
        {"name": "Dr. Meera Iyer", "specialty": "Endocrinologist", "address": "B-5, Max Healthcare, Saket"},
        {"name": "Dr. Ambrish Mithal", "specialty": "Endocrinologist", "address": "Max Healthcare, Saket"},
        {"name": "Dr. S.V. Madhu", "specialty": "Endocrinologist", "address": "GTB Hospital, Dilshad Garden"},
        # Oncologists
        {"name": "Dr. Arjun Khanna", "specialty": "Oncologist", "address": "C-9, Fortis Hospital, Vasant Kunj"},
        {"name": "Dr. Harit Chaturvedi", "specialty": "Oncologist", "address": "Max Institute of Cancer Care, Saket"},
        {"name": "Dr. Vinod Raina", "specialty": "Oncologist", "address": "Fortis Memorial Research Institute, Gurgaon"},
        # Cardiologists
        {"name": "Dr. Ashok Seth", "specialty": "Cardiologist", "address": "Fortis Escorts Heart Institute, Okhla"},
        {"name": "Dr. Subhash Chandra", "specialty": "Cardiologist", "address": "BLK Super Speciality Hospital, Pusa Road"},
        {"name": "Dr. Viveka Kumar", "specialty": "Cardiologist", "address": "Max Hospital, Saket"},
        # Neurologists
        {"name": "Dr. Manvir Bhatia", "specialty": "Neurologist", "address": "Neurology and Sleep Centre, Hauz Khas"},
        {"name": "Dr. Sumit Singh", "specialty": "Neurologist", "address": "Artemis Hospital, Gurgaon"},
        # Orthopedic Surgeons
        {"name": "Dr. Ashok Rajgopal", "specialty": "Orthopedic Surgeon", "address": "Medanta - The Medicity, Gurgaon"},
        {"name": "Dr. S.K.S. Marya", "specialty": "Orthopedic Surgeon", "address": "Max Smart Super Speciality Hospital, Saket"},
        # Gynecologists
        {"name": "Dr. Urvashi Prasad Jha", "specialty": "Gynecologist", "address": "Fortis La Femme, Vasant Vihar"},
        {"name": "Dr. Geeta Chadha", "specialty": "Gynecologist", "address": "Indraprastha Apollo Hospitals, Sarita Vihar"},
        # Urologists
        {"name": "Dr. N.P. Gupta", "specialty": "Urologist", "address": "Medanta - The Medicity, Gurgaon"},
        {"name": "Dr. Anant Kumar", "specialty": "Urologist", "address": "Max Hospital, Saket"},
        # Pediatricians
        {"name": "Dr. Krishan Chugh", "specialty": "Pediatrician", "address": "Fortis Memorial Research Institute, Gurgaon"},
        {"name": "Dr. Mamta Jajoo", "specialty": "Pediatrician", "address": "BLK Super Speciality Hospital, Pusa Road"},
        # Dermatologists
        {"name": "Dr. Deepali Bhardwaj", "specialty": "Dermatologist", "address": "The Skin & Hair Clinic, Defence Colony"},
    ],
    "bangalore": [
        # General Physicians
        {"name": "Dr. Kavya Reddy", "specialty": "General Physician", "address": "34, MG Road, Trinity Circle"},
        {"name": "Dr. H.S. Satish", "specialty": "General Physician", "address": "Fortis Hospital, Bannerghatta Road"},
        {"name": "Dr. Sudha Menon", "specialty": "General Physician", "address": "Manipal Hospital, Old Airport Road"},
        {"name": "Dr. Shankar Prasad", "specialty": "General Physician", "address": "Apollo Hospitals, Jayanagar"},
        {"name": "Dr. Murali Mohan", "specialty": "General Physician", "address": "Narayana Health City, Bommasandra"},
        # Pulmonologists
        {"name": "Dr. Nikhil Gowda", "specialty": "Pulmonologist", "address": "77, Manipal Hospital, Old Airport Road"},
        {"name": "Dr. Sandeep H.S", "specialty": "Pulmonologist", "address": "BGS Gleneagles Global Hospitals, Kengeri"},
        {"name": "Dr. Sachin Kumar", "specialty": "Pulmonologist", "address": "Sakra World Hospital, Marathahalli"},
        # Gynecologists
        {"name": "Dr. Sunita Pillai", "specialty": "Gynecologist", "address": "88, Cloudnine Hospital, Jayanagar"},
        {"name": "Dr. Hema Divakar", "specialty": "Gynecologist", "address": "Divakars Speciality Hospital, JP Nagar"},
        {"name": "Dr. Kamini Rao", "specialty": "Gynecologist", "address": "Milann - The Fertility Center, Kumarapark"},
        # Cardiologists
        {"name": "Dr. Devi Shetty", "specialty": "Cardiologist", "address": "Narayana Health City, Bommasandra"},
        {"name": "Dr. C.N. Manjunath", "specialty": "Cardiologist", "address": "Sri Jayadeva Institute of Cardiovascular Sciences"},
        {"name": "Dr. Vivek Jawali", "specialty": "Cardiologist", "address": "Fortis Hospital, Bannerghatta Road"},
        # Oncologists
        {"name": "Dr. Kodaganur S. Gopinath", "specialty": "Oncologist", "address": "Bangalore Institute of Oncology, Kalasipalyam"},
        {"name": "Dr. Sandeep Nayak", "specialty": "Oncologist", "address": "Fortis Hospital, Bannerghatta Road"},
        # Neurologists
        {"name": "Dr. N.K. Venkataramana", "specialty": "Neurologist", "address": "Brains Neuro Spine Centre, Jayanagar"},
        {"name": "Dr. Ravi Gopal Varma", "specialty": "Neurologist", "address": "Aster CMI Hospital, Hebbal"},
        # Orthopedic Surgeons
        {"name": "Dr. Thomas A. Chandy", "specialty": "Orthopedic Surgeon", "address": "HOSMAT Hospital, Magrath Road"},
        {"name": "Dr. B.R.J. Kannan", "specialty": "Orthopedic Surgeon", "address": "Sparsh Hospital, Infantry Road"},
        # Pediatricians
        {"name": "Dr. Karthik Nagesh", "specialty": "Pediatrician", "address": "Manipal Hospital, Old Airport Road"},
        {"name": "Dr. Rajath Athreya", "specialty": "Pediatrician", "address": "Sakra World Hospital, Marathahalli"},
        # Nephrologists
        {"name": "Dr. Sudarshan Ballal", "specialty": "Nephrologist", "address": "Manipal Hospital, Old Airport Road"},
        {"name": "Dr. Sankaran Sundar", "specialty": "Nephrologist", "address": "Columbia Asia Referral Hospital, Yeshwanthpur"},
        # Dermatologists
        {"name": "Dr. B. S. Chandrashekar", "specialty": "Dermatologist", "address": "Cutis Academy of Cutaneous Sciences, Vijayanagar"},
    ]
}

# --- HELPER FUNCTIONS ---
def get_medicine_suggestion(symptoms):
    """Generates medicine suggestions based on symptoms using the Gemini model."""
    if not model:
        return "The AI model is not available. Please check your API key configuration."
    
    prompt = f"""
    You are an expert and helpful AI medical assistant. A user is reporting the following symptoms: "{symptoms}".

    Based on these symptoms, provide the following in a clear, structured format using Markdown:
    1.  **Possible Condition:** Briefly state what the symptoms might indicate in layman's terms.
    2.  **General Advice:** Offer some general wellness advice (e.g., rest, hydration, diet).
    3.  **Over-the-Counter Suggestions:** Suggest ONLY common, safe, over-the-counter medicines that could help alleviate these specific symptoms. For each suggestion, briefly explain what it does.
    4.  **When to See a Doctor:** Provide clear signs or a timeframe for when the user should consult a doctor if symptoms persist or worsen.
    5.  **Crucial Disclaimer:** End with a very clear and prominent disclaimer stating that you are an AI assistant, not a medical professional, and the user MUST consult a real doctor for an accurate diagnosis and treatment plan. Emphasize that this information should not be used for self-diagnosis or as a substitute for professional medical advice.

    Structure your response clearly for easy readability.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while generating the response: {e}"

def find_doctors_in_city(city):
    """Finds doctors in the hardcoded database for a given city."""
    city_lower = city.lower().strip()
    return doctors_db.get(city_lower)

# --- STREAMLIT APP UI (BASIC) ---

st.title("🩺 AI HealthCare Chatbot")
st.markdown("Your friendly AI assistant for preliminary health queries.")

st.warning(
    "**Disclaimer:** This chatbot is an AI assistant and not a substitute for a real doctor. "
    "Please consult with a qualified healthcare professional for any medical concerns or before making any health decisions."
)

tab1, tab2 = st.tabs(["Symptom Checker", "Find a Doctor"])

with tab1:
    st.header("Symptom Checker & AI Suggestion")
    st.markdown("Describe your symptoms below, and the AI will provide some general advice and over-the-counter suggestions.")
    
    symptoms_input = st.text_area(
        "Enter your symptoms here (e.g., 'I have a headache, fever, and a runny nose')", 
        height=150
    )
    
    if st.button("Get AI Suggestion"):
        if symptoms_input and model:
            with st.spinner("Analyzing your symptoms..."):
                suggestion = get_medicine_suggestion(symptoms_input)
                st.markdown("---")
                st.subheader("AI-Powered Suggestion")
                st.markdown(suggestion)
        elif not model:
             st.error("Cannot get suggestion. The AI model is not configured correctly.")
        else:
            st.error("Please enter your symptoms.")

with tab2:
    st.header("Find a Doctor Nearby")
    st.markdown("Select your city to find a list of available doctors.")
    
    # Create a list of cities with a placeholder
    city_list = ["-- Select a City --"] + [city.title() for city in doctors_db.keys()]
    
    city_input = st.selectbox(
        "Select your city",
        options=city_list,
        label_visibility="collapsed"
    )
    
    if st.button("Search for Doctors"):
        if city_input != "-- Select a City --":
            with st.spinner(f"Searching for doctors in {city_input}..."):
                doctors_list = find_doctors_in_city(city_input)
                st.markdown("---")
                st.subheader(f"Doctors in {city_input.title()}")
                if doctors_list:
                    for doctor in doctors_list:
                        st.markdown(f"**Dr. {doctor['name']}**")
                        st.markdown(f"&nbsp;&nbsp;&nbsp;*Specialty:* {doctor['specialty']}")
                        st.markdown(f"&nbsp;&nbsp;&nbsp;*Address:* {doctor['address']}")
                        st.markdown("---")
                else:
                    st.info(f"Sorry, we couldn't find any doctors for '{city_input}'.")
        else:
            st.error("Please select a city to search.")
