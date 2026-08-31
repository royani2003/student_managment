# Student Record Management System

A command-line Student Record Management System written in Python, built for
**Assignment 1 — AI/ML Laboratory (M.Sc. 1st Semester)**. It stores and
retrieves student records using three different file formats — plain text
(`.txt`), CSV (`.csv`), and JSON (`.json`) — and is built entirely around
Object-Oriented Programming principles.

## B. Objective

The purpose of this assignment is to build a simple but complete Python
program that:

- Represents real-world entities (students) as objects using a `Student`
  class.
- Manages a collection of those objects using a separate `StudentManager`
  class.
- Reads and writes the same data in three different file formats (TXT, CSV,
  JSON), using only Python's built-in `csv` and `json` modules (no Pandas or
  NumPy).
- Is driven entirely from the command line using `argparse`, so that no
  input needs to be hard-coded.

Concepts implemented: classes, constructors, instance attributes, instance
methods, class methods (alternative constructors), file I/O in three
formats, and a command-line interface with sub-commands.

## C. Features

- Load student records from a TXT, CSV, or JSON file.
- Display all student records, including each student's total marks,
  average marks, and pass/fail result.
- Preview the raw first few lines of a text file (`peek`), to demonstrate
  `readline()`.
- Search for a student by Student ID.
- Add a new student record and save the updated list to a file (duplicate
  IDs are rejected).
- Remove a student record by ID and save the updated list.
- Update a student's marks (one, two, or all three subjects) and save the
  updated list.
- Convert a set of records from one file format to another (e.g. JSON →
  CSV).
- Automatic pass/fail determination and total/average calculation, done by
  the `Student` class itself.

## D. Project Structure

```
student-record-system/
├── main.py            → Command-line interface and program execution (single access point)
├── student.py         → Student class: attributes + per-student calculations
├── manager.py         → StudentManager class: manages a collection of Student objects
├── file_handler.py    → Reading/writing TXT, CSV and JSON files
├── data/
│   ├── students.txt   → Sample data in text format
│   ├── students.csv   → Sample data in CSV format
│   └── students.json  → Sample data in JSON format
├── .gitignore
└── README.md
```

| File | Purpose |
|---|---|
| `main.py` | Parses command-line arguments (`argparse`) and dispatches to the right action (display, search, add, remove, update-marks, convert, peek). This is the only file you run directly. |
| `student.py` | Defines the `Student` class — one object represents one student. Contains `calculate_total()`, `calculate_average()`, `get_result()`, `update_marks()`, `display_student()`, and conversion helpers to/from TXT/CSV/JSON. |
| `manager.py` | Defines the `StudentManager` class — manages a *list* of `Student` objects: `add_student()`, `remove_student()`, `search_student()`, `display_all_students()`, `load_from_file()`, `save_to_file()`. |
| `file_handler.py` | All raw file I/O lives here: `read_txt`/`write_txt`, `read_csv`/`write_csv` (using the `csv` module), `read_json`/`write_json` (using the `json` module), plus a small `preview_txt()` helper. |

## E. Requirements

- Python 3.8 or later.
- No external packages are required — only Python's standard library
  (`argparse`, `csv`, `json`, `os`, `sys`). Pandas/NumPy are **not** used,
  as required by the assignment guidelines.

## F. How to Run

All commands are run from inside the `student-record-system/` folder.

General form:

```
python main.py --file <path> [--format {txt,csv,json}] <command> [options]
```

`--format` can usually be omitted — it is guessed from the file extension —
but can be given explicitly if needed.

**Display all students**

```
python main.py --file data/students.csv --format csv display
python main.py --file data/students.json --format json display
python main.py --file data/students.txt --format txt display
```

**Search for a student by ID**

```
python main.py --file data/students.csv --format csv search --id 103
```

**Add a new student** (saved to `--out`; if `--out` is omitted, the input
file is updated in place)

```
python main.py --file data/students.csv --format csv add \
    --id 107 --name "Vikram Singh" --dept "Chemistry" --sem 1 \
    --marks 60 55 70 --out data/students_updated.csv
```

**Update a student's marks** (any subset of `--subject1/2/3`)

```
python main.py --file data/students.json --format json update-marks \
    --id 101 --subject1 85 --out data/students_updated.json
```

**Remove a student**

```
python main.py --file data/students.txt --format txt remove \
    --id 105 --out data/students_updated.txt
```

**Convert between formats**

```
python main.py --file data/students.json --format json convert \
    --out data/students_from_json.csv --out-format csv
```

**Preview raw lines of a text file** (demonstrates `readline()`)

```
python main.py --file data/students.txt --format txt peek --lines 2
```

Run `python main.py --help` or `python main.py <command> --help` for the
full list of options for any command.

## G. Input and Output

- **Inputs accepted:** a path to a student-records file (`--file`), its
  format (`--format`, optional), a sub-command (e.g. `add`, `search`), and
  any fields that command needs (e.g. `--id`, `--name`, `--marks`).
- **Required files:** at least one of `data/students.txt`,
  `data/students.csv`, or `data/students.json` must exist and be readable;
  sample versions of all three are included in `data/`.
- **What the program produces:** for read-only commands (`display`,
  `search`, `peek`) it only prints to the console. For commands that modify
  data (`add`, `remove`, `update-marks`, `convert`) it writes an updated
  file to the path given by `--out` (or overwrites `--file` if `--out` is
  omitted).
- **Where output files are stored:** wherever `--out` points to — by
  convention, alongside the input files inside `data/`.

### Example output

