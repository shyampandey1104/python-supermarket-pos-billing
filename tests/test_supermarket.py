"""Unit tests for SupermarketBillingEngine."""

from supermarket.engine import SupermarketBillingEngine, Product, CartItem


def test_supermarket_checkout():
    engine = SupermarketBillingEngine()
    engine.add_product(Product(barcode="8901030383742", item_name="Basmati Rice 5kg", mrp=650.0, sale_price=580.0, gst_rate=5.0))
    engine.add_product(Product(barcode="8901234567890", item_name="Sunflower Oil 1L", mrp=180.0, sale_price=160.0, gst_rate=5.0))

    cart = [
        CartItem(barcode="8901030383742", quantity=2),
        CartItem(barcode="8901234567890", quantity=3),
    ]

    bill = engine.checkout_cart(cart, coupon_code="SAVE10")
    assert bill["total_mrp"] == (650.0 * 2 + 180.0 * 3)  # 1300 + 540 = 1840
    assert bill["subtotal"] == (580.0 * 2 + 160.0 * 3)  # 1160 + 480 = 1640
    assert bill["discount"] == 164.0  # 10% of 1640
    assert bill["final_payable"] == (1640.0 - 164.0)
    assert bill["customer_savings"] > 200.0
