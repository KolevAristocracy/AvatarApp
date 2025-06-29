from accounts.models import CustomUser


def get_profile(pk):
    return CustomUser.objects.filter(pk=pk).first()