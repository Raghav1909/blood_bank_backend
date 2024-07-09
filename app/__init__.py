# Create database folder if it doesn't exist
import os
if not os.path.exists('db'):
    os.makedirs('db')


# Create database tables
from . import models
from .database import engine
models.Base.metadata.create_all(bind=engine)


# Initialize Blood Components Table
from .database import get_db

def initialize_blood_components():
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    blood_components = ['Plasma', 'Platelets', 'RBC']
    expiry_in_days = [365, 5, 42]

    for db in get_db():
        if db.query(models.BloodComponent).count() > 0:
            return

    new_blood_components = []

    for blood_group in blood_groups:
        for i, blood_component in enumerate(blood_components):
            new_blood_component = models.BloodComponent(blood_group=blood_group, component_name=blood_component, expiry_in_days=expiry_in_days[i])
            new_blood_components.append(new_blood_component)

    for db in get_db():
        db.bulk_save_objects(new_blood_components)
        db.commit()


initialize_blood_components()