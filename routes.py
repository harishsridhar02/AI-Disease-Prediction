

import logging
from flask import render_template, request, jsonify, redirect, url_for, flash, session
from app import app, db
from models import Doctor, Department, Service, Appointment, User
from datetime import datetime
import requests
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Routes for main pages
@app.route('/')
def index():
    # Get departments and services to display on homepage
    departments = Department.query.all()
    services = Service.query.all()
    doctors = Doctor.query.limit(3).all()  # Featured doctors
    
    return render_template('index.html', 
                          departments=departments, 
                          services=services,
                          doctors=doctors)

@app.route('/doctors')
def doctors():
    # Get all doctors
    all_doctors = Doctor.query.all()
    specialties = set([doctor.specialty for doctor in all_doctors])
    
    return render_template('doctors.html', 
                          doctors=all_doctors,
                          specialties=specialties)

@app.route('/appointments')
def appointments():
    # Get all doctors for the appointment form
    all_doctors = Doctor.query.all()
    departments = Department.query.all()
    
    # In a real app, you'd check if user is logged in
    # and show their existing appointments
    
    return render_template('appointments.html',
                          doctors=all_doctors,
                          departments=departments)

@app.route('/book-appointment', methods=['POST'])
def book_appointment():
    if request.method == 'POST':
        try:
            # Get form data
            patient_name = request.form.get('patientName')
            patient_email = request.form.get('patientEmail')
            doctor_id = request.form.get('doctorId')
            appointment_date = request.form.get('appointmentDate')
            appointment_time = request.form.get('appointmentTime')
            reason = request.form.get('reason')
            
            # Log the appointment data for debugging
            logging.debug(f"Appointment Data: {doctor_id}, {appointment_date}, {appointment_time}")
            
            # In a real application, you would:
            # 1. Check if the user exists or create one
            # 2. Validate the appointment time against doctor's availability
            # 3. Create the appointment in the database
            
            # Convert appointment_date string to Date object
            date_obj = datetime.strptime(appointment_date, '%Y-%m-%d').date()
            
            # Convert appointment_time string to Time object
            time_obj = datetime.strptime(appointment_time, '%H:%M').time()
            
            # Just creating a mock success message for now
            flash('Appointment booked successfully! We will contact you for confirmation.', 'success')
            return redirect(url_for('appointments'))
            
        except Exception as e:
            logging.error(f"Error booking appointment: {str(e)}")
            flash(f'Error booking appointment: {str(e)}', 'danger')
            return redirect(url_for('appointments'))

@app.route('/disease-prediction')
def disease_prediction():
    # Check if there's a clear parameter to reset prediction
    if request.args.get('clear'):
        if 'prediction_result' in session:
            session.pop('prediction_result', None)
            flash('Prediction cleared. You can make a new prediction.', 'info')
        return redirect(url_for('disease_prediction'))
        
    return render_template('disease-prediction.html')

@app.route('/predict-disease', methods=['POST'])
def predict_disease():
    if request.method == 'POST':
        try:
            # Get symptoms from form
            symptoms = request.form.getlist('symptoms')
            
            logging.debug(f"Selected symptoms: {symptoms}")
            
            # Mock prediction data instead of calling the external API
            # This simulates the response we would get from the real backend
            mock_diseases = [
                {"disease": "Common Cold", "probability": 0.85},
                {"disease": "Seasonal Allergies", "probability": 0.65},
                {"disease": "Sinusitis", "probability": 0.48}
            ]
            
            # Adjust probabilities based on number of symptoms
            symptom_count = len(symptoms)
            if symptom_count <= 2:
                # With few symptoms, lower the confidence
                for disease in mock_diseases:
                    disease["probability"] = max(0.1, disease["probability"] - 0.3)
            elif symptom_count >= 5:
                # With many symptoms, slightly higher confidence
                for disease in mock_diseases:
                    disease["probability"] = min(0.95, disease["probability"] + 0.1)
            
            # Add descriptions for each disease
            disease_descriptions = {
                "Common Cold": "A viral infectious disease of the upper respiratory tract that primarily affects the nose.",
                "Seasonal Allergies": "An allergic reaction to airborne substances such as pollen that causes inflammation of the nose and respiratory tract.",
                "Sinusitis": "Inflammation of the sinuses, typically caused by an infection or allergies."
            }
            
            prediction_data = {
                "predictions": mock_diseases,
                "symptoms": symptoms,
                "descriptions": disease_descriptions
            }
            
            # Store prediction in session for display
            session['prediction_result'] = prediction_data
            flash('Disease prediction complete!', 'success')
                
            return redirect(url_for('disease_prediction'))
            
        except Exception as e:
            logging.error(f"Error predicting disease: {str(e)}")
            flash(f'Error during prediction: {str(e)}', 'danger')
            return redirect(url_for('disease_prediction'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

# API endpoints for AJAX calls
@app.route('/api/doctors')
def api_doctors():
    doctors = Doctor.query.all()
    result = []
    for doctor in doctors:
        result.append({
            'id': doctor.id,
            'name': doctor.name,
            'specialty': doctor.specialty,
            'bio': doctor.bio
        })
    return jsonify(result)

@app.route('/api/doctor/<int:doctor_id>/availability')
def doctor_availability(doctor_id):
    # This would be implemented to get available time slots for a specific doctor
    # For now, returning mock data
    return jsonify({
        'message': 'This endpoint would return availability for the specified doctor'
    })

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
