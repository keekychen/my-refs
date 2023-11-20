# 使用 Requests-OAuthlib 获取 OIDC 令牌

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
token_url = 'https://YOUR_PINGFEDERATION_SERVER/oauth/token'

client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(token_url=token_url,
                          client_id=client_id,
                          client_secret=client_secret)

print(token)

#使用 Python-SAML 获取 SAML 令牌
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from flask import Flask, request

app = Flask(__name__)

@app.route('/saml')
def saml():
    req = prepare_flask_request(request)
    auth = OneLogin_Saml2_Auth(req, custom_base_path="/path/to/saml/")
    auth.login()
    return auth.get_attributes()

def prepare_flask_request(request):
    url_data = {
        'https': 'on' if request.scheme == 'https' else 'off',
        'http_host': request.host,
        'script_name': request.path,
        'server_port': request.environ['SERVER_PORT'],
        'get_data': request.args.copy(),
        'post_data': request.form.copy()
    }
    return url_data

if __name__ == "__main__":
    app.run()


#使用 Authlib 获取 OIDC 令牌
from authlib.integrations.requests_client import OAuth2Session

client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
token_url = 'https://YOUR_PINGFEDERATION_SERVER/oauth/token'

client = OAuth2Session(client_id, client_secret)
token = client.fetch_token(token_url)

print(token)


#使用 PySAML2 获取 SAML 令牌


from saml2 import config
from saml2.client import Saml2Client

conf = config.Config()
conf.load_file('/path/to/config/file')
client = Saml2Client(conf)

# For authentication request
(auth_req, relay_state) = client.prepare_for_authenticate()
auth_req_url = client.send(auth_req)

print(auth_req_url)
