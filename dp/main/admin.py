from django.contrib import admin
from .models import Costs, Income


#  Расходы
class CostsRubric(admin.ModelAdmin):
    list_display = ('content', 'title', 'price', 'author', 'created_at')
admin.site.register(Costs)


#  Доходы
class IncomeRubric(admin.ModelAdmin):
    list_display = ('content', 'title', 'price', 'author', 'created_at',)
admin.site.register(Income)



