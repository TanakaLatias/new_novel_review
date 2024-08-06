from django.shortcuts import reverse, redirect
import datetime
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import WorkForm, PostForm, SceneForm
from .models import User, Work, Scene, Poll, Post, Like, Read
from django.db.models import Count, Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import IntegrityError

class UserCheckMixin:
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')
        object = self.get_object()
        if object.user != self.request.user:
            return redirect('error')
        return super().get(request, *args, **kwargs)

class FormCreateView(LoginRequiredMixin, CreateView):
    template_name = 'htmls/basic_form.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FormUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'htmls/basic_form.html'
    success_url = reverse_lazy('top')
    
class ErrorView(TemplateView):
    template_name = 'htmls/error.html'

class TopAndIndexView(TemplateView):
    template_name = 'htmls/top.html'

class UserDetailView(DetailView):
    model = User
    template_name = 'htmls/user_detail.html'
    context_object_name = 'the_user'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_detail'] = 'user_detail'
        the_user = User.objects.get(id=self.kwargs.get('pk'))
        if self.request.user == the_user:
            context['posts'] = Post.objects.filter(user=the_user).order_by('-pk')[:5]
        else:
            context['posts'] = Post.objects.filter(user=the_user, hide=False).order_by('-pk')[:5]
        context['likes'] = Like.objects.filter(user=the_user).order_by('-pk')[:5]
        context['reads'] = Read.objects.filter(user=the_user).order_by('-pk')[:5]
        context['posts_count'] = Post.objects.filter(user=the_user).count()
        context['likes_count'] = Like.objects.filter(user=the_user).count()
        context['reads_count'] = Read.objects.filter(user=the_user).count()
        return context

class UserDetailPostsView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'htmls/user_detail.html'
    paginate_by = 20
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_detail_posts'] = 'user_detail_posts'
        the_user = User.objects.get(id=self.kwargs.get('pk'))
        context['the_user'] = the_user
        context['recent'] =  datetime.datetime.now() - datetime.timedelta(days=3)
        context['posts_count'] = Post.objects.filter(user=the_user).count()
        return context
    def get_queryset(self):
        the_user = User.objects.get(id=self.kwargs.get('pk'))
        if self.request.user == the_user:
            return Post.objects.filter(user=the_user).order_by('-pk')
        else:
            return Post.objects.filter(user=the_user, hide=False).order_by('-pk')

class UserDetailLikesView(LoginRequiredMixin, ListView):
    model = Like
    context_object_name = 'likes'
    template_name = 'htmls/user_detail.html'
    paginate_by = 20
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_detail_likes'] = 'user_detail_likes'
        the_user = User.objects.get(id=self.kwargs.get('pk'))
        context['the_user'] = the_user
        context['likes_count'] = Like.objects.filter(user=the_user).count()
        return context
    def get_queryset(self):
        the_user = User.objects.get(id=self.kwargs.get('pk'))
        return Like.objects.filter(user=the_user).order_by('-pk')

class UserDetailReadsView(LoginRequiredMixin, ListView):
    model = Read
    context_object_name = 'reads'
    template_name = 'htmls/user_detail.html'
    paginate_by = 50
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_detail_reads'] = 'user_detail_reads'
        the_user = User.objects.get(id=self.kwargs.get('pk'))
        context['the_user'] = the_user
        context['reads_count'] = Read.objects.filter(user=the_user).count()
        return context
    def get_queryset(self):
        the_user = User.objects.get(id=self.kwargs.get('pk'))
        return Read.objects.filter(user=the_user).order_by('-pk')

class UserUpdateView(FormUpdateView):
    model = User
    fields = ['username']
    def get_object(self, queryset=None):
        return self.request.user
    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': self.request.user.pk})

class BaseWorkIndex(ListView):
    model = Work
    context_object_name = 'works'
    template_name = 'htmls/work_index.html'
    paginate_by = 50
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class WorkIndexView(BaseWorkIndex):
    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs), 'index': 'index'}
    def get_queryset(self):
        return super().get_queryset().order_by('creator')

