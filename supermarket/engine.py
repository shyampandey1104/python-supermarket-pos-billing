"""High-Speed Retail Supermarket Barcode POS & Billing Engine."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class Product(BaseModel):
    barcode: str
    item_name: str
    mrp: float
    sale_price: float
    gst_rate: float = 18.0  # 0, 5, 12, 18, 28


class CartItem(BaseModel):
    barcode: str
    quantity: int = 1


class SupermarketBillingEngine:
    """Cashier barcode scanning, multi-tender split, and thermal bill generation."""

    def __init__(self):
        self.inventory: Dict[str, Product] = {}

    def add_product(self, product: Product):
        self.inventory[product.barcode] = product

    def checkout_cart(self, items: List[CartItem], coupon_code: Optional[str] = None) -> Dict[str, Any]:
        cart_lines = []
        subtotal = 0.0
        total_mrp = 0.0
        total_tax = 0.0

        for it in items:
            if it.barcode not in self.inventory:
                raise ValueError(f"Barcode {it.barcode} not found in inventory")

            prod = self.inventory[it.barcode]
            line_mrp = prod.mrp * it.quantity
            line_total = prod.sale_price * it.quantity

            # Reverse tax calculation (Price is inclusive of GST)
            tax_factor = prod.gst_rate / (100.0 + prod.gst_rate)
            tax_amount = line_total * tax_factor

            total_mrp += line_mrp
            subtotal += line_total
            total_tax += tax_amount

            cart_lines.append({
                "item_name": prod.item_name,
                "barcode": prod.barcode,
                "qty": it.quantity,
                "price": prod.sale_price,
                "total": line_total,
            })

        discount = 0.0
        if coupon_code == "SAVE10":
            discount = subtotal * 0.10

        final_payable = subtotal - discount

        return {
            "items": cart_lines,
            "total_mrp": round(total_mrp, 2),
            "subtotal": round(subtotal, 2),
            "customer_savings": round((total_mrp - subtotal) + discount, 2),
            "discount": round(discount, 2),
            "included_tax_gst": round(total_tax, 2),
            "final_payable": round(final_payable, 2),
        }
