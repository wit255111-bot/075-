// PC Builder Engine
let componentsData = {};
let presetsData = [];

const builderState = {
    cpu: null,
    motherboard: null,
    ram: null,
    gpu: null,
    storage: null,
    psu: null,
    case: null,
    cooler: null,
    monitor: null,
    software_os: null
};

const categoryLabels = {
    cpu: { name: "ซีพียู (CPU)", icon: "cpu", required: true },
    motherboard: { name: "เมนบอร์ด (Motherboard)", icon: "server", required: true },
    ram: { name: "แรม (RAM)", icon: "database", required: true },
    gpu: { name: "การ์ดจอ (Graphic Card / GPU)", icon: "hard-drive", required: false },
    storage: { name: "ที่จัดเก็บข้อมูล (SSD M.2)", icon: "save", required: true },
    psu: { name: "พาวเวอร์ซัพพลาย (Power Supply)", icon: "zap", required: true },
    case: { name: "เคสคอมพิวเตอร์ (Case)", icon: "box", required: true },
    cooler: { name: "พัดลม / ชุดน้ำระบายความร้อน (Cooler)", icon: "wind", required: false },
    monitor: { name: "จอมอนิเตอร์ (Monitor)", icon: "monitor", required: false },
    software_os: { name: "ระบบปฏิบัติการ (Windows OS)", icon: "grid", required: false }
};

let currentModalCategory = null;

// Initialize
async function initPCBuilder() {
    try {
        const [compRes, presetRes] = await Promise.all([
            fetch('/api/builder/components'),
            fetch('/api/builder/presets')
        ]);
        componentsData = await compRes.json();
        presetsData = await presetRes.json();

        renderSlots();
        renderPresets();
        updateSummary();
    } catch (err) {
        console.error("Error loading builder data:", err);
    }
}

// Render the builder slots
function renderSlots() {
    const container = document.getElementById('builder-slots');
    if (!container) return;

    let html = '';
    for (const [cat, meta] of Object.entries(categoryLabels)) {
        const item = builderState[cat];
        if (item) {
            // Selected state
            html += `
                <div class="bg-slate-800/80 border border-blue-500/30 hover:border-blue-500/60 transition rounded-2xl p-4 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-lg shadow-black/20" id="slot-${cat}">
                    <div class="flex items-center gap-4 flex-1 min-w-0">
                        <img src="${item.image_url}" alt="${item.name}" class="w-16 h-16 rounded-xl object-cover bg-slate-900 border border-slate-700 flex-shrink-0" onerror="this.src='https://via.placeholder.com/80?text=Part'">
                        <div class="min-w-0 flex-1">
                            <div class="flex items-center gap-2">
                                <span class="text-xs uppercase tracking-wider font-semibold text-blue-400 bg-blue-950/60 px-2 py-0.5 rounded border border-blue-800/40">${meta.name}</span>
                                <span class="text-xs text-slate-400">${item.brand}</span>
                            </div>
                            <h4 class="text-white font-medium text-sm sm:text-base truncate mt-1">${item.name}</h4>
                            <p class="text-xs text-slate-400 mt-0.5 truncate">${getShortSpecString(item)}</p>
                        </div>
                    </div>
                    <div class="flex items-center justify-between md:justify-end w-full md:w-auto gap-4 pt-2 md:pt-0 border-t md:border-t-0 border-slate-700/60">
                        <span class="text-lg font-bold text-white">฿${item.price.toLocaleString()}</span>
                        <div class="flex items-center gap-2">
                            <button onclick="openSelectModal('${cat}')" class="px-3 py-1.5 bg-slate-700 hover:bg-slate-600 text-slate-200 text-xs font-medium rounded-lg transition">เปลี่ยน</button>
                            <button onclick="removeComponent('${cat}')" class="p-1.5 text-slate-400 hover:text-red-400 rounded-lg transition" title="ลบออก">
                                <i data-lucide="trash-2" class="w-4 h-4"></i>
                            </button>
                        </div>
                    </div>
                </div>
            `;
        } else {
            // Empty slot state
            html += `
                <div class="bg-slate-800/40 border border-dashed border-slate-700 hover:border-blue-500/50 hover:bg-slate-800/60 transition rounded-2xl p-4 flex items-center justify-between gap-4 cursor-pointer" onclick="openSelectModal('${cat}')" id="slot-${cat}">
                    <div class="flex items-center gap-4">
                        <div class="w-16 h-16 rounded-xl bg-slate-800/80 border border-slate-700 flex items-center justify-center text-slate-400">
                            <i data-lucide="${meta.icon}" class="w-7 h-7 opacity-60"></i>
                        </div>
                        <div>
                            <div class="flex items-center gap-2">
                                <span class="text-xs font-semibold text-slate-300">${meta.name}</span>
                                ${meta.required ? '<span class="text-[10px] bg-red-950/60 text-red-400 border border-red-800/40 px-1.5 py-0.2 rounded font-medium">จำเป็น</span>' : '<span class="text-[10px] bg-slate-800 text-slate-400 px-1.5 py-0.2 rounded">ตัวเลือกเสริม</span>'}
                            </div>
                            <p class="text-xs text-slate-400 mt-1">คลิกเพื่อเลือก ${meta.name}</p>
                        </div>
                    </div>
                    <button class="flex items-center gap-1.5 px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-medium rounded-xl shadow-lg shadow-blue-600/20 transition">
                        <i data-lucide="plus" class="w-4 h-4"></i>
                        <span>เลือกสินค้า</span>
                    </button>
                </div>
            `;
        }
    }

    container.innerHTML = html;
    if (window.lucide) lucide.createIcons();
}

