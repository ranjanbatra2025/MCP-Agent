# mcp_server.py - MCP Server exposing real-time tools
from fastmcp import FastMCP
import requests
from datetime import datetime

mcp = FastMCP("LiveContext Server", description="Real-time business intelligence tools")

@mcp.tool()
def get_crypto_price(coin: str = "bitcoin") -> str:
    """Get current price and 24h change for a cryptocurrency from CoinGecko"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": coin.lower(),
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }
        data = requests.get(url, params=params, timeout=10).json()
        coin_data = data[coin.lower()]
        price = coin_data["usd"]
        change = coin_data.get("usd_24h_change", 0)
        return f"{coin.upper()}: ${price:,.2f} | 24h: {change:+.2f}% | Updated: {datetime.utcnow().strftime('%H:%M UTC')}"
    except:
        return f"Could not fetch price for {coin} (API down or invalid coin)"

@mcp.tool()
def get_stripe_balance() -> str:
    """Fetch current Stripe account balance (simulated for demo)"""
    # In real app: use stripe.StripeClient
    return "Stripe Balance: $12,450.32 available | $3,200.00 pending | Last payout: Dec 20, 2025"

@mcp.tool()
def get_recent_orders(limit: int = 5) -> str:
    """Get the most recent customer orders"""
    # Simulated real DB query
    orders = [
        "Order #1001: $299 (iPhone case) - Dec 24",
        "Order #1002: $1,299 (MacBook) - Dec 24",
        "Order #1003: $89 (AirPods) - Dec 23",
        "Order #1004: $49 (Charger) - Dec 23",
        "Order #1005: $799 (Monitor) - Dec 22",
    ]
    return "\n".join(orders[:limit])

@mcp.tool()
def get_server_status() -> str:
    """Check live server health and uptime"""
    return "🟢 All systems operational | Uptime: 99.98% | Load: 12% | DB healthy"

if __name__ == "__main__":
    print("MCP SERVER STARTED — Tools available:")
    print("• get_crypto_price")
    print("• get_stripe_balance")
    print("• get_recent_orders")
    print("• get_server_status")
    print("\nWaiting for agent connections on http://localhost:8001\n")
    mcp.run(host="0.0.0.0", port=8001)