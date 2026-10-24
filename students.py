import database
from utils import (
    confirm,
    find_student_by_id,
    print_error,
    print_info,
    print_students,
    print_success,
    format_student,
    read_int,
    read_non_empty,
)


def show_all_students() -> None:
    if not database.students:
        print_info("O‘quvchilar ro‘yxati bo‘sh.")
        return
    print_students(database.students)


def add_student() -> None:
    name = read_non_empty("Ism: ")
    age = read_int("Yosh: ", min_value=1)
    group = read_non_empty("Guruh: ")

    student = {
        "id": database.get_next_id(),
        "name": name,
        "age": age,
        "group": group,
        "grades": {},
    }
    database.students.append(student)
    database.save_data()
    print_success(f"O‘quvchi qo‘shildi. ID: {student['id']}")


def edit_student() -> None:
    student_id = read_int("Tahrirlanadigan o‘quvchi ID si: ")
    student = find_student_by_id(student_id)
    if student is None:
        print_error("Bunday ID li o‘quvchi topilmadi.")
        return

    print(format_student(student))
    print_info("O‘zgartirmaslik uchun bo‘sh qoldirib Enter bosing.")

    new_name = input(f"Yangi ism [{student['name']}]: ").strip()
    if new_name:
        student["name"] = new_name

    while True:
        new_age = input(f"Yangi yosh [{student['age']}]: ").strip()
        if not new_age:
            break
        if new_age.isdigit() and int(new_age) > 0:
            student["age"] = int(new_age)
            break
        print_error("Yosh musbat butun son bo‘lishi kerak.")

    new_group = input(f"Yangi guruh [{student['group']}]: ").strip()
    if new_group:
        student["group"] = new_group

    database.save_data()
    print_success("Ma’lumotlar yangilandi.")


def delete_student() -> None:
    student_id = read_int("O‘chiriladigan o‘quvchi ID si: ")
    student = find_student_by_id(student_id)
    if student is None:
        print_error("Bunday ID li o‘quvchi topilmadi.")
        return

    print(format_student(student))
    if not confirm("Rostdan o‘chirmoqchimisiz?"):
        print_info("O‘chirish bekor qilindi.")
        return

    database.students.remove(student)
    database.save_data()
    print_success("O‘quvchi o‘chirildi.")


def search_by_id() -> None:
    student_id = read_int("Qidirilayotgan ID: ")
    student = find_student_by_id(student_id)
    if student is None:
        print_error("Bunday ID li o‘quvchi topilmadi.")
        return
    print_students([student])


def search_by_name() -> None:
    query = read_non_empty("Ism (to‘liq yoki qisman): ").lower()
    found = [s for s in database.students if query in s["name"].lower()]
    if not found:
        print_error("Mos o‘quvchi topilmadi.")
        return
    print_students(found)
