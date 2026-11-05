# Jompoi ERP - Android Mobile Application (APK)

This folder contains the compiled, verified, and production-ready Android application package (APK) for the **Jompoi Supermarket ERP System**.

---

## 📱 Quick Download Links

- **Direct Raw APK Download (GitHub):**  
  [https://github.com/theju1703/Jumpoi/raw/main/apk/app-debug.apk](https://github.com/theju1703/Jumpoi/raw/main/apk/app-debug.apk)

- **Repository File Location:**  
  `apk/app-debug.apk` (Size: ~12.2 MB)

---

## 🚀 Installation & Testing Instructions

### Option 1: Sideload onto Physical Android Device (Phone / Tablet)
1. Download `app-debug.apk` directly to your Android device using Chrome or file transfer.
2. If prompted, tap **Settings** and allow **"Install unknown apps"** for your browser or file manager.
3. Tap **Install** and open **Jompoi ERP**.
4. The application opens directly to the authentication screen with pre-configured 1-tap demo roles or manual login.

### Option 2: Run via Android Studio Emulator
1. Start an Android Virtual Device (AVD) from Android Studio Device Manager.
2. In your terminal, run:
   ```bash
   adb install -r apk/app-debug.apk
   ```
3. Alternatively, drag and drop `apk/app-debug.apk` directly onto the running emulator window.
4. Launch **Jompoi ERP** from the emulator app drawer.

---

## 🔑 Pre-Configured Test Accounts (RBAC)

The app includes 1-tap quick login buttons for all supermarket roles:

| Role | Username | Password | Access Capabilities |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | Full ERP configuration, user registration, item deletion, inventory adjustments |
| **Store Manager** | `manager` | `manager123` | Master item pricing, supplier purchases, stock audit, executive reports |
| **POS Cashier** | `cashier` | `cashier123` | POS billing, barcode scanning, cart calculation, commercial invoice printing, refunds |
| **Inventory Staff** | `inventory` | `inventory123` | Real-time stock audit, warehouse inwards, goods receiving |

---

## 🌐 Backend Network Configuration

The Android application is configured with cleartext HTTP support (`usesCleartextTraffic="true"`) to connect to the ERP Backend API:
- **Android Emulator Default:** `http://10.0.2.2:8080` (Automatically routes to `localhost:8080` on host PC).
- **Physical Device on Wi-Fi:** Enter your host machine's local LAN IP (e.g., `http://192.168.1.100:8080`) in the app settings or login screen.
- **Offline Fallback Mode:** If the backend is temporarily unreachable, the app automatically enables the built-in offline demonstration data engine so all screens (Dashboard, POS, Invoices, Stock) can be tested seamlessly without crashes.

---

## 🛠 Features & Verification Matrix

- ✅ **Authentication:** JWT Bearer token management with auto-refresh and role enforcement.
- ✅ **POS Billing:** Live barcode search, item lookup, custom pricing, discount calculation.
- ✅ **Invoice Printing:** Commercial Tax Invoice with exact formula $\text{Total} = (\text{Price} + \text{Tax}) \times \text{Quantity}$ and printable table view.
- ✅ **Real-Time Stock:** Live balance on hand ($\sum \text{IN} - \sum \text{OUT}$), reorder alert badges, valuation.
- ✅ **Purchases:** Inward supplier bills with per-item GST rates (0%, 5%, 12%, 18%) and Input Tax Credit (ITC) tracking.
- ✅ **Reports:** GST Reconciliation (GSTR-1 vs GSTR-2B) and Profit & Loss financial statements.