function getShortSpecString(item) {
    if (!item.specs) return item.warranty || '';
    const parts = [];
    if (item.specs.socket) parts.push(`Socket ${item.specs.socket}`);
    if (item.specs.ram_type) parts.push(`${item.specs.ram_type}`);
    if (item.specs.capacity) parts.push(`${item.specs.capacity}`);
    if (item.specs.speed) parts.push(`${item.specs.speed}`);
    if (item.specs.vram) parts.push(`VRAM ${item.specs.vram}`);
    if (item.specs.wattage) parts.push(`${item.specs.wattage}W`);
    if (item.specs.license_type) parts.push(`${item.specs.license_type}`);
    if (item.warranty) parts.push(`ประกัน ${item.warranty}`);
    return parts.join(' • ');
}

// Open Component Selection Modal
function openSelectModal(cat) {
    currentModalCategory = cat;
    const meta = categoryLabels[cat];
    const items = componentsData[cat] || [];

    document.getElementById('modal-cat-title').innerText = `เลือก ${meta.name}`;
    document.getElementById('modal-search-input').value = '';

    renderModalItems(items);
    document.getElementById('select-modal').classList.remove('hidden');
    document.getElementById('select-modal').classList.add('flex');
}

function closeModal() {
    document.getElementById('select-modal').classList.add('hidden');
    document.getElementById('select-modal').classList.remove('flex');
    currentModalCategory = null;
}

