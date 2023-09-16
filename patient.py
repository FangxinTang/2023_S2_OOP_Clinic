
class Patient:

    next_id = 100 

    def __init__(self, first_name, last_name):

        self.__id = Patient.next_id
        Patient.next_id += 1

        self.__first_name = first_name   
        self.__last_name = last_name

        self.__assigned_doctor = None  # Initialize with no assigned doctor object
        self.__consultations = []

    
    # Set getters
    @property
    def id(self):
        return self.__id
    
    @property
    def first_name(self):
        return self.__first_name

    @property
    def last_name(self):
        return self.__last_name
    
    @property
    def assigned_doctor(self):
        return self.__assigned_doctor
    
    @property
    def consultations(self):
        return self.__consultations
    
    # Set setters
    @id.setter
    def id(self, new_id):
        raise AttributeError(f"id cannot be manually set{new_id}. It is auto-incremented.")
    
    @first_name.setter
    def first_name(self, new_first_name):
        self.__first_name = new_first_name
    
    @last_name.setter
    def last_name(self, new_last_name):
        self.__last_name = new_last_name
    
    @assigned_doctor.setter
    def assigned_doctor(self, doctor_obj):
        self.__assigned_doctor = doctor_obj


    # Methods

    def add_consultation(self, consultation):
        self.__consultations.append(consultation)


    def get_str_patient_id_name(self):
        return f"{self.__id} {self.__first_name} {self.__last_name}\n"
    
    def get_str_assigned_doctor_details(self):
        if self.__assigned_doctor is not None:
            return f"{self.__assigned_doctor.id} {self.__assigned_doctor.first_name} {self.__assigned_doctor.last_name}"

    def get_str_consultation_details(self):
        str_consultation_details_list= []
        for consultation in self.__consultations:
            details = f"{consultation.c_date} {consultation.c_doctor.first_name} {consultation.c_doctor.last_name} ${consultation.c_fee}\n"
            str_consultation_details_list.append(details)
        return str_consultation_details_list
    
    def get_total_fee(self):
        total_fee = 0.0
        for consultation in self.__consultations:
            total_fee += consultation.c_fee
        return round(total_fee,2)


    def __str__(self):
        #display patien id+name
        patient_info = self.get_str_patient_id_name()

        #display assigned doctor id+name
        assigned_doctor_details = self.get_str_assigned_doctor_details()
        if assigned_doctor_details:
            patient_info += f"  - Assigned Doctor: {assigned_doctor_details}\n\n"
        else:
            patient_info += "  - Assigned Doctor: (Not Assigned)\n\n"

        #display consultations
        str_consultation_details_list = self.get_str_consultation_details()
        patient_info += 'Consultations:\n'
        if str_consultation_details_list:
            for con_details in str_consultation_details_list:
                patient_info += f"  - {con_details}"
        else:
            patient_info += '  - (No consultation history)\n'
        
        #display total fee
        patient_info += f"\nTotal Fee Due: ${self.get_total_fee()}\n"
        return patient_info

