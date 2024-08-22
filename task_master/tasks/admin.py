from django.contrib import admin
from .models import Team, TeamMembership, Project, Task, Task_Img


class TeamMembershipInline(admin.TabularInline):
    model = TeamMembership
    extra = 1


# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'first_name', 'last_name', 'email')
#     search_fields = ('first_name', 'last_name', 'email')
#     list_filter = ('user',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [TeamMembershipInline]


@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'team__name')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'start_date', 'end_date')
    search_fields = ('name', 'team__name')
    list_filter = ('team',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'team', 'user', 'priority', 'c_time', 'u_time', 'd_time', 'mark')
    search_fields = ('title', 'project__name', 'team__name', 'user__username')
    list_filter = ('priority', 'team', 'project', 'mark')


@admin.register(Task_Img)
class TaskImgAdmin(admin.ModelAdmin):
    list_display = ('task', 'img')
    search_fields = ('task__title',)
