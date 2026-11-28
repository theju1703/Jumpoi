// Jompoi ERP Business System Application - v3.0.0
// Comprehensive ERP-wide Filtering, Search, Analytics, Sorting, Pagination & CSV Export Engine
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
      "VEND002": { id: "VEND002", name: "Adani Wilmar Dist", gstin: "33AABCA5678B1Z2", city: "Chennai, Tamil Nadu", phone: "+91 9444556677" },
      "VEND003": { id: "VEND003", name: "Tata Consumer Products", gstin: "33AAACT0001B1Z9", city: "Coimbatore, Tamil Nadu", phone: "+91 9444889900" },
      "VEND004": { id: "VEND004", name: "Aavin Dairy Cooperative", gstin: "33AAACA0002C1Z4", city: "Chennai, Tamil Nadu", phone: "+91 9444332211" },
      "VEND005": { id: "VEND005", name: "Fortune Agri Products", gstin: "33AAACF0003D1Z6", city: "Madurai, Tamil Nadu", phone: "+91 9444778899" }
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
      { item_code: "ITM001", name: "Basmati Rice 5kg", brand: "India Gate", category: "Grains & Rice", price: 450.0, cost_price: 380.0, gst_percent: 5.0, min_stock_alert: 10.0, barcode: "890123456001" },
      { item_code: "ITM002", name: "Sunflower Oil 1L", brand: "Fortune", category: "Edible Oils", price: 135.0, cost_price: 110.0, gst_percent: 5.0, min_stock_alert: 20.0, barcode: "890123456002" },
      { item_code: "ITM003", name: "Toor Dal 1kg", brand: "Tata Sampann", category: "Pulses", price: 160.0, cost_price: 130.0, gst_percent: 0.0, min_stock_alert: 15.0, barcode: "890123456003" },
      { item_code: "ITM004", name: "Milk 500ml", brand: "Aavin", category: "Dairy", price: 25.0, cost_price: 20.0, gst_percent: 0.0, min_stock_alert: 10.0, barcode: "890123456004" },
      { item_code: "ITM005", name: "Chakki Atta 5kg", brand: "Aashirvaad", category: "Flour & Atta", price: 260.0, cost_price: 200.0, gst_percent: 5.0, min_stock_alert: 15.0, barcode: "890123456005" }
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
      if (type.includes("IN") || type.includes("ADD")) {
        balances[code] += qty;
      } else if (type.includes("OUT") || type.includes("DEDUCT")) {
        balances[code] -= qty;
      }
    });
    return balances;
  }

  // =========================================================================
  // ERP-WIDE FILTER & SORT STATE MANAGEMENT
  // =========================================================================
  const erpState = {
    items: {
      filters: { search: "", category: "ALL", stock: "ALL", brand: "ALL", min_price: null, max_price: null, gst: "ALL" },
      sort: { col: "item_code", asc: true },
      page: 1,
      pageSize: 10
    },
    purchases: {
      filters: { search: "", vendor: "ALL", payment_status: "ALL", date_from: "", date_to: "", min_total: null, max_total: null, preset: "ALL" },
      sort: { col: "invoice_date", asc: false },
      page: 1,
      pageSize: 10
    },
    sales: {
      filters: { search: "", customer: "ALL", city: "ALL", date_from: "", date_to: "", min_total: null, max_total: null, preset: "ALL" },
      sort: { col: "invoice_date", asc: false },
      page: 1,
      pageSize: 10
    },
    inventory: {
      filters: { search: "", item: "ALL", type: "ALL", date_from: "", date_to: "", preset: "ALL" },
      sort: { col: "date", asc: false },
      page: 1,
      pageSize: 10
    },
    gst: {
      filters: { date_from: "", date_to: "", vendor: "ALL", preset: "ALL" }
    },
    pnl: {
      filters: { date_from: "", date_to: "", opex: 850.0, preset: "ALL" }
    }
  };

  // Date Presets Helper Function
  function getDatePresetRange(rangeName) {
    const today = new Date();
    const pad = (n) => String(n).padStart(2, "0");
    const fmt = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;

    if (rangeName === "TODAY") {
      const dStr = fmt(today);
      return { from: dStr, to: dStr };
    } else if (rangeName === "YESTERDAY") {
      const y = new Date(today);
      y.setDate(y.getDate() - 1);
      const dStr = fmt(y);
      return { from: dStr, to: dStr };
    } else if (rangeName === "THIS_WEEK") {
      const curr = new Date(today);
      const day = curr.getDay();
      const diff = curr.getDate() - (day === 0 ? 6 : day - 1);
      const monday = new Date(curr.setDate(diff));
      return { from: fmt(monday), to: fmt(today) };
    } else if (rangeName === "THIS_MONTH") {
      const first = new Date(today.getFullYear(), today.getMonth(), 1);
      return { from: fmt(first), to: fmt(today) };
    } else if (rangeName === "LAST_MONTH") {
      const first = new Date(today.getFullYear(), today.getMonth() - 1, 1);
      const last = new Date(today.getFullYear(), today.getMonth(), 0);
      return { from: fmt(first), to: fmt(last) };
    } else if (rangeName === "YTD") {
      const first = new Date(today.getFullYear(), 0, 1);
      return { from: fmt(first), to: fmt(today) };
    }
    return { from: "", to: "" };
  }

  // Sorting Helper
  function sortRecords(records, sortConfig) {
    if (!sortConfig || !sortConfig.col) return records;
    const { col, asc } = sortConfig;
    return [...records].sort((a, b) => {
      let valA = a[col];
      let valB = b[col];
      if (valA === undefined || valA === null) valA = "";
      if (valB === undefined || valB === null) valB = "";

      const numA = typeof valA === "number" ? valA : parseFloat(valA);
      const numB = typeof valB === "number" ? valB : parseFloat(valB);
      if (!isNaN(numA) && !isNaN(numB) && typeof valA !== "string") {
        return asc ? numA - numB : numB - numA;
      }
      if (typeof valA === "string" && !isNaN(Number(valA)) && typeof valB === "string" && !isNaN(Number(valB))) {
        return asc ? Number(valA) - Number(valB) : Number(valB) - Number(valA);
      }

      const strA = String(valA).toLowerCase();
      const strB = String(valB).toLowerCase();
      return asc ? strA.localeCompare(strB) : strB.localeCompare(strA);
    });
  }

  // Pagination Renderer
  function renderPagination(moduleName, totalItems, controlsContainerId, infoContainerId) {
    const state = erpState[moduleName];
    const isAll = state.pageSize === "ALL";
    const pageSize = isAll ? totalItems : parseInt(state.pageSize, 10);
    const totalPages = pageSize > 0 ? Math.ceil(totalItems / pageSize) || 1 : 1;

    if (state.page > totalPages) state.page = totalPages;
    if (state.page < 1) state.page = 1;

    const startIdx = totalItems === 0 ? 0 : (state.page - 1) * (isAll ? totalItems : pageSize) + 1;
    const endIdx = isAll ? totalItems : Math.min(state.page * pageSize, totalItems);

    const infoEl = document.getElementById(infoContainerId);
    if (infoEl) {
      infoEl.textContent = `Showing ${startIdx} to ${endIdx} of ${totalItems} entries`;
    }

    const ctrlEl = document.getElementById(controlsContainerId);
    if (!ctrlEl) return;
    ctrlEl.innerHTML = "";

    // Prev button
    const prevBtn = document.createElement("button");
    prevBtn.className = "pagination-btn";
    prevBtn.innerHTML = `<i class="fa-solid fa-angle-left"></i> Prev`;
    prevBtn.disabled = state.page <= 1;
    prevBtn.onclick = () => {
      if (state.page > 1) {
        state.page--;
        rerenderModule(moduleName);
      }
    };
    ctrlEl.appendChild(prevBtn);

    // Page buttons
    for (let p = 1; p <= totalPages; p++) {
      if (totalPages > 7 && Math.abs(p - state.page) > 2 && p !== 1 && p !== totalPages) {
        if (p === 2 || p === totalPages - 1) {
          const ellipsis = document.createElement("span");
          ellipsis.textContent = "...";
          ellipsis.style.padding = "0.2rem 0.4rem";
          ellipsis.style.color = "#64748b";
          ctrlEl.appendChild(ellipsis);
        }
        continue;
      }
      const pBtn = document.createElement("button");
      pBtn.className = `pagination-btn ${p === state.page ? "active" : ""}`;
      pBtn.textContent = p;
      pBtn.onclick = () => {
        state.page = p;
        rerenderModule(moduleName);
      };
      ctrlEl.appendChild(pBtn);
    }

    // Next button
    const nextBtn = document.createElement("button");
    nextBtn.className = "pagination-btn";
    nextBtn.innerHTML = `Next <i class="fa-solid fa-angle-right"></i>`;
    nextBtn.disabled = state.page >= totalPages;
    nextBtn.onclick = () => {
      if (state.page < totalPages) {
        state.page++;
        rerenderModule(moduleName);
      }
    };
    ctrlEl.appendChild(nextBtn);
  }

  // Setup Sortable Headers Helper
  function setupSortableHeaders(moduleName, tableSelector) {
    const table = document.querySelector(tableSelector);
    if (!table) return;
    const headers = table.querySelectorAll(`th.sortable-th[data-module="${moduleName}"]`);
    headers.forEach(th => {
      th.addEventListener("click", () => {
        const col = th.getAttribute("data-sort");
        const state = erpState[moduleName];
        if (state.sort.col === col) {
          state.sort.asc = !state.sort.asc;
        } else {
          state.sort.col = col;
          // Dates and amounts default to descending order
          state.sort.asc = !["invoice_date", "date", "price", "rate", "net_amount", "total_amount", "gross_total", "quantity"].includes(col);
        }
        // Update header visual classes
        headers.forEach(h => {
          h.classList.remove("sort-asc", "sort-desc");
          const icon = h.querySelector(".sort-icon");
          if (icon) icon.className = "fa-solid fa-sort sort-icon";
        });
        th.classList.add(state.sort.asc ? "sort-asc" : "sort-desc");
        const icon = th.querySelector(".sort-icon");
        if (icon) {
          icon.className = `fa-solid ${state.sort.asc ? "fa-sort-up" : "fa-sort-down"} sort-icon`;
        }
        state.page = 1;
        rerenderModule(moduleName);
      });
    });
  }

  // Universal CSV Export Helper
  function exportDataToCSV(filename, headers, rows) {
    let csvContent = headers.map(h => `"${String(h).replace(/"/g, '""')}"`).join(",") + "\n";
    rows.forEach(row => {
      csvContent += row.map(val => `"${String(val !== null && val !== undefined ? val : '').replace(/"/g, '""')}"`).join(",") + "\n";
    });
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.style.display = "none";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  // Master Rerender Dispatcher
  function rerenderModule(moduleName) {
    if (moduleName === "items") renderMasterItems();
    else if (moduleName === "purchases") renderPurchasesTable();
    else if (moduleName === "sales") renderSalesTable();
    else if (moduleName === "inventory") renderStockLedger();
    else if (moduleName === "gst") renderGSTReport();
    else if (moduleName === "pnl") renderPnLStatement();
  }

  // Tab Navigation Handling
  const navButtons = document.querySelectorAll(".nav-item");
  const tabPanes = document.querySelectorAll(".tab-pane");
  const pageTitle = document.getElementById("page-title");
  const pageSubtitle = document.getElementById("page-subtitle");

  const tabMetadata = {
    "tab-invoice": { title: "Tax Invoice & Commercial Bill Printing", subtitle: "Generate, review, and print official commercial Sales Invoices and Vendor Purchase Bills" },
    "tab-erp-pnl": { title: "ERP Profit & Loss Statement", subtitle: "Operational accounting financial statement generated from sales and procurement costs" },
    "tab-gst-itc": { title: "GST & ITC Tax Reconciliation", subtitle: "Input Tax Credit reconciliation between GSTR-1 output tax and GSTR-2B vendor purchases" },
    "tab-sales": { title: "Customer Sales Invoices", subtitle: "Register of operational customer sales transactions and billing records" },
    "tab-purchases": { title: "Vendor Purchase Invoices", subtitle: "Procurement bills from suppliers with itemized GST tax credit breakdown" },
    "tab-items": { title: "Master Items Stock & Catalog Analysis", subtitle: "Real-time quantity on hand, search filter by item code or name, and stock status" },
    "tab-inventory": { title: "Inventory Movement Ledger", subtitle: "Real-time audit stream of stock IN (purchases) and stock OUT (sales) movements" }
  };

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

    const hashName = targetTab.replace("tab-", "");
    if (window.location.hash !== "#" + hashName) {
      history.replaceState(null, null, "#" + hashName);
    }
  }

  navButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const targetTab = btn.getAttribute("data-tab");
      switchTab(targetTab);
    });
  });

  function handleHashRoute() {
    const hash = (window.location.hash || "").toLowerCase();
    if (hash === "#items" || hash === "#add-item" || hash === "#item") {
      switchTab("tab-items");
      const formCard = document.getElementById("master-item-form-card");
      if (formCard) formCard.style.display = "block";
    } else if (hash === "#purchases" || hash === "#create-purchase" || hash === "#purchase") {
      switchTab("tab-purchases");
      const formCard = document.getElementById("purchase-form-card");
      if (formCard) formCard.style.display = "block";
    } else if (hash === "#sales") {
      switchTab("tab-sales");
    } else if (hash === "#inventory") {
      switchTab("tab-inventory");
    } else if (hash === "#invoice") {
      switchTab("tab-invoice");
    } else if (hash === "#gst-itc") {
      switchTab("tab-gst-itc");
    } else if (hash === "#erp-pnl") {
      switchTab("tab-erp-pnl");
    } else {
      switchTab("tab-items");
    }
  }
  window.addEventListener("hashchange", handleHashRoute);

  // =========================================================================
  // MODULE 1: PRODUCT & CATALOG MANAGEMENT (TAB 6)
  // =========================================================================
  function getEnrichedMasterItems() {
    const balances = calculateStockBalances();
    return erpData.items.map(it => {
      const stockQty = balances[it.item_code] !== undefined ? balances[it.item_code] : 0;
      const minAlert = parseFloat(it.min_stock_alert) || 10;
      const isOut = stockQty <= 0;
      const isLow = stockQty <= minAlert && stockQty > 0;
      return {
        ...it,
        stock_on_hand: stockQty,
        is_low: isLow,
        is_out: isOut,
        status: isOut ? "OUT_OF_STOCK" : (isLow ? "LOW_STOCK" : "IN_STOCK")
      };
    });
  }

  function getFilteredItems() {
    const enriched = getEnrichedMasterItems();
    const f = erpState.items.filters;
    const searchVal = (f.search || "").toLowerCase().trim();

    return enriched.filter(it => {
      // 1. Text Search
      if (searchVal) {
        const matches = 
          (it.item_code || "").toLowerCase().includes(searchVal) ||
          (it.name || "").toLowerCase().includes(searchVal) ||
          (it.brand || "").toLowerCase().includes(searchVal) ||
          (it.category || "").toLowerCase().includes(searchVal) ||
          String(it.barcode || "").toLowerCase().includes(searchVal);
        if (!matches) return false;
      }

      // 2. Category
      if (f.category && f.category !== "ALL") {
        if ((it.category || "").toLowerCase() !== f.category.toLowerCase()) return false;
      }

      // 3. Stock Level
      if (f.stock && f.stock !== "ALL") {
        if (f.stock === "IN_STOCK" && it.stock_on_hand <= 0) return false;
        if (f.stock === "LOW_STOCK" && (!it.is_low && !it.is_out)) return false;
        if (f.stock === "OUT_OF_STOCK" && !it.is_out) return false;
      }

      // 4. Brand
      if (f.brand && f.brand !== "ALL") {
        if ((it.brand || "").toLowerCase() !== f.brand.toLowerCase()) return false;
      }

      // 5. Min Price
      if (f.min_price !== null && !isNaN(f.min_price) && f.min_price > 0) {
        if (parseFloat(it.price || 0) < f.min_price) return false;
      }

      // 6. Max Price
      if (f.max_price !== null && !isNaN(f.max_price) && f.max_price > 0) {
        if (parseFloat(it.price || 0) > f.max_price) return false;
      }

      // 7. GST Rate
      if (f.gst && f.gst !== "ALL") {
        if (parseFloat(it.gst_percent || 0) !== parseFloat(f.gst)) return false;
      }

      return true;
    });
  }

  function renderMasterItems(highlightCode = null) {
    const filtered = getFilteredItems();
    const sorted = sortRecords(filtered, erpState.items.sort);

    // Compute Dynamic KPI Metrics based on filtered records
    let totalStockUnits = 0;
    let inStockCount = 0;
    let lowStockCount = 0;
    let totalValuation = 0;

    filtered.forEach(it => {
      totalStockUnits += it.stock_on_hand;
      if (it.stock_on_hand > 0) inStockCount++;
      if (it.is_low || it.is_out) lowStockCount++;
      totalValuation += (it.stock_on_hand * (parseFloat(it.price) || 0));
    });

    const statTotalItems = document.getElementById("stat-total-items");
    const statTotalStock = document.getElementById("stat-total-stock");
    const statInStock = document.getElementById("stat-in-stock");
    const statLowStock = document.getElementById("stat-low-stock");
    const statValuation = document.getElementById("stat-stock-valuation");
    const countBadge = document.getElementById("items-count-badge");

    if (statTotalItems) statTotalItems.textContent = `${filtered.length} SKUs`;
    if (statTotalStock) statTotalStock.textContent = `${totalStockUnits} Units`;
    if (statInStock) statInStock.textContent = `${inStockCount} SKUs`;
    if (statLowStock) statLowStock.textContent = `${lowStockCount} SKU${lowStockCount !== 1 ? 's' : ''}`;
    if (statValuation) statValuation.textContent = `₹${totalValuation.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    if (countBadge) countBadge.textContent = `${filtered.length} Items`;

    // Active Filters Counter Badge
    let activeFilterCount = 0;
    const f = erpState.items.filters;
    if (f.search) activeFilterCount++;
    if (f.category !== "ALL") activeFilterCount++;
    if (f.stock !== "ALL") activeFilterCount++;
    if (f.brand !== "ALL") activeFilterCount++;
    if (f.min_price) activeFilterCount++;
    if (f.max_price) activeFilterCount++;
    if (f.gst !== "ALL") activeFilterCount++;

    const badgeEl = document.getElementById("items-active-filters-count");
    if (badgeEl) {
      if (activeFilterCount > 0) {
        badgeEl.textContent = `${activeFilterCount} active`;
        badgeEl.style.display = "inline-flex";
      } else {
        badgeEl.style.display = "none";
      }
    }

    // Pagination Slice
    const pageSize = erpState.items.pageSize === "ALL" ? sorted.length : parseInt(erpState.items.pageSize, 10);
    const startIdx = erpState.items.pageSize === "ALL" ? 0 : (erpState.items.page - 1) * pageSize;
    const pageRecords = sorted.slice(startIdx, startIdx + pageSize);

    const itemsTbody = document.querySelector("#table-items-master tbody");
    if (itemsTbody) {
      if (pageRecords.length === 0) {
        itemsTbody.innerHTML = `
          <tr>
            <td colspan="9" style="text-align:center; padding:2rem; color:#94a3b8;">
              <i class="fa-solid fa-magnifying-glass" style="font-size:1.5rem; margin-bottom:0.5rem; display:block;"></i>
              No products found matching the active filter criteria.
            </td>
          </tr>
        `;
      } else {
        itemsTbody.innerHTML = pageRecords.map(it => {
          let badgeHtml = "";
          if (it.is_out) {
            badgeHtml = `<span class="badge badge-warning" style="background:rgba(239,68,68,0.2); color:#ef4444; border:1px solid #ef4444;">OUT OF STOCK (0 Units)</span>`;
          } else if (it.is_low) {
            badgeHtml = `<span class="badge badge-warning" style="background:rgba(245,158,11,0.2); color:#f59e0b; border:1px solid #f59e0b;">LOW STOCK (${it.stock_on_hand} Units)</span>`;
          } else {
            badgeHtml = `<span class="badge badge-success" style="background:rgba(16,185,129,0.2); color:#10b981; border:1px solid #10b981;">IN STOCK (${it.stock_on_hand} Units)</span>`;
          }

          const isHighlighted = (highlightCode && it.item_code === highlightCode);
          const rowStyle = isHighlighted ? 'style="background: rgba(16, 185, 129, 0.22); border-left: 4px solid var(--accent-emerald); font-weight: 600;"' : '';
          const cost = parseFloat(it.cost_price || (it.price * 0.75)).toFixed(2);

          return `
            <tr ${rowStyle}>
              <td><code>${it.item_code}</code></td>
              <td><strong>${it.name}</strong></td>
              <td>${it.brand || "-"}</td>
              <td>${it.category || "-"}</td>
              <td>₹${parseFloat(it.price || 0).toFixed(2)}</td>
              <td>₹${cost}</td>
              <td><span class="badge badge-success">${parseFloat(it.gst_percent || 0)}%</span></td>
              <td><strong style="font-size:1.02rem; color:#f8fafc;">${it.stock_on_hand} Units</strong></td>
              <td>${badgeHtml}</td>
            </tr>
          `;
        }).join("");
      }
    }

    renderPagination("items", sorted.length, "items-pagination-controls", "items-pagination-info");
  }

  // Populate dynamic brand dropdown for items
  function refreshBrandDropdown() {
    const brandSelect = document.getElementById("items-filter-brand");
    if (!brandSelect) return;
    const currentVal = brandSelect.value;
    const brands = Array.from(new Set(erpData.items.map(i => i.brand).filter(Boolean))).sort();
    brandSelect.innerHTML = `<option value="ALL">All Brands</option>` + 
      brands.map(b => `<option value="${b}">${b}</option>`).join("");
    if (brands.includes(currentVal)) {
      brandSelect.value = currentVal;
    }
  }

  // Setup Items Filter Event Listeners
  const itemsSearch = document.getElementById("items-filter-search");
  const itemsCat = document.getElementById("items-filter-category");
  const itemsStock = document.getElementById("items-filter-stock");
  const itemsBrand = document.getElementById("items-filter-brand");
  const itemsMinPrice = document.getElementById("items-filter-min-price");
  const itemsMaxPrice = document.getElementById("items-filter-max-price");
  const itemsGst = document.getElementById("items-filter-gst");
  const itemsPageSize = document.getElementById("items-page-size");
  const btnResetItems = document.getElementById("btn-reset-items-filters");
  const btnExportItems = document.getElementById("btn-export-items-csv");

  if (itemsSearch) {
    itemsSearch.addEventListener("input", (e) => {
      erpState.items.filters.search = e.target.value;
      erpState.items.page = 1;
      renderMasterItems();
    });
  }
  if (itemsCat) {
    itemsCat.addEventListener("change", (e) => {
      erpState.items.filters.category = e.target.value;
      erpState.items.page = 1;
      renderMasterItems();
    });
  }
  if (itemsStock) {
    itemsStock.addEventListener("change", (e) => {
      erpState.items.filters.stock = e.target.value;
      erpState.items.page = 1;
      renderMasterItems();
    });
  }
  if (itemsBrand) {
    itemsBrand.addEventListener("change", (e) => {
      erpState.items.filters.brand = e.target.value;
      erpState.items.page = 1;
      renderMasterItems();
    });
  }
  if (itemsMinPrice) {
    itemsMinPrice.addEventListener("input", (e) => {
      erpState.items.filters.min_price = e.target.value ? parseFloat(e.target.value) : null;
      erpState.items.page = 1;
      renderMasterItems();
    });
  }
  if (itemsMaxPrice) {
    itemsMaxPrice.addEventListener("input", (e) => {
      erpState.items.filters.max_price = e.target.value ? parseFloat(e.target.value) : null;
      erpState.items.page = 1;
      renderMasterItems();
    });
  }
  if (itemsGst) {
    itemsGst.addEventListener("change", (e) => {
      erpState.items.filters.gst = e.target.value;
      erpState.items.page = 1;
      renderMasterItems();
    });
  }
  if (itemsPageSize) {
    itemsPageSize.addEventListener("change", (e) => {
      erpState.items.pageSize = e.target.value;
      erpState.items.page = 1;
      renderMasterItems();
    });
  }
  if (btnResetItems) {
    btnResetItems.addEventListener("click", () => {
      erpState.items.filters = { search: "", category: "ALL", stock: "ALL", brand: "ALL", min_price: null, max_price: null, gst: "ALL" };
      erpState.items.page = 1;
      if (itemsSearch) itemsSearch.value = "";
      if (itemsCat) itemsCat.value = "ALL";
      if (itemsStock) itemsStock.value = "ALL";
      if (itemsBrand) itemsBrand.value = "ALL";
      if (itemsMinPrice) itemsMinPrice.value = "";
      if (itemsMaxPrice) itemsMaxPrice.value = "";
      if (itemsGst) itemsGst.value = "ALL";
      renderMasterItems();
    });
  }
  if (btnExportItems) {
    btnExportItems.addEventListener("click", () => {
      const filtered = sortRecords(getFilteredItems(), erpState.items.sort);
      const headers = ["Item Code", "Item Name", "Brand", "Category", "Retail Price (INR)", "Cost Price (INR)", "GST %", "Stock on Hand", "Min Alert Qty", "Stock Status", "Barcode"];
      const rows = filtered.map(it => [
        it.item_code,
        it.name,
        it.brand || "",
        it.category || "",
        parseFloat(it.price || 0).toFixed(2),
        parseFloat(it.cost_price || (it.price * 0.75)).toFixed(2),
        it.gst_percent || 0,
        it.stock_on_hand,
        it.min_stock_alert || 10,
        it.status,
        it.barcode || ""
      ]);
      exportDataToCSV("products_catalog_export.csv", headers, rows);
    });
  }

  setupSortableHeaders("items", "#table-items-master");

  // =========================================================================
  // MODULE 2: PURCHASE INVOICES (TAB 5)
  // =========================================================================
  function getFilteredPurchases() {
    const f = erpState.purchases.filters;
    const searchVal = (f.search || "").toLowerCase().trim();

    return erpData.purchases.filter(p => {
      // 1. Search text
      if (searchVal) {
        const matches = 
          (p.invoice_no || "").toLowerCase().includes(searchVal) ||
          (p.vendor || "").toLowerCase().includes(searchVal) ||
          (p.item_code || "").toLowerCase().includes(searchVal) ||
          (p.item_name || "").toLowerCase().includes(searchVal);
        if (!matches) return false;
      }

      // 2. Vendor
      if (f.vendor && f.vendor !== "ALL") {
        if ((p.vendor || "").toLowerCase() !== f.vendor.toLowerCase()) return false;
      }

      // 2b. Payment Status
      if (f.payment_status && f.payment_status !== "ALL") {
        const pStatus = (p.payment_status || "UNPAID").toUpperCase();
        if (pStatus !== f.payment_status.toUpperCase()) return false;
      }

      // 3. Date Range
      if (f.date_from && (p.invoice_date || "") < f.date_from) return false;
      if (f.date_to && (p.invoice_date || "") > f.date_to) return false;

      // 4. Min / Max Gross Total
      const tot = parseFloat(p.total_amount) || 0;
      if (f.min_total !== null && !isNaN(f.min_total) && f.min_total > 0 && tot < f.min_total) return false;
      if (f.max_total !== null && !isNaN(f.max_total) && f.max_total > 0 && tot > f.max_total) return false;

      return true;
    });
  }

  function renderPurchasesTable(highlightNo = null) {
    const filtered = getFilteredPurchases();
    const sorted = sortRecords(filtered, erpState.purchases.sort);

    // Dynamic KPI Analytics calculation
    let uniqueBills = new Set();
    let totalLines = filtered.length;
    let totalNet = 0;
    let totalItc = 0;
    let totalGross = 0;

    filtered.forEach(p => {
      if (p.invoice_no) uniqueBills.add(p.invoice_no);
      totalNet += parseFloat(p.net_amount) || 0;
      totalItc += parseFloat(p.gst_amount) || 0;
      totalGross += parseFloat(p.total_amount) || 0;
    });

    const billCount = uniqueBills.size || filtered.length;
    const avgBill = billCount > 0 ? (totalGross / billCount) : 0;

    const purKpiCount = document.getElementById("pur-kpi-count");
    const purKpiLines = document.getElementById("pur-kpi-lines");
    const purKpiNet = document.getElementById("pur-kpi-net");
    const purKpiItc = document.getElementById("pur-kpi-itc");
    const purKpiTotal = document.getElementById("pur-kpi-total");
    const purKpiAvg = document.getElementById("pur-kpi-avg");
    const countBadge = document.getElementById("purchases-count-badge");

    if (purKpiCount) purKpiCount.textContent = `${billCount} Invoice${billCount !== 1 ? 's' : ''}`;
    if (purKpiLines) purKpiLines.textContent = `${totalLines} Line Item${totalLines !== 1 ? 's' : ''}`;
    if (purKpiNet) purKpiNet.textContent = `₹${totalNet.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    if (purKpiItc) purKpiItc.textContent = `₹${totalItc.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    if (purKpiTotal) purKpiTotal.textContent = `₹${totalGross.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    if (purKpiAvg) purKpiAvg.textContent = `₹${avgBill.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    if (countBadge) countBadge.textContent = `${billCount} Invoices (${totalLines} Items)`;

    // Active Filters Counter Badge
    let activeCount = 0;
    const f = erpState.purchases.filters;
    if (f.search) activeCount++;
    if (f.vendor !== "ALL") activeCount++;
    if (f.payment_status && f.payment_status !== "ALL") activeCount++;
    if (f.date_from || f.date_to) activeCount++;
    if (f.min_total) activeCount++;
    if (f.max_total) activeCount++;

    const badgeEl = document.getElementById("purchases-active-filters-count");
    if (badgeEl) {
      if (activeCount > 0) {
        badgeEl.textContent = `${activeCount} active`;
        badgeEl.style.display = "inline-flex";
      } else {
        badgeEl.style.display = "none";
      }
    }

    // Pagination Slice
    const pageSize = erpState.purchases.pageSize === "ALL" ? sorted.length : parseInt(erpState.purchases.pageSize, 10);
    const startIdx = erpState.purchases.pageSize === "ALL" ? 0 : (erpState.purchases.page - 1) * pageSize;
    const pageRecords = sorted.slice(startIdx, startIdx + pageSize);

    const purchasesTbody = document.querySelector("#table-purchases tbody");
    if (purchasesTbody) {
      if (pageRecords.length === 0) {
        purchasesTbody.innerHTML = `
          <tr>
            <td colspan="13" style="text-align:center; padding:2rem; color:#94a3b8;">
              <i class="fa-solid fa-magnifying-glass" style="font-size:1.5rem; margin-bottom:0.5rem; display:block;"></i>
              No purchase invoices found matching the active filter criteria.
            </td>
          </tr>
        `;
      } else {
        purchasesTbody.innerHTML = pageRecords.map(p => {
          const isHighlighted = (highlightNo && p.invoice_no === highlightNo);
          const payStatus = (p.payment_status || "UNPAID").toUpperCase();
          let badgeClass = "badge-unpaid";
          if (payStatus === "PAID") badgeClass = "badge-paid";
          else if (payStatus === "PARTIAL") badgeClass = "badge-partial";
          const balanceDue = p.balance_due !== undefined ? parseFloat(p.balance_due) : (payStatus === "PAID" ? 0 : parseFloat(p.total_amount || 0));

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
              <td><span class="${badgeClass}">${payStatus}</span></td>
              <td style="text-align: center; white-space: nowrap;">
                <button class="btn btn-secondary" style="padding:0.25rem 0.5rem; font-size:0.75rem;" onclick="printPurchaseBill('${p.invoice_no}')" title="Print Purchase Invoice">
                  <i class="fa-solid fa-print"></i>
                </button>
                ${payStatus !== 'PAID' ? `
                  <button class="btn btn-success btn-pay-vendor" style="padding:0.25rem 0.5rem; font-size:0.75rem; margin-left: 0.25rem;" 
                    onclick="window.openVendorPaymentModal('${p.invoice_no}', '${(p.vendor||'').replace(/'/g, "\\'")}', ${parseFloat(p.total_amount||0)}, ${balanceDue})" title="Pay Vendor Bill">
                    <i class="fa-solid fa-money-bill-wave"></i> Pay
                  </button>
                ` : ''}
              </td>
            </tr>
          `;
        }).join("");
      }
    }

    renderPagination("purchases", sorted.length, "purchases-pagination-controls", "purchases-pagination-info");
  }

  // Setup Purchases Filter Listeners
  const purSearch = document.getElementById("purchases-filter-search");
  const purVendor = document.getElementById("purchases-filter-vendor");
  const purDateFrom = document.getElementById("purchases-filter-date-from");
  const purDateTo = document.getElementById("purchases-filter-date-to");
  const purMinTotal = document.getElementById("purchases-filter-min-total");
  const purMaxTotal = document.getElementById("purchases-filter-max-total");
  const purPaymentStatus = document.getElementById("purchases-filter-payment-status");
  const purPageSize = document.getElementById("purchases-page-size");
  const btnResetPur = document.getElementById("btn-reset-purchases-filters");

  if (purPaymentStatus) {
    purPaymentStatus.addEventListener("change", (e) => {
      erpState.purchases.filters.payment_status = e.target.value;
      erpState.purchases.page = 1;
      renderPurchasesTable();
    });
  }
  const btnExportPur = document.getElementById("btn-export-purchases-csv");

  if (purSearch) {
    purSearch.addEventListener("input", (e) => {
      erpState.purchases.filters.search = e.target.value;
      erpState.purchases.page = 1;
      renderPurchasesTable();
    });
  }
  if (purVendor) {
    purVendor.addEventListener("change", (e) => {
      erpState.purchases.filters.vendor = e.target.value;
      erpState.purchases.page = 1;
      renderPurchasesTable();
    });
  }
  if (purDateFrom) {
    purDateFrom.addEventListener("change", (e) => {
      erpState.purchases.filters.date_from = e.target.value;
      erpState.purchases.page = 1;
      renderPurchasesTable();
    });
  }
  if (purDateTo) {
    purDateTo.addEventListener("change", (e) => {
      erpState.purchases.filters.date_to = e.target.value;
      erpState.purchases.page = 1;
      renderPurchasesTable();
    });
  }
  if (purMinTotal) {
    purMinTotal.addEventListener("input", (e) => {
      erpState.purchases.filters.min_total = e.target.value ? parseFloat(e.target.value) : null;
      erpState.purchases.page = 1;
      renderPurchasesTable();
    });
  }
  if (purMaxTotal) {
    purMaxTotal.addEventListener("input", (e) => {
      erpState.purchases.filters.max_total = e.target.value ? parseFloat(e.target.value) : null;
      erpState.purchases.page = 1;
      renderPurchasesTable();
    });
  }
  if (purPageSize) {
    purPageSize.addEventListener("change", (e) => {
      erpState.purchases.pageSize = e.target.value;
      erpState.purchases.page = 1;
      renderPurchasesTable();
    });
  }

  // Purchases Date Presets
  document.querySelectorAll('.preset-pill[data-module="purchases"]').forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll('.preset-pill[data-module="purchases"]').forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const range = btn.getAttribute("data-range");
      erpState.purchases.filters.preset = range;
      const { from, to } = getDatePresetRange(range);
      erpState.purchases.filters.date_from = from;
      erpState.purchases.filters.date_to = to;
      if (purDateFrom) purDateFrom.value = from;
      if (purDateTo) purDateTo.value = to;
      erpState.purchases.page = 1;
      renderPurchasesTable();
    });
  });

  if (btnResetPur) {
    btnResetPur.addEventListener("click", () => {
      erpState.purchases.filters = { search: "", vendor: "ALL", date_from: "", date_to: "", min_total: null, max_total: null, preset: "ALL" };
      erpState.purchases.page = 1;
      if (purSearch) purSearch.value = "";
      if (purVendor) purVendor.value = "ALL";
      if (purDateFrom) purDateFrom.value = "";
      if (purDateTo) purDateTo.value = "";
      if (purMinTotal) purMinTotal.value = "";
      if (purMaxTotal) purMaxTotal.value = "";
      if (purPaymentStatus) purPaymentStatus.value = "ALL";
      erpState.purchases.filters.payment_status = "ALL";
      document.querySelectorAll('.preset-pill[data-module="purchases"]').forEach(b => b.classList.toggle("active", b.getAttribute("data-range") === "ALL"));
      renderPurchasesTable();
    });
  }

  if (btnExportPur) {
    btnExportPur.addEventListener("click", () => {
      const filtered = sortRecords(getFilteredPurchases(), erpState.purchases.sort);
      const headers = ["Bill No", "Date", "Vendor", "Item Code", "Item Name", "Qty", "Rate (INR)", "Net Amount (INR)", "GST Rate %", "ITC Amount (INR)", "Gross Total (INR)"];
      const rows = filtered.map(p => [
        p.invoice_no,
        p.invoice_date,
        p.vendor,
        p.item_code,
        p.item_name,
        p.quantity,
        parseFloat(p.rate).toFixed(2),
        parseFloat(p.net_amount).toFixed(2),
        p.gst_percent,
        parseFloat(p.gst_amount).toFixed(2),
        parseFloat(p.total_amount).toFixed(2)
      ]);
      exportDataToCSV("purchase_invoices_export.csv", headers, rows);
    });
  }

  setupSortableHeaders("purchases", "#table-purchases");

  // =========================================================================
  // MODULE 3: CUSTOMER SALES INVOICES & POS (TAB 4)
  // =========================================================================
  function getFilteredSales() {
    const f = erpState.sales.filters;
    const searchVal = (f.search || "").toLowerCase().trim();

    return erpData.sales.filter(s => {
      // 1. Text Search
      if (searchVal) {
        const matches = 
          (s.invoice_no || "").toLowerCase().includes(searchVal) ||
          (s.customer_name || "").toLowerCase().includes(searchVal) ||
          (s.customer_city || "").toLowerCase().includes(searchVal) ||
          (s.item_name || "").toLowerCase().includes(searchVal);
        if (!matches) return false;
      }

      // 2. Customer
      if (f.customer && f.customer !== "ALL") {
        if ((s.customer_name || "").toLowerCase() !== f.customer.toLowerCase()) return false;
      }

      // 3. City
      if (f.city && f.city !== "ALL") {
        if ((s.customer_city || "").toLowerCase() !== f.city.toLowerCase()) return false;
      }

      // 4. Date Range
      if (f.date_from && (s.invoice_date || "") < f.date_from) return false;
      if (f.date_to && (s.invoice_date || "") > f.date_to) return false;

      // 5. Min / Max Gross Total
      const tot = parseFloat(s.total_amount) || 0;
      if (f.min_total !== null && !isNaN(f.min_total) && f.min_total > 0 && tot < f.min_total) return false;
      if (f.max_total !== null && !isNaN(f.max_total) && f.max_total > 0 && tot > f.max_total) return false;

      return true;
    });
  }

  function renderSalesTable() {
    const filtered = getFilteredSales();
    const sorted = sortRecords(filtered, erpState.sales.sort);

    // Compute Dynamic KPI Metrics based on filtered sales
    let uniqueInvoices = new Set();
    let totalQty = 0;
    let totalNet = 0;
    let totalGst = 0;
    let totalGross = 0;

    filtered.forEach(s => {
      if (s.invoice_no) uniqueInvoices.add(s.invoice_no);
      totalQty += parseFloat(s.quantity) || 0;
      totalNet += parseFloat(s.net_amount) || 0;
      totalGst += parseFloat(s.gst_amount) || 0;
      totalGross += parseFloat(s.total_amount) || 0;
    });

    const invoiceCount = uniqueInvoices.size || filtered.length;
    const avgTicket = invoiceCount > 0 ? (totalGross / invoiceCount) : 0;

    const salesKpiCount = document.getElementById("sales-kpi-count");
    const salesKpiQty = document.getElementById("sales-kpi-qty");
    const salesKpiNet = document.getElementById("sales-kpi-net");
    const salesKpiGst = document.getElementById("sales-kpi-gst");
    const salesKpiTotal = document.getElementById("sales-kpi-total");
    const salesKpiAvg = document.getElementById("sales-kpi-avg");
    const countBadge = document.getElementById("sales-count-badge");

    if (salesKpiCount) salesKpiCount.textContent = `${invoiceCount} Invoice${invoiceCount !== 1 ? 's' : ''}`;
    if (salesKpiQty) salesKpiQty.textContent = `${totalQty} Units`;
    if (salesKpiNet) salesKpiNet.textContent = `₹${totalNet.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    if (salesKpiGst) salesKpiGst.textContent = `₹${totalGst.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    if (salesKpiTotal) salesKpiTotal.textContent = `₹${totalGross.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    if (salesKpiAvg) salesKpiAvg.textContent = `₹${avgTicket.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    if (countBadge) countBadge.textContent = `${invoiceCount} Invoices`;

    // Active Filters Counter Badge
    let activeCount = 0;
    const f = erpState.sales.filters;
    if (f.search) activeCount++;
    if (f.customer !== "ALL") activeCount++;
    if (f.city !== "ALL") activeCount++;
    if (f.date_from || f.date_to) activeCount++;
    if (f.min_total) activeCount++;
    if (f.max_total) activeCount++;

    const badgeEl = document.getElementById("sales-active-filters-count");
    if (badgeEl) {
      if (activeCount > 0) {
        badgeEl.textContent = `${activeCount} active`;
        badgeEl.style.display = "inline-flex";
      } else {
        badgeEl.style.display = "none";
      }
    }

    // Pagination Slice
    const pageSize = erpState.sales.pageSize === "ALL" ? sorted.length : parseInt(erpState.sales.pageSize, 10);
    const startIdx = erpState.sales.pageSize === "ALL" ? 0 : (erpState.sales.page - 1) * pageSize;
    const pageRecords = sorted.slice(startIdx, startIdx + pageSize);

    const salesTbody = document.querySelector("#table-sales tbody");
    if (salesTbody) {
      if (pageRecords.length === 0) {
        salesTbody.innerHTML = `
          <tr>
            <td colspan="10" style="text-align:center; padding:2rem; color:#94a3b8;">
              <i class="fa-solid fa-magnifying-glass" style="font-size:1.5rem; margin-bottom:0.5rem; display:block;"></i>
              No sales records found matching the active filter criteria.
            </td>
          </tr>
        `;
      } else {
        salesTbody.innerHTML = pageRecords.map(s => `
          <tr>
            <td><strong>${s.invoice_no}</strong></td>
            <td>${s.invoice_date}</td>
            <td>${s.customer_name}</td>
            <td>${s.customer_city}</td>
            <td>${s.item_name}</td>
            <td>${s.quantity}</td>
            <td>₹${parseFloat(s.rate).toFixed(2)}</td>
            <td>₹${parseFloat(s.net_amount).toFixed(2)}</td>
            <td>₹${parseFloat(s.gst_amount).toFixed(2)} (${s.gst_percent}%)</td>
            <td><strong>₹${parseFloat(s.total_amount).toFixed(2)}</strong></td>
          </tr>
        `).join("");
      }
    }

    renderPagination("sales", sorted.length, "sales-pagination-controls", "sales-pagination-info");
  }

  // Setup Sales Filter Listeners
  const salesSearch = document.getElementById("sales-filter-search");
  const salesCustomer = document.getElementById("sales-filter-customer");
  const salesCity = document.getElementById("sales-filter-city");
  const salesDateFrom = document.getElementById("sales-filter-date-from");
  const salesDateTo = document.getElementById("sales-filter-date-to");
  const salesMinTotal = document.getElementById("sales-filter-min-total");
  const salesMaxTotal = document.getElementById("sales-filter-max-total");
  const salesPageSize = document.getElementById("sales-page-size");
  const btnResetSales = document.getElementById("btn-reset-sales-filters");
  const btnExportSales = document.getElementById("btn-export-sales-csv");

  if (salesSearch) {
    salesSearch.addEventListener("input", (e) => {
      erpState.sales.filters.search = e.target.value;
      erpState.sales.page = 1;
      renderSalesTable();
    });
  }
  if (salesCustomer) {
    salesCustomer.addEventListener("change", (e) => {
      erpState.sales.filters.customer = e.target.value;
      erpState.sales.page = 1;
      renderSalesTable();
    });
  }
  if (salesCity) {
    salesCity.addEventListener("change", (e) => {
      erpState.sales.filters.city = e.target.value;
      erpState.sales.page = 1;
      renderSalesTable();
    });
  }
  if (salesDateFrom) {
    salesDateFrom.addEventListener("change", (e) => {
      erpState.sales.filters.date_from = e.target.value;
      erpState.sales.page = 1;
      renderSalesTable();
    });
  }
  if (salesDateTo) {
    salesDateTo.addEventListener("change", (e) => {
      erpState.sales.filters.date_to = e.target.value;
      erpState.sales.page = 1;
      renderSalesTable();
    });
  }
  if (salesMinTotal) {
    salesMinTotal.addEventListener("input", (e) => {
      erpState.sales.filters.min_total = e.target.value ? parseFloat(e.target.value) : null;
      erpState.sales.page = 1;
      renderSalesTable();
    });
  }
  if (salesMaxTotal) {
    salesMaxTotal.addEventListener("input", (e) => {
      erpState.sales.filters.max_total = e.target.value ? parseFloat(e.target.value) : null;
      erpState.sales.page = 1;
      renderSalesTable();
    });
  }
  if (salesPageSize) {
    salesPageSize.addEventListener("change", (e) => {
      erpState.sales.pageSize = e.target.value;
      erpState.sales.page = 1;
      renderSalesTable();
    });
  }

  // Sales Date Presets
  document.querySelectorAll('.preset-pill[data-module="sales"]').forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll('.preset-pill[data-module="sales"]').forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const range = btn.getAttribute("data-range");
      erpState.sales.filters.preset = range;
      const { from, to } = getDatePresetRange(range);
      erpState.sales.filters.date_from = from;
      erpState.sales.filters.date_to = to;
      if (salesDateFrom) salesDateFrom.value = from;
      if (salesDateTo) salesDateTo.value = to;
      erpState.sales.page = 1;
      renderSalesTable();
    });
  });

  if (btnResetSales) {
    btnResetSales.addEventListener("click", () => {
      erpState.sales.filters = { search: "", customer: "ALL", city: "ALL", date_from: "", date_to: "", min_total: null, max_total: null, preset: "ALL" };
      erpState.sales.page = 1;
      if (salesSearch) salesSearch.value = "";
      if (salesCustomer) salesCustomer.value = "ALL";
      if (salesCity) salesCity.value = "ALL";
      if (salesDateFrom) salesDateFrom.value = "";
      if (salesDateTo) salesDateTo.value = "";
      if (salesMinTotal) salesMinTotal.value = "";
      if (salesMaxTotal) salesMaxTotal.value = "";
      document.querySelectorAll('.preset-pill[data-module="sales"]').forEach(b => b.classList.toggle("active", b.getAttribute("data-range") === "ALL"));
      renderSalesTable();
    });
  }

  if (btnExportSales) {
    btnExportSales.addEventListener("click", () => {
      const filtered = sortRecords(getFilteredSales(), erpState.sales.sort);
      const headers = ["Invoice No", "Date", "Customer", "City", "Item Name", "Quantity", "Rate (INR)", "Net Amount (INR)", "GST Amount (INR)", "GST %", "Gross Total (INR)"];
      const rows = filtered.map(s => [
        s.invoice_no,
        s.invoice_date,
        s.customer_name,
        s.customer_city,
        s.item_name,
        s.quantity,
        parseFloat(s.rate).toFixed(2),
        parseFloat(s.net_amount).toFixed(2),
        parseFloat(s.gst_amount).toFixed(2),
        s.gst_percent,
        parseFloat(s.total_amount).toFixed(2)
      ]);
      exportDataToCSV("sales_invoices_export.csv", headers, rows);
    });
  }

  setupSortableHeaders("sales", "#table-sales");

  // =========================================================================
  // MODULE 4: INVENTORY MOVEMENT AUDIT LEDGER (TAB 7)
  // =========================================================================
  function getFilteredInventory() {
    const f = erpState.inventory.filters;
    const searchVal = (f.search || "").toLowerCase().trim();

    return erpData.stock_ledger.filter(sl => {
      // 1. Text Search
      if (searchVal) {
        const matches = 
          (sl.item_code || "").toLowerCase().includes(searchVal) ||
          (sl.item_name || "").toLowerCase().includes(searchVal) ||
          (sl.voucher_no || "").toLowerCase().includes(searchVal) ||
          (sl.transaction_type || "").toLowerCase().includes(searchVal);
        if (!matches) return false;
      }

      // 2. Item Code
      if (f.item && f.item !== "ALL") {
        if ((sl.item_code || "").toLowerCase() !== f.item.toLowerCase()) return false;
      }

      // 3. Movement Type (IN / OUT)
      if (f.type && f.type !== "ALL") {
        const typeStr = (sl.transaction_type || "").toUpperCase();
        if (f.type === "IN" && !typeStr.includes("IN") && !typeStr.includes("ADD")) return false;
        if (f.type === "OUT" && !typeStr.includes("OUT") && !typeStr.includes("DEDUCT")) return false;
      }

      // 4. Date Range
      if (f.date_from && (sl.date || "") < f.date_from) return false;
      if (f.date_to && (sl.date || "") > f.date_to) return false;

      return true;
    });
  }

  function renderStockLedger(highlightVoucher = null) {
    const filtered = getFilteredInventory();
    const sorted = sortRecords(filtered, erpState.inventory.sort);

    // Compute Dynamic KPI Metrics based on filtered inventory movements
    let totalIn = 0;
    let totalOut = 0;

    filtered.forEach(sl => {
      const qty = parseFloat(sl.quantity) || 0;
      const typeStr = (sl.transaction_type || "").toUpperCase();
      if (typeStr.includes("IN") || typeStr.includes("ADD")) {
        totalIn += qty;
      } else if (typeStr.includes("OUT") || typeStr.includes("DEDUCT")) {
        totalOut += qty;
      }
    });

    const netDelta = totalIn - totalOut;

    const invKpiMovements = document.getElementById("inv-kpi-movements");
    const invKpiIn = document.getElementById("inv-kpi-in");
    const invKpiOut = document.getElementById("inv-kpi-out");
    const invKpiNet = document.getElementById("inv-kpi-net");
    const countBadge = document.getElementById("inv-count-badge");

    if (invKpiMovements) invKpiMovements.textContent = `${filtered.length} Events`;
    if (invKpiIn) invKpiIn.textContent = `${totalIn} Units`;
    if (invKpiOut) invKpiOut.textContent = `${totalOut} Units`;
    if (invKpiNet) invKpiNet.textContent = `${netDelta >= 0 ? '+' : ''}${netDelta} Units`;
    if (countBadge) countBadge.textContent = `${filtered.length} Movements`;

    // Active Filters Counter Badge
    let activeCount = 0;
    const f = erpState.inventory.filters;
    if (f.search) activeCount++;
    if (f.item !== "ALL") activeCount++;
    if (f.type !== "ALL") activeCount++;
    if (f.date_from || f.date_to) activeCount++;

    const badgeEl = document.getElementById("inv-active-filters-count");
    if (badgeEl) {
      if (activeCount > 0) {
        badgeEl.textContent = `${activeCount} active`;
        badgeEl.style.display = "inline-flex";
      } else {
        badgeEl.style.display = "none";
      }
    }

    // Pagination Slice
    const pageSize = erpState.inventory.pageSize === "ALL" ? sorted.length : parseInt(erpState.inventory.pageSize, 10);
    const startIdx = erpState.inventory.pageSize === "ALL" ? 0 : (erpState.inventory.page - 1) * pageSize;
    const pageRecords = sorted.slice(startIdx, startIdx + pageSize);

    const stockTbody = document.querySelector("#table-stock-ledger tbody");
    if (stockTbody) {
      if (pageRecords.length === 0) {
        stockTbody.innerHTML = `
          <tr>
            <td colspan="6" style="text-align:center; padding:2rem; color:#94a3b8;">
              <i class="fa-solid fa-magnifying-glass" style="font-size:1.5rem; margin-bottom:0.5rem; display:block;"></i>
              No inventory movements found matching the active filter criteria.
            </td>
          </tr>
        `;
      } else {
        stockTbody.innerHTML = pageRecords.map(sl => {
          const isOut = (sl.transaction_type || "").toUpperCase().includes("OUT");
          const badgeClass = isOut ? "badge-warning" : "badge-success";
          const isHighlighted = (highlightVoucher && sl.voucher_no === highlightVoucher);
          return `
            <tr class="${isHighlighted ? 'highlight-row' : ''}">
              <td>${sl.date}</td>
              <td><code>${sl.item_code}</code></td>
              <td><strong>${sl.item_name}</strong></td>
              <td><span class="badge ${badgeClass}">${sl.transaction_type}</span></td>
              <td><strong style="color:${isOut ? '#ef4444' : '#10b981'}; font-size:1.02rem;">${isOut ? '-' : '+'}${sl.quantity}</strong></td>
              <td><code>${sl.voucher_no}</code></td>
            </tr>
          `;
        }).join("");
      }
    }

    renderPagination("inventory", sorted.length, "inv-pagination-controls", "inv-pagination-info");
  }

  // Populate dynamic item dropdown for inventory filter
  function refreshInventoryItemDropdown() {
    const itemSelect = document.getElementById("inv-filter-item");
    if (!itemSelect) return;
    const currentVal = itemSelect.value;
    itemSelect.innerHTML = `<option value="ALL">All Items</option>` + 
      erpData.items.map(i => `<option value="${i.item_code}">${i.item_code} - ${i.name}</option>`).join("");
    if (currentVal) itemSelect.value = currentVal;
  }

  // Setup Inventory Filter Listeners
  const invSearch = document.getElementById("inv-filter-search");
  const invItem = document.getElementById("inv-filter-item");
  const invType = document.getElementById("inv-filter-type");
  const invDateFrom = document.getElementById("inv-filter-date-from");
  const invDateTo = document.getElementById("inv-filter-date-to");
  const invPageSize = document.getElementById("inv-page-size");
  const btnResetInv = document.getElementById("btn-reset-inventory-filters");
  const btnExportInv = document.getElementById("btn-export-inventory-csv");

  if (invSearch) {
    invSearch.addEventListener("input", (e) => {
      erpState.inventory.filters.search = e.target.value;
      erpState.inventory.page = 1;
      renderStockLedger();
    });
  }
  if (invItem) {
    invItem.addEventListener("change", (e) => {
      erpState.inventory.filters.item = e.target.value;
      erpState.inventory.page = 1;
      renderStockLedger();
    });
  }
  if (invType) {
    invType.addEventListener("change", (e) => {
      erpState.inventory.filters.type = e.target.value;
      erpState.inventory.page = 1;
      renderStockLedger();
    });
  }
  if (invDateFrom) {
    invDateFrom.addEventListener("change", (e) => {
      erpState.inventory.filters.date_from = e.target.value;
      erpState.inventory.page = 1;
      renderStockLedger();
    });
  }
  if (invDateTo) {
    invDateTo.addEventListener("change", (e) => {
      erpState.inventory.filters.date_to = e.target.value;
      erpState.inventory.page = 1;
      renderStockLedger();
    });
  }
  if (invPageSize) {
    invPageSize.addEventListener("change", (e) => {
      erpState.inventory.pageSize = e.target.value;
      erpState.inventory.page = 1;
      renderStockLedger();
    });
  }

  // Inventory Date Presets
  document.querySelectorAll('.preset-pill[data-module="inventory"]').forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll('.preset-pill[data-module="inventory"]').forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const range = btn.getAttribute("data-range");
      erpState.inventory.filters.preset = range;
      const { from, to } = getDatePresetRange(range);
      erpState.inventory.filters.date_from = from;
      erpState.inventory.filters.date_to = to;
      if (invDateFrom) invDateFrom.value = from;
      if (invDateTo) invDateTo.value = to;
      erpState.inventory.page = 1;
      renderStockLedger();
    });
  });

  if (btnResetInv) {
    btnResetInv.addEventListener("click", () => {
      erpState.inventory.filters = { search: "", item: "ALL", type: "ALL", date_from: "", date_to: "", preset: "ALL" };
      erpState.inventory.page = 1;
      if (invSearch) invSearch.value = "";
      if (invItem) invItem.value = "ALL";
      if (invType) invType.value = "ALL";
      if (invDateFrom) invDateFrom.value = "";
      if (invDateTo) invDateTo.value = "";
      document.querySelectorAll('.preset-pill[data-module="inventory"]').forEach(b => b.classList.toggle("active", b.getAttribute("data-range") === "ALL"));
      renderStockLedger();
    });
  }

  if (btnExportInv) {
    btnExportInv.addEventListener("click", () => {
      const filtered = sortRecords(getFilteredInventory(), erpState.inventory.sort);
      const headers = ["Date", "Item Code", "Item Name", "Movement Type", "Quantity", "Voucher Reference"];
      const rows = filtered.map(sl => [
        sl.date,
        sl.item_code,
        sl.item_name,
        sl.transaction_type,
        sl.quantity,
        sl.voucher_no
      ]);
      exportDataToCSV("inventory_movement_ledger_export.csv", headers, rows);
    });
  }

  setupSortableHeaders("inventory", "#table-stock-ledger");

  // =========================================================================
  // MODULE 5: GST TAX & ITC RECONCILIATION REPORT (TAB 3)
  // =========================================================================
  function renderGSTReport() {
    const f = erpState.gst.filters;

    // Filter purchases for ITC
    const filteredPurchases = erpData.purchases.filter(p => {
      if (f.vendor && f.vendor !== "ALL" && (p.vendor || "").toLowerCase() !== f.vendor.toLowerCase()) return false;
      if (f.date_from && (p.invoice_date || "") < f.date_from) return false;
      if (f.date_to && (p.invoice_date || "") > f.date_to) return false;
      return true;
    });

    // Filter sales for Output Tax
    const filteredSales = erpData.sales.filter(s => {
      if (f.date_from && (s.invoice_date || "") < f.date_from) return false;
      if (f.date_to && (s.invoice_date || "") > f.date_to) return false;
      return true;
    });

    let outputGst = 0;
    filteredSales.forEach(s => {
      outputGst += parseFloat(s.gst_amount) || 0;
    });

    let inputGst = 0;
    filteredPurchases.forEach(p => {
      inputGst += parseFloat(p.gst_amount) || 0;
    });

    outputGst = Math.round(outputGst * 100) / 100;
    inputGst = Math.round(inputGst * 100) / 100;

    const itcUtilized = Math.min(outputGst, inputGst);
    const netPayable = Math.max(0, outputGst - inputGst);
    const excessItc = Math.max(0, inputGst - outputGst);

    const gstOutputEl = document.getElementById("gst-kpi-output");
    const gstItcEl = document.getElementById("gst-kpi-itc");
    const gstUtilizedEl = document.getElementById("gst-kpi-utilized");
    const gstPayableEl = document.getElementById("gst-kpi-payable");
    const gstExcessEl = document.getElementById("gst-kpi-excess");
    const gstCountBadge = document.getElementById("gst-count-badge");
    const tableTotalEl = document.getElementById("gst-itc-table-total");

    if (gstOutputEl) gstOutputEl.textContent = `₹${outputGst.toFixed(2)}`;
    if (gstItcEl) gstItcEl.textContent = `₹${inputGst.toFixed(2)}`;
    if (gstUtilizedEl) gstUtilizedEl.textContent = `₹${itcUtilized.toFixed(2)}`;
    if (gstPayableEl) gstPayableEl.textContent = `₹${netPayable.toFixed(2)}`;
    if (gstExcessEl) gstExcessEl.textContent = `₹${excessItc.toFixed(2)}`;
    if (gstCountBadge) gstCountBadge.textContent = `${filteredPurchases.length} Bills Reconciled`;
    if (tableTotalEl) tableTotalEl.textContent = `₹${inputGst.toFixed(2)}`;

    // Group purchases by voucher for ITC reconciliation rows
    const voucherMap = {};
    filteredPurchases.forEach(p => {
      const v = p.invoice_no;
      if (!voucherMap[v]) {
        voucherMap[v] = {
          vendor: p.vendor,
          voucher_no: p.invoice_no,
          date: p.invoice_date,
          taxable_val: 0,
          itc_amount: 0,
          gst_percent: p.gst_percent
        };
      }
      voucherMap[v].taxable_val += (parseFloat(p.net_amount) || 0);
      voucherMap[v].itc_amount += (parseFloat(p.gst_amount) || 0);
    });

    const tbody = document.getElementById("gst-itc-tbody");
    if (tbody) {
      const rows = Object.values(voucherMap);
      if (rows.length === 0) {
        tbody.innerHTML = `
          <tr>
            <td colspan="7" style="text-align:center; padding:2rem; color:#94a3b8;">
              <i class="fa-solid fa-magnifying-glass" style="font-size:1.5rem; margin-bottom:0.5rem; display:block;"></i>
              No vendor ITC records found for the selected period.
            </td>
          </tr>
        `;
      } else {
        const trHtml = rows.map(r => `
          <tr>
            <td><strong>${r.vendor}</strong></td>
            <td><code>${r.voucher_no}</code></td>
            <td>${r.date}</td>
            <td>₹${r.taxable_val.toFixed(2)}</td>
            <td>${r.gst_percent}%</td>
            <td><strong>₹${r.itc_amount.toFixed(2)}</strong></td>
            <td><span class="badge badge-success">ELIGIBLE (GSTR-2B Matched)</span></td>
          </tr>
        `).join("");

        tbody.innerHTML = trHtml + `
          <tr style="background: rgba(16, 185, 129, 0.1); font-weight: bold;">
            <td colspan="5"><strong>TOTAL INPUT TAX CREDIT (ITC) AVAILABLE</strong></td>
            <td><strong>₹${inputGst.toFixed(2)}</strong></td>
            <td><span class="badge badge-success">100% Reconciled</span></td>
          </tr>
        `;
      }
    }
  }

  // Setup GST Filter Listeners
  const gstDateFrom = document.getElementById("gst-filter-date-from");
  const gstDateTo = document.getElementById("gst-filter-date-to");
  const gstVendor = document.getElementById("gst-filter-vendor");
  const btnResetGst = document.getElementById("btn-reset-gst-filters");
  const btnExportGst = document.getElementById("btn-export-gst-csv");

  if (gstDateFrom) {
    gstDateFrom.addEventListener("change", (e) => {
      erpState.gst.filters.date_from = e.target.value;
      renderGSTReport();
    });
  }
  if (gstDateTo) {
    gstDateTo.addEventListener("change", (e) => {
      erpState.gst.filters.date_to = e.target.value;
      renderGSTReport();
    });
  }
  if (gstVendor) {
    gstVendor.addEventListener("change", (e) => {
      erpState.gst.filters.vendor = e.target.value;
      renderGSTReport();
    });
  }

  // GST Date Presets
  document.querySelectorAll('.preset-pill[data-module="gst"]').forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll('.preset-pill[data-module="gst"]').forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const range = btn.getAttribute("data-range");
      erpState.gst.filters.preset = range;
      const { from, to } = getDatePresetRange(range);
      erpState.gst.filters.date_from = from;
      erpState.gst.filters.date_to = to;
      if (gstDateFrom) gstDateFrom.value = from;
      if (gstDateTo) gstDateTo.value = to;
      renderGSTReport();
    });
  });

  if (btnResetGst) {
    btnResetGst.addEventListener("click", () => {
      erpState.gst.filters = { date_from: "", date_to: "", vendor: "ALL", preset: "ALL" };
      if (gstDateFrom) gstDateFrom.value = "";
      if (gstDateTo) gstDateTo.value = "";
      if (gstVendor) gstVendor.value = "ALL";
      document.querySelectorAll('.preset-pill[data-module="gst"]').forEach(b => b.classList.toggle("active", b.getAttribute("data-range") === "ALL"));
      renderGSTReport();
    });
  }

  if (btnExportGst) {
    btnExportGst.addEventListener("click", () => {
      const headers = ["Metric / Voucher", "Vendor / Head", "Date", "Taxable Value (INR)", "Input GST Rate", "ITC Amount (INR)", "Status"];
      const rows = [];
      const f = erpState.gst.filters;
      const filteredPurchases = erpData.purchases.filter(p => {
        if (f.vendor && f.vendor !== "ALL" && (p.vendor || "").toLowerCase() !== f.vendor.toLowerCase()) return false;
        if (f.date_from && (p.invoice_date || "") < f.date_from) return false;
        if (f.date_to && (p.invoice_date || "") > f.date_to) return false;
        return true;
      });

      filteredPurchases.forEach(p => {
        rows.push([
          p.invoice_no,
          p.vendor,
          p.invoice_date,
          parseFloat(p.net_amount).toFixed(2),
          `${p.gst_percent}%`,
          parseFloat(p.gst_amount).toFixed(2),
          "ELIGIBLE"
        ]);
      });
      exportDataToCSV("gst_itc_reconciliation_report.csv", headers, rows);
    });
  }

  // =========================================================================
  // MODULE 6: PROFIT & LOSS STATEMENT (TAB 2)
  // =========================================================================
  function renderPnLStatement() {
    const f = erpState.pnl.filters;

    // Filter sales
    const filteredSales = erpData.sales.filter(s => {
      if (f.date_from && (s.invoice_date || "") < f.date_from) return false;
      if (f.date_to && (s.invoice_date || "") > f.date_to) return false;
      return true;
    });

    let grossSales = 0;
    let gstOutput = 0;
    let netRevenue = 0;

    filteredSales.forEach(s => {
      grossSales += parseFloat(s.total_amount) || 0;
      gstOutput += parseFloat(s.gst_amount) || 0;
      netRevenue += parseFloat(s.net_amount) || 0;
    });

    // Calculate COGS: Units sold * item cost price
    let cogsTotal = 0;
    const cogsBreakdown = [];
    const itemCatalog = {};
    erpData.items.forEach(it => { itemCatalog[it.name] = it; });

    filteredSales.forEach(s => {
      const it = itemCatalog[s.item_name] || {};
      const unitCost = parseFloat(it.cost_price || (parseFloat(s.rate) * 0.75));
      const lineCogs = Math.round((s.quantity * unitCost) * 100) / 100;
      cogsTotal += lineCogs;
      cogsBreakdown.push({
        name: s.item_name,
        qty: s.quantity,
        unitCost: unitCost,
        totalCost: lineCogs
      });
    });

    cogsTotal = Math.round(cogsTotal * 100) / 100;
    const grossProfit = Math.round((netRevenue - cogsTotal) * 100) / 100;
    const gpMargin = netRevenue > 0 ? ((grossProfit / netRevenue) * 100).toFixed(1) : "0.0";
    const opex = parseFloat(f.opex) || 850.0;
    const netProfit = Math.round((grossProfit - opex) * 100) / 100;

    const pnlGrossRev = document.getElementById("pnl-gross-rev");
    const pnlGstOut = document.getElementById("pnl-gst-out");
    const pnlNetRev = document.getElementById("pnl-net-rev");
    const pnlTotalCogs = document.getElementById("pnl-total-cogs");
    const pnlGrossProfit = document.getElementById("pnl-gross-profit");
    const pnlOpexDisplay = document.getElementById("pnl-opex-display");
    const pnlNetProfit = document.getElementById("pnl-net-profit");

    if (pnlGrossRev) pnlGrossRev.textContent = `₹${grossSales.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    if (pnlGstOut) pnlGstOut.textContent = `(₹${gstOutput.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })})`;
    if (pnlNetRev) pnlNetRev.textContent = `₹${netRevenue.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    if (pnlTotalCogs) pnlTotalCogs.textContent = `₹${cogsTotal.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    if (pnlGrossProfit) pnlGrossProfit.textContent = `₹${grossProfit.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} (${gpMargin}%)`;
    if (pnlOpexDisplay) pnlOpexDisplay.textContent = `₹${opex.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    if (pnlNetProfit) pnlNetProfit.textContent = `₹${netProfit.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

    const cogsContainer = document.getElementById("pnl-cogs-items-breakdown");
    if (cogsContainer) {
      if (cogsBreakdown.length === 0) {
        cogsContainer.innerHTML = `<div class="pnl-row indent"><span>No product sales recorded in this period</span><span>₹0.00</span></div>`;
      } else {
        cogsContainer.innerHTML = cogsBreakdown.map(c => `
          <div class="pnl-row indent">
            <span>${c.name} (${c.qty} units sold @ ₹${c.unitCost.toFixed(2)} purchase cost)</span>
            <span>₹${c.totalCost.toFixed(2)}</span>
          </div>
        `).join("");
      }
    }
  }

  // Setup PnL Filter Listeners
  const pnlDateFrom = document.getElementById("pnl-filter-date-from");
  const pnlDateTo = document.getElementById("pnl-filter-date-to");
  const pnlOpexInput = document.getElementById("pnl-input-opex");
  const btnResetPnl = document.getElementById("btn-reset-pnl-filters");
  const btnExportPnl = document.getElementById("btn-export-pnl-csv");

  if (pnlDateFrom) {
    pnlDateFrom.addEventListener("change", (e) => {
      erpState.pnl.filters.date_from = e.target.value;
      renderPnLStatement();
    });
  }
  if (pnlDateTo) {
    pnlDateTo.addEventListener("change", (e) => {
      erpState.pnl.filters.date_to = e.target.value;
      renderPnLStatement();
    });
  }
  if (pnlOpexInput) {
    pnlOpexInput.addEventListener("input", (e) => {
      erpState.pnl.filters.opex = parseFloat(e.target.value) || 0;
      renderPnLStatement();
    });
  }

  // PnL Period Presets
  document.querySelectorAll('.preset-pill[data-module="pnl"]').forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll('.preset-pill[data-module="pnl"]').forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const range = btn.getAttribute("data-range");
      erpState.pnl.filters.preset = range;
      const { from, to } = getDatePresetRange(range);
      erpState.pnl.filters.date_from = from;
      erpState.pnl.filters.date_to = to;
      if (pnlDateFrom) pnlDateFrom.value = from;
      if (pnlDateTo) pnlDateTo.value = to;
      renderPnLStatement();
    });
  });

  if (btnResetPnl) {
    btnResetPnl.addEventListener("click", () => {
      erpState.pnl.filters = { date_from: "", date_to: "", opex: 850.0, preset: "ALL" };
      if (pnlDateFrom) pnlDateFrom.value = "";
      if (pnlDateTo) pnlDateTo.value = "";
      if (pnlOpexInput) pnlOpexInput.value = "850.00";
      document.querySelectorAll('.preset-pill[data-module="pnl"]').forEach(b => b.classList.toggle("active", b.getAttribute("data-range") === "ALL"));
      renderPnLStatement();
    });
  }

  if (btnExportPnl) {
    btnExportPnl.addEventListener("click", () => {
      const headers = ["Account Head / Line Item", "Amount (INR)"];
      const rows = [
        ["I. REVENUE FROM OPERATIONS", ""],
        ["Gross Sales of Grocery Supplies", document.getElementById("pnl-gross-rev")?.textContent || "0.00"],
        ["Less: GST Output Tax (Collected)", document.getElementById("pnl-gst-out")?.textContent || "0.00"],
        ["Net Operational Revenue", document.getElementById("pnl-net-rev")?.textContent || "0.00"],
        ["II. COST OF GOODS SOLD (COGS)", ""],
        ["Total Cost of Goods Sold (COGS)", document.getElementById("pnl-total-cogs")?.textContent || "0.00"],
        ["III. GROSS PROFIT", ""],
        ["Gross Profit (Revenue - COGS)", document.getElementById("pnl-gross-profit")?.textContent || "0.00"],
        ["IV. OPERATING EXPENSES", ""],
        ["Store Operations & Delivery Logistics", document.getElementById("pnl-opex-display")?.textContent || "0.00"],
        ["NET OPERATING PROFIT", document.getElementById("pnl-net-profit")?.textContent || "0.00"]
      ];
      exportDataToCSV("profit_and_loss_statement.csv", headers, rows);
    });
  }

  // =========================================================================
  // MODULE 7: PRINT TAX INVOICE & COMMERCIAL BILL (TAB 1)
  // =========================================================================
  let currentInvoiceKey = "INV-2026-001";

  function renderInvoice(invoiceKey) {
    const inv = erpData.invoices[invoiceKey];
    if (!inv) return;

    const isPurchase = inv.type === "PURCHASE" || invoiceKey.startsWith("PUR-");

    const badgeSpan = document.querySelector(".invoice-badge-title");
    if (badgeSpan) {
      badgeSpan.textContent = isPurchase ? "PURCHASE INVOICE / BILL" : "TAX INVOICE";
      badgeSpan.style.background = isPurchase ? "#0284c7" : "#0f172a";
    }

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

  const invoiceSelector = document.getElementById("invoice-selector");
  if (invoiceSelector) {
    invoiceSelector.addEventListener("change", (e) => {
      currentInvoiceKey = e.target.value;
      renderInvoice(currentInvoiceKey);
    });
  }

  window.printPurchaseBill = function(invoiceNo) {
    if (invoiceSelector) {
      let opt = invoiceSelector.querySelector(`option[value="${invoiceNo}"]`);
      if (!opt) {
        const purGroup = invoiceSelector.querySelector('optgroup[label*="Purchase"]') || invoiceSelector;
        const newOpt = document.createElement("option");
        newOpt.value = invoiceNo;
        newOpt.textContent = `${invoiceNo} (Vendor Purchase Bill)`;
        purGroup.appendChild(newOpt);
      }
      invoiceSelector.value = invoiceNo;
    }
    currentInvoiceKey = invoiceNo;
    switchTab("tab-invoice");
    renderInvoice(invoiceNo);
  };

  renderInvoice(currentInvoiceKey);

  // =========================================================================
  // MULTI-ITEM PURCHASE BILL ENGINE (Client Audio Requirement)
  // =========================================================================
  let currentBillItems = [];

  function renderCurrentBillItems() {
    const container = document.getElementById("pur-line-items-container");
    const tbody = document.getElementById("pur-line-items-tbody");
    const countBadge = document.getElementById("pur-line-items-count");
    const sumNet = document.getElementById("pur-sum-net");
    const sumGst = document.getElementById("pur-sum-gst");
    const sumTotal = document.getElementById("pur-sum-total");

    if (countBadge) countBadge.textContent = currentBillItems.length;

    if (currentBillItems.length === 0) {
      if (container) container.style.display = "none";
      if (tbody) tbody.innerHTML = "";

      const qty = parseFloat(document.getElementById("pur-input-qty")?.value) || 0;
      const rate = parseFloat(document.getElementById("pur-input-rate")?.value) || 0;
      const gstPct = parseFloat(document.getElementById("pur-input-gst")?.value) || 0;
      const net = Math.round(qty * rate * 100) / 100;
      const gstAmt = Math.round(net * (gstPct / 100.0) * 100) / 100;
      const total = Math.round((net + gstAmt) * 100) / 100;

      if (sumNet) sumNet.textContent = `₹${net.toFixed(2)}`;
      if (sumGst) sumGst.textContent = `₹${gstAmt.toFixed(2)} (${gstPct}%)`;
      if (sumTotal) sumTotal.textContent = `₹${total.toFixed(2)}`;
      return;
    }

    if (container) container.style.display = "block";

    let totalNet = 0;
    let totalGst = 0;

    if (tbody) {
      tbody.innerHTML = currentBillItems.map((it, idx) => {
        const net = Math.round(it.quantity * it.rate * 100) / 100;
        const gst = Math.round(net * (it.gst_percent / 100.0) * 100) / 100;
        const total = Math.round((net + gst) * 100) / 100;

        totalNet += net;
        totalGst += gst;

        return `
          <tr>
            <td><code>${it.item_code}</code></td>
            <td><strong>${it.item_name}</strong></td>
            <td>${it.quantity}</td>
            <td>₹${parseFloat(it.rate).toFixed(2)}</td>
            <td><span class="badge badge-warning">${it.gst_percent}%</span></td>
            <td>₹${net.toFixed(2)}</td>
            <td><strong style="color:var(--accent-emerald);">₹${gst.toFixed(2)}</strong></td>
            <td><strong>₹${total.toFixed(2)}</strong></td>
            <td style="text-align: center;">
              <button type="button" class="btn btn-secondary btn-sm" style="padding: 0.2rem 0.5rem; color: #ef4444;" onclick="window.removePurchaseBillItem(${idx})">
                <i class="fa-solid fa-trash"></i>
              </button>
            </td>
          </tr>
        `;
      }).join("");
    }

    const grossTotal = Math.round((totalNet + totalGst) * 100) / 100;
    if (sumNet) sumNet.textContent = `₹${totalNet.toFixed(2)}`;
    if (sumGst) sumGst.textContent = `₹${totalGst.toFixed(2)}`;
    if (sumTotal) sumTotal.textContent = `₹${grossTotal.toFixed(2)}`;
  }

  window.removePurchaseBillItem = function(idx) {
    if (idx >= 0 && idx < currentBillItems.length) {
      currentBillItems.splice(idx, 1);
      renderCurrentBillItems();
    }
  };

  function updatePurchaseFormCalculations() {
    renderCurrentBillItems();
  }

  const purVendorSelect = document.getElementById("pur-input-vendor");
  if (purVendorSelect) {
    purVendorSelect.addEventListener("change", () => {
      const selectedOpt = purVendorSelect.options[purVendorSelect.selectedIndex];
      const gstin = selectedOpt?.getAttribute("data-gstin") || "33AAAAA0000A1Z5";
      const gstinInput = document.getElementById("pur-input-gstin");
      if (gstinInput) gstinInput.value = gstin;
    });
  }

  function syncSelectedItemDefaults() {
    const itemSelect = document.getElementById("pur-input-item-code");
    if (itemSelect && itemSelect.selectedIndex >= 0) {
      const selectedOpt = itemSelect.options[itemSelect.selectedIndex];
      const rate = selectedOpt?.getAttribute("data-rate");
      const gst = selectedOpt?.getAttribute("data-gst");
      const rateInput = document.getElementById("pur-input-rate");
      const gstInput = document.getElementById("pur-input-gst");
      if (rate && rateInput && (!rateInput.value || parseFloat(rateInput.value) <= 0)) {
        rateInput.value = rate;
      }
      if (gst && gstInput) {
        gstInput.value = gst;
      }
    }
  }

  const purItemSelectInput = document.getElementById("pur-input-item-code");
  if (purItemSelectInput) {
    purItemSelectInput.addEventListener("change", () => {
      const selectedOpt = purItemSelectInput.options[purItemSelectInput.selectedIndex];
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

  ["pur-input-qty", "pur-input-rate", "pur-input-gst"].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener("input", updatePurchaseFormCalculations);
      el.addEventListener("change", updatePurchaseFormCalculations);
    }
  });

  const purDateInput = document.getElementById("pur-input-date");
  if (purDateInput && !purDateInput.value) {
    purDateInput.value = new Date().toISOString().split("T")[0];
  }
  syncSelectedItemDefaults();
  updatePurchaseFormCalculations();

  // Add Line Item to Bill button handler (Unique ID: btn-add-bill-item)
  const btnAddBillItem = document.getElementById("btn-add-bill-item");
  if (btnAddBillItem) {
    btnAddBillItem.addEventListener("click", () => {
      const itemSelect = document.getElementById("pur-input-item-code");
      const itemCode = itemSelect ? itemSelect.value : "ITM001";
      const selectedItemOpt = itemSelect ? itemSelect.options[itemSelect.selectedIndex] : null;
      const itemName = selectedItemOpt?.getAttribute("data-name") || "Basmati Rice 5kg";
      const qty = parseFloat(document.getElementById("pur-input-qty")?.value) || 0;
      let rate = parseFloat(document.getElementById("pur-input-rate")?.value) || 0;
      const gst = parseFloat(document.getElementById("pur-input-gst")?.value) || 0;

      if (rate <= 0 && selectedItemOpt?.getAttribute("data-rate")) {
        rate = parseFloat(selectedItemOpt.getAttribute("data-rate")) || 0;
        const rateEl = document.getElementById("pur-input-rate");
        if (rateEl) rateEl.value = rate;
      }

      if (qty <= 0) {
        alert("Please enter a valid Quantity (greater than 0)");
        document.getElementById("pur-input-qty")?.focus();
        return;
      }
      if (rate <= 0) {
        alert("Please enter a valid Purchase Rate ₹ (greater than 0)");
        document.getElementById("pur-input-rate")?.focus();
        return;
      }

      currentBillItems.push({
        item_code: itemCode,
        item_name: itemName,
        quantity: qty,
        rate: rate,
        gst_percent: gst
      });

      const qtyInput = document.getElementById("pur-input-qty");
      if (qtyInput) {
        qtyInput.value = "";
        qtyInput.focus();
      }

      renderCurrentBillItems();
    });
  }

  // Submit Purchase Invoice Function
  async function submitPurchaseInvoice(payload) {
    const btn = document.getElementById("btn-submit-purchase");
    const originalBtnHtml = btn ? btn.innerHTML : `<i class="fa-solid fa-check"></i> Save Purchase Invoice`;

    if (btn) {
      btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Saving...`;
      btn.disabled = true;
    }

    try {
      await fetch("/api/purchases/invoice", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
    } catch (e) {
      console.warn("Backend purchase sync fallback:", e);
    }

    // Add purchase line items to local erpData.purchases
    payload.items.forEach(it => {
      const net = Math.round(it.quantity * it.rate * 100) / 100;
      const gst = Math.round(net * (it.gst_percent / 100.0) * 100) / 100;
      const total = Math.round((net + gst) * 100) / 100;

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

      erpData.stock_ledger.unshift({
        date: payload.invoice_date,
        item_code: it.item_code,
        item_name: it.item_name,
        transaction_type: "IN (Purchase)",
        quantity: it.quantity,
        voucher_no: payload.invoice_no
      });
    });

    // Register into invoices dictionary for commercial printing
    erpData.invoices[payload.invoice_no] = {
      type: "PURCHASE",
      invoice_no: payload.invoice_no,
      invoice_date: payload.invoice_date,
      vendor_id: "VEND001",
      items: payload.items.map(it => ({
        name: it.item_name,
        desc: `Item code ${it.item_code}`,
        qty: it.quantity,
        price: it.rate,
        tax_percent: it.gst_percent
      }))
    };

    // Re-render UI components across all modules
    renderPurchasesTable(payload.invoice_no);
    renderStockLedger(payload.invoice_no);
    renderMasterItems();
    renderGSTReport();
    renderPnLStatement();

    if (btn) {
      btn.innerHTML = `<i class="fa-solid fa-circle-check"></i> Invoice Saved!`;
      btn.className = "btn btn-success";
      setTimeout(() => {
        btn.innerHTML = originalBtnHtml;
        btn.disabled = false;
      }, 2500);
    }

    const alertBox = document.getElementById("purchase-status-alert");
    const alertContent = document.getElementById("purchase-status-alert-content");
    if (alertBox && alertContent) {
      const grossTotal = payload.items.reduce((acc, i) => acc + (i.quantity * i.rate * (1 + i.gst_percent / 100)), 0);
      alertContent.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.75rem;">
          <i class="fa-solid fa-circle-check" style="font-size: 1.4rem; color: var(--accent-emerald);"></i>
          <div>
            <strong>Purchase invoice saved successfully.</strong><br>
            <span style="font-size: 0.85rem; color: var(--text-secondary);">Invoice '${payload.invoice_no}' with ${payload.items.length} item(s) from ${payload.vendor} recorded &bull; Stock updated &bull; Total: ₹${grossTotal.toFixed(2)}</span>
          </div>
        </div>
      `;
      alertBox.style.display = "flex";
    }
  }

  const btnSubmitPurchase = document.getElementById("btn-submit-purchase");
  if (btnSubmitPurchase) {
    btnSubmitPurchase.addEventListener("click", () => {
      const invNo = document.getElementById("pur-input-no")?.value.trim();
      const invDate = document.getElementById("pur-input-date")?.value.trim() || new Date().toISOString().split("T")[0];
      const vendorSelect = document.getElementById("pur-input-vendor");
      const vendor = vendorSelect ? vendorSelect.value : "KR Agro Supplies";
      const gstin = document.getElementById("pur-input-gstin")?.value.trim() || "33AAAAA0000A1Z5";
      const itc = document.getElementById("pur-input-itc")?.checked ?? true;

      if (!invNo) {
        alert("Please provide an Invoice / Bill Number");
        document.getElementById("pur-input-no")?.focus();
        return;
      }

      if (currentBillItems.length === 0) {
        const itemSelect = document.getElementById("pur-input-item-code");
        const itemCode = itemSelect ? itemSelect.value : "ITM001";
        const selectedItemOpt = itemSelect ? itemSelect.options[itemSelect.selectedIndex] : null;
        const itemName = selectedItemOpt?.getAttribute("data-name") || "Basmati Rice 5kg";
        const qty = parseFloat(document.getElementById("pur-input-qty")?.value) || 0;
        const rate = parseFloat(document.getElementById("pur-input-rate")?.value) || 0;
        const gst = parseFloat(document.getElementById("pur-input-gst")?.value) || 0;

        if (qty > 0 && rate > 0) {
          currentBillItems.push({
            item_code: itemCode,
            item_name: itemName,
            quantity: qty,
            rate: rate,
            gst_percent: gst
          });
        }
      }

      if (currentBillItems.length === 0) {
        alert("Please add at least one line item to this purchase invoice (enter quantity and rate, then click '+ Add to Bill')");
        document.getElementById("pur-input-qty")?.focus();
        return;
      }

      const invoicePayload = {
        invoice_no: invNo,
        invoice_date: invDate,
        vendor: vendor,
        vendor_gstin: gstin,
        itc_eligible: itc,
        items: [...currentBillItems]
      };

      submitPurchaseInvoice(invoicePayload);

      currentBillItems = [];
      renderCurrentBillItems();
      ["pur-input-no", "pur-input-qty", "pur-input-rate"].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = "";
      });
    });
  }

  const btnPurchaseClear = document.getElementById("btn-purchase-clear-form");
  if (btnPurchaseClear) {
    btnPurchaseClear.addEventListener("click", (e) => {
      e.preventDefault();
      currentBillItems = [];
      renderCurrentBillItems();
      ["pur-input-no", "pur-input-qty", "pur-input-rate"].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = "";
      });
      const alertBox = document.getElementById("purchase-status-alert");
      if (alertBox) alertBox.style.display = "none";
    });
  }

  // =========================================================================
  // SUBMIT MASTER PRODUCT (TAB 6)
  // =========================================================================
  async function submitMasterItem(itemPayload) {
    const btn = document.getElementById("btn-submit-master-item");
    const originalBtnHtml = btn ? btn.innerHTML : `<i class="fa-solid fa-check"></i> Save Product`;

    if (btn) {
      btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Saving...`;
      btn.disabled = true;
    }

    try {
      const res = await fetch("/api/items", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(itemPayload)
      });
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        console.warn("API Item Save response:", res.status, errData);
      }
    } catch (e) {
      console.warn("Backend item sync fallback:", e);
    }

    const existingIdx = erpData.items.findIndex(it => it.item_code === itemPayload.item_code);
    if (existingIdx >= 0) {
      erpData.items[existingIdx] = { ...erpData.items[existingIdx], ...itemPayload };
    } else {
      erpData.items.unshift(itemPayload);
    }

    if (itemPayload.opening_stock && itemPayload.opening_stock > 0) {
      erpData.stock_ledger.unshift({
        date: new Date().toISOString().split("T")[0],
        item_code: itemPayload.item_code,
        item_name: itemPayload.name,
        transaction_type: "IN (Opening Stock)",
        quantity: itemPayload.opening_stock,
        voucher_no: `OP-${itemPayload.item_code}`
      });
      renderStockLedger();
    }

    renderMasterItems(itemPayload.item_code);
    updatePurchaseItemDropdown();
    refreshInventoryItemDropdown();
    refreshBrandDropdown();

    if (btn) {
      btn.innerHTML = `<i class="fa-solid fa-circle-check"></i> Product Saved!`;
      btn.className = "btn btn-success";
      setTimeout(() => {
        btn.innerHTML = originalBtnHtml;
        btn.disabled = false;
      }, 2500);
    }

    const alertBox = document.getElementById("master-item-status-alert");
    const alertContent = document.getElementById("master-item-status-alert-content");
    if (alertBox && alertContent) {
      alertContent.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.75rem;">
          <i class="fa-solid fa-circle-check" style="font-size: 1.4rem; color: var(--accent-emerald);"></i>
          <div>
            <strong>Product saved successfully.</strong><br>
            <span style="font-size: 0.85rem; color: var(--text-secondary);">'${itemPayload.name}' (${itemPayload.item_code}) registered &bull; Price: ₹${parseFloat(itemPayload.price).toFixed(2)} &bull; Stock: ${itemPayload.opening_stock || 0} Units</span>
          </div>
        </div>
      `;
      alertBox.style.display = "flex";
    }
  }

  const btnSubmitMasterItem = document.getElementById("btn-submit-master-item");
  if (btnSubmitMasterItem) {
    btnSubmitMasterItem.addEventListener("click", () => {
      const code = document.getElementById("master-input-code")?.value.trim();
      const name = document.getElementById("master-input-name")?.value.trim();
      const brand = document.getElementById("master-input-brand")?.value.trim() || "General";
      const category = document.getElementById("master-input-category")?.value.trim() || "General";
      const priceVal = document.getElementById("master-input-price")?.value;
      const price = priceVal !== "" ? parseFloat(priceVal) : 0;
      const costVal = document.getElementById("master-input-cost")?.value;
      const cost = costVal !== "" ? parseFloat(costVal) : Math.round(price * 0.75 * 100) / 100;
      const gst = parseFloat(document.getElementById("master-input-gst")?.value) || 5;
      const opening = parseFloat(document.getElementById("master-input-opening")?.value) || 0;
      const alertQty = parseFloat(document.getElementById("master-input-alert")?.value) || 10;
      const barcode = document.getElementById("master-input-barcode")?.value.trim() || "";

      if (!code) {
        alert("Please enter Item Code (e.g. ITM007)");
        document.getElementById("master-input-code")?.focus();
        return;
      }
      if (!name) {
        alert("Please enter Item Name (e.g. Himalayan Rock Salt 1kg)");
        document.getElementById("master-input-name")?.focus();
        return;
      }
      if (price <= 0) {
        alert("Please enter a valid Retail Price greater than 0");
        document.getElementById("master-input-price")?.focus();
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

  const btnMasterItemClear = document.getElementById("btn-master-item-clear");
  if (btnMasterItemClear) {
    btnMasterItemClear.addEventListener("click", (e) => {
      e.preventDefault();
      [
        "master-input-code",
        "master-input-name",
        "master-input-brand",
        "master-input-category",
        "master-input-price",
        "master-input-cost",
        "master-input-opening",
        "master-input-alert",
        "master-input-barcode"
      ].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = "";
      });
      const alertBox = document.getElementById("master-item-status-alert");
      if (alertBox) alertBox.style.display = "none";
    });
  }

  function updatePurchaseItemDropdown() {
    const itemDrop = document.getElementById("pur-input-item-code");
    if (!itemDrop) return;
    const currentVal = itemDrop.value;
    itemDrop.innerHTML = erpData.items.map(it => {
      const rate = it.cost_price || (it.price * 0.75);
      return `<option value="${it.item_code}" data-name="${it.name}" data-rate="${rate}" data-gst="${it.gst_percent}">${it.item_code} - ${it.name}</option>`;
    }).join("");
    if (currentVal && erpData.items.some(i => i.item_code === currentVal)) {
      itemDrop.value = currentVal;
    }
    syncSelectedItemDefaults();
  }

  // Load backend catalog
  async function loadBackendCatalog() {
    try {
      const res = await fetch("/api/items");
      if (res.ok) {
        const items = await res.json();
        if (Array.isArray(items) && items.length > 0) {
          const codes = new Set(erpData.items.map(i => i.item_code));
          items.forEach(it => {
            if (!codes.has(it.item_code)) {
              erpData.items.push(it);
              codes.add(it.item_code);
            }
          });
          renderMasterItems();
          updatePurchaseItemDropdown();
          refreshInventoryItemDropdown();
          refreshBrandDropdown();
        }
      }
    } catch (e) {
      console.log("Local items catalog loaded.");
    }
  }

  // Load backend purchases
  async function loadBackendPurchases() {
    try {
      const res = await fetch("/api/purchases");
      if (res.ok) {
        const invoices = await res.json();
        if (Array.isArray(invoices) && invoices.length > 0) {
          const loadedRows = [];
          invoices.forEach(inv => {
            if (Array.isArray(inv.items)) {
              inv.items.forEach(it => {
                const net = it.net_amount || Math.round(it.quantity * it.rate * 100) / 100;
                const gst = it.gst_amount || Math.round(net * (it.gst_percent / 100.0) * 100) / 100;
                const total = it.total_amount || Math.round((net + gst) * 100) / 100;
                loadedRows.push({
                  invoice_no: inv.invoice_no,
                  invoice_date: inv.invoice_date,
                  vendor: inv.vendor,
                  item_code: it.item_code,
                  item_name: it.item_name,
                  quantity: it.quantity,
                  rate: it.rate,
                  net_amount: net,
                  gst_percent: it.gst_percent,
                  gst_amount: gst,
                  total_amount: total
                });
              });
            }
          });
          if (loadedRows.length > 0) {
            erpData.purchases = loadedRows;
            renderPurchasesTable();
            renderGSTReport();
          }
        }
      }
    } catch (e) {
      console.log("Local purchases loaded.");
    }
  }


  // =========================================================================
  // MASTER ERP ENHANCEMENT 1: REAL-TIME ANALYTICS & PURE SVG CHARTS
  // =========================================================================

  async function fetchAndRenderDashboardAnalytics() {
    try {
      const resp = await fetch("/api/analytics/dashboard");
      if (!resp.ok) return;
      const data = await resp.json();
      renderSalesTrendSvg(data.sales_trend_7d || []);
      renderCategoryDonutSvg(data.category_breakdown || []);
      renderStockHealthGaugeSvg(data.stock_health || {});
    } catch (e) {
      console.warn("Analytics fetch error:", e);
    }
  }

  function renderSalesTrendSvg(trendData) {
    const container = document.getElementById("svg-sales-trend-container");
    if (!container) return;
    if (!trendData || trendData.length === 0) {
      container.innerHTML = '<div style="color:#64748b; font-size:0.8rem; text-align:center; padding-top:60px;">No sales history recorded</div>';
      return;
    }
    const totalRev = trendData.reduce((acc, d) => acc + (d.revenue || 0), 0);
    const totalEl = document.getElementById("chart-trend-total");
    if (totalEl) totalEl.textContent = `₹${totalRev.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;

    const width = 340;
    const height = 150;
    const padX = 35;
    const padY = 25;
    const maxVal = Math.max(...trendData.map(d => d.revenue), 100);

    const barW = Math.max(12, Math.floor((width - padX * 2) / trendData.length) - 8);

    let barsSvg = "";
    trendData.forEach((d, i) => {
      const x = padX + i * Math.floor((width - padX * 2) / trendData.length) + 4;
      const barH = Math.max(4, Math.round((d.revenue / maxVal) * (height - padY * 2)));
      const y = height - padY - barH;
      const dateLabel = (d.date || "").slice(5);
      const formattedRev = d.revenue >= 1000 ? `₹${(d.revenue/1000).toFixed(1)}k` : `₹${Math.round(d.revenue)}`;

      barsSvg += `
        <g class="svg-bar-group" style="cursor: pointer;">
          <title>${d.date}: ₹${d.revenue.toLocaleString('en-IN')} (${d.invoices || 1} inv)</title>
          <rect x="${x}" y="${y}" width="${barW}" height="${barH}" rx="3" fill="#38bdf8" fill-opacity="0.85" />
          <text x="${x + barW/2}" y="${y - 4}" text-anchor="middle" fill="#94a3b8" font-size="9" font-weight="600">${formattedRev}</text>
          <text x="${x + barW/2}" y="${height - 8}" text-anchor="middle" fill="#64748b" font-size="9">${dateLabel}</text>
        </g>
      `;
    });

    container.innerHTML = `
      <svg viewBox="0 0 ${width} ${height}" style="width: 100%; height: 100%; overflow: visible;">
        <line x1="${padX - 5}" y1="${height - padY}" x2="${width - 10}" y2="${height - padY}" stroke="#334155" stroke-width="1" />
        ${barsSvg}
      </svg>
    `;
  }

  function renderCategoryDonutSvg(categories) {
    const container = document.getElementById("svg-category-donut-container");
    if (!container) return;
    if (!categories || categories.length === 0) {
      container.innerHTML = '<div style="color:#64748b; font-size:0.8rem; text-align:center;">No category data</div>';
      return;
    }
    const colors = ["#10b981", "#3b82f6", "#8b5cf6", "#f59e0b", "#ec4899", "#06b6d4"];
    const totalRev = categories.reduce((acc, c) => acc + (c.revenue || 0), 0);
    const catCountEl = document.getElementById("chart-cat-count");
    if (catCountEl) catCountEl.textContent = `${categories.length} Categories`;

    let topCats = categories.slice(0, 4);
    if (categories.length > 4) {
      const otherRev = categories.slice(4).reduce((acc, c) => acc + c.revenue, 0);
      topCats.push({ category: "Other", revenue: otherRev });
    }

    const cx = 75, cy = 75, r = 50, strokeW = 20;
    const circ = 2 * Math.PI * r;
    let currentOffset = 0;
    let pathsSvg = "";

    topCats.forEach((c, idx) => {
      const share = totalRev > 0 ? (c.revenue / totalRev) : 0;
      const dash = share * circ;
      const col = colors[idx % colors.length];
      pathsSvg += `
        <circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="${col}" stroke-width="${strokeW}"
          stroke-dasharray="${dash} ${circ - dash}" stroke-dashoffset="${-currentOffset}"
          transform="rotate(-90 ${cx} ${cy})">
          <title>${c.category}: ₹${c.revenue.toLocaleString('en-IN')} (${(share*100).toFixed(1)}%)</title>
        </circle>
      `;
      currentOffset += dash;
    });

    let legendHtml = '<div style="display: flex; flex-direction: column; gap: 0.35rem; font-size: 0.75rem;">';
    topCats.forEach((c, idx) => {
      const share = totalRev > 0 ? Math.round((c.revenue / totalRev) * 100) : 0;
      const col = colors[idx % colors.length];
      legendHtml += `
        <div style="display: flex; align-items: center; gap: 0.4rem;">
          <span style="width: 8px; height: 8px; border-radius: 50%; background: ${col}; flex-shrink: 0;"></span>
          <span style="color: #cbd5e1; max-width: 90px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${c.category}</span>
          <strong style="color: #fff; margin-left: auto;">${share}%</strong>
        </div>
      `;
    });
    legendHtml += '</div>';

    container.innerHTML = `
      <svg width="150" height="150" viewBox="0 0 150 150" style="flex-shrink: 0;">
        <circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="#1e293b" stroke-width="${strokeW}" />
        ${pathsSvg}
        <text x="${cx}" y="${cy + 4}" text-anchor="middle" fill="#fff" font-size="12" font-weight="700">₹${totalRev >= 1000 ? (totalRev/1000).toFixed(0) + 'k' : totalRev}</text>
      </svg>
      ${legendHtml}
    `;
  }

  function renderStockHealthGaugeSvg(health) {
    const container = document.getElementById("svg-stock-gauge-container");
    if (!container) return;
    const total = health.total_skus || 1;
    const inStock = health.in_stock || 0;
    const lowStock = health.low_stock || 0;
    const outStock = health.out_of_stock || 0;
    const ratio = Math.round((inStock / total) * 100);

    const gaugeColor = ratio >= 80 ? "#10b981" : (ratio >= 50 ? "#f59e0b" : "#ef4444");

    container.innerHTML = `
      <div style="text-align: center; margin-bottom: 0.5rem;">
        <div style="font-size: 1.8rem; font-weight: 800; color: ${gaugeColor}; line-height: 1;">
          ${ratio}%
        </div>
        <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 0.2rem;">
          Active Stock Health Index
        </div>
      </div>
      <div style="width: 80%; background: #334155; height: 8px; border-radius: 4px; overflow: hidden; margin-bottom: 0.75rem; display: flex;">
        <div style="width: ${ratio}%; background: #10b981;" title="In-Stock: ${inStock}"></div>
        <div style="width: ${Math.round((lowStock / total) * 100)}%; background: #f59e0b;" title="Low-Stock: ${lowStock}"></div>
        <div style="width: ${Math.round((outStock / total) * 100)}%; background: #ef4444;" title="Out of Stock: ${outStock}"></div>
      </div>
      <div style="display: flex; justify-content: space-between; width: 90%; font-size: 0.72rem; color: #94a3b8;">
        <span><span style="color: #10b981; font-weight: 700;">●</span> ${inStock} Healthy</span>
        <span><span style="color: #f59e0b; font-weight: 700;">●</span> ${lowStock} Low</span>
        <span><span style="color: #ef4444; font-weight: 700;">●</span> ${outStock} Empty</span>
      </div>
    `;
  }

  // Toggle Charts display button
  const btnToggleCharts = document.getElementById("btn-toggle-charts");
  if (btnToggleCharts) {
    btnToggleCharts.addEventListener("click", () => {
      const wrapper = document.getElementById("charts-wrapper");
      if (wrapper) {
        if (wrapper.style.display === "none") {
          wrapper.style.display = "grid";
          btnToggleCharts.innerHTML = '<i class="fa-solid fa-compress"></i> Hide Charts';
        } else {
          wrapper.style.display = "none";
          btnToggleCharts.innerHTML = '<i class="fa-solid fa-chart-simple"></i> Show Charts';
        }
      }
    });
  }

  // =========================================================================
  // MASTER ERP ENHANCEMENT 2: SMART AUTO-PO RESTOCK WORKFLOW
  // =========================================================================

  function initAutoPoRestock() {
    const btnAutoPO = document.getElementById("btn-auto-restock-po");
    const btnQuickPO = document.getElementById("btn-quick-auto-po");

    const handleAutoPo = async () => {
      try {
        const resp = await fetch("/api/stock/auto-reorder-draft");
        if (!resp.ok) throw new Error("Server error fetching restock draft");
        const draft = await resp.json();

        if (!draft.items || draft.items.length === 0) {
          alert("All warehouse items have healthy stock levels. No reorder required!");
          return;
        }

        // Switch tab to Purchases
        window.location.hash = "#purchases";
        handleHashRoute();

        // Select suggested vendor
        const purVendorInput = document.getElementById("pur-input-vendor");
        if (purVendorInput && draft.suggested_vendor) {
          let found = false;
          for (let opt of purVendorInput.options) {
            if (opt.value.toLowerCase() === draft.suggested_vendor.toLowerCase()) {
              purVendorInput.value = opt.value;
              found = true;
              break;
            }
          }
          if (!found) {
            const opt = new Option(draft.suggested_vendor, draft.suggested_vendor, true, true);
            purVendorInput.add(opt);
          }
        }

        // Populate currentBillItems with draft
        currentBillItems = draft.items.map(it => {
          const qty = it.suggested_quantity || 10;
          const rate = it.rate || 100;
          const gstPct = it.gst_percent || 5.0;
          const net = Math.round(qty * rate * 100) / 100;
          const gst = Math.round(net * (gstPct / 100.0) * 100) / 100;
          const total = Math.round((net + gst) * 100) / 100;
          return {
            item_code: it.item_code,
            item_name: it.item_name,
            item_description: it.item_description,
            quantity: qty,
            rate: rate,
            net_amount: net,
            gst_percent: gstPct,
            gst_amount: gst,
            total_amount: total
          };
        });

        renderBillItemsTable();
        calculatePurchaseTotals();

        const alertBox = document.getElementById("purchase-status-alert");
        const alertContent = document.getElementById("purchase-status-alert-content");
        if (alertBox && alertContent) {
          alertContent.innerHTML = `<strong>⚡ Smart Auto-Restock Order Generated:</strong> Prepared ${draft.items.length} low-stock SKUs from supplier <em>${draft.suggested_vendor}</em> (Est. Cost: ₹${draft.total_estimated_cost.toLocaleString('en-IN')}). Review and click 'Save Purchase Invoice'.`;
          alertBox.style.display = "flex";
        }
      } catch (err) {
        console.error("Auto PO error:", err);
        alert("Failed to auto-generate purchase order: " + err.message);
      }
    };

    if (btnAutoPO) btnAutoPO.addEventListener("click", handleAutoPo);
    if (btnQuickPO) btnQuickPO.addEventListener("click", handleAutoPo);
  }

  // =========================================================================
  // MASTER ERP ENHANCEMENT 3: RAPID BARCODE SCANNER LISTENER & AUDIO BEEP
  // =========================================================================

  function playScannerAudioBeep(isSuccess = true) {
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;
      const ctx = new AudioCtx();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);

      if (isSuccess) {
        osc.type = "sine";
        osc.frequency.setValueAtTime(1200, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(1800, ctx.currentTime + 0.08);
        gain.gain.setValueAtTime(0.15, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.08);
        osc.start(ctx.currentTime);
        osc.stop(ctx.currentTime + 0.08);
      } else {
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(300, ctx.currentTime);
        gain.gain.setValueAtTime(0.2, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.15);
        osc.start(ctx.currentTime);
        osc.stop(ctx.currentTime + 0.15);
      }
    } catch (e) {
      // Audio autoplay policy
    }
  }

  function initBarcodeScanner() {
    let barcodeBuffer = "";
    let lastKeyTime = 0;

    document.addEventListener("keydown", async (e) => {
      const targetTag = (e.target.tagName || "").toLowerCase();
      // Allow barcode scanning even if not focused, or inside barcode input
      const now = Date.now();
      const diff = now - lastKeyTime;
      lastKeyTime = now;

      // Scanners emit characters rapidly (< 70ms)
      if (diff > 90) {
        barcodeBuffer = "";
      }

      if (e.key === "Enter") {
        if (barcodeBuffer.length >= 3) {
          e.preventDefault();
          const code = barcodeBuffer.trim();
          barcodeBuffer = "";
          await onBarcodeScanned(code);
        }
      } else if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {
        barcodeBuffer += e.key;
      }
    });

    async function onBarcodeScanned(code) {
      try {
        const resp = await fetch(`/api/items?search=${encodeURIComponent(code)}`);
        if (!resp.ok) return;
        const items = await resp.json();
        if (items && items.length > 0) {
          const item = items[0];
          playScannerAudioBeep(true);

          const pill = document.getElementById("barcode-scanner-pill");
          if (pill) {
            pill.innerHTML = `<i class="fa-solid fa-check"></i> Scanned: ${item.name} (${item.item_code})`;
            pill.style.background = "rgba(16, 185, 129, 0.4)";
            setTimeout(() => {
              pill.innerHTML = `<i class="fa-solid fa-barcode"></i> Barcode Scanner: Ready`;
              pill.style.background = "rgba(16, 185, 129, 0.15)";
            }, 3500);
          }

          // If on Items tab, search and highlight
          const itemsSearch = document.getElementById("items-filter-search");
          if (itemsSearch) {
            itemsSearch.value = item.item_code;
            itemsSearch.dispatchEvent(new Event("input"));
          }
          // If on Purchase bill tab, select item in dropdown
          const purItemSelect = document.getElementById("pur-input-item");
          if (purItemSelect) {
            purItemSelect.value = item.item_code;
            purItemSelect.dispatchEvent(new Event("change"));
          }
        } else {
          playScannerAudioBeep(false);
        }
      } catch (err) {
        console.error("Barcode scan lookup error:", err);
      }
    }
  }

  // =========================================================================
  // MASTER ERP ENHANCEMENT 4: CUSTOMER CREDIT & KHATA LEDGER MODAL
  // =========================================================================

  function initCustomerLedgerModal() {
    const modal = document.getElementById("modal-customer-ledger");
    const btnOpen = document.getElementById("btn-open-customer-ledger");
    const btnClose1 = document.getElementById("btn-close-cust-modal");
    const btnClose2 = document.getElementById("btn-modal-cust-done");
    const custSelect = document.getElementById("modal-cust-select");

    const statsBox = document.getElementById("modal-cust-stats");
    const payBox = document.getElementById("modal-cust-pay-box");
    const duesEl = document.getElementById("modal-cust-dues");
    const limitEl = document.getElementById("modal-cust-limit");
    const availEl = document.getElementById("modal-cust-avail");
    const tbody = document.getElementById("modal-cust-ledger-tbody");

    const btnSubmitPay = document.getElementById("btn-submit-cust-pay");
    const payAmountInput = document.getElementById("modal-cust-pay-amount");
    const payModeSelect = document.getElementById("modal-cust-pay-mode");
    const payRefInput = document.getElementById("modal-cust-pay-ref");
    const payMsg = document.getElementById("modal-cust-pay-msg");

    const closeModal = () => { if (modal) modal.style.display = "none"; };

    if (btnOpen) {
      btnOpen.addEventListener("click", async () => {
        if (modal) modal.style.display = "flex";
        // Load customers into dropdown
        try {
          const resp = await fetch("/api/customers");
          if (!resp.ok) return;
          const customers = await resp.json();
          if (custSelect) {
            custSelect.innerHTML = '<option value="">-- Choose Customer Account --</option>';
            customers.forEach(c => {
              const cid = c.customer_id || c._id;
              const dues = c.outstanding_dues || 0;
              const opt = document.createElement("option");
              opt.value = cid;
              opt.textContent = `${c.name} (${c.city || 'TN'}) - Dues: ₹${dues.toFixed(2)}`;
              custSelect.appendChild(opt);
            });
          }
        } catch (e) {
          console.error("Failed to load customer list:", e);
        }
      });
    }

    if (btnClose1) btnClose1.addEventListener("click", closeModal);
    if (btnClose2) btnClose2.addEventListener("click", closeModal);

    async function loadCustomerLedger(customerId) {
      if (!customerId) {
        if (statsBox) statsBox.style.display = "none";
        if (payBox) payBox.style.display = "none";
        if (tbody) tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 1rem; color: #64748b;">Select a customer to view ledger</td></tr>';
        return;
      }
      try {
        const resp = await fetch(`/api/customers/${encodeURIComponent(customerId)}/ledger`);
        if (!resp.ok) return;
        const ledger = await resp.json();

        if (statsBox) statsBox.style.display = "grid";
        if (payBox) payBox.style.display = "block";

        if (duesEl) duesEl.textContent = `₹${(ledger.outstanding_dues || 0).toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
        if (limitEl) limitEl.textContent = `₹${(ledger.credit_limit || 10000).toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
        if (availEl) availEl.textContent = `₹${(ledger.available_credit || 0).toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;

        if (tbody) {
          const txs = ledger.transactions || [];
          if (txs.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 1rem; color: #64748b;">No transaction history found for this customer</td></tr>';
          } else {
            tbody.innerHTML = txs.map(t => {
              const isSale = t.type === "SALE_INVOICE";
              return `
                <tr style="border-bottom: 1px solid #334155;">
                  <td style="padding: 0.5rem; color: #cbd5e1;">${t.date || ''}</td>
                  <td style="padding: 0.5rem;"><span class="badge ${isSale ? 'badge-warning' : 'badge-success'}" style="font-size:0.7rem;">${isSale ? 'SALE' : 'PAYMENT'}</span></td>
                  <td style="padding: 0.5rem; color: #fff;"><code>${t.ref_no || ''}</code></td>
                  <td style="padding: 0.5rem; text-align: right; color: ${t.debit > 0 ? '#f87171' : '#64748b'};">${t.debit > 0 ? '₹' + t.debit.toFixed(2) : '-'}</td>
                  <td style="padding: 0.5rem; text-align: right; color: ${t.credit > 0 ? '#34d399' : '#64748b'};">${t.credit > 0 ? '₹' + t.credit.toFixed(2) : '-'}</td>
                </tr>
              `;
            }).join("");
          }
        }
      } catch (err) {
        console.error("Ledger load error:", err);
      }
    }

    if (custSelect) {
      custSelect.addEventListener("change", (e) => {
        loadCustomerLedger(e.target.value);
      });
    }

    if (btnSubmitPay) {
      btnSubmitPay.addEventListener("click", async () => {
        const cid = custSelect ? custSelect.value : "";
        if (!cid) {
          alert("Please select a customer first.");
          return;
        }
        const amt = parseFloat(payAmountInput ? payAmountInput.value : 0);
        if (isNaN(amt) || amt <= 0) {
          alert("Please enter a valid payment amount greater than zero.");
          return;
        }
        const mode = payModeSelect ? payModeSelect.value : "CASH";
        const ref = payRefInput ? payRefInput.value : "";

        try {
          const resp = await fetch(`/api/customers/${encodeURIComponent(cid)}/payment`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ amount: amt, payment_mode: mode, reference_no: ref })
          });
          if (!resp.ok) throw new Error("Payment recording failed");
          const result = await resp.json();

          if (payMsg) {
            payMsg.style.display = "block";
            payMsg.style.color = "#34d399";
            payMsg.innerHTML = `<i class="fa-solid fa-circle-check"></i> ${result.message}`;
            setTimeout(() => { payMsg.style.display = "none"; }, 4000);
          }
          if (payAmountInput) payAmountInput.value = "";
          if (payRefInput) payRefInput.value = "";

          // Reload ledger and refresh sales table
          loadCustomerLedger(cid);
          renderSalesTable();
        } catch (err) {
          alert("Payment failed: " + err.message);
        }
      });
    }
  }

  // =========================================================================
  // MASTER ERP ENHANCEMENT 5: VENDOR BILL PAYMENT MODAL
  // =========================================================================

  function initVendorPaymentModal() {
    const modal = document.getElementById("modal-vendor-payment");
    const btnClose1 = document.getElementById("btn-close-vendor-modal");
    const btnClose2 = document.getElementById("btn-close-vendor-modal-2");
    const btnSubmit = document.getElementById("btn-submit-vendor-payment");

    const billNoEl = document.getElementById("vpay-bill-no");
    const vendorNameEl = document.getElementById("vpay-vendor-name");
    const totalAmtEl = document.getElementById("vpay-total-amt");
    const balanceDueEl = document.getElementById("vpay-balance-due");
    const amtInput = document.getElementById("vpay-input-amount");
    const modeSelect = document.getElementById("vpay-input-mode");
    const refInput = document.getElementById("vpay-input-ref");
    const statusMsg = document.getElementById("vpay-status-msg");

    let currentInvNo = "";

    window.openVendorPaymentModal = function(invoiceNo, vendor, totalAmt, balanceDue) {
      currentInvNo = invoiceNo;
      if (billNoEl) billNoEl.textContent = invoiceNo;
      if (vendorNameEl) vendorNameEl.textContent = vendor;
      if (totalAmtEl) totalAmtEl.textContent = `₹${parseFloat(totalAmt).toFixed(2)}`;
      if (balanceDueEl) balanceDueEl.textContent = `₹${parseFloat(balanceDue).toFixed(2)}`;
      if (amtInput) amtInput.value = parseFloat(balanceDue).toFixed(2);
      if (refInput) refInput.value = "";
      if (statusMsg) statusMsg.style.display = "none";
      if (modal) modal.style.display = "flex";
    };

    const closeModal = () => { if (modal) modal.style.display = "none"; };
    if (btnClose1) btnClose1.addEventListener("click", closeModal);
    if (btnClose2) btnClose2.addEventListener("click", closeModal);

    if (btnSubmit) {
      btnSubmit.addEventListener("click", async () => {
        if (!currentInvNo) return;
        const amt = parseFloat(amtInput ? amtInput.value : 0);
        if (isNaN(amt) || amt <= 0) {
          alert("Please enter a valid payment amount greater than zero.");
          return;
        }
        const mode = modeSelect ? modeSelect.value : "NEFT";
        const ref = refInput ? refInput.value : "";

        try {
          const resp = await fetch(`/api/purchases/${encodeURIComponent(currentInvNo)}/payment`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ amount: amt, payment_mode: mode, reference_no: ref })
          });
          if (!resp.ok) throw new Error("Payment record failed");
          const result = await resp.json();

          // Update local memory purchase invoice record
          erpData.purchases.forEach(p => {
            if (p.invoice_no === currentInvNo) {
              p.amount_paid = result.amount_paid;
              p.payment_status = result.payment_status;
              p.balance_due = result.balance_due;
            }
          });

          renderPurchasesTable();
          fetchAndRenderDashboardAnalytics();
          closeModal();
          alert(`Success: Payment of ₹${amt.toFixed(2)} recorded for bill ${currentInvNo}. Status: ${result.payment_status}`);
        } catch (err) {
          alert("Payment error: " + err.message);
        }
      });
    }
  }

  // Initial Initialization & Renders
  updatePurchaseItemDropdown();
  refreshInventoryItemDropdown();
  refreshBrandDropdown();

  renderMasterItems();
  renderPurchasesTable();
  renderSalesTable();
  renderStockLedger();
  renderGSTReport();
  renderPnLStatement();

  loadBackendCatalog();
  loadBackendPurchases();

  // Master ERP Enhancements Initializers
  fetchAndRenderDashboardAnalytics();
  initAutoPoRestock();
  initBarcodeScanner();
  initCustomerLedgerModal();
  initVendorPaymentModal();

  handleHashRoute();
});
