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
    players[username] = {"username": username, "level": 1}
    save_db()
    return jsonify({"status": "ok", "message": "Добро пожаловать!", "player": players[username]})

# ---------------- Получить данные игрока ----------------
@app.route("/player/<username>", methods=["GET"])
def get_player(username):
    if username not in players:
        return jsonify({"status": "error", "message": "Игрок не найден!"}), 404
    return jsonify({"status": "ok", "player": players[username]})

# ---------------- Запуск ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)












