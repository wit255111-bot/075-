import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os

def create_manual():
    doc = Document()

    # Set Margins (1 inch all around)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Palette
    COLOR_PRIMARY = RGBColor(30, 58, 138)     # Navy #1E3A8A
    COLOR_SECONDARY = RGBColor(37, 99, 235)   # Blue #2563EB
    COLOR_DARK = RGBColor(15, 23, 42)         # Slate 900
    COLOR_MUTED = RGBColor(100, 116, 139)     # Slate 500
    COLOR_SUCCESS = RGBColor(16, 185, 129)    # Emerald

    # Helper: Set font
    def set_font(run, name="Cordia New", size=14, bold=False, italic=False, color=COLOR_DARK):
        run.font.name = name
        run.font.size = Pt(size)
        run.bold = bold
        run.italic = italic
        run.font.color.rgb = color

    # Helper: Cell background color
    def set_cell_bg(cell, fill_hex):
        tcPr = cell._element.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    # Helper: Cell borders (subtle gray)
    def set_cell_borders(cell, top="CCCCCC", bottom="CCCCCC", left=None, right=None):
        tcPr = cell._element.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="4" w:space="0" w:color="{top}"/>
                <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{bottom}"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)

    # Helper: Callout Box
    def add_callout(text, title="คำแนะนำสำคัญ (Important Note)", fill_hex="EFF6FF", border_hex="3B82F6"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_bg(cell, fill_hex)
        tcPr = cell._element.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_hex}"/>
                <w:top w:val="none"/>
                <w:right w:val="none"/>
                <w:bottom w:val="none"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(2)
        r_title = p.add_run(f"📌 {title}\n")
        set_font(r_title, size=14, bold=True, color=COLOR_SECONDARY)
        r_text = p.add_run(text)
        set_font(r_text, size=13, color=COLOR_DARK)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Helper: Add Heading 1
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        set_font(r, size=20, bold=True, color=COLOR_PRIMARY)
        return p

    # Helper: Add Heading 2
    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        set_font(r, size=16, bold=True, color=COLOR_SECONDARY)
        return p

    # Helper: Add Paragraph
    def add_p(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            set_font(r_pre, size=14, bold=True, color=COLOR_DARK)
        r = p.add_run(text)
        set_font(r, size=14, color=COLOR_DARK)
        return p

    # Helper: Add Bullet
    def add_bullet(text, bold_prefix=None, level=0):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.left_indent = Inches(0.25 * (level + 1))
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            set_font(r_pre, size=14, bold=True, color=COLOR_DARK)
        r = p.add_run(text)
        set_font(r, size=14, color=COLOR_DARK)
        return p

    # ==========================================
    # COVER PAGE
    # ==========================================
    p_top = doc.add_paragraph()
    p_top.paragraph_format.space_before = Pt(30)
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_badge = p_top.add_run("เอกสารคู่มือการใช้งานระบบ (SYSTEM USER MANUAL)")
    set_font(r_badge, size=12, bold=True, color=COLOR_SECONDARY)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(10)
    r_title = p_title.add_run("NEXUS TECH\nE-Commerce & Smart PC Builder Platform")
    set_font(r_title, size=26, bold=True, color=COLOR_PRIMARY)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(30)
    r_sub = p_sub.add_run("คู่มือการใช้งานระบบจำหน่ายอุปกรณ์คอมพิวเตอร์ ฮาร์ดแวร์ ซอฟต์แวร์ลิขสิทธิ์แท้\nและระบบจัดสเปคคอมพิวเตอร์อัจฉริยะ (พร้อมตรวจสอบความเข้ากันได้)")
    set_font(r_sub, size=15, color=COLOR_MUTED)

    # Info Box Table on Cover
    tbl_cover = doc.add_table(rows=5, cols=2)
    tbl_cover.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_info = [
        ("ชื่อระบบงาน:", "NEXUS TECH (ร้านขายอุปกรณ์คอมพิวเตอร์และซอฟต์แวร์)"),
        ("เวอร์ชันระบบ:", "Version 2.0 (Full-Stack Edition)"),
        ("แพลตฟอร์ม:", "Python Flask / SQLite / Tailwind CSS / Vanilla JS"),
        ("กลุ่มผู้ใช้งาน:", "ลูกค้าทั่วไป, ช่างจัดสเปคคอมพิวเตอร์, และผู้ดูแลระบบ (Admin)"),
        ("วันที่จัดทำ:", "พฤศจิกายน 2026")
    ]
    for i, (k, v) in enumerate(meta_info):
        row = tbl_cover.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        set_cell_bg(c0, "F1F5F9")
        set_cell_bg(c1, "F8FAFC")
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(k)
        set_font(r0, size=13, bold=True, color=COLOR_PRIMARY)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(v)
        set_font(r1, size=13, color=COLOR_DARK)

    doc.add_page_break()

    # ==========================================
    # TABLE OF CONTENTS
    # ==========================================
    add_h1("สารบัญเนื้อหา (Table of Contents)")
    toc_items = [
        ("บทที่ 1: ภาพรวมระบบและความสามารถหลัก (System Overview)", "หน้า 3"),
        ("บทที่ 2: การเริ่มต้นใช้งานและเข้าสู่เว็บไซต์ (Getting Started)", "หน้า 4"),
        ("บทที่ 3: การเลือกชมสินค้าฮาร์ดแวร์และซอฟต์แวร์ (Product Catalog)", "หน้า 5"),
        ("บทที่ 4: การใช้งานระบบจัดสเปคคอมพิวเตอร์อัจฉริยะ (Smart PC Builder)", "หน้า 6"),
        ("       4.1 การเลือกชิ้นส่วนและการตรวจจับความเข้ากันได้ (Compatibility Engine)", "หน้า 6"),
        ("       4.2 การคำนวณวัตต์ไฟและแนะนำ Power Supply (PSU Wattage Meter)", "หน้า 7"),
        ("       4.3 การใช้งานสเปคสำเร็จรูปยอดนิยม (Preset Builds)", "หน้า 8"),
        ("       4.4 การพิมพ์ใบเสนอราคาทางการ (Official Quotation PDF/Print)", "หน้า 8"),
        ("       4.5 การคัดลอกแชร์สเปคและการเพิ่มลงตะกร้าในคลิกเดียว", "หน้า 9"),
        ("บทที่ 5: การสั่งซื้อสินค้าและระบบตะกร้า (Cart & Checkout Process)", "หน้า 10"),
        ("       5.1 การจัดการตะกร้าสินค้า (Cart Drawer & Full Page)", "หน้า 10"),
        ("       5.2 การจำลองการชำระเงินและข้อมูลจัดส่ง", "หน้า 10"),
        ("       5.3 ระบบส่งมอบรหัส Digital License Key สำหรับซอฟต์แวร์แท้", "หน้า 11"),
        ("บทที่ 6: การใช้งานระบบหลังบ้านสำหรับผู้ดูแลระบบ (Admin Dashboard)", "หน้า 12"),
        ("บทที่ 7: คำถามที่พบบ่อยและการแก้ไขปัญหาเบื้องต้น (FAQ & Troubleshooting)", "หน้า 13"),
    ]
    tbl_toc = doc.add_table(rows=len(toc_items), cols=2)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (topic, page) in enumerate(toc_items):
        r = tbl_toc.rows[idx]
        c0, c1 = r.cells[0], r.cells[1]
        c0.width = Inches(5.2)
        c1.width = Inches(1.3)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(topic)
        set_font(r0, size=13, color=COLOR_DARK)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r1 = p1.add_run(page)
        set_font(r1, size=13, bold=True, color=COLOR_MUTED)

    doc.add_page_break()

    # ==========================================
    # CHAPTER 1
    # ==========================================
    add_h1("บทที่ 1: ภาพรวมระบบและความสามารถหลัก (System Overview)")
    add_p("เว็บไซต์ NEXUS TECH เป็นแพลตฟอร์มพาณิชย์อิเล็กทรอนิกส์ (E-Commerce) ที่พัฒนาขึ้นโดยเฉพาะสำหรับธุรกิจจำหน่ายอุปกรณ์คอมพิวเตอร์และซอฟต์แวร์ เพื่อแก้ปัญหาความยุ่งยากในการเลือกซื้ออุปกรณ์คอมพิวเตอร์ที่ต้องคำนึงถึงความเข้ากันได้ทางเทคนิค (Hardware Compatibility) และการส่งมอบซอฟต์แวร์ลิขสิทธิ์แท้ได้อย่างรวดเร็ว")

    add_h2("จุดเด่นที่สำคัญของแพลตฟอร์ม:")
    add_bullet(" ตรวจสอบซ็อกเก็ต CPU และเมนบอร์ด (Socket Matching) แบบเรียลไทม์ เช่น LGA1700, AM5 รวมถึงตรวจสอบประเภทแรม DDR4 หรือ DDR5 ป้องกันปัญหาซื้อไปแล้วประกอบไม่ได้", bold_prefix="1. ระบบจัดสเปคคอมอัจฉริยะ (AI Compatibility Engine):")
    add_bullet(" คำนวณค่า TDP รวมของซีพียูและการ์ดจอ พร้อมแนะนำขนาดพาวเวอร์ซัพพลาย (PSU) ที่เหมาะสมเพื่อความเสถียรของเครื่อง", bold_prefix="2. ระบบคำนวณวัตต์ไฟ (PSU Wattage Calculator):")
    add_bullet(" มีสเปคคอมสำหรับทำงานเบาๆ (15k), เกมมิ่งยอดนิยม (35k) และสตรีมมิ่งระดับโปร (63k) ให้กดโหลดชิ้นส่วนทั้งหมดเข้าสู่เครื่องจำลองได้ทันที", bold_prefix="3. สเปคสำเร็จรูปยอดนิยม (Preset Builds):")
    add_bullet(" สามารถสร้างเอกสารใบเสนอราคาทางการที่มีเลขที่ใบเสนอราคา รายละเอียดประกัน คำนวณ VAT 7% พร้อมช่องลงนาม สามารถสั่งพิมพ์หรือบันทึกเป็น PDF ได้ทันที", bold_prefix="4. ระบบออกใบเสนอราคา (Quotation Generator):")
    add_bullet(" เมื่อลูกค้าสั่งซื้อซอฟต์แวร์ เช่น Windows 11, Office 2024 หรือ Antivirus ระบบจะสร้างรหัสลิขสิทธิ์ (License Key) ให้บนหน้าใบเสร็จทันที พร้อมส่งสำเนาเข้าอีเมล", bold_prefix="5. ระบบส่งมอบ Digital License Key อัตโนมัติ:")
    add_bullet(" ให้ความรู้สึกทันสมัย สวยงามแบบ Tech Dark Mode ใช้งานได้ทั้งบนคอมพิวเตอร์ แท็บเล็ต และสมาร์ตโฟน", bold_prefix="6. ดีไซน์แบบ Responsive & Glassmorphism:")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 2
    # ==========================================
    add_h1("บทที่ 2: การเริ่มต้นใช้งานและเข้าสู่เว็บไซต์ (Getting Started)")
    add_p("ระบบถูกออกแบบมาให้สามารถติดตั้งและรันบนเครื่องคอมพิวเตอร์ที่มี Python ติดตั้งอยู่ได้อย่างง่ายดาย โดยใช้ฐานข้อมูล SQLite ในตัว ทำให้ไม่ต้องติดตั้งซอฟต์แวร์ฐานข้อมูลขนาดใหญ่เพิ่มเติม")

    add_h2("ความต้องการของระบบ (System Requirements):")
    add_bullet(" Windows 10 / Windows 11 หรือ macOS / Linux", bold_prefix="ระบบปฏิบัติการ: ")
    add_bullet(" Python 3.10 ขึ้นไป (รองรับเต็มรูปแบบบน Python 3.14)", bold_prefix="โปรแกรมแปลภาษา: ")
    add_bullet(" Google Chrome, Microsoft Edge, Safari หรือ Mozilla Firefox รุ่นปัจจุบัน", bold_prefix="เว็บเบราว์เซอร์: ")
    add_bullet(" Flask (ติดตั้งผ่านคำสั่ง `pip install flask`)", bold_prefix="โมดูลเสริม: ")

    add_h2("ขั้นตอนการเปิดใช้งานระบบ (How to Run):")
    add_p("1. เปิดโปรแกรม Command Prompt (CMD) หรือ PowerShell")
    add_p("2. ไปยังโฟลเดอร์ของโปรเจกต์ เช่น:")
    add_callout("cd c:\\075\npython app.py", title="คำสั่งสำหรับรันระบบ (Terminal Commands)", fill_hex="F8FAFC", border_hex="1E3A8A")
    add_p("3. ระบบจะแสดงข้อความว่า `Running on http://127.0.0.1:5000`")
    add_p("4. เปิดเว็บเบราว์เซอร์แล้วพิมพ์ URL:")
    add_callout("http://127.0.0.1:5000", title="ที่อยู่เว็บไซต์ (Web URL)", fill_hex="EFF6FF", border_hex="2563EB")

    add_h2("โครงสร้างหน้าจอหลัก (Navigation Overview):")
    add_bullet(" โลโก้ NEXUS TECH คลิกเพื่อกลับมายังหน้าแรกเสมอ", bold_prefix="• แถบเมนูด้านบน (Header):")
    add_bullet(" ค้นหาชื่อรุ่น แบรนด์ หรือคีย์เวิร์ดของสินค้าได้แบบแสดงผลสดทันที", bold_prefix="• ช่องค้นหาอัจฉริยะ (Live Search):")
    add_bullet(" ทางลัดพิเศษไปยังระบบจัดสเปคคอม พร้อมเอฟเฟกต์ไฟกระพริบดึงดูดสายตา", bold_prefix="• ปุ่ม 'จัดสเปคคอม' (PC Builder):")
    add_bullet(" เมนูแยกประเภทสินค้าระหว่างอุปกรณ์ฮาร์ดแวร์ และ ซอฟต์แวร์ลิขสิทธิ์แท้", bold_prefix="• เมนูสินค้าฮาร์ดแวร์ & ซอฟต์แวร์:")
    add_bullet(" แสดงจำนวนสินค้าในตะกร้าแบบเรียลไทม์ และคลิกเพื่อเปิดลิ้นชักด้านข้าง (Cart Drawer)", bold_prefix="• ไอคอนตะกร้าสินค้า (Cart Drawer):")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 3
    # ==========================================
    add_h1("บทที่ 3: การเลือกชมสินค้าฮาร์ดแวร์และซอฟต์แวร์ (Product Catalog)")
    add_p("ผู้ใช้สามารถเลือกชมสินค้าได้อย่างหลากหลายและสะดวกสบาย ผ่านเมนูสินค้าที่แยกหมวดหมู่อย่างชัดเจน")

    add_h2("1. การแยกแยะประเภทสินค้า:")
    add_bullet(" ซีพียู (CPU), เมนบอร์ด (Mainboard), แรม (RAM), การ์ดจอ (GPU), ที่จัดเก็บข้อมูล (SSD M.2), พาวเวอร์ซัพพลาย (PSU), เคส (Case), ระบบระบายความร้อน (Cooler) และ จอมอนิเตอร์ (Monitor) โดยสินค้าทุกชิ้นจะระบุเงื่อนไขการรับประกันศูนย์ไทยแท้ เช่น 3 ปี Synnex / WTG / Ascenti", bold_prefix="• สินค้าฮาร์ดแวร์ (Hardware): ")
    add_bullet(" ระบบปฏิบัติการ Windows 11 Home / Pro (FPP / ESD Digital License), ชุดโปรแกรม Microsoft Office 2024 / Microsoft 365, โปรแกรมป้องกันไวรัส Kaspersky, Bitdefender และโปรแกรมช่วยดาวน์โหลด IDM ซึ่งทั้งหมดเป็นลิขสิทธิ์แท้ 100%", bold_prefix="• สินค้าซอฟต์แวร์ (Software): ")

    add_h2("2. การใช้งานตัวกรองสินค้า (Product Filtering):")
    add_p("ในหน้าสินค้ารวม (`/products`) ผู้ใช้สามารถใช้แผงตัวกรองทางซ้ายมือได้ดังนี้:")
    add_bullet("คลิกเลือกแท็บ 'ฮาร์ดแวร์' หรือ 'ซอฟต์แวร์แท้' เพื่อดูเฉพาะกลุ่มสินค้าที่ต้องการ")
    add_bullet("คลิกเลือกหมวดหมู่ย่อย เช่น เลือกดูเฉพาะซีพียู หรือ การ์ดจอ")
    add_bullet("คลิกเลือกแบรนด์ที่ต้องการ เช่น Intel, AMD, ASUS, MSI, Corsair, Kingston, Samsung ฯลฯ")
    add_bullet("จัดเรียงลำดับสินค้า: เรียงตามราคาจากต่ำไปสูง, ราคาจากสูงไปต่ำ หรือเรียงตามคะแนนรีวิว")

    add_h2("3. หน้ารายละเอียดสินค้า (Product Detail):")
    add_p("เมื่อคลิกที่สินค้าใดๆ ระบบจะแสดงหน้ารายละเอียดเชิงลึก ซึ่งประกอบด้วย:")
    add_bullet("รูปภาพสินค้าขนาดใหญ่พร้อมป้ายส่วนลด (%)")
    add_bullet("ตารางสเปคทางเทคนิค (Technical Specifications) เช่น Socket, TDP, Bus Speed, VRAM, Read/Write Speed")
    add_bullet("ข้อมูลการรับประกันศูนย์ และสถานะสินค้าในสต็อก")
    add_bullet("ตัวปรับจำนวนชิ้น (Quantity Selector) และปุ่ม 'เพิ่มลงในตะกร้า'")
    add_bullet("ปุ่ม 'จัดสเปคด้วยชิ้นนี้' สำหรับนำชิ้นส่วนฮาร์ดแวร์ไปบรรจุลงในระบบ PC Builder อัตโนมัติ")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 4
    # ==========================================
    add_h1("บทที่ 4: การใช้งานระบบจัดสเปคคอมพิวเตอร์อัจฉริยะ (Smart PC Builder)")
    add_p("ระบบจัดสเปคคอมพิวเตอร์ (PC Builder) เป็นฟีเจอร์ไฮไลต์ของเว็บไซต์ ออกแบบมาเพื่อให้ทั้งผู้เริ่มต้นและผู้เชี่ยวชาญสามารถจัดสเปคคอมพิวเตอร์ได้อย่างมั่นใจ รวดเร็ว และไม่มีข้อผิดพลาด")

    add_h2("4.1 ขั้นตอนการเลือกชิ้นส่วนทีละขั้นตอน:")
    add_p("1. เข้าสู่หน้าจัดสเปคคอมโดยคลิกที่ปุ่ม 'จัดสเปคคอม' ที่เมนูด้านบน หรือเข้า URL `/builder`")
    add_p("2. หน้าจอจะแสดงช่องชิ้นส่วนหลัก 10 รายการ ได้แก่:")
    add_bullet("1. ซีพียู (CPU) *จำเป็น")
    add_bullet("2. เมนบอร์ด (Mainboard) *จำเป็น")
    add_bullet("3. หน่วยความจำแรม (RAM) *จำเป็น")
    add_bullet("4. การ์ดจอแสดงผล (GPU)")
    add_bullet("5. ตัวจัดเก็บข้อมูล (SSD M.2 NVMe) *จำเป็น")
    add_bullet("6. พาวเวอร์ซัพพลาย (Power Supply) *จำเป็น")
    add_bullet("7. เคสคอมพิวเตอร์ (Case) *จำเป็น")
    add_bullet("8. ระบบระบายความร้อนซีพียู (Cooler)")
    add_bullet("9. จอมอนิเตอร์ (Monitor)")
    add_bullet("10. ระบบปฏิบัติการ (Windows OS)")
    add_p("3. คลิกที่ปุ่ม 'เลือกสินค้า' ในแต่ละช่องเพื่อเปิดหน้าต่างแสดงสินค้า")
    add_p("4. ระบบจะมี Smart Badge ระบุชัดเจนว่าสินค้าชิ้นใด 'เข้ากันได้กับอุปกรณ์ที่เลือกไว้แล้ว' หรือ 'ไม่เข้ากัน'")

    add_h2("4.2 กลไกการตรวจสอบความเข้ากันได้ (Compatibility Engine):")
    add_p("ระบบจะตรวจสอบเงื่อนไขทางวิศวกรรมฮาร์ดแวร์ 3 ประการอย่างต่อเนื่อง:")
    
    # Table of Compatibility rules
    tbl_compat = doc.add_table(rows=4, cols=3)
    tbl_compat.alignment = WD_TABLE_ALIGNMENT.CENTER
    rules_data = [
        ("รายการตรวจสอบ", "เงื่อนไขทางเทคนิค", "การแจ้งเตือนของระบบ"),
        ("1. ซ็อกเก็ต CPU vs เมนบอร์ด", "Socket ต้องตรงกันทุกประการ (เช่น LGA1700 กับ LGA1700, AM5 กับ AM5)", "หากไม่ตรงกัน ระบบจะขึ้นกล่องสีแดงเตือน: 'ซ็อกเก็ตไม่ตรงกัน ไม่สามารถติดตั้งได้'"),
        ("2. ชนิดแรม vs เมนบอร์ด", "RAM Type ต้องตรงกับบอร์ด (DDR4 ต้องใช้กับบอร์ด DDR4, DDR5 ต้องใช้กับบอร์ด DDR5)", "หากชนิดแรมไม่ตรง ระบบจะขึ้นเตือน: 'ชนิดแรมไม่ตรงกับเมนบอร์ด'"),
        ("3. กำลังไฟ PSU vs สเปคเครื่อง", "ขนาดวัตต์ PSU ต้องมากกว่าหรือเท่ากับค่า TDP (CPU + GPU + องค์ประกอบอื่น) x 1.3", "หากวัตต์ต่ำเกินไป ระบบจะเตือน: 'พาวเวอร์ซัพพลายต่ำกว่าที่แนะนำ เสี่ยงเครื่องดับ'")
    ]
    for row_idx, data in enumerate(rules_data):
        row = tbl_compat.rows[row_idx]
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            if row_idx == 0:
                set_cell_bg(cell, "1E3A8A")
                p = cell.paragraphs[0]
                r = p.add_run(text)
                set_font(r, size=13, bold=True, color=RGBColor(255, 255, 255))
            else:
                set_cell_bg(cell, "F8FAFC" if row_idx % 2 == 1 else "FFFFFF")
                p = cell.paragraphs[0]
                r = p.add_run(text)
                set_font(r, size=12, color=COLOR_DARK)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_h2("4.3 การคำนวณวัตต์ไฟและแนะนำ PSU (Wattage Meter):")
    add_p("แถบวัดพลังงานจะคำนวณการกินไฟรวมแบบ Dynamic:")
    add_bullet("นำค่า TDP ของซีพียู (เช่น Intel i7-14700K = 125W) มารวมกับค่า TDP ของการ์ดจอ (เช่น RTX 4070 SUPER = 220W) บวกค่าไฟพื้นฐานของเมนบอร์ด แรม และพัดลม (70W)")
    add_bullet("แสดงผล Estimated Wattage เช่น 415 W")
    add_bullet("คำนวณขนาดพาวเวอร์ซัพพลายที่แนะนำ (Recommended PSU) โดยเผื่อ Headroom ป้องกันไฟกระชาก 30% เช่น แนะนำ 650W หรือ 750W")

    add_h2("4.4 การใช้งานสเปคสำเร็จรูป (Preset Builds):")
    add_p("หากลูกค้ายังไม่แน่ใจว่าจะเลือกชิ้นส่วนใด ทางร้านได้จัดชุดสเปคมาตรฐานไว้ให้ 3 ระดับ:")
    add_bullet(" ซีพียู 10 คอร์ แรม 16GB SSD 1TB ทำงานเอกสารและเล่นเกมเบาๆ ได้ลื่นไหล", bold_prefix="• งบประหยัด (14,900 บาท): ")
    add_bullet(" ซีพียู Core i5 Gen 14 + การ์ดจอ RTX 4060 8GB DLSS 3 ปรับภาพระดับ Full HD Ultra", bold_prefix="• ชุดยอดนิยม (34,900 บาท): ")
    add_bullet(" ซีพียู Ryzen 7 7800X3D (3D V-Cache) + การ์ดจอ RTX 4070 SUPER 12GB แรม DDR5 32GB พร้อมชุดน้ำ เล่นเกม 2K และสตรีมมิ่งระดับโปร", bold_prefix="• ชุดเกมมิ่ง & สตรีมมิ่ง 2K (62,900 บาท): ")
    add_p("เพียงคลิกปุ่ม **'โหลดสเปคนี้'** ระบบจะนำชิ้นส่วนทุกชิ้นเข้ามาใส่ในช่องให้โดยอัตโนมัติ และลูกค้าสามารถปรับเปลี่ยนเฉพาะชิ้นที่ต้องการเพิ่มเติมได้ทันที")

    add_h2("4.5 การออกใบเสนอราคาทางการ (Official Quotation PDF/Print):")
    add_p("เมื่อจัดสเปคเสร็จแล้ว สามารถคลิกปุ่ม **'พิมพ์ใบเสนอราคา'**:")
    add_bullet("ระบบจะสร้างเอกสารใบเสนอราคามาตรฐาน มีหัวกระดาษบริษัท NEXUS TECH CO., LTD.")
    add_bullet("มีเลขที่ใบเสนอราคาอัตโนมัติ (เช่น QT-849201), วันที่ออกเอกสาร และวันหมดอายุใบเสนอราคา (7 วัน)")
    add_bullet("มีตารางสรุปรายการอุปกรณ์ พร้อมระบุการรับประกันของแต่ละชิ้นส่วน")
    add_bullet("มีสรุปยอดก่อนภาษี, ภาษีมูลค่าเพิ่ม 7% (VAT) และยอดรวมสุทธิ")
    add_bullet("มีช่องลงนามของผู้เสนอราคา และช่องลงนามอนุมัติสั่งซื้อของลูกค้า พร้อมสั่งพิมพ์ทางเครื่องพิมพ์หรือกดบันทึกเป็นไฟล์ PDF ได้ทันที")

    add_h2("4.6 การแชร์สเปคและการเพิ่มลงตะกร้าในคลิกเดียว:")
    add_bullet(" คัดลอกรายการชิ้นส่วนทั้งหมดพร้อมราคาและลิงก์เว็บไซต์ลงคลิปบอร์ด เพื่อนำไปส่งให้เพื่อนใน Line หรือโพสต์ถามความคิดเห็นในกลุ่ม Facebook ได้ทันที", bold_prefix="• ปุ่ม 'แชร์สเปค':")
    add_bullet(" เพิ่มชิ้นส่วนทั้งหมดที่เลือกไว้ (สูงสุด 10 ชิ้นส่วน) เข้าสู่ตะกร้าสินค้าในคราวเดียว โดยไม่ต้องกดทีละชิ้นส่วน พร้อมเข้าสู่ขั้นตอนสั่งซื้อทันที", bold_prefix="• ปุ่ม 'เพิ่มทั้งหมดลงตะกร้า':")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 5
    # ==========================================
    add_h1("บทที่ 5: การสั่งซื้อสินค้าและระบบตะกร้า (Cart & Checkout Process)")
    add_p("ระบบการสั่งซื้อของ NEXUS TECH ได้รับการออกแบบให้รองรับทั้งการจัดส่งพัสดุฮาร์ดแวร์ถึงบ้าน และการส่งมอบซอฟต์แวร์ลิขสิทธิ์แท้แบบดิจิทัลได้ทันที")

    add_h2("5.1 การจัดการตะกร้าสินค้า (Cart Drawer & Full Cart):")
    add_bullet("เปิดดูตะกร้าด่วนได้ตลอดเวลาผ่านไอคอนตะกร้าบนแถบเมนู (มีลิ้นชักสไลด์ออกมาจากขวา)")
    add_bullet("ปรับเพิ่ม/ลดจำนวนสินค้า หรือกดปุ่มถังขยะเพื่อลบรายการที่ไม่ต้องการ")
    add_bullet("ระบบจะจำลองราคารวมและบันทึกลงในหน่วยความจำของเบราว์เซอร์ (LocalStorage) ทำให้รายการสินค้าไม่สูญหายแม้ปิดหน้าต่างเว็บไป")

    add_h2("5.2 ขั้นตอนการยืนยันคำสั่งซื้อและการชำระเงิน (Checkout):")
    add_p("ในหน้าตะกร้าเต็ม (`/cart`) ลูกค้ากรอกข้อมูลในแบบฟอร์ม:")
    add_bullet("ชื่อ-นามสกุล และ เบอร์โทรศัพท์ของผู้รับ")
    add_bullet("อีเมล (สำคัญมากสำหรับลูกค้ารับรหัส Digital License Key ของซอฟต์แวร์)")
    add_bullet("ที่อยู่จัดส่งพัสดุสำหรับสินค้าฮาร์ดแวร์")
    add_bullet("เลือกช่องทางชำระเงิน: สแกน QR PromptPay, บัตรเครดิต หรือ โอนผ่านธนาคาร")
    add_bullet("คลิกปุ่ม **'ยืนยันการสั่งซื้อและชำระเงิน'**")

    add_h2("5.3 ระบบส่งมอบรหัส Digital License Key สำหรับซอฟต์แวร์แท้:")
    add_p("กรณีที่ลูกค้าสั่งซื้อซอฟต์แวร์แท้ เช่น Windows 11 Pro หรือ Microsoft Office เมื่อยืนยันการสั่งซื้อสำเร็จ:")
    add_bullet("ระบบจะสร้างรหัสลิขสิทธิ์แท้ (Digital License Key) แสดงบนหน้าจอใบเสร็จรับเงินทันที พร้อมปุ่มกดคัดลอกคีย์ใน 1 คลิก")
    add_bullet("ระบบจะส่งสำเนารหัสคีย์และใบเสร็จไปยังอีเมลที่ลูกค้าระบุไว้")
    add_bullet("มีคำแนะนำขั้นตอนการเปิดใช้งาน (Activation Guide) ให้ลูกค้าปฏิบัติตามได้ทันที เช่น เข้าไปที่ Settings > System > Activation บน Windows")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 6
    # ==========================================
    add_h1("บทที่ 6: การใช้งานระบบหลังบ้านสำหรับผู้ดูแลระบบ (Admin Dashboard)")
    add_p("ผู้ดูแลระบบ (Admin) สามารถเข้าดูรายงานยอดขายและตรวจสอบคลังสินค้าได้ผ่านหน้าเว็บโดยตรง")

    add_h2("การเข้าถึงระบบหลังบ้าน:")
    add_p("คลิกที่เมนู 'หลังบ้าน' ด้านบนขวา หรือเปิด URL:")
    add_callout("http://127.0.0.1:5000/admin", title="ทางเข้าสู่ระบบหลังบ้าน (Admin URL)", fill_hex="FAF5FF", border_hex="9333EA")

    add_h2("ฟังก์ชันการทำงานในระบบหลังบ้าน:")
    add_bullet(" แสดงจำนวนรายการสินค้าทั้งหมดในระบบ, จำนวนคำสั่งซื้อที่เกิดขึ้น และสถานะการเชื่อมต่อฐานข้อมูล", bold_prefix="1. แผงสรุปสถิติสำคัญ (KPI Overview):")
    add_bullet(" แสดงตารางคำสั่งซื้อเรียงจากล่าสุด พร้อมแสดงเลขที่ออเดอร์, ชื่อลูกค้า, เบอร์โทร, ช่องทางการชำระเงิน, จำนวนรายการ, ยอดชำระสุทธิ และมีปุ่มคลิกดูใบเสร็จฉบับเต็ม", bold_prefix="2. รายการคำสั่งซื้อล่าสุด (Recent Orders):")
    add_bullet(" แสดงรายการอุปกรณ์คอมพิวเตอร์และซอฟต์แวร์ทั้งหมดในคลัง พร้อมรหัสสินค้า แบรนด์ หมวดหมู่ ราคาขาย และจำนวนสต็อกคงเหลือแบบเรียลไทม์", bold_prefix="3. ตรวจสอบคลังสินค้า (Inventory Overview):")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 7
    # ==========================================
    add_h1("บทที่ 7: คำถามที่พบบ่อยและการแก้ไขปัญหาเบื้องต้น (FAQ & Troubleshooting)")

    faqs = [
        ("Q1: เปิดเบราว์เซอร์ไปที่ http://127.0.0.1:5000 แล้วหน้าเว็บไม่ขึ้น?", 
         "A: ตรวจสอบว่าในโปรแกรม Command Prompt หรือ Terminal ได้รันคำสั่ง `python app.py` ค้างไว้อยู่หรือไม่ หากยังไม่ได้รัน ให้สั่งรันโปรแกรมก่อนเปิดหน้าเว็บ"),
        
        ("Q2: ในหน้า PC Builder ระบบขึ้นเตือนกรอบสีแดง หมายความว่าอย่างไร?", 
         "A: หมายถึงมีชิ้นส่วนอย่างน้อย 2 ชิ้นที่เลือกไม่เข้ากัน เช่น ซ็อกเก็ต CPU กับ เมนบอร์ด คนละขนาดกัน หรือเลือกแรม DDR4 ไปใส่บนบอร์ด DDR5 แนะนำให้คลิกปุ่ม 'เปลี่ยน' ที่ชิ้นส่วนนั้นๆ เพื่อเลือกรุ่นที่ระบบขึ้นสัญลักษณ์สีเขียวว่าเข้ากันได้"),

        ("Q3: ชิ้นส่วนที่เลือกไปแล้วใน PC Builder สามารถเปลี่ยนหรือลบได้หรือไม่?", 
         "A: สามารถทำได้ตลอดเวลา โดยกดปุ่ม 'เปลี่ยน' เพื่อเลือกรุ่นใหม่ หรือกดปุ่ม 'ถังขยะ' สีเทาเพื่อเอาชิ้นส่วนนั้นออกจากชุดจัดสเปค หรือกดปุ่ม 'ล้างสเปค' เพื่อเริ่มต้นใหม่ทั้งหมด"),

        ("Q4: รหัส Digital License Key ของซอฟต์แวร์จะได้รับเมื่อใด?", 
         "A: ระบบจัดส่งให้อัตโนมัติทันทีที่กดยืนยันการชำระเงิน โดยรหัสจะแสดงบนหน้าจอใบเสร็จรับเงิน และสามารถกดปุ่มไอคอนคัดลอกรหัสเพื่อนำไปเปิดใช้งานได้ทันที"),

        ("Q5: ต้องการพิมพ์ใบเสนอราคาเพื่อนำไปเสนอเบิกงบประมาณขององค์กร ทำอย่างไร?", 
         "A: หลังจากเลือกชิ้นส่วนในระบบ PC Builder ครบถ้วนแล้ว ให้คลิกปุ่ม 'พิมพ์ใบเสนอราคา' (Quotation) จากนั้นกดบันทึกเป็นไฟล์ PDF เพื่อแนบส่งทางอีเมล หรือสั่งพิมพ์ออกทางเครื่องพิมพ์ได้ทันที")
    ]

    for q, a in faqs:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(8)
        p_q.paragraph_format.space_after = Pt(2)
        r_q = p_q.add_run(q)
        set_font(r_q, size=14, bold=True, color=COLOR_PRIMARY)

        p_a = doc.add_paragraph()
        p_a.paragraph_format.space_after = Pt(6)
        r_a = p_a.add_run(a)
        set_font(r_a, size=13, color=COLOR_DARK)

    # Save document
    path_en = os.path.join(os.path.dirname(__file__), "User_Manual_NEXUS_TECH.docx")
    path_th = os.path.join(os.path.dirname(__file__), "คู่มือการใช้งาน_NEXUS_TECH.docx")
    doc.save(path_en)
    doc.save(path_th)
    print("User manuals generated successfully:")
    print("1.", path_en)
    print("2.", path_th)

if __name__ == '__main__':
    create_manual()
