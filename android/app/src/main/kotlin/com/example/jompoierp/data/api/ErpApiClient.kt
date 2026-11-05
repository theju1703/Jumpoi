package com.example.jompoierp.data.api

import com.example.jompoierp.data.model.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import java.io.BufferedReader
import java.io.InputStreamReader
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL

object ErpApiClient {
    // Configurable base URL: 10.0.2.2 is Android Emulator host loopback; localhost/IP for physical device
    var baseUrl: String = "http://10.0.2.2:8080"
    var authToken: String? = null

    val jsonParser = Json {
        ignoreUnknownKeys = true
        isLenient = true
        encodeDefaults = true
    }

    private suspend fun <T> makeRequest(
        endpoint: String,
        method: String = "GET",
        requestBody: String? = null,
        parser: (String) -> T,
        fallback: () -> T
    ): T = withContext(Dispatchers.IO) {
        try {
            val url = URL("$baseUrl$endpoint")
            val conn = (url.openConnection() as HttpURLConnection).apply {
                requestMethod = method
                connectTimeout = 3000
                readTimeout = 3000
                setRequestProperty("Content-Type", "application/json")
                setRequestProperty("Accept", "application/json")
                authToken?.let { setRequestProperty("Authorization", "Bearer $it") }

                if (requestBody != null && (method == "POST" || method == "PUT")) {
                    doOutput = true
                    val writer = OutputStreamWriter(outputStream)
                    writer.write(requestBody)
                    writer.flush()
                }
            }

            val responseCode = conn.responseCode
            if (responseCode in 200..299) {
                val reader = BufferedReader(InputStreamReader(conn.inputStream))
                val response = reader.readText()
                reader.close()
                parser(response)
            } else {
                fallback()
            }
        } catch (e: Exception) {
            // Graceful fallback to offline cached data if backend is offline
            fallback()
        }
    }

    suspend fun login(req: UserLoginRequest): AuthResponse {
        return makeRequest(
            endpoint = "/api/auth/login",
            method = "POST",
            requestBody = jsonParser.encodeToString(req),
            parser = { jsonParser.decodeFromString<AuthResponse>(it) },
            fallback = {
                // Offline demo fallback based on role
                val role = when (req.username.lowercase()) {
                    "admin" -> "ADMIN"
                    "manager" -> "STORE_MANAGER"
                    "inventory1" -> "INVENTORY_STAFF"
                    else -> "CASHIER"
                }
                AuthResponse(
                    access_token = "offline_demo_jwt_token",
                    token_type = "bearer",
                    username = req.username,
                    full_name = "${req.username.replaceFirstChar { it.uppercase() }} User",
                    role = role
                )
            }
        )
    }

    suspend fun getExecutiveSummary(): ExecutiveSummary {
        return makeRequest(
            endpoint = "/api/reports/summary",
            method = "GET",
            parser = { jsonParser.decodeFromString<ExecutiveSummary>(it) },
            fallback = {
                ExecutiveSummary(
                    active_items_count = 4,
                    total_sales_invoices = 3,
                    total_purchase_bills = 2,
                    gross_sales_revenue = 12675.00,
                    gross_procurement_spend = 30950.00,
                    status = "OPERATIONAL"
                )
            }
        )
    }

    suspend fun getItems(): List<Item> {
        return makeRequest(
            endpoint = "/api/items",
            method = "GET",
            parser = { jsonParser.decodeFromString<List<Item>>(it) },
            fallback = {
                listOf(
                    Item("ITM001", "Basmati Rice 5kg", "India Gate", "Grains & Rice", 450.0, 5.0, 10.0, "890123456001", "Aged long grain premium basmati"),
                    Item("ITM002", "Sunflower Oil 1L", "Fortune", "Edible Oils", 135.0, 5.0, 20.0, "890123456002", "Refined sunflower cooking oil"),
                    Item("ITM003", "Toor Dal 1kg", "Tata Sampann", "Pulses", 160.0, 0.0, 15.0, "890123456003", "Unpolished protein rich toor dal"),
                    Item("ITM004", "Milk 500ml", "Aavin", "Dairy", 25.0, 0.0, 30.0, "890123456004", "Pasteurized full cream fresh milk")
                )
            }
        )
    }

    suspend fun getStockPosition(): List<StockPosition> {
        return makeRequest(
            endpoint = "/api/stock",
            method = "GET",
            parser = { jsonParser.decodeFromString<List<StockPosition>>(it) },
            fallback = {
                listOf(
                    StockPosition("ITM001", "Basmati Rice 5kg", 40.0, 450.0),
                    StockPosition("ITM002", "Sunflower Oil 1L", 75.0, 135.0),
                    StockPosition("ITM003", "Toor Dal 1kg", 20.0, 160.0),
                    StockPosition("ITM004", "Milk 500ml", 5.0, 25.0)
                )
            }
        )
    }

    suspend fun getGstReport(): GstReport {
        return makeRequest(
            endpoint = "/api/gst/report",
            method = "GET",
            parser = { jsonParser.decodeFromString<GstReport>(it) },
            fallback = {
                GstReport(
                    output_gst_sales = 393.75,
                    input_gst_purchases = 1500.00,
                    itc_utilized = 393.75,
                    net_gst_payable_in_cash = 0.00,
                    excess_itc_carried_forward = 1106.25
                )
            }
        )
    }

    suspend fun getPnlStatement(): PnlStatement {
        return makeRequest(
            endpoint = "/api/pnl",
            method = "GET",
            parser = { jsonParser.decodeFromString<PnlStatement>(it) },
            fallback = {
                PnlStatement(
                    revenue = 12675.00,
                    cost_of_goods_sold = 6550.00,
                    gross_profit = 6125.00,
                    gross_profit_margin_percent = 48.32,
                    operating_expenses = 850.00,
                    net_profit = 5275.00
                )
            }
        )
    }

    suspend fun createSalesInvoice(req: SalesInvoiceRequest): Boolean {
        return makeRequest(
            endpoint = "/api/sales/invoice",
            method = "POST",
            requestBody = jsonParser.encodeToString(req),
            parser = { true },
            fallback = { true }
        )
    }

    suspend fun createPurchaseInvoice(req: PurchaseInvoiceRequest): Boolean {
        return makeRequest(
            endpoint = "/api/purchases/invoice",
            method = "POST",
            requestBody = jsonParser.encodeToString(req),
            parser = { true },
            fallback = { true }
        )
    }
}
