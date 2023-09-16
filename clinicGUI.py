import tkinter as tk
from tkinter import ttk, scrolledtext
from tkcalendar import *
import os
from PIL import Image, ImageTk
from tkinter.messagebox import showinfo,showerror
from datetime import date, datetime, timedelta
from clinicController import clinicController


# Create the clinicController object
clinic = clinicController() 

# Load patient data from the controller
clinic.load_patients_from_file()

# Load doctor data from the controller 
clinic.load_doctors_from_file()


######## Functions #########

# get selected patient id as an int
def get_selected_patient_id():
    selected_patient_index = patient_listbox.curselection()
    if selected_patient_index:
        selected_patient_str = patient_listbox.get(selected_patient_index) # string displayed in the listbox
        selected_patient_id = int(selected_patient_str.split()[0]) # get the id as an int
        return selected_patient_id
    else:
        return None


# get selected doctor id as an int
def get_selected_doc_id():
    selected_doctor_index = doctor_listbox.curselection()
    if selected_doctor_index:
        selected_doctor_str = doctor_listbox.get(selected_doctor_index) # string displayed in the listbox
        selected_doctor_id = int(selected_doctor_str.split()[0]) # get the id as an int
        return selected_doctor_id
    else:
        return None


# get a list of time slots for all the consultation time
def get_all_time_slots():

    time_slots = [] # initialize an empty list

    # Assume clinic starts 8:30am and finishes at 4:30pm   
    clinic_start_datetime = datetime.strptime("8:30", "%I:%M") # converting a string into a datetime object(eg.1900-01-1 08:30:00)
    clinic_finish_datetime = datetime.strptime('16:30', '%H:%M') # converting a string into a datetime object(eg.1900-01-1 08:30:00)


    # Assume each consultation takes 30mins. 
    cons_datetime = clinic_start_datetime # initialize the first consultation datetime(eg:1900-01-01 09:00:00)

    while cons_datetime < clinic_finish_datetime: 
        time_slots.append(cons_datetime.strftime("%I:%M %p"))
        cons_datetime += timedelta(minutes=30)

    return time_slots


# validate time - get formatted_time
def get_valid_time():
    selected_time = time_var.get()

    # check for the default option
    if selected_time == options[0]:
        showerror(
            title='Invalid Option',
            message="Please select a valid time"
        )
        return None

    formatted_time = selected_time
    return formatted_time


# validate date - get fromatted_date
def get_valid_date():

    date_str = date_cal.get_date()
    selected_date = datetime.strptime(date_str,'%m/%d/%y')

#     day = day_var.get()
#     month = month_var.get()
#     year = year_var.get()

#     # validate day, month, year input
#     try:
#         day = int(day)
#         month = int(month)
#         year = int(year)
#     except ValueError:
#         showerror(
#             title="Invalid Date Format",
#             message="Please enter valid numeric values for the day, month, and year."
#         )
#         return False

#     # construct valid seleted date
#     try:
#         selected_date = date(year, month, day)
#     except ValueError:
#         showerror(
#             title='Invalid Date',
#             message="Please enter a valid date."
#         )
        # return False

    # check year - today or later
    current_datetime = datetime.now()
    if selected_date < current_datetime:
        showerror(
            title="Invalid date",
            message="Can't make an appointment in the past. Please select a date on or after today."
        )
    
    # convert the selected date into new zealand format
    formatted_date = selected_date.strftime('%d/%m/%Y') #in NZ date format

    return formatted_date


# get selected_datetime_str - await for furuther validation
def get_selected_datetime_str():
    formatted_date = get_valid_date()
    formatted_time = get_valid_time()
    selected_datetime_str = f"{formatted_date} {formatted_time}"
    return selected_datetime_str


# get c_doctor
def get_valid_doctor():
    selected_doctor_index = doctor_listbox.curselection()
    if not selected_doctor_index:
        showerror(
            title='Selection Required',
            message='Please select both a doctor and a patient'
        )
        return None
    
    selected_doctor_id = get_selected_doc_id()
    c_doctor = clinic.find_doctor_object(selected_doctor_id)
    if c_doctor is None:
        showerror(
        title='Doctor not found',
        message='Doctor not found. Please try again.'
        )
        return None
    
    return c_doctor



# get c_patient
def get_valid_patient():
    selected_patient_index = patient_listbox.curselection()
    if not selected_patient_index:
        showerror(
            title='Selection Required',
            message='Please select both a doctor and a patient'
        )
        return None

    selected_patient_id = get_selected_patient_id()
    c_patient = clinic.find_patient_object(selected_patient_id)
    if c_patient is None:
        showerror(
            title='Patient not found',
            message='Patient not found. Please try again.'
        )
        return None
    
    return c_patient
    


