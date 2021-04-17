from logging.config import dictConfig
from flask import Flask, jsonify, abort, request, redirect
from flasgger import Swagger, swag_from
from geneticlib import get_rank_function, evolve, recreate_function
from settings import LOG_CONFIG

app = Flask(__name__)
Swagger(app)
dictConfig(LOG_CONFIG)


@app.route('/process', methods=['POST'])
@swag_from('docs/api/process.yml')
def process():
    """
    Process endpoint doc
    """
    if request.method == 'POST':
        content = request.json
        app.logger.info(content)
        if content:
            rf = get_rank_function(content["train"])
            winner = evolve(1, 'str', 500, rf, mutation_rate=0.2, breed_ingrate=0.1, p_exp=0.7, p_new=0.1)
            return jsonify({"answer": [winner.evaluate([i]) for i in content["test"]]})
        else:
            abort(400, description="'content' is expected")


@app.route('/function/generate', methods=['POST'])
@swag_from('docs/api/function_generate.yml')
def function_generate():
    """
    Get function endpoint doc
    """
    if request.method == 'POST':
        content = request.json
        app.logger.info(content)
        if content:
            rf = get_rank_function(content["train"])
            winner = evolve(1, 'str', 500, rf, mutation_rate=0.2, breed_ingrate=0.1, p_exp=0.7, p_new=0.1)
            return jsonify({"function": winner.to_dict()})
        else:
            abort(400, description="'content' is expected")


@app.route('/function/process', methods=['POST'])
@swag_from('docs/api/function_process.yml')
def function_process():
    """
    Process a previous generated function
    """
    if request.method == 'POST':
        content = request.json
        app.logger.info(content)
        if content:
            winner = recreate_function(content["function"])
            return jsonify({"answer": [winner.evaluate([i]) for i in content["test"]]})
        else:
            abort(400, description="'content' is expected")


@app.route('/')
def index():
    return redirect('apidocs')


if __name__ == '__main__':
    app.run()
