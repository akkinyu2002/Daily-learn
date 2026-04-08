from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from html import escape
from pathlib import Path
import uuid

DEFAULT_STORE_NAME = "CITY MART"
DEFAULT_STORE_ADDRESS = "221B Market Street, Kathmandu"
DEFAULT_STORE_PHONE = "+977-9800000000"
DEFAULT_STORE_TAX_ID = "VAT-000000"
TAX_RATE = Decimal("0.13")  # 13% VAT
LINE_WIDTH = 104


@dataclass
class ShopInfo:
    name: str
    address: str
    phone: str
    tax_id: str


@dataclass
class CustomerInfo:
    name: str
    phone: str


@dataclass
class BillItem:
    name: str
    details: str
    unit_price: Decimal
    quantity: int

    @property
    def amount(self) -> Decimal:
        return self.unit_price * self.quantity


def money(value: Decimal) -> str:
    rounded = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"{rounded:.2f}"


def ask_with_default(prompt: str, default: str) -> str:
    value = input(f"{prompt} [{default}]: ").strip()
    return value if value else default


def ask_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter a value.")


def ask_optional(prompt: str, default: str = "") -> str:
    value = input(prompt).strip()
    if value:
        return value
    return default


def ask_decimal(prompt: str) -> Decimal:
    while True:
        raw = input(prompt).strip()
        try:
            value = Decimal(raw)
        except InvalidOperation:
            print("Please enter a valid number.")
            continue

        if value <= 0:
            print("Value must be greater than 0.")
            continue

        return value


