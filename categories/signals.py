from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Category

User = get_user_model()


@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        default_categories = [
            # Incomes
            {'name': 'Salário', 'category_type': 'INCOME', 'color': '#2EC47D'},
            {'name': 'Investimentos', 'category_type': 'INCOME', 'color': '#EDF63B'},
            {'name': 'Outras Entradas', 'category_type': 'INCOME', 'color': '#667eea'},
            # Expenses
            {'name': 'Alimentação', 'category_type': 'EXPENSE', 'color': '#EF3823'},
            {'name': 'Transporte', 'category_type': 'EXPENSE', 'color': '#F5A623'},
            {'name': 'Lazer', 'category_type': 'EXPENSE', 'color': '#331F19'},
            {'name': 'Moradia', 'category_type': 'EXPENSE', 'color': '#2B130C'},
            {'name': 'Saúde', 'category_type': 'EXPENSE', 'color': '#EF3823'},
            {'name': 'Educação', 'category_type': 'EXPENSE', 'color': '#EDF63B'},
            {'name': 'Outras Saídas', 'category_type': 'EXPENSE', 'color': '#9A8176'},
        ]

        for cat_data in default_categories:
            Category.objects.create(user=instance, **cat_data)
