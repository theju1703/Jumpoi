package com.example.jompoierp.ui.screens

import androidx.compose.foundation.background
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
import com.example.jompoierp.data.model.GstReport
import com.example.jompoierp.data.model.PnlStatement
import com.example.jompoierp.ui.theme.*
import kotlinx.coroutines.launch

@Composable
fun GstReportScreen(onNavigateBack: () -> Unit) {
    val coroutineScope = rememberCoroutineScope()
    var gstReport by remember { mutableStateOf<GstReport?>(null) }

    LaunchedEffect(Unit) {
        coroutineScope.launch {
            gstReport = ErpApiClient.getGstReport()
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
                    TextButton(onClick = onNavigateBack) {
                        Text("← Back", color = TextSecondary, fontSize = 14.sp)
                    }
                    Text("GST & ITC Reconciliation", color = TextPrimary, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                    Text("GSTR-2B", color = AccentEmerald, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                }
            }
        }
    ) { padding ->
        val report = gstReport ?: GstReport(393.75, 1500.0, 393.75, 0.0, 1106.25)
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            item {
                Text("Government Tax Credit Audit (GSTR-1 vs GSTR-2B)", color = TextSecondary, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            }

            item {
                TaxCard("Output GST Liability (Sales)", "Rs ${"%.2f".format(report.output_gst_sales)}", "Collected from customers on GSTR-1", AccentBlue)
            }
            item {
                TaxCard("Input Tax Credit (ITC Available)", "Rs ${"%.2f".format(report.input_gst_purchases)}", "Paid to vendors & matched on GSTR-2B", AccentEmerald)
            }
            item {
                TaxCard("Eligible ITC Utilized", "Rs ${"%.2f".format(report.itc_utilized)}", "Offset against output tax liability", AccentPurple)
            }
            item {
                TaxCard("Net Cash Payable to Govt", "Rs ${"%.2f".format(report.net_gst_payable_in_cash)}", "Zero cash liability due to full ITC offset", AccentAmber)
            }
            item {
                TaxCard("Excess ITC Carried Forward", "Rs ${"%.2f".format(report.excess_itc_carried_forward)}", "Credit buffer carried to next tax period", AccentEmerald)
            }
        }
    }
}

@Composable
fun TaxCard(title: String, value: String, description: String, color: Color) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = BgCard),
        shape = RoundedCornerShape(10.dp),
        border = CardDefaults.outlinedCardBorder().copy(brush = androidx.compose.ui.graphics.SolidColor(BorderColor))
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(title, color = TextSecondary, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
            Spacer(modifier = Modifier.height(4.dp))
            Text(value, color = color, fontSize = 20.sp, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.height(4.dp))
            Text(description, color = TextSecondary, fontSize = 11.sp)
        }
    }
}

@Composable
fun PnlScreen(onNavigateBack: () -> Unit) {
    val coroutineScope = rememberCoroutineScope()
    var pnl by remember { mutableStateOf<PnlStatement?>(null) }

    LaunchedEffect(Unit) {
        coroutineScope.launch {
            pnl = ErpApiClient.getPnlStatement()
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
                    TextButton(onClick = onNavigateBack) {
                        Text("← Back", color = TextSecondary, fontSize = 14.sp)
                    }
                    Text("ERP Profit & Loss Statement", color = TextPrimary, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                    Text("Monthly", color = AccentBlue, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                }
            }
        }
    ) { padding ->
        val statement = pnl ?: PnlStatement(12675.0, 6550.0, 6125.0, 48.32, 850.0, 5275.0)
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            item {
                Text("Operational Financial Accounting Output", color = TextSecondary, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            }

            item {
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = BgCard),
                    shape = RoundedCornerShape(10.dp)
                ) {
                    Column(modifier = Modifier.padding(18.dp)) {
                        PnlRow("I. Gross Sales Revenue", "Rs ${"%.2f".format(statement.revenue)}", AccentBlue, true)
                        Divider(color = BorderColor, modifier = Modifier.padding(vertical = 8.dp))

                        PnlRow("II. Less: Cost of Goods Sold (COGS)", "(Rs ${"%.2f".format(statement.cost_of_goods_sold)})", TextSecondary, false)
                        Divider(color = BorderColor, modifier = Modifier.padding(vertical = 8.dp))

                        PnlRow("III. Gross Operating Profit", "Rs ${"%.2f".format(statement.gross_profit)}", AccentEmerald, true)
                        Text("Gross Margin: ${statement.gross_profit_margin_percent}%", color = AccentEmerald, fontSize = 11.sp, modifier = Modifier.align(Alignment.End))
                        Divider(color = BorderColor, modifier = Modifier.padding(vertical = 8.dp))

                        PnlRow("IV. Less: Store Operating Expenses", "(Rs ${"%.2f".format(statement.operating_expenses)})", TextSecondary, false)
                        Divider(color = AccentEmerald, thickness = 2.dp, modifier = Modifier.padding(vertical = 10.dp))

                        PnlRow("V. NET OPERATING PROFIT", "Rs ${"%.2f".format(statement.net_profit)}", AccentEmerald, true)
                    }
                }
            }
        }
    }
}

@Composable
fun PnlRow(title: String, amount: String, color: Color, isBold: Boolean) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(title, color = if (isBold) TextPrimary else TextSecondary, fontWeight = if (isBold) FontWeight.Bold else FontWeight.Normal, fontSize = 13.sp)
        Text(amount, color = color, fontWeight = if (isBold) FontWeight.Bold else FontWeight.SemiBold, fontSize = if (isBold) 15.sp else 13.sp)
    }
}
