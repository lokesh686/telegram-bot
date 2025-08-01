import sqlite3

conn = sqlite3.connect("expenses.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount REAL,
    category TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

def add_expense(user_id, amount, category):
    cursor.execute("INSERT INTO expenses (user_id, amount, category) VALUES (?, ?, ?)", 
                   (user_id, amount, category))
    conn.commit()

def get_summary(user_id):
    cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE user_id = ? GROUP BY category", 
                   (user_id,))
    data = cursor.fetchall()
    if not data:
        return "No expenses yet."
    return "\n".join([f"{cat.capitalize()}: ₹{amt:.2f}" for cat, amt in data])

def reset_expenses(user_id):
    cursor.execute("DELETE FROM expenses WHERE user_id = ?", (user_id,))
    conn.commit()
