package com.example.jompoierp.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
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
import com.example.jompoierp.data.model.StockPosition
import com.example.jompoierp.ui.theme.*
import kotlinx.coroutines.launch

@Composable
fun InventoryScreen(
    onNavigateBack: () -> Unit
) {
    val coroutineScope = rememberCoroutineScope()
    var stockList by remember { mutableStateOf<List<StockPosition>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }

    LaunchedEffect(Unit) {
        coroutineScope.launch {
            stockList = ErpApiClient.getStockPosition()
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
                    TextButton(onClick = onNavigateBack) {
                        Text("← Back", color = TextSecondary, fontSize = 14.sp)
                    }
                    Text("Stock & Inventory Ledger", color = TextPrimary, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                    Text("${stockList.size} SKUs", color = AccentEmerald, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                }
            }
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            item {
                Text(
                    "Real-Time Warehouse Stock Balance (IN - OUT)",
                    color = TextSecondary,
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold
                )
            }

            items(stockList) { stock ->
                Card(
                    colors = CardDefaults.cardColors(containerColor = BgCard),
                    shape = RoundedCornerShape(10.dp),
                    border = CardDefaults.outlinedCardBorder().copy(brush = androidx.compose.ui.graphics.SolidColor(BorderColor))
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(14.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text(stock.item_code, color = AccentBlue, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                                Spacer(modifier = Modifier.width(6.dp))
                                Surface(
                                    color = if (stock.current_stock <= 10) AccentRed.copy(alpha = 0.2f) else AccentEmerald.copy(alpha = 0.2f),
                                    shape = RoundedCornerShape(4.dp)
                                ) {
                                    Text(
                                        text = if (stock.current_stock <= 10) "LOW STOCK" else "IN STOCK",
                                        color = if (stock.current_stock <= 10) AccentRed else AccentEmerald,
                                        fontSize = 9.sp,
                                        fontWeight = FontWeight.Bold,
                                        modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                                    )
                                }
                            }
                            Spacer(modifier = Modifier.height(4.dp))
                            Text(stock.item_name ?: stock.item_code, color = TextPrimary, fontWeight = FontWeight.Bold, fontSize = 15.sp)
                            Text("Retail Valuation: Rs ${stock.unit_valuation}", color = TextSecondary, fontSize = 12.sp)
                        }

                        Column(horizontalAlignment = Alignment.End) {
                            Text("${stock.current_stock.toInt()} Units", color = TextPrimary, fontWeight = FontWeight.ExtraBold, fontSize = 18.sp)
                            Text("Audit Verified", color = AccentEmerald, fontSize = 10.sp)
                        }
                    }
                }
            }
        }
    }
}
