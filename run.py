"""
Application Launcher - Rajby Textile Industries
Runs the Flask application for the Pakistani Textile Employee HR & Payroll System.
"""
import os
import sys
import webbrowser
import threading

# Add backend directory to sys.path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
sys.path.insert(0, backend_dir)

from app import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    url = f"http://127.0.0.1:{port}"
    print("=" * 70)
    print("  * RAJBY TEXTILE INDUSTRIES - KARACHI, PAKISTAN")
    print("  * Industry: Textile & Denim Manufacturing")
    print("  * Currency: Pakistani Rupee (PKR / Rs.)")
    print("  * In-Memory Python OOP Storage (No Database)")
    print(f"  * Dashboard URL: {url}")
    print("=" * 70)
    
    # Automatically open browser on launch
    try:
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    except Exception:
        pass

    # Run Flask server
    app.run(host="127.0.0.1", port=port, debug=False)
