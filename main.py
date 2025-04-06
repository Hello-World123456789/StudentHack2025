import json
import requests
import time
from LLM import extract_investor_info  # Ensure this import matches your actual file/module

# API Configuration
URL = "mts-prism.com"
PORT = 8082
TEAM_API_CODE = "d747eea0e03cea824389395740436f6d"

# API Helper Functions
def send_get_request(path):
    headers = {"X-API-Code": TEAM_API_CODE}
    response = requests.get(f"http://{URL}:{PORT}/{path}", headers=headers)
    if response.status_code != 200:
        return (False, f"Error [CODE {response.status_code}]: {response.text}")
    return (True, response.text)

def send_post_request(path, data=None):
    headers = {"X-API-Code": TEAM_API_CODE, "Content-Type": "application/json"}
    response = requests.post(f"http://{URL}:{PORT}{path}", 
                           data=json.dumps(data), 
                           headers=headers)
    if response.status_code != 200:
        return (False, f"Error [CODE {response.status_code}]: {response.text}")
    return (True, response.text)

def get_context():
    return send_get_request("/request")

def get_my_current_information():
    return send_get_request("/info")

def send_portfolio(weighted_stocks):
    # Handle both integer and float quantities
    data = [{"ticker": ws[0], "quantity": float(ws[1])} if ws[0] == "CASH" 
            else {"ticker": ws[0], "quantity": int(ws[1])} 
            for ws in weighted_stocks]
    return send_post_request("/submit", data=data)

# Main Execution
if __name__ == "__main__":
    # Initial team information check
    success, info = get_my_current_information()
    if not success:
        print(f"Error: {info}")
        exit()
    print(f"Team Info: {info}")

    # Main trading loop
    while True:
        t0 = time.time()
        try:
            # Get market context
            success, context = get_context()
            if not success:
                print(f"Error getting context: {context}")
                time.sleep(10)
                continue

            # Process context
            print("\n=== Raw Context ===")
            print(context)
            t1 = time.time()

            # Extract investor information using LLM
            investor_data = extract_investor_info(context)
            print("\n=== Extracted Investor Data ===")
            print(json.dumps(investor_data, indent=2, ensure_ascii=False))

            # Generate portfolio (IMPLEMENT YOUR STRATEGY HERE)
            # Example format: [("AAPL", 100), ("GOOG", 50), ("CASH", 500.50)]
            weighted_stocks = [
                ("AAPL", 100),      # Replace with your actual stock picks
                ("CASH", 500.50)    # Replace with your cash allocation
            ]

            # Submit portfolio
            success, response = send_portfolio(weighted_stocks)
            print("\n=== Server Response ===")
            print(response)

            # Performance metrics
            t2 = time.time()
            print(f"\nContext processing time: {t1 - t0:.2f}s")
            print(f"Total iteration time: {t2 - t0:.2f}s")

        except Exception as e:
            print(f"\nCritical error in iteration: {str(e)}")
        
        # Wait before next iteration
        print("\nWaiting for next iteration...")
        time.sleep(10)  # Adjust sleep duration as needed