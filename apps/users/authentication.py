from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.utils import timezone
from django.conf import settings
from datetime import timedelta

class expiring_token(TokenAuthentication):

    def expire_detect(self, token):

        time_left_token = timezone.now() - token.created #utilizamos timezone de django ya que este devolvera el tiempo segun al zona hoaria actual
        left_time = timedelta(seconds = settings.TOKEN_TIMEOUT) - time_left_token #utilizamos timedelta ya que nos devolvera en este caso un valor en segundos
        expire_flag = False

        print('14 de expiring'+str(left_time))

        if left_time < timedelta(seconds = 0):

            expire_flag = True
            user = token.user
            token.delete()#eliminamos el token para crearlo nuevamente
            token = self.get_model().objects.create(user=user)

            print('20 auth token refrescado al expirar')
        
        return expire_flag, token

    def authenticate_credentials(self, key):#metodo sobreescrito https://github.com/encode/django-rest-framework/blob/master/rest_framework/authentication.py
        model = self.get_model()
        message = None
        expire_flag = False
        user = None
        token = None

        try:#verificamos que el token recibido este asociado a algun usuario, en caso afirmativo sera retornado, en caso negativo se retornara un mensaje indicando el problema
            token = model.objects.select_related('user').get(key=key)
            user = token.user
            print('37 '+str(user))
        except model.DoesNotExist:
            print('37 ath')
            message = 'Invalid token.'
            expire_flag = True
    
            #raise exceptions.AuthenticationFailed(('Invalid token.'))
        
        if token is not None:
            if not token.user.is_active:
                message = 'User inactive or deleted.'
                
                #raise exceptions.AuthenticationFailed(('User inactive or deleted.'))
            
            expire_flag, token = self.expire_detect(token)
            if expire_flag is True:
                message = 'Token has expired.'
            
                #raise exceptions.AuthenticationFailed(('Token has expired.'))
        print('54 ath')
        print(user)
        print(token)
        return (user, token, expire_flag, message)
    