function renderModalItems(items) {
    const list = document.getElementById('modal-items-list');
    if (!list) return;

    if (items.length === 0) {
        list.innerHTML = `
            <div class="text-center py-12 text-slate-400">
                <i data-lucide="package-search" class="w-12 h-12 mx-auto mb-3 opacity-40"></i>
                <p>ไม่พบสินค้าในหมวดหมู่นี้</p>
            </div>
        `;
        if (window.lucide) lucide.createIcons();
        return;
    }

    let html = '';
    items.forEach(item => {
        // Compatibility hint check
        let compatBadge = '';
        if (currentModalCategory === 'cpu' && builderState.motherboard && item.specs && builderState.motherboard.specs) {
            if (item.specs.socket !== builderState.motherboard.specs.socket) {
                compatBadge = `<span class="text-[10px] bg-red-950/70 text-red-400 border border-red-800/50 px-2 py-0.5 rounded font-medium">⚠️ ซ็อกเก็ตไม่ตรงกับบอร์ด (${builderState.motherboard.specs.socket})</span>`;
            } else {
                compatBadge = `<span class="text-[10px] bg-emerald-950/70 text-emerald-400 border border-emerald-800/50 px-2 py-0.5 rounded font-medium">✓ เข้ากันได้กับเมนบอร์ด</span>`;
            }
        } else if (currentModalCategory === 'motherboard' && builderState.cpu && item.specs && builderState.cpu.specs) {
            if (item.specs.socket !== builderState.cpu.specs.socket) {
                compatBadge = `<span class="text-[10px] bg-red-950/70 text-red-400 border border-red-800/50 px-2 py-0.5 rounded font-medium">⚠️ ซ็อกเก็ตไม่ตรงกับ CPU (${builderState.cpu.specs.socket})</span>`;
            } else {
                compatBadge = `<span class="text-[10px] bg-emerald-950/70 text-emerald-400 border border-emerald-800/50 px-2 py-0.5 rounded font-medium">✓ ซ็อกเก็ตตรงกับ CPU</span>`;
            }
        } else if (currentModalCategory === 'ram' && builderState.motherboard && item.specs && builderState.motherboard.specs) {
            if (item.specs.ram_type !== builderState.motherboard.specs.ram_type) {
                compatBadge = `<span class="text-[10px] bg-red-950/70 text-red-400 border border-red-800/50 px-2 py-0.5 rounded font-medium">⚠️ ชนิดแรมไม่ตรงกับบอร์ด (${builderState.motherboard.specs.ram_type})</span>`;
            } else {
                compatBadge = `<span class="text-[10px] bg-emerald-950/70 text-emerald-400 border border-emerald-800/50 px-2 py-0.5 rounded font-medium">✓ ชนิดแรมตรงกับเมนบอร์ด</span>`;
            }
        }

        html += `
            <div class="flex items-center justify-between p-3.5 bg-slate-800/60 hover:bg-slate-800 border border-slate-700/60 hover:border-blue-500/50 rounded-xl transition gap-4">
                <div class="flex items-center gap-3.5 flex-1 min-w-0">
                    <img src="${item.image_url}" alt="${item.name}" class="w-14 h-14 rounded-lg object-cover bg-slate-900 border border-slate-700 flex-shrink-0" onerror="this.src='https://via.placeholder.com/60?text=Hardware'">
                    <div class="min-w-0 flex-1">
                        <div class="flex items-center gap-2 flex-wrap">
                            <span class="text-xs font-semibold text-slate-400">${item.brand}</span>
                            ${compatBadge}
                        </div>
                        <h4 class="text-white text-sm font-medium truncate mt-0.5" title="${item.name}">${item.name}</h4>
                        <p class="text-xs text-slate-400 truncate mt-0.5">${getShortSpecString(item)}</p>
                    </div>
                </div>
                <div class="flex items-center gap-4 flex-shrink-0">
                    <div class="text-right">
                        <span class="text-base font-bold text-blue-400">฿${item.price.toLocaleString()}</span>
                        ${item.original_price ? `<p class="text-[11px] text-slate-500 line-through">฿${item.original_price.toLocaleString()}</p>` : ''}
                    </div>
                    <button onclick="selectComponent(${item.id})" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold rounded-lg shadow-md transition">เลือก</button>
                </div>
            </div>
        `;
    });

    list.innerHTML = html;
    if (window.lucide) lucide.createIcons();
}

function filterModalItems() {
    const q = document.getElementById('modal-search-input').value.toLowerCase().trim();
    const items = componentsData[currentModalCategory] || [];
    const filtered = items.filter(it => it.name.toLowerCase().includes(q) || it.brand.toLowerCase().includes(q));
    renderModalItems(filtered);
}

function selectComponent(itemId) {
    const items = componentsData[currentModalCategory] || [];
    const found = items.find(it => it.id === itemId);
    if (found) {
        builderState[currentModalCategory] = found;
        renderSlots();
        updateSummary();
        closeModal();
    }
}

function removeComponent(cat) {
    builderState[cat] = null;
    renderSlots();
    updateSummary();
}

function clearAllComponents() {
    if (confirm("คุณแน่ใจหรือไม่ว่าต้องการล้างชิ้นส่วนทั้งหมด?")) {
        for (const cat of Object.keys(builderState)) {
            builderState[cat] = null;
        }
        renderSlots();
        updateSummary();
    }
}

