"""Flask-приложение «Мои задачи» (To-Do List)."""

import os

from flask import Flask, flash, redirect, render_template, request, url_for

from config import Config
from models import Task, db

MAX_TITLE_LENGTH = 200


def create_app(config_class: type[Config] = Config) -> Flask:
    """Создаёт и настраивает экземпляр приложения."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Каталог instance/ (и файл SQLite внутри него) создаются автоматически.
    os.makedirs(app.instance_path, exist_ok=True)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    def get_task_or_redirect(task_id: int) -> Task | None:
        """Возвращает задачу по ID или None, если её уже нет в базе."""
        task = db.session.get(Task, task_id)
        if task is None:
            flash("Задача не найдена — возможно, она уже была удалена.", "error")
        return task

    @app.get("/")
    def index():
        tasks = Task.query.order_by(
            Task.completed.asc(), Task.created_at.desc()
        ).all()
        total = len(tasks)
        completed = sum(1 for task in tasks if task.completed)

        return render_template(
            "index.html",
            tasks=tasks,
            total=total,
            completed=completed,
            active=total - completed,
        )

    @app.post("/add")
    def add_task():
        title = request.form.get("title", "").strip()

        if not title:
            flash("Название задачи не может быть пустым.", "error")
            return redirect(url_for("index"))

        if len(title) > MAX_TITLE_LENGTH:
            flash(
                f"Название задачи не должно превышать {MAX_TITLE_LENGTH} символов.",
                "error",
            )
            return redirect(url_for("index"))

        db.session.add(Task(title=title))
        db.session.commit()
        return redirect(url_for("index"))

    @app.post("/toggle/<int:task_id>")
    def toggle_task(task_id: int):
        task = get_task_or_redirect(task_id)
        if task is None:
            return redirect(url_for("index"))

        task.completed = not task.completed
        db.session.commit()
        return redirect(url_for("index"))

    @app.post("/delete/<int:task_id>")
    def delete_task(task_id: int):
        task = get_task_or_redirect(task_id)
        if task is None:
            return redirect(url_for("index"))

        db.session.delete(task)
        db.session.commit()
        return redirect(url_for("index"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "5000")),
        debug=app.config["DEBUG"],
    )
