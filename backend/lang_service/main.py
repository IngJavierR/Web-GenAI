from flask import Flask, request, jsonify
from db_answer import answer_db_question
from documents import answer_chatbot_question, insert_files, reset_db
from content_generator import post_content, get_preview_content
from recipe_generator import recipe_generator
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/qna',methods = ["POST"])
def qnaprocess():
    try:
        input_json = request.get_json(force=True)
        query = input_json["query"]
        catalog = input_json["catalog"]
        print('query', query)
        print('catalog', catalog)
        response = answer_db_question(query, catalog)
        print('Response: ', response['result'])
        return jsonify(response)
    except Exception as error:
        print('Error', error)
        return jsonify({"Status":"Failure --- some error occured"}), 400

@app.route('/doc',methods = ["POST"])
def docprocess():
    try:
        input_json = request.get_json(force=True)
        query = input_json["query"]
        print('query', query)
        response = answer_chatbot_question(query)
        print('Response: ', response['result'])

        return jsonify({"query": query, "result": response['result']}), 200
    except Exception as error:
        print('Error', error)
        return jsonify({"Status":"Failure --- some error occured"}), 400

@app.route('/files',methods = ["POST"])
def upload_files():
    try:
        print("Request Files", request.files)
        print("Request", request.files.getlist('files[]'))
        if 'files[]' not in request.files:
            return jsonify({'error': 'No files part in the request'}), 400

        files = request.files.getlist('files[]')
        catalog = request.form.get("catalog")
        if not files:
            return jsonify({'error': 'No files uploaded'}), 400

        insert_files(files, catalog)

        return jsonify({}), 200
    except Exception as error:
        print('Error', error)
        return jsonify({"Status":"Failure --- some error occured"}), 400

@app.route('/files',methods = ["DELETE"])
def delete_files():
    try:
        catalog = request.args.get('catalog')
        print('catalog', catalog)

        reset_db(catalog)

        return jsonify({}), 200
    except Exception as error:
        print('Error', error)
        return jsonify({"Status":"Failure --- some error occured"}), 400

@app.route('/content',methods = ["POST"])
def publish_content():
    try:
        input_json = request.get_json(force=True)
        text = input_json["text"]
        image_name = input_json["image_name"]
        type = input_json["type"]
        print('text', text)
        print('image_name', image_name)
        print('type', type)

        post_content(text, image_name, type)
        return jsonify({}), 200
    except Exception as error:
        print('Error', error)
        return jsonify({"Status":"Failure --- some error occured"}), 400

@app.route('/content',methods = ["GET"])
def get_content():
    try:
        print('Params', request.args)

        query = request.args.get("query")
        image = request.args.get("image").lower() == 'true'
        context = request.args.get("context").lower() == 'true'
        print('query', query)
        print('image', image)
        print('context', context)

        response = get_preview_content(query, include_image=image, include_context=context)

        #print('Response: ', response)
        return jsonify(response), 200
    except Exception as error:
        print('Error', error)
        return jsonify({"Status":"Failure --- some error occured"}), 400


@app.route('/recipe',methods = ["GET"])
def get_recipe():
    try:
        print('Params', request.args)

        query = request.args.get("query")
        print('query', query)

        response = recipe_generator(query)

        print('Response: ', response)
        return jsonify(response), 200
    except Exception as error:
        print('Error', error)
        return jsonify({"Status":"Failure --- some error occured"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8095, debug=False)