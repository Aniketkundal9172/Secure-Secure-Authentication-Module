# Streamlit Secure Authentication System

A simple yet secure authentication system built using Streamlit. This project features user registration, secure login with hashed passwords, 2-Factor Authentication (2FA) using Google Authenticator, and a basic dashboard-style website after successful login.

> This project is currently under development. There may be bugs or incomplete features which will be improved in upcoming updates.

## Features

- User Registration with password hashing using bcrypt
- Secure Login with password + OTP-based 2FA using pyotp
- TOTP Support for Google Authenticator with QR code integration
- Account Lockout after 3 failed login attempts (5-minute timeout)
- Dashboard UI: Home, Profile, Settings, Logout (with persistent login via session)
- Custom HTML/CSS styling for clean and user-friendly interface
- Simple JSON-based user database (users.json)

## Demo

[Screenshot Coming Soon]

## Project Structure

```
project/
│
├── users.json                 # JSON file to store registered users and login metadata
├── app.py                     # Main Streamlit app
└── README.md                  # Project documentation (you’re here)
```

## Requirements

- Python 3.8+
- Streamlit
- bcrypt
- pyotp
- qrcode
- Pillow (for QR image generation)

Install them using:

```
pip install streamlit bcrypt pyotp qrcode pillow
```

## How to Run

1. Clone the repository:

```
git clone https://github.com/yourusername/streamlit-auth-system.git
cd streamlit-auth-system
```

2. Run the app:

```
streamlit run app.py
```

3. Open in your browser (usually at http://localhost:8501)

## Using Google Authenticator

After registration, a QR Code will be displayed. Scan this using the Google Authenticator App (or any TOTP app).

Use the OTP shown in your app to log in securely.

## Planned Features

- Email verification
- Password reset functionality
- Admin dashboard
- Dark mode toggle
- Persistent session with cookies or DB

## Developers

- Reg. No: 12313061  
- Reg. No: 12316660  
- Reg. No: 12315690

## Known Issues

- No email/password recovery yet
- Currently using a local JSON file instead of a real database
- Basic UI — more frontend features to come

Feel free to report any issues or contribute!

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Note

This is a student project still in active development. Expect bugs and experimental features. Stay tuned for improvements.