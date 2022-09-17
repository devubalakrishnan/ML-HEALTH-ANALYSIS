from django.shortcuts import redirect
from django.contrib import messages
def not_loggedin(view_func):
    def wrapper_func(request):
        if request.user.is_authenticated==True:
            messages.error(request,f"You are already Logged In as {request.user.username}!")
            return redirect('home')
        else:
            return view_func(request)
    return wrapper_func
