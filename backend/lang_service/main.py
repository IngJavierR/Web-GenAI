from flask import Flask, request, jsonify
from answer import answer_question
from documents import answer_document_question, inser_files, reset_db
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/qna',methods = ["POST"])
def qnaprocess():
    try:
        input_json = request.get_json(force=True)
        query = input_json["query"]
        print('query', query)
        response = answer_question(query)
        print('response', response)
        return jsonify(response)
    except Exception as error:
        return jsonify({"Status":"Failure --- some error occured"}), 400

@app.route('/doc',methods = ["POST"])
def docprocess():
    try:
        input_json = request.get_json(force=True)
        query = input_json["query"]
        print('query', query)
        response = answer_document_question(query)
        print('response', response['result'])

        return jsonify({"query": query, "result": response['result']}), 200
    except Exception as error:
        return jsonify({"Status":"Failure --- some error occured"}), 400

@app.route('/files',methods = ["POST"])
def upload_files():
    try:
        if 'files[]' not in request.files:
            return jsonify({'error': 'No files part in the request'}), 400

        files = request.files.getlist('files[]')
        if not files:
            return jsonify({'error': 'No files uploaded'}), 400

        inser_files(files)

        return jsonify({}), 200
    except Exception as error:
        return jsonify({"Status":"Failure --- some error occured"}), 400

@app.route('/files',methods = ["DELETE"])
def delete_files():
    try:
        reset_db()

        return jsonify({}), 200
    except Exception as error:
        return jsonify({"Status":"Failure --- some error occured"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8095, debug=False)