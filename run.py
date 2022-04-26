from app import app, views
import os


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # data for production: host="0.0.0.0", port=port, debug=False
    # data for local server: debug=True
    app.run(host="0.0.0.0", port=port, debug=False)