# check double booking
def is_double_booked():
    selected_datetime_str = get_selected_datetime_str()
    c_doctor = get_valid_doctor()
    c_patient = get_valid_patient()

    doctor_double_booked = clinic.is_doctor_double_booked(c_doctor,selected_datetime_str)
    patient_double_booked = clinic.is_patient_double_booked(c_patient,selected_datetime_str)

    return doctor_double_booked, patient_double_booked


# get c_date - as a valid c_date-datetime_str
def get_valid_datetime_str():
    doctor_double_booked, patient_double_booked = is_double_booked()
    if not (doctor_double_booked or patient_double_booked):
        c_date = get_selected_datetime_str()
        return c_date
    else:
        return None


# get_c_reason
def get_valid_reason():
    reason = reason_var.get()
    if not reason:
        showerror(
            title='Reason Required',
            message='Please enter a reason for the consultation.'
        )
        return None
    else:
        c_reason = reason.capitalize()
        return c_reason



# get_c_fee
def get_valid_fee():
    fee = fee_var.get() # this is a string
    if not fee:
        showerror(
            title='Fee Required',
            message='Please enter a fee for the consultation.'
        )
        return None
    else:
        try:
            fee = float(fee)
            # check if the fee has more than two decimal places
            if fee != round(fee,2):
                showerror(
                    title='Invalid Fee',
                    message="Please enter a fee with no more than two decimal places."
                )
                return None
        except ValueError:
            showerror(
                title='Invalid Fee',
                message='Please enter a valid numeric value for the fee.'
            )
            return None
   
    c_fee = round(fee, 2)
    return c_fee



# get consultation info as a dictionary
def get_consultation_info():   
    c_date = get_valid_datetime_str()
    c_patient = get_valid_patient()
    c_doctor = get_valid_doctor()
    c_reason = get_valid_reason()
    c_fee = get_valid_fee()

    cons_info = {
        'c_date': c_date,
        'c_patient': c_patient,
        'c_doctor': c_doctor,
        'c_reason': c_reason,
        'c_fee': c_fee
    }
    
    return cons_info



#### Section One ####
# call controller method to get the patients list in the format of id+name)
def btn_show_all_patients():
    patient_data_list = clinic.display_all_patients_ids_and_names()

    # Clear the previous content in the patient_listbox
    patient_listbox.delete(0, tk.END)
    # populate data into listbox
    for data in patient_data_list:
        patient_listbox.insert(tk.END, data)


# call controller method to get the doctors list in the format of id+name+specialisation
def btn_show_all_doctors():
    doctor_data_list = clinic.display_all_doctors_ids_names_specs()

    # Clear the previous content in the doctor_listbox
    doctor_listbox.delete(0, tk.END)
    # populate the listbox with new data
    for data in doctor_data_list:
        doctor_listbox.insert(tk.END, data)


# Call the controller method to add valid consultation 
def btn_add_a_new_consultation():
    cons_info = get_consultation_info()
    if cons_info is not None:
        doctor_double_booked, patient_double_booked = is_double_booked()

    
        if doctor_double_booked:
            showerror(
                title="Doctor double booked",
                message="Doctor is booked at this time. Please select another time"
            )
        elif patient_double_booked: 
            showerror(
                title="Patient double booked",
                message="Patient is booked at this time. Please select another time"
            )

        else:
            clinic.create_and_add_consultation(
                c_date=cons_info['c_date'],
                c_patient=cons_info['c_patient'],
                c_doctor=cons_info['c_doctor'],
                c_reason=cons_info['c_reason'],
                c_fee=cons_info['c_fee']
                )
            
            showinfo(
                title="New Consultation Added",
                message=(
                    f"New Consultation Added:\n"
                    f"Date:{cons_info['c_date']}\n"
                    f"Patient:{cons_info['c_patient'].first_name} {cons_info['c_patient'].last_name}\n"
                    f"Doctor:{cons_info['c_doctor'].first_name} {cons_info['c_doctor'].last_name}\n"
                    f"Reason:{cons_info['c_reason']}\n"
                    f"Fee:{cons_info['c_fee']}"
                )
            )

            
        
    
#### Section Two ####
# call controller method to get patient info, push it to the widget
def btn_view_patient_info():

    # find the selected patient
    selected_patient_id = get_selected_patient_id()
    if selected_patient_id is None:
        showerror(
            title="Patient not selected",
            message="Please select a patient."
        )
    patient_obj = clinic.get_patient_info_for_report_by_id(selected_patient_id)

    if patient_obj is not None:
        text_widget.delete('1.0', tk.END) # clear existing text in the widget
        text_widget.insert(tk.END, patient_obj) # insert patient info into widget
    else:
        text_widget.delete('1.0', tk.END)
        text_widget.insert(tk.END, "No patient infomation available")


