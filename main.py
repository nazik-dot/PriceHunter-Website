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

products = {
    "1998": {
        "id": "02-5324246",
        "name": "Лимонадник Yiwu Sunflower HP-19-289 2 л",
        "price": 1426,
        "image": "/files/limonnik_yiwu_sunflower_hp-19-289_2l.webp"
    },
    "99": {
        "id": "602-1565346",
        "name": "Сукні WN19-98 темно-коричневий S, M",
        "price": 1187,
        "image": "/files/sukni_wn19-98_s_temno-korichneviy.webp"
    },
    "1": {
        "id": "02-5156452",
        "name": "Чохол на диван 4-місний Love You Corn Fleece 81223 коричневий",
        "price": 1689,
        "image": "/files/chohol_na_duvan.webp"
    },
    "8677": {
        "id": "02-5324203",
        "name": "Набір сервірувальних серветок Ardesto Autumn leaves ART15MN 30х45 см 2 шт",
        "price": 382,
        "image": "/files/nabir_serviruvalnix_servetok_ardesto_autumn_leaves.webp"
    },
    "2736": {
        "id": "02-5150640",
        "name": "Набір сервірувальних серветок Ardesto Christmas Gingerbread ART15HG 30х45 см 2 шт",
        "price": 399,
        "image": "/files/nabir_serviruvalnix_servetok_ardesto_christmas_gingerbread.webp"
    },
    "2": {
        "id": "991-120031284",
        "name": "Холст на підрамнику 40х60 см Art Craft 16020",
        "price": 382,
        "image": "/files/holst_na_pidramniku.jpg"
    },
    "3": {
        "id": "451-100396",
        "name": "Розгалужувач прикурювача на 3 гнізда з USB",
        "price": 227,
        "image": "/files/roshaluzuvach.webp"
    },
    "4": {
        "id": "321-111119190",
        "name": "Силіконова сушарка DT-1503 50×35 см сіра • Сушарка для посуду DT-1503 з килимком, тримачами для тарілок, чашок і приборів",
        "price": 550,
        "image": "/files/silikonova_susarka.webp"
    },
    "2701": {
        "id": "02-589588467",
        "name": "Чоловіча туалетна вода LA RIVE EXTREME STORY, 75 мл La Rive HIM-063223",
        "price": 574,
        "image": "/files/cholovicha_tualetna_woda_la_rive_extreme_story_75ml.webp"
    },
    "5": {
        "id": "321-111119183",
        "name": "Шарф Intelligent Heating Scarf з підігрівом чорний",
        "price": 526,
        "image": "/files/sharf_z_pidigrivom.webp"
    },
    "6": {
        "id": "02-5264672",
        "name": "Випрямляч для волосся Ardesto Pink Touch HC-R365PT 68 Вт сірий",
        "price": 1040,
        "image": "/files/vip_dla_volosya.webp"
    },
    "7": {
        "id": "991-120069877",
        "name": "М'яка іграшка 'Товстий кіт' K15215(White) 60 см",
        "price": 766,
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
        "price": 3137,
        "image": "/files/elektropila_lanzugova.webp"
    },
    "10": {
       "id": "02-1440146635",
       "name": "Кросівки жіночі Fashion Wizard 3127 37 розмір 23,5 см Білий",
       "price": 798,
       "image": "/files/fashion_wizard312737.webp"
    },
    "98": {
        "id": "602-1565339",
        "name": "Светри WN20-664 темно-бежевий L, XL",
        "price": 1022,
        "image": "/files/swetri_wn20-664_xl_temno-begeviy.webp"
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
        "price": 1460,
        "image": "/files/rekvizit_dla_animatora_parashut.webp"
    },
    "13": {
        "id": "02-5118786",
        "name": "Набір салатників SNT 30098-02 7 предметів білий",
        "price": 727,
        "image": "/files/nabir_salatnikiv_snt_biluy.webp"
    },
    "14": {
        "id": "123-110211",
        "name": "IPAD 10.1 Планшет на 5 камер / Планшет з великим екраном та сучасним дизайном",
        "price": 5406,
        "image": "/files/ipad_10.1.webp"
    },
    "15": {
        "id": "451-127368",
        "name": "Ультразвуковий відлякувач гризунів та кротів",
        "price": 442,
        "image": "/files/ulyrazvukoviy_vidlakuvach_grizuniw.webp"
    },
    "256": {
        "id": "02-5264795",
        "name": "Мультимейкер 8в1 Zepline ZP-808 581591 2200 Вт чорна уцінка",
        "price": 1998,
        "image": "/files/multimaker_8in1_zepline_chorna_uzinka.webp"
    },
    "16": {
        "id": "451-127269",
        "name": "Кільцева світлодіодна лампа для професійної зйомки Soft Ring Light 26см",
        "price": 416,
        "image": "/files/kilzeva_svitlodiodna_lampa_dla_zyomki.webp"
    },
    # "17": {
    #     "id": "02-5309509",
    #     "name": "Постільна білизна євро з мусліну Koloco Print 1 23119 200х230 см",
    #     "price": 1110,
    #     "image": "/files/postilna_biluzna_evro_muslin_koloco_print1.webp"
    # },
    "18": {
        "id": "321-111119227",
        "name": "Термосумка холодильник 26 л синя 39×23×28 см",
        "price": 424,
        "image": "/files/termosumka_holodilnik_26l.webp"
    },
    "19": {
        "id": "321-111119228",
        "name": "Термосумка-холодильник 26 л 39×23×28 см бежева",
        "price": 424,
        "image": "/files/termosumka_holodilnik_26l_begeva.webp"
    },
    # "20": {
    #     "id": "451-129210",
    #     "name": "Складная, походная канистра для воды 20 л Емкость для воды с краном",
    #     "price": 319,
    #     "image": "/files/skladnaya_pohodnaya_kanistra_dla_vody.webp"
    # },
    "391": {
        "id": "602-1562442",
        "name": "Чоловічі спортивні штани GN-570 темно-сірий S, M, L, XL, XXL",
        "price": 1061,
        "image": "/files/cholovichi_sportivni_shtany_gb-570_temno-siruy.webp"
    },
    "21": {
        "id": "02-5272947",
        "name": "Клавіатура провідна комп'ютерна Logitech G PRO Mechanical Gaming USB L920-009392 чорна",
        "price": 7925,
        "image": "/files/klaviatura_providna_computerna_logitech_g_pro.webp"
    },
    "22": {
        "id": "02-5056112",
        "name": "Легінси жіночі з пуш-ап 18871 M сірі",
        "price": 600,
        "image": "/files/leginsu_zinochi_pushup.webp"
    },
    "23": {
        "id": "02-5280405",
        "name": "Рушник банний махровий Koloco 22215 70х140 см капучино",
        "price": 435,
        "image": "/files/rushnuk_banniy_machroviy_koloco.webp"
    },
    # "24": {
    #     "id": "999-26877",
    #     "name": "Стільниковий акумулятор, Переносний зарядний банк, Портативний акумулятор для телефону WQ-25",
    #     "price": 476,
    #     "image": "/files/stilnikoviy_akamulator_perenosni_zaradniy_bank.webp"
    # },
    "5738": {
        "id": "02-5324202",
        "name": "Плед Ardesto Flannel ART0238SB 200х220 см синій",
        "price": 996,
        "image": "/files/pled_ardesto_flannel_suniy.webp"
    },
    "25": {
        "id": "02-5208483",
        "name": "Стайлер для волосся Inspire WT-631-6IN1 1000 Вт чорний",
        "price": 4023,
        "image": "/files/styler_dla_volosya_inspire.webp"
    },
    "26": {
        "id": "321-111119386",
        "name": "Годівниця з поїлкою Pet Automatic 2 в 1 синя • Автоматична гравітаційна годівниця Pet Automatic для котів і собак із резервуарами для сухого корму та води без електрики",
        "price": 526,
        "image": "/files/godivnuza_z_poilkoyu_petautomatic.webp"
    },
    "27": {
        "id": "02-5210737",
        "name": "Тример VGR V-983 5 Вт золотистий",
        "price": 786,
        "image": "/files/trimer_vgr_zolotistiy.webp"
    },
    # "28": {
    #     "id": "321-111119381",
    #     "name": "Компактна шафка XL-1613 для ванної з основою 15×15 см • вертикальна система зберігання білого кольору з полицями та закритими секціями для косметики й дрібниць",
    #     "price": 601,
    #     "image": "/files/kompaktna_shafa_dla_vannoi_z_osnovoyu.webp"
    # },
    "29": {
        "id": "02-5273818",
        "name": "Форма для запікання прямокутна Maestro MR-1107-35 7х29.5х37 см чорна",
        "price": 938,
        "image": "/files/forma_dla_zapikanya_pramokutna_maestro_mr.webp"
    },
    "2799": {
        "id": "02-5324275",
        "name": "Термокухоль Ardesto Provence AR2650BD 500 мл синій",
        "price": 628,
        "image": "/files/termokuhol_ardesto_provence_500ml_suniy.webp"
    },
    "30": {
        "id": "02-589229575",
        "name": "Жіноча парфумована вода MISS DREAM,100 мл La Rive HIM-066071",
        "price": 604,
        "image": "/files/zhinocha_parfumovana_woda_missdream_100ml.webp"
    },
    "31": {
        "id": "02-4721785",
        "name": "Кондиціонер для білизни Lavandera Морський Бриз 8435495828730 1.76 л",
        "price": 406,
        "image": "/files/kondizioner_dla_biluznu_lavandera_morskiy_1_76l.webp"
    },
    "32": {
        "id": "602-1563329",
        "name": "Светри WN20-773 Universal бордовий",
        "price": 1064,
        "image": "/files/svetri_wn20-773_universal_bordoviy.webp"
    },
    "33": {
        "id": "123-110897",
        "name": "Лампа LED LA-08 15W / Світильник з гачком на microUSB / Акумуляторна LED-лампочка",
        "price": 335,
        "image": "/files/lampa_led_svitulnuk_z_hachlom_microUSB.webp"
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