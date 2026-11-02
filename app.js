// Jompoi Analytics & Pipeline Dashboard Application
document.addEventListener("DOMContentLoaded", () => {
  // Master Datasets (Replicated from MongoDB Collections)
  const appData = {
    customers: [
      { _id: "CUST001", customer_id: "C001", name: "ABC Stores", city: "Chennai", phone: "9876543210" },
      { _id: "CUST002", customer_id: "C002", name: "Sri Murugan Supermarket", city: "Madurai", phone: "9876543211" },
      { _id: "CUST003", customer_id: "C003", name: "Kovai Fresh Mart", city: "Coimbatore", phone: "9876543212" }
    ],
    items: [
      { item_code: "ITM001", name: "Basmati Rice 5kg", brand: "India Gate", category: "Grains & Rice", price: 450.0, gst_percent: 5.0 },
      { item_code: "ITM002", name: "Sunflower Oil 1L", brand: "Fortune", category: "Edible Oils", price: 135.0, gst_percent: 5.0 },
      { item_code: "ITM003", name: "Toor Dal 1kg", brand: "Tata Sampann", category: "Pulses", price: 160.0, gst_percent: 0.0 },
      { item_code: "ITM004", name: "Milk 500ml", brand: "Aavin", category: "Dairy", price: 25.0, gst_percent: 0.0 }
    ],
    sales: [
      { invoice_no: "INV-2026-001", invoice_date: "2026-08-24", customer_name: "ABC Stores", customer_city: "Chennai", item_code: "ITM001", item_name: "Basmati Rice 5kg", quantity: 10, rate: 450.0, net_amount: 4500.0, gst_percent: 5.0, gst_amount: 225.0, total_amount: 4725.0 },
      { invoice_no: "INV-2026-002", invoice_date: "2026-08-24", customer_name: "Sri Murugan Supermarket", customer_city: "Madurai", item_code: "ITM002", item_name: "Sunflower Oil 1L", quantity: 25, rate: 135.0, net_amount: 3375.0, gst_percent: 5.0, gst_amount: 168.75, total_amount: 3543.75 },
      { invoice_no: "INV-2026-003", invoice_date: "2026-08-25", customer_name: "Kovai Fresh Mart", customer_city: "Coimbatore", item_code: "ITM003", item_name: "Toor Dal 1kg", quantity: 30, rate: 160.0, net_amount: 4800.0, gst_percent: 0.0, gst_amount: 0.0, total_amount: 4800.0 }
    ],
    purchases: [
      { invoice_no: "PUR-2026-001", invoice_date: "2026-08-20", vendor: "KR Agro Supplies", item_code: "ITM001", item_name: "Basmati Rice 5kg", quantity: 50, rate: 380.0, net_amount: 19000.0, gst_percent: 5.0, gst_amount: 950.0, total_amount: 19950.0 },
      { invoice_no: "PUR-2026-002", invoice_date: "2026-08-21", vendor: "Adani Wilmar Dist", item_code: "ITM002", item_name: "Sunflower Oil 1L", quantity: 100, rate: 110.0, net_amount: 11000.0, gst_percent: 5.0, gst_amount: 550.0, total_amount: 11550.0 }
    ],
    stock_ledger: [
      { date: "2026-08-20", item_code: "ITM001", item_name: "Basmati Rice 5kg", transaction_type: "IN", quantity: 50, voucher_no: "PUR-2026-001" },
      { date: "2026-08-21", item_code: "ITM002", item_name: "Sunflower Oil 1L", transaction_type: "IN", quantity: 100, voucher_no: "PUR-2026-002" },
      { date: "2026-08-24", item_code: "ITM001", item_name: "Basmati Rice 5kg", transaction_type: "OUT", quantity: 10, voucher_no: "INV-2026-001" },
      { date: "2026-08-24", item_code: "ITM002", item_name: "Sunflower Oil 1L", transaction_type: "OUT", quantity: 25, voucher_no: "INV-2026-002" },
      { date: "2026-08-25", item_code: "ITM003", item_name: "Toor Dal 1kg", transaction_type: "OUT", quantity: 30, voucher_no: "INV-2026-003" }
    ],
    sync_states: [
      { collection: "customers", table: "customers", strategy: "Incremental (updated_at)", status: "Active / Up-to-Date" },
      { collection: "items", table: "items", strategy: "Incremental (updated_at)", status: "Active / Up-to-Date" },
      { collection: "orders", table: "orders", strategy: "Flattened Incremental", status: "Active / Up-to-Date" },
      { collection: "sales_invoice", table: "sales", strategy: "Flattened Incremental", status: "Active / Up-to-Date" },
      { collection: "purchase_invoice", table: "purchases", strategy: "Incremental (updated_at)", status: "Active / Up-to-Date" },
      { collection: "stock_ledger", table: "stock_ledger", strategy: "Append-only Audit Stream", status: "Active / Up-to-Date" }
    ]
  };

  // Setup Navigation Tabs
  const navButtons = document.querySelectorAll(".nav-item");
  const tabPanes = document.querySelectorAll(".tab-pane");
  const pageTitle = document.getElementById("page-title");
  const pageSubtitle = document.getElementById("page-subtitle");

  const tabMetadata = {
    "tab-executive": { title: "Executive Dashboard", subtitle: "Real-time business performance and data warehouse metrics" },
    "tab-sales": { title: "Sales Analytics", subtitle: "Breakdown of daily grocery transactions, item volumes, and customer locations" },
    "tab-purchases": { title: "Purchases & Suppliers", subtitle: "Procurement records, supplier performance, and purchase rate variance" },
    "tab-inventory": { title: "Inventory & Stock Position", subtitle: "Real-time stock on hand, valuation at retail price, and warehouse movements" },
    "tab-gst": { title: "GST & ITC Reconciliation", subtitle: "Automated tax reconciliation between GSTR-1 output tax and GSTR-2B input tax credit" },
    "tab-erp": { title: "ERPNext Profit & Loss Statement", subtitle: "Operational financial statement generated from synchronized cloud tables" },
    "tab-etl": { title: "ETL Pipeline Inspector", subtitle: "MongoDB document flattening and BigQuery schema replication preview" }
  };

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

  // Populate Items Master Table
  const itemsTbody = document.querySelector("#table-items-master tbody");
  if (itemsTbody) {
    itemsTbody.innerHTML = appData.items.map(it => `
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

  // Populate Sales Table
  const salesTbody = document.querySelector("#table-sales tbody");
  if (salesTbody) {
    salesTbody.innerHTML = appData.sales.map(s => `
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

  // Populate Purchases Table
  const purchasesTbody = document.querySelector("#table-purchases tbody");
  if (purchasesTbody) {
    purchasesTbody.innerHTML = appData.purchases.map(p => `
      <tr>
        <td><strong>${p.invoice_no}</strong></td>
        <td>${p.invoice_date}</td>
        <td>${p.vendor}</td>
        <td><code>${p.item_code}</code></td>
        <td>${p.item_name}</td>
        <td>${p.quantity}</td>
        <td>₹${p.rate.toFixed(2)}</td>
        <td>₹${p.net_amount.toFixed(2)}</td>
        <td>₹${p.gst_amount.toFixed(2)}</td>
        <td><strong>₹${p.total_amount.toFixed(2)}</strong></td>
      </tr>
    `).join("");
  }

  // Populate Inventory Table
  const inventoryTbody = document.querySelector("#table-inventory tbody");
  if (inventoryTbody) {
    const stockMap = {};
    appData.stock_ledger.forEach(l => {
      if (!stockMap[l.item_code]) {
        stockMap[l.item_code] = { in: 0, out: 0 };
      }
      if (l.transaction_type === "IN") stockMap[l.item_code].in += l.quantity;
      if (l.transaction_type === "OUT") stockMap[l.item_code].out += l.quantity;
    });

    inventoryTbody.innerHTML = appData.items.map(item => {
      const counts = stockMap[item.item_code] || { in: 0, out: 0 };
      const current = counts.in - counts.out;
      const valuation = current * item.price;
      const statusClass = current <= 10 ? "badge-warning" : (current > 50 ? "badge-success" : "badge-success");
      const statusText = current <= 10 ? "Low Stock" : "Optimal";

      return `
        <tr>
          <td><code>${item.item_code}</code></td>
          <td><strong>${item.name}</strong></td>
          <td>${item.brand}</td>
          <td>${item.category}</td>
          <td>₹${item.price.toFixed(2)}</td>
          <td>${counts.in}</td>
          <td>${counts.out}</td>
          <td><strong>${current}</strong></td>
          <td>₹${valuation.toFixed(2)}</td>
          <td><span class="badge ${statusClass}">${statusText}</span></td>
        </tr>
      `;
    }).join("");
  }

  // Populate Stock Ledger Table
  const ledgerTbody = document.querySelector("#table-stock-ledger tbody");
  if (ledgerTbody) {
    ledgerTbody.innerHTML = appData.stock_ledger.map(l => `
      <tr>
        <td>${l.date}</td>
        <td><code>${l.item_code}</code></td>
        <td>${l.item_name}</td>
        <td><span class="badge ${l.transaction_type === 'IN' ? 'badge-success' : 'badge-warning'}">${l.transaction_type}</span></td>
        <td>${l.quantity}</td>
        <td><code>${l.voucher_no}</code></td>
      </tr>
    `).join("");
  }

  // Populate GST Table
  const gstTbody = document.querySelector("#table-gst-reconciliation tbody");
  if (gstTbody) {
    gstTbody.innerHTML = `
      <tr>
        <td><strong>Outward Supplies (Sales)</strong></td>
        <td>GST on taxable delivery of grocery supplies (GSTR-1)</td>
        <td>₹12,675.00</td>
        <td>₹393.75</td>
        <td>-</td>
        <td>₹393.75</td>
      </tr>
      <tr>
        <td><strong>Inward Supplies (Purchases)</strong></td>
        <td>Eligible Input Tax Credit from registered vendors (GSTR-2B)</td>
        <td>₹30,000.00</td>
        <td>-</td>
        <td>₹1,500.00</td>
        <td>(₹1,500.00 Credit)</td>
      </tr>
      <tr style="background: rgba(16, 185, 129, 0.1); font-weight: bold;">
        <td><strong>Net Tax Settlement (GSTR-3B)</strong></td>
        <td>Input Tax Credit fully offsets Output Tax liability</td>
        <td>-</td>
        <td>₹0.00 Cash</td>
        <td>₹1,106.25 Carry Forward</td>
        <td><span class="badge badge-success">Zero Cash Liability</span></td>
      </tr>
    `;
  }

  // Populate Sync State Table
  const syncTbody = document.querySelector("#table-sync-state tbody");
  if (syncTbody) {
    syncTbody.innerHTML = appData.sync_states.map(s => `
      <tr>
        <td><code>${s.collection}</code></td>
        <td><strong>${s.table}</strong></td>
        <td>${s.strategy}</td>
        <td>${new Date().toISOString()}</td>
        <td><span class="badge badge-success">${s.status}</span></td>
      </tr>
    `).join("");
  }

  // Populate ETL Previews
  const previewMongo = document.getElementById("preview-mongo");
  const previewBq = document.getElementById("preview-bq");
  if (previewMongo && previewBq) {
    const sampleMongo = {
      _id: "INV001",
      invoice_no: "INV-2026-001",
      invoice_date: "2026-08-24",
      customer: {
        name: "ABC Stores",
        city: "Chennai"
      },
      item_code: "ITM001",
      item_name: "Basmati Rice 5kg",
      quantity: 10,
      rate: 450.0,
      net_amount: 4500.0,
      gst_percent: 5.0,
      gst_amount: 225.0,
      total_amount: 4725.0,
      created_at: "2026-08-24T10:30:00Z",
      updated_at: "2026-08-24T10:30:00Z"
    };

    const sampleBq = {
      _id: "INV001",
      invoice_no: "INV-2026-001",
      invoice_date: "2026-08-24",
      customer_name: "ABC Stores",
      customer_city: "Chennai",
      item_code: "ITM001",
      item_name: "Basmati Rice 5kg",
      quantity: 10,
      rate: 450.0,
      net_amount: 4500.0,
      gst_percent: 5.0,
      gst_amount: 225.0,
      total_amount: 4725.0,
      created_at: "2026-08-24T10:30:00+00:00",
      updated_at: "2026-08-24T10:30:00+00:00"
    };

    previewMongo.textContent = JSON.stringify(sampleMongo, null, 2);
    previewBq.textContent = JSON.stringify(sampleBq, null, 2);
  }

  // Initialize Charts
  // 1. Daily Trends
  const ctxDaily = document.getElementById("chartDailyTrends");
  if (ctxDaily) {
    new Chart(ctxDaily, {
      type: "bar",
      data: {
        labels: ["2026-08-20", "2026-08-21", "2026-08-24", "2026-08-25"],
        datasets: [
          { label: "Sales (Revenue)", data: [0, 0, 8268.75, 4800.0], backgroundColor: "#3b82f6" },
          { label: "Purchases (Procurement)", data: [19950.0, 11550.0, 0, 0], backgroundColor: "#8b5cf6" }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { labels: { color: "#94a3b8" } } },
        scales: {
          x: { ticks: { color: "#94a3b8" }, grid: { color: "#334155" } },
          y: { ticks: { color: "#94a3b8" }, grid: { color: "#334155" } }
        }
      }
    });
  }

  // 2. Category Share
  const ctxCat = document.getElementById("chartCategoryShare");
  if (ctxCat) {
    new Chart(ctxCat, {
      type: "doughnut",
      data: {
        labels: ["Grains & Rice", "Edible Oils", "Pulses", "Dairy"],
        datasets: [{
          data: [4725.0, 3543.75, 4800.0, 0],
          backgroundColor: ["#3b82f6", "#10b981", "#f59e0b", "#8b5cf6"]
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: "bottom", labels: { color: "#94a3b8" } } }
      }
    });
  }

  // 3. Sales by City
  const ctxCity = document.getElementById("chartSalesByCity");
  if (ctxCity) {
    new Chart(ctxCity, {
      type: "pie",
      data: {
        labels: ["Chennai", "Madurai", "Coimbatore"],
        datasets: [{
          data: [4725.0, 3543.75, 4800.0],
          backgroundColor: ["#3b82f6", "#8b5cf6", "#10b981"]
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: "bottom", labels: { color: "#94a3b8" } } }
      }
    });
  }

  // 4. Sales by Item
  const ctxItem = document.getElementById("chartSalesByItem");
  if (ctxItem) {
    new Chart(ctxItem, {
      type: "bar",
      data: {
        labels: ["Basmati Rice 5kg", "Sunflower Oil 1L", "Toor Dal 1kg"],
        datasets: [
          { label: "Units Sold", data: [10, 25, 30], backgroundColor: "#10b981" }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { labels: { color: "#94a3b8" } } },
        scales: {
          x: { ticks: { color: "#94a3b8" }, grid: { color: "#334155" } },
          y: { ticks: { color: "#94a3b8" }, grid: { color: "#334155" } }
        }
      }
    });
  }

  // 5. Purchases by Vendor
  const ctxVendor = document.getElementById("chartVendorPurchases");
  if (ctxVendor) {
    new Chart(ctxVendor, {
      type: "doughnut",
      data: {
        labels: ["KR Agro Supplies", "Adani Wilmar Dist"],
        datasets: [{
          data: [19950.0, 11550.0],
          backgroundColor: ["#8b5cf6", "#f59e0b"]
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: "bottom", labels: { color: "#94a3b8" } } }
      }
    });
  }

  // 6. Rate Margin
  const ctxMargin = document.getElementById("chartRateMargin");
  if (ctxMargin) {
    new Chart(ctxMargin, {
      type: "bar",
      data: {
        labels: ["Basmati Rice 5kg", "Sunflower Oil 1L"],
        datasets: [
          { label: "Purchase Rate (Cost)", data: [380.0, 110.0], backgroundColor: "#ef4444" },
          { label: "Selling Rate (Revenue)", data: [450.0, 135.0], backgroundColor: "#10b981" }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { labels: { color: "#94a3b8" } } },
        scales: {
          x: { ticks: { color: "#94a3b8" }, grid: { color: "#334155" } },
          y: { ticks: { color: "#94a3b8" }, grid: { color: "#334155" } }
        }
      }
    });
  }

  // ETL Sync Button Action
  const btnSync = document.getElementById("btn-sync");
  if (btnSync) {
    btnSync.addEventListener("click", () => {
      btnSync.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Syncing...';
      btnSync.disabled = true;

      setTimeout(() => {
        btnSync.innerHTML = '<i class="fa-solid fa-check"></i> Sync Complete!';
        setTimeout(() => {
          btnSync.innerHTML = '<i class="fa-solid fa-sync"></i> Run ETL Sync';
          btnSync.disabled = false;
        }, 2000);
      }, 1200);
    });
  }

  // Refresh Button Action
  const btnRefresh = document.getElementById("btn-refresh-data");
  if (btnRefresh) {
    btnRefresh.addEventListener("click", () => {
      window.location.reload();
    });
  }
});
