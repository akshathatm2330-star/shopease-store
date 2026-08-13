#Create product list
products = {
    1: {"name": "Laptop", "price": 55000},
    2: {"name": "Smartphone", "price": 25000},
    3: {"name": "Headphones", "price": 2000},
    4: {"name": "Keyboard", "price": 1200},
    5: {"name": "Mouse", "price": 700}
}

cart = {}


#Display products
def display_products():
    print("\n===== PRODUCTS =====")

    for product_id, product in products.items():
        print(product_id, product["name"], "₹", product["price"])

#Add product to cart
def add_to_cart():
    display_products()

    product_id = int(input("\nEnter product number: "))
    quantity = int(input("Enter quantity: "))

    if product_id in products:
        if product_id in cart:
            cart[product_id] += quantity
        else:
            cart[product_id] = quantity

        print("Product added to cart.")
    else:
        print("Invalid product.")

#View cart
def view_cart():
    print("\n===== YOUR CART =====")

    if not cart:
        print("Cart is empty.")
        return

    total = 0

    for product_id, quantity in cart.items():
        product = products[product_id]
        price = product["price"] * quantity
        total += price

        print(product["name"], "x", quantity, "=", "₹", price)

    print("--------------------")
    print("Total = ₹", total)

#Remove product
def remove_from_cart():
    view_cart()

    if not cart:
        return

    product_id = int(input("\nEnter product number to remove: "))

    if product_id in cart:
        del cart[product_id]
        print("Product removed from cart.")
    else:
        print("Product not found in cart.")

#Checkout
def checkout():
    if not cart:
        print("\nYour cart is empty.")
        return

    print("\n===== BILL =====")

    total = 0

    for product_id, quantity in cart.items():
        product = products[product_id]
        price = product["price"] * quantity
        total += price

        print(product["name"], "x", quantity, "=", "₹", price)

    print("--------------------")
    print("Total Amount = ₹", total)

    name = input("Enter your name: ")
    address = input("Enter your address: ")

    print("\nOrder placed successfully!")
    print("Customer:", name)
    print("Address:", address)
    print("Amount Paid: ₹", total)

    cart.clear()

#Create the main menu
while True:
    print("\n===== E-COMMERCE SHOPPING =====")
    print("1. Display Products")
    print("2. Add to Cart")
    print("3. View Cart")
    print("4. Remove from Cart")
    print("5. Checkout")
    print("6. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        display_products()

    elif choice == 2:
        add_to_cart()

    elif choice == 3:
        view_cart()

    elif choice == 4:
        remove_from_cart()

    elif choice == 5:
        checkout()

    elif choice == 6:
        print("Thank you for shopping!")
        break

    else:
        print("Invalid choice.")
        