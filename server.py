from flask import Flask, jsonify, request, send_from_directory, send_file
from response import get_search_query_response
import os
from add_articles import main_path

app = Flask(__name__, static_url_path='/', static_folder='./papers_data/pdf/')


@app.route('/hello')
def hello():
    return 'hello'

@app.route("/search_by_query")
def search_by_query():
    return jsonify(get_search_query_response(request.args.get('query')))


@app.route("/search_by_dataset")
def search_by_dataset():
    return jsonify({'response': request.json})


# @app.route('/download/<filename>')
# def download_file(filename):
#     print(os.path.join(main_path, 'pdf', filename + '.pdf'))
#     return send_file(os.path.join(main_path, 'pdf'),
#                                filename + '.pdf', as_attachment=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
