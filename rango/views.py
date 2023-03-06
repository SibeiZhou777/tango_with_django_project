from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.models import Review
from django.db.models import Avg
from rango.forms import CategoryForm,PageForm,ReviewForm
from django.shortcuts import redirect


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
    print(result)
    #context_dict = {'reviews':review_list}
    # Return a rendered response to send to the client.        
    # We make use of the shortcut function to make our lives easier.        
    # Note that the first parameter is the template we wish to use.    
    form = ReviewForm()
    # A HTTP POST?
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect('/rango/review/')
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)
    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    context_dict = {'form': form,'avgStar':result,'reviews':review_list,'boldmessage': 'This review page has been put together by sybil.'}   
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


# def add_category(request):
    # form = CategoryForm()
    # # A HTTP POST?
    # if request.method == 'POST':
        # form = CategoryForm(request.POST)
        # # Have we been provided with a valid form?
        # if form.is_valid():
            # # Save the new category to the database.
            # form.save(commit=True)
            # # Now that the category is saved, we could confirm this.
            # # For now, just redirect the user back to the index view.
            # return redirect('/rango/')
        # else:
            # # The supplied form contained errors -
            # # just print them to the terminal.
            # print(form.errors)
    # # Will handle the bad form, new form, or no form supplied cases.
    # # Render the form with error messages (if any).
    # return render(request, 'rango/add_category.html', {'form': form})
    
