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
import com.example.jompoierp.data.model.PurchaseInvoiceRequest
import com.example.jompoierp.data.model.PurchaseItemRequest
import com.example.jompoierp.ui.theme.*
import kotlinx.coroutines.launch

@Composable
fun PurchasesScreen(
    onNavigateBack: () -> Unit
) {
    val coroutineScope = rememberCoroutineScope()
    var vendorName by remember { mutableStateOf("KR Agro Supplies") }
    var invoiceNo by remember { mutableStateOf("PUR-2026-099") }
    var itemName by remember { mutableStateOf("Basmati Rice 5kg") }
    var qty by remember { mutableStateOf("50") }
    var rate by remember { mutableStateOf("350.0") }
    var gstPercent by remember { mutableStateOf("5.0") }
    var isSubmitted by remember { mutableStateOf(false) }

    val qtyNum = qty.toDoubleOrNull() ?: 0.0
    val rateNum = rate.toDoubleOrNull() ?: 0.0
    val gstNum = gstPercent.toDoubleOrNull() ?: 0.0
    val netAmount = qtyNum * rateNum
    val gstAmount = netAmount * (gstNum / 100.0)
    val totalAmount = netAmount + gstAmount

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
                    Text("Vendor Procurement Bill", color = TextPrimary, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                    Text("ITC Source", color = AccentAmber, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                }
            }
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            item {
                Text(
                    "Record Vendor Inward Bill with Per-Item GST",
                    color = TextSecondary,
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold
                )
            }

            item {
                Card(
                    colors = CardDefaults.cardColors(containerColor = BgCard),
                    shape = RoundedCornerShape(10.dp)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        OutlinedTextField(
                            value = vendorName,
                            onValueChange = { vendorName = it },
                            label = { Text("Vendor / Supplier Name") },
                            modifier = Modifier.fillMaxWidth(),
                            singleLine = true
                        )
                        Spacer(modifier = Modifier.height(10.dp))
                        OutlinedTextField(
                            value = invoiceNo,
                            onValueChange = { invoiceNo = it },
                            label = { Text("Vendor Invoice No") },
                            modifier = Modifier.fillMaxWidth(),
                            singleLine = true
                        )
                    }
                }
            }

            item {
                Card(
                    colors = CardDefaults.cardColors(containerColor = BgCard),
                    shape = RoundedCornerShape(10.dp)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Item & Input Tax Credit (ITC) Details", color = TextSecondary, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(10.dp))
                        OutlinedTextField(
                            value = itemName,
                            onValueChange = { itemName = it },
                            label = { Text("Product / Item Name") },
                            modifier = Modifier.fillMaxWidth(),
                            singleLine = true
                        )
                        Spacer(modifier = Modifier.height(10.dp))
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            OutlinedTextField(
                                value = qty,
                                onValueChange = { qty = it },
                                label = { Text("Quantity") },
                                modifier = Modifier.weight(1f),
                                singleLine = true
                            )
                            OutlinedTextField(
                                value = rate,
                                onValueChange = { rate = it },
                                label = { Text("Cost Price (Rs)") },
                                modifier = Modifier.weight(1f),
                                singleLine = true
                            )
                            OutlinedTextField(
                                value = gstPercent,
                                onValueChange = { gstPercent = it },
                                label = { Text("GST %") },
                                modifier = Modifier.weight(1f),
                                singleLine = true
                            )
                        }

                        Spacer(modifier = Modifier.height(14.dp))
                        Divider(color = BorderColor)
                        Spacer(modifier = Modifier.height(10.dp))

                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            Text("Taxable Net:", color = TextSecondary, fontSize = 12.sp)
                            Text("Rs ${"%.2f".format(netAmount)}", color = TextPrimary, fontSize = 12.sp)
                        }
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            Text("Input Tax Credit (ITC Claimed):", color = AccentEmerald, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                            Text("Rs ${"%.2f".format(gstAmount)}", color = AccentEmerald, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                        }
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            Text("Gross Procurement Total:", color = TextPrimary, fontWeight = FontWeight.Bold, fontSize = 13.sp)
                            Text("Rs ${"%.2f".format(totalAmount)}", color = AccentAmber, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                        }

                        Spacer(modifier = Modifier.height(16.dp))

                        Button(
                            onClick = {
                                coroutineScope.launch {
                                    val req = PurchaseInvoiceRequest(
                                        invoice_no = invoiceNo,
                                        invoice_date = "2026-11-05",
                                        vendor = vendorName,
                                        items = listOf(
                                            PurchaseItemRequest(
                                                item_code = "ITM001",
                                                item_name = itemName,
                                                quantity = qtyNum,
                                                rate = rateNum,
                                                gst_percent = gstNum
                                            )
                                        )
                                    )
                                    ErpApiClient.createPurchaseInvoice(req)
                                    isSubmitted = true
                                }
                            },
                            modifier = Modifier.fillMaxWidth(),
                            colors = ButtonDefaults.buttonColors(containerColor = AccentAmber),
                            shape = RoundedCornerShape(8.dp)
                        ) {
                            Text(
                                if (isSubmitted) "✓ Inward Bill Registered & Stock IN Logged" else "Record Inward Bill & Claim ITC",
                                fontWeight = FontWeight.Bold,
                                color = Color(0xFF0F172A)
                            )
                        }
                    }
                }
            }
        }
    }
}
