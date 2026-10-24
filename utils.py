from colored import cprint

import database

# (belgi, matn, rang) — belgi doira ichidagi raqam
menu_items = [
    ("①", "Barcha o‘quvchilarni ko‘rish", "cyan"),
    ("②", "O‘quvchi qo‘shish", "cyan"),
    ("③", "O‘quvchi ma’lumotlarini tahrirlash", "cyan"),
    ("④", "O‘quvchini o‘chirish", "cyan"),
    ("⑤", "O‘quvchini ID orqali qidirish", "cyan"),
    ("⑥", "O‘quvchini ism orqali qidirish", "cyan"),
    ("⑦", "O‘quvchiga baho qo‘shish", "cyan"),
    ("⑧", "O‘quvchining baholarini ko‘rish", "cyan"),
    ("⑨", "O‘rtacha bahoni ko‘rish", "cyan"),
    ("⑩", "O‘quvchilar reytingi", "cyan"),
    ("⑪", "Eng yuqori natijali o‘quvchi", "cyan"),
    ("⑫", "Guruh bo‘yicha filtrlash", "magenta"),
    ("⑬", "Fan bo‘yicha eng yuqori o‘rtacha", "magenta"),
    ("⑭", "O‘rtacha bahosi 4 dan yuqori o‘quvchilar", "magenta"),
    ("⑮", "Matnli hisobot yaratish", "magenta"),
    ("⓪", "Chiqish", "red"),
]


def show_menu() -> None:
    cprint(
        text="===== STUDENT MANAGEMENT SYSTEM =====", fore_256="black", back_256="cyan"
    )
    for symbol, text, color in menu_items:
        cprint(f" {symbol}  {text}", fore_256=color)


def break_line() -> None:
    cprint("-" * 100, fore_256="blue")


# ---------- Rangli xabarlar ----------
def print_success(message: str) -> None:
    cprint(f" {message} ", fore_256="black", back_256="green")


def print_error(message: str) -> None:
    cprint(f" {message} ", fore_256="white", back_256="red")


def print_info(message: str) -> None:
    cprint(f" {message} ", fore_256="black", back_256="yellow")


def print_title(message: str) -> None:
    cprint(f" {message} ", fore_256="black", back_256="cyan")


# ---------- Input tekshirish ----------
def read_int(prompt: str, min_value: int = None, max_value: int = None) -> int:
    """To'g'ri butun son kiritilguncha so'raydi."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print_error("Iltimos, butun son kiriting.")
            continue

        if min_value is not None and value < min_value:
            print_error(f"Qiymat {min_value} dan kichik bo‘lmasligi kerak.")
            continue
        if max_value is not None and value > max_value:
            print_error(f"Qiymat {max_value} dan katta bo‘lmasligi kerak.")
            continue
        return value


def read_non_empty(prompt: str) -> str:
    """Bo'sh bo'lmagan matn kiritilguncha so'raydi."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print_error("Bu maydon bo‘sh bo‘lmasligi kerak.")


def confirm(prompt: str) -> bool:
    answer = input(f"{prompt} (ha/yo‘q): ").strip().lower()
    return answer in ("ha", "h", "yes", "y")


# ---------- O'quvchi bilan ishlash ----------
def find_student_by_id(student_id: int):
    for student in database.students:
        if student["id"] == student_id:
            return student
    return None


def format_student(student: dict) -> str:
    return (
        f"ID: {student['id']:<4} | Ism: {student['name']:<25} | "
        f"Yosh: {student['age']:<4} | Guruh: {student['group']}"
    )


def print_students(students_list: list) -> None:
    print_title("O‘QUVCHILAR RO‘YXATI")
    for student in students_list:
        print(format_student(student))
