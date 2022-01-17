
# ** EPS ** API - Comunicação Externa
# ** EPS ** <190821> - moneynow
# exemplo local: http://127.0.0.1:5000/vmservice/api/v1/private?moneynow=1

from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from metodos import moneynow_requisicao

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("SuperSecretPwd"),
    "padilha": generate_password_hash("12345")
}

# verifica a senha
@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    return False

# Classe Middleware
class PrefixMiddleware(object):
    # class for URL sorting
    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        # in this line I'm doing a replace of the word vmoneyapiservice which is my app name in IIS to ensure proper URL redirect
        if environ['PATH_INFO'].lower().replace('/vmservice', '').startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'].lower().replace('/vmservice', '')[len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["Esta URL não pertence ao aplicativo.".encode()]

# prefixo de rota
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/api/v1')

# metodo de entrada login
@app.route("/private", methods=['POST'])
@auth.login_required
def login():
    status, json_data = processa_requisicao()
    if not status:
        return jsonify({'requisição falhou parâmetro inválido :)': json_data})
    else:
        return jsonify(json_data)   


# processa chamada da requisicao
def processa_requisicao():
    
    parametros_aceitaveis = ["1", "2"]
    
    # recuperando dados de json
    data = request.get_json()

    # valor de parametro (KEY)
    params = request.args.get("moneynow") 

    # testa o parametro de chegada    
    if params in parametros_aceitaveis:
        json_data = moneynow_requisicao(data)
        return True, json_data
    else:
        return False, params


if __name__ == '__main__':
    app.run(debug=True)


# classe privada , requer login de autenticacao
# class PrivateResource(Resource):
#     @auth.login_required
#     def get(self):
#         status, json_data = processa_requisicao()
#         if not status:
#             return jsonify({'requisição falhou parâmetro inválido :)': json_data})
#         else:
#             return jsonify(json_data)            

#api.add_resource(PrivateResource, '/private')