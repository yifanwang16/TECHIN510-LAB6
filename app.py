import os
import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

prompt_template = """
You are an expert fitness coach. 
Please generate a personalized {workout_days} day workout plan, with each workout lasting {workout_minutes} minutes, based on the following user information:

Gender: {gender}
Age: {age}
Weight: {weight} kg
Height: {height} cm
Fitness Experience: {fitness_experience} years 
Current Fitness Level: {fitness_level}
Injuries or Limitations: {limitations}
Preferred Workout Types: {preferred_workouts}
Goals: {goals}
Available Equipment: {equipment}

Please provide a structured workout plan with the following sections:
1. Warm-up exercises
2. Main exercises (including sets, reps, and rest times)
3. Cool-down exercises
4. Safety precautions and modifications based on the user's injuries or limitations
"""

def generate_workout_plan(prompt):
    response = model.generate_content(prompt)
    return response.text

st.title("💪 AI Fitness Coach Pro")

# User input fields
gender = st.selectbox('Gender', ['Male', 'Female', 'Other'])
age = st.number_input('Age', min_value=18, max_value=100)
weight = st.number_input('Weight (in kg)', min_value=40.0, max_value=200.0)
height = st.number_input('Height (in cm)', min_value=100, max_value=250)
fitness_experience = st.number_input('Fitness Experience (in years)', min_value=0, max_value=100)
fitness_level = st.selectbox('Current Fitness Level', ['Beginner', 'Intermediate', 'Advanced'])
limitations = st.text_input('Injuries or Limitations (if any)')
preferred_workouts = st.text_input('Preferred Workout Types (e.g., strength training, cardio, yoga)')
goals = st.text_input('Your Fitness Goals')
workout_days = st.number_input('How many workout days per week?', min_value=1, max_value=7)
workout_minutes = st.number_input('How many minutes per workout?', min_value=10, max_value=180)

# Multi-select field for equipment
equipment_options = [
    'Dumbbells', 'Barbell', 'Kettlebell', 'Resistance Bands',
    'Yoga Mat', 'Stability Ball', 'Foam Roller', 'Jump Rope',
    'Medicine Ball', 'Pull-Up Bar', 'Dip Station', 'Bench',
    'Squat Rack', 'Treadmill', 'Stationary Bike', 'Rowing Machine',
    'Elliptical Machine', 'Stair Climber', 'Battle Ropes', 'Plyo Box'
]
selected_equipment = st.multiselect('Select Available Equipment (leave blank if no equipment)', equipment_options)

if st.button('Generate Workout Plan'):
    prompt = prompt_template.format(
        gender=gender,
        age=age,
        weight=weight,
        height=height,
        fitness_experience=fitness_experience,
        fitness_level=fitness_level,
        limitations=limitations,
        preferred_workouts=preferred_workouts,
        goals=goals,
        workout_days=workout_days,
        workout_minutes=workout_minutes,
        equipment=', '.join(selected_equipment) if selected_equipment else 'No equipment'
    )

    with st.spinner('Generating your personalized workout plan...'):
        workout_plan = generate_workout_plan(prompt)
    
    st.success('Done!')
    st.write('Your personalized workout plan:')
    st.write(workout_plan)