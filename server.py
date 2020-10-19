from flask import Flask, jsonify, request, send_from_directory
from response import get_search_query_response
import os
from add_articles import main_path

app = Flask(__name__)


@app.route("/search_by_query")
def search_by_query():
    return jsonify(get_search_query_response(request.json['query']))


@app.route("/search_by_dataset")
def search_by_dataset():
    return jsonify({'response': request.json})


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(os.path.join(main_path, 'pdf'),
                               filename + '.pdf', as_attachment=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
