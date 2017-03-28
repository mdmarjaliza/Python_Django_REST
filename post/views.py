from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.datetime_safe import datetime
from django.views import View
from django.views.generic import ListView
from post.forms import PostForm
from post.models import Post
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.

class HomeView(View):
    def get(self, request):
        """
        Renderiza el home con un listado de los ultimos post publicados por los usuarios
        :param request: objeto HttpRequest con los datos de la peticion
        :return:
        """
        posts = Post.objects.all().filter(fec_publicacion__lte=datetime.now()).order_by(
            '-fec_publicacion').select_related("owner")
        context = {'posts_list': posts[:5]}
        return render(request, "post/home.html", context)


class PostQueryset(object):
    @staticmethod
    def get_postdetail_by_user(user, pk, blogger):
        if user.is_authenticated() and user.username == blogger:
            possible_posts = Post.objects.filter(Q(pk=pk) & Q(owner__username=blogger)).select_related("owner")
        else:
            possible_posts = Post.objects.filter(
                Q(pk=pk) & Q(owner__username=blogger) & Q(fec_publicacion__lte=datetime.now())).select_related(
                "owner")
        return possible_posts


class PostDetailView(View):
    def get(self, request, pk, blogger):
        """
        Renderiza el detalle de un post
        :param request: objeto HttpRequest con los datos de la peticion
        :param pk: clave primaria del post a recuperar
        :param blogger: usuario autor del post
        :return:
        """
        possible_posts = PostQueryset.get_postdetail_by_user(request.user, pk, blogger)

        if len(possible_posts) == 0:
            return HttpResponseNotFound("El post solicitado no existe")
        elif len(possible_posts) > 1:
            return HttpResponse("Multiples opciones", status=300)

        post = possible_posts[0]
        context = {'post': post}
        return render(request, 'post/post_detail.html', context)


class UserPostsView(ListView):
    """
    Muestra la lista de posts del blog de un usuario
    :param request: objeto HttpRequest con los datos de la peticion
    :param blogger: nombre de usuario de la persona cuyo blog queremos ver
    :return:
    """
    model = Post
    template_name = 'post/user_posts.html'

    def get(self, request, *args, **kwargs):
        if not User.objects.filter(username=self.kwargs["blogger"]).exists():
            return HttpResponseNotFound("No existe ningún blog con este nombre")
        else:
            posts = self.get_queryset()
            context = {'posts_list': posts, 'blogger': self.kwargs["blogger"]}
            return render(request, 'post/user_posts.html', context)

    def get_queryset(self):
        if User.objects.filter(username=self.kwargs["blogger"]).exists():
            if self.request.user.is_authenticated() and self.request.user.username == self.kwargs["blogger"]:
                result = super().get_queryset().filter(owner__username=self.kwargs["blogger"]).order_by(
                    '-fec_publicacion')
                return result
            else:
                result = super().get_queryset().filter(
                    Q(owner__username=self.kwargs["blogger"]) & Q(fec_publicacion__lte=datetime.now())).order_by(
                    '-fec_publicacion')
                return result


class CreatePostView(View):
    @method_decorator(login_required())
    def get(self, request):
        """
        Muestra el formulario para añadir un nuevo post al blog.
        :param request: objeto HttpRequest con los datos de la peticion
        :return:
        """
        message = None
        post_form = PostForm()
        context = {"form": post_form, "message": message}
        return render(request, "post/new_post.html", context)

    @method_decorator(login_required())
    def post(self, request):
        """
        Valida el formulario de creacion de nuevo post y lo crea.
        :param request: objeto HttpRequest con los datos de la peticion
        :return:
        """
        message = None
        post_with_user = Post(owner=request.user)
        post_form = PostForm(request.POST, instance=post_with_user)
        if post_form.is_valid():
            new_post = post_form.save()
            post_form = PostForm()
            message = "Post creado satisfactoriamente."
        context = {"form": post_form, "message": message}
        return render(request, "post/new_post.html", context)
