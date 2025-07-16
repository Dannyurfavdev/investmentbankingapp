# InvestmentBank 💳📈

**InvestmentBank** is a simulated investment and portfolio banking platform built with Django. It is designed to mimic the core functionalities of a modern investment bank, including user account management, crypto wallet operations, fund transfers, market tracking, and automated ROI systems—all within a secure and KYC-compliant framework.

---

## 🚀 Key Features

- ✅ User registration and authentication
- 🔐 KYC (Know Your Customer) verification workflow
- 📬 Automated email notifications for account updates and activities
- 📊 Real-time ROI (Return on Investment) calculations
- 🌍 Supports deposits in over 25 cryptocurrencies
- 💼 Wallet creation and balance monitoring
- 🔁 Secure fund transfers and receiving mechanisms
- 🧾 Comprehensive transaction history tracking
- 📈 Simulated market movement monitoring

---

## 🛠️ Tech Stack

- **Backend Framework**: Django (Python 3.x)
- **Database**: SQLite (for development; PostgreSQL recommended for production)
- **Frontend**: HTML, CSS, and JavaScript
- **Other Tools**: Django Email Backend, RESTful design principles (optional DRF extension)

---

## 📁 Project Structure

InvestmentBank/
├── InvestmentBank/ # Project settings, URLs, WSGI
├── InvestmentBankapp/ # Core banking logic (models, views, forms, etc.)
├── static/ # Static assets (CSS, JS, images)
├── manage.py # Django entry point
├── requirements.txt # Project dependencies
└── README.md # Project documentation

---

## ⚙️ Getting Started

Follow the steps below to run the project locally:

```bash
# 1. Clone the repository
git clone https://github.com/Dannyurfavdev/InvestmentBank.git
cd InvestmentBank

# 2. (Optional) Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install required packages
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Run the development server
python manage.py runserver



📬 Email Notifications

This project uses Django’s email backend to send automated messages regarding:

Account registration confirmations
KYC approval status
Wallet transactions and balance updates
ROI reports
You can configure your own SMTP settings in settings.py to enable this feature.



🌍 Cryptocurrency Support

InvestmentBank integrates NowPayments to support deposits in over 25 cryptocurrencies. This allows users to simulate real-world crypto deposit flows securely and efficiently.

You can further extend this integration with:

Wallet generation and callback handling
Transaction confirmation tracking
Real-time exchange rate display


🤝 Contributing

Contributions are welcome! Feel free to:

Fork the repository
Create a new branch
Make your changes
Submit a pull request
For significant changes, please open an issue to discuss your ideas first.


📫 Contact

Developed by Daniel Tobenna
GitHub: @Dannyurfavdev


🚧 Future Improvements

✅ Add REST API with Django REST Framework
📱 Build a companion mobile app with React Native
🔐 Integrate two-factor authentication (2FA)
📈 Live charting of portfolio performance