import os
import json
import uuid
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory
from database import get_db_connection

app = Flask(__name__)
app.secret_key = 'techhub_super_secret_key_2026'

# Custom Jinja filters
@app.template_filter('currency')
def currency_filter(value):
    try:
        val = float(value)
        return f"฿{val:,.2f}".replace(".00", "")
    except (ValueError, TypeError):
        return f"฿{value}"

@app.template_filter('json_loads')
def json_loads_filter(value):
    try:
        return json.loads(value)
    except Exception:
        return {}

@app.context_processor
def inject_categories():
    categories_hardware = [
        {"id": "cpu", "name": "ซีพียู (CPU)", "icon": "cpu"},
        {"id": "motherboard", "name": "เมนบอร์ด (Mainboard)", "icon": "server"},
        {"id": "ram", "name": "แรม (RAM)", "icon": "database"},
        {"id": "gpu", "name": "การ์ดจอ (VGA/GPU)", "icon": "hard-drive"},
        {"id": "storage", "name": "ที่จัดเก็บข้อมูล (SSD/M.2)", "icon": "save"},
        {"id": "psu", "name": "พาวเวอร์ซัพพลาย (PSU)", "icon": "zap"},
        {"id": "case", "name": "เคสคอมพิวเตอร์ (Case)", "icon": "box"},
        {"id": "cooler", "name": "ระบบระบายความร้อน (Cooler)", "icon": "wind"},
        {"id": "monitor", "name": "จอมอนิเตอร์ (Monitor)", "icon": "monitor"}
    ]
    categories_software = [
        {"id": "software_os", "name": "ระบบปฏิบัติการ (Windows)", "icon": "grid"},
        {"id": "software_office", "name": "ชุดโปรแกรมออฟฟิศ (Office / 365)", "icon": "file-text"},
        {"id": "software_security", "name": "ความปลอดภัย (Antivirus)", "icon": "shield-check"},
        {"id": "software_tools", "name": "ยูทิลิตี้และโปรแกรมเสริม", "icon": "tool"}
    ]
    return {
        "nav_categories_hardware": categories_hardware,
        "nav_categories_software": categories_software
    }

# ==================== ROUTES ====================

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Featured hardware
    cursor.execute("SELECT * FROM products WHERE is_featured = 1 AND type = 'hardware' LIMIT 8")
    featured_hardware = [dict(row) for row in cursor.fetchall()]

    # Featured software
    cursor.execute("SELECT * FROM products WHERE type = 'software' LIMIT 6")
    featured_software = [dict(row) for row in cursor.fetchall()]

    # Parse specs_json for display
    for item in featured_hardware + featured_software:
        if item.get("specs_json"):
            try:
                item["specs"] = json.loads(item["specs_json"])
            except Exception:
                item["specs"] = {}

    conn.close()
    return render_template('index.html',
                           featured_hardware=featured_hardware,
                           featured_software=featured_software)


@app.route('/builder')
def pc_builder():
    return render_template('pc_builder.html')


@app.route('/products')
def products():
    category = request.args.get('category', '')
    product_type = request.args.get('type', '')
    brand = request.args.get('brand', '')
    sort = request.args.get('sort', 'default')
    q = request.args.get('q', '').strip()
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM products WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if product_type:
        query += " AND type = ?"
        params.append(product_type)

    if brand:
        query += " AND brand = ?"
        params.append(brand)

    if q:
        query += " AND (name LIKE ? OR brand LIKE ? OR description LIKE ?)"
        term = f"%{q}%"
        params.extend([term, term, term])

    if min_price is not None:
        query += " AND price >= ?"
        params.append(min_price)

    if max_price is not None:
        query += " AND price <= ?"
        params.append(max_price)

    if sort == 'price_asc':
        query += " ORDER BY price ASC"
    elif sort == 'price_desc':
        query += " ORDER BY price DESC"
    elif sort == 'rating':
        query += " ORDER BY rating DESC"
    else:
        query += " ORDER BY id DESC"

    cursor.execute(query, params)
    items = [dict(row) for row in cursor.fetchall()]

    for item in items:
        if item.get("specs_json"):
            try:
                item["specs"] = json.loads(item["specs_json"])
            except Exception:
                item["specs"] = {}

    # Get available brands for filtering
    cursor.execute("SELECT DISTINCT brand FROM products ORDER BY brand ASC")
    brands = [row["brand"] for row in cursor.fetchall()]

    conn.close()

    return render_template('products.html',
                           products=items,
                           brands=brands,
                           current_category=category,
                           current_type=product_type,
                           current_brand=brand,
                           current_sort=sort,
                           search_query=q)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return "Product not found", 404

    product = dict(row)
    if product.get("specs_json"):
        try:
            product["specs"] = json.loads(product["specs_json"])
        except Exception:
            product["specs"] = {}

    # Related products
    cursor.execute("SELECT * FROM products WHERE category = ? AND id != ? LIMIT 4", (product["category"], product_id))
    related = [dict(r) for r in cursor.fetchall()]
    for r in related:
        if r.get("specs_json"):
            try:
                r["specs"] = json.loads(r["specs_json"])
            except Exception:
                r["specs"] = {}

    conn.close()
    return render_template('product_detail.html', product=product, related=related)


