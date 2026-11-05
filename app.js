// Jompoi ERP Business System Application
document.addEventListener("DOMContentLoaded", () => {
  // ERP Master & Transaction Datasets
  const erpData = {
    customers: {
      "CUST001": { id: "CUST001", name: "ABC Stores", city: "Chennai, Tamil Nadu", phone: "+91 9876543210" },
      "CUST002": { id: "CUST002", name: "Sri Murugan Supermarket", city: "Madurai, Tamil Nadu", phone: "+91 9876543211" },
      "CUST003": { id: "CUST003", name: "Kovai Fresh Mart", city: "Coimbatore, Tamil Nadu", phone: "+91 9876543212" }
    },

    vendors: {
      "VEND001": { id: "VEND001", name: "KR Agro Supplies", gstin: "33AABCK1234A1Z5", city: "Kanchipuram, Tamil Nadu", phone: "+91 9444112233" },
      "VEND002": { id: "VEND002", name: "Adani Wilmar Dist", gstin: "33AABCA5678B1Z2", city: "Chennai, Tamil Nadu", phone: "+91 9444556677" }
    },

    invoices: {
      "INV-2026-001": {
        type: "SALES",
        invoice_no: "INV-2026-001",
        invoice_date: "2026-08-24",
        customer_id: "CUST001",
        items: [
          { name: "Basmati Rice 5kg", desc: "India Gate Classic Aged Grain", qty: 10, price: 450.0, tax_percent: 5.0 },
          { name: "Toor Dal 1kg", desc: "Tata Sampann High Protein Pulses", qty: 15, price: 160.0, tax_percent: 0.0 },
          { name: "Aavin Milk 500ml", desc: "Pasteurized Full Cream Dairy", qty: 20, price: 25.0, tax_percent: 0.0 }
        ]
      },
      "INV-2026-002": {
        type: "SALES",
        invoice_no: "INV-2026-002",
        invoice_date: "2026-08-24",
        customer_id: "CUST002",
        items: [
          { name: "Sunflower Oil 1L", desc: "Fortune Pure Refined Oil", qty: 25, price: 135.0, tax_percent: 5.0 },
          { name: "Basmati Rice 5kg", desc: "Royal Heritage Biryani Pack", qty: 5, price: 450.0, tax_percent: 5.0 }
        ]
      },
      "INV-2026-003": {
        type: "SALES",
        invoice_no: "INV-2026-003",
        invoice_date: "2026-08-25",
        customer_id: "CUST003",
        items: [
          { name: "Toor Dal 1kg", desc: "Unpolished Organic Dal", qty: 30, price: 160.0, tax_percent: 0.0 },
          { name: "Sunflower Oil 1L", desc: "Fortune Edible Oil 1L Pouch", qty: 10, price: 135.0, tax_percent: 5.0 }
        ]
      },
      "PUR-2026-001": {
        type: "PURCHASE",
        invoice_no: "PUR-2026-001",
        invoice_date: "2026-08-20",
        vendor_id: "VEND001",
        items: [
          { name: "Basmati Rice 5kg", desc: "Raw Paddy Procurement 50 Bags", qty: 50, price: 380.0, tax_percent: 5.0 }
        ]
      },
      "PUR-2026-002": {
        type: "PURCHASE",
        invoice_no: "PUR-2026-002",
        invoice_date: "2026-08-21",
        vendor_id: "VEND002",
        items: [
          { name: "Sunflower Oil 1L", desc: "Refined Edible Oil Batch 100 Cartons", qty: 100, price: 110.0, tax_percent: 5.0 }
        ]
      }
    },

    items: [
      { item_code: "ITM001", name: "Basmati Rice 5kg", brand: "India Gate", category: "Grains & Rice", price: 450.0, gst_percent: 5.0, min_stock_alert: 10.0 },
      { item_code: "ITM002", name: "Sunflower Oil 1L", brand: "Fortune", category: "Edible Oils", price: 135.0, gst_percent: 5.0, min_stock_alert: 20.0 },
      { item_code: "ITM003", name: "Toor Dal 1kg", brand: "Tata Sampann", category: "Pulses", price: 160.0, gst_percent: 0.0, min_stock_alert: 15.0 },
      { item_code: "ITM004", name: "Milk 500ml", brand: "Aavin", category: "Dairy", price: 25.0, gst_percent: 0.0, min_stock_alert: 10.0 }
    ],

    sales: [
      { invoice_no: "INV-2026-001", invoice_date: "2026-08-24", customer_name: "ABC Stores", customer_city: "Chennai", item_name: "Basmati Rice 5kg", quantity: 10, rate: 450.0, net_amount: 4500.0, gst_percent: 5.0, gst_amount: 225.0, total_amount: 4725.0 },
      { invoice_no: "INV-2026-002", invoice_date: "2026-08-24", customer_name: "Sri Murugan Supermarket", customer_city: "Madurai", item_name: "Sunflower Oil 1L", quantity: 25, rate: 135.0, net_amount: 3375.0, gst_percent: 5.0, gst_amount: 168.75, total_amount: 3543.75 },
      { invoice_no: "INV-2026-003", invoice_date: "2026-08-25", customer_name: "Kovai Fresh Mart", customer_city: "Coimbatore", item_name: "Toor Dal 1kg", quantity: 30, rate: 160.0, net_amount: 4800.0, gst_percent: 0.0, gst_amount: 0.0, total_amount: 4800.0 }
    ],

    purchases: [
      { invoice_no: "PUR-2026-001", invoice_date: "2026-08-20", vendor: "KR Agro Supplies", item_code: "ITM001", item_name: "Basmati Rice 5kg", quantity: 50, rate: 380.0, net_amount: 19000.0, gst_percent: 5.0, gst_amount: 950.0, total_amount: 19950.0 },
      { invoice_no: "PUR-2026-002", invoice_date: "2026-08-21", vendor: "Adani Wilmar Dist", item_code: "ITM002", item_name: "Sunflower Oil 1L", quantity: 100, rate: 110.0, net_amount: 11000.0, gst_percent: 5.0, gst_amount: 550.0, total_amount: 11550.0 }
    ],

    stock_ledger: [
      { date: "2026-08-20", item_code: "ITM001", item_name: "Basmati Rice 5kg", transaction_type: "IN (Purchase)", quantity: 50, voucher_no: "PUR-2026-001" },
      { date: "2026-08-21", item_code: "ITM002", item_name: "Sunflower Oil 1L", transaction_type: "IN (Purchase)", quantity: 100, voucher_no: "PUR-2026-002" },
      { date: "2026-08-22", item_code: "ITM003", item_name: "Toor Dal 1kg", transaction_type: "IN (Opening Stock)", quantity: 50, voucher_no: "OPENING-ITM003" },
      { date: "2026-08-22", item_code: "ITM004", item_name: "Milk 500ml", transaction_type: "IN (Opening Stock)", quantity: 40, voucher_no: "OPENING-ITM004" },
      { date: "2026-08-24", item_code: "ITM001", item_name: "Basmati Rice 5kg", transaction_type: "OUT (Sale)", quantity: 10, voucher_no: "INV-2026-001" },
      { date: "2026-08-24", item_code: "ITM002", item_name: "Sunflower Oil 1L", transaction_type: "OUT (Sale)", quantity: 25, voucher_no: "INV-2026-002" },
      { date: "2026-08-25", item_code: "ITM003", item_name: "Toor Dal 1kg", transaction_type: "OUT (Sale)", quantity: 30, voucher_no: "INV-2026-003" }
    ]
  };

  // Helper: Compute real-time stock balances (sum(IN) - sum(OUT))
  function calculateStockBalances() {
    const balances = {};
    erpData.stock_ledger.forEach(entry => {
      const code = entry.item_code;
      const qty = parseFloat(entry.quantity) || 0;
      const type = (entry.transaction_type || "").toUpperCase();
      if (!balances[code]) balances[code] = 0;
      if (type.includes("IN")) {
        balances[code] += qty;
      } else if (type.includes("OUT")) {
        balances[code] -= qty;
      }
    });
    return balances;
  }

  // Tab Metadata
  const tabMetadata = {
    "tab-invoice": { title: "Tax Invoice & Commercial Bill Printing", subtitle: "Generate, review, and print official commercial Sales Invoices and Vendor Purchase Bills" },
    "tab-erp-pnl": { title: "ERP Profit & Loss Statement", subtitle: "Operational accounting financial statement generated from sales and procurement costs" },
    "tab-gst-itc": { title: "GST & ITC Tax Reconciliation", subtitle: "Input Tax Credit reconciliation between GSTR-1 output tax and GSTR-2B vendor purchases" },
    "tab-sales": { title: "Customer Sales Invoices", subtitle: "Register of operational customer sales transactions and billing records" },
    "tab-purchases": { title: "Vendor Purchase Invoices", subtitle: "Procurement bills from suppliers with itemized GST tax credit breakdown" },
    "tab-items": { title: "Master Items Stock & Catalog Analysis", subtitle: "Real-time quantity on hand, search filter by item code or name, and stock status" },
    "tab-inventory": { title: "Inventory Movement Ledger", subtitle: "Real-time audit stream of stock IN (purchases) and stock OUT (sales) movements" }
  };

  // Tab Navigation Handling
  const navButtons = document.querySelectorAll(".nav-item");
  const tabPanes = document.querySelectorAll(".tab-pane");
  const pageTitle = document.getElementById("page-title");
  const pageSubtitle = document.getElementById("page-subtitle");

  function switchTab(targetTab) {
    navButtons.forEach(b => b.classList.remove("active"));
    tabPanes.forEach(p => p.classList.remove("active"));

    const activeBtn = document.querySelector(`.nav-item[data-tab="${targetTab}"]`);
    if (activeBtn) activeBtn.classList.add("active");

    const targetPane = document.getElementById(targetTab);
    if (targetPane) targetPane.classList.add("active");

    if (tabMetadata[targetTab]) {
      pageTitle.textContent = tabMetadata[targetTab].title;
      pageSubtitle.textContent = tabMetadata[targetTab].subtitle;
    }
  }

  navButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const targetTab = btn.getAttribute("data-tab");
      switchTab(targetTab);
    });
  });

  // --- INVOICE RENDERING ENGINE ---
  let currentInvoiceKey = "INV-2026-001";

  function renderInvoice(invoiceKey) {
    const inv = erpData.invoices[invoiceKey];
    if (!inv) return;

    const isPurchase = inv.type === "PURCHASE" || invoiceKey.startsWith("PUR-");

    // Badge Title & Color
    const badgeSpan = document.querySelector(".invoice-badge-title");
    if (badgeSpan) {
      badgeSpan.textContent = isPurchase ? "PURCHASE INVOICE / BILL" : "TAX INVOICE";
      badgeSpan.style.background = isPurchase ? "#0284c7" : "#0f172a";
    }

    // Header fields
    document.getElementById("inv-no").textContent = inv.invoice_no;
    document.getElementById("inv-date").textContent = inv.invoice_date;

    const partyBoxes = document.querySelectorAll(".party-box");
    if (partyBoxes.length >= 2) {
      if (isPurchase) {
        const vendor = erpData.vendors[inv.vendor_id] || { name: "KR Agro Supplies", gstin: "33AABCK1234A1Z5", city: "Tamil Nadu", phone: "+91 9444112233" };
        partyBoxes[0].innerHTML = `
          <h4>Vendor / Supplier</h4>
          <p><strong>${vendor.name}</strong></p>
          <p>GSTIN: ${vendor.gstin}</p>
          <p>City: ${vendor.city}</p>
          <p>Phone: ${vendor.phone}</p>
        `;
        partyBoxes[1].innerHTML = `
          <h4>Billed / Received At (Recipient)</h4>
          <p><strong>Jompoi Central Supermarket Hub</strong></p>
          <p>GSTIN: 33AAAAA0000A1Z5</p>
          <p>Ambattur Industrial Estate, Chennai</p>
          <p>State Code: 33 (Tamil Nadu)</p>
        `;
      } else {
        const customer = erpData.customers[inv.customer_id] || { name: "Customer", city: "Tamil Nadu", phone: "-" };
        partyBoxes[0].innerHTML = `
          <h4>Billed To (Customer)</h4>
          <p><strong id="inv-customer-name">${customer.name}</strong></p>
          <p id="inv-customer-city">City: ${customer.city}</p>
          <p id="inv-customer-phone">Phone: ${customer.phone}</p>
        `;
        partyBoxes[1].innerHTML = `
          <h4>Dispatched From (Warehouse)</h4>
          <p><strong>Jompoi Central Fulfillment Hub</strong></p>
          <p>Ambattur Industrial Estate, Chennai</p>
          <p>State Code: 33 (Tamil Nadu)</p>
        `;
      }
    }

    // Update Table Header to match client's exact required format:
    // Item name | Item description(Optional) | quantity | price | tax | (total=(price+tax)*quantity)
    const tableHeader = document.querySelector(".invoice-table thead tr");
    if (tableHeader) {
      tableHeader.innerHTML = `
        <th style="width:5%;">#</th>
        <th style="width:25%;">Item name</th>
        <th style="width:22%;">Item description(Optional)</th>
        <th class="num" style="width:10%;">quantity</th>
        <th class="num" style="width:12%;">price (₹)</th>
        <th class="num" style="width:13%;">tax</th>
        <th class="num" style="width:18%;">total=(price+tax)*quantity</th>
      `;
    }

    const tbody = document.getElementById("invoice-items-body");
    tbody.innerHTML = "";

    let subtotal = 0;
    let totalTax = 0;
    let grandTotal = 0;

    inv.items.forEach((item, index) => {
      const price = parseFloat(item.price);
      const qty = parseFloat(item.qty);
      const taxPercent = parseFloat(item.tax_percent);

      // Formula strictly enforced:
      // Tax per unit = price * (tax_percent / 100)
      // total = (price + tax) * quantity
      const unitTax = price * (taxPercent / 100.0);
      const lineNet = price * qty;
      const lineTax = unitTax * qty;
      const lineTotal = (price + unitTax) * qty;

      subtotal += lineNet;
      totalTax += lineTax;
      grandTotal += lineTotal;

      const descHtml = item.desc ? `<span class="desc-text">${item.desc}</span>` : "";

      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${index + 1}</td>
        <td><strong>${item.name}</strong></td>
        <td>${descHtml || '<span style="color:#94a3b8; font-size:0.8rem;">&mdash;</span>'}</td>
        <td class="num">${qty}</td>
        <td class="num">₹${price.toFixed(2)}</td>
        <td class="num">
          ${taxPercent}% 
          <span style="font-size:0.75rem; color:#64748b; display:block;">(₹${unitTax.toFixed(2)}/unit)</span>
        </td>
        <td class="num"><strong>₹${lineTotal.toFixed(2)}</strong></td>
      `;
      tbody.appendChild(tr);
    });

    document.getElementById("inv-subtotal").textContent = `₹${subtotal.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
    document.getElementById("inv-totaltax").textContent = `₹${totalTax.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
    document.getElementById("inv-grandtotal").textContent = `₹${grandTotal.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
  }

  // Invoice Selector change handler
  const invoiceSelector = document.getElementById("invoice-selector");
  if (invoiceSelector) {
    invoiceSelector.addEventListener("change", (e) => {
      currentInvoiceKey = e.target.value;
      renderInvoice(currentInvoiceKey);
    });
  }

  // Add Item to Invoice handler
  const btnAddLineItem = document.getElementById("btn-add-line-item");
  if (btnAddLineItem) {
    btnAddLineItem.addEventListener("click", () => {
      const nameInput = document.getElementById("new-item-name");
      const descInput = document.getElementById("new-item-desc");
      const qtyInput = document.getElementById("new-item-qty");
      const priceInput = document.getElementById("new-item-price");
      const taxInput = document.getElementById("new-item-tax");

      const name = nameInput.value.trim();
      const desc = descInput.value.trim();
      const qty = parseFloat(qtyInput.value) || 1;
      const price = parseFloat(priceInput.value) || 0;
      const taxPercent = parseFloat(taxInput.value) || 0;

      if (!name) {
        alert("Please enter an item name.");
        return;
      }

      if (!erpData.invoices[currentInvoiceKey]) {
        erpData.invoices[currentInvoiceKey] = {
          type: currentInvoiceKey.startsWith("PUR-") ? "PURCHASE" : "SALES",
          invoice_no: currentInvoiceKey,
          invoice_date: new Date().toISOString().split("T")[0],
          customer_id: "CUST001",
          items: []
        };
      }

      erpData.invoices[currentInvoiceKey].items.push({
        name: name,
        desc: desc || null,
        qty: qty,
        price: price,
        tax_percent: taxPercent
      });

      // Clear inputs
      nameInput.value = "";
      descInput.value = "";
      qtyInput.value = "1";
      priceInput.value = "100.00";

      renderInvoice(currentInvoiceKey);
    });
  }

  // Global helper to print purchase bill from Tab 5
  window.printPurchaseBill = function(invoiceNo) {
    if (invoiceSelector) {
      invoiceSelector.value = invoiceNo;
    }
    currentInvoiceKey = invoiceNo;
    switchTab("tab-invoice");
    renderInvoice(invoiceNo);
  };

  // Initial render of invoice
  renderInvoice(currentInvoiceKey);

  // --- TAB 6: MASTER ITEMS STOCK DATA ANALYSIS & FILTER ENGINE ---
  function renderMasterItems() {
    const balances = calculateStockBalances();
    const searchVal = (document.getElementById("item-search-filter")?.value || "").toLowerCase().trim();
    const filterVal = document.getElementById("item-stock-filter")?.value || "ALL";

    let totalStockUnits = 0;
    let inStockCount = 0;
    let lowStockCount = 0;

    const enrichedItems = erpData.items.map(it => {
      const stockQty = balances[it.item_code] !== undefined ? balances[it.item_code] : 0;
      totalStockUnits += stockQty;
      const minAlert = it.min_stock_alert || 10;
      const isLow = stockQty <= minAlert && stockQty > 0;
      const isOut = stockQty <= 0;

      if (stockQty > 0) inStockCount++;
      if (isLow || isOut) lowStockCount++;

      return {
        ...it,
        stock_on_hand: stockQty,
        is_low: isLow,
        is_out: isOut,
        status: isOut ? "OUT_OF_STOCK" : (isLow ? "LOW_STOCK" : "IN_STOCK")
      };
    });

    // Update KPI Cards
    const statTotalItems = document.getElementById("stat-total-items");
    const statTotalStock = document.getElementById("stat-total-stock");
    const statInStock = document.getElementById("stat-in-stock");
    const statLowStock = document.getElementById("stat-low-stock");

    if (statTotalItems) statTotalItems.textContent = `${erpData.items.length} SKUs`;
    if (statTotalStock) statTotalStock.textContent = `${totalStockUnits} Units`;
    if (statInStock) statInStock.textContent = `${inStockCount} SKUs`;
    if (statLowStock) statLowStock.textContent = `${lowStockCount} SKU`;

    // Filter items based on client query and stock dropdown
    const filtered = enrichedItems.filter(it => {
      // 1. Text filter (item_code or name or brand or category)
      const matchesSearch = !searchVal || 
        it.item_code.toLowerCase().includes(searchVal) ||
        it.name.toLowerCase().includes(searchVal) ||
        it.brand.toLowerCase().includes(searchVal) ||
        it.category.toLowerCase().includes(searchVal);

      // 2. Stock filter
      let matchesStock = true;
      if (filterVal === "IN_STOCK") matchesStock = it.stock_on_hand > 0;
      if (filterVal === "LOW_STOCK") matchesStock = it.is_low || it.is_out;

      return matchesSearch && matchesStock;
    });

    const itemsTbody = document.querySelector("#table-items-master tbody");
    if (itemsTbody) {
      if (filtered.length === 0) {
        itemsTbody.innerHTML = `
          <tr>
            <td colspan="8" style="text-align:center; padding:2rem; color:#94a3b8;">
              <i class="fa-solid fa-magnifying-glass" style="font-size:1.5rem; margin-bottom:0.5rem; display:block;"></i>
              No item matched your search filter "<strong>${searchVal}</strong>".
            </td>
          </tr>
        `;
      } else {
        itemsTbody.innerHTML = filtered.map(it => {
          let badgeHtml = "";
          if (it.is_out) {
            badgeHtml = `<span class="badge badge-warning" style="background:rgba(239,68,68,0.2); color:#ef4444; border:1px solid #ef4444;">OUT OF STOCK (0 Units)</span>`;
          } else if (it.is_low) {
            badgeHtml = `<span class="badge badge-warning" style="background:rgba(245,158,11,0.2); color:#f59e0b; border:1px solid #f59e0b;">LOW STOCK (${it.stock_on_hand} Units)</span>`;
          } else {
            badgeHtml = `<span class="badge badge-success" style="background:rgba(16,185,129,0.2); color:#10b981; border:1px solid #10b981;">IN STOCK (${it.stock_on_hand} Units)</span>`;
          }

          return `
            <tr>
              <td><code>${it.item_code}</code></td>
              <td><strong>${it.name}</strong></td>
              <td>${it.brand}</td>
              <td>${it.category}</td>
              <td>₹${it.price.toFixed(2)}</td>
              <td><span class="badge badge-success">${it.gst_percent}%</span></td>
              <td><strong style="font-size:1.05rem; color:#f8fafc;">${it.stock_on_hand} Units</strong></td>
              <td>${badgeHtml}</td>
            </tr>
          `;
        }).join("");
      }
    }
  }

  // Attach search and filter event listeners
  const searchInput = document.getElementById("item-search-filter");
  const filterSelect = document.getElementById("item-stock-filter");
  if (searchInput) searchInput.addEventListener("input", renderMasterItems);
  if (filterSelect) filterSelect.addEventListener("change", renderMasterItems);

  renderMasterItems();

  // --- POPULATE OTHER ERP TABLES ---

  // 2. Sales Table
  const salesTbody = document.querySelector("#table-sales tbody");
  if (salesTbody) {
    salesTbody.innerHTML = erpData.sales.map(s => `
      <tr>
        <td><strong>${s.invoice_no}</strong></td>
        <td>${s.invoice_date}</td>
        <td>${s.customer_name}</td>
        <td>${s.customer_city}</td>
        <td>${s.item_name}</td>
        <td>${s.quantity}</td>
        <td>₹${s.rate.toFixed(2)}</td>
        <td>₹${s.net_amount.toFixed(2)}</td>
        <td>₹${s.gst_amount.toFixed(2)} (${s.gst_percent}%)</td>
        <td><strong>₹${s.total_amount.toFixed(2)}</strong></td>
      </tr>
    `).join("");
  }

  // 3. Purchase Table (with per-item GST, ITC, and Print Bill Action Button)
  const purchasesTbody = document.querySelector("#table-purchases tbody");
  if (purchasesTbody) {
    purchasesTbody.innerHTML = erpData.purchases.map(p => `
      <tr>
        <td><strong>${p.invoice_no}</strong></td>
        <td>${p.invoice_date}</td>
        <td>${p.vendor}</td>
        <td><code>${p.item_code}</code></td>
        <td>${p.item_name}</td>
        <td>${p.quantity}</td>
        <td>₹${p.rate.toFixed(2)}</td>
        <td>₹${p.net_amount.toFixed(2)}</td>
        <td><span class="badge badge-warning">${p.gst_percent}%</span></td>
        <td><strong style="color:var(--accent-emerald);">₹${p.gst_amount.toFixed(2)}</strong></td>
        <td><strong>₹${p.total_amount.toFixed(2)}</strong></td>
        <td>
          <button class="btn btn-secondary" style="padding:0.3rem 0.6rem; font-size:0.75rem;" onclick="printPurchaseBill('${p.invoice_no}')">
            <i class="fa-solid fa-print"></i> Print Bill
          </button>
        </td>
      </tr>
    `).join("");
  }

  // 4. Stock Ledger Table
  const stockTbody = document.querySelector("#table-stock-ledger tbody");
  if (stockTbody) {
    stockTbody.innerHTML = erpData.stock_ledger.map(sl => {
      const isOut = sl.transaction_type.includes("OUT");
      const badgeClass = isOut ? "badge-warning" : "badge-success";
      return `
        <tr>
          <td>${sl.date}</td>
          <td><code>${sl.item_code}</code></td>
          <td>${sl.item_name}</td>
          <td><span class="badge ${badgeClass}">${sl.transaction_type}</span></td>
          <td><strong>${sl.quantity}</strong></td>
          <td><code>${sl.voucher_no}</code></td>
        </tr>
      `;
    }).join("");
  }
});
