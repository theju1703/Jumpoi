# Python script to apply enterprise Master ERP enhancements to app.js and web/app.js

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update erpState.purchases.filters with payment_status
target1 = 'purchases: {\n      filters: { search: "", vendor: "ALL",'
replacement1 = 'purchases: {\n      filters: { search: "", vendor: "ALL", payment_status: "ALL",'
if target1 in js:
    js = js.replace(target1, replacement1, 1)
    print("[OK] erpState.purchases.filters updated")
else:
    print("[WARN] target1 not found")

# 2. Update getFilteredPurchases with payment_status check
target2 = 'if (f.vendor !== "ALL" && p.vendor !== f.vendor) return false;'
replacement2 = '''if (f.vendor !== "ALL" && p.vendor !== f.vendor) return false;
      if (f.payment_status && f.payment_status !== "ALL" && (p.payment_status || "UNPAID").toUpperCase() !== f.payment_status.toUpperCase()) return false;'''
if target2 in js:
    js = js.replace(target2, replacement2, 1)
    print("[OK] getFilteredPurchases updated")
else:
    print("[WARN] target2 not found")

# 3. Update active filter count for purchases
target3 = 'if (f.vendor !== "ALL") activeCount++;'
replacement3 = '''if (f.vendor !== "ALL") activeCount++;
    if (f.payment_status && f.payment_status !== "ALL") activeCount++;'''
if target3 in js:
    js = js.replace(target3, replacement3, 1)
    print("[OK] activeCount purchases updated")
else:
    print("[WARN] target3 not found")

# 4. Update table purchases row rendering
old_pur_row = '''          return `
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
              <td style="text-align: center;">
                <button class="btn btn-secondary" style="padding:0.3rem 0.6rem; font-size:0.75rem;" onclick="printPurchaseBill('${p.invoice_no}')">
                  <i class="fa-solid fa-print"></i> Print Bill
                </button>
              </td>
            </tr>
          `;'''

new_pur_row = '''          const payStatus = (p.payment_status || "UNPAID").toUpperCase();
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
                    onclick="window.openVendorPaymentModal('${p.invoice_no}', '${(p.vendor||'').replace(/'/g, "\\\\'")}', ${parseFloat(p.total_amount||0)}, ${balanceDue})" title="Pay Vendor Bill">
                    <i class="fa-solid fa-money-bill-wave"></i> Pay
                  </button>
                ` : ''}
              </td>
            </tr>
          `;'''

if old_pur_row in js:
    js = js.replace(old_pur_row, new_pur_row, 1)
    print("[OK] renderPurchasesTable row updated")
else:
    print("[WARN] old_pur_row not found")

# Update colspan if no records found
js = js.replace('<td colspan="12" style="text-align:center; padding:2rem; color:#94a3b8;">', '<td colspan="13" style="text-align:center; padding:2rem; color:#94a3b8;">')

# 5. Purchases Filter Listeners (payment status dropdown)
old_pur_listeners = '''  const purMaxTotal = document.getElementById("purchases-filter-max-total");
  const purPageSize = document.getElementById("purchases-page-size");
  const btnResetPur = document.getElementById("btn-reset-purchases-filters");'''

new_pur_listeners = '''  const purMaxTotal = document.getElementById("purchases-filter-max-total");
  const purPaymentStatus = document.getElementById("purchases-filter-payment-status");
  const purPageSize = document.getElementById("purchases-page-size");
  const btnResetPur = document.getElementById("btn-reset-purchases-filters");

  if (purPaymentStatus) {
    purPaymentStatus.addEventListener("change", (e) => {
      erpState.purchases.filters.payment_status = e.target.value;
      erpState.purchases.page = 1;
      renderPurchasesTable();
    });
  }'''

if old_pur_listeners in js:
    js = js.replace(old_pur_listeners, new_pur_listeners, 1)
    print("[OK] purPaymentStatus listener added")
else:
    print("[WARN] old_pur_listeners not found")

# In reset purchases filters:
old_pur_reset = 'if (purMaxTotal) purMaxTotal.value = "";'
new_pur_reset = '''if (purMaxTotal) purMaxTotal.value = "";
      if (purPaymentStatus) purPaymentStatus.value = "ALL";
      erpState.purchases.filters.payment_status = "ALL";'''
if old_pur_reset in js:
    js = js.replace(old_pur_reset, new_pur_reset, 1)
    print("[OK] reset purchases updated with payment_status")

# 6. Append New Enterprise Feature Modules right before initialization at the bottom
new_enterprise_modules = r'''
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
'''

# 7. Add calls in Initial Initialization & Renders
init_calls = '''  // Initial Initialization & Renders
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
  initVendorPaymentModal();'''

old_init_calls = '''  // Initial Initialization & Renders
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
  loadBackendPurchases();'''

if old_init_calls in js:
    js = js.replace(old_init_calls, new_enterprise_modules + '\n' + init_calls, 1)
    print("[OK] initial calls and new enterprise modules added")
else:
    print("[WARN] old_init_calls not found")

# Write out to app.js and web/app.js
for p in ['app.js', 'web/app.js']:
    with open(p, 'w', encoding='utf-8') as f:
        f.write(js)
    print(f"[OK] written {p} ({len(js)} bytes)")