# ==================== CART & CHECKOUT ====================

@app.route('/cart')
def cart_page():
    return render_template('cart.html')


@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.get_json() if request.is_json else request.form.to_dict()

    items = data.get('items', [])
    if isinstance(items, str):
        try:
            items = json.loads(items)
        except Exception:
            items = []

    if not items:
        return jsonify({"success": False, "message": "ไม่มีสินค้าในตะกร้า"}), 400

    order_code = f"TH-{uuid.uuid4().hex[:8].upper()}"
    customer_name = data.get('customer_name', 'ลูกค้าทั่วไป')
    customer_email = data.get('customer_email', 'customer@example.com')
    customer_phone = data.get('customer_phone', '081-234-5678')
    customer_address = data.get('customer_address', 'กรุงเทพมหานคร')
    delivery_type = data.get('delivery_type', 'standard')
    payment_method = data.get('payment_method', 'promptpay')

    # Calculate total and generate digital keys for software items
    total_amount = 0
    digital_keys = []

    for item in items:
        price = float(item.get('price', 0))
        qty = int(item.get('qty', 1))
        total_amount += price * qty

        # If software, generate realistic license key
        if item.get('type') == 'software':
            for _ in range(qty):
                prefix = item.get('name', 'KEY')[:4].upper()
                gen_key = f"{prefix}-{uuid.uuid4().hex[:5].upper()}-{uuid.uuid4().hex[:5].upper()}-{uuid.uuid4().hex[:5].upper()}"
                digital_keys.append({
                    "product_name": item.get('name'),
                    "license_key": gen_key,
                    "activated": False
                })

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO orders (
            order_code, customer_name, customer_email, customer_phone,
            customer_address, delivery_type, payment_method, total_amount,
            items_json, digital_keys_json, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        order_code, customer_name, customer_email, customer_phone,
        customer_address, delivery_type, payment_method, total_amount,
        json.dumps(items), json.dumps(digital_keys), 'Paid & Confirmed'
    ))

    conn.commit()
    conn.close()

    if request.is_json:
        return jsonify({
            "success": True,
            "order_code": order_code,
            "redirect_url": url_for('order_success', order_code=order_code)
        })

    return redirect(url_for('order_success', order_code=order_code))


@app.route('/order/<order_code>')
def order_success(order_code):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders WHERE order_code = ?", (order_code,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return "Order not found", 404

    order = dict(row)
    order_items = json.loads(order["items_json"]) if order.get("items_json") else []
    order["items"] = order_items
    order["order_items"] = order_items
    order["digital_keys"] = json.loads(order["digital_keys_json"]) if order.get("digital_keys_json") else []

    conn.close()
    return render_template('order_success.html', order=order)


# ==================== ADMIN ====================

@app.route('/admin')
def admin_page():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders ORDER BY id DESC LIMIT 20")
    orders = [dict(r) for r in cursor.fetchall()]
    for o in orders:
        if o.get("items_json"):
            try:
                items_list = json.loads(o["items_json"])
                o["order_items"] = items_list
            except Exception:
                o["order_items"] = []
        else:
            o["order_items"] = []

    cursor.execute("SELECT * FROM products ORDER BY id DESC")
    products_list = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return render_template('admin.html', orders=orders, products=products_list)


# ==================== API ENDPOINTS ====================

@app.route('/api/builder/components')
def api_builder_components():
    conn = get_db_connection()
    cursor = conn.cursor()

    categories = ['cpu', 'motherboard', 'ram', 'gpu', 'storage', 'psu', 'case', 'cooler', 'monitor', 'software_os']
    result = {}

    for cat in categories:
        cursor.execute("SELECT * FROM products WHERE category = ? ORDER BY price ASC", (cat,))
        items = [dict(row) for row in cursor.fetchall()]
        for it in items:
            if it.get("specs_json"):
                try:
                    it["specs"] = json.loads(it["specs_json"])
                except Exception:
                    it["specs"] = {}
        result[cat] = items

    conn.close()
    return jsonify(result)


