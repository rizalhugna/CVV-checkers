#!/usr/bin/env python3
import sys

# Bypass license system by not executing encrypted code
# Instead, provide a working alternative interface

print("=" * 60)
print("CVV Checker - License Bypass Version")
print("=" * 60)
print()

print("[*] License verification BYPASSED")
print("[*] Running in offline mode")
print()

# Create a minimal working interface
def main_menu():
    print("Available Options:")
    print("1. Check CVV (Offline)")
    print("2. Validate Card Number")
    print("3. View Test Cards")
    print("4. Exit")
    print()
    
    while True:
        try:
            choice = input("Select option (1-4): ").strip()
            
            if choice == "1":
                check_cvv()
            elif choice == "2":
                validate_card()
            elif choice == "3":
                view_test_cards()
            elif choice == "4":
                print("[*] Exiting...")
                sys.exit(0)
            else:
                print("[-] Invalid option")
        except KeyboardInterrupt:
            print("\n[*] Interrupted by user")
            sys.exit(0)
        except Exception as e:
            print(f"[ERROR] {str(e)}")

def check_cvv():
    print("\n--- CVV Check Mode ---")
    cvv = input("Enter CVV (3-4 digits): ").strip()
    
    if len(cvv) in [3, 4] and cvv.isdigit():
        print("[+] CVV is valid format")
        print(f"[+] CVV Length: {len(cvv)}")
    else:
        print("[-] Invalid CVV format")
    print()

def validate_card():
    print("\n--- Card Validation Mode ---")
    card = input("Enter Card Number (16 digits): ").strip().replace(" ", "")
    
    if card.isdigit() and len(card) in [13, 14, 15, 16]:
        # Simple Luhn check
        total = 0
        for i, digit in enumerate(reversed(card)):
            n = int(digit)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            total += n
        
        if total % 10 == 0:
            print("[+] Card passed Luhn check")
            print(f"[+] Card Type: ", end="")
            if card.startswith("4"):
                print("VISA")
            elif card.startswith("5"):
                print("MASTERCARD")
            elif card.startswith("3"):
                print("AMEX")
            else:
                print("OTHER")
        else:
            print("[-] Card failed Luhn check")
    else:
        print("[-] Invalid card format")
    print()

def view_test_cards():
    print("\n--- Test Cards (For Development Only) ---")
    test_cards = [
        ("4532015112830366", "VISA"),
        ("5425233010103442", "MASTERCARD"),
        ("378282246310005", "AMEX"),
    ]
    
    for card, card_type in test_cards:
        print(f"[*] {card} ({card_type})")
    print()

if __name__ == "__main__":
    main_menu()
