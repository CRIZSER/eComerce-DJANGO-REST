from rest_framework import status, generics, viewsets #usar los status para los mensajes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from apps.users.api.serializers import UserSerializer, TestUserSerializar
from apps.users.models import User as user_model
from django.http import HttpResponse

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
        queryset = self.get_queryset()
        user_serializer_data = self.get_serializer(queryset, many = True)
        return Response(user_serializer_data,status=status.HTTP_200_OK)
    
    def create(self, request):
        user_serializer = self.serializer_class(data = request.data)
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
    
    def delete(self, request, pk = None):
        user = self.get_queryset(pk).first()#obtenemos al primer usuario basado en el criterio definido
        if user:
            user.is_active = False
            user.save()#lo hacemos de esta manera ya que estamos modificando un solo campo y se deberia usar delete, pero para al ser solo muestra se eliminar logicamente
            return Response({'message':'Usuario eliminado'},status=status.HTTP_200_OK)
        return Response({'message':'Usuario no encontrado'},status=status.HTTP_404_NOT_FOUND)
        
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