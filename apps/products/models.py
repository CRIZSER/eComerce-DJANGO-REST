from django.db import models
from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel

# Create your models here.

class MeasureUnit(BaseModel):#heredamos de base model

    #campos especificos
    description = models.CharField('Descripcion', max_length=50, blank = False, null = False, unique = True)
    """historical = HistoricalRecords()#esto esta en base model

    @property #esto funciona como un metodo que se utiliza de manera automatica al instanticar el objeto y puede ser accedido como atributo
    def _histoy_user(self):
        return self.change_by


    @_histoy_user.setter #funciona como el anterior pero de manera complementaria, ya que se ejecutara al momento de que queramos asignar un calo a la propiedad
    def _histoy_user(self, value):
        self.change_by = value
        
        """
    class Meta:
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medidas'

    def __str__(self):
        return self.description

class CategoryProduct(BaseModel):

    description = models.CharField('Descripcion', max_length=50, blank = False, null = False, unique = True)
    
    class Meta:
        verbose_name = 'Categoria de producto'
        verbose_name_plural = 'Categoria de productos'

    def __str__(self):
        return self.description
    

class Indicator(BaseModel):

    discountValue = models.PositiveSmallIntegerField(default=0)
    categoryProduct = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, verbose_name='Indicador de oferta')

    class Meta:
        verbose_name = 'Indicador de oferta'
        verbose_name_plural = 'Indicador de ofertas'

    def __str__(self):
        return f'Oferta de la categoria {self.categoryProduct} : {self.discountValue}%'
    
class Products(BaseModel):

    name = models.CharField('Nombre de Producto', max_length=150, blank = False, null = False, unique = True)
    description = models.TextField('Descripcion de Producto', blank = False, null = False)
    image = models.ImageField('Imagenes de Producto',upload_to='products/', null= True, blank= True)
    mesureUnit = models.ForeignKey(MeasureUnit, on_delete=models.CASCADE, verbose_name='Unidad de medida',null = True)
    categoryProduct =  models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, verbose_name='Categoria de producto',null = True)
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.name


    
