from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.contrib.staticfiles.storage import staticfiles_storage
import os
import random

from .models import Profile, Card

class MainView(LoginRequiredMixin, View):
    template_name = 'home/main.html'

    def get(self, request):
        profile = get_object_or_404(Profile, owner=request.user)
        images = os.listdir(staticfiles_storage.path('images'))
        if profile.first_time:
            profile.first_time = False
            profile.save()
            card1 = Card(level=random.randint(1, 3), image=random.choice(images), owner=request.user)
            card1.save()
            card2 = Card(level=random.randint(1, 3), image=random.choice(images), owner=request.user)
            card2.save()
            card3 = Card(level=random.randint(1, 3), image=random.choice(images), owner=request.user)
            card3.save()
        return render(request, self.template_name)