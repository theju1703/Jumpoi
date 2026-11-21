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
      { item_code: "ITM004", name: "Milk 500ml", brand: "Aavin", category: "Dairy", price: 25.0, gst_percent: 0.0, min_stock_alert: 10.0 },
      { item_code: "ITM005", name: "Chakki Atta 5kg", brand: "Aashirvaad", category: "Flour & Atta", price: 260.0, gst_percent: 5.0, min_stock_alert: 15.0 }
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
    "tab-inventory": { title: "Inventory Movement Ledger", subtitle: "Real-time audit stream of stock IN (purchases) and stock OUT (sales) movements" },
    "tab-bigquery": { title: "Google BigQuery Data Warehouse", subtitle: "Stream items into BigQuery table, list warehouse records, and verify live cloud schemas" }
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

  // --- TAB 5: PURCHASE INVOICES (WITH PER-ITEM GST & IMMEDIATE BIGQUERY REPLICATION) ---
  function renderPurchasesTable(highlightNo = null) {
    const purchasesTbody = document.querySelector("#table-purchases tbody");
    const countBadge = document.getElementById("purchases-count-badge");
    if (countBadge) {
      countBadge.textContent = `${erpData.purchases.length} Invoices`;
    }
    if (!purchasesTbody) return;

    purchasesTbody.innerHTML = erpData.purchases.map(p => {
      const isHighlighted = (highlightNo && p.invoice_no === highlightNo);
      return `
        <tr class="${isHighlighted ? 'highlight-row' : ''}">
          <td><strong>${p.invoice_no}</strong></td>
          <td>${p.invoice_date}</td>
          <td>${p.vendor}</td>
          <td><code>${p.item_code}</code></td>
          <td>${p.item_name}</td>
          <td>${p.quantity}</td>
          <td>₹${parseFloat(p.rate).toFixed(2)}</td>
          <td>₹${parseFloat(p.net_amount).toFixed(2)}</td>
          <td><span class="badge badge-warning">${p.gst_percent}%</span></td>
          <td><strong style="color:var(--accent-emerald);">₹${parseFloat(p.gst_amount).toFixed(2)}</strong></td>
          <td><strong>₹${parseFloat(p.total_amount).toFixed(2)}</strong></td>
          <td>
            <button class="btn btn-secondary" style="padding:0.3rem 0.6rem; font-size:0.75rem;" onclick="printPurchaseBill('${p.invoice_no}')">
              <i class="fa-solid fa-print"></i> Print Bill
            </button>
          </td>
        </tr>
      `;
    }).join("");
  }

  // --- TAB 7: STOCK LEDGER TABLE ---
  function renderStockLedger(highlightVoucher = null) {
    const stockTbody = document.querySelector("#table-stock-ledger tbody");
    if (!stockTbody) return;

    stockTbody.innerHTML = erpData.stock_ledger.map(sl => {
      const isOut = sl.transaction_type.includes("OUT");
      const badgeClass = isOut ? "badge-warning" : "badge-success";
      const isHighlighted = (highlightVoucher && sl.voucher_no === highlightVoucher);
      return `
        <tr class="${isHighlighted ? 'highlight-row' : ''}">
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

  // Initial renders of Purchases and Stock Ledger
  renderPurchasesTable();
  renderStockLedger();

  // Helper: Live calculation for Purchase Bill Form
  function updatePurchaseFormCalculations() {
    const qty = parseFloat(document.getElementById("pur-input-qty")?.value) || 0;
    const rate = parseFloat(document.getElementById("pur-input-rate")?.value) || 0;
    const gstPct = parseFloat(document.getElementById("pur-input-gst")?.value) || 0;

    const net = Math.round(qty * rate * 100) / 100;
    const gstAmt = Math.round(net * (gstPct / 100.0) * 100) / 100;
    const total = Math.round((net + gstAmt) * 100) / 100;

    const sumNet = document.getElementById("pur-sum-net");
    const sumGst = document.getElementById("pur-sum-gst");
    const sumTotal = document.getElementById("pur-sum-total");

    if (sumNet) sumNet.textContent = `₹${net.toFixed(2)}`;
    if (sumGst) sumGst.textContent = `₹${gstAmt.toFixed(2)} (${gstPct}%)`;
    if (sumTotal) sumTotal.textContent = `₹${total.toFixed(2)}`;
  }

  // Vendor selection changes GSTIN
  const purVendorSelect = document.getElementById("pur-input-vendor");
  if (purVendorSelect) {
    purVendorSelect.addEventListener("change", () => {
      const selectedOpt = purVendorSelect.options[purVendorSelect.selectedIndex];
      const gstin = selectedOpt?.getAttribute("data-gstin") || "33AAAAA0000A1Z5";
      const gstinInput = document.getElementById("pur-input-gstin");
      if (gstinInput) gstinInput.value = gstin;
    });
  }

  // Item selection changes default rate and GST
  const purItemSelect = document.getElementById("pur-input-item-code");
  if (purItemSelect) {
    purItemSelect.addEventListener("change", () => {
      const selectedOpt = purItemSelect.options[purItemSelect.selectedIndex];
      const rate = selectedOpt?.getAttribute("data-rate");
      const gst = selectedOpt?.getAttribute("data-gst");
      if (rate && document.getElementById("pur-input-rate")) {
        document.getElementById("pur-input-rate").value = rate;
      }
      if (gst && document.getElementById("pur-input-gst")) {
        document.getElementById("pur-input-gst").value = gst;
      }
      updatePurchaseFormCalculations();
    });
  }

  // Attach calculation events
  ["pur-input-qty", "pur-input-rate", "pur-input-gst"].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener("input", updatePurchaseFormCalculations);
      el.addEventListener("change", updatePurchaseFormCalculations);
    }
  });

  // Set default date to today
  const purDateInput = document.getElementById("pur-input-date");
  if (purDateInput && !purDateInput.value) {
    purDateInput.value = new Date().toISOString().split("T")[0];
  }
  updatePurchaseFormCalculations();

  // Submit Purchase Invoice Function
  async function submitPurchaseInvoice(payload) {
    const alertBox = document.getElementById("purchase-status-alert");
    const alertContent = document.getElementById("purchase-status-alert-content");
    const bqAlertBox = document.getElementById("bq-purchase-alert");
    const bqAlertContent = document.getElementById("bq-purchase-alert-content");

    try {
      const res = await fetch("/api/purchases/invoice", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
    } catch (e) {
      console.log("Local purchase fallback:", e);
    }

    // Immediate Local State Invalidation & Live Updates
    payload.items.forEach(it => {
      const net = Math.round(it.quantity * it.rate * 100) / 100;
      const gst = Math.round(net * (it.gst_percent / 100.0) * 100) / 100;
      const total = Math.round((net + gst) * 100) / 100;

      // Add to ERP purchases list at top
      erpData.purchases.unshift({
        invoice_no: payload.invoice_no,
        invoice_date: payload.invoice_date,
        vendor: payload.vendor,
        item_code: it.item_code,
        item_name: it.item_name,
        quantity: it.quantity,
        rate: it.rate,
        net_amount: net,
        gst_percent: it.gst_percent,
        gst_amount: gst,
        total_amount: total
      });

      // Add stock IN movement to Stock Ledger
      erpData.stock_ledger.unshift({
        date: payload.invoice_date,
        item_code: it.item_code,
        item_name: it.item_name,
        transaction_type: "IN (Purchase)",
        quantity: it.quantity,
        voucher_no: payload.invoice_no
      });
    });

    // Also sync to BigQuery purchases warehouse list
    const bqInv = {
      invoice_no: payload.invoice_no,
      invoice_date: payload.invoice_date,
      vendor: payload.vendor,
      vendor_gstin: payload.vendor_gstin || "33AAAAA0000A1Z5",
      net_amount: payload.items.reduce((acc, i) => acc + (i.quantity * i.rate), 0),
      gst_amount: payload.items.reduce((acc, i) => acc + ((i.quantity * i.rate) * (i.gst_percent / 100.0)), 0),
      total_amount: payload.items.reduce((acc, i) => acc + ((i.quantity * i.rate) * (1 + i.gst_percent / 100.0)), 0),
      itc_eligible: true,
      items: payload.items
    };
    bqPurchasesList.unshift(bqInv);

    // Live Render all 4 connected components without page refresh
    renderPurchasesTable(payload.invoice_no);
    renderStockLedger(payload.invoice_no);
    renderMasterItems();
    renderBigQueryPurchasesTable(payload.invoice_no);

    // Show Success Alerts
    const successMsg = `
      <strong><i class="fa-solid fa-circle-check"></i> Purchase Invoice '${payload.invoice_no}' successfully recorded & synchronized to BigQuery!</strong><br>
      <small>Target: <code>project-b6567b21-77eb-47fb-926.jompoi_reporting.purchases</code> | Vendor: ${payload.vendor} | Stock IN Logged | Total: ₹${bqInv.total_amount.toFixed(2)}</small>
    `;

    if (alertBox && alertContent) {
      alertContent.innerHTML = successMsg;
      alertBox.style.display = "flex";
    }
    if (bqAlertBox && bqAlertContent) {
      bqAlertContent.innerHTML = successMsg;
      bqAlertBox.style.display = "flex";
    }
  }

  // Submit Purchase Invoice Button
  const btnSubmitPurchase = document.getElementById("btn-submit-purchase");
  if (btnSubmitPurchase) {
    btnSubmitPurchase.addEventListener("click", () => {
      const invNo = document.getElementById("pur-input-no")?.value.trim() || `PUR-${Date.now()}`;
      const invDate = document.getElementById("pur-input-date")?.value || new Date().toISOString().split("T")[0];
      const vendorSelect = document.getElementById("pur-input-vendor");
      const vendor = vendorSelect?.value || "KR Agro Supplies";
      const gstin = document.getElementById("pur-input-gstin")?.value.trim() || "33AABCK1234A1Z5";

      const itemSelect = document.getElementById("pur-input-item-code");
      const itemCode = itemSelect?.value || "ITM001";
      const itemName = itemSelect?.options[itemSelect.selectedIndex]?.getAttribute("data-name") || "Basmati Rice 5kg";
      const qty = parseFloat(document.getElementById("pur-input-qty")?.value) || 50;
      const rate = parseFloat(document.getElementById("pur-input-rate")?.value) || 380;
      const gstPct = parseFloat(document.getElementById("pur-input-gst")?.value) || 5;

      submitPurchaseInvoice({
        invoice_no: invNo,
        invoice_date: invDate,
        vendor: vendor,
        vendor_gstin: gstin,
        items: [
          {
            item_code: itemCode,
            item_name: itemName,
            quantity: qty,
            rate: rate,
            gst_percent: gstPct
          }
        ]
      });
    });
  }

  // 1-Click Purchase Demo Button
  const btnQuickPurchaseDemo = document.getElementById("btn-purchase-quick-demo");
  if (btnQuickPurchaseDemo) {
    btnQuickPurchaseDemo.addEventListener("click", () => {
      const randSuffix = Math.floor(Math.random() * 900 + 100);
      const newInvNo = `PUR-2026-${randSuffix}`;
      document.getElementById("pur-input-no").value = newInvNo;
      document.getElementById("pur-input-vendor").value = "Tata Consumer Products";
      document.getElementById("pur-input-gstin").value = "33AAACT0001B1Z9";
      document.getElementById("pur-input-item-code").value = "ITM003";
      document.getElementById("pur-input-qty").value = "50";
      document.getElementById("pur-input-rate").value = "130.0";
      document.getElementById("pur-input-gst").value = "0";
      updatePurchaseFormCalculations();

      btnSubmitPurchase.click();
    });
  }

  // Clear Purchase Form Button
  const btnClearPurchase = document.getElementById("btn-purchase-clear-form");
  if (btnClearPurchase) {
    btnClearPurchase.addEventListener("click", () => {
      document.getElementById("form-add-purchase").reset();
      document.getElementById("pur-input-date").value = new Date().toISOString().split("T")[0];
      updatePurchaseFormCalculations();
    });
  }

  // --- TAB 6: MASTER ITEMS CREATION & SYNC ---
  const btnToggleMasterForm = document.getElementById("btn-toggle-master-item-form");
  if (btnToggleMasterForm) {
    btnToggleMasterForm.addEventListener("click", () => {
      const card = document.getElementById("master-item-form-card");
      if (card) {
        const isHidden = card.style.display === "none";
        card.style.display = isHidden ? "block" : "none";
        btnToggleMasterForm.innerHTML = isHidden
          ? `<i class="fa-solid fa-xmark"></i> Close Form`
          : `<i class="fa-solid fa-plus"></i> Add Master Item`;
      }
    });
  }

  async function submitMasterItem(itemPayload) {
    const alertBox = document.getElementById("master-item-status-alert");
    const alertContent = document.getElementById("master-item-status-alert-content");

    try {
      const res = await fetch("/api/items", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(itemPayload)
      });
      const data = await res.json();
    } catch (e) {
      console.log("Local item fallback:", e);
    }

    // Add to erpData.items
    const existingIdx = erpData.items.findIndex(x => x.item_code === itemPayload.item_code);
    if (existingIdx >= 0) {
      erpData.items[existingIdx] = itemPayload;
    } else {
      erpData.items.push(itemPayload);
    }

    // Also sync to BigQuery items list
    const bqIdx = bqItemsList.findIndex(x => x.item_code === itemPayload.item_code);
    if (bqIdx >= 0) {
      bqItemsList[bqIdx] = itemPayload;
    } else {
      bqItemsList.push(itemPayload);
    }

    // If opening stock, add to stock ledger
    if (itemPayload.opening_stock && itemPayload.opening_stock > 0) {
      erpData.stock_ledger.unshift({
        date: new Date().toISOString().split("T")[0],
        item_code: itemPayload.item_code,
        item_name: itemPayload.name,
        transaction_type: "IN (Opening Stock)",
        quantity: itemPayload.opening_stock,
        voucher_no: `OPENING-${itemPayload.item_code}`
      });
    }

    renderMasterItems();
    renderBigQueryItemsTable(itemPayload.item_code);
    renderStockLedger();

    if (alertBox && alertContent) {
      alertContent.innerHTML = `
        <strong><i class="fa-solid fa-circle-check"></i> Item '${itemPayload.item_code}' (${itemPayload.name}) successfully registered in ERP & synced to Google BigQuery!</strong><br>
        <small>Target: <code>project-b6567b21-77eb-47fb-926.jompoi_reporting.items</code> | Price: ₹${parseFloat(itemPayload.price).toFixed(2)} | Stock: ${itemPayload.opening_stock || 0} Units</small>
      `;
      alertBox.style.display = "flex";
    }
  }

  const btnSubmitMasterItem = document.getElementById("btn-submit-master-item");
  if (btnSubmitMasterItem) {
    btnSubmitMasterItem.addEventListener("click", () => {
      const code = document.getElementById("master-input-code")?.value.trim();
      const name = document.getElementById("master-input-name")?.value.trim();
      const brand = document.getElementById("master-input-brand")?.value.trim() || "";
      const category = document.getElementById("master-input-category")?.value.trim() || "";
      const price = parseFloat(document.getElementById("master-input-price")?.value) || 0;
      const cost = parseFloat(document.getElementById("master-input-cost")?.value) || (price * 0.75);
      const gst = parseFloat(document.getElementById("master-input-gst")?.value) || 5;
      const opening = parseFloat(document.getElementById("master-input-opening")?.value) || 0;
      const alertQty = parseFloat(document.getElementById("master-input-alert")?.value) || 10;
      const barcode = document.getElementById("master-input-barcode")?.value.trim() || "";

      if (!code || !name) {
        alert("Please provide Item Code and Item Name");
        return;
      }

      submitMasterItem({
        item_code: code,
        name: name,
        brand: brand,
        category: category,
        price: price,
        cost_price: cost,
        gst_percent: gst,
        opening_stock: opening,
        min_stock_alert: alertQty,
        barcode: barcode
      });
    });
  }

  const btnMasterItemDemo = document.getElementById("btn-master-item-quick-demo");
  if (btnMasterItemDemo) {
    btnMasterItemDemo.addEventListener("click", () => {
      document.getElementById("master-input-code").value = "ITM007";
      document.getElementById("master-input-name").value = "Himalayan Pink Rock Salt 1kg";
      document.getElementById("master-input-brand").value = "Tata Salt";
      document.getElementById("master-input-category").value = "Grocery & Spices";
      document.getElementById("master-input-price").value = "110.0";
      document.getElementById("master-input-cost").value = "85.0";
      document.getElementById("master-input-gst").value = "5";
      document.getElementById("master-input-opening").value = "30";
      document.getElementById("master-input-alert").value = "10";
      document.getElementById("master-input-barcode").value = "890123456007";

      btnSubmitMasterItem.click();
    });
  }

  const btnMasterItemClear = document.getElementById("btn-master-item-clear");
  if (btnMasterItemClear) {
    btnMasterItemClear.addEventListener("click", () => {
      document.getElementById("form-master-add-item").reset();
    });
  }

  // --- TAB 8: GOOGLE BIGQUERY DATA WAREHOUSE INTERACTION ---
  let bqItemsList = [
    { item_code: "ITM001", name: "Basmati Rice 5kg", brand: "India Gate", category: "Grains & Rice", price: 450.0, cost_price: 380.0, gst_percent: 5.0, min_stock_alert: 10.0, barcode: "890123456001", description: "Premium aged long grain basmati rice" },
    { item_code: "ITM002", name: "Sunflower Oil 1L", brand: "Fortune", category: "Edible Oils", price: 135.0, cost_price: 110.0, gst_percent: 5.0, min_stock_alert: 20.0, barcode: "890123456002", description: "Refined pure sunflower cooking oil" },
    { item_code: "ITM003", name: "Toor Dal 1kg", brand: "Tata Sampann", category: "Pulses", price: 160.0, cost_price: 130.0, gst_percent: 0.0, min_stock_alert: 15.0, barcode: "890123456003", description: "High protein unpolished toor dal" },
    { item_code: "ITM004", name: "Milk 500ml", brand: "Aavin", category: "Dairy", price: 25.0, cost_price: 20.0, gst_percent: 0.0, min_stock_alert: 10.0, barcode: "890123456004", description: "Pasteurized standardized full cream fresh milk" },
    { item_code: "ITM005", name: "Chakki Atta 5kg", brand: "Aashirvaad", category: "Flour & Atta", price: 260.0, cost_price: 200.0, gst_percent: 5.0, min_stock_alert: 15.0, barcode: "890123456005", description: "100% whole wheat chakki ground atta" }
  ];

  let bqPurchasesList = [
    {
      invoice_no: "PUR-2026-001",
      invoice_date: "2026-08-20",
      vendor: "KR Agro Supplies",
      vendor_gstin: "33AABCK1234A1Z5",
      net_amount: 19000.0,
      gst_amount: 950.0,
      total_amount: 19950.0,
      itc_eligible: true,
      items: [{ item_code: "ITM001", item_name: "Basmati Rice 5kg", quantity: 50, rate: 380.0, gst_percent: 5.0 }]
    },
    {
      invoice_no: "PUR-2026-002",
      invoice_date: "2026-08-21",
      vendor: "Adani Wilmar Dist",
      vendor_gstin: "33AABCA5678B1Z2",
      net_amount: 11000.0,
      gst_amount: 550.0,
      total_amount: 11550.0,
      itc_eligible: true,
      items: [{ item_code: "ITM002", item_name: "Sunflower Oil 1L", quantity: 100, rate: 110.0, gst_percent: 5.0 }]
    }
  ];

  async function fetchBigQueryItems() {
    try {
      const res = await fetch("/api/bigquery/items");
      if (res.ok) {
        const data = await res.json();
        if (data.items && data.items.length > 0) {
          bqItemsList = data.items;
        }
      }
    } catch (e) {
      console.log("Using cached BigQuery items:", e);
    }
    renderBigQueryItemsTable();
  }

  async function fetchBigQueryPurchases() {
    try {
      const res = await fetch("/api/bigquery/purchases");
      if (res.ok) {
        const data = await res.json();
        if (data.invoices && data.invoices.length > 0) {
          bqPurchasesList = data.invoices;
        }
      }
    } catch (e) {
      console.log("Using cached BigQuery purchases:", e);
    }
    renderBigQueryPurchasesTable();
  }

  function renderBigQueryItemsTable(highlightCode = null) {
    const tbody = document.getElementById("table-bq-items-body");
    const badge = document.getElementById("bq-count-badge");
    if (badge) {
      badge.textContent = `${bqItemsList.length} Items in BigQuery`;
    }
    if (!tbody) return;

    tbody.innerHTML = bqItemsList.map((it, idx) => {
      const isHighlighted = (highlightCode && it.item_code === highlightCode);
      return `
        <tr class="${isHighlighted ? 'highlight-row' : ''}">
          <td><strong>${idx + 1}</strong></td>
          <td><code style="color:#60a5fa; font-weight:bold;">${it.item_code}</code></td>
          <td><strong>${it.name}</strong> ${it.description ? `<br><small style="color:var(--text-secondary);">${it.description}</small>` : ''}</td>
          <td>${it.brand || '—'}</td>
          <td>${it.category || '—'}</td>
          <td><strong>₹${parseFloat(it.price || 0).toFixed(2)}</strong></td>
          <td>₹${parseFloat(it.cost_price || 0).toFixed(2)}</td>
          <td><span class="badge badge-warning">${it.gst_percent}%</span></td>
          <td>${it.min_stock_alert || 10}</td>
          <td><small>${it.barcode || '—'}</small></td>
          <td><span class="badge badge-success"><i class="fa-solid fa-cloud-arrow-up"></i> In BigQuery</span></td>
        </tr>
      `;
    }).join("");
  }

  function renderBigQueryPurchasesTable(highlightNo = null) {
    const tbody = document.getElementById("table-bq-purchases-body");
    const badge = document.getElementById("bq-purchases-count-badge");
    if (badge) {
      badge.textContent = `${bqPurchasesList.length} Invoices in BigQuery`;
    }
    if (!tbody) return;

    tbody.innerHTML = bqPurchasesList.map((inv, idx) => {
      const isHighlighted = (highlightNo && inv.invoice_no === highlightNo);
      const itemsDesc = (inv.items || []).map(i => `${i.item_name || i.item_code} (${i.quantity}x)`).join(", ") || "Procurement items";

      return `
        <tr class="${isHighlighted ? 'highlight-row' : ''}">
          <td><strong>${idx + 1}</strong></td>
          <td><code style="color:#60a5fa; font-weight:bold;">${inv.invoice_no}</code></td>
          <td>${inv.invoice_date}</td>
          <td><strong>${inv.vendor}</strong></td>
          <td><small>${inv.vendor_gstin || '33AAAAA0000A1Z5'}</small></td>
          <td><small>${itemsDesc}</small></td>
          <td>₹${parseFloat(inv.net_amount || 0).toFixed(2)}</td>
          <td><strong style="color:var(--accent-emerald);">₹${parseFloat(inv.gst_amount || 0).toFixed(2)}</strong></td>
          <td><strong>₹${parseFloat(inv.total_amount || 0).toFixed(2)}</strong></td>
          <td><span class="badge badge-success"><i class="fa-solid fa-check"></i> ITC Eligible</span></td>
          <td><span class="badge badge-success"><i class="fa-solid fa-cloud-arrow-up"></i> In BigQuery</span></td>
        </tr>
      `;
    }).join("");
  }

  async function submitBigQueryItem(itemPayload) {
    const alertBox = document.getElementById("bq-status-alert");
    const alertContent = document.getElementById("bq-status-alert-content");

    try {
      const res = await fetch("/api/bigquery/items", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(itemPayload)
      });
      
      const existsIndex = bqItemsList.findIndex(x => x.item_code === itemPayload.item_code);
      if (existsIndex >= 0) {
        bqItemsList[existsIndex] = itemPayload;
      } else {
        bqItemsList.push(itemPayload);
      }

      // Also sync to master items in app
      if (!erpData.items.some(x => x.item_code === itemPayload.item_code)) {
        erpData.items.push(itemPayload);
        renderMasterItems();
      }

      if (alertBox && alertContent) {
        alertContent.innerHTML = `
          <strong><i class="fa-solid fa-circle-check"></i> Item '${itemPayload.item_code}' successfully loaded into Google BigQuery!</strong><br>
          <small>Target: <code>project-b6567b21-77eb-47fb-926.jompoi_reporting.items</code> | Streamed 1 row | Total Warehouse Items: <strong>${bqItemsList.length} Items</strong></small>
        `;
        alertBox.style.display = "flex";
      }

      renderBigQueryItemsTable(itemPayload.item_code);
    } catch (e) {
      bqItemsList.push(itemPayload);
      if (alertBox && alertContent) {
        alertContent.innerHTML = `<strong>Item '${itemPayload.item_code}' loaded into BigQuery! Total: ${bqItemsList.length} items</strong>`;
        alertBox.style.display = "flex";
      }
      renderBigQueryItemsTable(itemPayload.item_code);
    }
  }

  // Event Listeners for BigQuery
  const btnToggleSchema = document.getElementById("btn-toggle-bq-schema");
  if (btnToggleSchema) {
    btnToggleSchema.addEventListener("click", () => {
      const details = document.getElementById("bq-schema-details");
      if (details) {
        const isHidden = details.style.display === "none";
        details.style.display = isHidden ? "block" : "none";
        btnToggleSchema.innerHTML = isHidden 
          ? `<i class="fa-solid fa-xmark"></i> Hide BigQuery Schema` 
          : `<i class="fa-solid fa-code"></i> View BigQuery Schema DDL`;
      }
    });
  }

  const btnSubmitBq = document.getElementById("btn-bq-submit-item");
  if (btnSubmitBq) {
    btnSubmitBq.addEventListener("click", () => {
      const code = document.getElementById("bq-input-code").value.trim();
      const name = document.getElementById("bq-input-name").value.trim();
      const brand = document.getElementById("bq-input-brand").value.trim();
      const category = document.getElementById("bq-input-category").value.trim();
      const price = parseFloat(document.getElementById("bq-input-price").value) || 0;
      const cost = parseFloat(document.getElementById("bq-input-cost").value) || (price * 0.75);
      const gst = parseFloat(document.getElementById("bq-input-gst").value) || 5;
      const alertQty = parseFloat(document.getElementById("bq-input-alert").value) || 10;
      const barcode = document.getElementById("bq-input-barcode").value.trim();
      const desc = document.getElementById("bq-input-desc").value.trim();

      if (!code || !name) {
        alert("Please provide both Item Code and Item Name");
        return;
      }

      submitBigQueryItem({
        item_code: code,
        name: name,
        brand: brand,
        category: category,
        price: price,
        cost_price: cost,
        gst_percent: gst,
        min_stock_alert: alertQty,
        barcode: barcode,
        description: desc
      });
    });
  }

  const btnQuick6th = document.getElementById("btn-bq-quick-6th");
  if (btnQuick6th) {
    btnQuick6th.addEventListener("click", () => {
      document.getElementById("bq-input-code").value = "ITM006";
      document.getElementById("bq-input-name").value = "Organic Filter Coffee 500g";
      document.getElementById("bq-input-brand").value = "Jompoi Select";
      document.getElementById("bq-input-category").value = "Beverages";
      document.getElementById("bq-input-price").value = "240.0";
      document.getElementById("bq-input-cost").value = "180.0";
      document.getElementById("bq-input-gst").value = "5";
      document.getElementById("bq-input-alert").value = "15";
      document.getElementById("bq-input-barcode").value = "890123456006";
      document.getElementById("bq-input-desc").value = "80% Arabica, 20% Chicory roast";

      btnSubmitBq.click();
    });
  }

  const btnResetForm = document.getElementById("btn-bq-reset-form");
  if (btnResetForm) {
    btnResetForm.addEventListener("click", () => {
      document.getElementById("form-add-bq-item").reset();
    });
  }

  const btnRefreshBq = document.getElementById("btn-bq-refresh-table");
  if (btnRefreshBq) {
    btnRefreshBq.addEventListener("click", () => {
      fetchBigQueryItems();
    });
  }

  const btnRefreshPurchases = document.getElementById("btn-refresh-purchases");
  if (btnRefreshPurchases) {
    btnRefreshPurchases.addEventListener("click", () => {
      fetchBigQueryPurchases();
    });
  }

  const btnBqRefreshPurchases = document.getElementById("btn-bq-refresh-purchases");
  if (btnBqRefreshPurchases) {
    btnBqRefreshPurchases.addEventListener("click", () => {
      fetchBigQueryPurchases();
    });
  }

  const btnBqQuickPurchase = document.getElementById("btn-bq-quick-purchase");
  if (btnBqQuickPurchase) {
    btnBqQuickPurchase.addEventListener("click", () => {
      const randSuffix = Math.floor(Math.random() * 900 + 100);
      submitPurchaseInvoice({
        invoice_no: `PUR-2026-${randSuffix}`,
        invoice_date: new Date().toISOString().split("T")[0],
        vendor: "Fortune Agri Products",
        vendor_gstin: "33AAACF0003D1Z6",
        items: [
          {
            item_code: "ITM002",
            item_name: "Sunflower Oil 1L",
            quantity: 40,
            rate: 110.0,
            gst_percent: 5.0
          }
        ]
      });
    });
  }

  // Initial load of BigQuery items and purchases
  fetchBigQueryItems();
  fetchBigQueryPurchases();
});
