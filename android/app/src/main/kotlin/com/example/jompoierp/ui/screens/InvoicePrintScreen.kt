package com.example.jompoierp.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.jompoierp.ui.theme.*

@Composable
fun InvoicePrintScreen(
    invoiceNo: String,
    customerName: String,
    customerCity: String,
    totalAmount: Double,
    onNavigateBack: () -> Unit
) {
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
                    Text("Official Tax Invoice", color = TextPrimary, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                    Button(
                        onClick = { /* Android PrintManager trigger */ },
                        colors = ButtonDefaults.buttonColors(containerColor = AccentEmerald),
                        shape = RoundedCornerShape(6.dp),
                        contentPadding = PaddingValues(horizontal = 12.dp, vertical = 4.dp)
                    ) {
                        Text("🖨 Print", fontSize = 12.sp, fontWeight = FontWeight.Bold)
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
            item {
                // Printable White Sheet Container
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = Color.White),
                    shape = RoundedCornerShape(8.dp),
                    elevation = CardDefaults.cardElevation(6.dp)
                ) {
                    Column(modifier = Modifier.padding(20.dp)) {
                        // Header
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.Top
                        ) {
                            Column {
                                Text("JOMPOI ONLINE GROCERY", color = Color(0xFF0F172A), fontWeight = FontWeight.ExtraBold, fontSize = 18.sp)
                                Text("Wholesale & Retail Supermarket ERP", color = Color(0xFF64748B), fontSize = 11.sp)
                                Text("GSTIN: 33AAAAA0000A1Z5", color = Color(0xFF64748B), fontSize = 10.sp)
                            }
                            Surface(
                                color = Color(0xFF0F172A),
                                shape = RoundedCornerShape(4.dp)
                            ) {
                                Text(
                                    "TAX INVOICE",
                                    color = Color.White,
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Bold,
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                                )
                            }
                        }

                        Divider(color = Color(0xFF0F172A), thickness = 2.dp, modifier = Modifier.padding(vertical = 12.dp))

                        // Parties Row
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .background(Color(0xFFF8FAFC), shape = RoundedCornerShape(6.dp))
                                .padding(10.dp),
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Column(modifier = Modifier.weight(1f)) {
                                Text("BILLED TO:", color = Color(0xFF64748B), fontSize = 9.sp, fontWeight = FontWeight.Bold)
                                Text(customerName, color = Color(0xFF0F172A), fontSize = 13.sp, fontWeight = FontWeight.Bold)
                                Text("City: $customerCity, Tamil Nadu", color = Color(0xFF475569), fontSize = 11.sp)
                            }
                            Column(modifier = Modifier.weight(1f)) {
                                Text("INVOICE DETAILS:", color = Color(0xFF64748B), fontSize = 9.sp, fontWeight = FontWeight.Bold)
                                Text("Invoice No: $invoiceNo", color = Color(0xFF0F172A), fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
                                Text("Date: 2026-11-05", color = Color(0xFF475569), fontSize = 11.sp)
                                Text("Place of Supply: 33 (TN)", color = Color(0xFF475569), fontSize = 10.sp)
                            }
                        }

                        Spacer(modifier = Modifier.height(16.dp))

                        // EXACT CLIENT TABLE HEADER
                        Surface(color = Color(0xFF0F172A), shape = RoundedCornerShape(4.dp)) {
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(vertical = 8.dp, horizontal = 8.dp),
                                horizontalArrangement = Arrangement.SpaceBetween
                            ) {
                                Text("Item Details", color = Color.White, fontSize = 11.sp, fontWeight = FontWeight.Bold, modifier = Modifier.weight(2f))
                                Text("Qty", color = Color.White, fontSize = 11.sp, fontWeight = FontWeight.Bold, modifier = Modifier.weight(0.6f))
                                Text("Price", color = Color.White, fontSize = 11.sp, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f))
                                Text("Tax", color = Color.White, fontSize = 11.sp, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1f))
                                Text("Total", color = Color.White, fontSize = 11.sp, fontWeight = FontWeight.Bold, modifier = Modifier.weight(1.2f))
                            }
                        }

                        // Table Line Item 1
                        InvoiceLineRow(
                            name = "Basmati Rice 5kg",
                            desc = "India Gate Classic Aged Grain",
                            qty = "2",
                            price = "Rs 450.00",
                            tax = "5% (Rs 22.50)",
                            total = "Rs 945.00"
                        )
                        Divider(color = Color(0xFFE2E8F0))

                        // Table Line Item 2
                        InvoiceLineRow(
                            name = "Sunflower Oil 1L",
                            desc = "Fortune Pure Refined Oil",
                            qty = "1",
                            price = "Rs 135.00",
                            tax = "5% (Rs 6.75)",
                            total = "Rs 141.75"
                        )
                        Divider(color = Color(0xFFE2E8F0))

                        // Summary Section
                        Spacer(modifier = Modifier.height(16.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.End
                        ) {
                            Column(
                                modifier = Modifier
                                    .width(260.dp)
                                    .background(Color(0xFFF8FAFC), shape = RoundedCornerShape(6.dp))
                                    .padding(12.dp)
                            ) {
                                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                    Text("Subtotal:", color = Color(0xFF64748B), fontSize = 11.sp)
                                    Text("Rs 1,035.00", color = Color(0xFF0F172A), fontSize = 11.sp)
                                }
                                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                    Text("GST Output Tax:", color = Color(0xFF64748B), fontSize = 11.sp)
                                    Text("Rs 51.75", color = Color(0xFF0F172A), fontSize = 11.sp)
                                }
                                Divider(color = Color(0xFF0F172A), thickness = 1.dp, modifier = Modifier.padding(vertical = 4.dp))
                                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                    Column {
                                        Text("Grand Total", color = Color(0xFF0F172A), fontWeight = FontWeight.Bold, fontSize = 12.sp)
                                        Text("(Price+Tax)×Qty", color = AccentBlue, fontSize = 8.sp)
                                    }
                                    Text("Rs ${"%.2f".format(totalAmount)}", color = Color(0xFF0F172A), fontWeight = FontWeight.ExtraBold, fontSize = 15.sp)
                                }
                            }
                        }

                        // Footer Notes
                        Spacer(modifier = Modifier.height(20.dp))
                        Divider(color = Color(0xFFCBD5E1), modifier = Modifier.padding(vertical = 8.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Text("Computer-generated tax invoice.\nEligible for Input Tax Credit under GST.", color = Color(0xFF94A3B8), fontSize = 9.sp)
                            Text("Authorized Signatory\nJompoi Online Grocery", color = Color(0xFF64748B), fontSize = 9.sp, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun InvoiceLineRow(
    name: String,
    desc: String?,
    qty: String,
    price: String,
    tax: String,
    total: String
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp, horizontal = 8.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column(modifier = Modifier.weight(2f)) {
            Text(name, color = Color(0xFF0F172A), fontWeight = FontWeight.Bold, fontSize = 12.sp)
            if (desc != null) {
                Text(desc, color = Color(0xFF64748B), fontSize = 9.sp)
            }
        }
        Text(qty, color = Color(0xFF0F172A), fontSize = 11.sp, modifier = Modifier.weight(0.6f))
        Text(price, color = Color(0xFF475569), fontSize = 11.sp, modifier = Modifier.weight(1f))
        Text(tax, color = Color(0xFF475569), fontSize = 10.sp, modifier = Modifier.weight(1f))
        Text(total, color = Color(0xFF0F172A), fontWeight = FontWeight.Bold, fontSize = 11.sp, modifier = Modifier.weight(1.2f))
    }
}
