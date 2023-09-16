from consultation import Consultation
from doctor import Doctor
from patient import Patient

class clinicController:

    def __init__(self):
        # Keep track of doctors, patients and consultations
        self.__all_doctors = []
        self.__all_patients = []
        self.__all_consultations = []



    # Set getters
    @property
    def all_doctors(self):
        return self.__all_doctors
    
    @property
    def all_patients(self):
        return self.__all_patients
    
    @property
    def all_consultations(self):
        return self.__all_consultations
    


    # Methods

    def add_doctor(self, doctor):
        self.__all_doctors.append(doctor)

    def remove_doctor(self, doctor):
        self.__all_doctors.remove(doctor)


    def add_patient(self, patient):
        self.__all_patients.append(patient)

    def remove_patient(self, patient):
        self.__all_patients.remove(patient)


    def add_consultation(self, consultation):
        self.__all_consultations.append(consultation)

    def remove_consultation(self, consultation):
        self.__all_consultations.remove(consultation)
    


    # Create doctors
    def create_doctor(self, first_name, last_name, specialisation):
        # Create a new doctor object
        doctor = Doctor(first_name, last_name, specialisation)
        # Add this doctor object to the list of all_doctors
        self.add_doctor(doctor)


    # Load doctors from Doctor.txt to create doctor objects
    def load_doctors_from_file(self):
        try:
            with open('Doctor.txt', mode='r') as file:
                # Create a list of doctor names
                doctor_info = [line.strip() for line in file]

                for doc in doctor_info:
                    # Split the name into first name, last name and specialisation
                    first_name, last_name, spec = doc.split(',')
                    # Create a new doctor object
                    self.create_doctor(first_name, last_name, spec)
        except FileNotFoundError:
            print("Doctor File not found")

    
    # Create patients
    def create_patient(self, first_name, last_name):
        # Create a new patient object
        patient = Patient(first_name, last_name)
        # Add this patient object to the list of all_patients
        self.add_patient(patient)
    

    # Load patients from Patient.txt to create patient objects
    def load_patients_from_file(self):
        try:
            with open('Patient.txt', mode='r') as file:
                # Create a list of patient names list
                patient_names = [line.strip() for line in file]

                for name in patient_names:
                    # Split the name into first name and last name
                    first_name, last_name = name.split(',')
                    # Create a new patient object
                    self.create_patient(first_name, last_name)
        except FileNotFoundError:
            print('Patient File not found')


    # Display all patients for show all patients function 
    def display_all_patients_ids_and_names(self):
        patient_data_list=[] # initialize patient data list as a list of string
        for patient in self.__all_patients:

            id = patient.id
            full_name = f"{patient.first_name} {patient.last_name}"
            
            patient_data = f"{id}  {full_name}"

            patient_data_list.append(patient_data)
        return patient_data_list


    # Display all doctors for show all doctors function 
    def display_all_doctors_ids_names_specs(self):
        doctor_data_list=[]# initialize doctor data list as a list of string
        for doctor in self.__all_doctors:

            id = doctor.id
            full_name = f"{doctor.first_name} {doctor.last_name}"
            specialisation = doctor.specialisation
            
            doctor_data = f"{id}  {full_name}  {specialisation}"

            doctor_data_list.append(doctor_data)
        return doctor_data_list


    # Assign doctor to a patient
    def assign_doctor_to_patient(self, doctor, patient):
        if doctor is None or patient is None:
            return None
        else:
            # check if the patient is already assigned to another doctor:
            if patient.assigned_doctor is not None:
                patient.assigned_doctor.remove_patient(patient)

            # Assign the patient to the doctor
            patient.assigned_doctor = doctor
            # Add the patient to the doctor's list of patients
            doctor.patients.append(patient)
    

    # Check if a new consultation is double booked
    def is_doctor_double_booked(self, doctor, selected_datetime_str):
        for con in doctor.consultations:
            if con.c_date == selected_datetime_str:
                return True # double booking found at this time
        return False

    def is_patient_double_booked(self, patient, selected_datetime_str):
        for con in patient.consultations:
            if con.c_date == selected_datetime_str:
                return True
        else:
            return False




    # Add a consultation
    def create_and_add_consultation(self, c_date, c_doctor, c_patient, c_reason, c_fee):

        # Create a new consultation object with associated doctor obj and patient obj
        consultation = Consultation(c_date, c_doctor, c_patient, c_reason, c_fee)

        # Add the consultation to the clinic's list of consultations
        self.__all_consultations.append(consultation)

        # Add the consultation to the patient's list of consultations
        c_patient.add_consultation(consultation)

        # Add the consultation to the doctor's list of consultations
        c_doctor.add_consultation(consultation)


    # Search for a doctor object by id
    def find_doctor_object(self, selected_doctor_id):
        for doctor in self.__all_doctors:
            if doctor.id == selected_doctor_id:
                return doctor
        return None


    # Search for a patient object by id
    def find_patient_object(self, selected_patient_id):
        for patient in self.__all_patients:
            if patient.id == selected_patient_id:
                return patient
        return None


    # view patient info
    def get_patient_info_for_report_by_id(self, selected_patient_id):
        # find the patient object by id
        patient_obj = self.find_patient_object(selected_patient_id)
        return patient_obj

    # view doctor info
    def get_doctor_info_for_report_by_id(self, selected_doctor_id):
        # find the doctor object by id
        doctor_obj = self.find_doctor_object(selected_doctor_id)
        return doctor_obj


    # view consultation report
    def get_clinic_consultation_report_title(self):
        return "Consultation Report for XYZ Clinic"
    
    def get_clinic_consultation_report_total_fee(self):
        total_fee = 0.0
        for con in self.all_consultations:
            total_fee += con.c_fee
        return round(total_fee,2)
    
    def get_clinic_consultation_report_details(self):
        details = []
        for con in self.all_consultations:
            details.append(f'{con}')
        return details
    
    def get_clinic_consultation_full_report(self):
        report = f"{self.get_clinic_consultation_report_title()}\n\n"

        details = self.get_clinic_consultation_report_details()
        report += "Consultations:\n"
        if details:
            for d in details:
                report += f"{d}"
        else:
            report += "No consultation history\n"
        
        total_fee = self.get_clinic_consultation_report_total_fee()
        report += f"\nTotal Fee: ${total_fee}\n"
        
        return report





