import flask
import LuminariaSNMP.API.functions as funct

app = flask.Flask(__name__)
app.config["DEBUG"] = True
json = flask.jsonify

@app.route('/', methods=['GET'])
def home():
    return "<h1>API de snmpmonitor</h1>"

@app.route('/Interfaces', methods=['GET'])
def interfaces():
    return json(funct.get_interfaces())

app.run()