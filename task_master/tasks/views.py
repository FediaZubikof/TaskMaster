from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from .models import Task, Task_Img, Project, Team, TeamMembership
from .forms import TaskForm, TaskUpdateForm, PhotoForm, ProjectForm, TeamForm
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect


class TaskListView(View):
    template_name = 'tasks/tasks.html'

    def get(self, request, priority=None):
        query = request.GET.get('q')
        project_id = request.GET.get('project')
        completed = request.GET.get('completed')
        due_date = request.GET.get('due_date')
        user_filter = request.GET.get('user')  # Фильтр по пользователю

        tasks = Task.objects.all()

        if priority:
            tasks = tasks.filter(priority=priority)

        if query:
            tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))

        if project_id:
            tasks = tasks.filter(project_id=project_id)

        if completed == 'true':
            tasks = tasks.filter(mark=True)
        elif completed == 'false':
            tasks = tasks.filter(mark=False)

        if due_date:
            tasks = tasks.filter(d_time__lte=due_date)

        if user_filter:
            tasks = tasks.filter(user=user_filter)  # Фильтрация по пользователю, если указано

        tasks = tasks.order_by('-id')

        form = TaskForm()
        context = {
            'task_list': tasks,
            'form': form,
            'projects': Project.objects.all(),
            'now': timezone.now(),
            'bgall': 'primary' if not priority else None,
            'bgh': 'primary' if priority == 'High' else None,
            'bgm': 'primary' if priority == 'Medium' else None,
            'bgl': 'primary' if priority == 'Low' else None,
        }
        return render(request, self.template_name, context)


class TaskDetailsView(View):
    template_name = 'tasks/task_details.html'

    def get(self, request, pk):
        try:
            # Убираем фильтрацию по пользователю
            tasks = Task.objects.get(pk=pk)
            task_img = Task_Img.objects.filter(task=pk)
            context = {
                'task': tasks,
                'task_img': task_img,
                'now': timezone.now(),
                'project': tasks.project,
                'team': tasks.team,
                'assigned_to': tasks.assigned_to,
            }
        except Task.DoesNotExist:
            messages.error(request, "Задача не найдена.")
            return redirect('/tasks/')  # Перенаправление на список задач в случае ошибки

        return render(request, self.template_name, context)


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create_task.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.team = form.cleaned_data.get('project').team  # Привязываем команду
        form.instance.assigned_to = form.cleaned_data.get('assigned_to')  # Назначаем ответственного
        return super().form_valid(form)


# class TaskUpdateView(UpdateView):
#     model = Task
#     form_class = TaskUpdateForm
#     template_name = 'tasks/task_update.html'
#
#     def get_success_url(self):
#         # Перенаправление на страницу деталей задачи после успешного обновления
#         return reverse('more_details', args=[self.object.pk])
#
#     def form_valid(self, form):
#         # Устанавливаем текущего пользователя как автора изменений
#         form.instance.user = self.request.user
#         return super().form_valid(form)
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = 'tasks/task_update.html'

    def get_success_url(self):
        return reverse('more_details', args=[self.object.pk])

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        # Обновляем состав команды на основе данных формы
        team_members = form.cleaned_data.get('team_members')
        if team_members:
            form.instance.team.members.set(team_members)

        return response


class TaskDeleteView(DeleteView):
    # указываем модель, которую хотим использовать
    model = Task

    # можно указать URL успешного выполнения
    # url для перенаправления после успешного выполнения
    # удаление объекта
    success_url = "/"

    template_name = 'tasks/tasks.html'


def add_photo(request, id):
    if request.method == 'POST':

        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            task = Task.objects.get(pk=id)
            img = form.cleaned_data['img']
            img_form = Task_Img(task=task, img=img)
            img_form.save()
            return redirect(f'/tasks/{id}/')  # Перенаправить на просмотр, отображающий список скриншотов
    else:
        form = PhotoForm()

    context = {'form': form}

    return render(request, 'tasks/add_photo.html', context)


def delete_photo(request, id):
    if request.method == 'POST':
        task_id = Task_Img.objects.get(pk=id).task.id

        pi = Task_Img.objects.get(pk=id)
        pi.delete()
        return redirect(f'/tasks/{task_id}/')

    return render(request, 'tasks/task_details.html')


def complete(request, id):
    if request.method == 'POST':
        task = Task.objects.get(pk=id)
        if task.mark:
            task.mark = False
            task.save()

            return redirect('/')
        else:
            task.mark = True
            task.save()
            return redirect('/')
    return render(request, 'tasks/tasks.html')


class ProjectCreateView(UserPassesTestMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create_project.html'
    success_url = reverse_lazy('projects')

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        context = {
            'form': ProjectForm(),
            'team_form': TeamForm(),
            'error_message': "У вас нет прав на создание проекта"
        }
        return render(self.request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_form'] = TeamForm()  # Добавляем форму команды в контекст
        return context

    def form_valid(self, form):
        new_team_name = form.cleaned_data.get('new_team_name')
        team_members = form.cleaned_data.get('team_members')

        if new_team_name and team_members:
            # Проверка существования команды с таким именем
            if Team.objects.filter(name=new_team_name).exists():
                form.add_error('new_team_name', 'Команда с таким именем уже существует.')
                return self.form_invalid(form)
            else:
                # Создаем новую команду и добавляем участников
                team = Team.objects.create(name=new_team_name)
                for member in team_members:
                    TeamMembership.objects.create(user=member, team=team, role=TeamMembership.MEMBER)
                form.instance.team = team
        elif form.cleaned_data.get('team'):
            form.instance.team = form.cleaned_data.get('team')
        else:
            form.add_error(None, 'Необходимо выбрать существующую команду или создать новую.')
            return self.form_invalid(form)

        return super().form_valid(form)


class ProjectTaskListView(View):
    template_name = 'projects/project_tasks.html'

    def get(self, request, project_id):
        # Получаем проект; если проект не найден, выводим сообщение и перенаправляем на список проектов
        project = get_object_or_404(Project, id=project_id)

        # Получаем задачи проекта
        tasks = project.tasks.all()

        # Проверяем, есть ли задачи, и если нет, выводим сообщение
        if not tasks.exists():
            messages.info(request, "Для этого проекта пока нет задач.")

        context = {
            'project': project,
            'task_list': tasks
        }
        return render(request, self.template_name, context)


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/update_project.html'
    success_url = reverse_lazy('projects')


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'projects/project_delete.html'
    success_url = reverse_lazy('projects')
