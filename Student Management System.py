import csv
import os

DATABASE_FILE = "students.csv"
FIELDS = ["ID", "Name", "Grade"]


class Student:
    def __init__(self, student_id, name, grade):
        self.student_id = student_id
        self.name = name
        self.grade = grade

    def to_dict(self):
        return {
            "ID": self.student_id,
            "Name": self.name,
            "Grade": self.grade
        }


class StudentManager:
    def __init__(self, filename):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDS)
                writer.writeheader()

    def _read_all_students(self):
        with open(self.filename, "r", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def _write_all_students(self, students):
        with open(self.filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(students)

    def _id_exists(self, student_id):
        students = self._read_all_students()
        return any(s["ID"] == student_id for s in students)

    def add_student(self):
        print("\n--- Add Student ---")
        student_id = input("Enter ID: ").strip()

        if self._id_exists(student_id):
            print("❌ Error: Student ID already exists.")
            return

        name = input("Enter Name: ").strip()
        grade = input("Enter Grade: ").strip()

        student = Student(student_id, name, grade)

        with open(self.filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writerow(student.to_dict())

        print("✅ Student added successfully!")

    def list_students(self):
        print("\n--- Student List ---")
        students = self._read_all_students()

        if not students:
            print("⚠️ No students found.")
            return

        print(f"{'ID':<10}{'Name':<20}{'Grade':<10}")
        print("-" * 40)
        for s in students:
            print(f"{s['ID']:<10}{s['Name']:<20}{s['Grade']:<10}")

    def find_student(self):
        student_id = input("Enter ID to search: ").strip()
        students = self._read_all_students()

        for s in students:
            if s["ID"] == student_id:
                print("\n✅ Student Found")
                print(f"ID    : {s['ID']}")
                print(f"Name  : {s['Name']}")
                print(f"Grade : {s['Grade']}")
                return

        print("❌ Student not found.")

    def update_student(self):
        student_id = input("Enter ID to update: ").strip()
        students = self._read_all_students()
        updated = False

        for s in students:
            if s["ID"] == student_id:
                print("Leave blank to keep existing value")
                name = input(f"New Name ({s['Name']}): ").strip()
                grade = input(f"New Grade ({s['Grade']}): ").strip()

                if name:
                    s["Name"] = name
                if grade:
                    s["Grade"] = grade

                updated = True
                break

        if updated:
            self._write_all_students(students)
            print("✅ Student updated successfully!")
        else:
            print("❌ Student not found.")

    def delete_student(self):
        student_id = input("Enter ID to delete: ").strip()
        students = self._read_all_students()
        new_students = [s for s in students if s["ID"] != student_id]

        if len(new_students) == len(students):
            print("❌ Student not found.")
        else:
            self._write_all_students(new_students)
            print("✅ Student deleted successfully!")


def show_menu():
    print("\n==============================")
    print("   Student Management System  ")
    print("==============================")
    print("1. Add Student")
    print("2. List Students")
    print("3. Find Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")
    print("==============================")


if __name__ == "__main__":
    manager = StudentManager(DATABASE_FILE)

    while True:
        show_menu()
        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            manager.add_student()
        elif choice == "2":
            manager.list_students()
        elif choice == "3":
            manager.find_student()
        elif choice == "4":
            manager.update_student()
        elif choice == "5":
            manager.delete_student()
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("⚠️ Invalid choice. Try again.")
