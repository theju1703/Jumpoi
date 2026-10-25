from typing import List, Dict, Any

class ERPNextSyncService:
    """
    Simulates the ERPNext Business System synchronization and P&L Generation
    as specified in Step 3 & Step 5 of the Jompoi Architecture Blueprint.
    """

    def __init__(self, items: List[Dict[str, Any]], sales: List[Dict[str, Any]], purchases: List[Dict[str, Any]]):
        self.items = {item.get("item_code"): item for item in items}
        self.sales = sales
        self.purchases = purchases

    def sync_tables_from_cloud(self) -> Dict[str, Any]:
        """
        Simulates ERPNext pulling updated Item, Sales, and Purchase records from BigQuery / Cloud.
        """
        return {
            "synced_items_count": len(self.items),
            "synced_sales_count": len(self.sales),
            "synced_purchases_count": len(self.purchases),
            "status": "SUCCESS"
        }

    def generate_profit_and_loss(self, operating_expenses: float = 0.0) -> Dict[str, Any]:
        """
        Generates the Profit & Loss Statement (Step 5 of Blueprint):
          - Revenue (Total Net Sales)
          - Cost of Goods Sold (COGS) based on Average Purchase Rate
          - Gross Profit = Revenue - COGS
          - Operating Expenses
          - Net Profit = Gross Profit - Operating Expenses
        """
        total_revenue = sum(float(s.get("net_amount", 0.0)) for s in self.sales)

        # Calculate average purchase rate per item
        item_purchase_totals: Dict[str, Dict[str, float]] = {}
        for p in self.purchases:
            code = p.get("item_code")
            qty = float(p.get("quantity", 0.0))
            net = float(p.get("net_amount", 0.0))
            if code not in item_purchase_totals:
                item_purchase_totals[code] = {"qty": 0.0, "net": 0.0}
            item_purchase_totals[code]["qty"] += qty
            item_purchase_totals[code]["net"] += net

        avg_cost_map = {}
        for code, data in item_purchase_totals.items():
            avg_cost_map[code] = data["net"] / data["qty"] if data["qty"] > 0 else 0.0

        # Compute COGS
        total_cogs = 0.0
        item_sales_breakup = []
        for s in self.sales:
            code = s.get("item_code")
            qty = float(s.get("quantity", 0.0))
            revenue = float(s.get("net_amount", 0.0))
            cost_per_unit = avg_cost_map.get(code, 0.0)
            item_cogs = qty * cost_per_unit
            gross_margin = revenue - item_cogs

            total_cogs += item_cogs
            item_sales_breakup.append({
                "item_code": code,
                "item_name": s.get("item_name"),
                "quantity_sold": qty,
                "revenue": round(revenue, 2),
                "cost_per_unit": round(cost_per_unit, 2),
                "cogs": round(item_cogs, 2),
                "gross_profit": round(gross_margin, 2)
            })

        gross_profit = total_revenue - total_cogs
        net_profit = gross_profit - operating_expenses
        margin_pct = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0.0

        return {
            "revenue": round(total_revenue, 2),
            "cost_of_goods_sold": round(total_cogs, 2),
            "gross_profit": round(gross_profit, 2),
            "gross_profit_margin_percent": round(margin_pct, 2),
            "operating_expenses": round(operating_expenses, 2),
            "net_profit": round(net_profit, 2),
            "item_breakup": item_sales_breakup
        }
