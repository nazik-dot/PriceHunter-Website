from dotenv import load_dotenv
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import os
from scraper import search_products, get_product_by_code, SupplierError

app = Flask(__name__)
load_dotenv()

def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("is_admin"):
            abort(403)
        return view(*args, **kwargs)
    return wrapped_view

database_url = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_DATABASE_URI"] = database_url

db = SQLAlchemy(app)

app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
admin_name = os.environ["ADMIN_NAME"]
admin_password = os.environ["ADMIN_PASSWORD"]

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(70), nullable=False)
    delivery = db.Column(db.String(30), nullable=False)
    delivery_adress = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    warehouse = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    payment_mode = db.Column(db.String(30), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/files/<path:filename>')
def files(filename):
    return send_from_directory('files', filename)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/drops_catalogue')
def catalogue():
    # return render_template('drops.html', products=products)
    q = request.args.get('q', '').strip()
    items, error = [], None
    if q:
        try:
            items = search_products(q)
        except SupplierError:
            error = "Не вдалося отримати товари спробуйте пізніше."
    return render_template("drops.html", products=items, q=q, error=error)

@app.route('/send_order', methods=['POST'])
def send_order():
    product_id = request.form.get('product_id')
    name = request.form.get('name')
    phone = request.form.get('phone')
    delivery = request.form.get('delivery')
    delivery_adress = request.form.get('delivery_adress')
    city = request.form.get('city')
    warehouse = request.form.get('warehouse')
    price = request.form.get('price')
    quantity = request.form.get('quantity')
    payment_mode = request.form.get('payment_mode')

    if not all([product_id, name, phone, delivery, delivery_adress, city, warehouse, quantity, payment_mode]):
        return "Missing required fields.", 400

    try:
        product = get_product_by_code(product_id)
    except SupplierError:
        return "Supplier is unavailable, try a bit later.", 503
    if product is None:
        return "Not Found", 404

    try:
        price = int(price)
        quantity = int(quantity)
        if quantity <= 0:
            return "Quantity must be greater than 0", 400
        if price <= 0:
            return "Price must be greater than 0", 400
    except ValueError:
        return "Price and quantity must be integers", 400

    price = product['price']

    new_order = Order(
        name=name,
        phone=phone,
        delivery=delivery,
        delivery_adress=delivery_adress,
        product_id=product['id'],
        city=city,
        warehouse=warehouse,
        price=price,
        quantity=quantity,
        payment_mode=payment_mode
    )

    db.session.add(new_order)
    db.session.commit()
    db.session.refresh(new_order)

    return render_template("order_processing.html", order=new_order, product=product)

@app.route("/admin_login", methods=['GET', 'POST'])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == admin_name and password == admin_password:
            session.clear()
            session["is_admin"] = True
            return redirect(url_for("admin_pannel"))
    return render_template("admin_login.html", error="Something went wrong."), 401

@app.route("/admin_pannel")
@admin_required
def admin_pannel():
    orders = Order.query.all()
    return render_template("admin_pannel.html", orders=orders)

@app.route("/admin_pannel/delete/<int:order_id>", methods=["POST"])
@admin_required
def delete_order(order_id):
    order = db.session.get(Order, order_id)
    if order is None:
        return "Not found", 404
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for("admin_pannel"))

@app.route("/rules")
def rules():
    return render_template("rules.html")
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)