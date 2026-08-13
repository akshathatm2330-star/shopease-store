# ShopEase Flask Ecommerce

## Features
- Login / automatic account creation
- 18 products with JPG, WEBP and AVIF images
- Search and category filtering
- Wishlist
- Persistent cart
- Checkout
- Persistent order history
- SQLite database
- Responsive browser UI

## Run locally

Open PowerShell in this folder:

```powershell
python -m pip install -r requirements.txt
python app.py
```

Open:

http://127.0.0.1:5000

The first time a username is used, an account is created automatically.

## Images

Copy your exact 18 images into:

static/images/

## Important

`shopease.db` is created automatically. Do not delete it if you want to keep customer accounts, carts, wishlists and orders.

Before public deployment, set a strong `SECRET_KEY` environment variable and turn debug off.
