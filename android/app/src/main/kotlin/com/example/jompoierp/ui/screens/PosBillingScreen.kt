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
import com.example.jompoierp.data.model.*
import com.example.jompoierp.ui.theme.*
import kotlinx.coroutines.launch

data class CartItem(
    val item: Item,
    var quantity: Double
) {
    val unitTax: Double get() = item.price * (item.gst_percent / 100.0)
    val lineNet: Double get() = item.price * quantity
    val lineTax: Double get() = unitTax * quantity
    // Formula: (Price + Tax) * Quantity
    val lineTotal: Double get() = (item.price + unitTax) * quantity
}

@Composable
fun PosBillingScreen(
    onNavigateBack: () -> Unit,
    onNavigateToInvoicePrint: (invoiceNo: String, customerName: String, customerCity: String, total: Double) -> Unit
) {
    val coroutineScope = rememberCoroutineScope()
    var availableItems by remember { mutableStateOf<List<Item>>(emptyList()) }
    val cart = remember { mutableStateListOf<CartItem>() }
    var customerName by remember { mutableStateOf("ABC Stores") }
    var customerCity by remember { mutableStateOf("Chennai") }
    var barcodeInput by remember { mutableStateOf("") }
    var isCheckingOut by remember { mutableStateOf(false) }

    LaunchedEffect(Unit) {
        val items = ErpApiClient.getItems()
        availableItems = items
        // Seed initial demo cart
        if (items.isNotEmpty()) {
            cart.add(CartItem(items[0], 2.0)) // Basmati Rice
            if (items.size > 1) {
                cart.add(CartItem(items[1], 1.0)) // Sunflower Oil
            }
        }
    }

    val subtotal = cart.sumOf { it.lineNet }
    val totalTax = cart.sumOf { it.lineTax }
    val grandTotal = cart.sumOf { it.lineTotal }

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
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        TextButton(onClick = onNavigateBack) {
                            Text("← Back", color = TextSecondary, fontSize = 14.sp)
                        }
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("POS Counter Billing", color = TextPrimary, fontWeight = FontWeight.Bold, fontSize = 17.sp)
                    }
                    Text(
                        "${cart.size} Items",
                        color = AccentEmerald,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            }
        },
        bottomBar = {
            Surface(
                color = BgCard,
                border = CardDefaults.outlinedCardBorder().copy(brush = androidx.compose.ui.graphics.SolidColor(BorderColor))
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .navigationBarsPadding()
                        .padding(16.dp)
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Text("Taxable Subtotal:", color = TextSecondary, fontSize = 13.sp)
                        Text("Rs ${"%.2f".format(subtotal)}", color = TextPrimary, fontSize = 13.sp)
                    }
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Text("GST Output Tax:", color = TextSecondary, fontSize = 13.sp)
                        Text("Rs ${"%.2f".format(totalTax)}", color = AccentAmber, fontSize = 13.sp)
                    }
                    Divider(color = BorderColor, modifier = Modifier.padding(vertical = 8.dp))
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column {
                            Text("Grand Total", color = TextSecondary, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                            Text("(Price+Tax)×Qty", color = AccentBlue, fontSize = 9.sp)
                        }
                        Text(
                            "Rs ${"%.2f".format(grandTotal)}",
                            color = AccentEmerald,
                            fontSize = 20.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }

                    Spacer(modifier = Modifier.height(12.dp))

                    Button(
                        onClick = {
                            isCheckingOut = true
                            coroutineScope.launch {
                                val invoiceNo = "INV-POS-${System.currentTimeMillis() % 10000}"
                                val req = SalesInvoiceRequest(
                                    invoice_no = invoiceNo,
                                    customer_name = customerName,
                                    customer_city = customerCity,
                                    items = cart.map {
                                        SalesItemRequest(
                                            item_code = it.item.item_code,
                                            quantity = it.quantity,
                                            rate = it.item.price
                                        )
                                    }
                                )
                                ErpApiClient.createSalesInvoice(req)
                                isCheckingOut = false
                                onNavigateToInvoicePrint(invoiceNo, customerName, customerCity, grandTotal)
                            }
                        },
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(48.dp),
                        shape = RoundedCornerShape(8.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = AccentBlue),
                        enabled = cart.isNotEmpty() && !isCheckingOut
                    ) {
                        Text("Checkout & Print Invoice 🖨", fontWeight = FontWeight.Bold, fontSize = 15.sp)
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
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            // Customer Header
            item {
                Card(
                    colors = CardDefaults.cardColors(containerColor = BgCard),
                    shape = RoundedCornerShape(10.dp)
                ) {
                    Column(modifier = Modifier.padding(14.dp)) {
                        Text("Customer Details", color = TextSecondary, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                        Spacer(modifier = Modifier.height(8.dp))
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            OutlinedTextField(
                                value = customerName,
                                onValueChange = { customerName = it },
                                label = { Text("Name", fontSize = 11.sp) },
                                modifier = Modifier.weight(1.5f),
                                singleLine = true
                            )
                            OutlinedTextField(
                                value = customerCity,
                                onValueChange = { customerCity = it },
                                label = { Text("City", fontSize = 11.sp) },
                                modifier = Modifier.weight(1f),
                                singleLine = true
                            )
                        }
                    }
                }
            }

            // Quick Item Selector
            item {
                Text("Select Master Products to Add:", color = TextSecondary, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                Spacer(modifier = Modifier.height(6.dp))
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    availableItems.take(4).forEach { itm ->
                        AssistChip(
                            onClick = {
                                val existing = cart.find { it.item.item_code == itm.item_code }
                                if (existing != null) {
                                    existing.quantity += 1.0
                                } else {
                                    cart.add(CartItem(itm, 1.0))
                                }
                            },
                            label = { Text("+ ${itm.name.split(" ")[0]}", fontSize = 10.sp) }
                        )
                    }
                }
            }

            // Cart Items List
            item {
                Text("Cart Line Items with per-item Tax:", color = TextSecondary, fontSize = 12.sp, fontWeight = FontWeight.Bold)
            }

            items(cart) { line ->
                Card(
                    colors = CardDefaults.cardColors(containerColor = BgCard),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(12.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text(line.item.name, color = TextPrimary, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                            Text(
                                "Price: Rs ${line.item.price} + Tax (${line.item.gst_percent}% = Rs ${"%.2f".format(line.unitTax)})",
                                color = TextSecondary,
                                fontSize = 11.sp
                            )
                            Text(
                                "Total = (Price + Tax) × ${line.quantity.toInt()} = Rs ${"%.2f".format(line.lineTotal)}",
                                color = AccentBlue,
                                fontSize = 11.sp,
                                fontWeight = FontWeight.SemiBold
                            )
                        }

                        Row(verticalAlignment = Alignment.CenterVertically) {
                            IconButton(onClick = {
                                if (line.quantity > 1) {
                                    line.quantity -= 1.0
                                } else {
                                    cart.remove(line)
                                }
                            }) {
                                Text("-", color = AccentRed, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                            }
                            Text(
                                "${line.quantity.toInt()}",
                                color = TextPrimary,
                                fontWeight = FontWeight.Bold,
                                fontSize = 14.sp,
                                modifier = Modifier.padding(horizontal = 4.dp)
                            )
                            IconButton(onClick = { line.quantity += 1.0 }) {
                                Text("+", color = AccentEmerald, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
            }
        }
    }
}
