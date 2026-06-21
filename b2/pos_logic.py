import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

DRINK_MENU = {
    "P1": {
        "name": "Phin Sữa Đá",
        "price": 35000
    },
    "F1": {
        "name": "Freeze Trà Xanh",
        "price": 55000
    },
    "T1": {
        "name": "Trà Sen Vàng",
        "price": 45000
    }
}


class ItemNotFoundError(Exception):
    """Raised when drink code does not exist."""


class InvalidQuantityError(Exception):
    """Raised when quantity is invalid."""


def format_money(amount):
    """Format money."""
    return f"{amount:,}"


def view_menu():
    """Display drink menu."""
    print("\n--- THỰC ĐƠN HIGHLANDS COFFEE ---")

    for code, item in DRINK_MENU.items():
        print(
            f"[{code}] - {item['name']} - "
            f"{format_money(item['price'])} VNĐ"
        )


def add_to_order(current_order, drink_code, quantity):
    """Add item to order."""

    drink_code = drink_code.strip().upper()

    if drink_code not in DRINK_MENU:
        raise ItemNotFoundError(drink_code)

    if quantity <= 0:
        raise InvalidQuantityError(quantity)

    current_order.append({
        "code": drink_code,
        "quantity": quantity
    })

    logging.info(
        "Added %s of %s to order",
        quantity,
        drink_code
    )


def calculate_total(current_order):
    """Calculate total amount."""

    total = 0

    for item in current_order:
        code = item["code"]
        quantity = item["quantity"]

        total += (
            DRINK_MENU[code]["price"]
            * quantity
        )

    return total


def display_order(current_order):
    """Display order details."""

    if not current_order:
        print(
            "Giỏ hàng trống, vui lòng "
            "chọn món (Chức năng 2)."
        )
        return

    print("\n--- GIỎ HÀNG HIỆN TẠI ---")
    print(
        "Mã SP | Tên đồ uống | "
        "Đơn giá | Số lượng | Thành tiền"
    )

    print("-" * 64)

    total = 0

    for item in current_order:
        code = item["code"]
        quantity = item["quantity"]

        name = DRINK_MENU[code]["name"]
        price = DRINK_MENU[code]["price"]

        subtotal = price * quantity

        total += subtotal

        print(
            f"{code:<5} | "
            f"{name:<18} | "
            f"{format_money(price):<8} | "
            f"{quantity:<8} | "
            f"{format_money(subtotal)} VNĐ"
        )

    print("-" * 64)

    print(
        f"Tổng tiền cần thanh toán: "
        f"{format_money(total)} VNĐ"
    )


def checkout(current_order):
    """Process checkout."""

    if not current_order:
        print(
            "Giỏ hàng trống, vui lòng "
            "chọn món (Chức năng 2)."
        )
        return

    total = calculate_total(current_order)

    print("\n--- THANH TOÁN ---")
    print(
        f"Tổng tiền cần thanh toán: "
        f"{format_money(total)} VNĐ"
    )

    confirm = input(
        f"Xác nhận thanh toán "
        f"{format_money(total)} VNĐ? (y/n): "
    ).lower()

    if confirm == "y":
        print("Thanh toán thành công.")

        logging.info(
            "Checkout successful"
        )

        current_order.clear()

        print(
            "Giỏ hàng đã được làm trống."
        )

    elif confirm == "n":
        print(
            "Đã hủy thao tác thanh toán. "
            "Quay lại menu chính."
        )

    else:
        print(
            "Lựa chọn không hợp lệ. "
            "Thanh toán đã bị hủy."
        )