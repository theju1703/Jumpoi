package com.example.jompoierp

import androidx.compose.runtime.*
import androidx.navigation3.runtime.entryProvider
import androidx.navigation3.runtime.rememberNavBackStack
import androidx.navigation3.ui.NavDisplay
import com.example.jompoierp.ui.screens.*

@Composable
fun MainNavigation() {
    var isLoggedIn by remember { mutableStateOf(true) } // Start on Dashboard for instant demo review, switchable to Login
    var userRole by remember { mutableStateOf("ADMIN") }

    val backStack = rememberNavBackStack(DashboardNav)

    if (!isLoggedIn) {
        LoginScreen(onLoginSuccess = { role ->
            userRole = role
            isLoggedIn = true
        })
    } else {
        NavDisplay(
            backStack = backStack,
            onBack = { backStack.removeLastOrNull() },
            entryProvider = entryProvider {
                entry<DashboardNav> {
                    DashboardScreen(
                        onNavigateToPos = { backStack.add(PosBillingNav) },
                        onNavigateToInventory = { backStack.add(InventoryNav) },
                        onNavigateToPurchases = { backStack.add(PurchasesNav) },
                        onNavigateToGst = { backStack.add(GstReportNav) },
                        onNavigateToPnl = { backStack.add(PnlNav) },
                        onLogout = { isLoggedIn = false }
                    )
                }

                entry<PosBillingNav> {
                    PosBillingScreen(
                        onNavigateBack = { backStack.removeLastOrNull() },
                        onNavigateToInvoicePrint = { invNo, custName, city, total ->
                            backStack.add(InvoicePrintNav(invNo, custName, city, total))
                        }
                    )
                }

                entry<InvoicePrintNav> { key ->
                    InvoicePrintScreen(
                        invoiceNo = key.invoiceNo,
                        customerName = key.customerName,
                        customerCity = key.customerCity,
                        totalAmount = key.totalAmount,
                        onNavigateBack = { backStack.removeLastOrNull() }
                    )
                }

                entry<InventoryNav> {
                    InventoryScreen(
                        onNavigateBack = { backStack.removeLastOrNull() }
                    )
                }

                entry<PurchasesNav> {
                    PurchasesScreen(
                        onNavigateBack = { backStack.removeLastOrNull() }
                    )
                }

                entry<GstReportNav> {
                    GstReportScreen(
                        onNavigateBack = { backStack.removeLastOrNull() }
                    )
                }

                entry<PnlNav> {
                    PnlScreen(
                        onNavigateBack = { backStack.removeLastOrNull() }
                    )
                }
            }
        )
    }
}