# call controller method to get doctor info, push it to the widget
def btn_view_doctor_info():
    
    # find the selected doctor
    selected_doctor_id = get_selected_doc_id()
    if selected_doctor_id is None:
        showerror(
            title="Doctor not selected",
            message="Please select a doctor."
        )
    doctor_obj = clinic.get_doctor_info_for_report_by_id(selected_doctor_id)

    if doctor_obj is not None:
        text_widget.delete('1.0', tk.END) # clear existing text in the widget
        text_widget.insert(tk.END, doctor_obj) # insert doctor info into widget
    else:
        text_widget.delete('1.0', tk.END)
        text_widget.insert(tk.END, "No doctor infomation available")


# call controller method to assign doctor to a patient
def btn_assign_doctor():
    selected_doc_id = get_selected_doc_id()
    if selected_doc_id is not None:
        doctor = clinic.find_doctor_object(selected_doc_id)
    else:
        showerror(
            title="doctor not found",
            message="Doctor not found. Please try again."
        )
        doctor = None
        return doctor

    selected_pat_id = get_selected_patient_id()
    if selected_pat_id is not None:
        patient = clinic.find_patient_object(selected_pat_id)
    else:
        showerror(
            title="patient not found",
            message="Patient not found. Please try again."
        )
        patient = None
        return patient

    clinic.assign_doctor_to_patient(doctor=doctor,patient=patient)
    showinfo(
        title="Assign Doctor Successful",
        message=f"Doctor {doctor.first_name} {doctor.last_name} has been assigned to Patient {patient.first_name} {patient.last_name}."

    )


# call controller method to show consultation report
def btn_view_consultation_report():
    full_report = clinic.get_clinic_consultation_full_report()

    if full_report is not None:
        text_widget.delete('1.0', tk.END) # clear existing text in the widget
        text_widget.insert(tk.END, full_report) # insert doctor info into widget
    else:
        text_widget.delete('1.0', tk.END)
        text_widget.insert(tk.END, "No report info available")



####### GUI #######

# Create a root
root = tk.Tk() 
root.title("Clinic Management System")
root.geometry("920x800+30+30")
root.config(padx=10, pady=10)


# Create a clinic logo
image_path = os.path.join(os.getcwd(), 'logo.png') ## Specify the full path to the image file
img = Image.open(image_path) ## open the image
new_size = (50,50) # set width and height as a tuple
resized_img = img.resize(new_size) ## resize the image
tk_img = ImageTk.PhotoImage(resized_img) # Converting the Pillow Image object into a PhotoImage object for displaying in tkinter

# Place a heading part: label with the logo and clinic name, place the heading at the top centre of the window
heading_label = ttk.Label(
    root, 
    image=tk_img,
    text="Clinic Management System", 
    font=("Helvetica", 24, "bold"),
    compound='left',
    )
heading_label.grid(row=0,column=1,pady=10)



# Section One: patient list, doctor list, add consultation:

# Patient list:
## Create a title label
patient_lst_title_label = ttk.Label(root,text='Patient List',font=("Helvetica", 16))
patient_lst_title_label.grid(row=1,column=0, sticky='w',pady=5, padx=(30,0))

## Create a listbox for displaying patients
patient_listbox = tk.Listbox(root, width=20,height=15, exportselection=0, selectmode=tk.SINGLE)
patient_listbox.grid(row=2,column=0,padx=(30,0))

## Create a button to show all patients
button = ttk.Button(root,text="Show All Patients",command=btn_show_all_patients)
button.grid(row=3,column=0,sticky='nw',pady=5, padx=(30,0))



# Doctor list:
## Create a title label
doctor_lst_title_label = ttk.Label(root,text='Doctor List',font=("Helvetica", 16))
doctor_lst_title_label.grid(row=1,column=1, sticky='w',pady=5,padx=(50,0))

## Create a listbox for displaying doctors
doctor_listbox = tk.Listbox(root, width=30,height=15,exportselection=0,selectmode=tk.SINGLE)
doctor_listbox.grid(row=2,column=1, sticky='w',padx=(50, 0)) 

## Create a button to read data
button = ttk.Button(root,text="Show All Doctors",command=btn_show_all_doctors)
button.grid(row=3,column=1,sticky='nw',pady=5, padx=(50,0))



# Add Consultation
# Title label for the frame
cons_title = ttk.Label(root, text="Consultation", font=("Helvetica", 16))
cons_title.grid(row=1, column=2, sticky='w')

# Consultation frame
cons = ttk.Frame(root, borderwidth=0.5, relief="groove", padding=5)
cons.grid(row=2, column=2, sticky='w')



# date
###### Use tkcalendar to get date
date_label = ttk.Label(cons, text="Select a Date:")
date_label.grid(row=0,column=0, sticky='w',pady=(5,5))

now = datetime.now()
current_year = now.year # int
current_month = now.month # int
current_day = now.day # int

