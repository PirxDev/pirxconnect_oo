import webbrowser
import oauth2 as oauth
import configuracion
try:
    from urlparse2 import parse_qsl
except:
    from cgi import parse_qsl


class Obtenertoken(object):

    def __init__(self):

        self.REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
        self.ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
        self.AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
        self.SIGNIN_URL = 'https://api.twitter.com/oauth/authenticate'

        consumer_key = configuracion.ConfigSectionMap("Datos")['consumer_key']
        consumer_secret = configuracion.ConfigSectionMap("Datos")['consumer_secret']
        self.get_access_token(consumer_key, consumer_secret)

    def get_access_token(self, consumer_key, consumer_secret):
        signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
        oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
        oauth_client = oauth.Client(oauth_consumer)

        print('Requesting temp token from Twitter')

        resp, content = oauth_client.request(self.REQUEST_TOKEN_URL, 'POST', body="oauth_callback=oob")

        if resp['status'] != '200':
            print('Invalid respond from Twitter requesting temp token: %s' % resp['status'])
        else:
            request_token = dict(self.parse_qsl(content))
            url = '%s?oauth_token=%s' % (self.AUTHORIZATION_URL, request_token['oauth_token'])

            print('')
            print('I will try to start a browser to visit the following Twitter page')
            print('if a browser will not start, copy the URL to your browser')
            print('and retrieve the pincode to be used')
            print('in the next step to obtaining an Authentication Token:')
            print('')
            print(url)
            print('')

            webbrowser.open(url)
            pincode = input('Pincode? ')

            token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
            token.set_verifier(pincode)

            print('')
            print('Generating and signing request for an access token')
            print('')

            oauth_client = oauth.Client(oauth_consumer, token)
            resp, content = oauth_client.request(self.ACCESS_TOKEN_URL, method='POST', body='oauth_callback=oob&oauth_verifier=%s' % pincode)
            access_token = dict(self.parse_qsl(content))

            if resp['status'] != '200':
                print('The request for a Token did not succeed: %s' % resp['status'])
                print(access_token)
            else:
                configuracion.grabar("Datos", "access_token_key", access_token['oauth_token'])
                configuracion.grabar("Datos", "access_token_secret", access_token['oauth_token_secret'])
                configuracion.grabar("Estado", "configurado", 1)
