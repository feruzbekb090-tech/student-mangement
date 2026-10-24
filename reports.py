import os

import database
from colored import cprint
from utils import (
    find_student_by_id,
    print_error,
    print_info,
    print_success,
    print_title,
    read_int,
    read_non_empty,
)

REPORT_FILE = os.path.join(database.DATA_DIR, "report.txt")


# ---------- Hisoblash funksiyalari ----------
def calculate_average(numbers: list):
    """Ro'yxat o'rtachasi. Ro'yxat bo'sh bo'lsa None qaytaradi."""
    if not numbers:
        return None
    return sum(numbers) / len(numbers)


def calculate_student_average(student: dict):
    """Barcha fanlardagi barcha baholarning umumiy o'rtachasi."""
    all_grades = []
    for grades_list in student["grades"].values():
        all_grades.extend(grades_list)
    return calculate_average(all_grades)


def calculate_subject_averages(student: dict) -> dict:
    result = {}
    for subject, grades_list in student["grades"].items():
        average = calculate_average(grades_list)
        if average is not None:
            result[subject] = average
    return result


def build_ranking():
    """Reyting uchun yagona mantiq: (rank, student, avg) ro'yxati va bahosizlar."""
    graded = []
    without_grades = []
    for student in database.students:
        average = calculate_student_average(student)
        if average is None:
            without_grades.append(student)
        else:
            graded.append((student, average))

    # O'rtacha kamayish tartibida; teng bo'lsa ism bo'yicha alifbo tartibida
    graded.sort(key=lambda item: (-round(item[1], 2), item[0]["name"].lower()))

    ranked = []
    previous = None
    rank = 0
    for index, (student, average) in enumerate(graded, start=1):
        key = round(average, 2)
        if key != previous:  # teng natijalar bir xil o'rin oladi (1, 1, 3)
            rank = index
            previous = key
        ranked.append((rank, student, average))
    return ranked, without_grades


# ---------- Ko'rsatish funksiyalari ----------
def show_average() -> None:
    student_id = read_int("O‘quvchi ID si: ")
    student = find_student_by_id(student_id)
    if student is None:
        print_error("Bunday ID li o‘quvchi topilmadi.")
        return

    average = calculate_student_average(student)
    if average is None:
        print_info("Baholar mavjud emas.")
        return

    print_title(f"{student['name']} — o‘rtacha baho")
    print(f"Umumiy o‘rtacha: {average:.2f}")
    print("Fanlar kesimida:")
    for subject, subject_avg in calculate_subject_averages(student).items():
        print(f"  {subject}: {subject_avg:.2f}")


def show_ranking() -> None:
    if not database.students:
        print_info("O‘quvchilar ro‘yxati bo‘sh.")
        return

    ranked, without_grades = build_ranking()
    print_title("O‘QUVCHILAR REYTINGI")
    if not ranked:
        print_info("Hech bir o‘quvchida baho yo‘q.")
    for rank, student, average in ranked:
        row = f"{rank}. {student['name']:<25} {student['group']:<12} {average:.2f}"
        if rank == 1:
            cprint(row, fore_256="green")
        else:
            print(row)

    if without_grades:
        print_info("Bahosi yo‘q o‘quvchilar:")
        for student in without_grades:
            print(f"  - {student['name']} ({student['group']})")


def show_top_student() -> None:
    ranked, _ = build_ranking()
    if not ranked:
        print_info("Hech bir o‘quvchida baho yo‘q.")
        return

    top = [item for item in ranked if item[0] == 1]
    print_title("ENG YUQORI NATIJALI O‘QUVCHI(LAR)")
    for _, student, average in top:
        cprint(
            f"{student['name']} ({student['group']}) — {average:.2f}", fore_256="green"
        )
    if len(top) > 1:
        print_info("Natijalari teng bo‘lgan barcha o‘quvchilar ko‘rsatildi.")


def show_group_students() -> None:
    group = read_non_empty("Guruh nomi: ").lower()
    found = [s for s in database.students if s["group"].lower() == group]
    if not found:
        print_error("Bu guruhda o‘quvchi topilmadi.")
        return

    print_title(f"{found[0]['group']} guruhi")
    for student in found:
        average = calculate_student_average(student)
        avg_text = f"{average:.2f}" if average is not None else "baho yo‘q"
        print(f"ID {student['id']:<4} {student['name']:<25} o‘rtacha: {avg_text}")


def calculate_all_subject_averages() -> dict:
    pooled = {}
    for student in database.students:
        for subject, grades_list in student["grades"].items():
            pooled.setdefault(subject.lower(), []).extend(grades_list)
    return {
        subject: calculate_average(values)
        for subject, values in pooled.items()
        if values
    }


def show_best_subject() -> None:
    averages = calculate_all_subject_averages()
    if not averages:
        print_info("Baholar mavjud emas.")
        return

    best = max(round(v, 2) for v in averages.values())
    print_title("FANLAR BO‘YICHA O‘RTACHA")
    for subject, average in sorted(averages.items(), key=lambda x: -x[1]):
        row = f"{subject.capitalize():<20} {average:.2f}"
        if round(average, 2) == best:
            cprint(row, fore_256="green")
        else:
            print(row)


def show_above_four() -> None:
    ranked, _ = build_ranking()
    good = [item for item in ranked if item[2] > 4]
    if not good:
        print_info("O‘rtacha bahosi 4 dan yuqori o‘quvchi yo‘q.")
        return

    print_title("O‘RTACHA BAHOSI 4 DAN YUQORI")
    for _, student, average in good:
        print(f"{student['name']:<25} {student['group']:<12} {average:.2f}")


def create_text_report() -> None:
    if not database.students:
        print_info("O‘quvchilar ro‘yxati bo‘sh, hisobot yaratilmadi.")
        return

    ranked, without_grades = build_ranking()
    lines = ["STUDENT MANAGEMENT SYSTEM — HISOBOT", "=" * 40, ""]
    lines.append(f"Jami o‘quvchilar: {len(database.students)}")
    lines.append("")
    lines.append("Reyting:")
    for rank, student, average in ranked:
        lines.append(
            f"  {rank}. {student['name']} ({student['group']}) — {average:.2f}"
        )
    if without_grades:
        lines.append("")
        lines.append("Bahosi yo‘q o‘quvchilar:")
        for student in without_grades:
            lines.append(f"  - {student['name']} ({student['group']})")

    try:
        os.makedirs(database.DATA_DIR, exist_ok=True)
        with open(REPORT_FILE, "w", encoding="utf-8") as file:
            file.write("\n".join(lines) + "\n")
        print_success(f"Hisobot saqlandi: {REPORT_FILE}")
    except OSError:
        print_error("Hisobotni saqlab bo‘lmadi.")
