from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Costs, Income
from .form import CostsForm, IncomeForm
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, 'main/index.html')

# Вход
class BBLoginView(LoginView):
    template_name = 'main/login.html'

# Выход
class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'

# Профиль
@login_required
def profile(request):
    costsSum = Costs.objects.filter(author=request.user).aggregate(Sum('price'))
    incomeSum = Income.objects.filter(author=request.user).aggregate(Sum('price'))
    remainder = incomeSum.pop('price__sum') - costsSum.pop('price__sum')
    return render(request, 'main/profile.html', {'remainder': remainder })

# Регистрация
def register(request):
   form = UserCreationForm(request.POST)
   if form.is_valid():
       form.save()
       return HttpResponseRedirect("/main_str/")
   else:
       form = UserCreationForm()
       messages.add_message(request, messages.INFO, 'Повторите ввод данных')
       return render(request, 'main/register.html',  {'form': form})

# О сайте
def o_p(request):
    return render(request, 'main/o_p.html')

######## РАСХОДЫ ########
# Расходы с paginate
class CostsList(ListView):
    model = Costs
    template_name = 'main/costs.html'
    paginate_by = 5

    def get_queryset(self):
        return Costs.objects.filter(author=self.request.user)

# Добавить расходы
@login_required
def costs_add(request):
    if request.method == 'POST':
        form = CostsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Добавлено')
            return HttpResponseRedirect("/costs_add/")
    else:
        form = CostsForm(initial={'author': request.user.pk})
    context = {'form': form}
    return render(request, 'main/costs_add.html', context)

# Поиск по слову в расходах
def costs_search_form(request):
    return render(request, 'main/costs_search_form.html')

