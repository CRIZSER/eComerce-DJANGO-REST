from rest_framework.authentication import get_authorization_header
from apps.users.authentication import expiring_token
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status

class Authentication(object):

    user = None
    expiring_flag = False

    def get_user(self, request):
        
        token = get_authorization_header(request).split() #obtenemos el token presentes en el header de la petición
        
        if token: #si el token esta presente
            try:
                    token = token[1].decode()
                    print('TOKEN: '+str(token))
            except:
                return None
            
            expire_token = expiring_token() #creamos el objeto expiring_token que manejara la logica para verificar si el token enviado ha expirado

            user,token,expire_flag,message = expire_token.authenticate_credentials(token)
            print('26')
            print(user)
            print(token)
            print(expire_flag)
            print(message)
            
            if user is not None and token is not None:
                self.user = user #relizamos esto para tener disponible esta información en las demas aplicaciones, ya que cada una hereda de esta clase, los datos estaran diponibles
                self.expiring_flag = expire_flag #Estos datos necesitan estar disponible para enviarlos hacia el frontend

                if expire_flag is True:
                    return message
                return user
                
        return None

    def dispatch(self, request, *args, **kwargs):#el método que se ejecuta primera en cualquier peticion a django
        user_message = self.get_user(request)
        print('39 ath mixin '+str(self.expiring_flag))
        if user_message is not None:
            if type(user_message) == str:
                reponse = Response({'message':user_message, 'expire': self.expiring_flag}, status=status.HTTP_401_UNAUTHORIZED)
                reponse.accepted_renderer = JSONRenderer()
                reponse.accepted_media_type = 'application/json'
                reponse.renderer_context = {}
                return reponse
            
            if self.expiring_flag is not True:
                return super().dispatch(request, *args, **kwargs)
        
        reponse = Response({'message':'Las credenciades no han sido proveeidas'}, status=status.HTTP_400_BAD_REQUEST)
        reponse.accepted_renderer = JSONRenderer()
        reponse.accepted_media_type = 'application/json'
        reponse.renderer_context = {}
        return reponse
