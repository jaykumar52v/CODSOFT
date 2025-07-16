import tkinter as tk
from tkinter import scrolledtext, ttk
from difflib import get_close_matches
import random
import re

class StudentChatbot:
    def __init__(self, master):
        self.master = master
        self.master.title("Student Information System")
        self.master.geometry("750x650")
        self.setup_ui()
        
        # Configure chat display tags
        self.configure_tags()
        
        # Initialize student database
        self.students = self.create_student_database()
        
        # Conversation state
        self.current_context = None
        self.pending_action = None
        
        # Show welcome message
        self.show_welcome()

    def setup_ui(self):
        """Create the main application interface"""
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            self.main_frame,
            wrap=tk.WORD,
            width=80,
            height=28,
            font=('Segoe UI', 11),
            state='disabled'
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Input frame
        input_frame = ttk.Frame(self.main_frame)
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        # User input field
        self.user_input = ttk.Entry(
            input_frame,
            font=('Segoe UI', 12)
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.user_input.bind('<Return>', self.process_input)
        
        # Send button
        send_btn = ttk.Button(
            input_frame,
            text="Send",
            command=self.process_input
        )
        send_btn.pack(side=tk.RIGHT)
        
        # Make input field focused by default
        self.user_input.focus_set()

    def configure_tags(self):
        """Configure text tags for chat display"""
        self.chat_display.tag_config('system', foreground='#1E88E5', font=('Segoe UI', 11, 'bold'))
        self.chat_display.tag_config('user', foreground='#43A047', font=('Segoe UI', 11))
        self.chat_display.tag_config('alert', foreground='#E53935', font=('Segoe UI', 11))
        self.chat_display.tag_config('success', foreground='#7CB342', font=('Segoe UI', 11))

    def create_student_database(self):
        """Create a comprehensive student database with sample data"""
        students = [
            {
                'id': 101,
                'name': 'Alex Johnson',
                'class': '12A',
                'grades': {
                    'Math': {2020: 85, 2021: 88, 2022: 90},
                    'Science': {2020: 82, 2021: 85, 2022: 87},
                    'English': {2020: 78, 2021: 82, 2022: 83}
                },
                'contact': 'alex.johnson@school.edu',
                'address': '123 Maple Street',
                'attendance': {2020: 92, 2021: 88, 2022: 95},
                'extracurricular': ['Debate Club', 'Basketball']
            },
            {
                'id': 102,
                'name': 'Sam Wilson',
                'class': '11B',
                'grades': {
                    'Math': {2020: 92, 2021: 85, 2022: 82},
                    'Science': {2020: 94, 2021: 89, 2022: 90},
                    'English': {2020: 85, 2021: 82, 2022: 84}
                },
                'contact': 'sam.wilson@school.edu',
                'address': '456 Oak Avenue',
                'attendance': {2020: 85, 2021: 90, 2022: 88},
                'extracurricular': ['Science Club', 'Robotics']
            },
            {
                'id': 103,
                'name': 'Taylor Kim',
                'class': '12A',
                'grades': {
                    'Math': {2020: 78, 2021: 82, 2022: 85},
                    'Science': {2020: 85, 2021: 88, 2022: 90},
                    'English': {2020: 92, 2021: 89, 2022: 94}
                },
                'contact': 'taylor.kim@school.edu',
                'address': '789 Pine Road',
                'attendance': {2020: 90, 2021: 92, 2022: 93},
                'extracurricular': ['Student Council', 'Drama Club']
            },
            {
                'id': 104,
                'name': 'Jordan Chen',
                'class': '11B',
                'grades': {
                    'Math': {2020: 88, 2021: 90, 2022: 93},
                    'Science': {2020: 82, 2021: 85, 2022: 88},
                    'English': {2020: 78, 2021: 81, 2022: 84}
                },
                'contact': 'jordan.chen@school.edu',
                'address': '321 Elm Street',
                'attendance': {2020: 89, 2021: 91, 2022: 93},
                'extracurricular': ['Music Band', 'Chess Club']
            },
            {
                'id': 105,
                'name': 'Morgan Davis',
                'class': '12B',
                'grades': {
                    'Math': {2020: 85, 2021: 88, 2022: 91},
                    'Science': {2020: 92, 2021: 89, 2022: 93},
                    'English': {2020: 87, 2021: 85, 2022: 89}
                },
                'contact': 'morgan.davis@school.edu',
                'address': '654 Birch Lane',
                'attendance': {2020: 94, 2021: 92, 2022: 95},
                'extracurricular': ['Debate Club', 'Yearbook']
            }
        ]
        return students

    def show_welcome(self):
        """Display welcome message and help information"""
        welcome_msg = """╔═══════════════════════════╗
║  Student Information System  ║
╚═══════════════════════════╝

Welcome! I can help you with:

• Student details and records
• Academic performance tracking
• Class statistics and averages
• Contact information
• Extracurricular activities

Just ask naturally, like:
"Show me Alex's grades in Math."
"What's the average for class 12A?"
"List all students."

Type 'help' anytime for assistance.
"""
        self.display_message('system', welcome_msg)

    def display_message(self, tag, message):
        """Display a message in the chat window"""
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, message + '\n\n', tag)
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

    def process_input(self, event=None):
        """Process user input and generate response"""
        query = self.user_input.get().strip()
        if not query:
            return
            
        self.display_message('user', f"You: {query}")
        self.user_input.delete(0, tk.END)
        
        query = query.lower()
        
        # Handle conversation context if set
        if self.current_context:
            self.handle_context(query)
            return
        
        # Process greetings
        if self.check_greeting(query):
            return
            
        # Process help request
        if 'help' in query:
            self.show_help_menu()
            return
            
        # Process student details requests
        if any(word in query for word in ['detail', 'info', 'about', 'contact']):
            self.process_student_query(query)
            return
            
        # Process grade/marks requests
        if any(word in query for word in ['grade', 'mark', 'score', 'result']):
            self.process_grade_query(query)
            return
            
        # Process class statistics
        if any(word in query for word in ['average', 'statistics', 'performance']):
            self.process_statistics_query(query)
            return
            
        # Process list requests
        if any(word in query for word in ['list', 'show', 'all']):
            self.process_list_query(query)
            return
            
        # Process attendance requests
        if 'attendance' in query:
            self.process_attendance_query(query)
            return
            
        # Process extracurricular requests
        if any(word in query for word in ['activity', 'club', 'extracurricular']):
            self.process_activity_query(query)
            return
            
        # Default response for unrecognized queries
        self.default_response(query)

    def check_greeting(self, query):
        """Check for and respond to greetings"""
        greetings = {
            'hi': ["Hello! How can I assist you today?"],
            'hello': ["Hi there! What would you like to know?"],
            'hey': ["Hey! Ready to explore student information?"],
            'greetings': ["Greetings! How may I help you?"]
        }
        
        for word in greetings:
            if word in query:
                response = random.choice(greetings[word])
                self.display_message('system', f"Bot: {response}")
                return True
        return False

    def show_help_menu(self):
        """Display the help menu with available commands"""
        help_msg = """╔════════════ Help Menu ═══════════╗
║ 1. Student Details              ║
║   - "Tell me about [student]"   ║
║   - "[Name]'s contact info"     ║
║   - "Show [ID] details"         ║
║                                 ║
║ 2. Academic Information         ║
║   - "[Name]'s math grades"      ║
║   - "Grades for [ID] in 2022"   ║
║   - "Show [student]'s results"  ║
║                                 ║
║ 3. Class Statistics             ║
║   - "Class 12A average"         ║
║   - "Science performance 11B"   ║
║   - "Attendance stats"          ║
║                                 ║
║ 4. General                      ║
║   - "List all students"         ║
║   - "Show extracurriculars"     ║
║   - "Exit"                      ║
╚═════════════════════════════════╝
"""
        self.display_message('system', help_msg)

    def process_student_query(self, query):
        """Process queries about student details"""
        # Extract student identifier (name or ID)
        identifier = None
        
        # Check if query contains a student ID
        id_match = re.search(r'\d{3}', query)
        if id_match:
            identifier = int(id_match.group())
        else:
            # Try to find a student name
            for student in self.students:
                if student['name'].lower() in query:
                    identifier = student['id']
                    break
            
            if not identifier:
                # Try to extract possible name
                name_parts = [word.title() for word in query.split() if word.isalpha()]
                possible_name = ' '.join(name_parts[:2]) if len(name_parts) > 1 else name_parts[0] if name_parts else None
                
                if possible_name:
                    identifier = next((s['id'] for s in self.students if possible_name in s['name']), None)
        
        if identifier:
            student = next((s for s in self.students if s['id'] == identifier), None)
            if student:
                self.display_student_details(student)
            else:
                self.display_message('alert', "Bot: Student not found. Please check the ID or name.")
        else:
            self.current_context = 'student_query'
            self.pending_action = 'get_details'
            self.display_message('system', "Bot: Which student would you like information about? Please provide a name or ID.")

    def display_student_details(self, student):
        """Display comprehensive student details"""
        details = f"""
╔══════════ Student Details ══════════╗
║ ID: {student['id']:<35} ║
║ Name: {student['name']:<32} ║
║ Class: {student['class']:<33} ║
║ Contact: {student['contact']:<30} ║
║ Address: {student['address']:<31} ║
╟─────────────────────────────────────╢
║ Grades:                             ║"""
        
        for subject, grades in student['grades'].items():
            details += f"\n║   {subject}: {', '.join(f'{yr}={score}' for yr, score in grades.items())}"
        
        details += f"\n║                                     ║"
        details += f"\n║ Attendance:                        ║"
        for year, percent in student['attendance'].items():
            details += f"\n║   {year}: {percent}% attendance{' '*(18-len(str(percent)))}║"
        
        details += f"\n║                                     ║"
        details += f"\n║ Activities: {', '.join(student['extracurricular']):<26} ║"
        details += "\n╚═════════════════════════════════════╝"
        
        self.display_message('success', details)

    def process_grade_query(self, query):
        """Process queries about student grades"""
        # Extract components from query
        student_id = None
        subject = None
        year = None
        
        # Try to find a student ID
        id_match = re.search(r'\d{3}', query)
        if id_match:
            student_id = int(id_match.group())
        else:
            # Try to find a student name
            for student in self.students:
                if student['name'].lower() in query:
                    student_id = student['id']
                    break
            
            if not student_id:
                # Try to extract possible name
                name_parts = [word.title() for word in query.split() if word.isalpha()]
                possible_name = ' '.join(name_parts[:2]) if len(name_parts) > 1 else name_parts[0] if name_parts else None
                
                if possible_name:
                    student_id = next((s['id'] for s in self.students if possible_name in s['name']), None)
        
        # Try to find a subject
        subjects = ['math', 'science', 'english']
        for subj in subjects:
            if subj in query:
                subject = subj.title()
                break
        
        # Try to find a year
        year_match = re.search(r'20[0-9]{2}', query)
        if year_match:
            year = int(year_match.group())
        
        if student_id:
            student = next((s for s in self.students if s['id'] == student_id), None)
            if student:
                if subject and year:
                    # Display specific grade (subject + year)
                    grade = student['grades'].get(subject, {}).get(year, None)
                    if grade:
                        self.display_message('success', 
                            f"Bot: {student['name']}'s {subject} grade in {year}: {grade}")
                    else:
                        self.display_message('alert', 
                            f"Bot: Grade record not found for {subject} in {year}")
                elif subject:
                    # Display all years for a subject
                    grades = student['grades'].get(subject, {})
                    if grades:
                        grade_str = ', '.join(f"{yr}={score}" for yr, score in grades.items())
                        self.display_message('success', 
                            f"Bot: {student['name']}'s {subject} grades: {grade_str}")
                    else:
                        self.display_message('alert', 
                            f"Bot: No grade records found for {subject}")
                elif year:
                    # Display all subjects for a year
                    grades = {subj: scores.get(year, None) 
                            for subj, scores in student['grades'].items()}
                    if any(grade is not None for grade in grades.values()):
                        grade_str = '\n'.join(f"   {subj}: {score}" 
                                            for subj, score in grades.items() 
                                            if score is not None)
                        self.display_message('success', 
                            f"Bot: {student['name']}'s grades in {year}:\n{grade_str}")
                    else:
                        self.display_message('alert', 
                            f"Bot: No grade records found for {year}")
                else:
                    # Display simplified grade overview
                    grade_overview = '\n'.join(
                        f"   {subj}: {min(scores.values())}-{max(scores.values())}" 
                        for subj, scores in student['grades'].items()
                    )
                    self.display_message('success', 
                        f"Bot: {student['name']}'s grade range:\n{grade_overview}")
            else:
                self.display_message('alert', "Bot: Student not found. Please check the ID or name.")
        else:
            self.current_context = 'grade_query'
            self.pending_action = 'get_grades'
            self.display_message('system', 
                "Bot: Could you please specify which student you're asking about?")

    def process_statistics_query(self, query):
        """Process requests for class statistics and averages"""
        # Extract class identifier if present
        class_id = None
        if '12' in query or '12th' in query.lower():
            class_id = '12'
        elif '11' in query or '11th' in query.lower():
            class_id = '11'
        
        # Extract subject if present
        subject = None
        subjects = ['math', 'science', 'english']
        for subj in subjects:
            if subj in query:
                subject = subj.title()
                break
        
        # Extract year if present
        year = None
        year_match = re.search(r'20[0-9]{2}', query)
        if year_match:
            year = int(year_match.group())
        
        if class_id:
            # Calculate statistics for the specified class
            class_students = [s for s in self.students if s['class'].startswith(class_id)]
            
            if not class_students:
                self.display_message('alert', f"Bot: No students found in class {class_id}")
                return
            
            if subject and year:
                # Subject average for specific year
                grades = [s['grades'].get(subject, {}).get(year, 0) 
                         for s in class_students]
                if any(grades):
                    avg = sum(grades) / len([g for g in grades if g > 0])
                    self.display_message('success', 
                        f"Bot: Class {class_id} {subject} average in {year}: {avg:.1f}")
                else:
                    self.display_message('alert', 
                        f"Bot: No grade records found for {subject} in {year}")
            elif subject:
                # Overall subject average
                grades = []
                for student in class_students:
                    grades.extend(student['grades'].get(subject, {}).values())
                if grades:
                    avg = sum(grades) / len(grades)
                    self.display_message('success', 
                        f"Bot: Class {class_id} overall {subject} average: {avg:.1f}")
                else:
                    self.display_message('alert', 
                        f"Bot: No grade records found for {subject}")
            elif year:
                # Overall class average for year
                grades = []
                for student in class_students:
                    grades.extend(v.get(year, 0) 
                                for v in student['grades'].values())
                if any(grades):
                    avg = sum(grades) / len([g for g in grades if g > 0])
                    self.display_message('success', 
                        f"Bot: Class {class_id} overall average in {year}: {avg:.1f}")
                else:
                    self.display_message('alert', 
                        f"Bot: No grade records found for {year}")
            else:
                # Overall class average
                grades = []
                for student in class_students:
                    for subject_grades in student['grades'].values():
                        grades.extend(subject_grades.values())
                avg = sum(grades) / len(grades)
                self.display_message('success', 
                    f"Bot: Class {class_id} overall average: {avg:.1f}")
        else:
            # No class specified - show school-wide statistics
            if subject and year:
                # School-wide subject average for year
                grades = []
                for student in self.students:
                    if subject in student['grades'] and year in student['grades'][subject]:
                        grades.append(student['grades'][subject][year])
                if grades:
                    avg = sum(grades) / len(grades)
                    self.display_message('success', 
                        f"Bot: School-wide {subject} average in {year}: {avg:.1f}")
                else:
                    self.display_message('alert', 
                        f"Bot: No grade records found for {subject} in {year}")
            elif subject:
                # School-wide subject average all years
                grades = []
                for student in self.students:
                    grades.extend(student['grades'].get(subject, {}).values())
                if grades:
                    avg = sum(grades) / len(grades)
                    self.display_message('success', 
                        f"Bot: School-wide {subject} average: {avg:.1f}")
                else:
                    self.display_message('alert', 
                        f"Bot: No grade records found for {subject}")
            elif year:
                # School-wide overall average for year
                grades = []
                for student in self.students:
                    for subject_grades in student['grades'].values():
                        if year in subject_grades:
                            grades.append(subject_grades[year])
                if grades:
                    avg = sum(grades) / len(grades)
                    self.display_message('success', 
                        f"Bot: School-wide average in {year}: {avg:.1f}")
                else:
                    self.display_message('alert', 
                        f"Bot: No grade records found for {year}")
            else:
                # School-wide overall average
                all_grades = []
                for student in self.students:
                    for subject_grades in student['grades'].values():
                        all_grades.extend(subject_grades.values())
                avg = sum(all_grades) / len(all_grades)
                self.display_message('success', 
                    f"Bot: School-wide overall average: {avg:.1f}")

    def process_list_query(self, query):
        """Process requests to list students or information"""
        if 'student' in query or 'all' in query:
            # List all students
            student_list = "\n".join(
                f"{s['id']}: {s['name']} ({s['class']})"
                for s in self.students
            )
            self.display_message('success', f"Bot: All students:\n{student_list}")
        elif 'activity' in query or 'club' in query:
            # List all extracurricular activities
            activities = set()
            for student in self.students:
                activities.update(student['extracurricular'])
            activity_list = "\n".join(sorted(activities))
            self.display_message('success', f"Bot: All extracurricular activities:\n{activity_list}")
        elif 'subject' in query or 'class' in query:
            # List available subjects
            subjects = set()
            for student in self.students:
                subjects.update(student['grades'].keys())
            subject_list = "\n".join(sorted(subjects))
            self.display_message('success', f"Bot: Available subjects:\n{subject_list}")
        else:
            self.display_message('system', 
                "Bot: You can ask to list 'students', 'activities', or 'subjects'")

    def process_attendance_query(self, query):
        """Process queries about student attendance"""
        # Extract student identifier if present
        student_id = None
        id_match = re.search(r'\d{3}', query)
        if id_match:
            student_id = int(id_match.group())
        else:
            # Try to find a student name
            for student in self.students:
                if student['name'].lower() in query:
                    student_id = student['id']
                    break
        
        # Extract year if present
        year = None
        year_match = re.search(r'20[0-9]{2}', query)
        if year_match:
            year = int(year_match.group())
        
        if student_id:
            student = next((s for s in self.students if s['id'] == student_id), None)
            if student:
                if year:
                    # Show attendance for specific year
                    attendance = student['attendance'].get(year, None)
                    if attendance:
                        self.display_message('success', 
                            f"Bot: {student['name']}'s attendance in {year}: {attendance}%")
                    else:
                        self.display_message('alert', 
                            f"Bot: No attendance record found for {year}")
                else:
                    # Show all attendance records
                    attendance_list = "\n".join(
                        f"   {yr}: {percent}%"
                        for yr, percent in student['attendance'].items()
                    )
                    self.display_message('success', 
                        f"Bot: {student['name']}'s attendance records:\n{attendance_list}")
            else:
                self.display_message('alert', "Bot: Student not found. Please check the ID or name.")
        else:
            # No student specified - show class/school attendance
            if '12' in query or '12th' in query.lower():
                class_id = '12'
                class_name = '12th grade'
            elif '11' in query or '11th' in query.lower():
                class_id = '11'
                class_name = '11th grade'
            else:
                class_id = None
                class_name = 'school'
            
            if year:
                # Calculate average attendance for class/school in year
                attendances = []
                for student in self.students:
                    if not class_id or student['class'].startswith(class_id):
                        if year in student['attendance']:
                            attendances.append(student['attendance'][year])
                
                if attendances:
                    avg = sum(attendances) / len(attendances)
                    self.display_message('success', 
                        f"Bot: {class_name} average attendance in {year}: {avg:.1f}%")
                else:
                    self.display_message('alert', 
                        f"Bot: No attendance records found for {year}")
            else:
                # Calculate overall average attendance
                attendances = []
                for student in self.students:
                    if not class_id or student['class'].startswith(class_id):
                        attendances.extend(student['attendance'].values())
                
                avg = sum(attendances) / len(attendances)
                self.display_message('success', 
                    f"Bot: {class_name} overall attendance average: {avg:.1f}%")

    def process_activity_query(self, query):
        """Process queries about extracurricular activities"""
        # Try to find activity name
        activities = set()
        for student in self.students:
            activities.update(student['extracurricular'])
        
        matched_activity = None
        for activity in activities:
            if activity.lower() in query.lower():
                matched_activity = activity
                break
        
        # Extract student identifier if present
        student_id = None
        id_match = re.search(r'\d{3}', query)
        if id_match:
            student_id = int(id_match.group())
        else:
            # Try to find a student name
            for student in self.students:
                if student['name'].lower() in query:
                    student_id = student['id']
                    break
        
        if matched_activity:
            # Show students in this activity
            participants = [
                s['name'] for s in self.students
                if matched_activity in s['extracurricular']
            ]
            
            if participants:
                participant_list = "\n".join(participants)
                self.display_message('success', 
                    f"Bot: Students in {matched_activity}:\n{participant_list}")
            else:
                self.display_message('alert', 
                    f"Bot: No students found in {matched_activity}")
        elif student_id:
            # Show student's activities
            student = next((s for s in self.students if s['id'] == student_id), None)
            if student:
                if student['extracurricular']:
                    activity_list = "\n".join(student['extracurricular'])
                    self.display_message('success', 
                        f"Bot: {student['name']} participates in:\n{activity_list}")
                else:
                    self.display_message('alert', 
                        f"Bot: {student['name']} is not in any activities")
            else:
                self.display_message('alert', 
                    "Bot: Student not found. Please check the ID or name.")
        else:
            # Show all activities
            activity_list = "\n".join(sorted(activities))
            self.display_message('success', 
                f"Bot: All extracurricular activities:\n{activity_list}")

    def handle_context(self, query):
        """Handle follow-up responses in conversation context"""
        if self.current_context == 'student_query':
            if self.pending_action == 'get_details':
                self.process_student_query(query)
        
        elif self.current_context == 'grade_query':
            if self.pending_action == 'get_grades':
                self.process_grade_query(query)
        
        # Reset context 
        self.current_context = None
        self.pending_action = None

    def default_response(self, query):
        """Provide a default response for unrecognized queries"""
        # Try to find similar student names
        name_parts = [word.title() for word in query.split() if word.isalpha()]
        if len(name_parts) >= 2:
            possible_name = ' '.join(name_parts[:2])
            all_names = [s['name'] for s in self.students]
            matches = get_close_matches(possible_name, all_names, n=1, cutoff=0.6)
            
            if matches:
                self.display_message('system', 
                    f"Bot: Did you mean '{matches[0]}'? Try asking about them specifically.")
                return
        
        # Default unknown response
        responses = [
            "I'm not sure I understand. Could you rephrase that?",
            "I don't have information about that. Try asking about students or grades.",
            "Please ask about student records or school information."
        ]
        self.display_message('alert', f"Bot: {random.choice(responses)}\n(Type 'help' for options)")

if __name__ == "__main__":
    root = tk.Tk()
    chatbot = StudentChatbot(root)
    root.mainloop()
