import database
import grades
import reports
import students
from utils import break_line, print_error, print_info, show_menu

ACTIONS = {
    "1": students.show_all_students,
    "2": students.add_student,
    "3": students.edit_student,
    "4": students.delete_student,
    "5": students.search_by_id,
    "6": students.search_by_name,
    "7": grades.add_grade,
    "8": grades.show_grades,
    "9": reports.show_average,
    "10": reports.show_ranking,
    "11": reports.show_top_student,
    "12": reports.show_group_students,
    "13": reports.show_best_subject,
    "14": reports.show_above_four,
    "15": reports.create_text_report,
}


def main() -> None:
    if not database.load_data():
        print_error("database.json o‘qilmadi, bo‘sh ro‘yxat bilan boshlandi.")

    while True:
        show_menu()
        choice = input("> ").strip()
        break_line()

        if choice == "0":
            database.save_data()
            print_info("Dastur tugadi. Xayr!")
            break

        action = ACTIONS.get(choice)
        if action is None:
            print_error("Noto‘g‘ri tanlov. Menyudagi raqamlardan birini kiriting.")
        else:
            action()
        break_line()


if __name__ == "__main__":
    main()
