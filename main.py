import tkinter as tk
from tkinter import messagebox
import random

class HackerClickerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hacker Clicker: Crypto vs Firewall")

        # Currency & game state
        self.crypto = 0                # Main currency
        self.passwords = 0             # Rare currency
        self.crypto_per_click = 1      # Crypto gained per click
        self.password_drop_chance = 0.05  # 5% chance to get a password on click

        # Setup UI
        self.setup_ui()

        # Define available upgrades with their prices and effects
        self.upgrades = {
            "Increase Crypto per Click": {
                "cost_crypto": 50,
                "cost_passwords": 0,
                "effect": self.upgrade_crypto_per_click,
                "description": "+1 Crypto per click"
            },
            "Increase Password Drop Rate": {
                "cost_crypto": 100,
                "cost_passwords": 1,
                "effect": self.upgrade_password_drop_rate,
                "description": "+2% Password drop chance"
            },
            "Bypass Firewall": {
                "cost_crypto": 500,
                "cost_passwords": 5,
                "effect": self.bypass_firewall,
                "description": "Increase Crypto per click by 10"
            }
        }

        # Add upgrades buttons
        self.create_upgrades_ui()

    def setup_ui(self):
        # Title
        title = tk.Label(self.root, text="Hacker Clicker: Crypto vs Firewall", font=("Consolas", 24, "bold"))
        title.pack(pady=20)

        # Display Crypto
        self.crypto_label = tk.Label(self.root, text=f"Crypto: {self.crypto}", font=("Consolas", 20))
        self.crypto_label.pack(pady=5)

        # Display Passwords
        self.password_label = tk.Label(self.root, text=f"Passwords: {self.passwords}", font=("Consolas", 16))
        self.password_label.pack(pady=5)

        # Crypto Click Button (simulate a crypto symbol)
        self.crypto_button = tk.Button(self.root, text="🪙 Hack Crypto", font=("Consolas", 30), width=15, height=2, command=self.click_crypto)
        self.crypto_button.pack(pady=25)

        # Info label
        self.info_label = tk.Label(self.root, text="Click the crypto symbol to hack coins! Rare Passwords drop randomly.", font=("Consolas", 12))
        self.info_label.pack(pady=10)

        # Separator
        separator = tk.Frame(self.root,height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill=tk.X, padx=5, pady=10)

        # Upgrades label
        upgrade_title = tk.Label(self.root, text="Upgrades", font=("Consolas", 20, "bold"))
        upgrade_title.pack(pady=10)

    def create_upgrades_ui(self):
        self.upgrade_frames = {}

        for name, info in self.upgrades.items():
            frame = tk.Frame(self.root)
            frame.pack(pady=5, fill=tk.X, padx=20)

            # Upgrade description
            desc_text = f"{name}: {info['description']} (Cost: {info['cost_crypto']} Crypto"
            if info['cost_passwords'] > 0:
                desc_text += f", {info['cost_passwords']} Password{'s' if info['cost_passwords'] >1 else ''}"
            desc_text += ")"
            desc = tk.Label(frame, text=desc_text, font=("Consolas", 12))
            desc.pack(side=tk.LEFT)

            # Upgrade button
            btn = tk.Button(frame, text="Buy", command=lambda n=name: self.buy_upgrade(n))
            btn.pack(side=tk.RIGHT)

            self.upgrade_frames[name] = (frame, btn)

    def click_crypto(self):
        # Increase crypto by current amount
        self.crypto += self.crypto_per_click
        self.crypto_label.config(text=f"Crypto: {self.crypto}")

        # Possibly get a password
        if random.random() < self.password_drop_chance:
            self.passwords += 1
            self.password_label.config(text=f"Passwords: {self.passwords}")
            self.flash_info("Password Cracked! +1 Password")

    def buy_upgrade(self, upgrade_name):
        upgrade = self.upgrades[upgrade_name]
        cost_crypto = upgrade["cost_crypto"]
        cost_passwords = upgrade["cost_passwords"]

        # Check if player has enough currency
        if self.crypto >= cost_crypto and self.passwords >= cost_passwords:
            # Deduct costs
            self.crypto -= cost_crypto
            self.passwords -= cost_passwords
            self.crypto_label.config(text=f"Crypto: {self.crypto}")
            self.password_label.config(text=f"Passwords: {self.passwords}")

            # Apply upgrade effect
            upgrade["effect"]()

            # Increase upgrade cost for replayability
            upgrade["cost_crypto"] = int(upgrade["cost_crypto"] * 1.5)
            if upgrade["cost_passwords"] > 0:
                upgrade["cost_passwords"] = int(upgrade["cost_passwords"] * 1.3) or 1  # min 1

            # Update upgrade description with new cost
            frame, btn = self.upgrade_frames[upgrade_name]
            desc_text = f"{upgrade_name}: {upgrade['description']} (Cost: {upgrade['cost_crypto']} Crypto"
            if upgrade['cost_passwords'] > 0:
                desc_text += f", {upgrade['cost_passwords']} Password{'s' if upgrade['cost_passwords'] >1 else ''}"
            desc_text += ")"

            for widget in frame.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(text=desc_text)
                    break

            self.flash_info(f"Upgrade Purchased: {upgrade_name}")
        else:
            messagebox.showwarning("Insufficient Resources", "You don't have enough Crypto or Passwords to buy this upgrade.")

    def upgrade_crypto_per_click(self):
        self.crypto_per_click += 1
        self.flash_info(f"Crypto per click increased to {self.crypto_per_click}!")

    def upgrade_password_drop_rate(self):
        # Cap the drop chance at 50%
        if self.password_drop_chance < 0.5:
            self.password_drop_chance += 0.02
            self.password_drop_chance = min(self.password_drop_chance, 0.5)
            self.flash_info(f"Password drop chance increased to {int(self.password_drop_chance*100)}%!")
        else:
            messagebox.showinfo("Max Upgrade", "Password drop chance is already at maximum!")

    def bypass_firewall(self):
        self.crypto_per_click += 10
        self.flash_info("Firewall bypassed! Crypto per click +10!")

    def flash_info(self, message):
        self.info_label.config(text=message)
        self.root.after(3000, lambda: self.info_label.config(text="Click the crypto symbol to hack coins! Rare Passwords drop randomly."))


if __name__ == "__main__":
    root = tk.Tk()
    game = HackerClickerGame(root)
    root.geometry("600x600")
    root.mainloop()