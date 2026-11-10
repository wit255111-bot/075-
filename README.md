# NEXUS TECH — Computer Hardware & Genuine Software E-Commerce Platform

เว็บไซต์จำหน่ายอุปกรณ์คอมพิวเตอร์ (Hardware) และ ซอฟต์แวร์ลิขสิทธิ์แท้ (Software) พร้อมระบบ **PC Builder (จัดสเปคคอมพิวเตอร์อัจฉริยะ)** ตรวจสอบความเข้ากันได้ของอุปกรณ์ และคำนวณกำลังไฟฟ้า (PSU Wattage) แบบเรียลไทม์

---

## 🌟 ฟีเจอร์เด่นของระบบ

### 1. ระบบจัดสเปคคอมพิวเตอร์อัจฉริยะ (PC Builder / DIY PC)
- **ตรวจสอบความเข้ากันได้อัตโนมัติ (Compatibility Engine)**:
  - ตรวจสอบความตรงกันของ Socket ซีพียู และ เมนบอร์ด (เช่น LGA1700, AM5)
  - ตรวจสอบประเภทแรมที่รองรับ (DDR4 vs DDR5)
  - ตรวจสอบกำลังไฟ PSU เทียบกับความต้องการของระบบ (CPU TDP + GPU TDP)
- **คำนวณวัตต์ไฟแบบเรียลไทม์ (Estimated Wattage & PSU Recommendation)** พร้อมแถบวัดระดับพลังงาน
- **สเปคสำเร็จรูปยอดนิยม (Preset Builds)**:
  - ชุดประหยัด ทำงาน/เรียนออนไลน์ (฿14,900)
  - ชุดเกมมิ่งยอดนิยม Full HD ปรับสุด RTX 4060 (฿34,900)
  - ชุดเกมมิ่ง & สตรีมมิ่ง 2K ไฮเอนด์ RTX 4070 SUPER + Ryzen 7 (฿62,900)
- **พิมพ์ใบเสนอราคาทางการ (Official Quotation PDF/Print View)** พร้อมโลโก้บริษัท วันที่ เงื่อนไขรับประกัน และช่องลงนาม
- **แชร์สเปคคอม**: ฟังก์ชันคัดลอกสรุปสเปคทั้งหมดเป็นข้อความพร้อมลิงก์
- **เพิ่มชิ้นส่วนทั้งหมดลงตะกร้าใน 1 คลิก**

### 2. หมวดหมู่สินค้าฮาร์ดแวร์ (Hardware)
- CPU (Intel Core 14th Gen, AMD Ryzen 7000 Series)
- Mainboard (ASUS, MSI, GIGABYTE, ASRock)
- RAM (Kingston FURY, Corsair Vengeance DDR4/DDR5)
- GPU (NVIDIA GeForce RTX 4060, 4070 SUPER, 4080 SUPER, AMD Radeon RX 7800 XT)
- Storage (Samsung 990 PRO, WD Black SN850X, Kingston NV2)
- Power Supply (CORSAIR 80+ Gold, Cooler Master)
- Case (NZXT, Montech, Lian Li O11 Dynamic)
- CPU Cooler (Thermalright, NZXT Kraken LCD)
- Monitor (LG UltraGear 2K 165Hz, AOC 24" 165Hz)

### 3. หมวดหมู่ซอฟต์แวร์ลิขสิทธิ์แท้ (Genuine Software & Digital Keys)
- Microsoft Windows 11 Home & Pro (FPP / ESD Digital License ตลอดชีพ)
- Microsoft Office 2024 / Microsoft 365 Personal (รายปี และ ตลอดชีพ)
- Antivirus (Kaspersky Standard, Bitdefender Total Security)
- ยูทิลิตี้ (Internet Download Manager - IDM Lifetime)
- **ระบบจัดส่งรหัส Digital License Key อัตโนมัติ**: เมื่อสั่งซื้อซอฟต์แวร์ ระบบจะสร้าง Digital Key พร้อมคำแนะนำการ Activate ให้ลูกค้าทันที

### 4. ระบบการสั่งซื้อและตะกร้าสินค้า (Cart & Checkout)
- ระบบตะกร้าสินค้า (Cart Drawer & หน้ารวมตะกร้า) บันทึกข้อมูลด้วย LocalStorage
- คำนวณยอดรวม, ภาษีมูลค่าเพิ่ม (VAT 7%), ส่วนลด
- ระบบจำลองการชำระเงิน (PromptPay QR, บัตรเครดิต, โอนเงิน)
- หน้าใบเสร็จรับเงิน (Order Receipt) แสดงข้อมูลผู้รับ เลขพัสดุ และ Digital Key

### 5. ระบบหลังบ้าน (Admin Dashboard)
- เข้าใช้งานได้ที่ `/admin`
- ดูรายงานคำสั่งซื้อล่าสุด สถานะชำระเงิน ยอดเงิน
- ตรวจสอบรายการสินค้าในคลัง (Stock Inventory)

---

## 🚀 วิธีการรันโปรเจกต์ (How to Run)

1. เปิด Terminal ในโฟลเดอร์โปรเจกต์ `c:\075`
2. ติดตั้งแพ็กเกจ Flask:
   ```bash
   python -m pip install flask
   ```
3. รันเซิร์ฟเวอร์:
   ```bash
   python app.py
   ```
4. เปิดเว็บเบราว์เซอร์ไปที่:
   ```
   http://127.0.0.1:5000
   ```

---

## 📁 โครงสร้างโปรเจกต์

```
c:\075\
├── app.py                     # เซิร์ฟเวอร์หลัก Flask และ API Routes
├── database.py                # ระบบเชื่อมต่อและสร้างตารางฐานข้อมูล SQLite
├── seed_data.py               # ข้อมูลสินค้าตั้งต้น (ฮาร์ดแวร์ + ซอฟต์แวร์)
├── techhub.db                 # ฐานข้อมูล SQLite
├── static/
│   ├── css/
│   │   └── custom.css         # ฟอนต์ Prompt, แอนิเมชัน และสไตล์สำหรับพิมพ์ใบเสนอราคา
│   └── js/
│       ├── cart.js            # ระบบจัดการตะกร้าสินค้า และ Toast Notification
│       └── pc-builder.js      # ระบบจัดสเปคคอม ตรวจสอบ Socket, RAM และคำนวณวัตต์
└── templates/
    ├── base.html              # เลย์เอาต์หลัก เมนูบาร์ Mega-Menu และ Cart Drawer
    ├── index.html             # หน้าแรก สรุปโปรโมชั่น และสินค้าแนะนำ
    ├── pc_builder.html        # หน้าจัดสเปคคอมพิวเตอร์ (PC Builder)
    ├── products.html          # หน้ารายการสินค้า พร้อมตัวกรองประเภท แบรนด์ และราคา
    ├── product_detail.html    # หน้ารายละเอียดสินค้า สเปค ประกัน และสต็อก
    ├── cart.html              # หน้าตะกร้าสินค้า และฟอร์มสั่งซื้อ
    ├── order_success.html     # หน้าใบเสร็จรับเงิน และแสดง Digital License Key
    └── admin.html             # หน้าจัดการหลังบ้านสำหรับผู้ดูแลระบบ
```
