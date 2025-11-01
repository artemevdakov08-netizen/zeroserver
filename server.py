from flask import Flask, request, jsonify
import os, json

app = Flask(_name_)

DB_FILE = "players.json"

# Загружаем игроков при старте
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        players = json.load(f)
else:
    players = {}

def save_db():
    with open(DB_FILE, "w") as f:
        json.dump(players, f)

@app.route("/")
def home():
    return "✅ ZERO Breaker Server работает!"

# ---------------- Регистрация аккаунта ----------------
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"status": "error", "message": "Введите ник и пароль!"}), 400

    if username in players:
        return jsonify({"status": "error", "message": "Имя уже занято!"}), 400

    # Создаём аккаунт
    players[username] = {"username": username, "password": password, "money": 1000, "used_codes": []}
    save_db()
    return jsonify({"status": "ok", "message": "Аккаунт создан", "player": players[username]})

# ---------------- Получить данные игрока ----------------
@app.route("/player/<username>", methods=["GET"])
def get_player(username):
    if username not in players:
        return jsonify({"status": "error", "message": "Игрок не найден!"}), 404
    return jsonify({"status": "ok", "player": players[username]})

# ---------------- Удаление аккаунта ----------------
@app.route("/delete", methods=["POST"])
def delete_account():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username not in players:
        return jsonify({"status": "error", "message": "Игрок не найден"}), 404

    if players[username]["password"] != password:
        return jsonify({"status": "error", "message": "Неверный пароль"}), 400

    del players[username]
    save_db()
    return jsonify({"status": "ok", "message": f"Аккаунт {username} удалён"})

# ---------------- Активировать промокод ----------------
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

if _name_ == "_main_":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)









