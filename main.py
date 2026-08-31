"""
main.py

Command-line interface and single entry point for the Student Record
Management System.

Run `python main.py --help` (or `python main.py <command> --help`) to see
all available options.

Examples
--------
Display every student stored in a CSV file:
    python main.py --file data/students.csv --format csv display

Search for a student by ID inside a JSON file:
    python main.py --file data/students.json --format json search --id 102

Add a new student to a text file and save the result to a new file:
    python main.py --file data/students.txt --format txt add \\
        --id 106 --name "Sneha Rao" --dept "Physics" --sem 1 \\
        --marks 80 75 90 --out data/students_updated.txt

Update a student's marks in a CSV file:
    python main.py --file data/students.csv --format csv update-marks \\
        --id 101 --subject1 85 --out data/students_updated.csv

Convert a JSON file of students into a CSV file:
    python main.py --file data/students.json --format json convert \\
        --out data/students_from_json.csv --out-format csv
"""

import argparse
import os
import sys

import file_handler
from student import Student
from manager import StudentManager


def infer_format(filepath):
    """Guess a file format ('txt'/'csv'/'json') from its extension."""
    ext = os.path.splitext(filepath)[1].lower().lstrip(".")
    if ext in ("txt", "csv", "json"):
        return ext
    return None


def build_parser():
    parser = argparse.ArgumentParser(
        description="Student Record Management System (TXT / CSV / JSON)."
    )
    parser.add_argument(
        "--file", required=True,
        help="Path to the input file containing student records."
    )
    parser.add_argument(
        "--format", choices=["txt", "csv", "json"], default=None,
        help="Format of the input file. If omitted, it is guessed from "
             "the file extension of --file."
    )

    subparsers = parser.add_subparsers(dest="command", required=True,
                                        help="Action to perform.")

    # display -----------------------------------------------------------
    subparsers.add_parser("display", help="Display all student records.")

    # peek --------------------------------------------------------------
    peek_parser = subparsers.add_parser(
        "peek", help="Preview the first few raw lines of a TXT file "
                     "(demonstrates readline())."
    )
    peek_parser.add_argument("--lines", type=int, default=3,
                              help="Number of lines to preview (default: 3).")

    # search --------------------------------------------------------------
    search_parser = subparsers.add_parser("search", help="Search for a student by ID.")
    search_parser.add_argument("--id", required=True, type=int, help="Student ID to search for.")

    # add -------------------------------------------------------------------
    add_parser = subparsers.add_parser("add", help="Add a new student record.")
    add_parser.add_argument("--id", required=True, type=int, help="New student's ID.")
    add_parser.add_argument("--name", required=True, help="New student's name.")
    add_parser.add_argument("--dept", required=True, help="New student's department.")
    add_parser.add_argument("--sem", required=True, type=int, help="New student's semester.")
    add_parser.add_argument("--marks", required=True, type=int, nargs=3,
                             metavar=("SUBJECT1", "SUBJECT2", "SUBJECT3"),
                             help="Marks in three subjects, e.g. --marks 80 75 90")
    add_parser.add_argument("--out", default=None,
                             help="Output file to save the updated records to "
                                  "(defaults to overwriting --file).")
    add_parser.add_argument("--out-format", choices=["txt", "csv", "json"], default=None,
                             help="Format of the output file (defaults to --format).")

    # remove ------------------------------------------------------------
    remove_parser = subparsers.add_parser("remove", help="Remove a student record by ID.")
    remove_parser.add_argument("--id", required=True, type=int, help="Student ID to remove.")
    remove_parser.add_argument("--out", default=None,
                                help="Output file to save the updated records to "
                                     "(defaults to overwriting --file).")
    remove_parser.add_argument("--out-format", choices=["txt", "csv", "json"], default=None,
                                help="Format of the output file (defaults to --format).")

    # update-marks --------------------------------------------------------
    update_parser = subparsers.add_parser("update-marks", help="Update a student's marks.")
    update_parser.add_argument("--id", required=True, type=int, help="Student ID to update.")
    update_parser.add_argument("--subject1", type=int, default=None, help="New mark for subject 1.")
    update_parser.add_argument("--subject2", type=int, default=None, help="New mark for subject 2.")
    update_parser.add_argument("--subject3", type=int, default=None, help="New mark for subject 3.")
    update_parser.add_argument("--out", default=None,
                                help="Output file to save the updated records to "
                                     "(defaults to overwriting --file).")
    update_parser.add_argument("--out-format", choices=["txt", "csv", "json"], default=None,
                                help="Format of the output file (defaults to --format).")

    # convert -----------------------------------------------------------
    convert_parser = subparsers.add_parser(
        "convert", help="Load records in one format and save them in another format."
    )
    convert_parser.add_argument("--out", required=True, help="Output file path.")
    convert_parser.add_argument("--out-format", required=True, choices=["txt", "csv", "json"],
                                 help="Format to save the output file in.")

    return parser


def resolve_format(filepath, fmt, label="--file"):
    """Return an explicit format, falling back to guessing from the extension."""
    if fmt:
        return fmt
    guessed = infer_format(filepath)
    if guessed is None:
        sys.exit(f"Error: could not determine file format for {label}='{filepath}'. "
                  f"Please pass an explicit --format/--out-format.")
    return guessed


def main():
    parser = build_parser()
    args = parser.parse_args()

    input_format = resolve_format(args.file, args.format, "--file")

    manager = StudentManager()

    # 'peek' only needs the raw file, not parsed Student objects.
    if args.command == "peek":
        file_handler.preview_txt(args.file, num_lines=args.lines)
        return

    manager.load_from_file(args.file, input_format)

    if args.command == "display":
        manager.display_all_students()

    elif args.command == "search":
        student = manager.search_student(args.id)
        if student is None:
            print(f"No student found with ID {args.id}.")
        else:
            student.display_student()

    elif args.command == "add":
        new_student = Student(args.id, args.name, args.dept, args.sem, args.marks)
        if manager.add_student(new_student):
            out_path = args.out or args.file
            out_format = resolve_format(out_path, args.out_format or args.format, "--out")
            manager.save_to_file(out_path, out_format)

    elif args.command == "remove":
        if manager.remove_student(args.id):
            out_path = args.out or args.file
            out_format = resolve_format(out_path, args.out_format or args.format, "--out")
            manager.save_to_file(out_path, out_format)

    elif args.command == "update-marks":
        student = manager.search_student(args.id)
        if student is None:
            print(f"No student found with ID {args.id}.")
        else:
            student.update_marks(args.subject1, args.subject2, args.subject3)
            print(f"Updated marks for student ID {args.id}:")
            student.display_student()
            out_path = args.out or args.file
            out_format = resolve_format(out_path, args.out_format or args.format, "--out")
            manager.save_to_file(out_path, out_format)

    elif args.command == "convert":
        manager.save_to_file(args.out, args.out_format)


if __name__ == "__main__":
    main()