def ask_quantity(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return 1
        if raw.isdigit() and int(raw) > 0:
            return int(raw)
        print("Please enter a positive whole number.")


def ask_percentage(prompt: str) -> Decimal:
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return Decimal("0")
        try:
            value = Decimal(raw)
        except InvalidOperation:
            print("Please enter a valid number.")
            continue

        if value < 0 or value > 100:
            print("Please enter a percentage between 0 and 100.")
            continue

        return value


def collect_shop_info() -> ShopInfo:
    print("\nShop details")
    print("-" * 24)
    name = ask_with_default("Shop name", DEFAULT_STORE_NAME)
    address = ask_with_default("Shop address", DEFAULT_STORE_ADDRESS)
    phone = ask_with_default("Shop phone", DEFAULT_STORE_PHONE)
    tax_id = ask_with_default("Tax/VAT number", DEFAULT_STORE_TAX_ID)
    return ShopInfo(name=name, address=address, phone=phone, tax_id=tax_id)


def collect_customer_info() -> CustomerInfo:
    print("\nCustomer details")
    print("-" * 24)
    name = ask_optional("Customer name (default Walk-in Customer): ", "Walk-in Customer")
    phone = ask_optional("Customer phone (optional): ", "-")
    return CustomerInfo(name=name, phone=phone)


def collect_items() -> list[BillItem]:
    print("\nProduct entry")
    print("-" * 24)
    print("Press Enter on product name when finished.\n")

    items: list[BillItem] = []

    while True:
        name = input("Product name: ").strip()
        if name == "":
            if items:
                return items
            print("Add at least one product to create a bill.")
            continue

        details = ask_optional("Product details/specs (optional): ", "-")
        unit_price = ask_decimal("Unit price: ")
        quantity = ask_quantity("Quantity (default 1): ")

        items.append(
            BillItem(
                name=name,
                details=details,
                unit_price=unit_price,
                quantity=quantity,
            )
        )
        print("Item added.\n")


def prepare_bill_values(
    items: list[BillItem], discount_percent: Decimal
) -> tuple[str, datetime, Decimal, Decimal, Decimal, Decimal, Decimal]:
    date_now = datetime.now()
    invoice_no = f"INV-{date_now.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    subtotal = sum((item.amount for item in items), Decimal("0"))
    discount_amount = (
        subtotal * discount_percent / Decimal("100")
    ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    taxable_amount = subtotal - discount_amount
    tax_amount = (taxable_amount * TAX_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    grand_total = taxable_amount + tax_amount

    return (
        invoice_no,
        date_now,
        subtotal,
        discount_amount,
        taxable_amount,
        tax_amount,
        grand_total,
    )


def render_bill(
    shop: ShopInfo,
    customer: CustomerInfo,
    cashier_name: str,
    items: list[BillItem],
    invoice_no: str,
    date_now: datetime,
    discount_percent: Decimal,
    subtotal: Decimal,
    discount_amount: Decimal,
    taxable_amount: Decimal,
    tax_amount: Decimal,
    grand_total: Decimal,
) -> str:
    lines: list[str] = []
    lines.append("=" * LINE_WIDTH)
    lines.append(shop.name.center(LINE_WIDTH))
    lines.append(shop.address.center(LINE_WIDTH))
    lines.append((f"Phone: {shop.phone} | Tax ID: {shop.tax_id}").center(LINE_WIDTH))
    lines.append("=" * LINE_WIDTH)
    lines.append(f"Invoice No      : {invoice_no}")
    lines.append(f"Date            : {date_now.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Customer        : {customer.name}")
    lines.append(f"Customer Phone  : {customer.phone}")
    lines.append(f"Cashier         : {cashier_name}")
    lines.append("-" * LINE_WIDTH)
    lines.append(
        f"{'No':<4}{'Product':<24}{'Details':<26}{'Qty':>8}{'Unit Price':>18}{'Amount':>24}"
    )
    lines.append("-" * LINE_WIDTH)

    for index, item in enumerate(items, start=1):
        product_name = item.name[:24]
        details = item.details[:26]
        lines.append(
            f"{index:<4}{product_name:<24}{details:<26}{item.quantity:>8}{money(item.unit_price):>18}{money(item.amount):>24}"
        )

    lines.append("-" * LINE_WIDTH)
    lines.append(f"{'Subtotal':>80}{money(subtotal):>24}")
    if discount_amount > 0:
        lines.append(
            f"{f'Discount ({money(discount_percent)}%)':>80}{money(discount_amount):>24}"
        )
    lines.append(f"{'Taxable Amount':>80}{money(taxable_amount):>24}")
    lines.append(f"{'VAT (13%)':>80}{money(tax_amount):>24}")
    lines.append(f"{'Grand Total':>80}{money(grand_total):>24}")
    lines.append("=" * LINE_WIDTH)
    lines.append("Thank you for shopping with us!".center(LINE_WIDTH))
    lines.append("=" * LINE_WIDTH)

    return "\n".join(lines)


def render_bill_html(
    shop: ShopInfo,
    customer: CustomerInfo,
    cashier_name: str,
    items: list[BillItem],
    invoice_no: str,
    date_now: datetime,
    discount_percent: Decimal,
    subtotal: Decimal,
    discount_amount: Decimal,
    taxable_amount: Decimal,
    tax_amount: Decimal,
    grand_total: Decimal,
) -> str:
    rows = []
    for index, item in enumerate(items, start=1):
        rows.append(
            (
                "<tr>"
                f"<td>{index}</td>"
                f"<td>{escape(item.name)}</td>"
                f"<td>{escape(item.details)}</td>"
                f"<td class='num'>{item.quantity}</td>"
                f"<td class='num'>{money(item.unit_price)}</td>"
                f"<td class='num'>{money(item.amount)}</td>"
                "</tr>"
            )
        )

    discount_row = ""
    if discount_amount > 0:
        discount_row = (
            "<div class='row'>"
            f"<span>Discount ({money(discount_percent)}%)</span><span>-{money(discount_amount)}</span>"
            "</div>"
        )

    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>Invoice {escape(invoice_no)}</title>
  <style>
    :root {{
      --ink: #232323;
      --muted: #666;
      --line: #d9d9d9;
      --paper: #ffffff;
      --accent: #0f5a4b;
      --panel: #f7faf9;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background: #f1f3f4;
      color: var(--ink);
      font-family: "Segoe UI", Tahoma, sans-serif;
      padding: 28px 14px;
    }}
    .invoice {{
      max-width: 980px;
      margin: 0 auto;
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 10px;
      overflow: hidden;
      box-shadow: 0 14px 30px rgba(0, 0, 0, 0.07);
    }}
    .header {{
      background: var(--panel);
      border-bottom: 2px solid var(--accent);
      padding: 20px;
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      justify-content: space-between;
    }}
    .brand h1 {{
      font-size: 24px;
      margin-bottom: 4px;
    }}
    .brand p,
    .meta p {{
      font-size: 14px;
      color: var(--muted);
      margin-bottom: 3px;
    }}
    .meta p strong {{
      color: #252525;
    }}
    .section {{
      padding: 16px 20px 0;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
      font-size: 14px;
    }}
    th,
    td {{
      border-bottom: 1px solid var(--line);
      padding: 10px 8px;
      text-align: left;
      vertical-align: top;
    }}
    th {{
      background: #fafafa;
      font-weight: 600;
      color: #2a2a2a;
    }}
    .num {{
      text-align: right;
      white-space: nowrap;
    }}
    .totals {{
      max-width: 380px;
      margin: 16px 0 24px auto;
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: hidden;
    }}
    .totals .row {{
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 12px;
      padding: 10px 14px;
      border-bottom: 1px solid var(--line);
      font-size: 14px;
    }}
    .totals .row:last-child {{
      border-bottom: none;
      background: #f0f8f5;
      font-size: 16px;
      font-weight: 700;
    }}
    .footer {{
      border-top: 1px dashed var(--line);
      text-align: center;
      padding: 14px 16px 20px;
      font-size: 13px;
      color: var(--muted);
    }}
    @media print {{
      body {{
        background: #fff;
        padding: 0;
      }}
      .invoice {{
        border: none;
        border-radius: 0;
        box-shadow: none;
      }}
    }}
  </style>
</head>
<body>
  <div class=\"invoice\">
    <div class=\"header\">
      <div class=\"brand\">
        <h1>{escape(shop.name)}</h1>
        <p>{escape(shop.address)}</p>
        <p>Phone: {escape(shop.phone)}</p>
        <p>Tax ID: {escape(shop.tax_id)}</p>
      </div>
      <div class=\"meta\">
        <p><strong>Invoice:</strong> {escape(invoice_no)}</p>
        <p><strong>Date:</strong> {date_now.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Customer:</strong> {escape(customer.name)}</p>
        <p><strong>Customer Phone:</strong> {escape(customer.phone)}</p>
        <p><strong>Cashier:</strong> {escape(cashier_name)}</p>
      </div>
    </div>

    <div class=\"section\">
      <table>
        <thead>
          <tr>
            <th style=\"width: 7%;\">No</th>
            <th style=\"width: 22%;\">Product</th>
            <th style=\"width: 27%;\">Details</th>
            <th style=\"width: 10%;\" class=\"num\">Qty</th>
            <th style=\"width: 16%;\" class=\"num\">Unit Price</th>
            <th style=\"width: 18%;\" class=\"num\">Amount</th>
          </tr>
        </thead>
        <tbody>
          {''.join(rows)}
        </tbody>
      </table>

      <div class=\"totals\">
        <div class=\"row\"><span>Subtotal</span><span>{money(subtotal)}</span></div>
        {discount_row}
        <div class=\"row\"><span>Taxable Amount</span><span>{money(taxable_amount)}</span></div>
        <div class=\"row\"><span>VAT (13%)</span><span>{money(tax_amount)}</span></div>
        <div class=\"row\"><span>Grand Total</span><span>{money(grand_total)}</span></div>
      </div>
    </div>

    <div class=\"footer\">
      Thank you for shopping with us.
    </div>
  </div>
</body>
</html>
"""


def main() -> None:
    print("Automatic Bill Generator")
    print("=" * 24)

    shop = collect_shop_info()
    cashier_name = ask_non_empty("\nShopkeeper/Cashier name: ")
    customer = collect_customer_info()
    discount_percent = ask_percentage("\nOverall discount % (default 0): ")
    items = collect_items()

    (
        invoice_no,
        date_now,
        subtotal,
        discount_amount,
        taxable_amount,
        tax_amount,
        grand_total,
    ) = prepare_bill_values(items, discount_percent)

    bill_text = render_bill(
        shop=shop,
        customer=customer,
        cashier_name=cashier_name,
        items=items,
        invoice_no=invoice_no,
        date_now=date_now,
        discount_percent=discount_percent,
        subtotal=subtotal,
        discount_amount=discount_amount,
        taxable_amount=taxable_amount,
        tax_amount=tax_amount,
        grand_total=grand_total,
    )

    bill_html = render_bill_html(
        shop=shop,
        customer=customer,
        cashier_name=cashier_name,
        items=items,
        invoice_no=invoice_no,
        date_now=date_now,
        discount_percent=discount_percent,
        subtotal=subtotal,
        discount_amount=discount_amount,
        taxable_amount=taxable_amount,
        tax_amount=tax_amount,
        grand_total=grand_total,
    )

    print("\n" + bill_text)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_path = Path(f"bill_{timestamp}.txt")
    html_path = Path(f"bill_{timestamp}.html")

    txt_path.write_text(bill_text, encoding="utf-8")
    html_path.write_text(bill_html, encoding="utf-8")

    print(f"\nText bill saved to: {txt_path.resolve()}")
    print(f"HTML bill saved to: {html_path.resolve()}")
    print("Open the HTML file in a browser and use Print for a paper-style invoice.")


if __name__ == "__main__":
    main()