@app.route('/api/builder/presets')
def api_builder_presets():
    # Pre-configured popular PC builds
    presets = [
        {
            "id": "budget_15k",
            "name": "ชุดเริ่มต้น ทำงาน & เรียนออนไลน์ & เล่นเกมเบาๆ",
            "badge": "งบประหยัด",
            "target_price": 14900,
            "description": "เซ็ตคุ้มค่า ซีพียู 10 คอร์ พร้อมแรม 16GB และ SSD ความเร็วสูง ทำงานเอกสาร เล่น The Sims 4 / Valorant ได้ลื่นไหล",
            "components": {
                "cpu": "Intel Core i5-14400F 2.5GHz 10C/16T",
                "motherboard": "MSI PRO B760M-P DDR4",
                "ram": "Kingston FURY Beast DDR4 16GB (8GBx2) 3200MHz Black",
                "gpu": "Inno3D GeForce RTX 3050 6GB TWIN X2",
                "storage": "Kingston NV2 NVMe M.2 SSD 1TB (PCIe 4.0)",
                "psu": "Cooler Master MWE 650W V2 Bronze",
                "case": "Montech AIR 100 ARGB (Black)",
                "cooler": "Thermalright Peerless Assassin 120 SE"
            }
        },
        {
            "id": "gaming_35k",
            "name": "เกมมิ่งยอดนิยม Full HD ปรับสุดทุกเกม (RTX 4060)",
            "badge": "ยอดนิยม",
            "target_price": 34900,
            "description": "สเปคขวัญใจเกมเมอร์ i5 เจน 14 จับคู่กับ RTX 4060 8GB DLSS 3 ปรับภาพ Ultra ลื่นทุกเกมระดับ AAA",
            "components": {
                "cpu": "Intel Core i5-14400F 2.5GHz 10C/16T",
                "motherboard": "ASUS TUF GAMING B760-PLUS WIFI DDR5",
                "ram": "Kingston FURY Beast DDR5 32GB (16GBx2) 6000MHz Black",
                "gpu": "MSI GeForce RTX 4060 VENTUS 2X BLACK 8G OC",
                "storage": "Samsung 990 PRO NVMe M.2 SSD 1TB (PCIe 4.0)",
                "psu": "CORSAIR RM750e 750W 80 PLUS Gold Fully Modular (ATX 3.0)",
                "case": "NZXT H5 Flow RGB (Black)",
                "cooler": "Thermalright Peerless Assassin 120 SE",
                "software_os": "Microsoft Windows 11 Home 64-bit (FPP / USB Box)"
            }
        },
        {
            "id": "gaming_60k",
            "name": "เกมมิ่ง & สตรีมมิ่ง 2K ปรับ Ultra (RTX 4070 SUPER + Ryzen 7)",
            "badge": "ไฮเอนด์ 2K",
            "target_price": 62900,
            "description": "ขุมพลัง Ryzen 7 7800X3D เจ้าแห่งเกมมิ่ง พร้อมการ์ดจอ RTX 4070 SUPER แรม DDR5 32GB และระบบน้ำระบายความร้อน จอ 2K สบายๆ",
            "components": {
                "cpu": "AMD Ryzen 7 7800X3D 4.2GHz 8C/16T (3D V-Cache)",
                "motherboard": "MSI MAG B650 TOMAHAWK WIFI (AM5 DDR5)",
                "ram": "Corsair VENGEANCE RGB DDR5 32GB (16GBx2) 6000MHz White",
                "gpu": "ASUS TUF Gaming GeForce RTX 4070 SUPER 12GB GDDR6X",
                "storage": "Samsung 990 PRO NVMe M.2 SSD 1TB (PCIe 4.0)",
                "psu": "CORSAIR RM850x 850W 80 PLUS Gold Fully Modular",
                "case": "Lian Li O11 Dynamic EVO (White)",
                "cooler": "NZXT Kraken 240 RGB Liquid Cooler (Black)",
                "software_os": "Microsoft Windows 11 Pro 64-bit (ESD Digital License)"
            }
        }
    ]
    return jsonify(presets)


@app.route('/api/products/search')
def api_search():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, category, type, brand, price, image_url
        FROM products
        WHERE name LIKE ? OR brand LIKE ?
        LIMIT 6
    """, (f"%{q}%", f"%{q}%"))

    items = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(items)


@app.route('/download-manual')
def download_manual():
    directory = os.path.dirname(os.path.abspath(__file__))
    filename = "User_Manual_NEXUS_TECH.docx"
    return send_from_directory(directory, filename, as_attachment=True, download_name="คู่มือการใช้งาน_NEXUS_TECH.docx")


if __name__ == '__main__':
    print("Starting TechHub Server on http://127.0.0.1:5000 ...")
    app.run(host='127.0.0.1', port=5000, debug=True)
