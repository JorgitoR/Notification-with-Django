
# ContenType
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

#Timezone
from django.utils import timezone

# Models
from User.models import Usuario

#Django
from django.db import models


class NotificationQueryset(models.QuerySet):

	def leido(self, include_deleted=True):
		"""
			Retornamos las notificaciones que hayan sido leidas en el actual Queryset
		"""

		if include_deleted:
			return self.filter(read=True)

	def no_leido(self, include_deleted=False):
		"""
			Retornamos solo los items que no hayan sido leidos en el actual Queryset
		"""	
		if include_deleted==True:
			return self.filter(read=False)

	def marcar_todo_as_leido(self, destiny=None):
		"""
			Marcar todas las notify como leidas en el actual queryset
		"""
		qs = self.read(False)
		if destiny:
			qs = qs.filter(destiny=destiny)

		return qs.update(read=True)

	def marcar_todo_as_no_leido(self, destiny=None):
		"""
			Marcar todas las notificaciones como no leidas en el actual queryset
		"""

		qs = self.read(True)
		if destiny:
			qs = qs.filter(destiny=destiny)

		return qs.update(read=False)



class AbstractNotificationManager(models.Manager):
	def get_queryset(self):
		return self.NotificationQueryset(self.Model, using=self._db)

class AbstractNotificacion(models.Model):

	class Levels(models.TextChoices):
		success = 'Success', 'success',
		info = 'Info', 'info',
		wrong = 'Wrong', 'wrong'

	level = models.CharField(choices=Levels.choices, max_length=20, default=Levels.info)

	destiny = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notificaciones', blank=True, null=True)

	actor_content_type = models.ForeignKey(ContentType, related_name='notificar_actor', on_delete=models.CASCADE)
	object_id_actor = models.PositiveIntegerField()
	actor = GenericForeignKey('actor_content_type', 'object_id_actor')

	verbo = models.CharField(max_length=220)

	read = models.BooleanField(default=False)
	publico = models.BooleanField(default=True)
	eliminado = models.BooleanField(default=False)

	timestamp = models.DateTimeField(default=timezone.now, db_index=True)

	objects = NotificationQueryset.as_manager()

	class Meta:
		abstract = True


def notify_signals(verb, **kwargs):
	"""
		Funcion de controlador para crear una instancia de notificacion
		tras una llamada de signal de accion
	"""