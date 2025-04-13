import streamlit as st
import bcrypt
import pyotp
import json
import os
import qrcode
from io import BytesIO
import base64
import time

# Global DB
user_db_path = "users.json"
LOCKOUT_TIME = 300  # 5 min

# Load DB
def load_database():
    if os.path.exists(user_db_path):
        with open(user_db_path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

# Save DB
def save_database(data):
    with open(user_db_path, "w") as f:
        json.dump(data, f)

# Generate QR Code Image
def generate_qr_code(data):
    qr = qrcode.make(data)
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

# Password hashing
def hash_password(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def verify_password(stored, entered):
    return bcrypt.checkpw(entered.encode(), stored.encode())

# UI Styling
st.markdown("""
    <style>
    .title { text-align: center; font-size: 32px; font-weight: bold; margin-top: 20px; }
    .centered { text-align: center; }
    .error { color: red; }
    .success { color: green; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🔐  Secure Authentication Module System</div>", unsafe_allow_html=True)

# Choose mode
mode = st.sidebar.selectbox("Choose Action", ["Register", "Login"])

with st.sidebar:
    st.markdown("""
        <div style='text-align: left; font-size: 16px; font-weight: bold;'>
            Reg. No: 12313061<br>
            Reg. No: 12316660<br>
            Reg. No: 12315690
        </div>
    """, unsafe_allow_html=True)

db = load_database()

# REGISTER
if mode == "Register":
    st.subheader("📝 Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if username in db:
            st.error("Username already exists!")
        else:
            secret = pyotp.random_base32()
            hashed_pwd = hash_password(password)
            db[username] = {
                "password": hashed_pwd,
                "totp_secret": secret,
                "failed_attempts": 0,
                "lockout_time": 0
            }
            save_database(db)

            uri = pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name="StreamlitAuthApp")
            qr_img = generate_qr_code(uri)

            st.success("Registered successfully!")
            st.markdown("### 📱 Scan QR Code in Google Authenticator:")
            st.markdown(f"<div class='centered'><img src='{qr_img}' width='200'></div>", unsafe_allow_html=True)
            st.code(f"Secret Key: {secret}", language='bash')

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""
if "page" not in st.session_state:
    st.session_state.page = "Home"

# LOGIN
elif mode == "Login":
    if not st.session_state.logged_in:
        st.subheader("🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        otp = st.text_input("Enter OTP from Google Authenticator")

        if st.button("Login"):
            if username not in db:
                st.error("User not found.")
            else:
                user = db[username]
                current_time = time.time()
                if user["failed_attempts"] >= 3 and current_time < user["lockout_time"]:
                    remaining = int(user["lockout_time"] - current_time)
                    st.error(f"Account locked. Try again in {remaining} seconds.")
                elif verify_password(user["password"], password):
                    totp = pyotp.TOTP(user["totp_secret"])
                    if totp.verify(otp):
                        st.success("✅ Login successful!")
                        user["failed_attempts"] = 0
                        st.session_state.logged_in = True
                        st.session_state.current_user = username
                    else:
                        st.error("❌ Invalid OTP.")
                        user["failed_attempts"] += 1
                else:
                    st.error("❌ Incorrect password.")
                    user["failed_attempts"] += 1

                if user["failed_attempts"] >= 3:
                    user["lockout_time"] = time.time() + LOCKOUT_TIME
                db[username] = user
                save_database(db)
    else:
        # Main Website Interface
        st.sidebar.title(f"👋 Welcome, {st.session_state.current_user}")
        menu = st.sidebar.radio("📁 Navigate", ["Home", "Profile", "Settings", "Logout"])

        st.title("🌐 My Secure Website")
        st.markdown("""
    <style>
    .welcome {
        background-color: black;
        padding: 20px;
        border-radius: 10px;
        font-family: 'Arial', sans-serif;
        text-align: center;
    }
    .btn {
        padding: 10px 20px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 16px;
    }
    </style>

    <div class="welcome">
        <h2>🌟 Welcome to Your Website</h2>
        <p>Thankyou for visiting</p>
        
    </div>
""", unsafe_allow_html=True)


        if menu == "Home":
            st.header("🏠 Home")
            st.write("Welcome to your dashboard!")
            st.write("📊 View analytics, updates, and more here.")

        elif menu == "Profile":
            st.header("👤 Profile")
            st.write(f"Username: `{st.session_state.current_user}`")
            st.write("Email: user@example.com (dummy)")
            st.write("Joined: Just now 😉")

        elif menu == "Settings":
            st.header("⚙️ Settings")
            st.write("Feature coming soon!")

        elif menu == "Logout":
            st.session_state.logged_in = False
            st.session_state.current_user = ""
            st.experimental_rerun()
