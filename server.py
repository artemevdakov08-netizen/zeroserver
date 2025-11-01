from flask import Flask, request, jsonify
import os, json

app = Flask(_name_)

# Файл для хранения игроков
DB_FILE = "players.json"

# Загружаем игроков при старте
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        players = json.load(f)
else:
    players = {}

# Загружаем промокоды из файла
PROMO_FILE = "promo_codes.json"
if os.path.exists(PROMO_FILE):
    with open(PROMO_FILE, "r") as f:
        promo_codes = json.load(f)
else:
    promo_codes = {}  # пока пусто, потом заполни JSON с 50 кодами

def save_db():
    with open(DB_FILE, "w") as f:
        json.dump(players, f)

@app.route("/")
def home():
    return "✅ ZERO Breaker Server работает!"

# 📜 Регистрация аккаунта
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"status": "error", "message": "Введите ник и пароль!"}), 400

    if username in players:
        return jsonify({"status": "error", "message": "Имя уже занято!"}), 400

    players[username] = {"password": password, "money": 1000, "used_codes": []}
    save_db()
    return jsonify({"status": "ok", "message": "Аккаунт создан", "player": players[username]})

# 💰 Получить данные игрока
@app.route("/player/<username>")
def get_player(username):
    if username not in players:
        return jsonify({"status": "error", "message": "Игрок не найден!"}), 404
    return jsonify(players[username])

# 🎁 Активировать промокод
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
    






