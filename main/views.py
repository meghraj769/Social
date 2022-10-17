from django.http import HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import *
from django.views import View
from .forms import PostForm, CommentForm, ProfileForm
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.

class ProfileView(View):
	def get(self, request, pk, *args, **kwargs):
		profile = UserProfile.objects.get(pk=pk)
		user = profile.user
		posts = Post.objects.filter(author=user)

		followers = profile.followers.all()

		num_followers = len(followers)

		following = request.user in followers

		context = {
			'user': user,
			'posts': posts,
			'profile': profile,
			'num_followers' : num_followers,
			'following': following,
		}

		return render(request, 'main/profile.html', context)

class PostList(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		logged_in_user_id = request.user.id
		posts = Post.objects.filter(
			author__profile__followers__in = [logged_in_user_id]
		).order_by('-created_on')
		form = PostForm()

		for post in posts:
			post.does_like = request.user in post.likers.all()
			post.likes = len(post.likers.all())

		context = {
			'post_list' : posts,
			'form' : form,
		}

		return render(request, 'main/post_list.html', context)

	def post(self, request, *args, **kwargs):
		posts = Post.objects.all().order_by('-created_on')
		form = PostForm(request.POST)

		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.author = request.user
			new_post.save()

			context = {
				'post_list' : posts,
				'form' : form,
			}

			return render(request, 'main/post_list.html', context)


class PostDetailView(LoginRequiredMixin, View):
	def get(self, request, pk, *args, **kwargs):
		post = Post.objects.get(pk=pk)
		form = CommentForm()
		comments = Comment.objects.filter(post=post).order_by('-created_on')
		user_likers = post.likers.all()
		likes = len(user_likers)

		liking = request.user in user_likers


		context = {
			'post' : post,
			'form': form,
			'comments' : comments,
			'likes' : likes,
			'liking' : liking,
		}

		return render(request, 'main/post_detail.html', context)

	def post(self, request, pk, *args, **kwargs):
		post = Post.objects.get(pk=pk)
		form = CommentForm(request.POST)

		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.author = request.user
			new_comment.post = post
			new_comment.save()

		comments = Comment.objects.filter(post=post).order_by('-created_on')

		context = {
			'post' : post,
			'form' : form,
			'comments' : comments,
		}

		return render(request, 'main/post_detail.html', context)


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	# fields = ['body']
	template_name = 'main/post_edit.html'
	form_class = PostForm

	def get_success_url(self):
		pk = self.kwargs['pk']
		return reverse_lazy('post_detail', kwargs={'pk' : pk})

	def test_func(self):
		post = self.get_object()
		return post.author == self.request.user

class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = UserProfile
	template_name = 'main/profile_edit.html'
	form_class = ProfileForm

	def get_success_url(self, **kwargs):
		pk = self.kwargs['pk']
		return reverse_lazy('profile', kwargs ={'pk':pk})

	def test_func(self):
		profile = self.get_object()
		return self.request.user == profile.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	template_name = 'main/post_delete.html'
	success_url = reverse_lazy('post_list')

	def get_context_data(self, **kwargs):
		context =  super().get_context_data(**kwargs)
		context['post_pk']  = self.kwargs['pk']
		return context

	def test_func(self):
		post = self.get_object()
		return post.author == self.request.user

class CommentDeleteView(UserPassesTestMixin, DeleteView):
	model = Comment
	template_name = 'main/comment_delete.html'

	def test_func(self):
		comment = self.get_object()
		return comment.author == self.request.user or comment.post.author == self.request.user 

	def get_context_data(self, **kwargs):
		context =  super().get_context_data(**kwargs)
		context['post_pk']  = self.kwargs['post_pk']
		return context

	def get_success_url(self):
		pk = self.kwargs['post_pk']
		return reverse_lazy('post_detail', kwargs={'pk' : pk})


class AddFollower(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		profile = UserProfile.objects.get(pk=pk)
		profile.followers.add(request.user)

		return redirect('profile', pk=profile.pk)
		
class RemoveFollower(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		profile = UserProfile.objects.get(pk=pk)
		profile.followers.remove(request.user)

		return redirect('profile', pk=profile.pk)


class LikePost(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		post = Post.objects.get(pk=pk)
		post.likers.add(request.user)

		# return redirect('post_detail', pk=post.pk)
		# return HttpResponseRedirect(self.request.path_info)
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class UnLikePost(LoginRequiredMixin, View):
	def post(self, request, pk, *args, **kwargs):
		post = Post.objects.get(pk=pk)
		post.likers.remove(request.user)

		# return redirect('post_detail', pk=post.pk)
		# return HttpResponseRedirect(self.request.path_info)
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class UserSearch(View):
	def get(self, request, *args, **kwargs):
		query = self.request.GET['query']
		profiles = UserProfile.objects.filter(
			Q(user__username__icontains=query)
		)

		context = {
			'profiles' : profiles,
		}

		return render(request, 'main/search_results.html', context)


class ListFollowers(View):
	def get(self, request, pk, *args, **kwargs):
		profile = User.objects.get(pk=pk)
		followers = profile.profile.followers.all()

		context = {
			'profile': profile,
			'followers': followers,
		}

		return render(request, 'main/followers_list.html', context)




