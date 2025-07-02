from accounts.models import CustomUser


def get_customuser(pk):
    return CustomUser.objects.filter(pk=pk).first()