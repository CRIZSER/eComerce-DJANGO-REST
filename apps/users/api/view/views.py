from rest_framework import status, generics, viewsets #usar los status para los mensajes
#from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.views import Token
from rest_framework.authtoken.models import Token as token_model
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from apps.users.api.serializers.serializers import UserSerializer, UserTokenSerializer
from apps.users.models import User as user_model
from django.contrib.sessions.models import Session
from datetime import datetime
#from django.http import HttpResponse


# views.py se remplaza por el archivo apy.py

""""class UserAPIView(APIView):

    def get(self,request):
        userAll = user_model.objects.all() #obtenemos todos los usuarios
        user_serializer = UserSerializer(userAll, many = True) # many = True los serealizamos todos, convertimos a json todos los elementos del listado
        return Response(user_serializer.data) #obtenemos la primera vista de rest que obtine todos los usuarios 
        #luego de esto a urls.py""" #antes del decorador se utilizaba esto como clase en lugar de funcion 
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = user_model.objects.all()

    def list(self, request):
        print("listado")
        queryset = self.get_queryset()
        users_serializer = self.get_serializer(queryset, many = True)
        return Response(users_serializer.data,status=status.HTTP_200_OK)
    
    def create(self, request):
        user_serializer = self.serializer_class(data = request.data)
        print(user_serializer)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'message':'Usuario creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk = None):
        user = self.get_queryset(pk).first()#obtenemos al primer usuario basado en el criterio definido
        if user:
            user_serializer = self.serializer_class(user, data = request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response({'message':'Datos actualizados'},status=status.HTTP_200_OK)
            else:
                return Response({'message':'Datos invalidos'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'Usuario no encontrado'},status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk = None):
        user = self.get_queryset(pk).first()#obtenemos al primer usuario basado en el criterio definido
        if user:
            user.is_active = False
            user.save()#lo hacemos de esta manera ya que estamos modificando un solo campo y se deberia usar delete, pero para al ser solo muestra se eliminar logicamente
            return Response({'message':'Usuario eliminado'},status=status.HTTP_200_OK)
        return Response({'message':'Usuario no encontrado'},status=status.HTTP_404_NOT_FOUND)

class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data = request.data, context = {request:'request'})#serializer hace referencia a la clase ObtainAuthToken que posee el serializador
                                                #verificaremos que los datos enviados esten presentes
        print(login_serializer)
        if(login_serializer.is_valid()):
           
            user = login_serializer.validated_data['user']
            if(user.is_active):
                token, created = Token.objects.get_or_create(user=user) # https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
                userTokenSerializer = UserTokenSerializer(user)
                if created: 
                    return Response({
                        'token': token.key,
                        'email': userTokenSerializer.data['email'],
                        'username': userTokenSerializer.data['username'],
                        'message': 'Login exitoso'
                    }, status=status.HTTP_201_CREATED)
                else:
                    self.delete_sesions(user)
                    token.delete()#eliminamos el token para crearlo nuevamente, esto aplicara cada vez que inicie sesión 
                    token = Token.objects.create(user=user)
                    return Response({
                        'token': token.key,
                        'email': userTokenSerializer.data['email'],
                        'username': userTokenSerializer.data['username'],
                        'message': 'Login exitoso'
                    }, status=status.HTTP_201_CREATED)
                
                    #metodo alternativo
                    #token.delete()#eliminamos el token para crearlo nuevamente
                    #Response ({'message':'Sesion ya iniciada'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response ({'message':'Usuario no habilitado'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response ({'message':'Verifique sus credenciales de identificación'}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete_sesions(self, user):
        all_sessions = Session.objects.filter(expire_date__gte = datetime.now())#cerramos todas las sesiones activas
        if all_sessions.exists():
            for sesion in all_sessions:#recorremos cada sesion activa
                sesion_data = sesion.get_decoded()#decodificamos las sesiones activas
                if user.id == int(sesion_data.get('_auth_user_id')):#todas las sesiones referentes al usuario actual se borran
                    sesion.delete()

