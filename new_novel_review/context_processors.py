from .models import Work, Poll, Post, Like, Read

def side_works(request):
    side_works = Work.objects.all().order_by('-pk')[:10]
    return {'side_works': side_works}

def side_polls(request):
    side_polls = Poll.objects.all().order_by('-pk')[:10]
    return {'side_polls': side_polls}

def side_posts(request):
    side_posts = Post.objects.filter(hide=False).order_by('-pk')[:10]
    return {'side_posts': side_posts}

def side_likes(request):
    side_likes = Like.objects.all().order_by('-pk')[:10]
    return {'side_likes': side_likes}

def side_reads(request):
    side_reads = Read.objects.all().order_by('-pk')[:10]
    return {'side_reads': side_reads}