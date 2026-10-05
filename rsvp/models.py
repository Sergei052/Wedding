from django.db import models

class RSVP(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Имя")
    attending = models.BooleanField(verbose_name="Придёт")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время ответа")

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
        ordering = ['-created_at']

    def __str__(self):
        status = "Да" if self.attending else "Нет"
        return f"{self.name} — {status}"