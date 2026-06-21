import logging
import re


logging.basicConfig(
    filename="momo_transactions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class InvalidAmountError(Exception):
    """Raised when transaction amount is invalid."""


class InsufficientBalanceError(Exception):
    """Raised when wallet balance is insufficient."""


class Wallet:
    """Represent a MoMo wallet."""

    def __init__(self):
        """Initialize wallet with zero balance."""
        self.balance = 0

    def deposit(self, amount):
        """Deposit money into wallet."""
        if amount <= 0:
            raise InvalidAmountError(
                f"Attempted to process {amount} VND."
            )

        self.balance += amount

        logging.info(
            "Deposit successful: +%s VND. Current Balance: %s",
            amount,
            self.balance
        )

    def transfer(self, phone, amount):
        """Transfer money to another phone number."""
        if amount <= 0:
            raise InvalidAmountError(
                f"Attempted to process {amount} VND."
            )

        if self.balance < amount:
            raise InsufficientBalanceError(
                f"Attempted to transfer {amount} VND "
                f"with balance {self.balance} VND."
            )

        if amount >= 10_000_000:
            logging.warning(
                "High value transaction detected: %s VND to %s",
                amount,
                phone
            )

        self.balance -= amount

        logging.info(
            "Transfer successful: -%s VND to %s. "
            "Current Balance: %s",
            amount,
            phone,
            self.balance
        )

    def get_balance(self):
        """Return current wallet balance."""
        logging.info(
            "Balance checked. Current Balance: %s",
            self.balance
        )
        return self.balance


def format_money(amount):
    """Format currency."""
    return f"{amount:,}"


def validate_phone(phone):
    """Validate Vietnamese phone number."""
    return bool(re.fullmatch(r"\d{10}", phone))


def display_menu():
    """Display menu."""
    print("\n========== VÍ MOMO GIẢ LẬP ==========")
    print("1. Nạp tiền vào ví")
    print("2. Chuyển tiền")
    print("3. Xem số dư hiện tại")
    print("4. Thoát chương trình")
    print("=====================================")


def deposit_money(wallet):
    """Handle deposit feature."""
    print("\n--- NẠP TIỀN VÀO VÍ ---")

    while True:
        try:
            amount = int(input("Nhập số tiền cần nạp: "))

            wallet.deposit(amount)

            print(
                f"\nNạp tiền thành công: "
                f"+{format_money(amount)} VND"
            )

            print(
                f"Số dư hiện tại: "
                f"{format_money(wallet.balance)} VND"
            )

            break

        except ValueError:
            print("Lỗi: Vui lòng nhập số tiền hợp lệ.")

            logging.error(
                "ValueError: Invalid numeric input "
                "for deposit."
            )

        except InvalidAmountError as error:
            print("Lỗi: Số tiền giao dịch phải lớn hơn 0.")

            logging.error(
                "InvalidAmountError: %s",
                error
            )


def transfer_money(wallet):
    """Handle transfer feature."""
    print("\n--- CHUYỂN TIỀN ---")

    phone = input(
        "Nhập số điện thoại người nhận: "
    )

    if not validate_phone(phone):
        print("Số điện thoại không hợp lệ.")
        return

    try:
        amount = int(
            input("Nhập số tiền cần chuyển: ")
        )

        wallet.transfer(phone, amount)

        print(
            f"\nChuyển tiền thành công tới "
            f"số điện thoại {phone}."
        )

        print(
            f"Số tiền đã chuyển: "
            f"{format_money(amount)} VND"
        )

        print(
            f"Số dư còn lại: "
            f"{format_money(wallet.balance)} VND"
        )

    except ValueError:
        print("Lỗi: Vui lòng nhập số tiền hợp lệ.")

        logging.error(
            "ValueError: Invalid numeric input "
            "for transfer."
        )

    except InvalidAmountError as error:
        print("Lỗi: Số tiền giao dịch phải lớn hơn 0.")

        logging.error(
            "InvalidAmountError: %s",
            error
        )

    except InsufficientBalanceError as error:
        print(
            "\nGiao dịch thất bại: "
            "Số dư của bạn không đủ."
        )

        print(
            f"Số dư hiện tại: "
            f"{format_money(wallet.balance)} VND"
        )

        logging.error(
            "InsufficientBalanceError: %s",
            error
        )


def show_balance(wallet):
    """Display current balance."""
    print("\n--- SỐ DƯ VÍ MOMO ---")

    balance = wallet.get_balance()

    print(
        f"Số dư hiện tại: "
        f"{format_money(balance)} VND"
    )


def main():
    """Main program."""
    wallet = Wallet()

    while True:
        display_menu()

        choice = input(
            "\nChọn chức năng (1-4): "
        )

        if choice == "1":
            deposit_money(wallet)

        elif choice == "2":
            transfer_money(wallet)

        elif choice == "3":
            show_balance(wallet)

        elif choice == "4":
            print(
                "\nCảm ơn bạn đã sử dụng dịch vụ."
            )

            logging.info("System shutdown")

            break

        else:
            print("Lựa chọn không hợp lệ.")

main()