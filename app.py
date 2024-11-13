# app.py
from flask import Flask
from config import app
from api.api import api_blueprint

# Daftarkan Blueprint
app.register_blueprint(api_blueprint, url_prefix='/api')

# if __name__ == '__main__':
#     app.run(debug=True)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
