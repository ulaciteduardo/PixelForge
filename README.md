# 🎮 PixelForge

**PixelForge** es una aplicación web desarrollada con **Flask** que permite a los usuarios descubrir videojuegos, crear una cuenta, iniciar sesión y publicar reseñas con puntuaciones, utilizando la API pública de **RAWG**.

El proyecto está enfocado en ofrecer una experiencia moderna, elegante y centrada en la comunidad gamer.

---

## ✨ Características principales

- 🔐 **Autenticación de usuarios**
  - Registro con validaciones (usuario y email únicos)
  - Login con nombre de usuario y contraseña
  - Logout seguro con Flask-Login

- 🎮 **Exploración de videojuegos**
  - Listado dinámico de juegos desde la API de RAWG
  - Vista detallada de cada juego con imagen destacada

- ⭐ **Sistema de reseñas**
  - Puntuación por estrellas (1–5)
  - Comentarios escritos
  - Un usuario solo puede reseñar un juego una vez
  - Separación clara entre *Tu reseña* y *Reseñas de la comunidad*

- 👤 **Perfil de usuario avanzado**
  - Biografía editable
  - Estadísticas (reseñas publicadas)
  - Historial de reseñas
  - Diseño visual tipo “perfil gamer”

- 🎨 **Diseño moderno**
  - Inspirado en RAWG / Steam
  - UI oscura, limpia y responsiva
  - Animaciones suaves y tarjetas elegantes

---

## 🛠️ Tecnologías utilizadas

- **Backend**
  - Python 3
  - Flask
  - Flask-Login
  - SQLAlchemy
  - SQLite

- **Frontend**
  - HTML5
  - Jinja2
  - CSS3 (custom, sin frameworks)

- **API externa**
  - [RAWG Video Games Database API](https://rawg.io/apidocs)