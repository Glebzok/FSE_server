from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from response import get_search_query_response

app = Flask(__name__, static_url_path='/', static_folder='./papers_data/pdf/')
CORS(app)


@app.route('/hello')
def hello():
    return 'hello'


@app.route("/search_by_query", methods=['GET'])
def search_by_query():
    query = request.args.get('query', default="", type=str)
    try:
        response = get_search_query_response(query)
    except Exception as e:
        abort(400, f"Unknown error ({repr(e)}")
    else:
        return jsonify({'response': response}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0')
