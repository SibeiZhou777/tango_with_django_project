from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.models import Review
from django.db.models import Avg


def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    #context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories':category_list,'pages':page_list}
    return render(request, 'rango/index.html', context=context_dict)
    
def review(request):  
    review_list = Review.objects.order_by('-stars')[:5]
    result = Review.objects.aggregate(Avg("stars"))
    #context_dict = {'reviews':review_list}
    context_dict = {'avgStar':result,'reviews':review_list,'boldmessage': 'This review page has been put together by sybil.'}     
    # Return a rendered response to send to the client.        
    # We make use of the shortcut function to make our lives easier.        
    # Note that the first parameter is the template we wish to use.    
    return render(request, 'rango/review.html', context=context_dict)        

def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by sybil.'}
        # Return a rendered response to send to the client.
        # We make use of the shortcut function to make our lives easier.
        # Note that the first parameter is the template we wish to use.
    return render(request, 'rango/about.html', context=context_dict)
    
def show_category(request, category_name_slug):
    context_dict = {} 
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request,'rango/category.html',context_dict)