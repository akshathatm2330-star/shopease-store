from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import os
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "shopease-development-secret-key"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "shopease.db")


# =========================================================
# PRODUCTS
# =========================================================

PRODUCTS = [
    ("Laptop", "laptop1.webp", 49999, 59999, "Electronics", 4.9, 245,
     "Powerful laptop suitable for students, programming and professional work."),

    ("Smart Phone", "smart phone1.avif", 15999, 18999, "Electronics", 4.7, 532,
     "Modern smartphone with excellent camera, display and battery."),

    ("Wireless Headphones", "headphone.webp", 1499, 1999, "Electronics", 4.8, 321,
     "Wireless headphones with clear sound and deep bass."),

    ("Smart Watch", "smart watch1.webp", 2499, 3499, "Electronics", 4.7, 186,
     "Smart watch with fitness tracking and notifications."),

    ("Bluetooth Speaker", "bluetooth spe.avif", 1299, 1799, "Electronics", 4.6, 154,
     "Portable Bluetooth speaker with powerful sound."),

    ("Gaming Mouse", "mouse.jpg", 899, 1299, "Electronics", 4.5, 98,
     "High precision gaming mouse with comfortable grip."),

    ("Mechanical Keyboard", "keyboard.jpg", 1899, 2499, "Electronics", 4.8, 143,
     "Mechanical keyboard suitable for gaming and programming."),

    ("Power Bank", "powerbank.jpg", 999, 1499, "Electronics", 4.4, 88,
     "Compact high-capacity power bank."),

    ("Cotton T-Shirt", "tshirt.webp", 599, 899, "Fashion", 4.4, 112,
     "Soft and comfortable cotton T-shirt."),

    ("Denim Pants", "pant.webp", 1299, 1799, "Fashion", 4.5, 156,
     "Classic denim pants with comfortable fit."),

    ("Sports Shoes", "shoe.jpg", 1999, 2999, "Fashion", 4.7, 201,
     "Lightweight sports shoes for walking and running."),

    ("Handbag", "bag.avif", 1599, 2299, "Fashion", 4.5, 90,
     "Stylish handbag with spacious compartments."),

    ("Sunglasses", "sunglass.webp", 799, 1199, "Fashion", 4.3, 75,
     "Stylish lightweight sunglasses."),

    ("Coffee Mug", "mug.jpg", 299, 499, "Home", 4.5, 84,
     "Elegant ceramic coffee mug."),

    ("Table Lamp", "lamp.jpg", 899, 1299, "Home", 4.6, 102,
     "Modern table lamp for study and work."),

    ("Plant Pot", "pot.webp", 349, 499, "Home", 4.4, 70,
     "Decorative plant pot for home and office."),

    ("Wall Clock", "clock.jpg", 699, 999, "Home", 4.5, 91,
     "Modern wall clock with clean design."),

    ("Cap", "cap.webp", 399, 599, "Fashion", 4.4, 63,
     "Comfortable casual cap suitable for everyday use.")
]


# =========================================================
# DATABASE CONNECTION
# =========================================================

def db():
    conn = sqlite3.connect(
        DB_PATH,
        timeout=30,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA busy_timeout = 30000")

    return conn


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

def init_db():

    conn = db()

    try:

        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS cart (
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 1,
                PRIMARY KEY(user_id, product_id)
            );

            CREATE TABLE IF NOT EXISTS wishlist (
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                PRIMARY KEY(user_id, product_id)
            );

            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                order_code TEXT NOT NULL,
                total REAL NOT NULL,
                payment TEXT NOT NULL,
                address TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Order Placed',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                image TEXT NOT NULL,
                price REAL NOT NULL,
                old_price REAL NOT NULL,
                category TEXT NOT NULL,
                rating REAL NOT NULL,
                reviews INTEGER NOT NULL,
                description TEXT NOT NULL
            );
        """)

        for product_id, product in enumerate(PRODUCTS, start=1):

            conn.execute("""
                INSERT OR REPLACE INTO products
                (
                    id,
                    name,
                    image,
                    price,
                    old_price,
                    category,
                    rating,
                    reviews,
                    description
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                product_id,
                *product
            ))

        conn.commit()

    finally:

        conn.close()


