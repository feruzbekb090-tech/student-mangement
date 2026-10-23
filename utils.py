from colored import cprint

menu_text = """1. Barcha o‘quvchilarni ko‘rish
2. O‘quvchi qo‘shish
3. O‘quvchi ma’lumotlarini tahrirlash
4. O‘quvchini o‘chirish
5. O‘quvchini ID orqali qidirish
6. O‘quvchini ism orqali qidirish
7. O‘quvchiga baho qo‘shish
8. O‘quvchining baholarini ko‘rish
9. O‘rtacha bahoni ko‘rish
10. O‘quvchilar reytingi
11. Eng yuqori natijali o‘quvchi
0. Chiqish"""


def show_menu() -> None:
    cprint(
        text="===== STUDENT MANAGEMENT SYSTEM =====", fore_256="cyan", back_256="white"
    )
    print(menu_text)


def break_line() -> None:
    cprint(text="(" - " * 100)", fore_256="yellov", back_256="black")
