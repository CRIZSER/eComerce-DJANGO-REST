from django.db import models

from simple_history.models import HistoricalRecords

# Create your models here.
class BaseModel(models.Model):
    """Model definition for BaseModel."""

    # TODO: Define fields here
    id = models.AutoField(primary_key = True)
    state = models.BooleanField('Estado',default = True)
    created_date = models.DateField('Fecha de Creación', auto_now=False, auto_now_add=True)
    modified_date = models.DateField('Fecha de Modificación', auto_now=True, auto_now_add=False)
    deleted_date = models.DateField('Fecha de Eliminación', auto_now=True, auto_now_add=False)
    historical = HistoricalRecords(user_model="users.User", inherit=True)

    @property #esto funciona como un metodo que se utiliza de manera automatica al instanticar el objeto y puede ser accedido como atributo
    def _histoy_user(self):
        return self.change_by


    @_histoy_user.setter #funciona como el anterior pero de manera complementaria, ya que se ejecutara al momento de que queramos asignar un calo a la propiedad
    def _histoy_user(self, value):
        self.change_by = value

    class Meta:
        """Meta definition for BaseModel."""
        abstract = True # al incluir esto no se crea en la base de datos al relizar make migrations
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medidas'