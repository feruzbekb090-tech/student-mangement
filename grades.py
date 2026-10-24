import database
from utils import (
    find_student_by_id,
    print_error,
    print_info,
    print_success,
    print_title,
    read_int,
    read_non_empty,
)


def find_subject_key(student: dict, subject: str):
    """Katta-kichik harfga qaramasdan mavjud fan nomini topadi."""
    for key in student["grades"]:
        if key.lower() == subject.lower():
            return key
    return None


def add_grade() -> None:
    student_id = read_int("O‘quvchi ID si: ")
    student = find_student_by_id(student_id)
    if student is None:
        print_error("Bunday ID li o‘quvchi topilmadi.")
        return

    subject = read_non_empty("Fan nomi: ")
    grade = read_int("Baho (1-5): ", min_value=1, max_value=5)

    existing_key = find_subject_key(student, subject)
    if existing_key is None:
        student["grades"][subject] = [grade]  # yangi fan
    else:
        student["grades"][existing_key].append(grade)  # mavjud fan

    database.save_data()
    print_success("Baho qo‘shildi.")


def show_grades() -> None:
    student_id = read_int("O‘quvchi ID si: ")
    student = find_student_by_id(student_id)
    if student is None:
        print_error("Bunday ID li o‘quvchi topilmadi.")
        return

    if not student["grades"]:
        print_info(f"{student['name']} da hali baholar yo‘q.")
        return

    print_title(f"{student['name']} baholari")
    for subject, grades_list in student["grades"].items():
        print(f"{subject}: {', '.join(str(g) for g in grades_list)}")
