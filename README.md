# Demo 📈
https://stonkstream-j6qrukmayby8hkxr3dwch3.streamlit.app/
https://stnkyf-hgnjuscxk54j4xb4scwhuu.streamlit.app/

# 📈 Candlestick Chart Generator

A powerful Streamlit web application that generates and emails candlestick charts with EMA indicators for multiple stock symbols. Built with Python, yfinance, and mplfinance.

## 🌟 Features

- Generate candlestick charts for multiple stock symbols
- Automatic calculation and plotting of EMA (Exponential Moving Averages)
- Support for both regular and NSE (National Stock Exchange) symbols
- Customizable time intervals and date ranges
- Automatic PDF generation with multiple charts
- Email delivery system for generated reports
- Interactive Streamlit web interface

## 🛠️ Prerequisites

```bash
pip install streamlit yfinance mplfinance pandas matplotlib schedule
```

## 📋 Configuration

1. Create a CSV file with stock symbols in the following format:
```csv
Symbol
AAPL
GOOGL
MSFT
```

2. Update email configuration in `send_email` function:
```python
email_address = "your-email@gmail.com"
app_password = "your-app-password"  # Gmail App Password
```

## 🚀 Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Access the application through the URL with email parameter:
```
http://localhost:8501/?email=recipient@example.com
```

## 📊 Chart Features

- Candlestick patterns
- Volume indicators
- Multiple EMA lines (default: 10, 50, 100)
- Customizable time intervals:
  - 1d, 2m, 5m, 15m, 30m, 60m, 90m
  - 1h, 5d, 1wk, 1mo, 3mo

## 🔧 Technical Details

- Default time range: Last 150 days to present
- Supported file formats: CSV for symbol list, PDF for chart output
- Email delivery: Uses SMTP with Gmail
- Error handling for missing data and invalid symbols

## 📝 Code Structure

- `main()`: Entry point and Streamlit interface
- `generate_candlestick_chart()`: Core chart generation logic
- `plot_candlestick_to_pdf()`: Individual chart plotting
- `send_email()`: Email delivery system
- `parse_emas_input()`: EMA configuration parser
- `parse_date_input()`: Date input validator

## ⚠️ Important Notes

1. Ensure proper Gmail app password is configured for email functionality
2. Place CSV file with stock symbols in the same directory
3. Check internet connectivity for yfinance data download
4. Allow sufficient time for chart generation with multiple symbols

## 🔒 Security

- Remove hardcoded credentials before deploying
- Use environment variables for sensitive information
- Implement proper error handling for email delivery

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers.

---
Made with ❤️ by [Your Name]