# =========================================================
# IMPORTANT FOR RENDER
# =========================================================
#
# Gunicorn starts the application using:
#
# gunicorn app:app
#
# Therefore this code MUST run when app.py is imported.
#
# This fixes:
# sqlite3.OperationalError: no such table: users
#

init_db()


# =========================================================
# LOGIN CHECK
# =========================================================

def logged_in():
    return "user_id" in session


# =========================================================
# CART HELPER
# =========================================================

def get_cart():

    if not logged_in():
        return []

    conn = db()

    try:

        rows = conn.execute("""
            SELECT
                p.*,
                c.quantity
            FROM cart c
            JOIN products p
                ON p.id = c.product_id
            WHERE c.user_id = ?
            ORDER BY p.id
        """, (
            session["user_id"],
        )).fetchall()

        return rows

    finally:

        conn.close()


# =========================================================
# CART TOTAL
# =========================================================

def get_cart_total():

    items = get_cart()

    return sum(
        float(item["price"]) * int(item["quantity"])
        for item in items
    )


# =========================================================
# WISHLIST IDS
# =========================================================

def get_wishlist_ids():

    if not logged_in():
        return []

    conn = db()

    try:

        rows = conn.execute("""
            SELECT product_id
            FROM wishlist
            WHERE user_id = ?
        """, (
            session["user_id"],
        )).fetchall()

        return [
            row["product_id"]
            for row in rows
        ]

    finally:

        conn.close()


# =========================================================
# GLOBAL TEMPLATE VARIABLES
# =========================================================

@app.context_processor
def inject_globals():

    if not logged_in():

        return {
            "cart_count": 0,
            "wishlist_count": 0,
            "logged_user": None,
            "wishlist_ids": []
        }

    conn = db()

    try:

        user_id = session["user_id"]

        cart_count = conn.execute("""
            SELECT COALESCE(SUM(quantity), 0)
            FROM cart
            WHERE user_id = ?
        """, (
            user_id,
        )).fetchone()[0]

        wishlist_count = conn.execute("""
            SELECT COUNT(*)
            FROM wishlist
            WHERE user_id = ?
        """, (
            user_id,
        )).fetchone()[0]

        user = conn.execute("""
            SELECT username
            FROM users
            WHERE id = ?
        """, (
            user_id,
        )).fetchone()

        wishlist_rows = conn.execute("""
            SELECT product_id
            FROM wishlist
            WHERE user_id = ?
        """, (
            user_id,
        )).fetchall()

        wishlist_ids = [
            row["product_id"]
            for row in wishlist_rows
        ]

        return {
            "cart_count": cart_count,
            "wishlist_count": wishlist_count,
            "logged_user": user["username"] if user else None,
            "wishlist_ids": wishlist_ids
        }

    finally:

        conn.close()


# =========================================================
# LOGIN / REGISTER
# =========================================================

@app.route("/", methods=["GET", "POST"])
def login():

    if logged_in():
        return redirect(url_for("home"))

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        if not username or not password:

            flash(
                "Enter username and password.",
                "danger"
            )

            return render_template("login.html")

        conn = db()

        try:

            user = conn.execute("""
                SELECT *
                FROM users
                WHERE username = ?
            """, (
                username,
            )).fetchone()

            if user:

                if check_password_hash(
                    user["password"],
                    password
                ):

                    session.clear()

                    session["user_id"] = user["id"]
                    session["username"] = user["username"]

                    return redirect(
                        url_for("home")
                    )

                flash(
                    "Incorrect password.",
                    "danger"
                )

                return render_template(
                    "login.html"
                )

            password_hash = generate_password_hash(
                password
            )

            try:

                cursor = conn.execute("""
                    INSERT INTO users(
                        username,
                        password
                    )
                    VALUES (?, ?)
                """, (
                    username,
                    password_hash
                ))

                conn.commit()

                user_id = cursor.lastrowid

                session.clear()

                session["user_id"] = user_id
                session["username"] = username

                flash(
                    "Account created successfully!",
                    "success"
                )

                return redirect(
                    url_for("home")
                )

            except sqlite3.IntegrityError:

                conn.rollback()

                flash(
                    "Username already exists.",
                    "danger"
                )

                return render_template(
                    "login.html"
                )

        finally:

            conn.close()

    return render_template(
        "login.html"
    )


