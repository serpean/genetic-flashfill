from flask import Flask, jsonify, abort, request

app = Flask(__name__)

app.debug = True
app.reloader = True

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method == 'GET':
        return jsonify({'method': 'GET', 'handler': 'process'})

    elif request.method == 'POST':
        content = request.json
        if content:
            return jsonify({'method': 'POST', 'handler': 'process', 'content': content})
        else:
            abort(400, description="'content' is expected")


if __name__ == '__main__':
    app.run()
