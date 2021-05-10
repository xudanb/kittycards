from django.shortcuts import render

# Create your views here.
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from home.models import Profile
import random

# Create your views here.
class MainView(LoginRequiredMixin, View):
    template_name = 'kittywallet/main.html'

    def get(self, request):
        ctx = {
            'coins': Profile.objects.get(owner=request.user).coins,
            'coins_withholded': Profile.objects.get(owner=request.user).coins_withholded,
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        profile = Profile.objects.get(owner=request.user)
        profile.coins = min(10000, profile.coins+random.randint(1, 10)*100)
        profile.save()
        return redirect('/kittywallet')