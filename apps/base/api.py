from rest_framework import generics

class GeneralListApiView(generics.ListAPIView):
    serializer_class = None

    def get_queryset(self):
        model = self.get_serializer().Meta.model #generalizamos obtenemos el valor definimos en serializer class, accedemos a Meta y model
        return model.objects.filter(state = True) #luego obtenemos los objetos
    