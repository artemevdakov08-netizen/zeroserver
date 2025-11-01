from flask import Flask, request, jsonify

app = Flask(_name_)

# Простая база данных в памяти (потом можно заменить на файл или PostgreSQL)
players = {}

@app.route("/")
def home():
    return "✅ ZERO Breaker Server работает!"

# 📜 Регистрация аккаунта
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    if username in players:
        return jsonify({"status": "error", "message": "Имя уже занято!"}), 400
    players[username] = {"money": 1000, "used_codes": []}
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
    promo_codes = {
        "START100": 100,
        "PULSAR": 500,
        "FRIDAY": 10000
    }

    if username not in players:
        return jsonify({"status": "error", "message": "Игрок не найден!"}), 404

    if code in players[username]["used_codes"]:
        return jsonify({"status": "error", "message": "Код уже активирован!"}), 400

    if code in promo_codes:
        reward = promo_codes[code]
        players[username]["money"] += reward
        players[username]["used_codes"].append(code)
        return jsonify({"status": "ok", "message": f"Начислено {reward} монет!"})
    else:
        return jsonify({"status": "error", "message": "Неверный код!"}), 400


if _name_ == "_main_":
    app.run(host="0.0.0.0", port=10000)

