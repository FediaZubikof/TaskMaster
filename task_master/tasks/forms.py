from django import forms
from .models import Task, Task_Img, Project, Team, User, TeamMembership


# Переопределить dateinput и datetimeinput, чтобы django мог читать html-селекторы date и datetime.
class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class DateInput(forms.DateInput):
    input_type = 'date'


class TaskForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.none(),  # Изначально пусто
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Ответственный'
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'd_time', 'project', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название задачи'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание задачи'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'd_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Если форма инициализируется без данных, попробуем загрузить членов команды для первого проекта
        if not self.data:
            projects = Project.objects.all()
            if projects.exists():
                first_project = projects.first()
                self.fields['assigned_to'].queryset = first_project.team.members.all()
                self.fields['project'].initial = first_project.id

        # Обработка данных, если они есть
        if 'project' in self.data:
            try:
                project_id = int(self.data.get('project'))
                project = Project.objects.get(pk=project_id)
                self.fields['assigned_to'].queryset = project.team.members.all()
            except (ValueError, TypeError, Project.DoesNotExist):
                self.fields['assigned_to'].queryset = User.objects.none()
        elif self.instance.pk and self.instance.project:
            self.fields['assigned_to'].queryset = self.instance.project.team.members.all()

    def clean(self):
        cleaned_data = super().clean()
        project = cleaned_data.get('project')

        if project:
            team = project.team
            cleaned_data['team'] = team  # Привязка команды к задаче
        else:
            self.add_error('project',
                           'Проект не выбран. Выберите проект, чтобы назначить команду. Либо, создайте его на странице проектов.')

        return cleaned_data


class TaskUpdateForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Ответственный'
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'd_time', 'project', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название задачи'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание задачи'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'd_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Заполнение поля ответственным в зависимости от выбранного проекта
        if 'project' in self.data:
            try:
                project_id = int(self.data.get('project'))
                project = Project.objects.get(pk=project_id)
                self.fields['assigned_to'].queryset = project.team.members.all()
            except (ValueError, TypeError, Project.DoesNotExist):
                self.fields['assigned_to'].queryset = User.objects.none()
        elif self.instance.pk and self.instance.project:
            self.fields['assigned_to'].queryset = self.instance.project.team.members.all()

    def clean(self):
        cleaned_data = super().clean()
        project = cleaned_data.get('project')

        if project:
            team = project.team
            cleaned_data['team'] = team  # Привязка команды к задаче

        return cleaned_data


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Task_Img
        fields = ['img']


class ProjectForm(forms.ModelForm):
    new_team_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название новой команды'}),
        label='Новая команда'
    )
    team_members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label='Члены новой команды'
    )
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        required=False,  # Сделайте поле необязательным
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Существующая команда'
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'team', 'new_team_name', 'team_members']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название проекта'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание проекта'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'name': 'Название проекта',
            'description': 'Описание проекта',
            'start_date': 'Дата начала',
            'end_date': 'Дата завершения',
        }


class TeamForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label='Члены команды'
    )
    roles = forms.ChoiceField(
        choices=TeamMembership.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Роль'
    )

    class Meta:
        model = Team
        fields = ['name', 'members', 'roles']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название команды'}),
        }
        labels = {
            'name': 'Название команды',
        }