// Wattage & Compatibility Engine
function updateSummary() {
    let totalPrice = 0;
    let cpuTdp = 0;
    let gpuTdp = 0;
    let baseLoad = 70; // Fans, RAM, motherboard chipset, SSDs
    let selectedCount = 0;

    for (const [cat, item] of Object.entries(builderState)) {
        if (item) {
            totalPrice += item.price;
            selectedCount++;

            if (cat === 'cpu' && item.specs && item.specs.tdp) {
                cpuTdp = parseInt(item.specs.tdp) || 65;
            }
            if (cat === 'gpu' && item.specs && item.specs.tdp) {
                gpuTdp = parseInt(item.specs.tdp) || 150;
            }
        }
    }

    const estimatedWattage = (cpuTdp > 0 || gpuTdp > 0) ? (cpuTdp + gpuTdp + baseLoad) : 0;
    const recommendedWattage = estimatedWattage > 0 ? Math.ceil((estimatedWattage * 1.3) / 50) * 50 : 0;

    // Update Price elements
    const priceElem = document.getElementById('summary-total-price');
    const monthlyElem = document.getElementById('summary-monthly-price');
    const countElem = document.getElementById('summary-part-count');
    if (priceElem) priceElem.innerText = `฿${totalPrice.toLocaleString()}`;
    if (monthlyElem) monthlyElem.innerText = `฿${Math.round(totalPrice / 10).toLocaleString()}`;
    if (countElem) countElem.innerText = `${selectedCount} / 10 ชิ้นส่วน`;

    // Update Wattage elements
    const wattElem = document.getElementById('summary-wattage');
    const recWattElem = document.getElementById('summary-rec-wattage');
    const wattBar = document.getElementById('wattage-progress-bar');
    if (wattElem) wattElem.innerText = `${estimatedWattage} W`;
    if (recWattElem) recWattElem.innerText = `${recommendedWattage} W`;
    if (wattBar) {
        const percent = Math.min(100, Math.round((estimatedWattage / 1000) * 100));
        wattBar.style.width = `${percent}%`;
    }

    // Check Compatibility Alerts
    checkCompatibility(estimatedWattage, recommendedWattage);
}

