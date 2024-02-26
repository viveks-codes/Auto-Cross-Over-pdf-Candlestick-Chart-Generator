from flask import Flask, request, jsonify
import os
import yfinance as yf
import mplfinance as mpf
from datetime import datetime, timedelta
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import traceback

app = Flask(__name__)

def plot_candlestick_to_pdf(symbol, start_date, end_date, interval='1h', emas=(10, 50, 100), pdf_pages=None):
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date, interval=interval)

        # Check if data is empty for the symbol
        if stock_data.empty:
            symbol_with_ns = symbol + '.NS'
            stock_data_ns = yf.download(symbol_with_ns, start=start_date, end=end_date, interval=interval)

            if not stock_data_ns.empty:
                stock_data = stock_data_ns

        # Calculate EMAs based on user input
        for ema in emas:
            stock_data[f'EMA{ema}'] = stock_data['Close'].ewm(span=ema, adjust=False).mean()

        # Plotting candlestick chart
        title = f'\n{symbol} {start_date} to {end_date} ({interval} interval),\n {", ".join([f"{ema} EMA" for ema in emas])}'
        fig, axlist = mpf.plot(stock_data, type='candle', style='yahoo', title=title,
                               ylabel='Price', ylabel_lower='Volume', mav=emas, tight_layout=False, returnfig=True)

        # Add legends for EMA lines
        for ax in axlist:
            ax.legend(['Close'] + [f'EMA{ema}' for ema in emas])

        # Save the current candlestick chart plot to the PDF file
        pdf_pages.savefig(fig)
        plt.close(fig)

    except Exception as e:
        traceback.print_exc()

def parse_emas_input(input_string):
    if not input_string.strip():  # If the input is empty, use default values
        return [10, 50, 100]

    return list(map(int, input_string.split()))

def parse_date_input(date_string):
    try:
        return pd.to_datetime(date_string).strftime('%Y-%m-%d')
    except ValueError:
        return default_date

def generate_candlestick_chart(remail):
    output_file = 'candlestick_charts_all_symbols5.pdf'
    pdf_pages_candlestick = PdfPages(output_file)

    csv_files = [f for f in os.listdir() if f.endswith('.csv')]
    selected_index = 0
    csv_file = csv_files[selected_index]

    default_start_date = parse_date_input((datetime.now() - timedelta(days=150)).strftime('%Y-%m-%d'))
    start_date = parse_date_input(default_start_date)
    end_date = parse_date_input(datetime.now().strftime('%Y-%m-%d'))
    interval_options = ["1d", "2m", "5m", "15m", "30m", "60m", "90m", "1m", "1h", "5d", "1wk", "1mo", "3mo"]
    interval = interval_options[0]

    emas_input = '10 50 100'
    emas = parse_emas_input(emas_input)

    symbols_df = pd.read_csv(csv_file)
    symbols = symbols_df['Symbol'].tolist()

    for i, symbol in enumerate(symbols):
        plot_candlestick_to_pdf(symbol, start_date=start_date, end_date=end_date,
                                interval=interval, emas=emas, pdf_pages=pdf_pages_candlestick)
    
    # Close the PDF file for candlestick charts
    pdf_pages_candlestick.close()
    recipients = [remail]  # List of recipient email addresses
    for recipient_email in recipients:
        send_email(attachment_file=output_file, recipient_email=recipient_email)

def send_email(attachment_file,recipient_email):
    email_address = "ai20.vivek.patel@gmail.com"
    app_password = "kqql idxz noog lxpt"

    recipient_email =  recipient_email # Recipient's email address

    message = MIMEMultipart()
    message['From'] = email_address
    message['To'] = recipient_email
    message['Subject'] = "Daily Candlestick Chart Report,Have a nice day!"

    body = "Please find attached the daily candlestick chart report."
    message.attach(MIMEText(body, 'plain'))

    with open(attachment_file, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {attachment_file}')
    message.attach(part)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(email_address, app_password)
        server.sendmail(email_address, recipient_email, message.as_string())




@app.route('/')
def index():
    return 'Welcome to Candlestick Chart Generator!'

@app.route('/generate_candlestick_chart', methods=['GET'])
def generate_candlestick_chart_route():
    email = request.args.get('email')
    if email:
        generate_candlestick_chart(remail=email)
        return jsonify({'message': 'Candlestick chart generated and email sent successfully.'}), 200
    else:
        return jsonify({'error': 'Email parameter missing.'}), 400

if __name__ == "__main__":
    app.run(debug=True, threaded=True, host='0.0.0.0', port=os.environ.get('PORT', 5000), use_reloader=False)