class Logout(APIView):

    def post(self, request, *args, **kwargs):
        try:
            token = request.POST.get('token')#obtenemos el token actual del usuario como una variable en una pretición / resquest es un objeto que extiende a httpRequest, lo que nos permite realizar las solicitudes
            token_exists = Token.objects.filter(key = token).first()#obtebemos la primera conincidencia
        
            if token_exists:
                print(token_exists)
                self.delete_sesions(token_exists.user)
                token_exists.delete()#eliminamos el token
                return Response ({'message':'Sesión cerrada correctamente'}, status=status.HTTP_200_OK)
            else:
                return Response ({'message':'No se encontro un usuario con las credenciales proporcionadas'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response ({'message':'No se encontro el token en la petición'}, status=status.HTTP_409_CONFLICT)

    def delete_sesions(self, user):
        all_sessions = Session.objects.filter(expire_date__gte = datetime.now())#cerramos todas las sesiones activas
        if all_sessions.exists():
            for sesion in all_sessions:#recorremos cada sesion activa
                sesion_data = sesion.get_decoded()#decodificamos las sesiones activas
                if user.id == int(sesion_data.get('_auth_user_id')):#todas las sesiones referentes al usuario actual se borran
                    sesion.delete()

class UserToken(APIView):

    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        try:
            user = user_model.objects.filter(username=username).first()
            token = token_model.objects.filter(user = user).first()
            return Response({'token':token.key})
        except:
            return Response({'message': 'Invalid username'}, status=status.HTTP_400_BAD_REQUEST)


        
########################################################################################################################################################################################## 

@api_view(['GET','POST']) #Agregamos el decorador para las funciones, con post permite enviar daros 
def userAPIView(request): 

    #def get(self,request):antes del uso de decorador
    if request.method == 'GET':
        userAll = user_model.objects.all().values('id','username','email','password') #obtenemos todos los usuarios
        user_serializer = UserSerializer(userAll, many = True) # many = True los serealizamos todos, convertimos a json todos los elementos del listado

        """test_data = {
            'name':'testtir',
            'email':'testSerializer@gmail.com'
        }
        test_user=TestUserSerializar(data=test_data, context = test_data)
        if test_user.is_valid():
            test_user.save()
            print(test_user.data)
        else:
            print(test_user.errors) #cada error dado en las validaciones las guarda en el diccionario de errors"""


        return Response(user_serializer.data, status= status.HTTP_200_OK) #obtenemos la primera vista de rest que obtiene todos los usuarios 
        #luego de esto a urls.py
    elif request.method == 'POST':
        user_serializer = UserSerializer(data=request.data, context = request.data) #compara si el json enviado es igual al modelo establecido
        
        if user_serializer.is_valid():
            
            user_serializer.save()#guarda los datos en la base de datos, si se quiere dar cierta forma consultar este link https://www.django-rest-framework.org/tutorial/1-serialization/
            return Response(user_serializer.data,status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors,status=status.HTTP_400_BAD_REQUEST) #si no cumple con las validaciones, ya sea que le falta un campo o ya exite lo mostrara
    
@api_view(['GET','PUT', 'DELETE']) #put para actualizar los datos, esto ayuda a la interfaz 
def userDetail(request,pk=None):

    try: #de esta manera es más eficiente. esto esta en la documentación https://www.django-rest-framework.org/tutorial/1-serialization/
        userSelected = user_model.objects.get(id=pk)
    except user_model.DoesNotExist:
        return Response({'message':'Usuario No encontrado, por favor verifique que ingreso el id correcto'},status=status.HTTP_400_BAD_REQUEST) #httpResponde manda un html, Response usa la consola del framework


    if request.method == 'GET':
        #userSelected = user_model.objects.filter(id = pk).first() #obtenemos el primero que cumpla con la condicion, con el try except ya no es necesario esto, ya que en primera instancia lo obtenemos
        user_serializer = UserSerializer(userSelected) #no indicamos many, ya que por defecto retorna 1
        return Response(user_serializer.data, status= status.HTTP_200_OK)
    
    elif request.method == 'PUT':

        #userSelected = user_model.objects.filter(id = pk).first()#con el try except ya no es necesario esto, ya que en primera instancia lo obtenemos
        user_serializer = UserSerializer(userSelected,data = request.data, context = request.data) #al entregarle userSelected le estamos indicando que actualize la información

        if user_serializer.is_valid():
            
            user_serializer.save()#guarda los datos en la base de datos
            return Response(user_serializer.data, status= status.HTTP_200_OK)
        
        return Response(user_serializer.errors) #si no cumple con las validaciones, ya sea que le falta un campo o ya exite lo mostrara
    
    elif request.method == 'DELETE':
        userSelected.delete()
        return Response({'message':'Usuario eliminado correctamente'},status=status.HTTP_200_OK)