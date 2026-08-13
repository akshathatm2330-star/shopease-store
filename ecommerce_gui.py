import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pillow_avif
import os
import json
from datetime import datetime


# ============================================================
# COLORS
# ============================================================

BG = "#f4f7fb"
WHITE = "#ffffff"
DARK = "#172033"
TEXT = "#334155"
GRAY = "#64748b"
BORDER = "#e2e8f0"

BLUE = "#2563eb"
BLUE_DARK = "#1d4ed8"
BLUE_LIGHT = "#eff6ff"

GREEN = "#16a34a"
GREEN_LIGHT = "#f0fdf4"

RED = "#dc2626"
RED_LIGHT = "#fef2f2"

PINK = "#db2777"
PINK_LIGHT = "#fdf2f8"

PURPLE = "#7c3aed"
ORANGE = "#ea580c"


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

IMAGE_DIR = os.path.join(
    BASE_DIR,
    "images"
)

USER_DATA_FILE = os.path.join(
    BASE_DIR,
    "user_data.json"
)


# ============================================================
# USER DATA
# ============================================================

USER_DATA = {}


def load_user_data():

    global USER_DATA

    if not os.path.exists(USER_DATA_FILE):

        USER_DATA = {}

        return

    try:

        with open(
            USER_DATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            USER_DATA = json.load(file)

        print("User data loaded successfully.")

    except Exception as error:

        print(
            "Could not load user data:",
            error
        )

        USER_DATA = {}


def save_all_user_data():

    try:

        with open(
            USER_DATA_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                USER_DATA,
                file,
                indent=4,
                ensure_ascii=False
            )

        print("User data saved.")

    except Exception as error:

        print(
            "Could not save user data:",
            error
        )


def get_user_data(username):

    if username not in USER_DATA:

        USER_DATA[username] = {
            "cart": {},
            "wishlist": [],
            "orders": []
        }

        save_all_user_data()

    return USER_DATA[username]


# ============================================================
# PRODUCTS
# ============================================================

PRODUCTS = [

    {
        "name": "Laptop",
        "image": "laptop1.webp",
        "price": 49999,
        "old_price": 59999,
        "category": "Electronics",
        "rating": 4.9,
        "reviews": 245,
        "stock": 10,
        "emoji": "💻",
        "description":
            "Powerful laptop suitable for students, "
            "programming and professional work."
    },

    {
        "name": "Smart Phone",
        "image": "smart phone1.avif",
        "price": 15999,
        "old_price": 18999,
        "category": "Electronics",
        "rating": 4.7,
        "reviews": 532,
        "stock": 15,
        "emoji": "📱",
        "description":
            "Modern smartphone with excellent camera, "
            "display and battery."
    },

    {
        "name": "Wireless Headphones",
        "image": "headphone.webp",
        "price": 1499,
        "old_price": 1999,
        "category": "Electronics",
        "rating": 4.8,
        "reviews": 321,
        "stock": 20,
        "emoji": "🎧",
        "description":
            "Wireless headphones with clear sound "
            "and deep bass."
    },

    {
        "name": "Smart Watch",
        "image": "smart watch1.webp",
        "price": 2499,
        "old_price": 3499,
        "category": "Electronics",
        "rating": 4.7,
        "reviews": 186,
        "stock": 12,
        "emoji": "⌚",
        "description":
            "Smart watch with fitness tracking "
            "and notifications."
    },

    {
        "name": "Bluetooth Speaker",
        "image": "bluetooth spe.avif",
        "price": 1299,
        "old_price": 1799,
        "category": "Electronics",
        "rating": 4.6,
        "reviews": 154,
        "stock": 20,
        "emoji": "🔊",
        "description":
            "Portable Bluetooth speaker "
            "with powerful sound."
    },

    {
        "name": "Gaming Mouse",
        "image": "mouse.jpg",
        "price": 899,
        "old_price": 1299,
        "category": "Electronics",
        "rating": 4.5,
        "reviews": 98,
        "stock": 25,
        "emoji": "🖱️",
        "description":
            "High precision gaming mouse "
            "with comfortable grip."
    },

    {
        "name": "Mechanical Keyboard",
        "image": "keyboard.jpg",
        "price": 1899,
        "old_price": 2499,
        "category": "Electronics",
        "rating": 4.8,
        "reviews": 143,
        "stock": 18,
        "emoji": "⌨️",
        "description":
            "Mechanical keyboard suitable "
            "for gaming and programming."
    },

    {
        "name": "Power Bank",
        "image": "powerbank.jpg",
        "price": 999,
        "old_price": 1499,
        "category": "Electronics",
        "rating": 4.4,
        "reviews": 88,
        "stock": 30,
        "emoji": "🔋",
        "description":
            "Compact high-capacity power bank."
    },

    {
        "name": "Cotton T-Shirt",
        "image": "tshirt.webp",
        "price": 599,
        "old_price": 899,
        "category": "Fashion",
        "rating": 4.4,
        "reviews": 112,
        "stock": 40,
        "emoji": "👕",
        "description":
            "Soft and comfortable cotton T-shirt."
    },

    {
        "name": "Denim Pants",
        "image": "pant.webp",
        "price": 1299,
        "old_price": 1799,
        "category": "Fashion",
        "rating": 4.5,
        "reviews": 156,
        "stock": 25,
        "emoji": "👖",
        "description":
            "Classic denim pants with comfortable fit."
    },

    {
        "name": "Sports Shoes",
        "image": "shoe.jpg",
        "price": 1999,
        "old_price": 2999,
        "category": "Fashion",
        "rating": 4.7,
        "reviews": 201,
        "stock": 18,
        "emoji": "👟",
        "description":
            "Lightweight sports shoes "
            "for walking and running."
    },

    {
        "name": "Handbag",
        "image": "bag.avif",
        "price": 1599,
        "old_price": 2299,
        "category": "Fashion",
        "rating": 4.5,
        "reviews": 90,
        "stock": 14,
        "emoji": "👜",
        "description":
            "Stylish handbag with spacious compartments."
    },

    {
        "name": "Sunglasses",
        "image": "sunglass.webp",
        "price": 799,
        "old_price": 1199,
        "category": "Fashion",
        "rating": 4.3,
        "reviews": 75,
        "stock": 22,
        "emoji": "🕶️",
        "description":
            "Stylish lightweight sunglasses."
    },

    {
        "name": "Coffee Mug",
        "image": "mug.jpg",
        "price": 299,
        "old_price": 499,
        "category": "Home",
        "rating": 4.5,
        "reviews": 84,
        "stock": 50,
        "emoji": "☕",
        "description":
            "Elegant ceramic coffee mug."
    },

    {
        "name": "Table Lamp",
        "image": "lamp.jpg",
        "price": 899,
        "old_price": 1299,
        "category": "Home",
        "rating": 4.6,
        "reviews": 102,
        "stock": 20,
        "emoji": "💡",
        "description":
            "Modern table lamp for study and work."
    },

    {
        "name": "Plant Pot",
        "image": "pot.webp",
        "price": 349,
        "old_price": 499,
        "category": "Home",
        "rating": 4.4,
        "reviews": 70,
        "stock": 28,
        "emoji": "🪴",
        "description":
            "Decorative plant pot for home and office."
    },

    {
        "name": "Wall Clock",
        "image": "clock.jpg",
        "price": 699,
        "old_price": 999,
        "category": "Home",
        "rating": 4.5,
        "reviews": 91,
        "stock": 16,
        "emoji": "🕐",
        "description":
            "Modern wall clock with clean design."
    },

    {
        "name": "Cap",
        "image": "cap.webp",
        "price": 399,
        "old_price": 599,
        "category": "Fashion",
        "rating": 4.4,
        "reviews": 63,
        "stock": 25,
        "emoji": "🧢",
        "description":
            "Comfortable casual cap suitable "
            "for everyday use."
    }

]


# ============================================================
# LOGIN PAGE
# ============================================================

class LoginPage:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title(
            "ShopEase - Login"
        )

        self.root.geometry(
            "1150x720"
        )

        self.root.minsize(
            900,
            600
        )

        self.root.configure(
            bg=BG
        )

        self.password_visible = False

        self.build()


    def build(self):

        left = tk.Frame(
            self.root,
            bg=DARK,
            width=430
        )

        left.pack(
            side="left",
            fill="y"
        )

        left.pack_propagate(False)

        tk.Label(
            left,
            text="🛍️",
            font=("Segoe UI Emoji", 65),
            bg=DARK,
            fg=WHITE
        ).pack(
            pady=(75, 5)
        )

        tk.Label(
            left,
            text="ShopEase",
            font=("Segoe UI", 38, "bold"),
            bg=DARK,
            fg=WHITE
        ).pack()

        tk.Label(
            left,
            text="Everything you love.\nIn one place.",
            font=("Segoe UI", 15),
            bg=DARK,
            fg="#cbd5e1",
            justify="center"
        ).pack(
            pady=15
        )

        features = [
            "✓ Quality Products",
            "✓ Best Prices",
            "✓ Secure Shopping",
            "✓ Fast Delivery"
        ]

        for item in features:

            tk.Label(
                left,
                text=item,
                font=("Segoe UI", 11, "bold"),
                bg=DARK,
                fg="#93c5fd"
            ).pack(
                anchor="w",
                padx=100,
                pady=6
            )

        right = tk.Frame(
            self.root,
            bg=WHITE
        )

        right.pack(
            side="right",
            fill="both",
            expand=True
        )

        card = tk.Frame(
            right,
            bg=WHITE
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        tk.Label(
            card,
            text="Welcome Back!",
            font=("Segoe UI", 29, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack()

        tk.Label(
            card,
            text="Login to continue shopping",
            font=("Segoe UI", 10),
            bg=WHITE,
            fg=GRAY
        ).pack(
            pady=(5, 25)
        )

        tk.Label(
            card,
            text="Username",
            font=("Segoe UI", 10, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack(
            anchor="w"
        )

        user_box = tk.Frame(
            card,
            bg="#f8fafc",
            highlightbackground=BORDER,
            highlightthickness=1
        )

        user_box.pack(
            fill="x",
            pady=(5, 15)
        )

        tk.Label(
            user_box,
            text="👤",
            font=("Segoe UI Emoji", 12),
            bg="#f8fafc"
        ).pack(
            side="left",
            padx=10
        )

        self.username = tk.Entry(
            user_box,
            font=("Segoe UI", 11),
            bg="#f8fafc",
            fg=DARK,
            bd=0
        )

        self.username.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=10
        )

        self.username.bind(
            "<Return>",
            self.focus_password
        )

        tk.Label(
            card,
            text="Password",
            font=("Segoe UI", 10, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack(
            anchor="w"
        )

        password_box = tk.Frame(
            card,
            bg="#f8fafc",
            highlightbackground=BORDER,
            highlightthickness=1
        )

        password_box.pack(
            fill="x",
            pady=(5, 20)
        )

        tk.Label(
            password_box,
            text="🔑",
            font=("Segoe UI Emoji", 12),
            bg="#f8fafc"
        ).pack(
            side="left",
            padx=10
        )

        self.password = tk.Entry(
            password_box,
            font=("Segoe UI", 11),
            bg="#f8fafc",
            fg=DARK,
            bd=0,
            show="●"
        )

        self.password.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=10
        )

        tk.Button(
            password_box,
            text="👁",
            font=("Segoe UI Emoji", 10),
            bg="#f8fafc",
            relief="flat",
            bd=0,
            command=self.toggle_password
        ).pack(
            side="right",
            padx=8
        )

        self.password.bind(
            "<Return>",
            self.login_from_enter
        )

        tk.Button(
            card,
            text="LOGIN  →",
            font=("Segoe UI", 11, "bold"),
            bg=BLUE,
            fg=WHITE,
            activebackground=BLUE_DARK,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            width=30,
            pady=12,
            command=self.login
        ).pack()

        tk.Label(
            card,
            text="Press Enter after username and password",
            font=("Segoe UI", 8),
            bg=WHITE,
            fg=GRAY
        ).pack(
            pady=12
        )

        self.username.focus_set()


    def focus_password(self, event=None):

        self.password.focus_set()

        return "break"


    def login_from_enter(self, event=None):

        self.login()

        return "break"


    def toggle_password(self):

        self.password_visible = (
            not self.password_visible
        )

        self.password.configure(
            show=""
            if self.password_visible
            else "●"
        )


    def login(self):

        username = (
            self.username
            .get()
            .strip()
        )

        password = (
            self.password
            .get()
            .strip()
        )

        if not username:

            self.username.focus_set()

            return

        if not password:

            self.password.focus_set()

            return

        self.root.destroy()

        app = EcommerceApp(
            username
        )

        app.run()


# ============================================================
# ECOMMERCE APP
# ============================================================

class EcommerceApp:

    def __init__(
        self,
        username
    ):

        self.username = username

        data = get_user_data(
            username
        )

        self.cart = data.get(
            "cart",
            {}
        )

        self.wishlist = set(
            data.get(
                "wishlist",
                []
            )
        )

        self.orders = data.get(
            "orders",
            []
        )

        self.image_cache = {}

        self.current_canvas = None

        self.root = tk.Tk()

        self.root.title(
            f"ShopEase - {username}"
        )

        self.root.geometry(
            "1280x820"
        )

        self.root.minsize(
            950,
            620
        )

        self.root.configure(
            bg=BG
        )

        self.build_header()

        self.content = tk.Frame(
            self.root,
            bg=BG
        )

        self.content.pack(
            fill="both",
            expand=True
        )

        self.build_navigation()

        self.root.bind_all(
            "<MouseWheel>",
            self.mouse_wheel
        )

        self.root.bind_all(
            "<Button-4>",
            self.mouse_wheel_linux
        )

        self.root.bind_all(
            "<Button-5>",
            self.mouse_wheel_linux
        )

        self.show_home()


    # ========================================================
    # SAVE
    # ========================================================

    def save_user_data(self):

        USER_DATA[
            self.username
        ] = {
            "cart": self.cart,
            "wishlist": list(
                self.wishlist
            ),
            "orders": self.orders
        }

        save_all_user_data()


    # ========================================================
    # HEADER
    # ========================================================

    def build_header(self):

        header = tk.Frame(
            self.root,
            bg=DARK,
            height=70
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        tk.Label(
            header,
            text="🛍️ ShopEase",
            font=("Segoe UI", 23, "bold"),
            bg=DARK,
            fg=WHITE
        ).pack(
            side="left",
            padx=25
        )

        tk.Label(
            header,
            text=f"Welcome, {self.username} 👋",
            font=("Segoe UI", 10, "bold"),
            bg=DARK,
            fg="#cbd5e1"
        ).pack(
            side="right",
            padx=25
        )


    # ========================================================
    # NAVIGATION
    # ========================================================

    def build_navigation(self):

        nav = tk.Frame(
            self.root,
            bg=WHITE,
            height=78
        )

        nav.pack(
            side="bottom",
            fill="x"
        )

        nav.pack_propagate(False)

        tk.Frame(
            nav,
            bg=BORDER,
            height=1
        ).pack(
            fill="x"
        )

        buttons = [

            (
                "home",
                "⌂",
                "Home",
                BLUE,
                self.show_home
            ),

            (
                "wishlist",
                "♥",
                "Wishlist",
                PINK,
                self.show_wishlist
            ),

            (
                "cart",
                "🛒",
                "Cart",
                BLUE,
                self.show_cart
            ),

            (
                "orders",
                "📦",
                "Orders",
                GREEN,
                self.show_orders
            ),

            (
                "checkout",
                "💳",
                "Checkout",
                ORANGE,
                self.show_checkout
            ),

            (
                "logout",
                "↪",
                "Logout",
                RED,
                self.logout
            )
        ]

        self.nav_buttons = {}

        for (
            name,
            icon,
            text,
            color,
            command
        ) in buttons:

            holder = tk.Frame(
                nav,
                bg=WHITE
            )

            holder.pack(
                side="left",
                fill="both",
                expand=True,
                padx=3,
                pady=5
            )

            button = tk.Button(
                holder,
                text=f"{icon}\n{text}",
                font=("Segoe UI", 9, "bold"),
                bg=WHITE,
                fg=GRAY,
                activebackground=WHITE,
                relief="flat",
                bd=0,
                cursor="hand2",
                command=command
            )

            button.pack(
                fill="both",
                expand=True
            )

            self.nav_buttons[
                name
            ] = (
                holder,
                button,
                color
            )

        self.update_navigation()


    def update_navigation(self):

        cart_count = sum(
            self.cart.values()
        )

        wishlist_count = len(
            self.wishlist
        )

        order_count = len(
            self.orders
        )

        self.nav_buttons[
            "cart"
        ][1].configure(
            text=f"🛒\nCart ({cart_count})"
        )

        self.nav_buttons[
            "wishlist"
        ][1].configure(
            text=f"♥\nWishlist ({wishlist_count})"
        )

        self.nav_buttons[
            "orders"
        ][1].configure(
            text=f"📦\nOrders ({order_count})"
        )


    def set_active(self, name):

        for (
            key,
            (
                holder,
                button,
                color
            )
        ) in self.nav_buttons.items():

            if key == name:

                holder.configure(
                    bg=BLUE_LIGHT
                )

                button.configure(
                    bg=BLUE_LIGHT,
                    fg=color
                )

            else:

                holder.configure(
                    bg=WHITE
                )

                button.configure(
                    bg=WHITE,
                    fg=GRAY
                )


    # ========================================================
    # CLEAR CONTENT
    # ========================================================

    def clear_content(self):

        self.current_canvas = None

        for widget in (
            self.content.winfo_children()
        ):

            widget.destroy()


    # ========================================================
    # SCROLL AREA
    # ========================================================

    def create_scroll_area(self):

        outer = tk.Frame(
            self.content,
            bg=BG
        )

        outer.pack(
            fill="both",
            expand=True,
            padx=22,
            pady=5
        )

        canvas = tk.Canvas(
            outer,
            bg=BG,
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            outer,
            orient="vertical",
            width=16,
            command=canvas.yview
        )

        frame = tk.Frame(
            canvas,
            bg=BG
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        window = canvas.create_window(
            (0, 0),
            window=frame,
            anchor="nw"
        )

        self.current_canvas = canvas

        frame.bind(
            "<Configure>",
            lambda event:
            canvas.configure(
                scrollregion=canvas.bbox(
                    "all"
                )
            )
        )

        canvas.bind(
            "<Configure>",
            lambda event:
            canvas.itemconfigure(
                window,
                width=event.width
            )
        )

        return canvas, frame


    # ========================================================
    # MOUSE SCROLL
    # ========================================================

    def mouse_wheel(
        self,
        event
    ):

        if self.current_canvas:

            self.current_canvas.yview_scroll(
                int(-event.delta / 120),
                "units"
            )


    def mouse_wheel_linux(
        self,
        event
    ):

        if not self.current_canvas:

            return

        if event.num == 4:

            self.current_canvas.yview_scroll(
                -3,
                "units"
            )

        elif event.num == 5:

            self.current_canvas.yview_scroll(
                3,
                "units"
            )


    # ========================================================
    # IMAGE LOADING
    # ========================================================

    def load_product_image(
        self,
        filename,
        size=(230, 170)
    ):

        path = os.path.join(
            IMAGE_DIR,
            filename
        )

        if not os.path.exists(path):

            print(
                "❌ IMAGE NOT FOUND:",
                filename
            )

            return None

        key = (
            filename,
            size
        )

        if key in self.image_cache:

            return self.image_cache[key]

        try:

            image = Image.open(path)

            image = image.convert(
                "RGB"
            )

            image.thumbnail(
                size,
                Image.Resampling.LANCZOS
            )

            photo = ImageTk.PhotoImage(
                image
            )

            self.image_cache[key] = photo

            print(
                "✅ IMAGE LOADED:",
                filename
            )

            return photo

        except Exception as error:

            print(
                "❌ IMAGE ERROR:",
                filename,
                error
            )

            return None


    # ========================================================
    # HOME
    # ========================================================

    def show_home(self):

        self.clear_content()

        self.set_active(
            "home"
        )

        top = tk.Frame(
            self.content,
            bg=BG
        )

        top.pack(
            fill="x",
            padx=28,
            pady=12
        )

        tk.Label(
            top,
            text="Discover Products",
            font=("Segoe UI", 25, "bold"),
            bg=BG,
            fg=DARK
        ).pack(
            side="left"
        )

        search_var = tk.StringVar()

        search_box = tk.Frame(
            top,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        search_box.pack(
            side="right"
        )

        tk.Label(
            search_box,
            text="🔍",
            bg=WHITE
        ).pack(
            side="left",
            padx=8
        )

        search = tk.Entry(
            search_box,
            textvariable=search_var,
            font=("Segoe UI", 10),
            width=25,
            bd=0
        )

        search.pack(
            side="left",
            ipady=9
        )

        banner = tk.Frame(
            self.content,
            bg=BLUE,
            height=110
        )

        banner.pack(
            fill="x",
            padx=28,
            pady=5
        )

        banner.pack_propagate(False)

        tk.Label(
            banner,
            text="🔥 MEGA SHOPPING SALE",
            font=("Segoe UI", 20, "bold"),
            bg=BLUE,
            fg=WHITE
        ).pack(
            anchor="w",
            padx=25,
            pady=(15, 2)
        )

        tk.Label(
            banner,
            text="Great products • Great prices • Fast delivery",
            font=("Segoe UI", 10),
            bg=BLUE,
            fg="#dbeafe"
        ).pack(
            anchor="w",
            padx=25
        )

        category_var = tk.StringVar(
            value="All"
        )

        category_row = tk.Frame(
            self.content,
            bg=BG
        )

        category_row.pack(
            fill="x",
            padx=28,
            pady=7
        )

        canvas, frame = (
            self.create_scroll_area()
        )

        for c in range(3):

            frame.grid_columnconfigure(
                c,
                weight=1
            )

        def refresh():

            for widget in (
                frame.winfo_children()
            ):

                widget.destroy()

            query = (
                search_var
                .get()
                .strip()
                .lower()
            )

            category = (
                category_var.get()
            )

            filtered = []

            for product in PRODUCTS:

                if (
                    category != "All"
                    and product["category"]
                    != category
                ):
                    continue

                if (
                    query
                    and query
                    not in product["name"].lower()
                ):
                    continue

                filtered.append(
                    product
                )

            for i, product in enumerate(
                filtered
            ):

                self.create_product_card(
                    frame,
                    product,
                    i // 3,
                    i % 3
                )

        categories = [
            ("All", "🛍️", BLUE),
            ("Electronics", "💻", BLUE),
            ("Fashion", "👕", PURPLE),
            ("Home", "🏠", GREEN)
        ]

        for name, icon, color in categories:

            tk.Button(
                category_row,
                text=f"{icon} {name}",
                font=("Segoe UI", 9, "bold"),
                bg=WHITE,
                fg=color,
                relief="flat",
                bd=0,
                cursor="hand2",
                padx=14,
                pady=8,
                command=lambda n=name:
                (
                    category_var.set(n),
                    refresh()
                )
            ).pack(
                side="left",
                padx=3
            )

        search_var.trace_add(
            "write",
            lambda *args:
            refresh()
        )

        refresh()


    # ========================================================
    # PRODUCT CARD
    # ========================================================

    def create_product_card(
        self,
        parent,
        product,
        row,
        column
    ):

        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=7,
            pady=7
        )

        image_box = tk.Frame(
            card,
            bg="#f8fafc",
            height=175
        )

        image_box.pack(
            fill="x"
        )

        image_box.pack_propagate(False)

        photo = self.load_product_image(
            product["image"]
        )

        if photo:

            image_label = tk.Label(
                image_box,
                image=photo,
                bg="#f8fafc"
            )

            image_label.image = photo

            image_label.pack(
                expand=True
            )

        else:

            tk.Label(
                image_box,
                text=product["emoji"],
                font=("Segoe UI Emoji", 60),
                bg="#f8fafc"
            ).pack(
                expand=True
            )

        discount = round(
            (
                1
                - product["price"]
                / product["old_price"]
            ) * 100
        )

        tk.Label(
            image_box,
            text=f"{discount}% OFF",
            font=("Segoe UI", 8, "bold"),
            bg=RED,
            fg=WHITE,
            padx=6,
            pady=3
        ).place(
            x=9,
            y=9
        )

        heart = (
            "♥"
            if product["name"]
            in self.wishlist
            else "♡"
        )

        tk.Button(
            image_box,
            text=heart,
            font=("Segoe UI", 17, "bold"),
            bg=PINK_LIGHT,
            fg=PINK,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda p=product:
            self.toggle_wishlist(p)
        ).place(
            relx=0.90,
            y=7,
            anchor="n"
        )

        info = tk.Frame(
            card,
            bg=WHITE
        )

        info.pack(
            fill="x",
            padx=13,
            pady=11
        )

        tk.Label(
            info,
            text=product["name"],
            font=("Segoe UI", 12, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack(
            anchor="w"
        )

        tk.Label(
            info,
            text=(
                f"⭐ {product['rating']} "
                f"({product['reviews']})"
            ),
            font=("Segoe UI", 8),
            bg=WHITE,
            fg=GRAY
        ).pack(
            anchor="w",
            pady=3
        )

        tk.Label(
            info,
            text=self.money(
                product["price"]
            ),
            font=("Segoe UI", 14, "bold"),
            bg=WHITE,
            fg=GREEN
        ).pack(
            anchor="w"
        )

        row_frame = tk.Frame(
            info,
            bg=WHITE
        )

        row_frame.pack(
            fill="x",
            pady=6
        )

        tk.Button(
            row_frame,
            text="View",
            font=("Segoe UI", 8, "bold"),
            bg=BLUE_LIGHT,
            fg=BLUE,
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=7,
            command=lambda p=product:
            self.show_product_details(p)
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 3)
        )

        tk.Button(
            row_frame,
            text="🛒 Add",
            font=("Segoe UI", 8, "bold"),
            bg=BLUE,
            fg=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=7,
            command=lambda p=product:
            self.add_to_cart(p)
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(3, 0)
        )


    # ========================================================
    # PRODUCT DETAILS
    # ========================================================

    def show_product_details(
        self,
        product
    ):

        popup = tk.Toplevel(
            self.root
        )

        popup.title(
            product["name"]
        )

        popup.geometry(
            "650x560"
        )

        popup.configure(
            bg=WHITE
        )

        photo = self.load_product_image(
            product["image"],
            (300, 230)
        )

        if photo:

            label = tk.Label(
                popup,
                image=photo,
                bg=WHITE
            )

            label.image = photo

            label.pack(
                pady=15
            )

        else:

            tk.Label(
                popup,
                text=product["emoji"],
                font=("Segoe UI Emoji", 80),
                bg=WHITE
            ).pack(
                pady=15
            )

        tk.Label(
            popup,
            text=product["name"],
            font=("Segoe UI", 22, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack()

        tk.Label(
            popup,
            text=self.money(
                product["price"]
            ),
            font=("Segoe UI", 20, "bold"),
            bg=WHITE,
            fg=GREEN
        ).pack(
            pady=5
        )

        tk.Label(
            popup,
            text=product["description"],
            font=("Segoe UI", 10),
            bg=WHITE,
            fg=TEXT,
            wraplength=520
        ).pack(
            padx=30,
            pady=10
        )

        tk.Button(
            popup,
            text="🛒 ADD TO CART",
            font=("Segoe UI", 11, "bold"),
            bg=BLUE,
            fg=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=30,
            pady=12,
            command=lambda:
            (
                self.add_to_cart(product),
                popup.destroy()
            )
        ).pack(
            pady=15
        )


    # ========================================================
    # CART
    # ========================================================

    def add_to_cart(
        self,
        product
    ):

        name = product["name"]

        current = self.cart.get(
            name,
            0
        )

        if current >= product["stock"]:

            self.toast(
                "Maximum stock reached"
            )

            return

        self.cart[name] = (
            current + 1
        )

        self.save_user_data()

        self.update_navigation()

        self.toast(
            "✓ Added to cart"
        )


    def show_cart(self):

        self.clear_content()

        self.set_active(
            "cart"
        )

        tk.Label(
            self.content,
            text="🛒  Shopping Cart",
            font=("Segoe UI", 26, "bold"),
            bg=BG,
            fg=DARK
        ).pack(
            anchor="w",
            padx=28,
            pady=15
        )

        if not self.cart:

            tk.Label(
                self.content,
                text="🛒",
                font=("Segoe UI Emoji", 60),
                bg=BG
            ).pack(
                pady=(70, 5)
            )

            tk.Label(
                self.content,
                text="Your cart is empty",
                font=("Segoe UI", 18, "bold"),
                bg=BG,
                fg=GRAY
            ).pack()

            return

        canvas, frame = (
            self.create_scroll_area()
        )

        for name, quantity in list(
            self.cart.items()
        ):

            product = self.find_product(
                name
            )

            if product:

                self.create_cart_item(
                    frame,
                    product,
                    quantity
                )

        summary = tk.Frame(
            self.content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        summary.pack(
            fill="x",
            padx=22,
            pady=6
        )

        tk.Label(
            summary,
            text=(
                f"TOTAL: "
                f"{self.money(self.total())}"
            ),
            font=("Segoe UI", 20, "bold"),
            bg=WHITE,
            fg=GREEN
        ).pack(
            side="left",
            padx=18,
            pady=12
        )

        tk.Button(
            summary,
            text="💳 Checkout →",
            font=("Segoe UI", 11, "bold"),
            bg=ORANGE,
            fg=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=25,
            pady=10,
            command=self.show_checkout
        ).pack(
            side="right",
            padx=18,
            pady=8
        )


    def create_cart_item(
        self,
        parent,
        product,
        quantity
    ):

        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            padx=7,
            pady=6
        )

        photo = self.load_product_image(
            product["image"],
            (110, 85)
        )

        if photo:

            label = tk.Label(
                card,
                image=photo,
                bg=WHITE
            )

            label.image = photo

            label.pack(
                side="left",
                padx=15
            )

        else:

            tk.Label(
                card,
                text=product["emoji"],
                font=("Segoe UI Emoji", 40),
                bg=WHITE
            ).pack(
                side="left",
                padx=15
            )

        info = tk.Frame(
            card,
            bg=WHITE
        )

        info.pack(
            side="left",
            fill="x",
            expand=True
        )

        tk.Label(
            info,
            text=product["name"],
            font=("Segoe UI", 12, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack(
            anchor="w"
        )

        tk.Label(
            info,
            text=self.money(
                product["price"]
            ),
            font=("Segoe UI", 9),
            bg=WHITE,
            fg=GRAY
        ).pack(
            anchor="w"
        )

        quantity_box = tk.Frame(
            card,
            bg=WHITE
        )

        quantity_box.pack(
            side="right",
            padx=15
        )

        tk.Button(
            quantity_box,
            text="−",
            font=("Segoe UI", 12, "bold"),
            bg=RED_LIGHT,
            fg=RED,
            relief="flat",
            bd=0,
            width=3,
            command=lambda n=product["name"]:
            self.change_quantity(
                n,
                -1
            )
        ).pack(
            side="left"
        )

        tk.Label(
            quantity_box,
            text=str(quantity),
            font=("Segoe UI", 10, "bold"),
            bg=WHITE,
            width=4
        ).pack(
            side="left"
        )

        tk.Button(
            quantity_box,
            text="+",
            font=("Segoe UI", 12, "bold"),
            bg=GREEN_LIGHT,
            fg=GREEN,
            relief="flat",
            bd=0,
            width=3,
            command=lambda n=product["name"]:
            self.change_quantity(
                n,
                1
            )
        ).pack(
            side="left"
        )


    def change_quantity(
        self,
        name,
        amount
    ):

        product = self.find_product(
            name
        )

        if not product:
            return

        new_quantity = (
            self.cart.get(
                name,
                0
            )
            + amount
        )

        if new_quantity <= 0:

            self.cart.pop(
                name,
                None
            )

        elif new_quantity <= product["stock"]:

            self.cart[name] = (
                new_quantity
            )

        else:

            self.toast(
                "Maximum stock reached"
            )

            return

        self.save_user_data()

        self.update_navigation()

        self.show_cart()


    # ========================================================
    # WISHLIST
    # ========================================================

    def toggle_wishlist(
        self,
        product
    ):

        name = product["name"]

        if name in self.wishlist:

            self.wishlist.remove(
                name
            )

            self.toast(
                "Removed from wishlist"
            )

        else:

            self.wishlist.add(
                name
            )

            self.toast(
                "♥ Added to wishlist"
            )

        self.save_user_data()

        self.update_navigation()


    def show_wishlist(self):

        self.clear_content()

        self.set_active(
            "wishlist"
        )

        tk.Label(
            self.content,
            text="♥  My Wishlist",
            font=("Segoe UI", 26, "bold"),
            bg=BG,
            fg=DARK
        ).pack(
            anchor="w",
            padx=28,
            pady=15
        )

        if not self.wishlist:

            tk.Label(
                self.content,
                text="♡",
                font=("Segoe UI", 70),
                bg=BG,
                fg=PINK
            ).pack(
                pady=(70, 5)
            )

            tk.Label(
                self.content,
                text="Your wishlist is empty",
                font=("Segoe UI", 18, "bold"),
                bg=BG,
                fg=GRAY
            ).pack()

            return

        canvas, frame = (
            self.create_scroll_area()
        )

        for c in range(3):

            frame.grid_columnconfigure(
                c,
                weight=1
            )

        for i, name in enumerate(
            list(self.wishlist)
        ):

            product = self.find_product(
                name
            )

            if product:

                self.create_product_card(
                    frame,
                    product,
                    i // 3,
                    i % 3
                )


    # ========================================================
    # CHECKOUT
    # ========================================================

    def show_checkout(self):

        self.clear_content()

        self.set_active(
            "checkout"
        )

        tk.Label(
            self.content,
            text="💳  Checkout",
            font=("Segoe UI", 26, "bold"),
            bg=BG,
            fg=DARK
        ).pack(
            anchor="w",
            padx=28,
            pady=15
        )

        if not self.cart:

            tk.Label(
                self.content,
                text="Your cart is empty.",
                font=("Segoe UI", 18, "bold"),
                bg=BG,
                fg=GRAY
            ).pack(
                pady=100
            )

            return

        canvas, frame = (
            self.create_scroll_area()
        )

        address_box = tk.Frame(
            frame,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        address_box.pack(
            fill="x",
            padx=7,
            pady=6
        )

        tk.Label(
            address_box,
            text="📍 Delivery Address",
            font=("Segoe UI", 15, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack(
            anchor="w",
            padx=18,
            pady=11
        )

        address = tk.Text(
            address_box,
            height=4,
            font=("Segoe UI", 10),
            bg="#f8fafc",
            relief="flat",
            highlightbackground=BORDER,
            highlightthickness=1
        )

        address.pack(
            fill="x",
            padx=18,
            pady=(0, 15)
        )

        payment_box = tk.Frame(
            frame,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        payment_box.pack(
            fill="x",
            padx=7,
            pady=6
        )

        tk.Label(
            payment_box,
            text="💳 Payment Method",
            font=("Segoe UI", 15, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack(
            anchor="w",
            padx=18,
            pady=10
        )

        payment = tk.StringVar(
            value="Cash on Delivery"
        )

        for option in [
            "Cash on Delivery",
            "UPI",
            "Credit / Debit Card"
        ]:

            tk.Radiobutton(
                payment_box,
                text=option,
                variable=payment,
                value=option,
                font=("Segoe UI", 10),
                bg=WHITE,
                activebackground=WHITE,
                selectcolor=WHITE
            ).pack(
                anchor="w",
                padx=18,
                pady=3
            )

        summary = tk.Frame(
            frame,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        summary.pack(
            fill="x",
            padx=7,
            pady=6
        )

        tk.Label(
            summary,
            text="Order Summary",
            font=("Segoe UI", 17, "bold"),
            bg=WHITE,
            fg=DARK
        ).pack(
            anchor="w",
            padx=18,
            pady=11
        )

        for name, quantity in self.cart.items():

            product = self.find_product(
                name
            )

            if product:

                tk.Label(
                    summary,
                    text=(
                        f"{product['emoji']} "
                        f"{name} × {quantity}"
                    ),
                    font=("Segoe UI", 10),
                    bg=WHITE,
                    fg=TEXT
                ).pack(
                    anchor="w",
                    padx=18,
                    pady=2
                )

        tk.Label(
            summary,
            text=f"TOTAL: {self.money(self.total())}",
            font=("Segoe UI", 22, "bold"),
            bg=WHITE,
            fg=GREEN
        ).pack(
            anchor="e",
            padx=18,
            pady=15
        )

        def place_order():

            entered_address = (
                address.get(
                    "1.0",
                    "end"
                ).strip()
            )

            if not entered_address:

                messagebox.showwarning(
                    "Address Required",
                    "Please enter delivery address."
                )

                return

            order = {

                "id":
                    "SE"
                    + datetime.now().strftime(
                        "%Y%m%d%H%M%S"
                    ),

                "date":
                    datetime.now().strftime(
                        "%d-%m-%Y %I:%M %p"
                    ),

                "items": [],

                "total":
                    self.total(),

                "payment":
                    payment.get(),

                "address":
                    entered_address,

                "status":
                    "Order Placed"
            }

            for name, quantity in (
                self.cart.items()
            ):

                product = self.find_product(
                    name
                )

                if product:

                    order["items"].append(
                        {
                            "name": name,
                            "quantity": quantity,
                            "emoji": product["emoji"],
                            "price": product["price"]
                        }
                    )

            self.orders.append(
                order
            )

            self.cart.clear()

            # SAVE IMMEDIATELY
            self.save_user_data()

            self.update_navigation()

            messagebox.showinfo(
                "Order Successful",
                "Your order has been placed successfully!"
            )

            self.show_orders()

        tk.Button(
            frame,
            text="PLACE ORDER  ✓",
            font=("Segoe UI", 12, "bold"),
            bg=GREEN,
            fg=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=45,
            pady=13,
            command=place_order
        ).pack(
            pady=20
        )


    # ========================================================
    # ORDERS
    # ========================================================

    def show_orders(self):

        self.clear_content()

        self.set_active(
            "orders"
        )

        tk.Label(
            self.content,
            text="📦  My Orders",
            font=("Segoe UI", 26, "bold"),
            bg=BG,
            fg=DARK
        ).pack(
            anchor="w",
            padx=28,
            pady=15
        )

        if not self.orders:

            tk.Label(
                self.content,
                text="📦",
                font=("Segoe UI Emoji", 60),
                bg=BG
            ).pack(
                pady=(60, 5)
            )

            tk.Label(
                self.content,
                text="No orders yet",
                font=("Segoe UI", 18, "bold"),
                bg=BG,
                fg=GRAY
            ).pack()

            tk.Label(
                self.content,
                text="Your completed orders will appear here.",
                font=("Segoe UI", 10),
                bg=BG,
                fg=GRAY
            ).pack(
                pady=5
            )

            return

        canvas, frame = (
            self.create_scroll_area()
        )

        for order in reversed(
            self.orders
        ):

            self.create_order_card(
                frame,
                order
            )


    def create_order_card(
        self,
        parent,
        order
    ):

        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            padx=7,
            pady=8
        )

        top = tk.Frame(
            card,
            bg=WHITE
        )

        top.pack(
            fill="x",
            padx=18,
            pady=12
        )

        tk.Label(
            top,
            text=f"ORDER #{order.get('id', 'N/A')}",
            font=("Segoe UI", 12, "bold"),
            bg=WHITE,
            fg=BLUE
        ).pack(
            side="left"
        )

        tk.Label(
            top,
            text=order.get(
                "date",
                "Date unavailable"
            ),
            font=("Segoe UI", 9),
            bg=WHITE,
            fg=GRAY
        ).pack(
            side="right"
        )

        tk.Frame(
            card,
            bg=BORDER,
            height=1
        ).pack(
            fill="x"
        )

        tk.Label(
            card,
            text="PRODUCTS",
            font=("Segoe UI", 9, "bold"),
            bg=WHITE,
            fg=GRAY
        ).pack(
            anchor="w",
            padx=18,
            pady=(12, 5)
        )

        items = order.get(
            "items",
            []
        )

        for item in items:

            item_frame = tk.Frame(
                card,
                bg="#f8fafc"
            )

            item_frame.pack(
                fill="x",
                padx=18,
                pady=3
            )

            emoji = item.get(
                "emoji",
                "🛍️"
            )

            name = item.get(
                "name",
                "Product"
            )

            quantity = item.get(
                "quantity",
                1
            )

            price = item.get(
                "price",
                0
            )

            tk.Label(
                item_frame,
                text=emoji,
                font=("Segoe UI Emoji", 16),
                bg="#f8fafc"
            ).pack(
                side="left",
                padx=8,
                pady=6
            )

            tk.Label(
                item_frame,
                text=f"{name} × {quantity}",
                font=("Segoe UI", 10, "bold"),
                bg="#f8fafc",
                fg=DARK
            ).pack(
                side="left"
            )

            tk.Label(
                item_frame,
                text=self.money(
                    price * quantity
                ),
                font=("Segoe UI", 10, "bold"),
                bg="#f8fafc",
                fg=GREEN
            ).pack(
                side="right",
                padx=10
            )

        details = tk.Frame(
            card,
            bg=WHITE
        )

        details.pack(
            fill="x",
            padx=18,
            pady=12
        )

        payment = order.get(
            "payment",
            "Not specified"
        )

        address = order.get(
            "address",
            "Not specified"
        )

        status = order.get(
            "status",
            "Order Placed"
        )

        tk.Label(
            details,
            text=f"💳 {payment}",
            font=("Segoe UI", 9),
            bg=WHITE,
            fg=TEXT
        ).pack(
            anchor="w",
            pady=2
        )

        tk.Label(
            details,
            text=f"📍 {address}",
            font=("Segoe UI", 9),
            bg=WHITE,
            fg=TEXT,
            wraplength=800,
            justify="left"
        ).pack(
            anchor="w",
            pady=2
        )

        tk.Label(
            details,
            text=f"✓ {status}",
            font=("Segoe UI", 9, "bold"),
            bg=WHITE,
            fg=GREEN
        ).pack(
            anchor="w",
            pady=2
        )

        bottom = tk.Frame(
            card,
            bg=WHITE
        )

        bottom.pack(
            fill="x",
            padx=18,
            pady=(2, 15)
        )

        tk.Label(
            bottom,
            text="ORDER TOTAL",
            font=("Segoe UI", 9, "bold"),
            bg=WHITE,
            fg=GRAY
        ).pack(
            side="left"
        )

        tk.Label(
            bottom,
            text=self.money(
                order.get(
                    "total",
                    0
                )
            ),
            font=("Segoe UI", 17, "bold"),
            bg=WHITE,
            fg=GREEN
        ).pack(
            side="right"
        )


    # ========================================================
    # HELPERS
    # ========================================================

    def find_product(
        self,
        name
    ):

        for product in PRODUCTS:

            if product["name"] == name:

                return product

        return None


    def money(
        self,
        amount
    ):

        try:

            return f"₹{float(amount):,.0f}"

        except:

            return "₹0"


    def subtotal(self):

        total = 0

        for name, quantity in (
            self.cart.items()
        ):

            product = self.find_product(
                name
            )

            if product:

                total += (
                    product["price"]
                    * quantity
                )

        return total


    def delivery(self):

        if self.subtotal() == 0:

            return 0

        if self.subtotal() >= 1000:

            return 0

        return 49


    def total(self):

        return (
            self.subtotal()
            + self.delivery()
        )


    def toast(
        self,
        text
    ):

        popup = tk.Label(
            self.root,
            text=text,
            font=("Segoe UI", 10, "bold"),
            bg=DARK,
            fg=WHITE,
            padx=20,
            pady=10
        )

        popup.place(
            relx=0.5,
            rely=0.85,
            anchor="center"
        )

        self.root.after(
            1500,
            popup.destroy
        )


    # ========================================================
    # LOGOUT
    # ========================================================

    def logout(self):

        answer = messagebox.askyesno(
            "Logout",
            "Logout from this account?"
        )

        if not answer:

            return

        # SAVE EVERYTHING BEFORE LOGOUT
        self.save_user_data()

        self.root.destroy()

        login = LoginPage()

        login.root.mainloop()


    # ========================================================
    # RUN
    # ========================================================

    def run(self):

        self.root.mainloop()


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    # LOAD PREVIOUS USERS
    load_user_data()

    login = LoginPage()

    login.root.mainloop()