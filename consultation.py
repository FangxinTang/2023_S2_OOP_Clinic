from datetime import datetime

class Consultation:

    def __init__(self, c_date, c_doctor, c_patient, c_reason, c_fee):

        self.__c_date = c_date # string ()
        self.__c_doctor = c_doctor # doctor object
        self.__c_patient = c_patient # patient object
        self.__c_reason = c_reason
        self.__c_fee = c_fee
    

    # Set getters
    @property
    def c_date(self):
        return self.__c_date
    
    @property
    def c_doctor(self):
        return self.__c_doctor
    
    @property
    def c_patient(self):
        return self.__c_patient
    
    @property
    def c_reason(self):
        return self.__c_reason
    
    @property
    def c_fee(self):
        return self.__c_fee
    

    # Set setters
    @c_date.setter
    def c_date(self, new_c_date):
        self.__c_date = new_c_date

    @c_doctor.setter
    def c_doctor(self, new_c_doctor):
        self.__c_doctor = new_c_doctor
    
    @c_patient.setter
    def c_patient(self, new_c_patient):
        self.__c_patient = new_c_patient
    
    @c_reason.setter
    def c_reason(self, new_c_reason):
        self.__c_reason = new_c_reason

    @c_fee.setter
    def c_fee(self, new_c_fee):
        self.__c_fee = new_c_fee

    

    # Methods
    def __str__(self):
        return f"{self.__c_date} {self.__c_reason} {self.__c_patient.first_name} {self.__c_patient.last_name}  ${self.__c_fee}\n"