# =========================================================
# HOME
# =========================================================

@app.route("/home")
def home():

    if not logged_in():
        return redirect(url_for("login"))

    category = request.args.get(
        "category",
        "All"
    )

    search = request.args.get(
        "search",
        ""
    ).strip()

    conn = db()

    try:

        query = """
            SELECT *
            FROM products
            WHERE 1 = 1
        """

        args = []

        if category != "All":

            query += """
                AND category = ?
            """

            args.append(category)

        if search:

            query += """
                AND (
                    name LIKE ?
                    OR category LIKE ?
                )
            """

            args.extend([
                f"%{search}%",
                f"%{search}%"
            ])

        query += """
            ORDER BY id
        """

        products = conn.execute(
            query,
            args
        ).fetchall()

        wishlist_rows = conn.execute("""
            SELECT product_id
            FROM wishlist
            WHERE user_id = ?
        """, (
            session["user_id"],
        )).fetchall()

        wishlist_ids = [
            row["product_id"]
            for row in wishlist_rows
        ]

        return render_template(
            "home.html",
            products=products,
            category=category,
            search=search,
            wishlist_ids=wishlist_ids
        )

    finally:

        conn.close()


# =========================================================
# WISHLIST TOGGLE
# =========================================================

@app.route(
    "/wishlist/toggle/<int:product_id>",
    methods=["POST"]
)
def wishlist_toggle(product_id):

    if not logged_in():

        return jsonify({
            "ok": False,
            "login": True
        }), 401

    conn = db()

    try:

        product = conn.execute("""
            SELECT id
            FROM products
            WHERE id = ?
        """, (
            product_id,
        )).fetchone()

        if not product:

            return jsonify({
                "ok": False,
                "message": "Product not found."
            }), 404

        exists = conn.execute("""
            SELECT 1
            FROM wishlist
            WHERE user_id = ?
            AND product_id = ?
        """, (
            session["user_id"],
            product_id
        )).fetchone()

        if exists:

            conn.execute("""
                DELETE FROM wishlist
                WHERE user_id = ?
                AND product_id = ?
            """, (
                session["user_id"],
                product_id
            ))

            active = False

        else:

            conn.execute("""
                INSERT OR IGNORE INTO wishlist(
                    user_id,
                    product_id
                )
                VALUES (?, ?)
            """, (
                session["user_id"],
                product_id
            ))

            active = True

        conn.commit()

        count = conn.execute("""
            SELECT COUNT(*)
            FROM wishlist
            WHERE user_id = ?
        """, (
            session["user_id"],
        )).fetchone()[0]

        return jsonify({
            "ok": True,
            "active": active,
            "product_id": product_id,
            "wishlist_count": count
        })

    except sqlite3.OperationalError as error:

        conn.rollback()

        return jsonify({
            "ok": False,
            "message": str(error)
        }), 500

    finally:

        conn.close()


# =========================================================
# WISHLIST PAGE
# =========================================================

@app.route("/wishlist")
def wishlist():

    if not logged_in():
        return redirect(url_for("login"))

    conn = db()

    try:

        products = conn.execute("""
            SELECT p.*
            FROM wishlist w
            JOIN products p
                ON p.id = w.product_id
            WHERE w.user_id = ?
            ORDER BY p.id
        """, (
            session["user_id"],
        )).fetchall()

        wishlist_ids = [
            product["id"]
            for product in products
        ]

        return render_template(
            "wishlist.html",
            products=products,
            wishlist_ids=wishlist_ids
        )

    finally:

        conn.close()


