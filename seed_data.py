import sqlite3
import json
import os
from database import DB_PATH, init_db

PRODUCTS = [
    # ==================== CPU ====================
    {
        "name": "Intel Core i5-14400F 2.5GHz 10C/16T",
        "category": "cpu",
        "type": "hardware",
        "brand": "Intel",
        "price": 6890,
        "original_price": 7490,
        "stock": 18,
        "image_url": "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=500&q=80",
        "description": "ซีพียูเจเนอเรชันที่ 14 สถาปัตยกรรมไฮบริด 10 คอร์ (6P + 4E) เหมาะสำหรับการเล่นเกมและการทำงานทั่วไป ประหยัดพลังงาน คุ้มค่าที่สุด",
        "specs_json": json.dumps({
            "socket": "LGA1700",
            "tdp": 65,
            "cores": "10 (6P + 4E)",
            "threads": 16,
            "base_clock": "2.5 GHz",
            "boost_clock": "4.7 GHz",
            "cache": "20 MB Intel Smart Cache"
        }),
        "warranty": "3 ปี โดย Synnex / Ingram",
        "rating": 4.9,
        "is_featured": 1
    },
    {
        "name": "Intel Core i7-14700K 3.4GHz 20C/28T",
        "category": "cpu",
        "type": "hardware",
        "brand": "Intel",
        "price": 15900,
        "original_price": 16900,
        "stock": 12,
        "image_url": "https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?w=500&q=80",
        "description": "ความแรงระดับท็อป 20 คอร์ 28 เธรด พร้อมปลดล็อกการโอเวอร์คล็อก สำหรับสตรีมเมอร์ ครีเอเตอร์ และเกมเมอร์ระดับฮาร์ดคอร์",
        "specs_json": json.dumps({
            "socket": "LGA1700",
            "tdp": 125,
            "cores": "20 (8P + 12E)",
            "threads": 28,
            "base_clock": "3.4 GHz",
            "boost_clock": "5.6 GHz",
            "cache": "33 MB Intel Smart Cache"
        }),
        "warranty": "3 ปี โดย Synnex",
        "rating": 4.9,
        "is_featured": 1
    },
    {
        "name": "AMD Ryzen 5 7600 3.8GHz 6C/12T (AM5)",
        "category": "cpu",
        "type": "hardware",
        "brand": "AMD",
        "price": 7290,
        "original_price": 7990,
        "stock": 15,
        "image_url": "https://images.unsplash.com/photo-1555617981-d115df4545d6?w=500&q=80",
        "description": "ซีพียูสถาปัตยกรรม Zen 4 ขนาด 5nm บนแพลตฟอร์ม AM5 รองรับ DDR5 และ PCIe 5.0 พร้อมกราฟิกในตัว Radeon",
        "specs_json": json.dumps({
            "socket": "AM5",
            "tdp": 65,
            "cores": "6",
            "threads": 12,
            "base_clock": "3.8 GHz",
            "boost_clock": "5.1 GHz",
            "cache": "32 MB L3 Cache"
        }),
        "warranty": "3 ปี โดย S-Trek / Synnex",
        "rating": 4.8,
        "is_featured": 1
    },
    {
        "name": "AMD Ryzen 7 7800X3D 4.2GHz 8C/16T (3D V-Cache)",
        "category": "cpu",
        "type": "hardware",
        "brand": "AMD",
        "price": 16900,
        "original_price": 17900,
        "stock": 8,
        "image_url": "https://images.unsplash.com/photo-1555617981-d115df4545d6?w=500&q=80",
        "description": "ราชาแห่งซีพียูสำหรับเล่นเกมตัวจริง ด้วยเทคโนโลยี 3D V-Cache 96MB ให้เฟรมเรตสูงสุดในทุกเกมระดับ AAA",
        "specs_json": json.dumps({
            "socket": "AM5",
            "tdp": 120,
            "cores": "8",
            "threads": 16,
            "base_clock": "4.2 GHz",
            "boost_clock": "5.0 GHz",
            "cache": "96 MB 3D V-Cache"
        }),
        "warranty": "3 ปี โดย Synnex",
        "rating": 5.0,
        "is_featured": 1
    },

    # ==================== MOTHERBOARD ====================
    {
        "name": "ASUS TUF GAMING B760-PLUS WIFI DDR5",
        "category": "motherboard",
        "type": "hardware",
        "brand": "ASUS",
        "price": 6490,
        "original_price": 6990,
        "stock": 14,
        "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=500&q=80",
        "description": "เมนบอร์ด Intel LGA1700 แข็งแกร่งทนทานระดับเกรดทหาร รองรับ DDR5, PCIe 5.0, Wi-Fi 6 และช่อง M.2 ถึง 3 ช่อง",
        "specs_json": json.dumps({
            "socket": "LGA1700",
            "ram_type": "DDR5",
            "form_factor": "ATX",
            "ram_slots": 4,
            "max_memory": "192 GB",
            "pcie_slots": "1x PCIe 5.0 x16, 1x PCIe 3.0 x16",
            "m2_slots": 3
        }),
        "warranty": "3 ปี โดย Synnex",
        "rating": 4.8,
        "is_featured": 1
    },
    {
        "name": "MSI PRO B760M-P DDR4",
        "category": "motherboard",
        "type": "hardware",
        "brand": "MSI",
        "price": 3290,
        "original_price": 3590,
        "stock": 20,
        "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=500&q=80",
        "description": "เมนบอร์ดคุ้มค่า Intel LGA1700 ไซส์ Micro-ATX รองรับแรม DDR4 ราคาประหยัด ตอบโจทย์การใช้งานทั่วไปและออฟฟิศ",
        "specs_json": json.dumps({
            "socket": "LGA1700",
            "ram_type": "DDR4",
            "form_factor": "Micro-ATX",
            "ram_slots": 4,
            "max_memory": "128 GB",
            "pcie_slots": "1x PCIe 4.0 x16",
            "m2_slots": 2
        }),
        "warranty": "3 ปี โดย WTG",
        "rating": 4.7,
        "is_featured": 0
    },
    {
        "name": "MSI MAG B650 TOMAHAWK WIFI (AM5 DDR5)",
        "category": "motherboard",
        "type": "hardware",
        "brand": "MSI",
        "price": 7590,
        "original_price": 8190,
        "stock": 10,
        "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=500&q=80",
        "description": "เมนบอร์ดซ็อกเก็ต AM5 ยอดนิยม ภาคจ่ายไฟ 14+2+1 Duet Rail รองรับ DDR5 ความเร็วสูง พร้อมระบบระบายความร้อน Extended Heatsink",
        "specs_json": json.dumps({
            "socket": "AM5",
            "ram_type": "DDR5",
            "form_factor": "ATX",
            "ram_slots": 4,
            "max_memory": "192 GB",
            "pcie_slots": "1x PCIe 4.0 x16",
            "m2_slots": 3
        }),
        "warranty": "3 ปี โดย Synnex",
        "rating": 4.9,
        "is_featured": 1
    },
    {
        "name": "ASRock B650M-HDV/M.2 (AM5 DDR5)",
        "category": "motherboard",
        "type": "hardware",
        "brand": "ASRock",
        "price": 3890,
        "original_price": 4290,
        "stock": 16,
        "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=500&q=80",
        "description": "เมนบอร์ด AM5 Micro-ATX ราคาเป็นมิตร ภาคจ่ายไฟ 8+2+1 Phase รองรับ DDR5 และ PCIe 5.0 M.2 Blazing",
        "specs_json": json.dumps({
            "socket": "AM5",
            "ram_type": "DDR5",
            "form_factor": "Micro-ATX",
            "ram_slots": 2,
            "max_memory": "96 GB",
            "pcie_slots": "1x PCIe 4.0 x16",
            "m2_slots": 2
        }),
        "warranty": "3 ปี โดย S-Trek",
        "rating": 4.6,
        "is_featured": 0
    },

    # ==================== RAM ====================
    {
        "name": "Kingston FURY Beast DDR5 32GB (16GBx2) 6000MHz Black",
        "category": "ram",
        "type": "hardware",
        "brand": "Kingston",
        "price": 3990,
        "original_price": 4390,
        "stock": 25,
        "image_url": "https://images.unsplash.com/photo-1562976540-1502c2145186?w=500&q=80",
        "description": "แรม DDR5 ความเร็วบัส 6000MHz รองรับทั้ง Intel XMP 3.0 และ AMD EXPO ซิงค์ระบายความร้อนอะลูมิเนียมเรียบหรู",
        "specs_json": json.dumps({
            "ram_type": "DDR5",
            "capacity": "32GB (16GBx2)",
            "speed": "6000 MHz",
            "cas_latency": "CL30",
            "voltage": "1.35V",
            "rgb": False
        }),
        "warranty": "Lifetime (ตลอดอายุการใช้งาน) โดย Synnex",
        "rating": 4.9,
        "is_featured": 1
    },
    {
        "name": "Corsair VENGEANCE RGB DDR5 32GB (16GBx2) 6000MHz White",
        "category": "ram",
        "type": "hardware",
        "brand": "Corsair",
        "price": 4590,
        "original_price": 4990,
        "stock": 18,
        "image_url": "https://images.unsplash.com/photo-1562976540-1502c2145186?w=500&q=80",
        "description": "แรมเกมมิ่งสีขาวสวยงาม ไฟ RGB ปรับแต่งได้ผ่านซอฟต์แวร์ iCUE บัส 6000MHz พร้อม XMP 3.0",
        "specs_json": json.dumps({
            "ram_type": "DDR5",
            "capacity": "32GB (16GBx2)",
            "speed": "6000 MHz",
            "cas_latency": "CL36",
            "voltage": "1.35V",
            "rgb": True
        }),
        "warranty": "Lifetime โดย Ascenti Resources",
        "rating": 4.9,
        "is_featured": 1
    },
    {
        "name": "Kingston FURY Beast DDR4 16GB (8GBx2) 3200MHz Black",
        "category": "ram",
        "type": "hardware",
        "brand": "Kingston",
        "price": 1490,
        "original_price": 1690,
        "stock": 35,
        "image_url": "https://images.unsplash.com/photo-1562976540-1502c2145186?w=500&q=80",
        "description": "แรม DDR4 มาตรฐานยอดนิยม 16GB Dual Channel บัส 3200MHz เสถียรและประหยัดสำหรับบอร์ด DDR4",
        "specs_json": json.dumps({
            "ram_type": "DDR4",
            "capacity": "16GB (8GBx2)",
            "speed": "3200 MHz",
            "cas_latency": "CL16",
            "voltage": "1.35V",
            "rgb": False
        }),
        "warranty": "Lifetime โดย Synnex",
        "rating": 4.8,
        "is_featured": 0
    },

    # ==================== GPU ====================
    {
        "name": "MSI GeForce RTX 4060 VENTUS 2X BLACK 8G OC",
        "category": "gpu",
        "type": "hardware",
        "brand": "MSI",
        "price": 10900,
        "original_price": 11900,
        "stock": 15,
        "image_url": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500&q=80",
        "description": "การ์ดจอ Ada Lovelace รองรับ DLSS 3 และ Full Ray Tracing เล่นเกม 1080p ลื่นไหลทุกเกม กินไฟต่ำเพียง 115W",
        "specs_json": json.dumps({
            "tdp": 115,
            "vram": "8GB GDDR6",
            "recommended_psu": 550,
            "length_mm": 199,
            "power_connectors": "1x 8-pin",
            "outputs": "3x DisplayPort 1.4a, 1x HDMI 2.1a"
        }),
        "warranty": "3 ปี โดย WTG",
        "rating": 4.8,
        "is_featured": 1
    },
    {
        "name": "ASUS TUF Gaming GeForce RTX 4070 SUPER 12GB GDDR6X",
        "category": "gpu",
        "type": "hardware",
        "brand": "ASUS",
        "price": 24900,
        "original_price": 26900,
        "stock": 9,
        "image_url": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500&q=80",
        "description": "การ์ดจอระดับ 1440p 2K ตัวจบ คูดาคอร์เพิ่มขึ้น ระบบพัดลม Axial-tech 3 ตัว และโครงสร้างโลหะเสริมความแข็งแรง",
        "specs_json": json.dumps({
            "tdp": 220,
            "vram": "12GB GDDR6X",
            "recommended_psu": 650,
            "length_mm": 301,
            "power_connectors": "1x 16-pin (12VHPWR)",
            "outputs": "3x DisplayPort 1.4a, 1x HDMI 2.1a"
        }),
        "warranty": "3 ปี โดย Synnex",
        "rating": 5.0,
        "is_featured": 1
    },
    {
        "name": "GIGABYTE GeForce RTX 4080 SUPER GAMING OC 16GB",
        "category": "gpu",
        "type": "hardware",
        "brand": "GIGABYTE",
        "price": 38900,
        "original_price": 42000,
        "stock": 5,
        "image_url": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500&q=80",
        "description": "การ์ดจอไฮเอนด์สำหรับ 4K Ultra และงาน Render 3D หนักๆ ระบบระบายความร้อน WINDFORCE พร้อม Dual BIOS",
        "specs_json": json.dumps({
            "tdp": 320,
            "vram": "16GB GDDR6X",
            "recommended_psu": 750,
            "length_mm": 342,
            "power_connectors": "1x 16-pin",
            "outputs": "3x DisplayPort 1.4a, 1x HDMI 2.1a"
        }),
        "warranty": "3+1 ปี โดย Synnex",
        "rating": 4.9,
        "is_featured": 1
    },
    {
        "name": "Sapphire PULSE AMD Radeon RX 7800 XT 16GB",
        "category": "gpu",
        "type": "hardware",
        "brand": "Sapphire",
        "price": 18900,
        "original_price": 20500,
        "stock": 8,
        "image_url": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500&q=80",
        "description": "ความคุ้มค่าสาย AMD แรมการ์ดจอจุใจ 16GB สถาปัตยกรรม RDNA 3 เหมาะกับการเล่นเกม 1440p ปรับภาพสุด",
        "specs_json": json.dumps({
            "tdp": 263,
            "vram": "16GB GDDR6",
            "recommended_psu": 700,
            "length_mm": 280,
            "power_connectors": "2x 8-pin",
            "outputs": "2x DisplayPort 2.1, 2x HDMI 2.1"
        }),
        "warranty": "3 ปี โดย S-Trek",
        "rating": 4.8,
        "is_featured": 0
    },

    # ==================== STORAGE ====================
    {
        "name": "Samsung 990 PRO NVMe M.2 SSD 1TB (PCIe 4.0)",
        "category": "storage",
        "type": "hardware",
        "brand": "Samsung",
        "price": 4190,
        "original_price": 4590,
        "stock": 22,
        "image_url": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=500&q=80",
        "description": "SSD ตัวแรงระดับตำนาน ความเร็วอ่านสูงสุด 7,450 MB/s และเขียน 6,900 MB/s โหลดเกมและตัดต่อวิดีโอทันใจ",
        "specs_json": json.dumps({
            "capacity": "1TB",
            "interface": "PCIe 4.0 x4, NVMe 2.0",
            "read_speed": "7,450 MB/s",
            "write_speed": "6,900 MB/s",
            "form_factor": "M.2 2280"
        }),
        "warranty": "5 ปี โดย Ascenti Resources",
        "rating": 4.9,
        "is_featured": 1
    },
    {
        "name": "WD Black SN850X NVMe M.2 SSD 2TB (PCIe 4.0)",
        "category": "storage",
        "type": "hardware",
        "brand": "Western Digital",
        "price": 6790,
        "original_price": 7290,
        "stock": 14,
        "image_url": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=500&q=80",
        "description": "ความจุขนาดใหญ่ 2TB ความเร็วอ่าน 7,300 MB/s พร้อมฟีเจอร์ Game Mode 2.0 ช่วยลดเวลาโหลดฉากเกม",
        "specs_json": json.dumps({
            "capacity": "2TB",
            "interface": "PCIe 4.0 x4, NVMe",
            "read_speed": "7,300 MB/s",
            "write_speed": "6,600 MB/s",
            "form_factor": "M.2 2280"
        }),
        "warranty": "5 ปี โดย Synnex",
        "rating": 4.9,
        "is_featured": 0
    },
    {
        "name": "Kingston NV2 NVMe M.2 SSD 1TB (PCIe 4.0)",
        "category": "storage",
        "type": "hardware",
        "brand": "Kingston",
        "price": 2190,
        "original_price": 2490,
        "stock": 40,
        "image_url": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=500&q=80",
        "description": "SSD M.2 PCIe 4.0 ราคาประหยัด ความเร็วอ่าน 3,500 MB/s เหมาะกับการอัปเกรดเครื่องหรือใช้งานทั่วไป",
        "specs_json": json.dumps({
            "capacity": "1TB",
            "interface": "PCIe 4.0 x4, NVMe",
            "read_speed": "3,500 MB/s",
            "write_speed": "2,100 MB/s",
            "form_factor": "M.2 2280"
        }),
        "warranty": "3 ปี โดย Synnex",
        "rating": 4.7,
        "is_featured": 0
    },

    # ==================== PSU ====================
    {
        "name": "CORSAIR RM750e 750W 80 PLUS Gold Fully Modular (ATX 3.0)",
        "category": "psu",
        "type": "hardware",
        "brand": "Corsair",
        "price": 3890,
        "original_price": 4290,
        "stock": 18,
        "image_url": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500&q=80",
        "description": "พาวเวอร์ซัพพลายมาตรฐาน ATX 3.0 และ PCIe 5.0 พร้อมสาย 12VHPWR สำหรับการ์ดจอ RTX 40 Series พัดลมเงียบ Zero RPM",
        "specs_json": json.dumps({
            "wattage": 750,
            "rating": "80 PLUS Gold",
            "modular": "Fully Modular",
            "fan_size": "120mm",
            "pcie_gen5": True
        }),
        "warranty": "7 ปี โดย Ascenti Resources",
        "rating": 4.9,
        "is_featured": 1
    },
    {
        "name": "CORSAIR RM850x 850W 80 PLUS Gold Fully Modular",
        "category": "psu",
        "type": "hardware",
        "brand": "Corsair",
        "price": 4990,
        "original_price": 5490,
        "stock": 12,
        "image_url": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500&q=80",
        "description": "คาปาซิเตอร์เกรดพรีเมียมจากญี่ปุ่น 105°C จ่ายไฟนิ่งและเสถียร รองรับสเปคระดับไฮเอนด์",
        "specs_json": json.dumps({
            "wattage": 850,
            "rating": "80 PLUS Gold",
            "modular": "Fully Modular",
            "fan_size": "135mm Magnetic Levitation",
            "pcie_gen5": True
        }),
        "warranty": "10 ปี โดย Ascenti Resources",
        "rating": 5.0,
        "is_featured": 0
    },
    {
        "name": "Cooler Master MWE 650W V2 Bronze",
        "category": "psu",
        "type": "hardware",
        "brand": "Cooler Master",
        "price": 2090,
        "original_price": 2390,
        "stock": 25,
        "image_url": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500&q=80",
        "description": "พาวเวอร์ซัพพลาย 650W มาตรฐาน 80 Plus Bronze คุ้มค่าและปลอดภัยสำหรับคอมพิวเตอร์ระดับเริ่มต้นและระดับกลาง",
        "specs_json": json.dumps({
            "wattage": 650,
            "rating": "80 PLUS Bronze",
            "modular": "Non-Modular",
            "fan_size": "120mm HDB",
            "pcie_gen5": False
        }),
        "warranty": "5 ปี โดย Synnex",
        "rating": 4.7,
        "is_featured": 0
    },

    # ==================== CASE ====================
    {
        "name": "NZXT H5 Flow RGB (Black)",
        "category": "case",
        "type": "hardware",
        "brand": "NZXT",
        "price": 3590,
        "original_price": 3890,
        "stock": 10,
        "image_url": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500&q=80",
        "description": "เคส Mid-Tower แผงหน้า Mesh ถ่ายเทอากาศได้ดีเยี่ยม พร้อมพัดลม RGB และพัดลมเฉียงเป่าระบายความร้อนการ์ดจอโดยเฉพาะ",
        "specs_json": json.dumps({
            "form_factor_support": "ATX, Micro-ATX, Mini-ITX",
            "max_gpu_length": "365mm",
            "max_cpu_cooler_height": "165mm",
            "radiator_support": "Up to 280mm",
            "color": "Black"
        }),
        "warranty": "2 ปี โดย Engine",
        "rating": 4.9,
        "is_featured": 1
    },
    {
        "name": "Montech AIR 100 ARGB (Black)",
        "category": "case",
        "type": "hardware",
        "brand": "Montech",
        "price": 1690,
        "original_price": 1890,
        "stock": 20,
        "image_url": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500&q=80",
        "description": "เคส Micro-ATX ยอดนิยม แถมพัดลม ARGB ให้ถึง 4 ตัว ฝาข้างกระจกนิรภัยเปิดแบบบานพับ สะดวกและคุ้มค่าสุดๆ",
        "specs_json": json.dumps({
            "form_factor_support": "Micro-ATX, Mini-ITX",
            "max_gpu_length": "330mm",
            "max_cpu_cooler_height": "161mm",
            "radiator_support": "Up to 280mm",
            "color": "Black"
        }),
        "warranty": "1 ปี โดย Ascenti Resources",
        "rating": 4.8,
        "is_featured": 0
    },
    {
        "name": "Lian Li O11 Dynamic EVO (White)",
        "category": "case",
        "type": "hardware",
        "brand": "Lian Li",
        "price": 5490,
        "original_price": 5890,
        "stock": 6,
        "image_url": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500&q=80",
        "description": "เคสตู้ปลาในตำนาน ปรับเปลี่ยนเลย์เอาต์กลับด้านได้ กระจกสองด้านไร้เสากั้น โชว์ชุดน้ำและชิ้นส่วนได้สวยงามตระการตา",
        "specs_json": json.dumps({
            "form_factor_support": "E-ATX, ATX, Micro-ATX, Mini-ITX",
            "max_gpu_length": "426mm",
            "max_cpu_cooler_height": "167mm",
            "radiator_support": "Up to 360mm x3",
            "color": "White"
        }),
        "warranty": "1 ปี โดย Ascenti Resources",
        "rating": 5.0,
        "is_featured": 1
    },

    # ==================== COOLER ====================
    {
        "name": "Thermalright Peerless Assassin 120 SE",
        "category": "cooler",
        "type": "hardware",
        "brand": "Thermalright",
        "price": 1290,
        "original_price": 1490,
        "stock": 25,
        "image_url": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500&q=80",
        "description": "ฮีตซิงก์ลมระบายความร้อน Dual Tower 6 ท่อไปป์ ประสิทธิภาพเทียบเท่าชุดน้ำ 240mm ในราคาเบาๆ",
        "specs_json": json.dumps({
            "type": "Air Cooler Dual Tower",
            "tdp_rating": "245W",
            "socket_support": "LGA1700, LGA1200, AM5, AM4",
            "height": "155mm",
            "fan_count": 2
        }),
        "warranty": "3 ปี โดย Speed Gaming",
        "rating": 4.9,
        "is_featured": 1
    },
    {
        "name": "NZXT Kraken 240 RGB Liquid Cooler (Black)",
        "category": "cooler",
        "type": "hardware",
        "brand": "NZXT",
        "price": 5590,
        "original_price": 5990,
        "stock": 8,
        "image_url": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=500&q=80",
        "description": "ชุดระบายความร้อนด้วยน้ำแบบระบบปิด AIO หม้อน้ำ 240mm พร้อมหน้าจอ LCD ขนาด 1.54 นิ้ว แสดงอุณหภูมิหรือภาพ GIF สดๆ",
        "specs_json": json.dumps({
            "type": "Liquid Cooler AIO 240mm",
            "tdp_rating": "280W",
            "socket_support": "LGA1700, AM5, AM4",
            "radiator_size": "240mm",
            "has_screen": True
        }),
        "warranty": "6 ปี โดย Engine",
        "rating": 4.9,
        "is_featured": 0
    },

    # ==================== MONITOR ====================
    {
        "name": "LG UltraGear 27GR75Q-B 27\" IPS 2K QHD 165Hz",
        "category": "monitor",
        "type": "hardware",
        "brand": "LG",
        "price": 7990,
        "original_price": 8990,
        "stock": 12,
        "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=500&q=80",
        "description": "จอเกมมิ่ง IPS ความละเอียด 2560x1440 (2K) รีเฟรชเรต 165Hz 1ms (GtG) รองรับ HDR10 และ G-Sync Compatible สีสันคมชัดสมจริง",
        "specs_json": json.dumps({
            "screen_size": "27 Inch",
            "resolution": "2560 x 1440 (2K QHD)",
            "panel": "IPS",
            "refresh_rate": "165 Hz",
            "response_time": "1ms (GtG)",
            "hdr": "HDR10",
            "sync": "NVIDIA G-Sync & AMD FreeSync Premium"
        }),
        "warranty": "3 ปี แบบ On-site Service โดย LG Thailand",
        "rating": 4.9,
        "is_featured": 1
    },
    {
        "name": "AOC 24G2SP 23.8\" IPS Full HD 165Hz",
        "category": "monitor",
        "type": "hardware",
        "brand": "AOC",
        "price": 4190,
        "original_price": 4590,
        "stock": 19,
        "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=500&q=80",
        "description": "จอ 1080p ขนาด 24 นิ้ว ขวัญใจสาย E-Sports รีเฟรชเรต 165Hz พาเนล IPS สีสด ตอบสนองฉับไว ปรับหมุนจอแนวตั้งได้",
        "specs_json": json.dumps({
            "screen_size": "23.8 Inch",
            "resolution": "1920 x 1080 (Full HD)",
            "panel": "IPS",
            "refresh_rate": "165 Hz",
            "response_time": "1ms (MPRT)"
        }),
        "warranty": "3 ปี โดย Synnex",
        "rating": 4.8,
        "is_featured": 0
    },

    # ==================== SOFTWARE ====================
    {
        "name": "Microsoft Windows 11 Home 64-bit (FPP / USB Box)",
        "category": "software_os",
        "type": "software",
        "brand": "Microsoft",
        "price": 4890,
        "original_price": 5290,
        "stock": 30,
        "image_url": "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=500&q=80",
        "description": "ระบบปฏิบัติการของแท้แบบ FPP (Full Packaged Product) มาพร้อมแฟลชไดรฟ์แท้ ย้ายเครื่องได้ตลอดชีวิต เหมาะสำหรับคอมพิวเตอร์ใช้งานทั่วไปและเล่นเกม",
        "specs_json": json.dumps({
            "license_type": "FPP (Retail Box with USB)",
            "duration": "Lifetime (ตลอดอายุการใช้งาน)",
            "devices": "1 PC",
            "transferable": "ย้ายเครื่องได้",
            "delivery_method": "จัดส่งกล่องพัสดุพร้อมรหัสหรือรับที่หน้าร้าน"
        }),
        "warranty": "รับประกันลิขสิทธิ์แท้ 100% ตลอดชีพโดย Microsoft Thailand",
        "rating": 5.0,
        "is_featured": 1
    },
    {
        "name": "Microsoft Windows 11 Pro 64-bit (ESD Digital License)",
        "category": "software_os",
        "type": "software",
        "brand": "Microsoft",
        "price": 5790,
        "original_price": 6490,
        "stock": 50,
        "image_url": "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=500&q=80",
        "description": "ลิขสิทธิ์ระบบปฏิบัติการ Windows 11 Pro แท้ รองรับ BitLocker, Remote Desktop, Hyper-V ส่งคีย์ทันทีทางอีเมลหลังชำระเงิน",
        "specs_json": json.dumps({
            "license_type": "ESD (Electronic Software Delivery)",
            "duration": "Lifetime",
            "devices": "1 PC",
            "transferable": "ยึดติดกับ Microsoft Account",
            "delivery_method": "จัดส่ง Digital Key ทันทีผ่านทาง Email / SMS"
        }),
        "warranty": "รับประกันลิขสิทธิ์แท้ 100% ตลอดชีพ",
        "rating": 4.9,
        "is_featured": 1
    },
    {
        "name": "Microsoft Office Home & Student 2024 (1 PC/Mac Lifetime)",
        "category": "software_office",
        "type": "software",
        "brand": "Microsoft",
        "price": 4290,
        "original_price": 4790,
        "stock": 35,
        "image_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=500&q=80",
        "description": "ชุดโปรแกรมออฟฟิศยอดนิยม Word, Excel, PowerPoint, OneNote รุ่นใหม่ล่าสุด 2024 ซื้อครั้งเดียวใช้งานได้ตลอดชีพ ไม่มีค่าบริการรายปี",
        "specs_json": json.dumps({
            "license_type": "One-time Purchase (Lifetime)",
            "duration": "ตลอดชีพ (ไม่มีวันหมดอายุ)",
            "devices": "1 PC หรือ 1 Mac",
            "included_apps": "Word, Excel, PowerPoint, OneNote",
            "delivery_method": "Digital License Key ทาง Email"
        }),
        "warranty": "รับประกันลิขสิทธิ์แท้โดย Microsoft",
        "rating": 4.9,
        "is_featured": 1
    },
    {
        "name": "Microsoft 365 Personal (1 User / 1 Year Subscription)",
        "category": "software_office",
        "type": "software",
        "brand": "Microsoft",
        "price": 2090,
        "original_price": 2390,
        "stock": 40,
        "image_url": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=500&q=80",
        "description": "ใช้งาน Office ครบชุดบนคอมฯ แท็บเล็ต สมาร์ตโฟน ได้สูงสุด 5 อุปกรณ์พร้อมกัน พร้อมพื้นที่คลาวด์ OneDrive ขนาด 1TB ปลอดภัยสูง",
        "specs_json": json.dumps({
            "license_type": "Subscription (รายปี)",
            "duration": "1 ปี (ต่ออายุได้)",
            "devices": "สูงสุด 5 อุปกรณ์ (PC, Mac, iOS, Android)",
            "cloud_storage": "1 TB OneDrive Cloud Storage",
            "delivery_method": "Digital Key ส่งทันที"
        }),
        "warranty": "Microsoft Official License 1 Year",
        "rating": 4.8,
        "is_featured": 0
    },
    {
        "name": "Kaspersky Plus Antivirus & Security (1 Device / 1 Year)",
        "category": "software_security",
        "type": "software",
        "brand": "Kaspersky",
        "price": 690,
        "original_price": 890,
        "stock": 60,
        "image_url": "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=500&q=80",
        "description": "โปรแกรมแอนตี้ไวรัสระดับโลก ป้องกันไวรัส มัลแวร์ แรนซัมแวร์ การแฮกข้อมูล พร้อมระบบ Safe Money ป้องกันธุรกรรมการเงิน และ Unlimited Fast VPN",
        "specs_json": json.dumps({
            "license_type": "Subscription 1 Year",
            "duration": "1 ปี",
            "devices": "1 Device (Windows, macOS, Android, iOS)",
            "features": "Real-time Antivirus, Anti-Phishing, Unlimited VPN, Safe Banking",
            "delivery_method": "ส่งรหัสทันทีทาง Email ภายใน 1 นาที"
        }),
        "warranty": "รับประกันอัปเดตฐานข้อมูลไวรัสตลอดระยะเวลา 1 ปี",
        "rating": 4.9,
        "is_featured": 1
    },
    {
        "name": "Bitdefender Total Security (3 Devices / 1 Year)",
        "category": "software_security",
        "type": "software",
        "brand": "Bitdefender",
        "price": 990,
        "original_price": 1290,
        "stock": 45,
        "image_url": "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=500&q=80",
        "description": "ความปลอดภัยครบวงจรสำหรับครอบครัว ปกป้องได้ถึง 3 อุปกรณ์พร้อมกัน ไม่หน่วงเครื่อง ตรวจจับภัยคุกคามแบบ Real-Time Zero-day",
        "specs_json": json.dumps({
            "license_type": "Subscription 1 Year",
            "duration": "1 ปี",
            "devices": "3 อุปกรณ์",
            "features": "Multi-layer Ransomware Protection, Firewall, Parental Control",
            "delivery_method": "ส่งรหัส Activation Code ผ่าน Email ทันที"
        }),
        "warranty": "Bitdefender Thailand 1 Year",
        "rating": 4.8,
        "is_featured": 0
    },
    {
        "name": "Internet Download Manager (IDM) Lifetime License (1 PC)",
        "category": "software_tools",
        "type": "software",
        "brand": "Tonec Inc.",
        "price": 890,
        "original_price": 990,
        "stock": 50,
        "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=500&q=80",
        "description": "โปรแกรมช่วยดาวน์โหลดไฟล์ยอดนิยมอันดับหนึ่ง เร่งสปีดดาวน์โหลดเร็วขึ้นสูงสุด 5 เท่า รองรับเบราว์เซอร์ทุกตัว คีย์แท้ตลอดชีพ",
        "specs_json": json.dumps({
            "license_type": "Lifetime (ตลอดชีพ)",
            "duration": "ใช้ได้ตลอดไป + อัปเดตฟรี 3 ปี",
            "devices": "1 PC",
            "delivery_method": "ส่งรหัสซีเรียลนัมเบอร์ทาง Email ทันที"
        }),
        "warranty": "ลิขสิทธิ์แท้ 100% จากผู้พัฒนา Tonec Inc.",
        "rating": 5.0,
        "is_featured": 0
    }
]

def seed():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Clear old products if any
    cursor.execute("DELETE FROM products")

    for p in PRODUCTS:
        cursor.execute('''
            INSERT INTO products (
                name, category, type, brand, price, original_price, stock,
                image_url, description, specs_json, warranty, rating, is_featured
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            p["name"], p["category"], p["type"], p["brand"], p["price"],
            p.get("original_price"), p.get("stock", 10), p["image_url"],
            p["description"], p["specs_json"], p["warranty"],
            p.get("rating", 4.8), p.get("is_featured", 0)
        ))

    conn.commit()
    conn.close()
    print(f"Successfully seeded {len(PRODUCTS)} products into {DB_PATH}")

if __name__ == '__main__':
    seed()
