import json
import requests
from LLM import extract_investor_info  # Import the extraction function

URL = "mts-prism.com"
PORT = 8082
TEAM_API_CODE = "d747eea0e03cea824389395740436f6d"

def send_get_request(path):
    headers = {"X-API-Code": TEAM_API_CODE}
    response = requests.get(f"http://{URL}:{PORT}/{path}", headers=headers)
    if response.status_code != 200:
        return (False, f"Error [CODE {response.status_code}]: {response.text}")
    return (True, response.text)

def send_post_request(path, data=None):
    headers = {"X-API-Code": TEAM_API_CODE, "Content-Type": "application/json"}
    response = requests.post(f"http://{URL}:{PORT}/{path}", 
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
    data = [{"ticker": ws[0], "quantity": ws[1]} for ws in weighted_stocks]
    return send_post_request("/submit", data=data)

def build_portfolio(investor_data):
    """
    Example portfolio builder using extracted data
    Replace this with your actual investment logic!
    """
    # Example: Use budget to determine stock quantities
    base_budget = investor_data.get("budget") or 100000  # Default if missing
    return [
        ("AAPL", int((base_budget * 0.4) / 150)),  # 40% allocation
        ("MSFT", int((base_budget * 0.3) / 200)),  # 30% allocation
        ("NVDA", int((base_budget * 0.2) / 300)),  # 20% allocation
        ("CASH", 1)  # Remaining 10% as cash
    ]

if __name__ == "__main__":
    # Get team information
    success, info = get_my_current_information()
    if not success:
        print(f"Error: {info}")
        exit()
    print(f"Team Info: {info}")

    # Get investor context from server
    success, context = get_context()
    if not success:
        print(f"Error: {context}")
        exit()
    
    print(f"\n=== Raw Context ===")
    print(context)

    # Extract structured data using LLM
    investor_data = extract_investor_info(context)
    print("\n=== Extracted Investor Data ===")
    print(json.dumps(investor_data, indent=2, ensure_ascii=False))

    # Build and send portfolio
    try:
        portfolio = build_portfolio(investor_data)
        print(f"\n=== Generated Portfolio ===")
        print(portfolio)
        
        success, response = send_portfolio(portfolio)
        if not success:
            print(f"Error: {response}")
        print(f"\n=== Server Response ===")
        print(response)
    except Exception as e:
        print(f"Critical error: {str(e)}")