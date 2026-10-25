from typing import List, Dict, Any

class GSTReconciliationEngine:
    """
    Simulates the GST Government Portal API and computes Input Tax Credit (ITC)
    reconciliation as outlined in Step 4 & 5 of the Jompoi Architecture Blueprint.
    """

    def __init__(self, sales_records: List[Dict[str, Any]], purchase_records: List[Dict[str, Any]]):
        self.sales = sales_records
        self.purchases = purchase_records

    def calculate_output_gst(self) -> Dict[str, Any]:
        """Calculates total output GST collected from sales invoices."""
        total_net = 0.0
        total_gst = 0.0
        total_gross = 0.0
        document_wise = []
        rate_wise: Dict[float, Dict[str, float]] = {}

        for inv in self.sales:
            net = float(inv.get("net_amount", 0.0))
            gst = float(inv.get("gst_amount", 0.0))
            gross = float(inv.get("total_amount", net + gst))
            rate = float(inv.get("gst_percent", 0.0))

            total_net += net
            total_gst += gst
            total_gross += gross

            document_wise.append({
                "invoice_no": inv.get("invoice_no"),
                "invoice_date": inv.get("invoice_date"),
                "customer_name": inv.get("customer_name") or (inv.get("customer", {}).get("name") if isinstance(inv.get("customer"), dict) else ""),
                "item_name": inv.get("item_name"),
                "gst_percent": rate,
                "net_amount": round(net, 2),
                "gst_amount": round(gst, 2),
                "total_amount": round(gross, 2)
            })

            if rate not in rate_wise:
                rate_wise[rate] = {"taxable_value": 0.0, "tax_amount": 0.0}
            rate_wise[rate]["taxable_value"] += net
            rate_wise[rate]["tax_amount"] += gst

        return {
            "total_taxable_sales": round(total_net, 2),
            "total_output_gst": round(total_gst, 2),
            "total_gross_sales": round(total_gross, 2),
            "rate_wise_breakup": {
                f"{k}%": {
                    "taxable_value": round(v["taxable_value"], 2),
                    "tax_amount": round(v["tax_amount"], 2)
                } for k, v in rate_wise.items()
            },
            "documents": document_wise
        }

    def calculate_input_gst(self) -> Dict[str, Any]:
        """Calculates total input GST paid on vendor purchases (ITC)."""
        total_net = 0.0
        total_gst = 0.0
        total_gross = 0.0
        supplier_wise: Dict[str, Dict[str, float]] = {}
        document_wise = []

        for bill in self.purchases:
            net = float(bill.get("net_amount", 0.0))
            gst = float(bill.get("gst_amount", 0.0))
            gross = float(bill.get("total_amount", net + gst))
            vendor = bill.get("vendor", "Unknown Vendor")

            total_net += net
            total_gst += gst
            total_gross += gross

            document_wise.append({
                "invoice_no": bill.get("invoice_no"),
                "invoice_date": bill.get("invoice_date"),
                "vendor": vendor,
                "item_name": bill.get("item_name"),
                "net_amount": round(net, 2),
                "gst_amount": round(gst, 2),
                "total_amount": round(gross, 2),
                "itc_eligibility": "ELIGIBLE"
            })

            if vendor not in supplier_wise:
                supplier_wise[vendor] = {"taxable_value": 0.0, "itc_amount": 0.0}
            supplier_wise[vendor]["taxable_value"] += net
            supplier_wise[vendor]["itc_amount"] += gst

        return {
            "total_taxable_purchases": round(total_net, 2),
            "total_input_gst": round(total_gst, 2),
            "total_gross_purchases": round(total_gross, 2),
            "supplier_wise_breakup": {
                k: {
                    "taxable_value": round(v["taxable_value"], 2),
                    "itc_amount": round(v["itc_amount"], 2)
                } for k, v in supplier_wise.items()
            },
            "documents": document_wise
        }

    def generate_gst_payment_report(self) -> Dict[str, Any]:
        """
        Reconciles Output GST against Input Tax Credit (ITC) to determine net payable tax.
        Matches Box 5 of client architecture blueprint.
        """
        out_summary = self.calculate_output_gst()
        in_summary = self.calculate_input_gst()

        output_tax = out_summary["total_output_gst"]
        input_tax = in_summary["total_input_gst"]

        # ITC utilization cannot exceed output tax
        itc_utilized = min(output_tax, input_tax)
        net_payable = max(0.0, output_tax - input_tax)
        excess_itc_carry_forward = max(0.0, input_tax - output_tax)

        return {
            "output_gst_sales": output_tax,
            "input_gst_purchases": input_tax,
            "itc_eligible": input_tax,
            "itc_utilized": round(itc_utilized, 2),
            "net_gst_payable_in_cash": round(net_payable, 2),
            "excess_itc_carried_forward": round(excess_itc_carry_forward, 2),
            "filing_status": "READY_TO_FILE" if net_payable >= 0 else "NO_LIABILITY",
            "output_details": out_summary,
            "input_details": in_summary
        }
