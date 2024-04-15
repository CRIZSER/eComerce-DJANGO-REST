from rest_framework import serializers
from apps.users.models import User as user_model#importamos el modelo para class meta


class UserSerializer(serializers.ModelSerializer): #los serializar convierten una estructura en django a json, serializers.ModelSerializer le parasaremos un modelo con los campos ya establecidos
    class Meta: #generamos el serializer, luego de esto al archivo apy.py
        model = user_model
        fields = '__all__'
    
    def to_representation(self, instance): #ocupamos esta funcion para indicar que mostar, se complementa con apy.py qu indica que campos se seleccionan de la base de datos
        #un metodo alternativo es crear un serializador para manejar distintos casos 
        #esto sirve para listar datos, el crear y actualizar usara lo anterior en fileds
        data = super().to_representation(instance) #obtenmos los datos
        print(instance)
        filtered_data = {
                'id': data.get('id'), #ocupo de esta manera, ya que si se usa instance['id'], da un error al hacer post
                'username': data.get('username'),#esta manera de usar los datos es así ya que en eapy.py estoy restringiendo que datos mellegan, por lo que se forma un diccionario y por lo tanto no se puede acceder a instance.id
                'email': data.get('email'),
                'password': data.get('password')
            }
        return filtered_data
    

    #esto es para dar comportamiento a la hora de guardar o mofificar al llamar al metodo .save()
    def create(self, validated_data):
        user = user_model.objects.create(**validated_data) #creamos una instancia de user_model
        user.set_password(validated_data['password']) #con este logramos que al crear el usuario la contraseña se encripte
        user.save()
       
        return user

    def update(self, instance, validated_data):
        
        #Update and return an existing `Snippet` instance, given the validated data.
        updateUser = super().update(instance, validated_data) #retornamos el model actualizado
        updateUser.set_password(validated_data['password'])#encriptamos la contraseña
        updateUser.save() #guardamos cambios
        return updateUser
    
        #lo anterior tambien se puede hacer de la manera de abajo 
        
        """instance.set_password = validated_data.get('password', instance.password)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance"""

class TestUserSerializar(serializers.Serializer):#con serializers.Serializer indicamos que nosotros le daremos los campos
    name = serializers.CharField(max_length=200) #con los campos y sus restricciones seran usados en .valid()
    email = serializers.EmailField()
    requires_context = True

    #estas validaciones se crean por defecto si se usa un modelo, como en la clase anterior, sin embargo, igual se puede crear para sobre escribirlos
    def validate_name(self,value): #dada esta menra se usar un serializer
        if 'develop' in value:
            raise serializers.ValidationError('Error, no se permite un usuario con ese nombre')
        
        return value

    def validate_email(self,value):
        if value == '':
            raise serializers.ValidationError('Error, no se permite el campo vacio')
        
        if self.context['name'] in value: #para usar el context, este se debe pasar al crear la instancia del serializador
            raise serializers.ValidationError('Error, El email ingresado no puede contener el nombre de usuario')
        
        return value

    def validate(self,data): #dada esta menra se usar un serializer
        #if data['name'] in data['email']:
         #   raise serializers.ValidationError('Error, no se un email con el nombre de usuario')
        return(data)
    


    #lo siguiente se encuentra en esta documentación https://www.django-rest-framework.org/community/3.0-announcement/#the-create-and-update-methods
    def create(self, validated_data):
        print(validated_data)
        user = user_model.objects.create(**validated_data)#los ** para acceder a toda la información, primero definimos el modelo, accedemos a los objetos y creamos uno nuevo
        return user
    
    def update(self, instance, validated_data):
        print(instance)
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.save() #este .save es del modelo
        return instance
    

    #documentación de .save() aqui https://www.django-rest-framework.org/api-guide/serializers/#passing-additional-attributes-to-save
    def save(self): #para sobreescribir save debemos tener en cuenta ciertas cosas, 1 el .save() en apy es el save del serializador, el cual es el actual. Mientras que en update es del modelo
        #2 tenemos que tener en cuenta que queremos, ya que si no necesitamos crear una instancia del serializador save() nos ayudara a obtener la imforamación ingrsada
        email = self.validated_data['email'] 
        message = self.validated_data['name']
        print('tuki') #al sobreescribir el metodo save ya no identifica automaticamente si se trata de un create o update

    #para probar estos metodos crear una nueva view en urls o descomentar las lineas 27 a 36 de apy.py (test_data), o cambiar los UserSerializer por testUser