date_cal =Calendar(cons, selectemode="day", year=current_year, month=current_month, day=current_day)
date_cal.grid(row=1,column=0,columnspan=2, sticky='ew')

date_var = date_cal.get_date()


# time
## prepare for the options
time_slots = get_all_time_slots()
options = ['---  Select a Time  ---'] + time_slots
# print(options)

time_label = ttk.Label(cons, text="Time: ")
time_label.grid(row=2,column=0,sticky='w')

time_var = tk.StringVar()
time_var.set(options[0]) # set the default value

time_drop = ttk.OptionMenu(cons, time_var, *options)
time_drop.grid(row=2, column=1,sticky='w')

# reason
reason_label = ttk.Label(cons, text="Reason: ")
reason_label.grid(row=3,column=0,sticky='w')

reason_var = tk.StringVar()
reason_entry = ttk.Entry(cons, textvariable=reason_var)
reason_entry.grid(row=3,column=1,sticky='ew')

# fee
fee_label = ttk.Label(cons, text="Fee:")
fee_label.grid(row=4,column=0,sticky='w')

fee_var = tk.StringVar()
fee_entry = ttk.Entry(cons, textvariable=fee_var)
fee_entry.grid(row=4,column=1,sticky='ew')

####### Create 3 entries to get year, month, day
# # day
# day_label = ttk.Label(cons, text="Day (1 -31): ")
# day_label.grid(row=1,column=0,sticky='w',pady=(0,0))

# day_var = tk.IntVar()
# day_entry = ttk.Entry(cons, textvariable=day_var)
# day_entry.grid(row=1,column=1,sticky='ew',pady=(0,0))

# # month
# month_label = ttk.Label(cons, text="Month (1-12): ")
# month_label.grid(row=2,column=0,sticky='w')

# month_var = tk.IntVar()
# month_entry = ttk.Entry(cons, textvariable=month_var)
# month_entry.grid(row=2,column=1,sticky='ew')

# # year
# year_label = ttk.Label(cons, text="Year(e.g.,2023): ")
# year_label.grid(row=3,column=0,sticky='w')

# year_var = tk.IntVar()
# year_entry = ttk.Entry(cons, textvariable=year_var)
# year_entry.grid(row=3,column=1,sticky='ew')



# Add Consultation Button
addConsBtn = ttk.Button(root, text="Add a New Consultation", command=btn_add_a_new_consultation)
addConsBtn.grid(row=3, column=2, sticky='wn',pady=(5.0))



# Section Two
# # Create a title label for the frame
# frame_title_label = ttk.Label(root, text="Functions", font=("Helvetica", 16))
# frame_title_label.grid(row=4, column=0, columnspan=2, padx=(25,0), pady=(5, 5),sticky='w')

# Create a Frame
sec_2_frame = ttk.Frame(root, borderwidth=0.5, relief="groove", padding=5)
sec_2_frame.rowconfigure(0,minsize=50)
sec_2_frame.grid(row=5, column=0, columnspan=3, sticky='news',padx=(25,0))

# Configure the columns to have equal weight
sec_2_frame.columnconfigure(0, weight=1)
sec_2_frame.columnconfigure(1, weight=1)
sec_2_frame.columnconfigure(2, weight=1)
sec_2_frame.columnconfigure(3, weight=1)


# Place Patient Information button
btnPatInfo = ttk.Button(sec_2_frame, text="View Patient Info", command=btn_view_patient_info)
btnPatInfo.grid(row=0,column=0,sticky='ew',padx=(15,15))

# Place Doctor Information button
btnDocInfo = ttk.Button(sec_2_frame, text="View Doctor Info", command=btn_view_doctor_info)
btnDocInfo.grid(row=0,column=1,sticky='ew',padx=(15,15))


# Place Assign Doctor button
btnAssignDoctor = ttk.Button(sec_2_frame, text="Assign Doctor", command=btn_assign_doctor)
btnAssignDoctor.grid(row=0,column=2,sticky='ew',padx=(15,15))


# Place Consultation Report button
btnConReport = ttk.Button(sec_2_frame, text="View Consultation Report", command=btn_view_consultation_report)
btnConReport.grid(row=0,column=3,sticky='ew',padx=(15,15))


# Section Three

# Create a scrolledtext widget
## title label
text_widget_label = ttk.Label(root, text="Display Report", font=("Helvetica", 16))
text_widget_label.grid(row=8, column=0, padx=(25,0), pady=(10, 5),sticky='w')

## widget
text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD,width=40, height=15)
text_widget.grid(row=9, column=0, columnspan=2,padx=(25,0),sticky='ew')



#exit button
exit_button = ttk.Button(
    root,
    text='Exit',
    command=lambda: root.quit()
)
exit_button.grid(row=9,column=2,sticky='es',pady=(30,0))

root.mainloop()