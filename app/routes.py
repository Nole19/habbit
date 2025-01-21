from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from app import app
from app.database import get_db_connection


@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Retrieve all habits
        cursor.execute("""
            SELECT id, name, description, start_date 
            FROM habits
        """)
        habits_rows = cursor.fetchall()
        habits = [
            {
                "id": row.id,
                "name": row.name,
                "description": row.description or "No description provided.",
                "start_date": row.start_date,  # Already a datetime.date object
            }
            for row in habits_rows
        ]
    finally:
        cursor.close()
        conn.close()

    return render_template("index.html", habits=habits)


@app.route("/add", methods=["GET", "POST"])
def add_habit():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Insert habit with current date as the default start date
            cursor.execute(
                "INSERT INTO habits (name, description, start_date) VALUES (?, ?, GETDATE())",
                (name, description),
            )
            conn.commit()
            flash("Habit added successfully!")
        except Exception as e:
            flash(f"Error adding habit: {e}")
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for("index"))
    return render_template("add_habit.html")


@app.route("/edit/<int:habit_id>", methods=["GET", "POST"])
def edit_habit(habit_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        try:
            cursor.execute(
                "UPDATE habits SET name = ?, description = ? WHERE id = ?",
                (name, description, habit_id),
            )
            conn.commit()
            flash("Habit updated successfully!")
        except Exception as e:
            flash(f"Error updating habit: {e}")
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for("index"))
    else:
        try:
            cursor.execute("SELECT id, name, description, start_date FROM habits WHERE id = ?", (habit_id,))
            habit_row = cursor.fetchone()
            habit = {
                "id": habit_row.id,
                "name": habit_row.name,
                "description": habit_row.description or "No description provided.",
                "start_date": habit_row.start_date,  # Already a datetime.date object
            } if habit_row else None
        finally:
            cursor.close()
            conn.close()

        if habit is None:
            flash("Habit not found!")
            return redirect(url_for("index"))

    return render_template("edit_habit.html", habit=habit)


@app.route("/progress/<int:habit_id>")
def progress(habit_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, date, completed FROM habit_progress WHERE habit_id = ?", (habit_id,))
        progress_rows = cursor.fetchall()
        progress = [
            {
                "id": row.id,
                "date": row.date,  # Already a datetime.date object
                "completed": row.completed,
            }
            for row in progress_rows
        ]

        cursor.execute("SELECT id, name, description, start_date FROM habits WHERE id = ?", (habit_id,))
        habit_row = cursor.fetchone()
        habit = {
            "id": habit_row.id,
            "name": habit_row.name,
            "description": habit_row.description or "No description provided.",
            "start_date": habit_row.start_date,  # Already a datetime.date object
            # No need for datetime.strptime here
        } if habit_row else None
    finally:
        cursor.close()
        conn.close()

    if habit is None:
        flash("Habit not found!")
        return redirect(url_for("index"))

    return render_template("progress.html", habit=habit, progress=progress)


@app.route("/delete/<int:habit_id>")
def delete_habit(habit_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM habit_progress WHERE habit_id = ?", (habit_id,))
        cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        conn.commit()
        flash("Habit deleted successfully!")
    except Exception as e:
        flash(f"Error deleting habit: {e}")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for("index"))

@app.route("/done/<int:habit_id>", methods=["POST"])
def mark_done(habit_id):
    """
    Mark the habit as done for today in the habit_progress table.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    today = date.today()  # Get today's date

    try:
        # Check if there's already a progress record for today
        cursor.execute(
            "SELECT id FROM habit_progress WHERE habit_id = ? AND date = ?",
            (habit_id, today)
        )
        existing_progress = cursor.fetchone()

        if existing_progress:
            flash("Habit already marked as done for today!")
        else:
            # Insert a new progress record for today
            cursor.execute(
                "INSERT INTO habit_progress (habit_id, date, completed) VALUES (?, ?, ?)",
                (habit_id, today, True)
            )
            conn.commit()
            flash("Habit marked as done for today!")
    except Exception as e:
        flash(f"Error marking habit as done: {e}")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("index"))
