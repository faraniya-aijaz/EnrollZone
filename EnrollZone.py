import re
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from datetime import datetime, date

# ================ GLOBAL VARIABLES ================
current_student = None
root = None
profile_pic_label = None
courses_tree = None
schedule_tree = None
enrollment_tree = None

# Entry widgets for login
username_entry = None
password_entry = None

# Entry widgets for registration
first_name_entry = None
last_name_entry = None
email_entry = None
phone_entry = None
reg_username_entry = None
reg_password_entry = None
major_entry = None
year_var = None

# ================ DATA FILES ================
STUDENTS_FILE = "students.txt"
COURSES_FILE = "courses.txt"
ENROLLMENTS_FILE = "enrollments.txt"
SCHEDULE_FILE = "schedule.txt"

# ================ COLOR THEMES FOR EACH MAJOR ================
# Each major has its own color theme for consistent visual identity
COLOR_THEMES = {
    "Computer Science": {
        "primary": "#1E3A8A",  # Dark blue
        "secondary": "#DBEAFE",  # Light blue
        "accent": "#3B82F6",  # Medium blue
        "text": "#1E3A8A",  # Dark blue
        "button": "#3B82F6",  # Medium blue
        "button_text": "white"
    },
    "Software Engineering": {
        "primary": "#065F46",  # Dark green
        "secondary": "#D1FAE5",  # Light green
        "accent": "#10B981",  # Medium green
        "text": "#065F46",  # Dark green
        "button": "#10B981",  # Medium green
        "button_text": "white"
    },
    "Data Science": {
        "primary": "#7E22CE",  # Dark purple
        "secondary": "#F3E8FF",  # Light purple
        "accent": "#A855F7",  # Medium purple
        "text": "#7E22CE",  # Dark purple
        "button": "#A855F7",  # Medium purple
        "button_text": "white"
    },
    "default": {
        "primary": "#1F2937",  # Dark gray
        "secondary": "#F3F4F6",  # Light gray
        "accent": "#6B7280",  # Medium gray
        "text": "#1F2937",  # Dark gray
        "button": "#6B7280",  # Medium gray
        "button_text": "white"
    }
}

# ================ DATA INITIALIZATION FUNCTIONS ================
def init_data_files():
    """Create data files if they don't exist with sample data"""
    # Create students file if it doesn't exist
    if not os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, 'w') as f:
            f.write("# username|password|first_name|last_name|email|phone|major|year|profile_pic\n")
    
    # Create courses file with sample courses for each major
    if not os.path.exists(COURSES_FILE):
        with open(COURSES_FILE, 'w') as f:
            f.write("# course_id|course_name|major|credits|instructor|schedule|capacity|enrolled|prerequisites|description\n")
            
            # Computer Science courses
            f.write("CS101|Introduction to Programming|Computer Science|3|Ms.Hafiza Anisa|Mon Wed 10:00-11:30|30|0||Introduction to programming concepts using Python\n")
            f.write("CS201|Data Structures|Computer Science|4|Dr. bilal|Tue Thu 13:00-14:30|25|0|CS101|Implementation and analysis of data structures\n")
            f.write("CS301|Algorithms|Computer Science|4|Dr. Aijaz|Mon Wed 14:00-15:30|25|0|CS101|Design and analysis of algorithms\n")
            f.write("CS401|Database Systems|Computer Science|3|Ms. Sumbul|Tue Thu 10:00-11:30|30|0|CS301|Database design and implementation\n")
            
            # Software Engineering courses
            f.write("SE101|Programming Fundamentals|Software Engineering|3|Ms. Tehreem Qamar|Mon Wed 9:00-10:30|30|0||Introduction to software development lifecycle\n")
            f.write("SE201|Object-Oriented Programming|Software Engineering|4|Ms. Tehreem Qamar|Tue Thu 14:00-15:30|25|0|SE101|OOP concepts and design patterns\n")
            f.write("SE301|Software Design|Software Engineering|4|ms. Farah|Mon Wed 13:00-14:30|25|0|SE201|Software architecture and design principles\n")
            f.write("SE401|Software Testing|Software Engineering|3|Dr. Qamar|Tue Thu 9:00-10:30|30|0|SE201|Testing methodologies and quality assurance\n")
            
            # Data Science courses
            f.write("DS101|Introduction to Data Science|Data Science|3|Ms. Haniya|Mon Wed 11:00-12:30|30|0||Fundamentals of data science\n")
            f.write("DS201|Statistical Methods|Data Science|4|Prof. Amir|Tue Thu 15:00-16:30|25|0|DS101|Statistical analysis for data science\n")
            f.write("DS301|Machine Learning|Data Science|4|Dr. Saniya|Mon Wed 15:00-16:30|25|0|DS201|Machine learning algorithms and applications\n")
            f.write("DS401|Big Data Analytics|Data Science|3|Dr. Bilal Ahmed|Tue Thu 11:00-12:30|30|0|DS301|Processing and analyzing large datasets\n")
            
            # General Education courses (available to all majors)
            f.write("GE101|Calculus I|General|3|Ms. Namal|Mon Wed Fri 8:00-9:00|40|0||Limits, derivatives, and integrals\n")
            f.write("GE102|Calculus II|General|3|Ms. Anum Zameer|Tue Thu Fri 8:00-9:00|40|0|GE101|Advanced integration techniques and series\n")
            f.write("GE201|Ideology of Pakistan|General|4|Ms. Shagufta|Mon Wed 13:00-14:30|35|0||Principles of ideology of Pakistan\n")
            f.write("GE301|Technical Writing|General|3|Dr. Saba Mazhar|Tue Thu 10:00-11:30|40|0||Professional communication for technical fields\n")
            f.write("GE301|Islamic Studies|General|3|Ms. Saima Bano|Tue Thu 10:00-11:30|40|0||Principles of Islam\n")

    
    # Create enrollments file if it doesn't exist - 
    if not os.path.exists(ENROLLMENTS_FILE):
        with open(ENROLLMENTS_FILE, 'w') as f:
            f.write("# username|course_id|enrollment_date|status\n")
    
    # Create schedule file with detailed class schedules
    if not os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, 'w') as f:
            f.write("# course_id|day|start_time|end_time|room\n")
            # CS101 schedule
            f.write("CS101|Monday|10:00|11:30|Room 101\n")
            f.write("CS101|Wednesday|10:00|11:30|Room 101\n")
            # CS201 schedule
            f.write("CS201|Tuesday|13:00|14:30|Room 102\n")
            f.write("CS201|Thursday|13:00|14:30|Room 102\n")
            # CS301 schedule
            f.write("CS301|Monday|14:00|15:30|Room 103\n")
            f.write("CS301|Wednesday|14:00|15:30|Room 103\n")
            # CS401 schedule
            f.write("CS401|Tuesday|10:00|11:30|Room 104\n")
            f.write("CS401|Thursday|10:00|11:30|Room 104\n")
            
            # SE101 schedule
            f.write("SE101|Monday|09:00|10:30|Room 201\n")
            f.write("SE101|Wednesday|09:00|10:30|Room 201\n")
            # SE201 schedule
            f.write("SE201|Tuesday|14:00|15:30|Room 202\n")
            f.write("SE201|Thursday|14:00|15:30|Room 202\n")
            # SE301 schedule
            f.write("SE301|Monday|13:00|14:30|Room 203\n")
            f.write("SE301|Wednesday|13:00|14:30|Room 203\n")
            # SE401 schedule
            f.write("SE401|Tuesday|09:00|10:30|Room 204\n")
            f.write("SE401|Thursday|09:00|10:30|Room 204\n")
            
            # DS101 schedule
            f.write("DS101|Monday|11:00|12:30|Room 301\n")
            f.write("DS101|Wednesday|11:00|12:30|Room 301\n")
            # DS201 schedule
            f.write("DS201|Tuesday|15:00|16:30|Room 302\n")
            f.write("DS201|Thursday|15:00|16:30|Room 302\n")
            # DS301 schedule
            f.write("DS301|Monday|15:00|16:30|Room 303\n")
            f.write("DS301|Wednesday|15:00|16:30|Room 303\n")
            # DS401 schedule
            f.write("DS401|Tuesday|11:00|12:30|Room 304\n")
            f.write("DS401|Thursday|11:00|12:30|Room 304\n")
            
            # General Education courses schedules
            f.write("GE101|Monday|08:00|09:00|Room 401\n")
            f.write("GE101|Wednesday|08:00|09:00|Room 401\n")
            f.write("GE101|Friday|08:00|09:00|Room 401\n")
            
            f.write("GE102|Tuesday|08:00|09:00|Room 402\n")
            f.write("GE102|Thursday|08:00|09:00|Room 402\n")
            f.write("GE102|Friday|08:00|09:00|Room 402\n")
            
            f.write("GE201|Monday|13:00|14:30|Room 403\n")
            f.write("GE201|Wednesday|13:00|14:30|Room 403\n")
            
            f.write("GE301|Tuesday|10:00|11:30|Room 404\n")
            f.write("GE301|Thursday|10:00|11:30|Room 404\n")

