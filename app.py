import os
import pandas as pd

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# Let's get the api key from the environment variable
gemini_api_key = os.getenv('my-first-key')

# Let's configure the model
model = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash-lite',
    google_api_key=gemini_api_key)

# Design the UI of application

st.title(":orange[Healthify Me : ] :blue[ Your Personal Health Assistant]")
st.markdown('''
            This application will assist you to get better and customized Health advice.
            You can ask your health related issues and get personalized guidance.
            ''')
st.write( '''
Follow these steps:
* Enter you details in the sidebar.
* Rate your activity anf fitness on the scale of 0-5.
* Submit your details.
* Ask your health related question in the input box.
* Click on Generate Report to get your personalized health report.''')


# Design the sidebar for all the user parameters
st.sidebar.header(':red[Enter Your Details]')
name = st.sidebar.text_input('Enter Your Name')
gender = st.sidebar.selectbox('Select Your Gender', ['Male', 'Female', 'Other'])
age = st.sidebar.text_input('Enter Your Age')
weight = st.sidebar.text_input('Enter Your Weight (in kgs)')
height = st.sidebar.text_input('Enter Your Height (in cms)')
bmi = pd.to_numeric(weight) / ((pd.to_numeric(height)/100) ** 2)
active = st.sidebar.slider('Rate your Activity (0-5)',0,5,step = 1)
Fitness = st.sidebar.slider('Rate your Fitness (0-5)',0,5,step = 1)
if st.sidebar.button('Submit'):
    st.sidebar.write(f"{name}, your BMI is : {bmi:.2f}kg/m^2")

# Let's use the gemini model to generate the report
user_input = st.text_input('Ask me your question')
prompt = f'''
<Role> You are a health expert and wellness and has 10+ experience for guiding people.
<Goal> Generate the customized report addressing the problem the user has asked. Here is the question that 
user has asked : {user_input}.
<context> Here are the details that the user has provided.
name = {name}
age = {age}
gender = {gender}
weight = {weight}
height = {height}
bmi = {bmi:.2f}kg/m^2
activity level(0-5) = {active}
fitness level(0-5) = {Fitness}
<format> Following should be the outline of the report in the sequence provided below:
* Start with the 2-3 lines of comment on the details that user has provided.
* Explain what the real problem could be on the basis of input provided by user.
* Suggest the possible reasons for the problem.
* What are the possible solutions to the problem.
* Mention the doctor from which specialization can be visited if required.
* Mention any change in the diest plan which is required .
* In the last create a summary of all the things that has been discussed in the report.
<Instructions> * Use bullet points wherever possible.
* Create tables to represent any data where ever possible.
* Strictly do not advice any medicine.
'''
if st.button('Generate Report'):
    response = model.invoke(prompt)
    st.write(response.content)

   