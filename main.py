import streamlit as st
import random

# Custom CSS for hacking terminal style
st.markdown(
    """
    <style>
    /* Dark background and green neon text */
    .css-1d391kg {  /* main app container */
        background-color: #000000;
        color: #00ff00;
        font-family: 'Courier New', Courier, monospace;
    }
    /* Title style */
    .css-1v0mbdj h1 {
        color: #00ff00;
        text-shadow: 0 0 10px #0f0, 0 0 20px #0f0;
        font-weight: bold;
        font-family: 'Consolas', Courier, monospace;
    }
    /* Buttons styling */
    div.stButton > button:first-child {
        background-color: black;
        color: #00ff00;
        border: 2px solid #00ff00;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        transition: background-color 0.3s, color 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #00ff00;
        color: black;
        cursor: crosshair;
    }
    /* Upgrade boxes */
    .upgrade-box {
        border: 1px solid #00ff00;
        padding: 10px;
        margin-bottom: 10px;
        font-family: 'Courier New', Courier, monospace;
        background-color: #001100;
        box-shadow: 0 0 8px #00ff00;
        border-radius: 5px;
    }
    /* Stats and info styling */
    .stats {
        font-family: 'Courier New', Courier, monospace;
        font-size: 18px;
        padding: 10px;
        background-color: #001a00;
        border: 1px solid #00ff00;
        box-shadow: 0 0 6px #00ff00;
        margin-bottom: 15px;
        border-radius: 5px;
    }
    /* Horizontal Line styled like terminal prompt */
    hr {
        border: 1px solid #00ff00;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🕵️‍♂️ Hacker Clicker: Crypto vs Firewall 🪙")

# Initialize session state variables once
if "crypto" not in st.session_state:
    st.session_state.crypto = 0
if "passwords" not in st.session_state:
    st.session_state.passwords = 0
if "crypto_per_click" not in st.session_state:
    st.session_state.crypto_per_click = 1
if "password_drop_chance" not in st.session_state:
    st.session_state.password_drop_chance = 0.05

if "upgrades" not in st.session_state:
    st.session_state.upgrades = {
        "crypto_click": 0,
        "password_drop": 0,
        "bypass_firewall": 0,
        "decrypt_algorithms": 0,
        "quantum_decryptor": 0,
        "ai_botnet": 0,
    }

def click_crypto():
    st.session_state.crypto += st.session_state.crypto_per_click
    if random.random() < st.session_state.password_drop_chance:
        st.session_state.passwords += 1
        st.toast("Password Cracked! +1 Password")

def buy_upgrade(name):
    costs = {
        "crypto_click": (50, 0),
        "password_drop": (100, 1),
        "bypass_firewall": (500, 5),
        "decrypt_algorithms": (1200, 8),
        "quantum_decryptor": (3000, 15),
        "ai_botnet": (7000, 30),
    }
    effects = {
        "crypto_click": upgrade_crypto_click,
        "password_drop": upgrade_password_drop,
        "bypass_firewall": upgrade_bypass_firewall,
        "decrypt_algorithms": upgrade_decrypt_algorithms,
        "quantum_decryptor": upgrade_quantum_decryptor,
        "ai_botnet": upgrade_ai_botnet,
    }

    level = st.session_state.upgrades[name]
    cost_crypto, cost_passwords = costs[name]
    cost_crypto = int(cost_crypto * (1.8 ** level))
    cost_passwords = int(cost_passwords * (1.6 ** level)) if cost_passwords > 0 else 0

    if st.session_state.crypto >= cost_crypto and st.session_state.passwords >= cost_passwords:
        st.session_state.crypto -= cost_crypto
        st.session_state.passwords -= cost_passwords
        effects[name]()
        st.session_state.upgrades[name] += 1
        st.success(f"Upgrade bought: {upgrade_names[name]} (Level {st.session_state.upgrades[name]})")
    else:
        st.error(f"Not enough resources! Need {cost_crypto} Crypto and {cost_passwords} Passwords.")

def upgrade_crypto_click():
    st.session_state.crypto_per_click += 1

def upgrade_password_drop():
    st.session_state.password_drop_chance = min(st.session_state.password_drop_chance + 0.02, 0.5)

def upgrade_bypass_firewall():
    st.session_state.crypto_per_click += 10

def upgrade_decrypt_algorithms():
    st.session_state.crypto_per_click += 25
    st.session_state.password_drop_chance = min(st.session_state.password_drop_chance + 0.05, 0.5)

def upgrade_quantum_decryptor():
    st.session_state.crypto_per_click += 70
    st.session_state.password_drop_chance = min(st.session_state.password_drop_chance + 0.07, 0.5)

def upgrade_ai_botnet():
    st.session_state.crypto_per_click += 150
    st.session_state.password_drop_chance = min(st.session_state.password_drop_chance + 0.1, 0.5)

upgrade_names = {
    "crypto_click": "Increase Crypto per Click",
    "password_drop": "Increase Password Drop Rate",
    "bypass_firewall": "Bypass Firewall (+10 Crypto/Click)",
    "decrypt_algorithms": "Decrypt Algorithms (+25 Crypto/Click +5% Password Drop)",
    "quantum_decryptor": "Quantum Decryptor (+70 Crypto/Click +7% Password Drop)",
    "ai_botnet": "AI-powered Botnet (+150 Crypto/Click +10% Password Drop)",
}

# Show player stats with hacking terminal styling
st.markdown(
    f"""
    <div class="stats">
    <pre>
Crypto              : {st.session_state.crypto}
Passwords           : {st.session_state.passwords}
Crypto per Click    : {st.session_state.crypto_per_click}
Password Drop Chance: {int(st.session_state.password_drop_chance*100)}%
    </pre>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<hr>", unsafe_allow_html=True)

# Click button with hacking style
if st.button("🪙 Hack Crypto"):
    click_crypto()

st.markdown("<hr>", unsafe_allow_html=True)

st.header("Upgrades")

# Show upgrades in styled boxes
for key, display_name in upgrade_names.items():
    lvl = st.session_state.upgrades[key]
    base_cost_crypto, base_cost_passwords = {
        "crypto_click": (50, 0),
        "password_drop": (100, 1),
        "bypass_firewall": (500, 5),
        "decrypt_algorithms": (1200, 8),
        "quantum_decryptor": (3000, 15),
        "ai_botnet": (7000, 30),
    }[key]
    cost_crypto = int(base_cost_crypto * (1.8 ** lvl))
    cost_passwords = int(base_cost_passwords * (1.6 ** lvl)) if base_cost_passwords > 0 else 0

    upgrade_box_html = f"""
    <div class="upgrade-box">
    <b>{display_name}</b> (Level {lvl})<br/>
    Cost: {cost_crypto} Crypto{' + ' + str(cost_passwords) + ' Password(s)' if cost_passwords > 0 else ''}
    </div>
    """
    st.markdown(upgrade_box_html, unsafe_allow_html=True)

    cols = st.columns([5,1])
    with cols[1]:
        if st.button(f"Buy", key=f"buy_{key}"):
            buy_upgrade(key)

st.markdown(
    """
    <br><br><center style="color:#00ff00;">Hacking simulation © 2024</center>
    """,
    unsafe_allow_html=True,
)