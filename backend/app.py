from flask import Flask, jsonify
from flask_cors import CORS
import requests
from datetime import datetime, timedelta
import logging
import time

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COINGECKO_API = "https://api.coingecko.com/api/v3"
CACHE_DURATION = 300  # Cache for 5 minutes

# Simple global cache
cache = {
    'data': None,
    'timestamp': 0
}

@app.route('/api/bitcoin/price', methods=['GET'])
def get_bitcoin_price():
    try:
        current_time = time.time()
        
        # Return cached data if valid
        if cache['data'] and current_time - cache['timestamp'] < CACHE_DURATION:
            logger.info("Returning cached data")
            return jsonify({"success": True, "data": cache['data']})
        
        logger.info("Fetching fresh Bitcoin price data")
        response = requests.get(
            f"{COINGECKO_API}/coins/bitcoin/market_chart",
            params={
                "vs_currency": "usd",
                "days": "7",
                "interval": "daily"
            },
            headers={
                'Accept': 'application/json',
                'User-Agent': 'Bitcoin Price Tracker/1.0'
            },
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            prices = data.get('prices', [])
            formatted_data = [
                {
                    "timestamp": timestamp,
                    "price": price
                }
                for timestamp, price in prices
            ]
            
            # Update cache
            cache['data'] = formatted_data
            cache['timestamp'] = current_time
            
            return jsonify({"success": True, "data": formatted_data})
            
        elif response.status_code == 429:
            logger.warning("Rate limited by CoinGecko API")
            if cache['data']:
                return jsonify({"success": True, "data": cache['data']})
            return jsonify({"success": False, "error": "Rate limited, please try again later"}), 429
            
        else:
            logger.error(f"CoinGecko API error: {response.text}")
            if cache['data']:
                return jsonify({"success": True, "data": cache['data']})
            return jsonify({"success": False, "error": "Failed to fetch data"}), 500
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        if cache['data']:
            return jsonify({"success": True, "data": cache['data']})
        return jsonify({"success": False, "error": "Service temporarily unavailable"}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 