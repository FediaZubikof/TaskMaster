from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    """Для представления команды."""
    name = models.CharField(max_length=100, unique=True, verbose_name="Название команды")
    members = models.ManyToManyField(User, through='TeamMembership', related_name='teams', verbose_name="Члены команды")

    def __str__(self):
        return self.name


class TeamMembership(models.Model):
    """Для управления членством в команде и ролями."""
    ADMIN = 'admin'
    MEMBER = 'member'

    ROLE_CHOICES = [
        (ADMIN, 'Администратор'),
        (MEMBER, 'Обычный пользователь'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="Команда")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=MEMBER, verbose_name="Роль")

    class Meta:
        unique_together = ('user', 'team')

    def __str__(self):
        return f"{self.user.username} - {self.team.name} ({self.get_role_display()})"


class Project(models.Model):
    """Для представления проекта."""
    name = models.CharField(max_length=100, verbose_name="Название проекта")
    description = models.TextField(null=True, blank=True, verbose_name="Описание проекта")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='projects', verbose_name="Команда")
    start_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата начала")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата завершения")

    def __str__(self):
        return self.name


class Task(models.Model):
    """Для представления задачи."""
    PRIORITY_CHOICES = [
        ("Низкий", "Низкий"),
        ("Средний", "Средний"),
        ("Высокий", "Высокий"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', verbose_name='Проект',
                                null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='tasks', verbose_name='Команда', null=True,
                             blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField(max_length=100, null=True, verbose_name='Название задачи')
    description = models.TextField(max_length=255, null=True, blank=True, verbose_name='Описание задачи')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    u_time = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    d_time = models.DateTimeField(null=True, blank=True, verbose_name='Время окончания')
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        null=True,
        blank=True,
        verbose_name='Уровень приоритета'
    )
    mark = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_tasks', verbose_name='Ответственный')

    def __str__(self):
        return self.title


class Task_Img(models.Model):
    """Для хранения изображений, связанных с задачами."""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='images')
    img = models.ImageField(upload_to="task_img")

    def __str__(self):
        return f"Image for {self.task.title}"
