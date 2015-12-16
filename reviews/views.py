import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Wine, Review
from .forms import ReviewForm


def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'reviews/review_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk = review_id)
    context = {'review': review}
    return render(request, 'reviews/review_detail.html', context)


def wine_list(request):
    wines = Wine.objects.order_by('-name')
    context = {'wine_list': wines}
    return render(request, 'reviews/wine_list.html', context)


def wine_detail(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id )
    form = ReviewForm()
    context = {'wine': wine, 'form':form}
    return render(request, 'reviews/wine_detail.html', context)


@login_required
def add_review(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    form = ReviewForm(request.POST)

    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = request.user.username
        review = Review()
        review.wine = wine
        review.comment = comment
        review.user_name = user_name
        review.rating = rating
        review.pub_date = datetime.datetime.now()

        review.save()

        return HttpResponseRedirect(reverse('reviews:wine_detail', args=(wine_id,)))

    return render(request, 'reviews/wine_detail.html', {'wine':wine, 'form':form})


def user_review_list(request, username=None):
    if not username:
        username = request.user.username

    latest_reviews_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    context = {"latest_reviews_list": latest_reviews_list, "username": username}

    return render(request, 'reviews/user_review_list.html',context)



