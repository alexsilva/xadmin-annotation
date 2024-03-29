# coding=utf-8
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import Truncator
from django.utils.translation import gettext_lazy as _


class Annotation(models.Model):
	key = models.UUIDField(verbose_name=_("key"))
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
	                         on_delete=models.CASCADE,
	                         verbose_name=_("user"),
	                         null=True)
	description = models.TextField(verbose_name=_("description"))
	created_at = models.DateTimeField(_("created at"), auto_now_add=True)
	updated_at = models.DateTimeField(_("updated at"), auto_now=True)

	# relation
	content_type = models.ForeignKey(ContentType,
	                                 verbose_name=_("content"),
	                                 on_delete=models.CASCADE,
	                                 null=True)
	object_id = models.PositiveIntegerField(_("object id"),
	                                        null=True)

	object = GenericForeignKey('content_type', 'object_id')

	class Meta:
		verbose_name = _("Annotation")
		verbose_name_plural = _("Annotations")
		ordering = ("created_at",)
		indexes = [
			models.Index(fields=["content_type", "object_id"]),
		]

	def __str__(self):
		return Truncator(self.description).chars(32)
