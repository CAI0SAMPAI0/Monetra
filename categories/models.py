from django.conf import settings
from django.db import models


class Category(models.Model):
    CATEGORY_TYPES = [
        ('INCOME', 'Entrada'),
        ('EXPENSE', 'Saída'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    name = models.CharField('nome', max_length=50)
    category_type = models.CharField(
        'tipo',
        max_length=10,
        choices=CATEGORY_TYPES
    )
    color = models.CharField('cor', max_length=7, default='#667eea')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'
        ordering = ['category_type', 'name']
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name
