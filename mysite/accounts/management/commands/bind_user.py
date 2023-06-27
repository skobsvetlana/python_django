from django.core.management import BaseCommand
from django.contrib.auth.models import User, Group, Permission

class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(pk=4)
        group, created = Group.objects.get_or_create(
            name="profile_manager",
        )
        permission_profile = Permission.objects.get(
            codename="view_profile",
        )
        permission_logentry = Permission.objects.get(
            codename="view_logentry",
        )
        # Добавление разрешения в группу
        group.permissions.add(permission_profile)
        # Присоединение пользователя к группе
        user.groups.add(group)
        # Выдача пользователю разрешения на прямую
        user.user_permissions.add(permission_logentry)

        group.save()
        user.save()