function checkCompatibility(estWatt, recWatt) {
    const alertsContainer = document.getElementById('compatibility-alerts');
    if (!alertsContainer) return;

    const issues = [];
    const successes = [];

    // 1. CPU vs Motherboard Socket
    if (builderState.cpu && builderState.motherboard) {
        const cpuSocket = builderState.cpu.specs ? builderState.cpu.specs.socket : null;
        const mbSocket = builderState.motherboard.specs ? builderState.motherboard.specs.socket : null;

        if (cpuSocket && mbSocket) {
            if (cpuSocket !== mbSocket) {
                issues.push(`ซ็อกเก็ตไม่ตรงกัน: CPU ใช้ ${cpuSocket} แต่เมนบอร์ดใช้ ${mbSocket} (ไม่สามารถติดตั้งได้)`);
            } else {
                successes.push(`CPU และเมนบอร์ด ซ็อกเก็ตตรงกัน (${cpuSocket})`);
            }
        }
    }

    // 2. RAM Type vs Motherboard RAM Type
    if (builderState.ram && builderState.motherboard) {
        const ramType = builderState.ram.specs ? builderState.ram.specs.ram_type : null;
        const mbRamType = builderState.motherboard.specs ? builderState.motherboard.specs.ram_type : null;

        if (ramType && mbRamType) {
            if (ramType !== mbRamType) {
                issues.push(`ชนิดแรมไม่ตรงกัน: แรมเป็น ${ramType} แต่เมนบอร์ดรองรับ ${mbRamType}`);
            } else {
                successes.push(`เมนบอร์ดและแรมรองรับมาตรฐาน ${ramType}`);
            }
        }
    }

    // 3. PSU Wattage vs System Load
    if (builderState.psu && recWatt > 0) {
        const psuWatt = builderState.psu.specs ? builderState.psu.specs.wattage : 0;
        if (psuWatt > 0) {
            if (psuWatt < recWatt) {
                issues.push(`พาวเวอร์ซัพพลาย (${psuWatt}W) ต่ำกว่าที่แนะนำ (${recWatt}W) อาจเสี่ยงเครื่องดับเมื่อเล่นเกมหนัก`);
            } else {
                successes.push(`กำลังไฟ PSU เพียงพอต่อการใช้งาน (${psuWatt}W / แนะนำ ${recWatt}W)`);
            }
        }
    }

    // Render alert box
    if (issues.length > 0) {
        alertsContainer.innerHTML = `
            <div class="bg-rose-950/40 border border-rose-800/80 rounded-2xl p-4">
                <div class="flex items-center gap-2 text-rose-400 font-semibold mb-2">
                    <i data-lucide="alert-triangle" class="w-5 h-5"></i>
                    <span>พบปัญหาความเข้ากันได้ (${issues.length} รายการ)</span>
                </div>
                <ul class="text-xs text-rose-300 space-y-1.5 pl-7 list-disc">
                    ${issues.map(iss => `<li>${iss}</li>`).join('')}
                </ul>
            </div>
        `;
    } else if (successes.length > 0) {
        alertsContainer.innerHTML = `
            <div class="bg-emerald-950/40 border border-emerald-800/80 rounded-2xl p-4">
                <div class="flex items-center gap-2 text-emerald-400 font-semibold mb-2">
                    <i data-lucide="check-circle-2" class="w-5 h-5"></i>
                    <span>ชิ้นส่วนหลักเข้ากันได้สมบูรณ์แบบ!</span>
                </div>
                <ul class="text-xs text-emerald-300 space-y-1 pl-7 list-disc">
                    ${successes.map(s => `<li>${s}</li>`).join('')}
                </ul>
            </div>
        `;
    } else {
        alertsContainer.innerHTML = `
            <div class="bg-slate-800/60 border border-slate-700/60 rounded-2xl p-4 text-center text-slate-400 text-xs">
                <p>เลือก CPU และ เมนบอร์ด เพื่อเริ่มการตรวจสอบความเข้ากันได้อัตโนมัติ</p>
            </div>
        `;
    }

    if (window.lucide) lucide.createIcons();
}

// Preset Builds
function renderPresets() {
    const container = document.getElementById('preset-builds-list');
    if (!container) return;

    let html = '';
    presetsData.forEach((preset, idx) => {
        html += `
            <div class="bg-slate-800/70 border border-slate-700/80 hover:border-blue-500/60 rounded-2xl p-5 transition flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-2">
                        <span class="text-xs font-bold px-2.5 py-0.5 rounded-full bg-blue-900/60 text-blue-300 border border-blue-700/50">${preset.badge}</span>
                        <span class="text-sm font-bold text-white">~฿${preset.target_price.toLocaleString()}</span>
                    </div>
                    <h4 class="text-white font-semibold text-base mb-2">${preset.name}</h4>
                    <p class="text-xs text-slate-400 leading-relaxed mb-4">${preset.description}</p>
                </div>
                <button onclick="loadPreset(${idx})" class="w-full py-2.5 bg-blue-600/20 hover:bg-blue-600 text-blue-300 hover:text-white border border-blue-500/40 hover:border-transparent text-xs font-semibold rounded-xl transition flex items-center justify-center gap-2">
                    <i data-lucide="download" class="w-4 h-4"></i>
                    <span>โหลดสเปคนี้</span>
                </button>
            </div>
        `;
    });

    container.innerHTML = html;
    if (window.lucide) lucide.createIcons();
}

function loadPreset(idx) {
    const preset = presetsData[idx];
    if (!preset) return;

    for (const [cat, compName] of Object.entries(preset.components)) {
        const list = componentsData[cat] || [];
        const found = list.find(it => it.name.includes(compName) || compName.includes(it.name));
        if (found) {
            builderState[cat] = found;
        }
    }

    renderSlots();
    updateSummary();
    Cart.showToast(`โหลดสเปค "${preset.name}" เรียบร้อยแล้ว!`, 'success');

    // Scroll smoothly to builder slots
    document.getElementById('builder-slots').scrollIntoView({ behavior: 'smooth' });
}

