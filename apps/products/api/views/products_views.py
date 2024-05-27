from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from apps.base.api import GeneralListApiView
from apps.products.api.serializers.product_serializer import ProductSerializer
from apps.products.models import Products
from apps.users.authentication_mixin import Authentication

class ProductViewSet(Authentication, viewsets.ModelViewSet): #como utilizar un viewset 08-08-2023, 20-05-2024 Authentication es importado y usado para que el metodo dispatch sobreecrito verifique la autenticación
    serializer_class = ProductSerializer #Definifmos el serializador y el queryset
    queryset = Products.objects.filter(state = True)

    def get_queryset(self, pk = None):
        product_pk = pk
        queryset = Products.objects.filter(pk=product_pk)# si pongo esto aqui no es necesario ponerlo en el self.get_queryset()

        if pk is None:
            queryset = Products.objects.filter(state = True)
        return queryset

    def list(self, request):
        print('listado')
        product_serializer = self.get_serializer(self.get_queryset(), many = True)
        return Response(product_serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        product_serializer = self.serializer_class(data = request.data)

        if product_serializer.is_valid():
            
            product_serializer.save()#guarda los datos en la base de datos, si se quiere dar cierta forma consultar este link https://www.django-rest-framework.org/tutorial/1-serialization/
            return Response({'message':'Producto creado correctamente'},status=status.HTTP_201_CREATED)
        return Response(product_serializer.errors,status=status.HTTP_400_BAD_REQUEST) #si no cumple con las validaciones, ya sea que le falta un campo o ya exite lo mostrara
    
    def update(self, request, pk = None):
        product = self.get_queryset(pk).first() #first obtiene lo definido en str en models(que es como se ve la instancia en una cadena de texto al ser imprimida), igual que antes o se usa first p [0] para acceder a la instanca contenida en el arreglo

        if product:
            productSerializer = ProductSerializer(product, data=request.data)#creamos la instancia de product y los nuevos datos mediante data = request.data

            if productSerializer.is_valid():
                productSerializer.save()#guarda los datos en la base de datos
                return Response(productSerializer.data, status= status.HTTP_200_OK)
            else:
                return Response(productSerializer.errors, status=status.HTTP_400_BAD_REQUEST) #si no cumple con las validaciones, ya sea que le falta un campo o ya exite lo mostrara
    
    def destroy(self, request, pk = None):
        product = self.get_queryset(pk).first() #en este caso no ocupamos .filter

        if product:
            product.state = False #con esto eliminamos de manera logica, es decir, lo ocultamos al susaurio 
            product.save()
            return Response({'message': 'Producto eliminado correctamente'}, status=status.HTTP_200_OK)
        return Response({'error','No existe el producto'},status=status.HTTP_204_NO_CONTENT)

##########################################################################################################################################################################################
#Lo mas importante
            
class ProductListCreateApiView(generics.ListCreateAPIView):#con listCreateAPIView podemos generar tanto get como post, es una mezcla de ambas, depende de lo que se requiera 
    serializer_class = ProductSerializer

    def get_queryset(self):
        productos = Products.objects.filter(state = True)

        if productos is not None:
            return Products.objects.filter(state = True)

    def post(self, request): #lo mismo que hicimos en apy.py de users, se usa post ya que es un apiview
        product_serializer = self.serializer_class(data = request.data)

        if product_serializer.is_valid():
            
            product_serializer.save()#guarda los datos en la base de datos, si se quiere dar cierta forma consultar este link https://www.django-rest-framework.org/tutorial/1-serialization/
            return Response({'message':'Producto creado correctamente'},status=status.HTTP_201_CREATED)
        return Response(product_serializer.errors,status=status.HTTP_400_BAD_REQUEST) #si no cumple con las validaciones, ya sea que le falta un campo o ya exite lo mostrara

class ProductRetrieveUpdataDestroy(generics.RetrieveUpdateDestroyAPIView): #podemos tanto retornar uno especifico, modificarlo y eliminarlo

    serializer_class = ProductSerializer

    def get_queryset(self):
        product_pk = self.kwargs['pk']
        queryset = Products.objects.filter(pk=product_pk)# si pongo esto aqui no es necesario ponerlo en el self.get_queryset()
        print(queryset)
        print(queryset.first().description)
        return queryset

    def put(self, request, pk = None):#envia la información obtenida para modificar, el pk = none indica que es opcional 
        
        product = self.get_queryset().first() #first obtiene lo definido en str en models(que es como se ve la instancia en una cadena de texto al ser imprimida), igual que antes o se usa first p [0] para acceder a la instanca contenida en el arreglo

        if product:
            productSerializer = ProductSerializer(product, data=request.data)#creamos la instancia de product y los nuevos datos mediante data = request.data

            if productSerializer.is_valid():
                productSerializer.save()#guarda los datos en la base de datos
                return Response(productSerializer.data, status= status.HTTP_200_OK)
            else:
                return Response(productSerializer.errors, status=status.HTTP_400_BAD_REQUEST) #si no cumple con las validaciones, ya sea que le falta un campo o ya exite lo mostrara
        
    

    def delete(self, request, pk = None): #información en el siguiente link https://www.django-rest-framework.org/tutorial/3-class-based-views/
        product = self.get_queryset().first() #en este caso no ocupamos .filter

        if product:
            product.state = False #con esto eliminamos de manera logica, es decir, lo ocultamos al susaurio 
            product.save()
            return Response({'message': 'Producto eliminado correctamente'}, status=status.HTTP_200_OK)
        return Response({'error','No existe el producto'},status=status.HTTP_204_NO_CONTENT)
    
######################################################################################################################################################################################
class ProductListApiView(GeneralListApiView):#hereda de general
    serializer_class = ProductSerializer

class ProductCreateApiView(generics.CreateAPIView):
    serializer_class = ProductSerializer

    #debo utilizar el post ya que no se hace el queryset
    def post(self, request): #lo mismo que hicimos en apy.py de users, se usa post ya que es un apiview
        product_serializer = self.serializer_class(data = request.data)

        if product_serializer.is_valid():
            
            product_serializer.save()#guarda los datos en la base de datos, si se quiere dar cierta forma consultar este link https://www.django-rest-framework.org/tutorial/1-serialization/
            return Response({'message':'Producto creado correctamente'},status=status.HTTP_201_CREATED)
        return Response(product_serializer.errors,status=status.HTTP_400_BAD_REQUEST) #si no cumple con las validaciones, ya sea que le falta un campo o ya exite lo mostrara

class ProductRetriveApiView(generics.RetrieveAPIView): #solo para una cosa, para mas usar listApiView
    serializer_class = ProductSerializer

    def get_queryset(self):
        product_pk = self.kwargs['pk']
        queryset = Products.objects.filter(pk=product_pk)
        return queryset

class ProductDestroyApiView(generics.DestroyAPIView): #eliminación directa, con RetriveDestroy tambien nos entregara los datos y se quitara el mensaje de metodo get no permitido
    serializer_class = ProductSerializer #solo con esto elimina directamente 

    def get_queryset(self):
        product_pk = self.kwargs['pk']
        queryset = Products.objects.filter(pk=product_pk)
        return queryset
    
    def delete(self, request, pk = None): #información en el siguiente link https://www.django-rest-framework.org/tutorial/3-class-based-views/
        product = self.get_queryset().first()#obtenemos la primera instancia del modela, es necesario ya que esta dentro de un arreglo

        if product:
            product.state = False #con esto eliminamos de manera logica, es decir, lo ocultamos al susaurio 
            product.save()
            return Response({'message': 'Producto eliminado correctamente'}, status=status.HTTP_200_OK)
        return Response({'error','No existe el producto'},status=status.HTTP_204_NO_CONTENT)

class ProductUpdateApiView(generics.UpdateAPIView):#patch para obtener y put para actualizar

    serializer_class = ProductSerializer #solo con esto elimina directamente 

    def get_queryset(self):
        product_pk = self.kwargs['pk']
        queryset = Products.objects.filter(pk=product_pk)# si pongo esto aqui no es necesario ponerlo en el self.get_queryset()
        return queryset

    def patch(self, request, pk = None):#obtine la información de la instacia, solo en este caso, usualemnte patch es utilizado para modificar ciertos campos y put en todos
                                        #esto se hizo ya que no se puede hacer que los datos se muestre de otra manera ya qu estamos ocupando las vistas default de django rest
                                        #n resumen simulamos un get
        product = self.get_queryset().first()
        
        if product:
            #productSerializer = ProductSerializer(product)#esto puede ir así 
            productSerializer = self.serializer_class(product) #o ir de esta manera
            return Response(productSerializer.data, status=status.HTTP_200_OK)
        
        return Response({'error','No existe el producto'},status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk = None):#envia la información obtenida para modificar 
        
        product = self.get_queryset().first()

        if product:
            productSerializer = ProductSerializer(product, data=request.data)#creamos la instancia de product y los nuevos datos mediante data = request.data

            if productSerializer.is_valid():
                productSerializer.save()#guarda los datos en la base de datos
                return Response(productSerializer.data, status= status.HTTP_200_OK)
            else:
                return Response(productSerializer.errors, status=status.HTTP_400_BAD_REQUEST) #si no cumple con las validaciones, ya sea que le falta un campo o ya exite lo mostrara

class ProductRetrieveUpdate(generics.RetrieveUpdateAPIView): #podemos tanto retornar como modificar a la vez y realizar las validaciones correspondientes

    serializer_class = ProductSerializer

    def get_queryset(self):
        product_pk = self.kwargs['pk']
        queryset = Products.objects.filter(pk=product_pk)
        return queryset

    #no se definio path ya que no era necesario y ademas de que al usar RetrieveUpdateAPIView ya tenemos un get, por lo tanto no es necesario usar la modificacion de patch a get

    def put(self, request, pk = None):#envia la información obtenida para modificar 
        
        product = self.get_queryset().first()

        if product:
            productSerializer = ProductSerializer(product, data=request.data)#creamos la instancia de product y los nuevos datos mediante data = request.data

            if productSerializer.is_valid():
                productSerializer.save()#guarda los datos en la base de datos
                return Response(productSerializer.data, status= status.HTTP_200_OK)
            else:
                return Response(productSerializer.errors, status=status.HTTP_400_BAD_REQUEST) #si no cumple con las validaciones, ya sea que le falta un campo o ya exite lo mostrara

class ProductRetriveDestroy(generics.RetrieveDestroyAPIView):
    serializer_class = ProductSerializer #solo con esto elimina directamente 

    def get_queryset(self):
        product_pk = self.kwargs['pk']
        queryset = Products.objects.filter(pk=product_pk)
        return queryset
    
    def delete(self, request, pk = None): #información en el siguiente link https://www.django-rest-framework.org/tutorial/3-class-based-views/
        product = self.get_queryset().first()

        if product:
            product.state = False #con esto eliminamos de manera logica, es decir, lo ocultamos al susaurio 
            product.save()
            return Response({'message': 'Producto eliminado correctamente'}, status=status.HTTP_200_OK)
        return Response({'error','No existe el producto'},status=status.HTTP_204_NO_CONTENT)
    

    





 

