
# Hospital Management System Frontend
A professional hospital management system frontend that integrates with an existing Multi-Disease Prediction System backend.
## Features
- *Professional and Responsive User Interface*: Built with Bootstrap 5, featuring a clean, medical-focused design
- *Interactive Doctor Directory*: Search and filter doctors by specialty
- *Appointment Booking System*: Schedule appointments with doctors based on their availability
- *Disease Prediction Interface*: Submit symptoms and receive potential diagnoses
- *Detailed Hospital Services Information*: Department and service listings
- *Mobile-Friendly Design*: Optimized for all screen sizes
## Technologies Used
- *Flask*: Python web framework for backend
- *Bootstrap 5*: Frontend CSS framework
- *JavaScript*: For interactive elements
- *PostgreSQL*: Database management system
- *SQLAlchemy*: ORM for database interaction
- *FontAwesome*: Icon library
## Project Structure
![WhatsApp Image 2025-03-23 at 11 15 12_8b9269da](https://github.com/user-attachments/assets/68c59669-65e0-42f1-bdfb-07f9b96cadfe)
## Screenshots
<img width="1440" alt="Screenshot_2025-03-23_at_10 52 29 1" src="https://github.com/user-attachments/assets/d1cb1b43-73b9-4003-a2b0-0ee5f649db4f" />
![Doctors Avail](https://github.com/user-attachments/assets/d5203f04-7db5-4a45-b220-059f62713157)
![Book APpointment(Blank)](https://github.com/user-attachments/assets/386557ad-5f09-46ce-a3fd-00f392bd9adb)
![Book Appointement (Example)](https://github.com/user-attachments/assets/58287350-7277-44f7-b398-9eace9c936a7)
![Mutli Disease Prediction (Tab)](https://github.com/user-attachments/assets/54bca8ed-8e8c-4214-b29e-4c6146f03c14)
![Contact Us (Front End)](https://github.com/user-attachments/assets/7c2623cf-7712-47e1-afbb-98195db93c6e)





## Installation
1. Clone the repository:
git clone https://github.com/yourusername/hospital-management-frontend.git
cd hospital-management-frontend

2. Install dependencies:
pip install flask flask-sqlalchemy flask-login gunicorn psycopg2-binary email-validator requests

3. Set up environment variables:
export FLASK_APP=main.py
export DATABASE_URL=postgresql://username:password@localhost/hospital_db
export SESSION_SECRET=your-secret-key

4. Initialize the database and seed with sample data:
python seed_db.py

5. Run the application:
python main.py

## Integration with Disease Prediction Backend
To integrate with a Multi-Disease Prediction System backend:
1. Replace the mock prediction logic in routes.py with actual API calls to your backend
2. Update the symptoms list in disease-prediction.js to match your backend's available symptoms
3. Modify the prediction result display in disease-prediction.html as needed for your specific data format
## Contributing
1. Fork the repository
2. Create your feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add some amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request
## License
This project is licensed under the MIT License - see the LICENSE file for details.
## Acknowledgments
- Disease prediction backend: [Multi-Disease Prediction System](https://github.com/vamshi060605/Multi-Disease-Prediction-System-using-Machine-Learning)
- UI design inspired by professional medical websites like Mayo Clinic and Cleveland Clinic
- Sample doctor images from [RandomUser API](https://randomuser.me/)
2. requirements.txt
flask==2.2.3
flask-login==0.6.2
flask-sqlalchemy==3.0.3
gunicorn==20.1.0
psycopg2-binary==2.9.5
email-validator==2.0.0
requests==2.28.2
SQLAlchemy==2.0.4
3. app.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(_name_)
app.secret_key = os.environ.get("SESSION_SECRET")
# configure the database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
# initialize the app with the extension, flask-sqlalchemy >= 3.0.x
db.init_app(app)
with app.app_context():
    # Make sure to import the models here or their tables won't be created
    import models  # noqa: F401
    db.create_all()
4. main.py
from app import app
if _name_ == "_main_":
    app.run(host="0.0.0.0", port=5000, debug=True)
5. models.py
from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
# Association table for many-to-many relationship between doctors and departments
doctor_department = db.Table('doctor_department',
    db.Column('doctor_id', db.Integer, db.ForeignKey('doctor.id'), primary_key=True),
    db.Column('department_id', db.Integer, db.ForeignKey('department.id'), primary_key=True)
)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def _repr_(self):
        return f'<User {self.username}>'
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    availability = db.relationship('DoctorAvailability', backref='doctor', lazy=True)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    
    def _repr_(self):
        return f'<Doctor {self.name}>'
class DoctorAvailability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    
    def _repr_(self):
        return f'<Availability for Doctor {self.doctor_id} on day {self.day_of_week}>'
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, canceled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def _repr_(self):
        return f'<Appointment {self.id} with Doctor {self.doctor_id}>'
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    doctors = db.relationship('Doctor', secondary='doctor_department', backref='departments')
    
    def _repr_(self):
        return f'<Department {self.name}>'
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    department = db.relationship('Department', backref='services')
    
    def _repr_(self):
        return f'<Service {self.name}>'
6. routes.py
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
