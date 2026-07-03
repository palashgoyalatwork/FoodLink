import sqlite3


def create_table():
    conn = sqlite3.connect("foodlink.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS donations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        food_name TEXT,
        total_quantity INTEGER,
        remaining_quantity INTEGER,
        donor_name TEXT,
        location TEXT,
        pickup_deadline TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_donation(food_name, quantity, donor_name, location, pickup_deadline):
    conn = sqlite3.connect("foodlink.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO donations
    (
        food_name,
        total_quantity,
        remaining_quantity,
        donor_name,
        location,
        pickup_deadline,
        status
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        food_name,
        quantity,
        quantity,
        donor_name,
        location,
        str(pickup_deadline),
        "Available"
    ))

    conn.commit()
    conn.close()


def get_donations():
    conn = sqlite3.connect("foodlink.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM donations")
    data = cursor.fetchall()

    conn.close()

    return data


def reserve_donation(donation_id):
    conn = sqlite3.connect("foodlink.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE donations
    SET status = 'Reserved'
    WHERE id = ?
    """, (donation_id,))

    conn.commit()
    conn.close()


def total_donations():
    conn = sqlite3.connect("foodlink.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM donations")

    total = cursor.fetchone()[0]

    conn.close()

    return total


def total_meals_saved():
    conn = sqlite3.connect("foodlink.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(total_quantity) FROM donations"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total if total else 0


def reserved_donations():
    conn = sqlite3.connect("foodlink.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM donations
    WHERE status = 'Reserved'
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def request_food(donation_id, requested_qty):

    conn = sqlite3.connect("foodlink.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT remaining_quantity
    FROM donations
    WHERE id = ?
    """, (donation_id,))

    result = cursor.fetchone()

    if result is None:
        conn.close()
        return False

    remaining = result[0]

    print("Remaining =", remaining)
    print("Requested =", requested_qty)

    new_remaining = remaining - requested_qty

    if new_remaining < 0:
        conn.close()
        return False

    status = "Available"

    if new_remaining == 0:
        status = "Completed"

    cursor.execute("""
    UPDATE donations
    SET remaining_quantity = ?,
        status = ?
    WHERE id = ?
    """,
    (
        new_remaining,
        status,
        donation_id
    ))

    conn.commit()
    conn.close()

    return True