// Add all build items to cart
function addAllToCart() {
    const items = Object.values(builderState).filter(item => item !== null);
    if (items.length === 0) {
        Cart.showToast('กรุณาเลือกชิ้นส่วนอย่างน้อย 1 ชิ้นก่อนเพิ่มลงตะกร้า', 'error');
        return;
    }
    Cart.addMultiple(items);
}

// Copy build specs to clipboard
function copyBuildSpecs() {
    const items = Object.entries(builderState).filter(([_, item]) => item !== null);
    if (items.length === 0) {
        Cart.showToast('ไม่มีชิ้นส่วนในสเปคคอม', 'error');
        return;
    }

    let text = "🖥️ สเปคคอมพิวเตอร์จัดโดย NEXUS TECH\n";
    text += "====================================\n";
    let total = 0;
    items.forEach(([cat, item]) => {
        text += `• ${categoryLabels[cat].name}: ${item.name} (฿${item.price.toLocaleString()})\n`;
        total += item.price;
    });
    text += "====================================\n";
    text += `💰 ราคารวมทั้งหมด: ฿${total.toLocaleString()}\n`;
    text += `สั่งซื้อและจัดสเปคคอมได้ที่: ${window.location.origin}/builder`;

    navigator.clipboard.writeText(text).then(() => {
        Cart.showToast('คัดลอกสเปคคอมลงคลิปบอร์ดแล้ว!', 'success');
    }).catch(() => {
        Cart.showToast('ไม่สามารถคัดลอกได้', 'error');
    });
}

