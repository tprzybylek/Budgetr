from django import forms
from datetime import datetime
from .models import Category, Budget, Operation
from mptt.forms import TreeNodeChoiceField


class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        exclude = ['user']
        fields = ['datetime', 'category', 'parent_budget', 'child_budget', 'value', 'description']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')
        super(OperationForm, self).__init__(*args, **kwargs)
        self.fields['datetime'] = forms.DateTimeField(initial=datetime.now())
        self.fields['category'] = forms.ModelChoiceField(required=False,
                                                         queryset=Category.objects.filter(user=user)
                                                         )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ['user']
        fields = ['parent', 'name']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent'] = TreeNodeChoiceField(required=False,
                                                    queryset=Category.objects.filter(user=user)
                                                    )


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        exclude = ['user']
        fields = ['name']
