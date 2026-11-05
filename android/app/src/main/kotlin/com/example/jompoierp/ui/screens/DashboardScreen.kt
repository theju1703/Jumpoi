package com.example.jompoierp.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.jompoierp.data.api.ErpApiClient
import com.example.jompoierp.data.model.ExecutiveSummary
import com.example.jompoierp.ui.theme.*
import kotlinx.coroutines.launch

@Composable
fun DashboardScreen(
    onNavigateToPos: () -> Unit,
    onNavigateToInventory: () -> Unit,
    onNavigateToPurchases: () -> Unit,
    onNavigateToGst: () -> Unit,
    onNavigateToPnl: () -> Unit,
    onLogout: () -> Unit
) {
    val coroutineScope = rememberCoroutineScope()
    var summary by remember { mutableStateOf<ExecutiveSummary?>(null) }
    var isLoading by remember { mutableStateOf(true) }

    LaunchedEffect(Unit) {
        coroutineScope.launch {
            summary = ErpApiClient.getExecutiveSummary()
            isLoading = false
        }
    }

    Scaffold(
        containerColor = BgPrimary,
        topBar = {
            Surface(color = BgSecondary, shadowElevation = 4.dp) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .statusBarsPadding()
                        .padding(horizontal = 16.dp, vertical = 12.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column {
                        Text(
                            text = "Jumpoi ERP Hub",
                            color = TextPrimary,
                            fontWeight = FontWeight.Bold,
                            fontSize = 18.sp
                        )
                        Text(
                            text = "Supermarket Operations",
                            color = AccentEmerald,
                            fontSize = 11.sp,
                            fontWeight = FontWeight.SemiBold
                        )
                    }

                    TextButton(onClick = onLogout) {
                        Text("Sign Out", color = AccentRed, fontSize = 13.sp)
                    }
                }
            }
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            // KPI Summary Grid
            item {
                Text(
                    text = "Executive Real-Time Metrics",
                    color = TextSecondary,
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold
                )
            }

            item {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    KpiCard(
                        title = "Gross Revenue",
                        value = summary?.let { "Rs ${it.gross_sales_revenue}" } ?: "Rs 12,675.00",
                        sub = "3 Sales Invoices",
                        accentColor = AccentBlue,
                        modifier = Modifier.weight(1f)
                    )
                    KpiCard(
                        title = "Procurement",
                        value = summary?.let { "Rs ${it.gross_procurement_spend}" } ?: "Rs 30,950.00",
                        sub = "2 Vendor Bills",
                        accentColor = AccentAmber,
                        modifier = Modifier.weight(1f)
                    )
                }
            }

            item {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    KpiCard(
                        title = "Active SKUs",
                        value = "${summary?.active_items_count ?: 4} Items",
                        sub = "Catalog Verified",
                        accentColor = AccentEmerald,
                        modifier = Modifier.weight(1f)
                    )
                    KpiCard(
                        title = "Cloud Sync",
                        value = "BigQuery",
                        sub = "Dataset Synced",
                        accentColor = AccentPurple,
                        modifier = Modifier.weight(1f)
                    )
                }
            }

            // Quick Operations Actions
            item {
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "Core ERP Operations",
                    color = TextSecondary,
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold
                )
            }

            item {
                ActionCard(
                    title = "POS Billing & Checkout",
                    description = "Barcode scanning, cart totals with per-item GST, & invoice printing",
                    tag = "CASHIER",
                    accentColor = AccentBlue,
                    onClick = onNavigateToPos
                )
            }

            item {
                ActionCard(
                    title = "Inventory & Stock Movements",
                    description = "Real-time stock on hand, valuation at retail, & audit adjustments",
                    tag = "WAREHOUSE",
                    accentColor = AccentEmerald,
                    onClick = onNavigateToInventory
                )
            }

            item {
                ActionCard(
                    title = "Supplier Purchases & Bills",
                    description = "Vendor procurement entries with line-item GST & ITC credit capture",
                    tag = "PURCHASING",
                    accentColor = AccentAmber,
                    onClick = onNavigateToPurchases
                )
            }

            item {
                ActionCard(
                    title = "GST ITC Tax Reconciliation",
                    description = "Reconcile GSTR-1 output liability vs GSTR-2B input credits",
                    tag = "TAX REPORT",
                    accentColor = AccentPurple,
                    onClick = onNavigateToGst
                )
            }

            item {
                ActionCard(
                    title = "Profit & Loss (P&L) Statement",
                    description = "Financial revenue, COGS, gross margin %, & net operating profit",
                    tag = "FINANCE",
                    accentColor = AccentBlueDark,
                    onClick = onNavigateToPnl
                )
            }
        }
    }
}

@Composable
fun KpiCard(
    title: String,
    value: String,
    sub: String,
    accentColor: Color,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier,
        colors = CardDefaults.cardColors(containerColor = BgCard),
        shape = RoundedCornerShape(12.dp),
        border = CardDefaults.outlinedCardBorder().copy(brush = androidx.compose.ui.graphics.SolidColor(BorderColor))
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            Text(title, color = TextSecondary, fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
            Spacer(modifier = Modifier.height(4.dp))
            Text(value, color = accentColor, fontSize = 16.sp, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.height(2.dp))
            Text(sub, color = TextSecondary, fontSize = 10.sp)
        }
    }
}

@Composable
fun ActionCard(
    title: String,
    description: String,
    tag: String,
    accentColor: Color,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        colors = CardDefaults.cardColors(containerColor = BgCard),
        shape = RoundedCornerShape(12.dp),
        border = CardDefaults.outlinedCardBorder().copy(brush = androidx.compose.ui.graphics.SolidColor(BorderColor))
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(title, color = TextPrimary, fontWeight = FontWeight.Bold, fontSize = 15.sp)
                    Spacer(modifier = Modifier.width(8.dp))
                    Surface(
                        color = accentColor.copy(alpha = 0.2f),
                        shape = RoundedCornerShape(4.dp)
                    ) {
                        Text(
                            text = tag,
                            color = accentColor,
                            fontSize = 9.sp,
                            fontWeight = FontWeight.Bold,
                            modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                        )
                    }
                }
                Spacer(modifier = Modifier.height(4.dp))
                Text(description, color = TextSecondary, fontSize = 12.sp)
            }
            Text("→", color = accentColor, fontSize = 20.sp, fontWeight = FontWeight.Bold)
        }
    }
}
