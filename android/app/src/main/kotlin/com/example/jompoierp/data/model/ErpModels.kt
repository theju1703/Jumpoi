package com.example.jompoierp.data.model

import kotlinx.serialization.Serializable

@Serializable
data class UserLoginRequest(
    val username: String,
    val password: String
)

@Serializable
data class AuthResponse(
    val access_token: String,
    val token_type: String,
    val username: String,
    val full_name: String,
    val role: String
)

@Serializable
data class Item(
    val item_code: String,
    val name: String,
    val brand: String = "",
    val category: String = "",
    val price: Double = 0.0,
    val gst_percent: Double = 5.0,
    val min_stock_alert: Double = 10.0,
    val barcode: String? = null,
    val description: String? = null
)

@Serializable
data class SalesItemRequest(
    val item_code: String,
    val quantity: Double,
    val rate: Double? = null
)

@Serializable
data class SalesInvoiceRequest(
    val invoice_no: String,
    val customer_name: String,
    val customer_city: String,
    val payment_mode: String = "CASH",
    val items: List<SalesItemRequest>
)

@Serializable
data class PurchaseItemRequest(
    val item_code: String,
    val item_name: String,
    val item_description: String? = null,
    val quantity: Double,
    val rate: Double,
    val gst_percent: Double = 5.0
)

@Serializable
data class PurchaseInvoiceRequest(
    val invoice_no: String,
    val invoice_date: String,
    val vendor: String,
    val items: List<PurchaseItemRequest>
)

@Serializable
data class StockPosition(
    val item_code: String,
    val item_name: String? = null,
    val current_stock: Double = 0.0,
    val unit_valuation: Double = 0.0
)

@Serializable
data class StockAdjustmentRequest(
    val item_code: String,
    val adjustment_type: String, // 'ADD' or 'DEDUCT'
    val quantity: Double,
    val reason: String,
    val notes: String? = null
)

@Serializable
data class LowStockAlert(
    val item_code: String,
    val item_name: String? = null,
    val current_stock: Double,
    val min_stock_alert: Double,
    val status: String
)

@Serializable
data class GstReport(
    val output_gst_sales: Double = 0.0,
    val input_gst_purchases: Double = 0.0,
    val itc_utilized: Double = 0.0,
    val net_gst_payable_in_cash: Double = 0.0,
    val excess_itc_carried_forward: Double = 0.0
)

@Serializable
data class PnlStatement(
    val revenue: Double = 0.0,
    val cost_of_goods_sold: Double = 0.0,
    val gross_profit: Double = 0.0,
    val gross_profit_margin_percent: Double = 0.0,
    val operating_expenses: Double = 0.0,
    val net_profit: Double = 0.0
)

@Serializable
data class ExecutiveSummary(
    val active_items_count: Int = 0,
    val total_sales_invoices: Int = 0,
    val total_purchase_bills: Int = 0,
    val gross_sales_revenue: Double = 0.0,
    val gross_procurement_spend: Double = 0.0,
    val status: String = "OPERATIONAL"
)

@Serializable
data class Customer(
    val customer_id: String,
    val name: String,
    val city: String,
    val phone: String,
    val address: String? = null
)
