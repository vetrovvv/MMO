from django.shortcuts import redirect


def redirect_main(request):
    response = redirect('/announcements/')
    return response