// Print Official Quotation
function printQuotation() {
    const items = Object.entries(builderState).filter(([_, item]) => item !== null);
    if (items.length === 0) {
        Cart.showToast('กรุณาเลือกชิ้นส่วนอย่างน้อย 1 ชิ้นเพื่อพิมพ์ใบเสนอราคา', 'error');
        return;
    }

    const quotationCode = `QT-${Math.floor(100000 + Math.random() * 900000)}`;
    const today = new Date().toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' });
    const expireDate = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' });

    let tableRows = '';
    let total = 0;

    items.forEach(([cat, item], index) => {
        total += item.price;
        tableRows += `
            <tr class="border-b border-slate-200">
                <td class="py-2.5 px-3 text-center text-xs text-slate-600">${index + 1}</td>
                <td class="py-2.5 px-3">
                    <p class="font-semibold text-slate-800 text-xs">${item.name}</p>
                    <p class="text-[10px] text-slate-500">${categoryLabels[cat].name} • ประกัน: ${item.warranty || 'ตามเงื่อนไขผู้ผลิต'}</p>
                </td>
                <td class="py-2.5 px-3 text-center text-xs text-slate-700">1</td>
                <td class="py-2.5 px-3 text-right text-xs text-slate-700">฿${item.price.toLocaleString()}</td>
                <td class="py-2.5 px-3 text-right text-xs font-bold text-slate-900">฿${item.price.toLocaleString()}</td>
            </tr>
        `;
    });

    const quotationHTML = `
        <div class="p-8 max-w-4xl mx-auto font-sans text-slate-800 bg-white" id="printable-quotation">
            <!-- Header -->
            <div class="flex justify-between items-start border-b-2 border-blue-600 pb-4 mb-6">
                <div>
                    <h1 class="text-2xl font-black text-blue-700 tracking-wider">NEXUS TECH CO., LTD.</h1>
                    <p class="text-xs text-slate-500 mt-1">ผู้นำเข้าและจำหน่ายอุปกรณ์คอมพิวเตอร์และซอฟต์แวร์ลิขสิทธิ์แท้ 100%</p>
                    <p class="text-xs text-slate-500">โทร: 02-999-8888 | อีเมล: sales@nexustech.co.th | เว็บไซต์: www.nexustech.co.th</p>
                </div>
                <div class="text-right">
                    <span class="text-xl font-bold bg-blue-100 text-blue-800 px-3 py-1 rounded">ใบเสนอราคา (Quotation)</span>
                    <p class="text-xs text-slate-600 mt-2 font-mono font-bold">เลขที่: ${quotationCode}</p>
                    <p class="text-xs text-slate-500">วันที่: ${today}</p>
                    <p class="text-xs text-slate-500">ใช้ได้ถึง: ${expireDate}</p>
                </div>
            </div>

            <!-- Customer / Project Info -->
            <div class="bg-slate-50 p-4 rounded-lg mb-6 border border-slate-200 text-xs flex justify-between">
                <div>
                    <p class="font-bold text-slate-800 mb-1">ข้อมูลลูกค้า / ผู้ติดต่อ:</p>
                    <p class="text-slate-600">ชื่อ: ลูกค้าผู้มีอุปการคุณ</p>
                    <p class="text-slate-600">โครงการ: ชุดจัดสเปคคอมพิวเตอร์ประสิทธิภาพสูง (DIY Custom PC)</p>
                </div>
                <div class="text-right">
                    <p class="font-bold text-slate-800 mb-1">เงื่อนไขการรับประกันและบริการ:</p>
                    <p class="text-slate-600">✓ ประกอบและลงโปรแกรมฟรี</p>
                    <p class="text-slate-600">✓ สินค้ารับประกันศูนย์ไทยแท้ทุกชิ้น</p>
                </div>
            </div>

            <!-- Items Table -->
            <table class="w-full text-left mb-6 border-collapse">
                <thead>
                    <tr class="bg-slate-100 border-b border-slate-300 text-xs font-bold text-slate-700">
                        <th class="py-2.5 px-3 text-center w-12">ลำดับ</th>
                        <th class="py-2.5 px-3">รายการสินค้า / หมวดหมู่</th>
                        <th class="py-2.5 px-3 text-center w-16">จำนวน</th>
                        <th class="py-2.5 px-3 text-right w-24">ราคา/หน่วย</th>
                        <th class="py-2.5 px-3 text-right w-28">จำนวนเงิน</th>
                    </tr>
                </thead>
                <tbody>
                    ${tableRows}
                </tbody>
            </table>

            <!-- Summary -->
            <div class="flex justify-end mb-8">
                <div class="w-64 bg-slate-50 p-4 rounded border border-slate-200 text-xs space-y-2">
                    <div class="flex justify-between text-slate-600">
                        <span>ยอดรวมก่อนภาษี:</span>
                        <span>฿${(total * 0.934579).toLocaleString(undefined, {maximumFractionDigits: 2})}</span>
                    </div>
                    <div class="flex justify-between text-slate-600">
                        <span>ภาษีมูลค่าเพิ่ม (VAT 7% รวมแล้ว):</span>
                        <span>฿${(total * 0.065421).toLocaleString(undefined, {maximumFractionDigits: 2})}</span>
                    </div>
                    <div class="border-t border-slate-300 pt-2 flex justify-between text-sm font-bold text-blue-700">
                        <span>ยอดสุทธิทั้งสิ้น:</span>
                        <span>฿${total.toLocaleString()}</span>
                    </div>
                </div>
            </div>

            <!-- Signatures -->
            <div class="flex justify-between text-center pt-8 border-t border-slate-200 text-xs text-slate-600">
                <div class="w-48">
                    <div class="border-b border-slate-400 pb-8 mb-2"></div>
                    <p>ผู้เสนอราคา</p>
                    <p class="text-[10px] text-slate-400">(เจ้าหน้าที่ฝ่ายขาย NEXUS TECH)</p>
                </div>
                <div class="w-48">
                    <div class="border-b border-slate-400 pb-8 mb-2"></div>
                    <p>ผู้อนุมัติสั่งซื้อ / ลูกค้า</p>
                    <p class="text-[10px] text-slate-400">วันที่: ..... / ..... / .........</p>
                </div>
            </div>
        </div>
    `;

    // Render inside a hidden print area and call print
    let printArea = document.getElementById('print-container');
    if (!printArea) {
        printArea = document.createElement('div');
        printArea.id = 'print-container';
        printArea.className = 'print-only';
        document.body.appendChild(printArea);
    }
    printArea.innerHTML = quotationHTML;
    window.print();
}

document.addEventListener('DOMContentLoaded', () => {
    initPCBuilder();
});
