from flask import Flask, request, send_from_directory
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    print request.data
    return 'These are some predictions'


if __name__ == "__main__":
    app.run()
