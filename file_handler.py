"""
file_handler.py

Handles all reading and writing of student records to/from disk, in three
different file formats: plain text (.txt), CSV (.csv) and JSON (.json).

This module intentionally keeps all file I/O in one place, separate from
the Student class (student.py) and the StudentManager class (manager.py),
so that each file has a clear, single responsibility.
"""

import csv
import json

from student import Student

CSV_FIELDNAMES = ["Student_ID", "Name", "Department", "Semester",
                   "Subject1", "Subject2", "Subject3"]


# TXT file handling

def read_txt(filepath):
    """
    Read student records from a plain text file.

    Each line is expected to look like:
        101, Rahul, Computer Science, 1, 78, 82, 69

    Returns a list of Student objects.
    """
    students = []
    with open(filepath, "r") as f:
        # readlines() is used here to demonstrate reading the whole
        # file into a list of lines at once.
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue  # skip blank lines
        students.append(Student.from_txt_line(line))
    return students


def write_txt(filepath, students, mode="w"):
    """
    Write a list of Student objects to a plain text file.

    mode='w' overwrites the file, mode='a' appends to an existing file.
    """
    with open(filepath, mode) as f:
        for student in students:
            f.write(student.to_txt_line() + "\n")


def preview_txt(filepath, num_lines=3):
    """
    Print the first `num_lines` lines of a text file using readline().

    This is a small helper used to demonstrate open()/readline() usage
    separately from read()/readlines().
    """
    with open(filepath, "r") as f:
        print(f"Previewing first {num_lines} line(s) of '{filepath}':")
        for _ in range(num_lines):
            line = f.readline()
            if not line:
                break
            print("   " + line.rstrip())


# CSV file handling  (Do NOT use Pandas here - only the csv module)

def read_csv(filepath):
    """
    Read student records from a CSV file (with a header row).

    Returns a list of Student objects.
    """
    students = []
    with open(filepath, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append(Student.from_csv_row(row))
    return students


def write_csv(filepath, students):
    """
    Write a list of Student objects to a CSV file, including the header row.
    """
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        for student in students:
            writer.writerow(student.to_csv_row())


# JSON file handling

def read_json(filepath):
    """
    Read student records from a JSON file.

    The JSON file is expected to contain a list of student objects, e.g.:
        [
            {"student_id": 101, "name": "Rahul", ... "marks": {...}},
            ...
        ]

    Returns a list of Student objects.
    """
    with open(filepath, "r") as f:
        data = json.load(f)
    return [Student.from_dict(record) for record in data]


def write_json(filepath, students):
    """
    Write a list of Student objects to a JSON file.
    """
    data = [student.to_dict() for student in students]
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


# Format dispatch helpers - used by StudentManager

READERS = {
    "txt": read_txt,
    "csv": read_csv,
    "json": read_json,
}

WRITERS = {
    "txt": write_txt,
    "csv": write_csv,
    "json": write_json,
}


def read_students(filepath, file_format):
    """Dispatch to the correct reader based on file_format ('txt'/'csv'/'json')."""
    if file_format not in READERS:
        raise ValueError(f"Unsupported file format: {file_format}")
    return READERS[file_format](filepath)


def write_students(filepath, students, file_format):
    """Dispatch to the correct writer based on file_format ('txt'/'csv'/'json')."""
    if file_format not in WRITERS:
        raise ValueError(f"Unsupported file format: {file_format}")
    WRITERS[file_format](filepath, students)