class WorkIndexPostedView(BaseWorkIndex):
    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs), 'index_posted': 'index_posted'}
    def get_queryset(self):
        return super().get_queryset().annotate(post_count=Count('post')).order_by('-post_count')

class WorkIndexReadView(BaseWorkIndex):
    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs), 'index_read': 'index_read'}
    def get_queryset(self):
        return super().get_queryset().annotate(read_count=Count('read')).order_by('-read_count', '-pk')

class WorkIndexScenedView(BaseWorkIndex):
    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs), 'index_scened': 'index_scened'}
    def get_queryset(self):
        return super().get_queryset().annotate(scened_count=Count('scene')).order_by('-scened_count', '-pk')
    
class WorkSearchView(ListView):
    model = Work
    context_object_name = 'search_results'
    template_name = 'htmls/work_index.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Work.objects.filter(Q(title__icontains=query) | Q(creator__icontains=query)).order_by('creator', 'title')
        else:
            return Work.objects.none()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['work_search'] = 'work_search'
        context['search_query'] = self.request.GET.get('q', '')
        return context

class WorkDetailView(ListView):
    model = Post
    template_name = 'htmls/work_detail.html'
    context_object_name = 'posts'
    paginate_by = 20
    def get_queryset(self):
        the_work = Work.objects.get(pk=self.kwargs.get('pk'))
        return Post.objects.filter(work=the_work, hide=False).order_by('-updated_at')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['work_detail'] = 'work_detail'
        the_work = Work.objects.get(pk=self.kwargs.get('pk'))
        context['the_work'] = the_work
        context['posts_count'] = Post.objects.filter(work=the_work, hide=False).count()
        if self.request.user.is_authenticated:
            try:
                query = Post.objects.filter(user=self.request.user, work=the_work)
                if query.exists():
                    context['your_post'] = Post.objects.get(pk=query.first().pk)
            except Post.DoesNotExist:
                pass
        return context
    
class WorkDetailSceneView(ListView):
    model = Scene
    template_name = 'htmls/work_detail.html'
    context_object_name = 'scenes'
    paginate_by = 20
    def get_queryset(self):
        the_work = Work.objects.get(pk=self.kwargs.get('pk'))
        return Scene.objects.filter(work=the_work).annotate(poll_count=Count('poll')).order_by('-poll_count', '-pk')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['work_detail_scene'] = 'work_detail_scene'
        the_work = Work.objects.get(pk=self.kwargs.get('pk'))
        context['the_work'] = the_work
        context['reads_count'] = Read.objects.filter(work=the_work).count()
        if self.request.user.is_authenticated:
            try:
                read = Read.objects.get(user=self.request.user, work=the_work)
                context['read'] = read
            except Read.DoesNotExist:
                pass
            try:
                all_polls = Poll.objects.filter(user=self.request.user, scene__work=the_work)
                polls_dict = {poll.scene.pk: poll.pk for poll in all_polls}
                context['polls_dict'] = polls_dict
            except Poll.DoesNotExist:
                pass
        return context
    
class WorkCreateView(FormCreateView):
    model = Work
    form_class = WorkForm
    success_url = reverse_lazy('top')
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            return redirect(reverse('work_detail', kwargs={'pk': self.object.pk}))
        except IntegrityError:
            return redirect(reverse('error'))

class WorkUpdateView(FormUpdateView):
    model = Work
    form_class = WorkForm
    template_name = 'htmls/basic_form.html'
    def get_success_url(self):
        return reverse('work_detail', kwargs={'pk': self.object.pk})

class SceneCreateView(FormCreateView):
    model = Scene
    form_class = SceneForm
    success_url = reverse_lazy('top')
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['default_work'] = Work.objects.get(pk=self.kwargs.get('pk'))
        return kwargs
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            return redirect(reverse('work_detail_scene', kwargs={'pk': self.kwargs.get('pk')}))
        except IntegrityError:
            return redirect(reverse('error'))

class PostIndexView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'htmls/post_index.html'
    paginate_by = 20
    def get_queryset(self):
        return Post.objects.filter(hide=False).order_by('-pk')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent'] =  datetime.datetime.now() - datetime.timedelta(days=3)
        return context