def costs_search_results(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        titles = Costs.objects.filter(author=request.user).filter(title__icontains=q)
        return render_to_response('main/costs_search_results.html',
            {'titles': titles, 'query': q})
    else:
        return HttpResponse('Выберите условия поиска')


######## ДОХОДЫ ########
# Доходы с paginate
class IncomeList(ListView):
    model = Income
    template_name = 'main/income.html'
    paginate_by = 5

    def get_queryset(self):
        return Income.objects.filter(author=self.request.user)

# Добавить доходы
@login_required
def income_add(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Добавлено')
            return HttpResponseRedirect("/income_add/")
    else:
        form = IncomeForm(initial={'author': request.user.pk})
    context = {'form': form}
    return render(request, 'main/income_add.html', context)

from django.contrib.postgres.search import SearchVector


# Поиск по слову в доходах
@login_required
def income_search_form(request):
    return render(request, 'main/income_search_form.html')

@login_required
def income_search_results(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        titles = Income.objects.filter(author=request.user).filter(title__icontains=q)
        return render_to_response('main/income_search_results.html',
            {'titles': titles, 'query': q})
    else:
        return HttpResponse('Выберите условия поиска')


@login_required
def main_str(request):
    return render(request, 'main/main_str.html')

######## АНАЛИТИКА ########
# Анализ
@login_required
def analysis(request):
    costsSum = Costs.objects.filter(author=request.user).aggregate(Sum('price'))
    incomeSum = Income.objects.filter(author=request.user).aggregate(Sum('price'))
    remainder = incomeSum.pop('price__sum') - costsSum.pop('price__sum')
    return render(request, 'main/analysis.html', {'remainder': remainder})


# Аналитика в диапазоне дат
def analysis_form(request):
    return render(request, 'main/analysis_form.html')

def analysis_results(request):
    if 'start_date' in request.GET and request.GET['start_date'] \
                    and 'end_date' in request.GET and request.GET['end_date']:
        start_date = request.GET['start_date']
        end_date = request.GET['end_date']
        Cs = Costs.objects.filter(author=request.user).filter(created_at__range=(start_date, end_date))
        Cs_sum = Costs.objects.filter(author=request.user).filter(created_at__range=(start_date, end_date)).aggregate(Sum('price'))
        Cs1 = Costs.objects.filter(author=request.user).filter(created_at__range=(start_date, end_date))\
            .filter(content__exact='Без категории').aggregate(Sum('price'))
        Cs2 = Costs.objects.filter(author=request.user).filter(created_at__range=(start_date, end_date)) \
            .filter(content__exact='Комунальные услуги').aggregate(Sum('price'))
        Cs3 = Costs.objects.filter(author=request.user).filter(created_at__range=(start_date, end_date)) \
            .filter(content__exact='Продуктовые покупки').aggregate(Sum('price'))
        Cs4 = Costs.objects.filter(author=request.user).filter(created_at__range=(start_date, end_date)) \
            .filter(content__exact='Товары для дома').aggregate(Sum('price'))
        Cs5 = Costs.objects.filter(author=request.user).filter(created_at__range=(start_date, end_date)) \
            .filter(content__exact='Одежда, обувь, аксессуары').aggregate(Sum('price'))
        Cs6 = Costs.objects.filter(author=request.user).filter(created_at__range=(start_date, end_date)) \
            .filter(content__exact='Образование').aggregate(Sum('price'))
        Cs7 = Costs.objects.filter(author=request.user).filter(created_at__range=(start_date, end_date)) \
            .filter(content__exact='Лекарства и медицина').aggregate(Sum('price'))
        Cs8 = Costs.objects.filter(author=request.user).filter(created_at__range=(start_date, end_date)) \
            .filter(content__exact='Автомобиль/транспорт').aggregate(Sum('price'))
        Cs9 = Costs.objects.filter(author=request.user).filter(created_at__range=(start_date, end_date)) \
            .filter(content__exact='Развлечения').aggregate(Sum('price'))
        Cs10 = Costs.objects.filter(author=request.user).filter(created_at__range=(start_date, end_date)) \
            .filter(content__exact='Хобби').aggregate(Sum('price'))
        Cs11 = Costs.objects.filter(author=request.user).filter(created_at__range=(start_date, end_date)) \
            .filter(content__exact='Личные траты').aggregate(Sum('price'))

        Im = Income.objects.filter(author=request.user).filter(created_at__range=(start_date, end_date)).aggregate(Sum('price'))
        Im_sum = Income.objects.filter(author=request.user).filter(created_at__range=(start_date, end_date)).aggregate(Sum('price'))
        Im1 = Income.objects.filter(author=request.user).filter(created_at__range=(start_date, end_date)) \
            .filter(content__exact='Другое').aggregate(Sum('price'))
        Im2 = Income.objects.filter(author=request.user).filter(created_at__range=(start_date, end_date)) \
            .filter(content__exact='Аванс').aggregate(Sum('price'))
        Im3 = Income.objects.filter(author=request.user).filter(created_at__range=(start_date, end_date)) \
            .filter(content__exact='Зарплата').aggregate(Sum('price'))
        Im4 = Income.objects.filter(author=request.user).filter(created_at__range=(start_date, end_date)) \
            .filter(content__exact='Социальные выплаты').aggregate(Sum('price'))

        content = { 'start_date': start_date, 'end_date': end_date,
                    'Cs': Cs, 'Cs_sum': Cs_sum,
                    'Cs1': Cs1, 'Cs2': Cs2, 'Cs3': Cs3, 'Cs4': Cs4, 'Cs5': Cs5, 'Cs6': Cs6, 'Cs7': Cs7,
                    'Cs8': Cs8, 'Cs9': Cs9, 'Cs10': Cs10, 'Cs11': Cs11,
                    'Im': Im, 'Im_sum': Im_sum,
                    'Im1': Im1, 'Im2': Im2, 'Im3': Im3, 'Im4': Im4,
                    }

        return render_to_response('main/analysis_results.html', content)
    else:
        return render(request, 'main/analysis.html')