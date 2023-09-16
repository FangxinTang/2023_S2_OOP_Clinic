
class Doctor:

    next_id = 1000 # Class-level variable to keep track of the next ID

    def __init__(self, first_name, last_name, specialisation):

        self.__id = Doctor.next_id # Using the mangled name for the class variable
        Doctor.next_id += 1

        self.__first_name = first_name   
        self.__last_name = last_name
        self.__specialisation = specialisation

        self.__patients = [] # This is a list of patient objects
        self.__consultations = [] # This is a list of consultation objects

    
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
    def specialisation(self):
        return self.__specialisation
    
    @property
    def patients(self):
        return self.__patients
    
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
    
    @specialisation.setter
    def specialisation(self, new_specialisation):
        self.__specialisation = new_specialisation
    
        
    # Methods
    def add_patient(self, patient):
        self.__patients.append(patient)

    def remove_patient(self, patient):
        self.__patients.remove(patient)
    
    def add_consultation(self, consultation):
        self.__consultations.append(consultation)
        

    def get_str_doctor_id_name_spec(self):
        return f"{self.__id} {self.__first_name} {self.__last_name} {self.__specialisation}\n"
    
    def get_str_doctors_patients_list(self):
        str_doctors_patients_list = []
        for patient in self.__patients:
            str_doctors_patients_list.append(patient.get_str_patient_id_name())
        return str_doctors_patients_list
    
    def get_str_doctors_consultations_list(self):
        str_doctors_consultations_list = []
        for con in self.__consultations:
             str_doctors_consultations_list.append(con)
        return str_doctors_consultations_list

    def __str__(self):
        #display doctor id+name+specialisation
        doctor_info = self.get_str_doctor_id_name_spec()

        #display patients list - id+name
        str_doctors_patients_list = self.get_str_doctors_patients_list()
        doctor_info += f'\nPatient List\n'

        if str_doctors_patients_list:
            for patient_id_name in str_doctors_patients_list:
                doctor_info += f"  - {patient_id_name}"
        else:
            doctor_info += "  - No patients have been assigned to this doctor.\n"
        
        #display doctor's consultation list
        str_doctors_consultations_list = self.get_str_doctors_consultations_list()
        doctor_info += f'\nConsultations\n'

        if str_doctors_consultations_list:
            for con in str_doctors_consultations_list:
                doctor_info += f"  - {con}"
        else:
            doctor_info += "  - No consultation history.\n"

        return doctor_info