class PostSearchView(ListView):
    model = Post
    context_object_name = 'search_results'
    template_name = 'htmls/post_index.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(Q(title__icontains=query)).order_by('-pk')
        else:
            return Post.objects.none()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_search'] = 'post_search'
        context['search_query'] = self.request.GET.get('q', '')
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'htmls/post_detail.html'
    context_object_name = 'post'
    def get(self, request, *args, **kwargs):
        post = self.get_object()
        if post.hide and post.user != self.request.user:
            return redirect('error')
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        the_post = Post.objects.get(pk=self.kwargs.get('pk'))
        if self.request.user.is_authenticated:
            try:
                liked = Like.objects.get(user=self.request.user, post=the_post)
                context['liked'] = liked
            except Like.DoesNotExist:
                pass
        context['liked_count'] = Like.objects.filter(post=the_post).count()
        return context
        
class PostCreateView(FormCreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('top')
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['default_work'] = Work.objects.get(pk=self.kwargs.get('pk'))
        return kwargs
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            return redirect(reverse('post_detail', kwargs={'pk': self.object.pk}))
        except IntegrityError:
            return redirect(reverse('error'))
        
class PostUpdateView(UserCheckMixin, FormUpdateView):
    model = Post
    form_class = PostForm
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            return redirect(reverse('post_detail', kwargs={'pk': self.kwargs.get('pk')}))
        except IntegrityError:
            return reverse('error')

class PostDeleteView(UserCheckMixin, DeleteView):
    model = Post
    template_name = 'htmls/basic_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('post_index')

class ClickCreateView(LoginRequiredMixin, CreateView):
    model = None
    fields = []
    template_name = 'htmls/basic_form.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            self.handle_additional_fields(form)
            form.save()
            return self.get_redirect_url()
        except IntegrityError:
            return redirect('error')
    def handle_additional_fields(self, form):
        pass
    def get_redirect_url(self):
        pass

class LikeCreateView(ClickCreateView):
    model = Like
    def handle_additional_fields(self, form):
        form.instance.post = Post.objects.get(pk=self.kwargs.get('pk'))
        if form.instance.post.hide:
            return redirect('error')
    def get_redirect_url(self):
        return redirect(reverse('post_detail', kwargs={'pk': self.kwargs.get('pk')}))

class ReadCreateView(ClickCreateView):
    model = Read
    def handle_additional_fields(self, form):
        form.instance.work = Work.objects.get(pk=self.kwargs.get('pk'))
    def get_redirect_url(self):
        return redirect(reverse('work_detail_scene', kwargs={'pk': self.kwargs.get('pk')}))

class PollCreateView(ClickCreateView):
    model = Poll
    def handle_additional_fields(self, form):
        form.instance.scene = Scene.objects.get(pk=self.kwargs.get('pk'))
    def get_redirect_url(self):
        scene = Scene.objects.get(pk=self.kwargs.get('pk'))
        return redirect(reverse('work_detail_scene', kwargs={'pk': scene.work.pk}))
    
class ClickDeleteView(LoginRequiredMixin, UserCheckMixin, DeleteView):
    template_name = 'htmls/basic_delete.html'
    success_url = reverse_lazy('top')
    model = None
    def get_success_url(self):
        pass
    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs.get('pk'))
    
class SceneDeleteView(ClickDeleteView):
    model = Scene
    def get_success_url(self):
        scene = self.get_object()
        return reverse('work_detail_scene', kwargs={'pk': scene.work.pk})

class LikeDeleteView(ClickDeleteView):
    model = Like
    def get_success_url(self):
        like = self.get_object()
        return reverse('post_detail', kwargs={'pk': like.post.pk})

class ReadDeleteView(ClickDeleteView):
    model = Read
    def get_success_url(self):
        read = self.get_object()
        return reverse('work_detail_scene', kwargs={'pk': read.work.pk})

class PollDeleteView(ClickDeleteView):
    model = Poll
    def get_success_url(self):
        poll = self.get_object()
        return reverse('work_detail_scene', kwargs={'pk': poll.scene.work.pk}) 