# ================ DATA LOADING FUNCTIONS ================
def load_students():
    """Load student data from file into a dictionary"""
    students = {}
    try:
        with open(STUDENTS_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    parts = line.split('|')
                    if len(parts) >= 8:
                        username = parts[0]
                        students[username] = {
                            'password': parts[1],
                            'first_name': parts[2],
                            'last_name': parts[3],
                            'email': parts[4],
                            'phone': parts[5],
                            'major': parts[6],
                            'year': parts[7],
                            'profile_pic': parts[8] if len(parts) > 8 else ""
                        }
    except FileNotFoundError:
        print(f"Students file not found: {STUDENTS_FILE}")
    except Exception as e:
        print(f"Error loading students: {e}")
    
    return students

def load_courses(student_major=None):
    """
    Load course data from file into a dictionary
    If student_major is provided, filter courses to show only:
    1. Courses specific to the student's major
    2. General education courses available to all majors
    """
    courses = {}
    try:
        with open(COURSES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split('|')
                if len(parts) < 10:  # Make sure we have all required fields
                    continue
                
                try:
                    course_id = parts[0].strip()
                    course_major = parts[2].strip()
                    
                    # Filter courses based on student's major if specified
                    if student_major and course_major != "General" and course_major != student_major:
                        continue
                    
                    # Parse prerequisites
                    prerequisites = []
                    if parts[8].strip():
                        prerequisites = [p.strip() for p in parts[8].split(',') if p.strip()]
                    
                    courses[course_id] = {
                        'name': parts[1].strip(),
                        'major': course_major,
                        'credits': int(parts[3]),
                        'instructor': parts[4].strip(),
                        'schedule': parts[5].strip(),
                        'capacity': int(parts[6]),
                        'enrolled': int(parts[7]),
                        'prerequisites': prerequisites,
                        'description': parts[9].strip()
                    }
                except (ValueError, IndexError) as e:
                    print(f"Error parsing course line: {line}, Error: {e}")
                    continue
                    
    except FileNotFoundError:
        print(f"Courses file not found: {COURSES_FILE}")
    except Exception as e:
        print(f"Error loading courses: {e}")
    
    return courses

def load_schedule():
    """Load detailed schedule from file into a dictionary"""
    schedule = {}
    try:
        with open(SCHEDULE_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('|')
                    if len(parts) >= 5:
                        course_id = parts[0]
                        if course_id not in schedule:
                            schedule[course_id] = []
                        schedule[course_id].append({
                            'day': parts[1],
                            'start_time': parts[2],
                            'end_time': parts[3],
                            'room': parts[4]
                        })
    except FileNotFoundError:
        print(f"Schedule file not found: {SCHEDULE_FILE}")
    except Exception as e:
        print(f"Error loading schedule: {e}")
    
    return schedule

def load_enrollments(username):
    """Load enrollment data for a specific user """
    enrollments = []
    try:
        with open(ENROLLMENTS_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('|')
                    if len(parts) >= 4 and parts[0] == username:
                        enrollments.append({
                            'course_id': parts[1],
                            'enrollment_date': parts[2],
                            'status': parts[3]
                        })
    except FileNotFoundError:
        print(f"Enrollments file not found: {ENROLLMENTS_FILE}")
    except Exception as e:
        print(f"Error loading enrollments: {e}")
    
    return enrollments

# ================ DATA SAVING FUNCTIONS ================
def save_student(username, password, first_name, last_name, email, phone, major, year, profile_pic=""):
    """Save a new student to file"""
    try:
        with open(STUDENTS_FILE, 'a') as f:
            f.write(f"{username}|{password}|{first_name}|{last_name}|{email}|{phone}|{major}|{year}|{profile_pic}\n")
        return True
    except Exception as e:
        print(f"Error saving student: {e}")
        return False

def update_student_profile_pic(username, pic_path):
    """Update a student's profile picture"""
    students = load_students()
    if username in students:
        students[username]['profile_pic'] = pic_path
        try:
            with open(STUDENTS_FILE, 'w') as f:
                f.write("# username|password|first_name|last_name|email|phone|major|year|profile_pic\n")
                for user, data in students.items():
                    line = f"{user}|{data['password']}|{data['first_name']}|{data['last_name']}|{data['email']}|{data['phone']}|{data['major']}|{data['year']}|{data['profile_pic']}\n"
                    f.write(line)
            return True 
        except Exception as e:
            print(f"Error updating profile pic: {e}")
            return False  
    return False 

def save_enrollment(username, course_id):
    """Save a new enrollment to file and update course enrollment count """
    try:
        # Get today's date for enrollment record
        enrollment_date = date.today().strftime("%Y-%m-%d")
        
        # Add enrollment record 
        with open(ENROLLMENTS_FILE, 'a') as f:
            f.write(f"{username}|{course_id}|{enrollment_date}|Active\n")
        
        # Update course enrollment count
        update_course_enrollment(course_id)
        return True
    except Exception as e:
        print(f"Error saving enrollment: {e}")
        return False

def update_course_enrollment(course_id):
    """Update the enrolled count for a course"""
    try:
        courses = load_courses()  # Load all courses
        if course_id in courses:
            # Increment enrolled count
            courses[course_id]['enrolled'] += 1
            
            # Write back to file
            with open(COURSES_FILE, 'w') as f:
                f.write("# course_id|course_name|major|credits|instructor|schedule|capacity|enrolled|prerequisites|description\n")
                for cid, course in courses.items():
                    prereqs = ",".join(course['prerequisites']) if course['prerequisites'] else ""
                    f.write(f"{cid}|{course['name']}|{course['major']}|{course['credits']}|{course['instructor']}|{course['schedule']}|{course['capacity']}|{course['enrolled']}|{prereqs}|{course['description']}\n")
    except Exception as e:
        print(f"Error updating course enrollment: {e}")

# ================ VALIDATION FUNCTIONS ================
def check_schedule_conflict(username, new_course_id):
    """
    Check if enrolling in a course creates schedule conflicts
    Returns: (has_conflict, message)
    """
    # Get student's current enrollments
    enrollments = load_enrollments(username)
    # Get detailed schedule information
    schedule = load_schedule()
    
    # Check if the new course has schedule information
    if new_course_id not in schedule:
        return False, "No schedule information available for this course"
    
    # Get the new course's schedule
    new_course_times = schedule[new_course_id]
    
    # Check against each active enrollment
    for enrollment in enrollments:
        if enrollment['status'] == 'Active':
            enrolled_course_id = enrollment['course_id']
            if enrolled_course_id in schedule:
                enrolled_times = schedule[enrolled_course_id]
                
                # Check each time slot of the new course against each time slot of enrolled courses
                for new_time in new_course_times:
                    for enrolled_time in enrolled_times:
                        # Check if same day and overlapping time
                        if (new_time['day'] == enrolled_time['day'] and
                            time_overlap(new_time['start_time'], new_time['end_time'],
                                       enrolled_time['start_time'], enrolled_time['end_time'])):
                            return True, f"Schedule conflict with {enrolled_course_id} on {new_time['day']}"
    
    return False, "No conflicts"

def time_overlap(start1, end1, start2, end2):
    """Check if two time periods overlap"""
    # Convert time strings to minutes for easier comparison
    def time_to_minutes(time_str):
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    
    start1_min = time_to_minutes(start1)
    end1_min = time_to_minutes(end1)
    start2_min = time_to_minutes(start2)
    end2_min = time_to_minutes(end2)
    
    # No overlap if one ends before the other starts
    return not (end1_min <= start2_min or end2_min <= start1_min)

def check_prerequisites(username, course_id):
    """
    Check if student has completed prerequisites for a course
    Returns: (prerequisites_met, message)
    """
    # Load course data
    courses = load_courses()
    if course_id not in courses:
        return False, "Course not found"
    
    # Get prerequisites for the course
    prerequisites = courses[course_id]['prerequisites']
    if not prerequisites:
        return True, "No prerequisites required"
    
    # Get student's enrolled courses (Active status only)
    enrollments = load_enrollments(username)
    enrolled_courses = [e['course_id'] for e in enrollments if e['status'] == 'Active']
    
    # Check if all prerequisites are enrolled 
    missing_prereqs = [prereq for prereq in prerequisites if prereq not in enrolled_courses]
    
    if missing_prereqs:
        # Get the names of missing prerequisite courses for better feedback
        missing_names = []
        for prereq_id in missing_prereqs:
            if prereq_id in courses:
                missing_names.append(f"{prereq_id} ({courses[prereq_id]['name']})")
            else:
                missing_names.append(prereq_id)
        
        return False, f"Missing prerequisites: {', '.join(missing_names)}"
    
    return True, "Prerequisites satisfied"

# ================ UI HELPER FUNCTIONS ================
def clear_window():
    """Remove all widgets from the main window"""
    for widget in root.winfo_children():
        widget.destroy()

def get_theme_colors(major):
    """Get color theme based on student's major"""
    if major in COLOR_THEMES:
        return COLOR_THEMES[major]
    return COLOR_THEMES["default"]

# ================ UI SCREEN FUNCTIONS ================
def show_login_screen():
    """Display login/registration screen"""
    global username_entry, password_entry
    clear_window()
    
    # Main frame with neutral color
    main_frame = tk.Frame(root, bg='#E6E6FA')  # Light lavender background
    main_frame.pack(fill='both', expand=True, padx=50, pady=50)
    
    # Title
    title_label = tk.Label(main_frame, text="📝 EnrollZone", 
                          font=('Arial', 24, 'bold'), bg='#E6E6FA', fg='blue')
    title_label.pack(pady=(0, 30))
    
    # Login frame
    login_frame = tk.LabelFrame(main_frame, text="Student Login", 
                               font=('Arial', 14, 'bold'), bg='#E6E6FA')
    login_frame.pack(fill='x', pady=(0, 20))
    
    # Username
    tk.Label(login_frame, text="Username:", font=('Arial', 12), bg='#E6E6FA').pack(anchor='w', padx=20, pady=(20, 5))
    username_entry = tk.Entry(login_frame, font=('Arial', 12), width=30)
    username_entry.pack(padx=20, pady=(0, 10))
    
    # Password
    tk.Label(login_frame, text="Password:", font=('Arial', 12), bg='#E6E6FA').pack(anchor='w', padx=20, pady=(0, 5))
    password_entry = tk.Entry(login_frame, font=('Arial', 12), width=30, show="*")
    password_entry.pack(padx=20, pady=(0, 20))
    
    # Login button
    login_btn = tk.Button(login_frame, text="Login", font=('Arial', 12, 'bold'),
                         bg='lightblue', padx=30, pady=10, command=login_student)
    login_btn.pack(pady=(0, 20))
    
    # Registration frame
    reg_frame = tk.LabelFrame(main_frame, text="New Student Registration", 
                             font=('Arial', 14, 'bold'), bg='#E6E6FA')
    reg_frame.pack(fill='x')
    
    # Registration button
    reg_btn = tk.Button(reg_frame, text="Create New Account", font=('Arial', 12, 'bold'),
                       bg='lightgreen', padx=30, pady=10, command=show_registration_screen)
    reg_btn.pack(pady=20)
    
    # Set focus to username field
    username_entry.focus()

def show_registration_screen():
    """Display student registration screen"""
    global first_name_entry, last_name_entry, email_entry, phone_entry
    global reg_username_entry, reg_password_entry, major_entry, year_var
    
    clear_window()
    
    # Main frame
    main_frame = tk.Frame(root, bg='white')
    main_frame.pack(fill='both', expand=True, padx=50, pady=30)
    
    # Title
    title_label = tk.Label(main_frame, text="Create Student Account", 
                          font=('Arial', 20, 'bold'), bg='white', fg='blue')
    title_label.pack(pady=(0, 20))
    
    # Form frame
    form_frame = tk.Frame(main_frame, bg='white')
    form_frame.pack(fill='both', expand=True)
    
    # Left column
    left_frame = tk.Frame(form_frame, bg='white')
    left_frame.pack(side='left', fill='both', expand=True, padx=(0, 20))
    
    tk.Label(left_frame, text="Personal Information", font=('Arial', 14, 'bold'), bg='white').pack(anchor='w', pady=(0, 10))
    
    # First Name
    tk.Label(left_frame, text="First Name:", font=('Arial', 11), bg='white').pack(anchor='w')
    first_name_entry = tk.Entry(left_frame, font=('Arial', 11), width=25)
    first_name_entry.pack(anchor='w', pady=(0, 10))
    
    # Last Name
    tk.Label(left_frame, text="Last Name:", font=('Arial', 11), bg='white').pack(anchor='w')
    last_name_entry = tk.Entry(left_frame, font=('Arial', 11), width=25)
    last_name_entry.pack(anchor='w', pady=(0, 10))
    
    # Email
    tk.Label(left_frame, text="Email:", font=('Arial', 11), bg='white').pack(anchor='w')
    email_entry = tk.Entry(left_frame, font=('Arial', 11), width=25)
    email_entry.pack(anchor='w', pady=(0, 10))
    
    # Phone
    tk.Label(left_frame, text="Phone:", font=('Arial', 11), bg='white').pack(anchor='w')
    phone_entry = tk.Entry(left_frame, font=('Arial', 11), width=25)
    phone_entry.pack(anchor='w', pady=(0, 10))
    
    # Right column
    right_frame = tk.Frame(form_frame, bg='white')
    right_frame.pack(side='right', fill='both', expand=True)
    
    tk.Label(right_frame, text="Account Information", font=('Arial', 14, 'bold'), bg='white').pack(anchor='w', pady=(0, 10))
    
    # Username
    tk.Label(right_frame, text="Username:", font=('Arial', 11), bg='white').pack(anchor='w')
    reg_username_entry = tk.Entry(right_frame, font=('Arial', 11), width=25)
    reg_username_entry.pack(anchor='w', pady=(0, 10))
    
    # Password
    tk.Label(right_frame, text="Password:", font=('Arial', 11), bg='white').pack(anchor='w')
    reg_password_entry = tk.Entry(right_frame, font=('Arial', 11), width=25, show="*")
    reg_password_entry.pack(anchor='w', pady=(0, 10))
    
    # Major - Now using a dropdown with the three majors
    tk.Label(right_frame, text="Major:", font=('Arial', 11), bg='white').pack(anchor='w')
    major_var = tk.StringVar(value="Computer Science")
    major_combo = ttk.Combobox(right_frame, textvariable=major_var, width=22,
                             values=["Computer Science", "Software Engineering", "Data Science"])
    major_combo.pack(anchor='w', pady=(0, 10))
    major_entry = major_combo
    
    # Year
    tk.Label(right_frame, text="Academic Year:", font=('Arial', 11), bg='white').pack(anchor='w')
    year_var = tk.StringVar(value="First")
    year_combo = ttk.Combobox(right_frame, textvariable=year_var, width=22,
                             values=["First", "Second", "Third", "Fourth"])
    year_combo.pack(anchor='w', pady=(0, 20))
    
    # Buttons frame
    buttons_frame = tk.Frame(main_frame, bg='white')
    buttons_frame.pack(fill='x', pady=20)
    
    # Register button
    register_btn = tk.Button(buttons_frame, text="Create Account", font=('Arial', 12, 'bold'),
                           bg='lightgreen', padx=30, pady=10, command=register_student)
    register_btn.pack(side='left', padx=(0, 10))
    
    # Back button
    back_btn = tk.Button(buttons_frame, text="Back to Login", font=('Arial', 12),
                       bg='lightgray', padx=30, pady=10, command=show_login_screen)
    back_btn.pack(side='left')

def login_student():
    """Handle student login authentication"""
    global current_student
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    # Validate input
    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password!")
        return
    
    # Check credentials
    students = load_students()
    if username in students:
        if students[username]["password"] == password:
            current_student = username
            # Show the appropriate dashboard based on major
            show_major_dashboard(students[username]["major"])
        else:
            messagebox.showerror("Error", "Invalid username or password!")
    else:
        messagebox.showerror("Error", "Username not found.")

def register_student():
    """Handle student registration"""
    # Get form data
    first_name = first_name_entry.get().strip()
    last_name = last_name_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()
    username = reg_username_entry.get().strip()
    password = reg_password_entry.get().strip()
    major = major_entry.get()
    year = year_var.get()
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        
    # Validate required fields
    if not all([first_name, last_name, email, username, password, major]):
        messagebox.showerror("Error", "Please fill in all required fields!")
        return

    #validate email pattern
    if not re.match(email_pattern, email):
        messagebox.showerror("Invalid Email", "Please enter a valid email address.")
        return

    # Phone number validation: must be 11 digits and numeric
    if not (phone.isdigit() and len(phone) == 11):
        messagebox.showerror("Invalid Phone Number", "Phone number must be exactly 11 digits.")
        return

    # Check if username already exists
    students = load_students()
    if username in students:
        messagebox.showerror("Error", "Username already exists!")
        return

    # Save the new student
    if save_student(username, password, first_name, last_name, email, phone, major, year):
        messagebox.showinfo("Success", "Account created successfully! You can now login.")
        show_login_screen()
    else:
        messagebox.showerror("Error", "Failed to create account!")

def show_major_dashboard(major):
    """Display dashboard specific to student's major"""
    global current_student
    
    clear_window()
    
    # Get color theme based on major
    theme = get_theme_colors(major)
    
    # Create header with major-specific color
    header_frame = tk.Frame(root, bg=theme["primary"])
    header_frame.pack(fill='x')
    
    # Major-specific welcome message
    header_label = tk.Label(
        header_frame, 
        text=f"{major} Student Dashboard", 
        font=('Arial', 18, 'bold'), 
        bg=theme["primary"], 
        fg="white", 
        padx=20, 
        pady=10
    )
    header_label.pack(side='left')
    
    # Get student name for personalized welcome
    students = load_students()
    student_name = f"{students[current_student]['first_name']} {students[current_student]['last_name']}"
    
    # Welcome message with student name
    welcome_label = tk.Label(
        header_frame, 
        text=f"Welcome, {student_name}!", 
        font=('Arial', 12), 
        bg=theme["primary"], 
        fg="white", 
        padx=20
    )
    welcome_label.pack(side='left')
    
    # Logout button in header
    logout_btn = tk.Button(
        header_frame, 
        text="Logout", 
        font=('Arial', 10, 'bold'),
        bg='red', 
        fg='white', 
        padx=10, 
        pady=5, 
        command=logout
    )
    logout_btn.pack(side='right', padx=20, pady=10)
    
    # Create notebook for tabs with themed style
    style = ttk.Style()
    style.configure("TNotebook", background=theme["secondary"])
    style.configure("TNotebook.Tab", background=theme["secondary"], foreground=theme["text"])
    style.map("TNotebook.Tab", background=[("selected", theme["accent"])], 
              foreground=[("selected", "white")])
    
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Create tabs with major-specific filtering
    create_courses_tab(notebook, major, theme)
    create_enrollment_tab(notebook, theme)
    create_schedule_tab(notebook, theme)
    create_profile_tab(notebook, theme)

def create_courses_tab(notebook, major, theme):
    """Create course catalog tab with major-specific filtering"""
    global courses_tree
    
    courses_frame = tk.Frame(notebook, bg=theme["secondary"])
    notebook.add(courses_frame, text="Course Catalog")

    # Title
    title_label = tk.Label(
        courses_frame, 
        text=f"Available Courses for {major} Students", 
        font=('Arial', 18, 'bold'), 
        bg=theme["secondary"], 
        fg=theme["text"]
    )
    title_label.pack(pady=20)
    
    # Courses list frame
    list_frame = tk.Frame(courses_frame, bg=theme["secondary"])
    list_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
    
    # Create treeview for courses
    columns = ('Course ID', 'Course Name', 'Major', 'Credits', 'Instructor', 'Schedule', 'Capacity')
    courses_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
    
    # Define headings
    for col in columns:
        courses_tree.heading(col, text=col)
        courses_tree.column(col, width=120)
    
    # Scrollbar
    scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=courses_tree.yview)
    courses_tree.configure(yscrollcommand=scrollbar.set)
    
    # Pack treeview and scrollbar
    courses_tree.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    
    # Buttons frame
    buttons_frame = tk.Frame(courses_frame, bg=theme["secondary"])
    buttons_frame.pack(fill='x', padx=20, pady=10)
    
    # Course details button
    details_btn = tk.Button(
        buttons_frame, 
        text="View Course Details", 
        font=('Arial', 11, 'bold'),
        bg=theme["button"], 
        fg=theme["button_text"], 
        padx=20, 
        pady=8, 
        command=view_course_details
    )
    details_btn.pack(side='left', padx=(0, 10))
    
    # Enroll button
    enroll_btn = tk.Button(
        buttons_frame, 
        text="Enroll in Course", 
        font=('Arial', 11, 'bold'),
        bg='green', 
        fg='white', 
        padx=20, 
        pady=8, 
        command=enroll_in_course
    )
    enroll_btn.pack(side='left', padx=(0, 10))
    
    # Refresh button
    refresh_btn = tk.Button(
        buttons_frame, 
        text="Refresh", 
        font=('Arial', 11, 'bold'),
        bg='lightgray', 
        padx=20, 
        pady=8, 
        command=lambda: load_courses_list(major)
    )
    refresh_btn.pack(side='left')
    
    # Load courses filtered by major
    load_courses_list(major)

def create_enrollment_tab(notebook, theme):
    """Create enrollment management tab"""
    global enrollment_tree
    
    enrollment_frame = tk.Frame(notebook, bg=theme["secondary"])
    notebook.add(enrollment_frame, text="My Enrollments")

    # Title
    title_label = tk.Label(
        enrollment_frame, 
        text="My Course Enrollments", 
        font=('Arial', 18, 'bold'), 
        bg=theme["secondary"], 
        fg=theme["text"]
    )
    title_label.pack(pady=20)
    
    # Enrollments list frame
    list_frame = tk.Frame(enrollment_frame, bg=theme["secondary"])
    list_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
    
    # Create treeview for enrollments 
    columns = ('Course ID', 'Course Name', 'Credits', 'Enrollment Date', 'Status')
    enrollment_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
    
    # Define headings
    for col in columns:
        enrollment_tree.heading(col, text=col)
        enrollment_tree.column(col, width=140)  # Wider columns since we have fewer
    
    # Scrollbar
    scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=enrollment_tree.yview)
    enrollment_tree.configure(yscrollcommand=scrollbar.set)
    
    # Pack treeview and scrollbar
    enrollment_tree.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    
    # Buttons frame 
    buttons_frame = tk.Frame(enrollment_frame, bg=theme["secondary"])
    buttons_frame.pack(fill='x', padx=20, pady=10)
    
    # Drop course button
    drop_btn = tk.Button(
        buttons_frame, 
        text="Drop Course", 
        font=('Arial', 11, 'bold'),
        bg='red', 
        fg='white', 
        padx=20, 
        pady=8, 
        command=drop_course
    )
    drop_btn.pack(side='left', padx=(0, 10))
    
    # Refresh button
    refresh_btn = tk.Button(
        buttons_frame, 
        text="Refresh", 
        font=('Arial', 11, 'bold'),
        bg='lightgray', 
        padx=20, 
        pady=8, 
        command=load_enrollments_list
    )
    refresh_btn.pack(side='left')
    
    # Load enrollments
    load_enrollments_list()

def create_schedule_tab(notebook, theme):
    """Create schedule management tab"""
    global schedule_tree
    
    schedule_frame = tk.Frame(notebook, bg=theme["secondary"])
    notebook.add(schedule_frame, text="My Schedule")

    # Title
    title_label = tk.Label(
        schedule_frame, 
        text="My Class Schedule", 
        font=('Arial', 18, 'bold'), 
        bg=theme["secondary"], 
        fg=theme["text"]
    )
    title_label.pack(pady=20)
    
    # Schedule list frame
    list_frame = tk.Frame(schedule_frame, bg=theme["secondary"])
    list_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
    
    # Create treeview for schedule
    columns = ('Day', 'Time', 'Course ID', 'Course Name', 'Room')
    schedule_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
    
    # Define headings
    for col in columns:
        schedule_tree.heading(col, text=col)
        schedule_tree.column(col, width=120)
    
    # Scrollbar
    scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=schedule_tree.yview)
    schedule_tree.configure(yscrollcommand=scrollbar.set)
    
    # Pack treeview and scrollbar
    schedule_tree.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    
    # Refresh button
    refresh_btn = tk.Button(
        schedule_frame, 
        text="Refresh Schedule", 
        font=('Arial', 11, 'bold'),
        bg=theme["button"], 
        fg=theme["button_text"], 
        padx=20, 
        pady=8, 
        command=load_student_schedule
    )
    refresh_btn.pack(pady=10)
    
    # Load schedule
    load_student_schedule()

def create_profile_tab(notebook, theme):
    """Create profile tab"""
    global profile_pic_label
    
    profile_frame = tk.Frame(notebook, bg=theme["secondary"])
    notebook.add(profile_frame, text="My Profile")
    
    # Main container
    main_container = tk.Frame(profile_frame, bg=theme["secondary"])
    main_container.pack(fill='both', expand=True, padx=30, pady=20)
    
    # Title
    title_label = tk.Label(
        main_container, 
        text="Student Profile", 
        font=('Arial', 18, 'bold'), 
        bg=theme["secondary"], 
        fg=theme["text"]
    )
    title_label.pack(pady=(0, 20))
    
    # Profile content frame
    content_frame = tk.Frame(main_container, bg=theme["secondary"])
    content_frame.pack(fill='both', expand=True)
    
    # Left side - Profile picture
    left_frame = tk.Frame(content_frame, bg=theme["secondary"])
    left_frame.pack(side='left', fill='y', padx=(0, 30))
    
    # Profile picture frame
    pic_frame = tk.LabelFrame(
        left_frame, 
        text="Profile Picture", 
        font=('Arial', 12, 'bold'), 
        bg=theme["secondary"],
        fg=theme["text"]
    )
    pic_frame.pack(fill='x', pady=(0, 20))
    
    # Profile picture label
    profile_pic_label = tk.Label(
        pic_frame, 
        text="No Picture", 
        width=20, 
        height=10,
        bg='lightgray', 
        relief='solid', 
        bd=1
    )
    profile_pic_label.pack(padx=10, pady=10)
    
    # Upload picture button
    upload_btn = tk.Button(
        pic_frame, 
        text="Upload Picture", 
        font=('Arial', 10, 'bold'),
        bg=theme["button"], 
        fg=theme["button_text"], 
        padx=15, 
        pady=5, 
        command=upload_profile_picture
    )
    upload_btn.pack(pady=(0, 10))
    
    # Right side - Profile information
    right_frame = tk.Frame(content_frame, bg=theme["secondary"])
    right_frame.pack(side='right', fill='both', expand=True)
    
    # Profile info frame
    info_frame = tk.LabelFrame(
        right_frame, 
        text="Personal Information", 
        font=('Arial', 12, 'bold'), 
        bg=theme["secondary"],
        fg=theme["text"]
    )
    info_frame.pack(fill='both', expand=True)
    
    # Load and display profile information
    load_profile_info(info_frame, theme)

# ================ ACTION FUNCTIONS ================
def enroll_in_course():
    """Handle course enrollment with validation"""
    # Check if a course is selected
    selected = courses_tree.selection()
    if not selected:
        messagebox.showwarning("Select Course", "Please select a course to enroll in.")
        return

    # Get course ID from selection
    item = courses_tree.item(selected[0])
    course_id = item['values'][0]
    
    # Check if already enrolled
    enrollments = load_enrollments(current_student)
    for enrollment in enrollments:
        if enrollment['course_id'] == course_id and enrollment['status'] == 'Active':
            messagebox.showwarning("Already Enrolled", "You are already enrolled in this course!")
            return
    
    # Check prerequisites
    prereq_ok, prereq_msg = check_prerequisites(current_student, course_id)
    if not prereq_ok:
        messagebox.showerror("Prerequisites Not Met", prereq_msg)
        return
    
    # Check schedule conflicts
    conflict, conflict_msg = check_schedule_conflict(current_student, course_id)
    if conflict:
        result = messagebox.askyesno("Schedule Conflict", 
                                   f"{conflict_msg}\n\nDo you want to enroll anyway?")
        if not result:
            return
    
    # Check capacity
    courses = load_courses()
    course = courses[course_id]
    if course['enrolled'] >= course['capacity']:
        messagebox.showerror("Course Full", "This course has reached its maximum capacity!")
        return
    
    # Enroll the student
    if save_enrollment(current_student, course_id):
        messagebox.showinfo("Success", f"Successfully enrolled in {course['name']}!")
        
        # Get student's major for refreshing the course list
        students = load_students()
        student_major = students[current_student]['major']
        
        # Refresh all views
        load_courses_list(student_major)
        load_enrollments_list()
        load_student_schedule()
    else:
        messagebox.showerror("Error", "Failed to enroll in course!")

def drop_course():
    """Handle course dropping"""
    # Check if a course is selected
    selected = enrollment_tree.selection()
    if not selected:
        messagebox.showwarning("Select Course", "Please select a course to drop.")
        return

    # Get course ID from selection
    item = enrollment_tree.item(selected[0])
    course_id = item['values'][0]
    status = item['values'][4]  # Status column
    
    # Check if course is already dropped
    if status != "Active":
        messagebox.showwarning("Cannot Drop", f"Course is already {status}.")
        return
    
    # Confirm drop
    result = messagebox.askyesno("Confirm Drop", 
                               f"Are you sure you want to drop {course_id}?")
    if not result:
        return
    
    # Update enrollment status
    try:
        enrollments = []
        with open(ENROLLMENTS_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('|')
                    if len(parts) >= 4:
                        if parts[0] == current_student and parts[1] == course_id and parts[3] == 'Active':
                            parts[3] = 'Dropped'
                        enrollments.append('|'.join(parts))
                else:
                    enrollments.append(line)
        
        with open(ENROLLMENTS_FILE, 'w') as f:
            for enrollment in enrollments:
                f.write(enrollment + '\n')
        
        # Update course enrollment count
        courses = load_courses()
        if course_id in courses:
            courses[course_id]['enrolled'] = max(0, courses[course_id]['enrolled'] - 1)
            
            with open(COURSES_FILE, 'w') as f:
                f.write("# course_id|course_name|major|credits|instructor|schedule|capacity|enrolled|prerequisites|description\n")
                for cid, course in courses.items():
                    prereqs = ",".join(course['prerequisites']) if course['prerequisites'] else ""
                    f.write(f"{cid}|{course['name']}|{course['major']}|{course['credits']}|{course['instructor']}|{course['schedule']}|{course['capacity']}|{course['enrolled']}|{prereqs}|{course['description']}\n")
        
        messagebox.showinfo("Success", f"Successfully dropped {course_id}!")
        
        # Get student's major for refreshing the course list
        students = load_students()
        student_major = students[current_student]['major']
        
        # Refresh all views
        load_courses_list(student_major)
        load_enrollments_list()
        load_student_schedule()
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to drop course: {e}")

def upload_profile_picture():
    """Upload profile picture"""
    try:
        path = filedialog.askopenfilename(
            title="Choose Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        
        if path:
            if update_student_profile_pic(current_student, path):
                messagebox.showinfo("Success", "Profile picture uploaded successfully!")
                load_profile_picture()
            else:
                messagebox.showerror("Error", "Failed to save profile picture!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to upload picture: {e}")

def view_course_details():
    """View details of selected course"""
    # Check if a course is selected
    selected = courses_tree.selection()
    if not selected:
        messagebox.showwarning("Select Course", "Please select a course.")
        return

    # Get course ID from selection
    item = courses_tree.item(selected[0])
    course_id = item['values'][0]

    # Load course data
    courses = load_courses()
    if course_id not in courses:
        messagebox.showerror("Error", "Course not found!")
        return
        
    course = courses[course_id]
    
    # Get student's major for theming
    students = load_students()
    student_major = students[current_student]['major']
    theme = get_theme_colors(student_major)

    # Create details window
    details_window = tk.Toplevel(root)
    details_window.title("Course Details")
    details_window.geometry("500x400")
    details_window.configure(bg=theme["secondary"])

    # Course info
    info_text = f"""Course ID: {course_id}
Name: {course['name']}
Major: {course['major']}
Credits: {course['credits']}
Instructor: {course['instructor']}
Schedule: {course['schedule']}
Capacity: {course['enrolled']}/{course['capacity']}
Prerequisites: {', '.join(course['prerequisites']) if course['prerequisites'] else 'None'}
Description: {course['description']}"""

    info_label = tk.Label(
        details_window, 
        text=info_text, 
        justify='left', 
        font=('Arial', 10), 
        bg=theme["secondary"], 
        fg=theme["text"],
        wraplength=450
    )
    info_label.pack(padx=20, pady=20)

    # Close button
    close_btn = tk.Button(
        details_window, 
        text="Close", 
        bg=theme["button"], 
        fg=theme["button_text"],
        font=('Arial', 10), 
        command=details_window.destroy
    )
    close_btn.pack(pady=10)

def logout():
    """Logout and return to login screen"""
    global current_student
    current_student = None
    show_login_screen()

# ================ DATA DISPLAY FUNCTIONS ================
def load_courses_list(major=None):
    """Load courses into treeview, filtered by major if specified"""
    try:
        # Clear existing items
        for item in courses_tree.get_children():
            courses_tree.delete(item)
        
        # Load courses, filtered by major if specified
        courses = load_courses(major)
        
        for course_id, course_data in courses.items():
            capacity_text = f"{course_data['enrolled']}/{course_data['capacity']}"
            
            courses_tree.insert('', 'end', values=(
                course_id,
                course_data['name'],
                course_data['major'],
                course_data['credits'],
                course_data['instructor'],
                course_data['schedule'],
                capacity_text
            ))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load courses: {e}")

def load_enrollments_list():
    """Load student enrollments into treeview"""
    try:
        # Clear existing items
        for item in enrollment_tree.get_children():
            enrollment_tree.delete(item)
        
        enrollments = load_enrollments(current_student)
        courses = load_courses()  # Load all courses regardless of major
        
        for enrollment in enrollments:
            course_id = enrollment['course_id']
            if course_id in courses:
                course = courses[course_id]

                enrollment_tree.insert('', 'end', values=(
                    course_id,
                    course['name'],
                    course['credits'],
                    enrollment['enrollment_date'],
                    enrollment['status']
                ))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load enrollments: {e}")

def load_student_schedule():
    """Load student's schedule into treeview, organized by day"""
    try:
        # Clear existing items
        for item in schedule_tree.get_children():
            schedule_tree.delete(item)
        
        # Get student's active enrollments
        enrollments = load_enrollments(current_student)
        active_enrollments = [e['course_id'] for e in enrollments if e['status'] == 'Active']
        
        if not active_enrollments:
            # If no active enrollments, show a message
            schedule_tree.insert('', 'end', values=('', 'No active enrollments', '', '', ''))
            return
        
        # Load all courses and schedule data
        courses = load_courses()  # Load all courses regardless of major
        schedule = load_schedule()
        
        # Days of the week for sorting
        days_order = {
            'Monday': 1,
            'Tuesday': 2,
            'Wednesday': 3,
            'Thursday': 4,
            'Friday': 5,
            'Saturday': 6,
            'Sunday': 7
        }
        
        # Collect all schedule entries
        schedule_entries = []
        
        for course_id in active_enrollments:
            if course_id in courses and course_id in schedule:
                course = courses[course_id]
                course_schedule = schedule[course_id]
                
                for time_slot in course_schedule:
                    schedule_entries.append({
                        'day': time_slot['day'],
                        'day_order': days_order.get(time_slot['day'], 99),  # For sorting
                        'time': f"{time_slot['start_time']}-{time_slot['end_time']}",
                        'start_time': time_slot['start_time'],  # For sorting
                        'course_id': course_id,
                        'course_name': course['name'],
                        'room': time_slot['room']
                    })
        
        # Sort by day and then by start time
        schedule_entries.sort(key=lambda x: (x['day_order'], x['start_time']))
        
        # Insert into treeview
        for entry in schedule_entries:
            schedule_tree.insert('', 'end', values=(
                entry['day'],
                entry['time'],
                entry['course_id'],
                entry['course_name'],
                entry['room']
            ))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load schedule: {e}")

def load_profile_info(frame, theme):
    """Load and display profile information"""
    students = load_students()
    
    if current_student not in students:
        tk.Label(frame, text="Error loading profile", bg=theme["secondary"]).pack()
        return
    
    student = students[current_student]

    # Remove old widgets
    for widget in frame.winfo_children():
        widget.destroy()

    # Prepare info text
    info_text = f"""Name: {student['first_name']} {student['last_name']}
Username: {current_student}
Email: {student['email']}
Phone: {student['phone']}
Major: {student['major']}
Academic Year: {student['year']}"""

    # Create label to show the info
    info_label = tk.Label(
        frame, 
        text=info_text, 
        font=('Arial', 11), 
        bg=theme["secondary"], 
        fg=theme["text"], 
        justify='left'
    )
    info_label.pack(padx=20, pady=20)

    # Load profile picture
    load_profile_picture()

def load_profile_picture():
    """Load and display profile picture"""
    students = load_students()
    student = students[current_student]
    pic_path = student["profile_pic"]
    
    if pic_path and os.path.exists(pic_path):
        try:
            profile_pic_label.configure(text=f"Picture: {os.path.basename(pic_path)}")
        except:
            profile_pic_label.configure(text="Error loading picture")
    else:
        profile_pic_label.configure(text="No Picture")

# ================ MAIN FUNCTION ================
def main():
    """Main function to start the application"""
    global root
    
    root = tk.Tk()
    root.title("📝 EnrollZone - Smart Enroll, Study Smooth")
    root.geometry("1200x800")
    root.configure(bg='white')
    
    init_data_files()
    show_login_screen()
    
    root.mainloop()

# Run the application by directly calling main()
main()