```
$ python main.py --file data/students.csv --format csv search --id 103
Loaded 6 student record(s) from 'data/students.csv' (csv).
---------------------------------------------
Student ID   : 103
Name         : Amit
Department   : Mathematics
Semester     : 1
Marks        : Subject1=65, Subject2=71, Subject3=68
Total Marks  : 204
Average Marks: 68.00
Result       : Pass
---------------------------------------------
```

```
$ python main.py --file data/students.csv --format csv add \
      --id 107 --name "Vikram Singh" --dept "Chemistry" --sem 1 \
      --marks 60 55 70 --out data/students_updated.csv
Loaded 6 student record(s) from 'data/students.csv' (csv).
Saved 7 student record(s) to 'data/students_updated.csv' (csv).
```

## H. OOP Concepts Used

- **Classes:** `Student` (student.py) and `StudentManager` (manager.py).
- **Objects:** each row of student data becomes one `Student` object;
  `StudentManager` holds a list of these objects.
- **Constructors:** `Student.__init__()` builds a student from its core
  fields; three **class methods** (`from_txt_line`, `from_csv_row`,
  `from_dict`) act as alternative constructors that build a `Student`
  directly from a text line, a CSV row, or a JSON record.
- **Attributes:** `student_id`, `name`, `department`, `semester`, `marks`
  (instance attributes on `Student`); `students` (instance attribute on
  `StudentManager`); `PASS_MARK` (a class attribute shared by all
  `Student` instances).
- **Instance methods:** `calculate_total()`, `calculate_average()`,
  `get_result()`, `update_marks()`, `display_student()` on `Student`;
  `add_student()`, `remove_student()`, `search_student()`,
  `display_all_students()`, `load_from_file()`, `save_to_file()` on
  `StudentManager`.
- **Encapsulation / separation of concerns:** `Student` only knows about a
  single student's data and behaviour; `StudentManager` only knows how to
  manage a collection of `Student` objects; `file_handler.py` only knows
  how to read/write files. `main.py` ties them together via the CLI.

## I. File Handling Concepts Used

- **TXT:** `open()`, `readlines()` (bulk read in `read_txt`), `readline()`
  (line-by-line preview in `preview_txt`), `write()` inside a `with
  open(path, mode) as f:` block, using modes `"r"` and `"w"`/`"a"`.
- **CSV:** Python's `csv` module — `csv.DictReader` to read rows into
  dictionaries keyed by the header (`Student_ID, Name, Department,
  Semester, Subject1, Subject2, Subject3`), and `csv.DictWriter` with
  `writeheader()` + `writerow()` to write them back out. Pandas is **not**
  used for this part, as required.
- **JSON:** `json.load()` to parse a JSON array of student records into
  Python dictionaries/lists, and `json.dump()` (with `indent=4`) to write
  an updated list of records back to a JSON file.
- All file access uses `with open(...) as f:` so files are always closed
  properly, even if an error occurs.

## J. Sample Output

**Display (JSON input):**

```
$ python main.py --file data/students.json --format json display
Loaded 6 student record(s) from 'data/students.json' (json).

Total students: 6
---------------------------------------------
Student ID   : 101
Name         : Rahul
Department   : Computer Science
Semester     : 1
Marks        : Subject1=78, Subject2=82, Subject3=69
Total Marks  : 229
Average Marks: 76.33
Result       : Pass
---------------------------------------------
...
---------------------------------------------
Student ID   : 105
Name         : Karan
Department   : Mathematics
Semester     : 1
Marks        : Subject1=35, Subject2=42, Subject3=38
Total Marks  : 115
Average Marks: 38.33
Result       : Fail
---------------------------------------------
```

**Update marks (JSON input):**

```
$ python main.py --file data/students.json --format json update-marks \
      --id 101 --subject1 85 --out data/students_updated.json
Loaded 6 student record(s) from 'data/students.json' (json).
Updated marks for student ID 101:
---------------------------------------------
Student ID   : 101
Name         : Rahul
Department   : Computer Science
Semester     : 1
Marks        : Subject1=85, Subject2=82, Subject3=69
Total Marks  : 236
Average Marks: 78.67
Result       : Pass
---------------------------------------------
Saved 6 student record(s) to 'data/students_updated.json' (json).
```

**Peek (TXT input):**

```
$ python main.py --file data/students.txt --format txt peek --lines 2
Previewing first 2 line(s) of 'data/students.txt':
   101, Rahul, Computer Science, 1, 78, 82, 69
   102, Priya, Computer Science, 1, 91, 87, 94
```

All of the commands above (`display`, `search`, `add`, `remove`,
`update-marks`, `convert`, `peek`) were run against the six sample records
in `data/` and produced the outputs shown, confirming the program works
end-to-end across all three file formats.

## K. Learning Outcome / Conclusion

This assignment helped in understanding how to model a real-world entity
(a student) as a Python object, and the difference between an object that
represents *one* entity (`Student`) and a class that manages *many* such
objects (`StudentManager`). It also gave hands-on practice with Python's
three most common ways of persisting structured data — plain text, CSV,
and JSON — and with `argparse` for building a proper command-line
interface instead of hard-coding inputs.

One of the trickier parts was designing `Student` so that the *same*
object could be converted cleanly to and from all three file formats
without duplicating logic in `main.py` — this was solved by giving
`Student` its own `to_txt_line()/to_csv_row()/to_dict()` methods and
matching `from_txt_line()/from_csv_row()/from_dict()` class methods, so
`file_handler.py` never needs to know the internal details of the
`Student` class. Handling optional/partial updates in `update_marks()`
(where a user may want to change only one subject) also required some
care with default argument values.
