// Shopping Cart State Manager
const Cart = {
    key: 'techhub_cart',

    getItems() {
        try {
            return JSON.parse(localStorage.getItem(this.key)) || [];
        } catch (e) {
            return [];
        }
    },

    save(items) {
        localStorage.setItem(this.key, JSON.stringify(items));
        this.updateBadge();
        this.renderDrawer();
    },

    addItem(product, qty = 1) {
        let items = this.getItems();
        const existingIndex = items.findIndex(i => i.id === product.id);

        if (existingIndex > -1) {
            items[existingIndex].qty += qty;
        } else {
            items.push({
                id: product.id,
                name: product.name,
                price: parseFloat(product.price),
                image_url: product.image_url,
                category: product.category,
                type: product.type || 'hardware',
                brand: product.brand,
                qty: qty
            });
        }

        this.save(items);
        this.showToast(`เพิ่ม "${product.name}" ลงตะกร้าแล้ว!`, 'success');
    },

    addMultiple(products) {
        let items = this.getItems();
        let addedCount = 0;

        products.forEach(product => {
            if (!product || !product.id) return;
            const existingIndex = items.findIndex(i => i.id === product.id);
            if (existingIndex > -1) {
                items[existingIndex].qty += 1;
            } else {
                items.push({
                    id: product.id,
                    name: product.name,
                    price: parseFloat(product.price),
                    image_url: product.image_url,
                    category: product.category,
                    type: product.type || 'hardware',
                    brand: product.brand,
                    qty: 1
                });
            }
            addedCount++;
        });

        this.save(items);
        this.showToast(`เพิ่มชิ้นส่วนสเปคคอมทั้งหมด ${addedCount} รายการลงตะกร้าแล้ว!`, 'success');
    },

    updateQty(productId, qty) {
        let items = this.getItems();
        const index = items.findIndex(i => i.id === productId);
        if (index > -1) {
            if (qty <= 0) {
                items.splice(index, 1);
            } else {
                items[index].qty = qty;
            }
            this.save(items);
        }
    },

    removeItem(productId) {
        let items = this.getItems();
        items = items.filter(i => i.id !== productId);
        this.save(items);
        this.showToast('ลบสินค้าออกจากตะกร้าแล้ว', 'info');
    },

    clear() {
        localStorage.removeItem(this.key);
        this.updateBadge();
        this.renderDrawer();
    },

    getTotal() {
        const items = this.getItems();
        return items.reduce((sum, i) => sum + (i.price * i.qty), 0);
    },

    getCount() {
        const items = this.getItems();
        return items.reduce((sum, i) => sum + i.qty, 0);
    },

    updateBadge() {
        const count = this.getCount();
        const badges = document.querySelectorAll('.cart-badge');
        badges.forEach(b => {
            b.innerText = count;
            if (count > 0) {
                b.classList.remove('hidden');
            } else {
                b.classList.add('hidden');
            }
        });
    },

    renderDrawer() {
        const container = document.getElementById('cart-drawer-items');
        const totalElem = document.getElementById('cart-drawer-total');
        if (!container) return;

        const items = this.getItems();
        if (items.length === 0) {
            container.innerHTML = `
                <div class="text-center py-12 text-slate-400">
                    <i data-lucide="shopping-bag" class="w-12 h-12 mx-auto mb-3 opacity-30"></i>
                    <p class="text-sm">ไม่มีสินค้าในตะกร้า</p>
                </div>
            `;
            if (totalElem) totalElem.innerText = '฿0';
            if (window.lucide) lucide.createIcons();
            return;
        }

        let html = '';
        items.forEach(item => {
            html += `
                <div class="flex items-center gap-3 p-3 bg-slate-800/60 rounded-xl border border-slate-700/50">
                    <img src="${item.image_url}" alt="${item.name}" class="w-14 h-14 object-cover rounded-lg bg-slate-900 border border-slate-700 flex-shrink-0" onerror="this.src='https://via.placeholder.com/60?text=Hardware'">
                    <div class="flex-1 min-w-0">
                        <h4 class="text-xs font-semibold text-white truncate" title="${item.name}">${item.name}</h4>
                        <div class="flex items-center gap-2 mt-1">
                            <span class="text-xs text-blue-400 font-bold">฿${(item.price * item.qty).toLocaleString()}</span>
                            ${item.type === 'software' ? '<span class="text-[10px] bg-purple-900/60 text-purple-300 px-1.5 py-0.5 rounded">Digital Key</span>' : ''}
                        </div>
                        <div class="flex items-center gap-2 mt-2">
                            <button onclick="Cart.updateQty(${item.id}, ${item.qty - 1})" class="w-5 h-5 flex items-center justify-center bg-slate-700 hover:bg-slate-600 rounded text-xs text-slate-300">-</button>
                            <span class="text-xs text-slate-200 px-1 font-medium">${item.qty}</span>
                            <button onclick="Cart.updateQty(${item.id}, ${item.qty + 1})" class="w-5 h-5 flex items-center justify-center bg-slate-700 hover:bg-slate-600 rounded text-xs text-slate-300">+</button>
                        </div>
                    </div>
                    <button onclick="Cart.removeItem(${item.id})" class="text-slate-400 hover:text-red-400 p-1 rounded transition">
                        <i data-lucide="trash-2" class="w-4 h-4"></i>
                    </button>
                </div>
            `;
        });

        container.innerHTML = html;
        if (totalElem) totalElem.innerText = '฿' + this.getTotal().toLocaleString();
        if (window.lucide) lucide.createIcons();
    },

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        const bg = type === 'success' ? 'bg-emerald-600 text-white' : (type === 'error' ? 'bg-rose-600 text-white' : 'bg-blue-600 text-white');
        toast.className = `fixed bottom-6 right-6 z-50 flex items-center gap-2 px-4 py-3 rounded-xl shadow-2xl transition-all transform duration-300 translate-y-4 opacity-0 ${bg}`;
        toast.innerHTML = `
            <i data-lucide="${type === 'success' ? 'check-circle' : 'info'}" class="w-5 h-5 flex-shrink-0"></i>
            <span class="text-sm font-medium">${message}</span>
        `;
        document.body.appendChild(toast);
        if (window.lucide) lucide.createIcons();

        requestAnimationFrame(() => {
            toast.classList.remove('translate-y-4', 'opacity-0');
        });

        setTimeout(() => {
            toast.classList.add('opacity-0', 'translate-y-4');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
};

document.addEventListener('DOMContentLoaded', () => {
    Cart.updateBadge();
    Cart.renderDrawer();
});
