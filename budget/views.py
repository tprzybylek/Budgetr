from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Sum

from django.utils import timezone

from django.contrib.auth.decorators import login_required

from .models import Operation, Budget, Category
from .forms import OperationForm, BudgetForm, CategoryForm

import json
import decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


@login_required
def budgets(request):
    budgets = Budget.objects.filter(user=request.user)

    for budget in budgets:
        inflow = Operation.objects.filter(child_budget=budget).aggregate(Sum('value'))
        outflow = Operation.objects.filter(parent_budget=budget).aggregate(Sum('value'))

        budget.value = sum(filter(None, (inflow['value__sum'], outflow['value__sum'])))     # filters out None
    return render(request, 'budget/budgets.html', {'budgets': budgets})


@login_required
def budget_details(request, id):
    budget = get_object_or_404(Budget, pk=id)
    operations = Operation.objects.filter(user=request.user, child_budget=id) | Operation.objects.filter(user=request.user, parent_budget=id)
    return render(request, 'budget/budget_details.html', {'operations': operations, 'budget': budget})


def save_budget_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()

            data['form_is_valid'] = True
            budgets = Budget.objects.filter(user=request.user)

            for budget in budgets:
                inflow = Operation.objects.filter(child_budget=budget).aggregate(Sum('value'))
                outflow = Operation.objects.filter(parent_budget=budget).aggregate(Sum('value'))

                budget.value = sum(filter(None, (inflow['value__sum'], outflow['value__sum'])))

            data['html_budgets_list'] = render_to_string('budget/includes/partial_budget_list.html', {
                'budgets': budgets})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
    else:
        form = BudgetForm()
    return save_budget_form(request, form, 'budget/includes/partial_budget_create.html')


def budget_update(request, id):
    budget = get_object_or_404(Budget, pk=id)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
    else:
        form = BudgetForm(instance=budget)
    return save_budget_form(request, form, 'budget/includes/partial_budget_update.html')


def budget_delete(request, id):
    budget = get_object_or_404(Budget, pk=id)
    data = dict()
    if request.method == 'POST':
        budget.delete()
        data['form_is_valid'] = True
        budgets = Budget.objects.filter(user=request.user)

        for budget in budgets:
            inflow = Operation.objects.filter(child_budget=budget).aggregate(Sum('value'))
            outflow = Operation.objects.filter(parent_budget=budget).aggregate(Sum('value'))

            budget.value = sum(filter(None, (inflow['value__sum'], outflow['value__sum'])))

        data['html_budgets_list'] = render_to_string('budget/includes/partial_budget_list.html', {
                'budgets': budgets})
    else:
        context = {'budget': budget}
        data['html_form'] = render_to_string('budget/includes/partial_budget_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


@login_required
def categories(request):
    categories = Category.objects.filter(user=request.user)

    return render(request, 'budget/categories.html', {'categories': categories})


@login_required
def category_details(request, id):
    category = get_object_or_404(Category, pk=id)
    operations = Operation.objects.filter(user=request.user, category=id)
    return render(request, 'budget/category_details.html', {'operations': operations, 'category': category.name})


def save_category_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()

            data['form_is_valid'] = True
            categories = Category.objects.filter(user=request.user)

            data['html_categories_list'] = render_to_string('budget/includes/partial_category_list.html', {
                'categories': categories})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, user=request.user)
    else:
        form = CategoryForm(user=request.user)
    return save_category_form(request, form, 'budget/includes/partial_category_create.html')


def category_update(request, id):
    category = get_object_or_404(Category, pk=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category, user=request.user)
    else:
        form = CategoryForm(instance=category, user=request.user)
    return save_category_form(request, form, 'budget/includes/partial_category_update.html')


def category_delete(request, id):
    category = get_object_or_404(Category, pk=id)
    data = dict()
    if request.method == 'POST':
        category.delete()
        data['form_is_valid'] = True
        categories = Category.objects.filter(user=request.user)

        data['html_categories_list'] = render_to_string('budget/includes/partial_category_list.html', {
            'categories': categories})
    else:
        context = {'category': category}
        data['html_form'] = render_to_string('budget/includes/partial_category_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


@login_required
def dashboard(request):
    operations = Operation.objects.all()[:10]
    return render(request, 'budget/dashboard.html', {'operations': operations})

@login_required
def archive(request):
    operations = Operation.objects.filter(user=request.user)
    first_operation = operations.first()
    last_operation = operations.last()

    first_year = first_operation.datetime.year
    last_year = last_operation.datetime.year

    years = list(range(first_year, last_year + 1))
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    active_year = request.GET.get('active_year')
    active_month = request.GET.get('active_month')

    if active_year is None:
        active_year = timezone.now().year
    else:
        active_year = int(active_year)

    if active_month is None:
        active_month = timezone.now().month
    else:
        active_month = int(active_month)

    operations = operations.filter(datetime__year=active_year, datetime__month=active_month)

    categories = operations.values('category').annotate(value_sum=Sum('value')).order_by('-value_sum')

    categories = list(categories.values('category__name', 'value_sum'))

    categories = json.dumps(categories, indent=4, cls=DecimalEncoder)
    # categories = json.dumps(build_category_tree(categories), indent=4, cls=DecimalEncoder)

    context = {
        'years': years,
        'months': months,
        'operations': operations,
        'categories': categories,
        'active_year': int(active_year),
        'active_month': int(active_month),
    }

    return render(request, 'budget/archive.html', context)


def save_operation_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()

            data['form_is_valid'] = True
            operations = Operation.objects.filter(user=request.user)

            data['html_operations_list'] = render_to_string('budget/includes/partial_operation_list.html', {
                'operations': operations})
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def operation_create(request):
    if request.method == 'POST':
        form = OperationForm(request.POST, user=request.user)
    else:
        form = OperationForm(user=request.user)
    return save_operation_form(request, form, 'budget/includes/partial_operation_create.html')


def operation_update(request, id):
    operation = get_object_or_404(Operation, pk=id)
    if request.method == 'POST':
        form = OperationForm(request.POST, instance=operation, user=request.user)
    else:
        form = OperationForm(instance=operation, user=request.user)
    return save_operation_form(request, form, 'budget/includes/partial_operation_update.html')


def operation_delete(request, id):
    operation = get_object_or_404(Operation, pk=id)
    data = dict()
    if request.method == 'POST':
        operation.delete()
        data['form_is_valid'] = True
        operations = Operation.objects.filter(user=request.user)

        data['html_operations_list'] = render_to_string('budget/includes/partial_operation_list.html', {
            'operations': operations})
    else:
        context = {'operation': operation}
        data['html_form'] = render_to_string('budget/includes/partial_operation_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)
