from logging.config import dictConfig
from flask import Flask, jsonify, abort, request, redirect
from flasgger import Swagger

from geneticlib import getrankfunction, evolve, recreate_function
from settings import LOG_CONFIG

app = Flask(__name__)
swagger = Swagger(app)
dictConfig(LOG_CONFIG)


@app.route('/process', methods=['POST'])
def process():
    """Process endpoint doc
       ---
       definitions:
         Train:
           type: array
           items:
            type: string
           example: [["José Pérez", "José"],["Uncle Bob", "Uncle"]]
         Test:
           type: string
           example: ["Alice Bob", "Robert Martin", "Kent Beck"]
       parameters:
         - name: body
           in: body
           type: Object
           properties:
            train:
                type: array
                items:
                    $ref: "#/definitions/Train"
            test:
                type: array
                items:
                    $ref: "#/definitions/Test"
           required: true
       responses:
         200:
           description: Answer to Test' array
           examples:
             answer: ['string']
       """
    if request.method == 'POST':
        content = request.json
        app.logger.info(content)
        if content:
            rf = getrankfunction(content["train"])
            winner = evolve(1, 'str', 500, rf, mutationrate=0.2, breedingrate=0.1, pexp=0.7, pnew=0.1)
            return jsonify({"answer": [winner.evaluate([i]) for i in content["test"]]})
        else:
            abort(400, description="'content' is expected")


@app.route('/function/generate', methods=['POST'])
def function():
    """Get function endpoint doc
       ---
       definitions:
         Train:
           type: array
           items:
            type: string
           example: [["José Pérez", "José"],["Uncle Bob", "Uncle"]]
         Function:
           type: Object
           items:
            type: string
           example: [["José Pérez", "José"],["Uncle Bob", "Uncle"]]
       parameters:
         - name: body
           in: body
           type: Object
           properties:
            train:
                type: array
                items:
                    $ref: "#/definitions/Train"
           required: true
       responses:
         200:
           description: Function generated with Train array
           examples:
             function: ['string']
       """
    if request.method == 'POST':
        content = request.json
        app.logger.info(content)
        if content:
            rf = getrankfunction(content["train"])
            winner = evolve(1, 'str', 500, rf, mutationrate=0.2, breedingrate=0.1, pexp=0.7, pnew=0.1)
            return jsonify({"function": winner.toDict()})
        else:
            abort(400, description="'content' is expected")

@app.route('/function/proccess', methods=['POST'])
def processFunction():
    """Proccess a previous generated function
       ---
       definitions:
         Function:
           type: Object
           items:
            type: string
           example: {
                  "substring": [
                    0,
                    0,
                    {
                      "index": [
                        0,
                        " "
                      ]
                    }
                  ]
            }
         Test:
           type: string
           example: ["Alice Bob", "Robert Martin", "Kent Beck"]
       parameters:
         - name: body
           in: body
           type: Object
           properties:
            train:
                type: array
                items:
                    $ref: "#/definitions/Train"
            function:
                $ref: "#/definitions/Function"
           required: true
       responses:
         200:
           description: Function generated with Train array
           examples:
             function: ['string']
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
