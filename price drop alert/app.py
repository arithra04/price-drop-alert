import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage

# Get user inputs for product URL, target price, and email ID
product_url = input("Enter the Amazon product URL: ")
target_price = float(input("Enter your target price (₹): "))
email_id = input("Enter your Gmail ID: ")

# Hardcoded App Password (Generated from Google Account)
email_pass = ""  # 🔴 Replace with your actual app password

# Function to send email alert
def alert_system(product, link):
    msg = EmailMessage()
    msg['Subject'] = 'Price Drop Alert!'
    msg['From'] = email_id
    msg['To'] = ''  # Replace with the recipient's email
    msg.set_content(f'Hey, price of "{product}" has dropped below ₹{target_price}!\nCheck it out: {link}')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_id, email_pass)
        smtp.send_message(msg)
        print("✅ Email alert sent successfully!")

# Headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip',
    'DNT': '1',  # Do Not Track
    'Connection': 'close'
}

# Function to check product price
def check_price():
    page = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Extract product title
    title = soup.find(id='productTitle').get_text(strip=True)

    # Extract price
    price_tag = soup.find("span", class_="a-price-whole")

    if price_tag:
        price_text = price_tag.get_text(strip=True).replace(",", "")
        try:
            price = float(price_text)
            print(f"🔍 Product: {title}\n💰 Current Price: ₹{price}")

            # If price is below target, send an alert
            if price <= target_price:
                alert_system(title, product_url)
            else:
                print("🚀 Price is still high. No alert sent.")
        except ValueError:
            print("⚠️ Error: Could not convert price to float.")
    else:
        print("❌ Price not found on the page. Please check the URL.")

# Run the price check
check_price()
