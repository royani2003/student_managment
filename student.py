"""
student.py

Defines the Student class, which represents a single student record.

This module demonstrates basic Object-Oriented Programming concepts:
- A class with a constructor (__init__)
- Instance attributes
- Instance methods that operate on those attributes
- Class methods used as alternative constructors (building a Student
  from a text line, a CSV row, or a JSON-style dictionary)
"""


class Student:
    """Represents a single student and their marks in three subjects."""

    # A subject is considered "passed" if the mark is at least this value.
    PASS_MARK = 40

    def __init__(self, student_id, name, department, semester, marks):
        """
        Create a new Student.

        Parameters
        ----------
        student_id : int
            Unique identifier for the student.
        name : str
            Student's full name.
        department : str
            Department the student belongs to.
        semester : int
            Current semester of the student.
        marks : list[int] or tuple[int]
            Marks in exactly three subjects, e.g. [78, 82, 69].
        """
        self.student_id = int(student_id)
        self.name = str(name).strip()
        self.department = str(department).strip()
        self.semester = int(semester)
        # Store marks as a list of three integers.
        self.marks = [int(m) for m in marks]

    # Core behaviour
    
    def calculate_total(self):
        """Return the total marks obtained across all three subjects."""
        return sum(self.marks)

    def calculate_average(self):
        """Return the average marks (as a float) across all three subjects."""
        return self.calculate_total() / len(self.marks)

    def get_result(self):
        """
        Return 'Pass' if every subject mark is >= PASS_MARK,
        otherwise return 'Fail'.
        """
        if all(mark >= self.PASS_MARK for mark in self.marks):
            return "Pass"
        return "Fail"

    def update_marks(self, subject1=None, subject2=None, subject3=None):
        """
        Update one or more subject marks for this student.

        Only the subjects that are explicitly passed in are changed;
        the rest keep their existing values. This method mutates the
        Student object in place.
        """
        if subject1 is not None:
            self.marks[0] = int(subject1)
        if subject2 is not None:
            self.marks[1] = int(subject2)
        if subject3 is not None:
            self.marks[2] = int(subject3)

    def display_student(self):
        """Print a human-readable summary of the student's record."""
        print("-" * 45)
        print(f"Student ID   : {self.student_id}")
        print(f"Name         : {self.name}")
        print(f"Department   : {self.department}")
        print(f"Semester     : {self.semester}")
        print(f"Marks        : Subject1={self.marks[0]}, "
              f"Subject2={self.marks[1]}, Subject3={self.marks[2]}")
        print(f"Total Marks  : {self.calculate_total()}")
        print(f"Average Marks: {self.calculate_average():.2f}")
        print(f"Result       : {self.get_result()}")
        print("-" * 45)

    # Conversion helpers - used by file_handler.py when saving records
    
    def to_txt_line(self):
        """Return this student as a single comma-separated text line."""
        return (f"{self.student_id}, {self.name}, {self.department}, "
                f"{self.semester}, {self.marks[0]}, {self.marks[1]}, {self.marks[2]}")

    def to_csv_row(self):
        """Return this student as a dictionary suitable for csv.DictWriter."""
        return {
            "Student_ID": self.student_id,
            "Name": self.name,
            "Department": self.department,
            "Semester": self.semester,
            "Subject1": self.marks[0],
            "Subject2": self.marks[1],
            "Subject3": self.marks[2],
        }

    def to_dict(self):
        """Return this student as a dictionary suitable for JSON output."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "department": self.department,
            "semester": self.semester,
            "marks": {
                "subject1": self.marks[0],
                "subject2": self.marks[1],
                "subject3": self.marks[2],
            },
        }

    # Alternative constructors - used by file_handler.py when loading
   
    @classmethod
    def from_txt_line(cls, line):
        """Build a Student from a comma-separated text line."""
        parts = [p.strip() for p in line.strip().split(",")]
        student_id, name, department, semester, s1, s2, s3 = parts
        return cls(student_id, name, department, semester, [s1, s2, s3])

    @classmethod
    def from_csv_row(cls, row):
        """Build a Student from a dictionary produced by csv.DictReader."""
        return cls(
            row["Student_ID"],
            row["Name"],
            row["Department"],
            row["Semester"],
            [row["Subject1"], row["Subject2"], row["Subject3"]],
        )

    @classmethod
    def from_dict(cls, data):
        """Build a Student from a dictionary produced by json.load."""
        marks = data["marks"]
        return cls(
            data["student_id"],
            data["name"],
            data["department"],
            data["semester"],
            [marks["subject1"], marks["subject2"], marks["subject3"]],
        )

    def __str__(self):
        return (f"Student({self.student_id}, {self.name}, {self.department}, "
                f"Sem {self.semester}, Marks={self.marks})")

    def __repr__(self):
        return self.__str__()
