Code..

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
