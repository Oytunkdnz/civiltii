from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, FormView, RedirectView

from tweets.forms import KayitForm, GirisForm, TweetForm, ProfilForm
from tweets.models import User, Tweet


class Karsilama(TemplateView):
    template_name = "karsilama.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/akis/")

        return super(Karsilama, self).dispatch(request, *args, **kwargs)


class KayitOl(FormView):
    template_name = "kayit_ol.html"
    form_class = KayitForm
    success_url = "/akis/"

    def form_valid(self, form):
        user = User.objects.create(
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            email=form.cleaned_data["email"],
            username=form.cleaned_data["username"],
        )
        user.set_password(form.cleaned_data["password"])
        user.save()
        login(self.request, user)
        return super(KayitOl, self).form_valid(form)


class GirisYap(FormView):
    template_name = "giris_yap.html"
    form_class = GirisForm
    success_url = "/akis/"

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"]
        )
        if user:
            login(self.request, user)
            return super(GirisYap, self).form_valid(form)
        else:
            return super(GirisYap, self).form_invalid(form)


class Akis(FormView):
    template_name = "akis.html"
    form_class = TweetForm
    success_url = "/akis/"

    def get_context_data(self, **kwargs):
        context = super(Akis, self).get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user.username)
        follows = list(user.follows.all().values_list('id', flat=True))
        follows.append(self.request.user.id)
        # follows = list(user.follows.all().values_list('username', flat=True))
        # follows.append(self.request.user.username)
        username = self.kwargs.get("username", self.request.user.username)
        profil = User.objects.get(username=username)
        context["profile"] = profil
        context["follows"] = user.follows.filter(id=profil.id).exists()
        timeline = Tweet.objects.filter(author__in=follows).order_by("-created")
        # timeline = Tweet.objects.filter(author__username_in=follows).order_by("-created")
        context["timeline"] = timeline
        return context

    def form_valid(self, form):
        Tweet.objects.create(
            author=User.objects.get(id=self.request.user.id),
            text=form.cleaned_data["text"]
        )
        return super(Akis, self).form_valid(form)
class takip_ettiklerim(TemplateView):
    template_name = "takip_ettiklerim.html"
    def get_context_data(self,**kwargs):
        context = super(takip_ettiklerim, self).get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user.username)
        username = self.kwargs.get("username", self.request.user.username)
        follows = list(user.follows.all().values_list('username', flat=True))
        kullanicilar = User.objects.filter(username__in=follows)
        profil = User.objects.get(username=username)
        context["profile"] = profil
        context["follows"] = user.follows.filter(id=profil.id).exists()
        context["kullanicilar"] = kullanicilar
        return context
class takip_edenler(TemplateView):
    template_name = "takip_edenler.html"
    def get_context_data(self,**kwargs):
        context = super(takip_edenler, self).get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user.username)
        username = self.kwargs.get("username", self.request.user.username)
        follows = list(user.followed_by.all().values_list('username', flat=True))
        kullanicilar = User.objects.filter(username__in=follows)
        profil = User.objects.get(username=username)
        context["profile"] = profil
        context["follows"] = user.follows.filter(id=profil.id).exists()
        context["kullanicilar"] = kullanicilar
        return context



class Profil(FormView):
    template_name = "profil.html"
    form_class = ProfilForm

    def get_context_data(self, **kwargs):
        context = super(Profil, self).get_context_data(**kwargs)
        # self.request.user.username != "":
        user = User.objects.get(username=self.request.user.username)
        username = self.kwargs.get("username", self.request.user.username)
        profil = User.objects.get(username=username)
        context["profile"] = profil
        context["timeline"] = profil.tweet_set.all()
        context["follows"] = user.follows.filter(id=profil.id).exists()
        return context

    def form_valid(self, form):
        user = User.objects.get(username=self.request.user.username)
        profil = User.objects.get(username=self.kwargs.get("username"))
        if user.follows.filter(id=profil.id).exists():
            user.follows.remove(profil)
        else:
            user.follows.add(profil)
        self.success_url = "/profil/" + profil.username + "/"
        return super(Profil, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get("username") is None and not request.user.is_authenticated:
            return redirect("/giris_yap/?next=/profil/")
        return super(Profil, self).dispatch(request, *args, **kwargs)

class tum_kullanicilari_goster(FormView):
    template_name = "tum_kullanicilar.html"
    form_class = ProfilForm
    def get_context_data(self,**kwargs):
        context = super(tum_kullanicilari_goster, self).get_context_data(**kwargs)
        username = self.kwargs.get("username", self.request.user.username)
        profil = User.objects.get(username=username)
        user = User.objects.get(username=self.request.user.username)
        context["profile"] = profil
        context["kullanicilar"] = User.objects.all()
        context["follows"] = user.follows.filter(id=profil.id).exists()
        return context
    def form_valid(self, form):
        user = User.objects.get(username=self.request.user.username)
        profil = User.objects.get(username=self.kwargs.get("username"))
        if user.follows.filter(id=profil.id).exists():
            user.follows.remove(profil)
        else:
            user.follows.add(profil)
        self.success_url = "/profil/" + profil.username + "/"
        return super(tum_kullanicilari_goster, self).form_valid(form)



class CikisYap(RedirectView):
    pattern_name = "karsilama"

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super(CikisYap, self).get_redirect_url(*args, **kwargs)
