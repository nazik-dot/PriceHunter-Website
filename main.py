from dotenv import load_dotenv
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import os

app = Flask(__name__)
load_dotenv()

def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("is_admin"):
            abort(403)
        return view(*args, **kwargs)
    return wrapped_view

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///order_service.db'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False

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

products = {
    "1": {
        "id": "02-5156452",
        "name": "Чохол на диван 4-місний Love You Corn Fleece 81223 коричневий",
        "price": 1564,
        "image": "/files/chohol_na_duvan.webp"
    },
    "2": {
        "id": "991-120031284",
        "name": "Холст на підрамнику 40х60 см Art Craft 16020",
        "price": 315,
        "image": "/files/holst_na_pidramniku.jpg"
    },
    "3": {
        "id": "451-100396",
        "name": "Розгалужувач прикурювача на 3 гнізда з USB",
        "price": 165,
        "image": "/files/roshaluzuvach.webp"
    },
    "4": {
        "id": "321-111119190",
        "name": "Силіконова сушарка DT-1503 50×35 см сіра • Сушарка для посуду DT-1503 з килимком, тримачами для тарілок, чашок і приборів",
        "price": 476,
        "image": "/files/silikonova_susarka.webp"
    },
    "5": {
        "id": "321-111119183",
        "name": "Шарф Intelligent Heating Scarf з підігрівом чорний",
        "price": 505,
        "image": "/files/sharf_z_pidigrivom.webp"
    },
    "6": {
        "id": "02-5264672",
        "name": "Випрямляч для волосся Ardesto Pink Touch HC-R365PT 68 Вт сірий",
        "price": 1077,
        "image": "/files/vip_dla_volosya.webp"
    },
    "7": {
        "id": "991-120069877",
        "name": "М'яка іграшка 'Товстий кіт' K15215(White) 60 см",
        "price": 794,
        "image": "/files/tovstiy_kit.webp"
    },
    "8": {
        "id": "02-5271854",
        "name": "Форма для запікання з кришкою прямокутна SNT 50016-01 31.5х19х8.5 см 3.5 л",
        "price": 667,
        "image": "/files/sklana_forma_zapikanya.webp"
    },
    "9": {
        "id": "321-111119232",
        "name": "Електропила ланцюгова MLD із шиною 16″ у валізі",
        "price": 3004,
        "image": "/files/elektropila_lanzugova.webp"
    },
    "10": {
       "id": "02-1440146635",
       "name": "Кросівки жіночі Fashion Wizard 3127 37 розмір 23,5 см Білий",
       "price": 742,
       "image": "/files/fashion_wizard312737.webp"
    },
    "11": {
        "id": "451-127099",
        "name": "Органайзер настільний для канцелярії, маркерів та олівців з тумбочкою",
        "price": 406,
        "image": "/files/organayzer_nastilniy_dla_kanz_tumbochka.webp"
    },
    "12": {
        "id": "991-120069565",
        "name": "Реквізит для аніматора 'Парашут' KJ07-2 діаметр 3 м",
        "price": 1514,
        "image": "/files/rekvizit_dla_animatora_parashut.webp"
    },
    "13": {
        "id": "123-109953",
        "name": "Магнітола 901W 10.26' PND / Монітор 10.26' / Автомобільна стереосистема Bluetooth, Mirror Link, AUX",
        "price": 2927,
        "image": "/files/magnitola_901W.webp"
    },
    "14": {
        "id": "123-110211",
        "name": "IPAD 10.1 Планшет на 5 камер / Планшет з великим екраном та сучасним дизайном",
        "price": 5145,
        "image": "/files/ipad_10.1.webp"
    },
    "15": {
        "id": "451-127368",
        "name": "Ультразвуковий відлякувач гризунів та кротів",
        "price": 442,
        "image": "/files/ulyrazvukoviy_vidlakuvach_grizuniw.webp"
    },
    "16": {
        "id": "451-127269",
        "name": "Кільцева світлодіодна лампа для професійної зйомки Soft Ring Light 26см",
        "price": 416,
        "image": "/files/kilzeva_svitlodiodna_lampa_dla_zyomki.webp"
    },
    "17": {
        "id": "991-120049278",
        "name": "Аптечка першої допомоги спортивна First Aid Kit NE-LG-MED1",
        "price": 621,
        "image": "/files/aptechka_pershoi_dopomogi_sportivna.webp"
    },
    "18": {
        "id": "321-111119227",
        "name": "Термосумка холодильник 26 л синя 39×23×28 см",
        "price": 412,
        "image": "/files/termosumka_holodilnik_26l.webp"
    },
    "19": {
        "id": "321-111119228",
        "name": "Термосумка-холодильник 26 л 39×23×28 см бежева",
        "price": 412,
        "image": "/files/termosumka_holodilnik_26l_begeva.webp"
    },
    "20": {
        "id": "02-5232774",
        "name": "Ковдра двоспальна ТЕП ALASKA Зірки 1-00152_23926 180х205 см",
        "price": 1292,
        "image": "/files/kowdra_dvospalna_alaska_tepla.webp"
    }
}

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
    return render_template('drops.html', products=products)

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

    if product_id not in products:
        return "Not found", 404

    product = products[product_id]

    if not all([name, phone, delivery, delivery_adress, city, warehouse, price, quantity, payment_mode]):
        return "Missing required fields", 400

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
        product_id=product_id,
        city=city,
        warehouse=warehouse,
        price=price,
        quantity=quantity,
        payment_mode=payment_mode
    )

    db.session.add(new_order)
    db.session.commit()

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
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)