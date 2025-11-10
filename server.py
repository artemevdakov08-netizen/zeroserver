from flask import Flask, request, jsonify
import os, json

app = Flask(__name__)

DB_FILE = "players.json"

# Загружаем игроков при старте
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        players = json.load(f)
else:
    players = {}

def save_db():
    with open(DB_FILE, "w") as f:
        json.dump(players, f, ensure_ascii=False, indent=2)

@app.route("/")
def home():
    return "✅ ZERO Breaker Server работает!"

# ---------------- Игрок заходит с ником ----------------
@app.route("/join", methods=["POST"])
def join():
    data = request.json
    username = data.get("username")

    if not username or username.strip() == "":
        return jsonify({"status": "error", "message": "Введите ник!"}), 400

    username = username.strip()

    if username in players:
        return jsonify({"status": "error", "message": "Ник занят!"}), 400

    # Создаём нового игрока
    players[username] = {"username": username, "money": 1000, "level": 1, "used_codes": []}
    save_db()
    return jsonify({"status": "ok", "message": "Добро пожаловать!", "player": players[username]})

# ---------------- Получить данные игрока ----------------
@app.route("/player/<username>", methods=["GET"])
def get_player(username):
    if username not in players:
        return jsonify({"status": "error", "message": "Игрок не найден!"}), 404
    return jsonify({"status": "ok", "player": players[username]})

# ---------------- Промокоды ----------------
PROMO_FILE = "promo_codes.json"
if os.path.exists(PROMO_FILE):
    with open(PROMO_FILE, "r") as f:
        promo_codes = json.load(f)
else:
    promo_codes = {
        "ZERO": 1000, "NEZOKS": 2500, "ИГРА": 1500, "КАРТЫ": 2000, "АМНИСТИЙ": 3000,
        "МИР": 5000, "ДЕНЬГИ": 777, "УДАЧА": 3333, "ПЯТНИЦА": 3000, "СЕКРЕТ": 9999,
        "DEEBING": 3000, "ВИКА": 5000, "ПРИЗРАК": 500, "+5": 500, "ПРОИГРЫШЬ": 200,
        "РОБОТ": 400, "GODOT": 5000, "PLAY": 1000, "1.0": 300, "WaffleEater3000": 3000,
        "КРАСНЫЙ": 500, "СТАРТ": 1000, "ПЕРВЫЙ ХОД": 1200, "ШАНС": 1000, "БОНУС": 1200,
        "КОМБО": 1300, "ХОД": 900, "СДЕЛКА": 1400, "ТУР": 1100, "РЕШЕНИЕ": 2500,
        "МОНЕТА": 2000, "ПРОРЫВ": 3500, "ПРОБУЖДЕНИЕ": 3000, "ТЕНЬ": 4000, "РЕВАНШ": 3000,
        "ПАМЯТЬ": 3500, "МУЗЫКА": 3000, "КОД505": 6000, "СИЛА": 6000, "ОГОНЬ": 7000,
        "ПУЛЬС": 5000, "БОГ": 10000, "ФИНАЛ": 15000, "СЛУЧАЙ": 20000, "НОЛЬ": 30000,
        "КОНТРОЛЬ": 25000, "ПЕРЕЗАПУСК": 18000, "ЭХО": 4500, "ИЛЛЮЗИЯ": 5500, "ФОРТУНА": 7000
    } 

@app.route("/promo", methods=["POST"])
def promo():
    data = request.json
    username = data.get("username")
    code = data.get("code")

    if username not in players:
        return jsonify({"status": "error", "message": "Игрок не найден!"}), 404

    if code in players[username]["used_codes"]:
        return jsonify({"status": "error", "message": "Код уже активирован!"}), 400

    if code in promo_codes:
        reward = promo_codes[code]
        players[username]["money"] += reward
        players[username]["used_codes"].append(code)
        save_db()
        return jsonify({"status": "ok", "message": f"Начислено {reward} монет!"})
    else:
        return jsonify({"status": "error", "message": "Неверный код!"}), 400

# ---------------- Получение денег ----------------
@app.route("/get_money", methods=["GET"])
def get_money():
    username = request.args.get("username")
    if not username or username not in players:
        return jsonify({"status": "error", "message": "Игрок не найден!"}), 404
    return jsonify({"status": "ok", "money": players[username]["money"]})

# ---------------- Обновление денег ----------------
@app.route("/update_money", methods=["POST"])
def update_money():
    data = request.json
    username = data.get("username")
    money = data.get("money")

    if not username or username not in players:
        return jsonify({"status": "error", "message": "Игрок не найден!"}), 404

    if money is None or not isinstance(money, (int, float)):
        return jsonify({"status": "error", "message": "Некорректное значение денег!"}), 400

    players[username]["money"] = int(money)
    save_db()
    return jsonify({"status": "ok", "message": "Баланс обновлён!", "money": int(money)})

# ---------------- Запуск ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)











