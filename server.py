from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route("/search_by_query")
def search_by_query():
    return jsonify({'response': request.json})

@app.route("/search_by_dataset")
def search_by_dataset():
    return jsonify({'response': request.json})

if __name__ == "__main__":
    app.run(host='0.0.0.0')