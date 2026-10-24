import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DB_FILE = os.path.join(DATA_DIR, "database.json")

# O'quvchilar ro'yxati va ID hisoblagichi.
# Ular boshqa modullar import qilgani uchun o'zgaruvchining o'zi emas,
# ichidagi qiymat o'zgartiriladi (clear/append, id_counter["next_id"]).
students = []
id_counter = {"next_id": 1}


def get_next_id() -> int:
    new_id = id_counter["next_id"]
    id_counter["next_id"] += 1
    return new_id


def save_data() -> bool:
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        data = {"next_id": id_counter["next_id"], "students": students}
        with open(DB_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return True
    except OSError:
        return False


def load_data() -> bool:
    """JSON fayldan o'qiydi. Fayl yo'q bo'lsa ham xato hisoblanmaydi."""
    students.clear()
    id_counter["next_id"] = 1

    if not os.path.exists(DB_FILE):
        return True

    try:
        with open(DB_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        loaded = data.get("students", [])
        students.extend(loaded)
        saved_next_id = data.get("next_id", 1)
    except (json.JSONDecodeError, OSError, AttributeError):
        return False

    max_id = max((s["id"] for s in students), default=0)
    id_counter["next_id"] = max(saved_next_id, max_id + 1)
    return True
