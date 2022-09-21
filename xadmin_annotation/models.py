# coding=utf-8
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Annotation(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
	                         on_delete=models.CASCADE,
	                         verbose_name=_("user"))
	description = models.TextField(verbose_name=_("description"))
	created_at = models.DateTimeField(_("created at"), auto_now_add=True)
	updated_at = models.DateTimeField(_("updated at"), auto_now=True)

	# relation
	content_type = models.ForeignKey(ContentType,
	                                 verbose_name=_("content"),
	                                 on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField(_("object id"))

	object = GenericForeignKey('content_type', 'object_id')

	class Meta:
		verbose_name = _("Annotation")
		verbose_name_plural = _("Annotations")
		indexes = [
			models.Index(fields=["content_type", "object_id"]),
		]

	def __str__(self):
		return self.user
