"""
manager.py

Defines the StudentManager class, which is responsible for managing a
*collection* of Student objects (as opposed to student.py, which defines
what a single Student looks like).

This separation demonstrates the difference between:
- an object representing one student (Student), and
- a class that manages many such objects (StudentManager).
"""

import file_handler


class StudentManager:
    """Manages a collection of Student objects and their persistence to disk."""

    def __init__(self):
        self.students = []  # list of Student objects currently in memory

    # In-memory record management
    
    def add_student(self, student):
        """
        Add a new Student object to the manager.

        If a student with the same student_id already exists, it is
        rejected to avoid duplicate IDs.
        """
        if self.search_student(student.student_id) is not None:
            print(f"A student with ID {student.student_id} already exists. "
                  f"Student not added.")
            return False
        self.students.append(student)
        return True

    def remove_student(self, student_id):
        """Remove the student with the given student_id, if present."""
        student = self.search_student(student_id)
        if student is None:
            print(f"No student found with ID {student_id}.")
            return False
        self.students.remove(student)
        return True

    def search_student(self, student_id):
        """Return the Student object with the given ID, or None if not found."""
        student_id = int(student_id)
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def display_all_students(self):
        """Print every student currently managed, with their computed results."""
        if not self.students:
            print("No student records to display.")
            return
        print(f"\nTotal students: {len(self.students)}")
        for student in self.students:
            student.display_student()

    # File persistence - delegated to file_handler.py
    
    def load_from_file(self, filepath, file_format):
        """
        Load student records from a file and replace the current in-memory
        list of students with the ones read from disk.
        """
        self.students = file_handler.read_students(filepath, file_format)
        print(f"Loaded {len(self.students)} student record(s) from "
              f"'{filepath}' ({file_format}).")

    def save_to_file(self, filepath, file_format):
        """Save the current in-memory list of students to a file."""
        file_handler.write_students(filepath, self.students, file_format)
        print(f"Saved {len(self.students)} student record(s) to "
              f"'{filepath}' ({file_format}).")
