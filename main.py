from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import requests

from config import Config
from models import db, User, Review

def rawg_get(url):
    try:
        response = requests.get(url, verify=False, timeout=5)

        if response.status_code != 200:
            return None

        return response.json()

    except Exception as e:
        print("RAWG ERROR:", e)
        return None


app = Flask(__name__)
app.config.from_object(Config)

@app.context_processor
def inject_year():
    return {"now": lambda: datetime.now(timezone.utc)}

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    data = rawg_get(
    f"https://api.rawg.io/api/games?key={Config.RAWG_API_KEY}"
    )

    games = data["results"] if data and "results" in data else []

    return render_template("index.html", games=games)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Convertir fecha
        fecha_nacimiento = datetime.strptime(
            request.form["fecha_nacimiento"], "%Y-%m-%d"
        ).date()

        if User.query.filter_by(username=username).first():
            return render_template(
                "register.html",
                error="El nombre de usuario ya existe"
            )

        if User.query.filter_by(email=email).first():
            return render_template(
                "register.html",
                error="El email ya está registrado"
            )

        # Crear usuario
        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            fecha_nacimiento=fecha_nacimiento,
            cambio_contrasennia=False,
            estado=True
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/profile")
@login_required
def profile():
    reviews = Review.query.filter_by(user_id=current_user.id).all()
    return render_template("profile.html", reviews=reviews)

@app.route("/profile/biography", methods=["POST"])
@login_required
def edit_biography():
    bio = request.form.get("biografia", "").strip()

    current_user.biografia = bio
    db.session.commit()

    return redirect(url_for("profile"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("index"))

        return render_template("login.html", error="Credenciales incorrectas")

    return render_template("login.html")

@app.route("/game/<int:game_id>", methods=["GET", "POST"])
@login_required
def game(game_id):

    # Consulta al API
    game_data = rawg_get(
        f"https://api.rawg.io/api/games/{game_id}?key={Config.RAWG_API_KEY}"
    )

    # Catch de errores al consultar
    if not game_data:
        return render_template(
            "game.html",
            game=None,
            reviews=[],
            user_review=None
        )

    # Valida si el usuario ya reseñó el juego
    user_review = Review.query.filter_by(
        user_id=current_user.id,
        game_id=game_id
    ).first()

    # Guarda la reseña sólo si no hay aun
    if request.method == "POST" and not user_review:
        rating = int(request.form["rating"])
        content = request.form["comment"]

        review = Review(
            game_id=game_id,
            game_name=game_data["name"],
            rating=rating,
            comment=content,
            user_id=current_user.id
        )
        db.session.add(review)
        db.session.commit()

        return redirect(url_for("game", game_id=game_id))

    # Todas las reseñas
    reviews = Review.query.filter(
        Review.game_id == game_id,
        Review.user_id != current_user.id
    ).all()


    return render_template(
        "game.html",
        game=game_data,
        reviews=reviews,
        user_review=user_review
    )


if __name__ == "__main__":
    app.run(debug=True, port=3000)
