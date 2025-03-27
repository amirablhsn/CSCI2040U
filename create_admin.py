from django.contrib.auth import get_user_model


def create_admin():
    User = get_user_model()
    username = "admin"
    password = "admin123"

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, password=password)
        print(f"Admin created.\n\tUsername: {username}\n\tPassword: {password}")
    else:
        print(f"Admin with {username} already exists")
