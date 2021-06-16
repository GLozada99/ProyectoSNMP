import sys
import flask
from waitress import serve
from flask import jsonify as json, request as rq
import LuminariaSNMP.API.functions as fu
from LuminariaSNMP.Daemon.daemon import Daemon


class Server(Daemon):
    def run(self):
        app = flask.Flask(__name__)

        @app.route('/', methods=['GET'])
        def home():
            return "<h1>API de snmpmonitor</h1>"

        @app.route('/interface', methods=['GET'])
        def interfaces():
            return json(fu.get_interfaces())

        @app.route('/SNMP_Interface', methods=['GET'])
        def snmp_interfaces():
            ip = rq.args["ip"]
            community = rq.args["community"]
            return json(fu.get_snmp_interfaces(ip,community))

        @app.route('/rack', methods=['GET'])
        def racks():
            return json(fu.get_racks())

        @app.route('/log', methods=['GET'])
        def log():
            return json(fu.get_log())

        @app.route('/down_interfaces', methods=['GET'])
        def down_interfaces():
            return json(fu.get_down_interfaces())



        @app.route('/insert/interface', methods=['POST'])
        def insert_interface():
            ip =
            interface =
            community =
            oid_num = 
            fu.insert_interface(ip,interface,community,oid_num)         

        @app.route('/insert/rack', methods=['GET'])
        def down_interfaces():
            return json(fu.get_down_interfaces())
        @app.route('/insert/resolve', methods=['GET'])
        def down_interfaces():
            return json(fu.get_down_interfaces())
        serve(app,host='0.0.0.0', port=5000)
        
#app.config["DEBUG"] = True #Must be False if going to be visible
#app.run(host='0.0.0.0',port=5000)

if __name__ == '__main__':
    server = Server('/tmp/server.pid','/tmp/server.date',stdout='/tmp/server.log')
    if sys.argv[1] == 'start':
            server.start()
    elif sys.argv[1] == 'stop':
            server.stop()
    elif sys.argv[1] == 'restart':
            server.restart()
    elif sys.argv[1] == 'debug':
            server.run()
    elif sys.argv[1] == 'running':
            server.is_running()
    else:
        print('No se escogió una opción adecuada')


