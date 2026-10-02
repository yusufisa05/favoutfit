from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hesabınız başarıyla oluşturuldu, {username}!')
            referer = request.META.get('HTTP_REFERER')
            if referer and 'kaydol' not in referer:
                return redirect(referer)
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            referer = request.META.get('HTTP_REFERER')
            if referer and 'kaydol' not in referer:
                return redirect(referer)
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})
