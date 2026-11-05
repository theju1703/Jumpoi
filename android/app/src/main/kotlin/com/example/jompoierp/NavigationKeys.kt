package com.example.jompoierp

import androidx.navigation3.runtime.NavKey
import kotlinx.serialization.Serializable

@Serializable
data object LoginNav : NavKey

@Serializable
data object DashboardNav : NavKey

@Serializable
data object PosBillingNav : NavKey

@Serializable
data class InvoicePrintNav(
    val invoiceNo: String = "INV-2026-001",
    val customerName: String = "ABC Stores",
    val customerCity: String = "Chennai",
    val totalAmount: Double = 4725.0
) : NavKey

@Serializable
data object InventoryNav : NavKey

@Serializable
data object PurchasesNav : NavKey

@Serializable
data object GstReportNav : NavKey

@Serializable
data object PnlNav : NavKey
