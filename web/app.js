// Jompoi ERP Business System Application
document.addEventListener("DOMContentLoaded", () => {
  // ERP Master & Transaction Datasets
  const erpData = {
    customers: {
      "CUST001": { id: "CUST001", name: "ABC Stores", city: "Chennai, Tamil Nadu", phone: "+91 9876543210" },
      "CUST002": { id: "CUST002", name: "Sri Murugan Supermarket", city: "Madurai, Tamil Nadu", phone: "+91 9876543211" },
      "CUST003": { id: "CUST003", name: "Kovai Fresh Mart", city: "Coimbatore, Tamil Nadu", phone: "+91 9876543212" }
    },

    invoices: {
      "INV-2026-001": {
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
        invoice_no: "INV-2026-002",
        invoice_date: "2026-08-24",
        customer_id: "CUST002",
        items: [
          { name: "Sunflower Oil 1L", desc: "Fortune Pure Refined Oil", qty: 25, price: 135.0, tax_percent: 5.0 },
          { name: "Basmati Rice 5kg", desc: "Royal Heritage Biryani Pack", qty: 5, price: 450.0, tax_percent: 5.0 }
        ]
      },
      "INV-2026-003": {
        invoice_no: "INV-2026-003",
        invoice_date: "2026-08-25",
        customer_id: "CUST003",
        items: [
          { name: "Toor Dal 1kg", desc: "Unpolished Organic Dal", qty: 30, price: 160.0, tax_percent: 0.0 },
          { name: "Sunflower Oil 1L", desc: "Fortune Edible Oil 1L Pouch", qty: 10, price: 135.0, tax_percent: 5.0 }
        ]
      }
    },

    items: [
      { item_code: "ITM001", name: "Basmati Rice 5kg", brand: "India Gate", category: "Grains & Rice", price: 450.0, gst_percent: 5.0 },
      { item_code: "ITM002", name: "Sunflower Oil 1L", brand: "Fortune", category: "Edible Oils", price: 135.0, gst_percent: 5.0 },
      { item_code: "ITM003", name: "Toor Dal 1kg", brand: "Tata Sampann", category: "Pulses", price: 160.0, gst_percent: 0.0 },
      { item_code: "ITM004", name: "Milk 500ml", brand: "Aavin", category: "Dairy", price: 25.0, gst_percent: 0.0 }
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
      { date: "2026-08-24", item_code: "ITM001", item_name: "Basmati Rice 5kg", transaction_type: "OUT (Sale)", quantity: 10, voucher_no: "INV-2026-001" },
      { date: "2026-08-24", item_code: "ITM002", item_name: "Sunflower Oil 1L", transaction_type: "OUT (Sale)", quantity: 25, voucher_no: "INV-2026-002" },
      { date: "2026-08-25", item_code: "ITM003", item_name: "Toor Dal 1kg", transaction_type: "OUT (Sale)", quantity: 30, voucher_no: "INV-2026-003" }
    ]
  };

  // Tab Metadata
  const tabMetadata = {
    "tab-invoice": { title: "Tax Invoice & Billing", subtitle: "Generate, review, and print official commercial invoices with per-item GST calculations" },
    "tab-erp-pnl": { title: "ERP Profit & Loss Statement", subtitle: "Operational accounting financial statement generated from sales and procurement costs" },
    "tab-gst-itc": { title: "GST & ITC Tax Reconciliation", subtitle: "Input Tax Credit reconciliation between GSTR-1 output tax and GSTR-2B vendor purchases" },
    "tab-sales": { title: "Customer Sales Invoices", subtitle: "Register of operational customer sales transactions and billing records" },
    "tab-purchases": { title: "Vendor Purchase Invoices", subtitle: "Procurement bills from suppliers with itemized GST tax credit breakdown" },
    "tab-items": { title: "Master Items Catalog", subtitle: "Item codes, categories, retail prices, and applicable GST percentage rates" },
    "tab-inventory": { title: "Inventory Movement Ledger", subtitle: "Real-time audit stream of stock IN (purchases) and stock OUT (sales) movements" }
  };

  // Tab Navigation Handling
  const navButtons = document.querySelectorAll(".nav-item");
  const tabPanes = document.querySelectorAll(".tab-pane");
  const pageTitle = document.getElementById("page-title");
  const pageSubtitle = document.getElementById("page-subtitle");

  navButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const targetTab = btn.getAttribute("data-tab");
      navButtons.forEach(b => b.classList.remove("active"));
      tabPanes.forEach(p => p.classList.remove("active"));

      btn.classList.add("active");
      const targetPane = document.getElementById(targetTab);
      if (targetPane) targetPane.classList.add("active");

      if (tabMetadata[targetTab]) {
        pageTitle.textContent = tabMetadata[targetTab].title;
        pageSubtitle.textContent = tabMetadata[targetTab].subtitle;
      }
    });
  });

  // --- INVOICE RENDERING ENGINE ---
  let currentInvoiceKey = "INV-2026-001";

  function renderInvoice(invoiceKey) {
    const inv = erpData.invoices[invoiceKey];
    if (!inv) return;

    const customer = erpData.customers[inv.customer_id] || { name: "Customer", city: "Tamil Nadu", phone: "-" };

    // Update Header fields
    document.getElementById("inv-no").textContent = inv.invoice_no;
    document.getElementById("inv-date").textContent = inv.invoice_date;
    document.getElementById("inv-customer-name").textContent = customer.name;
    document.getElementById("inv-customer-city").textContent = `City: ${customer.city}`;
    document.getElementById("inv-customer-phone").textContent = `Phone: ${customer.phone}`;

    const tbody = document.getElementById("invoice-items-body");
    tbody.innerHTML = "";

    let subtotal = 0;
    let totalTax = 0;
    let grandTotal = 0;

    inv.items.forEach((item, index) => {
      const price = parseFloat(item.price);
      const qty = parseFloat(item.qty);
      const taxPercent = parseFloat(item.tax_percent);

      // Formula as specified by client:
      // Tax per unit = price * (tax_percent / 100)
      // Total = (price + tax) * quantity
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

  // Initial render of invoice
  renderInvoice(currentInvoiceKey);

  // --- POPULATE OTHER ERP TABLES ---

  // 1. Master Items Table
  const itemsTbody = document.querySelector("#table-items-master tbody");
  if (itemsTbody) {
    itemsTbody.innerHTML = erpData.items.map(it => `
      <tr>
        <td><code>${it.item_code}</code></td>
        <td><strong>${it.name}</strong></td>
        <td>${it.brand}</td>
        <td>${it.category}</td>
        <td>₹${it.price.toFixed(2)}</td>
        <td><span class="badge badge-success">${it.gst_percent}%</span></td>
        <td><span class="badge badge-success">Active Master</span></td>
      </tr>
    `).join("");
  }

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

  // 3. Purchase Table (with per-item GST and ITC)
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