# =========================================================
# ADD TO CART
# =========================================================

@app.route(
    "/cart/add/<int:product_id>",
    methods=["POST"]
)
def cart_add(product_id):

    if not logged_in():

        if request.headers.get(
            "X-Requested-With"
        ) == "XMLHttpRequest":

            return jsonify({
                "ok": False,
                "login": True
            }), 401

        return redirect(
            url_for("login")
        )

    conn = db()

    try:

        product = conn.execute("""
            SELECT *
            FROM products
            WHERE id = ?
        """, (
            product_id,
        )).fetchone()

        if not product:

            return jsonify({
                "ok": False,
                "message": "Product not found."
            }), 404

        row = conn.execute("""
            SELECT quantity
            FROM cart
            WHERE user_id = ?
            AND product_id = ?
        """, (
            session["user_id"],
            product_id
        )).fetchone()

        if row:

            new_quantity = row["quantity"] + 1

            conn.execute("""
                UPDATE cart
                SET quantity = ?
                WHERE user_id = ?
                AND product_id = ?
            """, (
                new_quantity,
                session["user_id"],
                product_id
            ))

        else:

            new_quantity = 1

            conn.execute("""
                INSERT INTO cart(
                    user_id,
                    product_id,
                    quantity
                )
                VALUES (?, ?, ?)
            """, (
                session["user_id"],
                product_id,
                1
            ))

        conn.commit()

        if request.headers.get(
            "X-Requested-With"
        ) == "XMLHttpRequest":

            return jsonify({
                "ok": True,
                "message": f"{product['name']} added to cart.",
                "quantity": new_quantity
            })

        flash(
            f"{product['name']} added to cart.",
            "success"
        )

        return redirect(
            request.referrer or url_for("home")
        )

    except sqlite3.OperationalError as error:

        conn.rollback()

        return jsonify({
            "ok": False,
            "message": str(error)
        }), 500

    finally:

        conn.close()


# =========================================================
# CART
# =========================================================

@app.route("/cart")
def cart():

    if not logged_in():
        return redirect(url_for("login"))

    return render_template(
        "cart.html",
        items=get_cart(),
        subtotal=get_cart_total()
    )


# =========================================================
# UPDATE CART
# =========================================================

@app.route(
    "/cart/update/<int:product_id>",
    methods=["POST"]
)
def cart_update(product_id):

    if not logged_in():
        return redirect(url_for("login"))

    action = request.form.get(
        "action",
        ""
    )

    conn = db()

    try:

        row = conn.execute("""
            SELECT quantity
            FROM cart
            WHERE user_id = ?
            AND product_id = ?
        """, (
            session["user_id"],
            product_id
        )).fetchone()

        if row:

            quantity = row["quantity"]

            if action == "plus":
                quantity += 1

            elif action == "minus":
                quantity -= 1

            if quantity <= 0:

                conn.execute("""
                    DELETE FROM cart
                    WHERE user_id = ?
                    AND product_id = ?
                """, (
                    session["user_id"],
                    product_id
                ))

            else:

                conn.execute("""
                    UPDATE cart
                    SET quantity = ?
                    WHERE user_id = ?
                    AND product_id = ?
                """, (
                    quantity,
                    session["user_id"],
                    product_id
                ))

            conn.commit()

    finally:

        conn.close()

    return redirect(
        url_for("cart")
    )


# =========================================================
# REMOVE CART ITEM
# =========================================================

@app.route(
    "/cart/remove/<int:product_id>",
    methods=["POST"]
)
def cart_remove(product_id):

    if not logged_in():
        return redirect(url_for("login"))

    conn = db()

    try:

        conn.execute("""
            DELETE FROM cart
            WHERE user_id = ?
            AND product_id = ?
        """, (
            session["user_id"],
            product_id
        ))

        conn.commit()

    finally:

        conn.close()

    flash(
        "Product removed from cart.",
        "success"
    )

    return redirect(
        url_for("cart")
    )


