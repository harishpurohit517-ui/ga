
from flask import Flask, request, redirect, url_for, render_template_string, send_from_directory, session
from pathlib import Path
from datetime import datetime
import json
import os
import secrets
import requests

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()

# Configure these environment variables before deployment.
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
RESEND_TO_EMAIL = os.environ.get("RESEND_TO_EMAIL", "")
RESEND_FROM_EMAIL = os.environ.get(
    "RESEND_FROM_EMAIL",
    "Gajanand Telecom <onboarding@resend.dev>"
)
RESEND_API_URL = "https://api.resend.com/emails"

app.secret_key = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)

PRODUCTS = [
    {"id": 1, "name": "U&i Earbuds", "category": "Audio", "image": "earbuds.jfif"},
    {"id": 2, "name": "U&i Neckband", "category": "Audio", "image": "neckband.jfif"},
    {"id": 3, "name": "U&i Headphones", "category": "Audio", "image": "headphones.jfif"},
    {"id": 4, "name": "U&i Speaker", "category": "Audio", "image": "speaker.jfif"},
    {"id": 5, "name": "U&i Smartwatch", "category": "Wearables", "image": "smartwatch.jfif"},
    {"id": 6, "name": "U&i Charger", "category": "Charging", "image": "charger.jfif"},
    {"id": 7, "name": "U&i Charging Cable", "category": "Charging", "image": "cable.jfif"},
    {"id": 8, "name": "U&i Power Bank", "category": "Charging", "image": "powerbank.jfif"},
]

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Gajanand Telecom | U&i Products</title>
<style>
:root {
    --yellow: #F5CD28;
    --black: #151515;
    --white: #ffffff;
    --muted: #666666;
}
* { box-sizing: border-box; }
body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background: var(--yellow);
    color: var(--black);
}
header {
    background: var(--black);
    color: white;
    padding: 16px 5%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 15px;
    flex-wrap: wrap;
}
.brand { font-size: 27px; font-weight: 900; letter-spacing: .5px; }
.brand span { color: var(--yellow); }
nav { display: flex; align-items: center; gap: 18px; flex-wrap: wrap; }
nav a { color: white; text-decoration: none; font-weight: bold; }
nav a:hover { color: var(--yellow); }
.hero {
    margin: 22px auto;
    width: 92%;
    min-height: 310px;
    border-radius: 18px;
    overflow: hidden;
    position: relative;
    display: flex;
    align-items: center;
    background: #222;
    color: white;
}
.hero::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image: url("/image/theme.jfif");
    background-size: cover;
    background-position: center;
    opacity: .72;
}
.hero::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, rgba(0,0,0,.82), rgba(0,0,0,.18));
}
.hero-content { position: relative; z-index: 1; padding: 35px; max-width: 600px; }
.hero h1 { font-size: clamp(32px, 5vw, 56px); margin: 0 0 12px; line-height: 1.08; }
.hero p { font-size: 17px; line-height: 1.6; }
.hero .tag {
    display: inline-block; background: var(--yellow); color: black;
    font-weight: bold; padding: 8px 13px; border-radius: 5px;
}
main { width: 92%; max-width: 1250px; margin: auto; }
.section-heading {
    display: flex; justify-content: space-between; align-items: center;
    gap: 15px; flex-wrap: wrap; margin: 28px 0 16px;
}
.section-heading h2 { font-size: 30px; margin: 0; }
.search {
    width: 100%; max-width: 330px; padding: 12px 15px;
    border: 2px solid var(--black); border-radius: 8px; font-size: 15px;
}
.filters { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 22px; }
.filter-button {
    background: transparent; border: 2px solid var(--black);
    border-radius: 20px; padding: 8px 15px; font-weight: bold; cursor: pointer;
}
.filter-button.active, .filter-button:hover { background: var(--black); color: white; }
.products { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 18px; }
.product {
    background: white; border: 1px solid rgba(0,0,0,.15); border-radius: 13px;
    overflow: hidden; display: flex; flex-direction: column;
    box-shadow: 0 5px 12px rgba(0,0,0,.08);
}
.product-image {
    height: 210px; background: #f4f4f4; display: flex;
    align-items: center; justify-content: center; padding: 12px;
}
.product-image img { width: 100%; height: 100%; object-fit: contain; }
.product-info { padding: 15px; display: flex; flex-direction: column; flex: 1; }
.category { font-size: 12px; color: var(--muted); text-transform: uppercase; font-weight: bold; letter-spacing: 1px; }
.product h3 { font-size: 18px; margin: 8px 0; }
.product p { color: var(--muted); font-size: 14px; line-height: 1.4; margin: 0 0 15px; }
button, .button {
    background: var(--black); color: white; border: 0; padding: 12px 14px;
    border-radius: 7px; cursor: pointer; font-weight: bold; font-size: 14px;
    text-decoration: none; text-align: center;
}
button:hover, .button:hover { background: #383838; }
.product button { margin-top: auto; width: 100%; }
.cart-box, .enquiry-box {
    background: white; border-radius: 14px; padding: 22px;
    margin: 28px 0; box-shadow: 0 5px 12px rgba(0,0,0,.07);
}
.cart-item {
    display: flex; justify-content: space-between; align-items: center;
    gap: 12px; border-bottom: 1px solid #e5e5e5; padding: 12px 0; flex-wrap: wrap;
}
.cart-controls { display: flex; align-items: center; gap: 9px; }
.small-button { padding: 6px 11px; }
form { display: grid; gap: 13px; }
input, textarea, select {
    width: 100%; padding: 12px; border: 1px solid #ccc;
    border-radius: 7px; font-size: 15px; font-family: inherit;
}
textarea { min-height: 100px; resize: vertical; }
.notice { background: #fff5c2; padding: 12px; border-radius: 7px; margin-bottom: 14px; }
footer {
    background: var(--black); color: white; text-align: center;
    padding: 25px 12px; margin-top: 35px; line-height: 1.8;
}
footer strong { color: var(--yellow); }
@media (max-width: 950px) {
    .products { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}
@media (max-width: 650px) {
    .products { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px; }
    .product-image { height: 160px; }
    .hero { min-height: 270px; }
    .hero-content { padding: 22px; }
    .brand { font-size: 22px; }
    .product-info { padding: 11px; }
}
@media (max-width: 380px) {
    .products { grid-template-columns: 1fr; }
}
</style>
</head>
<body>
<header>
    <div class="brand">GAJANAND <span>TELECOM</span></div>
    <nav>
        <a href="/">Home</a>
        <a href="#products">Products</a>
        <a href="#cart">Cart ({{ cart_count }})</a>
        <a href="#enquiry">Enquiry</a>
    </nav>
</header>

<section class="hero">
    <div class="hero-content">
        <span class="tag">OFFICIAL PRODUCT ENQUIRIES</span>
        <h1>Discover U&i Accessories</h1>
        <p>Explore our collection of U&i audio, charging and smart accessories.
        Add products to your cart and send us an enquiry for availability and details.</p>
        <a class="button" href="#products">Explore Products</a>
    </div>
</section>

<main>
<section id="products">
    <div class="section-heading">
        <h2>Our Products</h2>
        <input class="search" id="searchBox" type="search" placeholder="Search U&i products...">
    </div>
    <div class="filters">
        <button type="button" class="filter-button active" data-category="All">All</button>
        <button type="button" class="filter-button" data-category="Audio">Audio</button>
        <button type="button" class="filter-button" data-category="Wearables">Wearables</button>
        <button type="button" class="filter-button" data-category="Charging">Charging</button>
    </div>
    <div class="products" id="productGrid">
    {% for p in products %}
        <article class="product" data-name="{{ p.name|lower }}" data-category="{{ p.category }}">
            <div class="product-image">
                <img src="{{ url_for('product_image', filename=p.image) }}"
                     alt="{{ p.name }}" loading="lazy"
                     onerror="this.onerror=null;this.style.display='none';">
            </div>
            <div class="product-info">
                <span class="category">{{ p.category }}</span>
                <h3>{{ p.name }}</h3>
                <p>Contact us for product availability and details.</p>
                <form action="{{ url_for('add_to_cart') }}" method="post">
                    <input type="hidden" name="product_id" value="{{ p.id }}">
                    <button type="submit">+ Add to Cart</button>
                </form>
            </div>
        </article>
    {% endfor %}
    </div>
</section>

<section class="cart-box" id="cart">
    <h2>Your Cart ({{ cart_count }} items)</h2>
    {% if cart_items %}
        {% for item in cart_items %}
        <div class="cart-item">
            <div><strong>{{ item.name }}</strong><div>Quantity: {{ item.quantity }}</div></div>
            <div class="cart-controls">
                <form action="{{ url_for('change_quantity') }}" method="post">
                    <input type="hidden" name="product_id" value="{{ item.id }}">
                    <input type="hidden" name="change" value="1">
                    <button class="small-button" type="submit">+</button>
                </form>
                <form action="{{ url_for('change_quantity') }}" method="post">
                    <input type="hidden" name="product_id" value="{{ item.id }}">
                    <input type="hidden" name="change" value="-1">
                    <button class="small-button" type="submit">−</button>
                </form>
                <form action="{{ url_for('remove_from_cart') }}" method="post">
                    <input type="hidden" name="product_id" value="{{ item.id }}">
                    <button class="small-button" type="submit">Remove</button>
                </form>
            </div>
        </div>
        {% endfor %}
        <p><strong>No prices are shown. Send an enquiry for details.</strong></p>
        <a class="button" href="#enquiry">Enquire About My Cart</a>
    {% else %}
        <p>Your cart is empty. Add products to get started.</p>
    {% endif %}
</section>

<section class="enquiry-box" id="enquiry">
    <h2>Product Enquiry</h2>
    <p>Send your details and the products you are interested in.</p>
    {% if submitted %}
        <div class="notice">
            Your enquiry email was accepted by Resend. Your cart has been cleared.
        </div>
    {% endif %}
    <form action="{{ url_for('enquiry') }}" method="post">
        <input type="text" name="customer_name" placeholder="Your full name" required maxlength="100">
        <input type="tel" name="phone" placeholder="Your phone number" required maxlength="30">
        <input type="email" name="email" placeholder="Your email (optional)" maxlength="150">
        <label for="product_choice"><strong>Product of interest</strong></label>
        <select name="product_choice" id="product_choice">
            <option value="Products in my cart">Products in my cart</option>
            {% for p in products %}
            <option value="{{ p.name }}">{{ p.name }}</option>
            {% endfor %}
            <option value="Multiple products">Multiple products</option>
        </select>
        <textarea name="message" placeholder="Write your question or enquiry..." maxlength="2000"></textarea>
        <button type="submit">Submit Enquiry</button>
    </form>
</section>
</main>

<footer>
    <strong>GAJANAND TELECOM</strong><br>
    Your destination for U&i accessories<br>
    Product availability and details available on enquiry.
</footer>

<script>
let selectedCategory = "All";
const searchBox = document.getElementById("searchBox");
const cards = document.querySelectorAll(".product");
const filterButtons = document.querySelectorAll(".filter-button");

function filterProducts() {
    const search = searchBox.value.toLowerCase().trim();
    cards.forEach(card => {
        const matchesSearch = card.dataset.name.includes(search);
        const matchesCategory = selectedCategory === "All" ||
            card.dataset.category === selectedCategory;
        card.style.display = matchesSearch && matchesCategory ? "flex" : "none";
    });
}
searchBox.addEventListener("input", filterProducts);
filterButtons.forEach(button => {
    button.addEventListener("click", () => {
        selectedCategory = button.dataset.category;
        filterButtons.forEach(item => item.classList.remove("active"));
        button.classList.add("active");
        filterProducts();
    });
});
</script>
</body>
</html>
"""


def get_cart():
    return session.get("cart", {})


def save_cart(cart_data):
    session["cart"] = cart_data


@app.route("/image/<path:filename>")
def product_image(filename):
    allowed_images = {
        "theme.jfif", "earbuds.jfif", "neckband.jfif",
        "headphones.jfif", "speaker.jfif", "smartwatch.jfif",
        "charger.jfif", "cable.jfif", "powerbank.jfif",
        "missing.jfif",
    }

    if filename not in allowed_images:
        return "Image not found", 404

    return send_from_directory(BASE_DIR, filename)


@app.route("/")
def home():
    cart_data = get_cart()
    cart_items = []

    for product in PRODUCTS:
        quantity = int(cart_data.get(str(product["id"]), 0))
        if quantity > 0:
            cart_items.append({**product, "quantity": quantity})

    cart_count = sum(item["quantity"] for item in cart_items)

    return render_template_string(
        PAGE,
        products=PRODUCTS,
        cart_items=cart_items,
        cart_count=cart_count,
        submitted=request.args.get("submitted") == "1",
    )


@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    try:
        product_id = int(request.form.get("product_id", "0"))
    except ValueError:
        return redirect(url_for("home"))

    if any(p["id"] == product_id for p in PRODUCTS):
        cart_data = get_cart()
        key = str(product_id)
        cart_data[key] = min(99, int(cart_data.get(key, 0)) + 1)
        save_cart(cart_data)

    return redirect(url_for("home") + "#cart")


@app.route("/change-quantity", methods=["POST"])
def change_quantity():
    try:
        product_id = int(request.form.get("product_id", "0"))
        change = int(request.form.get("change", "0"))
    except ValueError:
        return redirect(url_for("home") + "#cart")

    if any(p["id"] == product_id for p in PRODUCTS) and change in (-1, 1):
        cart_data = get_cart()
        key = str(product_id)
        quantity = max(0, int(cart_data.get(key, 0)) + change)

        if quantity:
            cart_data[key] = min(99, quantity)
        else:
            cart_data.pop(key, None)

        save_cart(cart_data)

    return redirect(url_for("home") + "#cart")


@app.route("/remove-from-cart", methods=["POST"])
def remove_from_cart():
    try:
        product_id = int(request.form.get("product_id", "0"))
    except ValueError:
        return redirect(url_for("home") + "#cart")

    cart_data = get_cart()
    cart_data.pop(str(product_id), None)
    save_cart(cart_data)

    return redirect(url_for("home") + "#cart")


@app.route("/enquiry", methods=["POST"])
def enquiry():
    customer_name = request.form.get("customer_name", "").strip()[:100]
    phone = request.form.get("phone", "").strip()[:30]
    email = request.form.get("email", "").strip()[:150]
    product_choice = request.form.get("product_choice", "").strip()[:100]
    message = request.form.get("message", "").strip()[:2000]

    if not customer_name or not phone:
        return "Please provide your name and phone number.", 400

    cart_data = get_cart()

    enquiry_data = {
        "time": datetime.now().astimezone().isoformat(timespec="seconds"),
        "customer_name": customer_name,
        "phone": phone,
        "email": email,
        "product": product_choice,
        "message": message,
        "cart": [
            {
                "name": p["name"],
                "quantity": int(cart_data.get(str(p["id"]), 0))
            }
            for p in PRODUCTS
            if int(cart_data.get(str(p["id"]), 0)) > 0
        ],
    }

    # Save enquiry locally where writable storage is available.
    try:
        enquiry_file = BASE_DIR / "enquiries.jsonl"
        with enquiry_file.open("a", encoding="utf-8") as file:
            file.write(json.dumps(enquiry_data, ensure_ascii=False) + "\n")
    except OSError as error:
        print("Could not save enquiry locally:", error)

    if not RESEND_API_KEY or not RESEND_TO_EMAIL:
        print("Missing RESEND_API_KEY or RESEND_TO_EMAIL.")
        return (
            "Email is not configured. Your cart has not been cleared. "
            "Please contact the shop owner."
        ), 500

    cart_details = "\n".join(
        f"- {item['name']} x {item['quantity']}"
        for item in enquiry_data["cart"]
    ) or "No products in cart"

    email_body = f"""
NEW GAJANAND TELECOM ENQUIRY

Date: {enquiry_data['time']}
Customer name: {customer_name}
Phone: {phone}
Customer email: {email or 'Not provided'}
Product of interest: {product_choice}

Products in cart:
{cart_details}

Customer message:
{message or 'No message provided'}
"""

    payload = {
        "from": RESEND_FROM_EMAIL,
        "to": [RESEND_TO_EMAIL],
        "subject": f"New Gajanand Telecom Enquiry - {customer_name}",
        "text": email_body,
    }

    try:
        response = requests.post(
            RESEND_API_URL,
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=20,
        )

        if not response.ok:
            print("Resend error:", response.status_code, response.text[:1000])
            return (
                "Your enquiry was saved, but email sending failed. "
                "Your cart has not been cleared. Please try again later."
            ), 502

        print("Resend accepted the enquiry email:", response.text[:500])

    except requests.RequestException as error:
        print("Resend connection error:", str(error))
        return (
            "Your enquiry was saved, but email sending failed. "
            "Your cart has not been cleared. Please try again later."
        ), 502

    # IMPORTANT: Clear this visitor's cart after successful email acceptance.
    session.pop("cart", None)

    return redirect(url_for("home", submitted="1") + "#enquiry")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5055))
    print("======================================")
    print("GAJANAND TELECOM WEBSITE IS STARTING")
    print(f"Open Chrome: http://127.0.0.1:{port}")
    print("======================================")
    app.run(host="0.0.0.0", port=port, debug=False)
