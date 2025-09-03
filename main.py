import streamlit as st
import random

st.title("Hacker Clicker: Crypto vs Firewall")

# Initialize session state only once
if "crypto" not in st.session_state:
    st.session_state.crypto = 0
if "passwords" not in st.session_state:
    st.session_state.passwords = 0
if "crypto_per_click" not in st.session_state:
    st.session_state.crypto_per_click = 1
if "password_drop_chance" not in st.session_state:
    st.session_state.password_drop_chance = 0.05

def click_crypto():
    st.session_state.crypto += st.session_state.crypto_per_click
    # Randomly drop a password
    if random.random() < st.session_state.password_drop_chance:
        st.session_state.passwords += 1
        st.success("Password Cracked! +1 Password")

st.write(f"Crypto: {st.session_state.crypto}")
st.write(f"Passwords: {st.session_state.passwords}")

if st.button("🪙 Hack Crypto"):
    click_crypto()

st.write("---")
st.write("### Upgrades")

def buy_crypto_upgrade():
    cost = 50
    if st.session_state.crypto >= cost:
        st.session_state.crypto -= cost
        st.session_state.crypto_per_click += 1
        st.success("Crypto per click +1")
    else:
        st.error("Not enough Crypto!")

if st.button("Increase Crypto per Click (50 Crypto)"):
    buy_crypto_upgrade()

def buy_password_drop_upgrade():
    cost_crypto = 100
    cost_passwords = 1
    if st.session_state.crypto >= cost_crypto and st.session_state.passwords >= cost_passwords:
        st.session_state.crypto -= cost_crypto
        st.session_state.passwords -= cost_passwords
        st.session_state.password_drop_chance = min(st.session_state.password_drop_chance + 0.02, 0.5)
        st.success("Password drop chance increased!")
    else:
        st.error("Not enough Crypto or Passwords!")

if st.button("Increase Password Drop Rate (100 Crypto, 1 Password)"):
    buy_password_drop_upgrade()