# =========================================================
# CHECKOUT
# =========================================================

@app.route(
    "/checkout",
    methods=["GET", "POST"]
)
def checkout():

    if not logged_in():
        return redirect(url_for("login"))

    items = get_cart()

    if not items:

        flash(
            "Your cart is empty.",
            "danger"
        )

        return redirect(
            url_for("cart")
        )

    total = get_cart_total()

    if request.method == "POST":

        address = request.form.get(
            "address",
            ""
        ).strip()

        payment = request.form.get(
            "payment",
            "Cash on Delivery"
        )

        if not address:

            flash(
                "Enter delivery address.",
                "danger"
            )

            return render_template(
                "checkout.html",
                items=items,
                total=total
            )

        order_code = (
            "SE" +
            datetime.datetime.now().strftime(
                "%Y%m%d%H%M%S"
            )
        )

        conn = db()

        try:

            cursor = conn.execute("""
                INSERT INTO orders(
                    user_id,
                    order_code,
                    total,
                    payment,
                    address
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                session["user_id"],
                order_code,
                total,
                payment,
                address
            ))

            order_id = cursor.lastrowid

            for item in items:

                conn.execute("""
                    INSERT INTO order_items(
                        order_id,
                        product_id,
                        product_name,
                        price,
                        quantity
                    )
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    order_id,
                    item["id"],
                    item["name"],
                    item["price"],
                    item["quantity"]
                ))

            conn.execute("""
                DELETE FROM cart
                WHERE user_id = ?
            """, (
                session["user_id"],
            ))

            conn.commit()

        except Exception:

            conn.rollback()

            flash(
                "Unable to place order. Please try again.",
                "danger"
            )

            return redirect(
                url_for("checkout")
            )

        finally:

            conn.close()

        flash(
            f"Order {order_code} placed successfully!",
            "success"
        )

        return redirect(
            url_for("orders")
        )

    return render_template(
        "checkout.html",
        items=items,
        total=total
    )


# =========================================================
# ORDERS
# =========================================================

@app.route("/orders")
def orders():

    if not logged_in():
        return redirect(url_for("login"))

    conn = db()

    try:

        orders_rows = conn.execute("""
            SELECT *
            FROM orders
            WHERE user_id = ?
            ORDER BY id DESC
        """, (
            session["user_id"],
        )).fetchall()

        result = []

        for order in orders_rows:

            items = conn.execute("""
                SELECT *
                FROM order_items
                WHERE order_id = ?
                ORDER BY id
            """, (
                order["id"],
            )).fetchall()

            result.append({
                "order": order,
                "items": items
            })

        return render_template(
            "orders.html",
            orders=result
        )

    finally:

        conn.close()


# =========================================================
# PRODUCT DETAILS
# =========================================================

@app.route(
    "/product/<int:product_id>"
)
def product(product_id):

    if not logged_in():
        return redirect(url_for("login"))

    conn = db()

    try:

        product_row = conn.execute("""
            SELECT *
            FROM products
            WHERE id = ?
        """, (
            product_id,
        )).fetchone()

    finally:

        conn.close()

    if not product_row:

        flash(
            "Product not found.",
            "danger"
        )

        return redirect(
            url_for("home")
        )

    return render_template(
        "product.html",
        product=product_row
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")
def health():

    try:

        conn = db()

        tables = conn.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
        """).fetchall()

        conn.close()

        table_names = [
            row["name"]
            for row in tables
        ]

        return jsonify({
            "status": "ok",
            "application": "ShopEase",
            "database": "connected",
            "tables": table_names
        })

    except Exception as error:

        return jsonify({
            "status": "error",
            "application": "ShopEase",
            "database": "error",
            "message": str(error)
        }), 500


# =========================================================
# LOCAL DEVELOPMENT
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )