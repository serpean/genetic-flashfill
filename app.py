from logging.config import dictConfig
from flask import Flask, jsonify, abort, request, redirect
from flasgger import Swagger

from geneticlib import getrankfunction, evolve
from settings import LOG_CONFIG

app = Flask(__name__)
swagger = Swagger(app)
dictConfig(LOG_CONFIG)


@app.route('/process', methods=['POST'])
def process():
    """Process endpoint doc
       ---
       definitions:
         Example:
           type: array
           items:
            string
         Question:
           type: string
       parameters:
         - name: body
           in: body
           type: Object
           properties:
            examples:
                type: array
                items:
                    $ref: "#/definitions/Example"
            questions:
                type: array
                items:
                    $ref: "#/definitions/Question"
           required: true
       responses:
         200:
           description: Answer to Questions' array
           examples:
             answer: ['string']
       """
    if request.method == 'POST':
        content = request.json
        app.logger.info(content)
        if content:
            rf = getrankfunction(content["examples"])
            winner = evolve(1, 'str', 500, rf, mutationrate=0.2, breedingrate=0.1, pexp=0.7, pnew=0.1)
            return jsonify({"answer": [winner.evaluate([i]) for i in content["questions"]]})
        else:
            abort(400, description="'content' is expected")

@app.route('/')
def index():
    return redirect('apidocs')

if __name__ == '__main__':
    app.run()
