import os
import stripe
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set Stripe API key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "gbp",
                        "product_data": {"name": "Accounting Services"},
                        "unit_amount": int(float(request.json["amount"]) * 100),
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url="https://yourwebsite.com/success",
            cancel_url="https://yourwebsite.com/cancel",
        )
        return jsonify({"url": session.url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
