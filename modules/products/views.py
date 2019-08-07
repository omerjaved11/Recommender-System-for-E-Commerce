"""
View for Products page
where All Products will be shown
Products can be cattered by category or sub category
Products are divided using pagination, One page contain 24 products
"""
import datetime
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.http import HttpResponse

from django.template import loader
import pandas as pd
from django.db.models import Avg
from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response,render
from django.core.paginator import Paginator
from modules.products.models import Product, ProductImage,CustomerProductReview,CustomerProductRating,Category,SubCategory,ProductRating,Color
from modules.shopping_cart.models import ShoppingCartEntry
from hitcount.views import HitCountDetailView
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
# Create your views here.

import pandas as pd
# from rake_nltk import Rake
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


def show_products(request, category_name='All'):
    """
    :param request:
    :param category_name: It can be Men, Women, Kid, Accessories, Ethnic Wear
    :return: All Products, containing Title, Image, Price of each product

    show_products returns All the products
    category_name is optional param, If given return Products of particular category

    """
    ctx={}
    cond = False

    categories = Category.objects.all()
    sub_categories=SubCategory.objects.all()
    colors = Color.objects.all()
    entries = ShoppingCartEntry.get_entries(request)
    try:
        total_quantity = sum([entry['quantity'] for entry in entries])
    except:
        total_quantity = 0

    # print(category_name)
    final_products = []
    if category_name != 'All':
        cat_id = Category.objects.filter(category_name=category_name).first()
        sub_cat_id = cat_id.sub_categories.all()
        for sub_id in sub_cat_id.all():
            if request.GET.get('search-product'):
                cond = True

                search_tag = request.GET.get('search-product')
                products = sub_id.products.all().filter(Q(product_title__icontains=search_tag) |
                                                  Q(product_sku_no__icontains=search_tag) |
                                                  Q(product_description__icontains=search_tag)
                                                  # Q(product_clothes_print_id=search_tag)
                                                  )
            elif request.GET.getlist("color-filter"):
                cond = True

                clr_list = request.GET.getlist("color-filter")
                first_filter = sub_id.products.all().filter(product_color=clr_list[0])
                list_lenght = len(clr_list)
                for x in range(list_lenght):
                    products = first_filter.filter(product_color=clr_list[x])

            elif request.GET.get("sorting"):
                cond = True

                print(request.GET.get("sorting"))
                if request.GET.get("sorting")=='1':
                    products = sub_id.products.all().filter(product_selling_price__range=(0,500))
                elif request.GET.get("sorting")=='2':
                    products = sub_id.products.all().filter(product_selling_price__range=(500, 1000))
                elif request.GET.get("sorting")=='3':
                    products = sub_id.products.all().filter(product_selling_price__range=(1000, 1500))
                elif request.GET.get("sorting")=='4':
                    products = sub_id.products.all().filter(product_selling_price__range=(1500, 2000))
                elif request.GET.get("sorting") == '5':
                    products = sub_id.products.all().filter(product_selling_price__range=(2000, 3000000000000))
                elif request.GET.get("sorting") == 'Popularity':
                    products = sub_id.products.all().order_by('product_average_rating').reverse()
                elif request.GET.get("sorting") == 'Price: low to high':
                    products = sub_id.products.all().order_by('product_selling_price')
                else:
                    products = sub_id.products.all().order_by('product_selling_price').reverse()


            else:
                products =  sub_id.products.all()
            if products:
                count = products.count()
                ctx['message'] = str(count)
                for product in products:
                    image = ProductImage.objects.filter(product_id=product.product_id)
                    try:
                        image = image[image.count() - 1].product_image.url
                    except Exception as exp:
                        print(exp)
                        pass
                    final_products.append({"product_id": product.product_id, "product_title": product.product_title,
                                           "product_selling_price": product.product_selling_price, "product_image": image})

            else:
                ctx['message'] = '0'


    else:
        if request.GET.get('search-product'):
            cond = True

            search_tag = request.GET.get('search-product')
            products = Product.objects.filter(Q(product_title__icontains=search_tag) |
                                                    Q(product_sku_no__icontains=search_tag) |
                                                    Q(product_description__icontains=search_tag)
                                                    # Q(product_clothes_print_id=search_tag)
                                                    )
        elif request.GET.getlist("color-filter"):
            cond = True

            clr_list = request.GET.getlist("color-filter")
            first_filter = Product.objects.filter(product_color=clr_list[0])
            list_lenght = len(clr_list)
            for x in range(list_lenght):
                products = first_filter.filter(product_color=clr_list[x])

        elif request.GET.get("sorting"):
            cond = True

            print(request.GET.get("sorting"))
            if request.GET.get("sorting") == '1':
                products = Product.objects.filter(product_selling_price__range=(0, 500))
            elif request.GET.get("sorting") == '2':
                products = Product.objects.filter(product_selling_price__range=(500, 1000))
            elif request.GET.get("sorting") == '3':
                products = Product.objects.filter(product_selling_price__range=(1000, 1500))
            elif request.GET.get("sorting") == '4':
                products = Product.objects.filter(product_selling_price__range=(1500, 2000))
            elif request.GET.get("sorting") == '5':
                products = Product.objects.all().filter(product_selling_price__range=(2000, 3000000000000))
            elif request.GET.get("sorting") == 'Popularity':
                products = Product.objects.all().order_by('product_average_rating').reverse()
            elif request.GET.get("sorting") == 'Price: low to high':
                products = Product.objects.all().order_by('product_selling_price')
            else:
                products = Product.objects.all().order_by('product_selling_price').reverse()


        else:

            products = Product.objects.all()
        if products:
            count = products.count()
            ctx['message'] = str(count)
            for product in products:
                image = ProductImage.objects.filter(product_id=product.product_id)
                try:
                    image = image[image.count() - 1].product_image.url
                except Exception as exp:
                    print(exp)
                    pass
                final_products.append({"product_id": product.product_id, "product_title": product.product_title,
                                       "product_selling_price": product.product_selling_price, "product_image": image})



        else:
            ctx['message'] = ' 0'
    ctx.update({"products": final_products, "categories": categories, "sub_categories": sub_categories,"colors":colors,
           "entries": ShoppingCartEntry.get_entries(request),"total_quantity":total_quantity })
    paginator = Paginator(ctx['products'], 24)

    page = request.GET.get('page')
    ctx['products'] = paginator.get_page(page)
    referer = request.META.get('HTTP_REFERER')
    print(referer)
    # if(category_name=='All'):
    print('products' in referer)
    if('products' not in referer or category_name=='All' or cond ):
        print('Not')
        return render_to_response("products/product.html",ctx)
    else:
        return render_to_response("products/product1.html", {'products': ctx['products']})
    # return render(request,"products/product.html",ctx)

def sub_category_products(request,sub_catgory):
    """
    This functions filter Products of particular sub categories
    and display them of products page

    :param request:
    :param sub_catgory: Id of sub category
    :return: return Products for particular Sub Categories
    """
    ctx = {}
    cond = False
    categories = Category.objects.all()
    sub_categories=SubCategory.objects.all()
    colors = Color.objects.all()
    entries = ShoppingCartEntry.get_entries(request)
    try:
        total_quantity = sum([entry['quantity'] for entry in entries])
    except:
        total_quantity = 0

    if request.GET.get('search-product'):
        cond = True
        search_tag = request.GET.get('search-product')
        products = Product.objects.filter(Q(product_sub_category_id=sub_catgory) , Q(product_title__icontains=search_tag) |
                                          Q(product_sku_no__icontains=search_tag) |
                                          Q(product_description__icontains=search_tag)
                                          # Q(product_clothes_print_id=search_tag)
                                          )
    elif request.GET.getlist("color-filter"):
        cond = True

        clr_list = request.GET.getlist("color-filter")
        first_filter = Product.objects.filter(Q(product_sub_category_id=sub_catgory) ,Q(product_color=clr_list[0]))
        list_lenght = len(clr_list)
        for x in range(list_lenght):
            products = first_filter.filter(product_color=clr_list[x])

    elif request.GET.get("sorting"):
        cond = True

        print(request.GET.get("sorting"))
        if request.GET.get("sorting") == '1':
            products = Product.objects.filter(Q(product_sub_category_id=sub_catgory) ,Q(product_selling_price__range=(0, 500)))
        elif request.GET.get("sorting") == '2':
            products = Product.objects.filter(Q(product_sub_category_id=sub_catgory) ,Q(product_selling_price__range=(500, 1000)))
        elif request.GET.get("sorting") == '3':
            products = Product.objects.filter(Q(product_sub_category_id=sub_catgory) ,Q(product_selling_price__range=(1000, 1500)))
        elif request.GET.get("sorting") == '4':
            products = Product.objects.filter(Q(product_sub_category_id=sub_catgory) ,Q(product_selling_price__range=(1500, 2000)))
        elif request.GET.get("sorting") == '5':
            products = Product.objects.filter(Q(product_sub_category_id=sub_catgory) ,Q(product_selling_price__range=(2000, 3000000000000)))
        elif request.GET.get("sorting") == 'Popularity':
            products = Product.objects.filter(product_sub_category_id=sub_catgory).order_by('product_average_rating').reverse()
        elif request.GET.get("sorting") == 'Price: low to high':
            products = Product.objects.filter(product_sub_category_id=sub_catgory).order_by('product_selling_price')
        else:
            products = Product.objects.filter(product_sub_category_id=sub_catgory).order_by('product_selling_price').reverse()

    else:
        products = Product.objects.filter(product_sub_category_id=sub_catgory)

    final_products = []
    if products:
        count = products.count()
        sub_category = SubCategory.objects.get(sub_category_id=sub_catgory)
        ctx['message'] = str(count) +  '  Item(s) found.'
        for p in products:
            image = ProductImage.objects.filter(product_id=p.product_id)
            try:
                image = image[image.count() - 1].product_image.url
            except:
                pass
            final_products.append({"product_id": p.product_id, "product_title": p.product_title,
                                   "product_selling_price": p.product_selling_price, "product_image": image})
    else:

        ctx['message'] = ' 0 Items found.'
    ctx.update({"products": final_products, "categories": categories, "sub_categories": sub_categories,"colors":colors,
           "entries": ShoppingCartEntry.get_entries(request),"total_quantity":total_quantity})
    paginator = Paginator(ctx['products'], 24)
    page = request.GET.get('page')
    ctx['products'] = paginator.get_page(page)

    referer = request.META.get('HTTP_REFERER')
    print(referer)
    # if(category_name=='All'):
    print('products' in referer)

    if('products' not in referer or cond):
        print('Not')

        return render_to_response("products/product.html",ctx)
    else:
        return render_to_response("products/product1.html", {'products': ctx['products']})

    # return render(request,"products/product1.html", ctx)


def product_details(request, product_id):
    """
    :param request:
    :param product_id: Contain the unique Id of a particular product
    :return: Details of a Product => Title, Price, Description, Ratings , Reviews, images of Product,


    This function will execute when user click on only product for its detail
    A Products details of particular product will be loaded.

    """
    entries = ShoppingCartEntry.get_entries(request)


    try:
        total_quantity = sum([entry['quantity'] for entry in entries])
    except:
        total_quantity = 0

    count_hit = True
    try:
        df = pd.DataFrame(list(CustomerProductRating.objects.all().values()))
        productmat = df.pivot_table(index='user_id', columns='product_id_id', values='product_rating_id_id',aggfunc='first').astype(float)
        df.product_rating_id_id = df.product_rating_id_id.astype(int)
        ratings = pd.DataFrame(df.groupby('product_id_id')['product_rating_id_id',].mean())
        ratings['num of ratings'] = pd.DataFrame(df.groupby('product_id_id')['product_rating_id_id'].count())
        productcorr = productmat.corr()

        corrMat = pd.DataFrame(productcorr[int(product_id)])
        corrMat.columns = ['Correlation']
        corrMat.dropna(inplace=True)

        corrMat = corrMat.join(ratings['num of ratings'])
        related_prod = corrMat[corrMat['num of ratings'] > 2].sort_values('Correlation', ascending=False)
        related_prod.drop(int(product_id), inplace=True)
        # related_products = Product.objects.filter(product_sub_category_id=product.product_sub_category_id).order_by('?')[:8]
        related_products = Product.objects.filter(pk__in=related_prod.index.values.tolist())

    except Exception as exp:
        related_products = []
        print(exp)

    try:
        content_rs_p_list = crs_recommendations(int(product_id))
    except:
        content_rs_p_list = []
    try:
        content_rs_products = Product.objects.filter(pk__in=content_rs_p_list)
    except Exception as exp:
        content_rs_products = []
        print(exp)



    image = ProductImage.objects.filter(product_id=product_id)
    product = Product.objects.get(product_id=product_id)
    # print(request.session)
    # print(request.session['Recents'])

    if not 'Recents' in request.session or not request.session['Recents']:
        request.session['Recents'] = [product_id]
    else:
        saved_list = request.session['Recents']
        if product_id not in saved_list:
            saved_list.append(product_id)
        request.session['Recents'] = saved_list
    # try:
    #     card = Card.objects.get(id=request.session['card'])
    # except (KeyError, Card.DoesNotExist):
    #     card = None
    # request.session.setdefault('history', []).append(product)
    # request.session.modified = True
    # if not 'Recents' in request.session or not request.session['Recents']:
    #     request.session['Recents'] = [product]
    # else:
    #     request.session['Recents'].append(product)

    cloth_sizes = product.product_size.all()
    cloth_colors = product.product_color.all()
    review = CustomerProductReview.objects.filter(product_id=product.product_id)
    rating = CustomerProductRating.objects.filter(product_id=product.product_id)
    reviewscount = review.count()
    count = 1
    result = 0
    for rate in rating:
        result = result + int(rate.product_rating_id.product_rating_id)
        count = count + 1

    if count == 1:
        pass
    else:
        count = count - 1

    average_rating = round(result / count)

    for content_rs_product in content_rs_products:
        image2 = ProductImage.objects.filter(product_id=content_rs_product.product_id)
        image_count = image2.count()
        try:
            # set image in desription for saving memory or extra stuff
            content_rs_product.product_description = image2[image_count - 1].product_image.url
            print(content_rs_product.product_description)

        except Exception as exp:
            print(exp)
            pass
    print('contentRS',content_rs_products)

    for related_product in related_products:
        image2 = ProductImage.objects.filter(product_id=related_product.product_id)
        image_count = image2.count()
        try:
            # set image in desription for saving memory or extra stuff
            related_product.product_description = image2[image_count - 1].product_image.url
            print(related_product.product_description)

        except Exception as exp:
            print(exp)
            pass
    print('related',related_products)


    ratinglist=[]
    if average_rating == 0:
        count = 0
        ratinglist=[0,0,0,0,0]
    else:
        for n in range(5):
            try:
                temp = CustomerProductRating.objects.filter(product_rating_id=(n+1), product_id=product_id).count()
                temp = (temp/count)*100
                temp = round(temp)
                ratinglist.append(temp)
            except:
                pass

    print(ratinglist)

    hit_count = HitCount.objects.get_for_object(product)
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    ctx={"product":product,"sizes":cloth_sizes,"colors":cloth_colors,
         "images":image,"reviews":review,"rating":average_rating,
         "related_products":related_products,"recents":productsfromsession(request),"no_users_rating":count,
         "ratinglist":ratinglist,"reviewscount":reviewscount,"content_rs_products":content_rs_products,
         "entries":ShoppingCartEntry.get_entries(request),"total_quantity":total_quantity}
    productsfromsession(request)

    return render(request,"products/product-detail.html",ctx)
#
# @login_required
# def add_review_rating(request):
#     if request.method == 'GET':
#         products = Product.objects.all()
#         ctx = {'products':products}
#         return render(request,'products/add_rating_review.html',ctx)
#
#     elif request.method == 'POST':
#
#         rating = request.POST['rating']
#         product_id = request.POST['products']
#         new_review = request.POST['review']
#         prod = Product.objects.get(product_id=product_id)
#         customer_product_rating = CustomerProductRating()
#         customer_product_rating.product_id=prod
#         customer_product_rating.product_rating_id = ProductRating.objects.get(product_rating_id=rating)
#         customer_product_rating.user=request.user
#         customer_product_rating.save()
#
#         review = ProductReview()
#         review.product_review_text=new_review
#         review.save()
#
#         customer_product_review=CustomerProductReview()
#         customer_product_review.product_id=prod
#         customer_product_review.user=request.user
#         customer_product_review.product_review_id=review
#         customer_product_review.date = datetime.datetime.now()
#
#         customer_product_review.save()
#
#
#         average_rating = CustomerProductRating.objects.filter(product_id=prod).aggregate(Avg('product_rating_id'))
#         prod.product_average_rating = average_rating['product_rating_id__avg']
#         print(average_rating)
#         prod.save()
#
#         print(rating,product_id,review)
#         products = Product.objects.all()
#         ctx = {'products':products,"entries":ShoppingCartEntry.get_entries(request)}
#         return render(request,'products/add_rating_review.html',ctx)


def color_filter(request):
    if request.GET.get('color-filter'):
        print("ajao")
        # list = request.GET.getlist('color-filter')
        # print("list of colors")
        # print(list)
    return render(request, "products/product.html", {})

def weeklypopular(request):
    """
      Landing page of website contains many items,
      Popularity Base Recommender systems,
      Links to other pages
      :param request:
      :return: Most popular Products
      """
    pridected_products = []

    period = timezone.now() - timedelta(days=7)
    most_visited_in_7days = Product.objects.filter(hit_count_generic__hit__created__gte=period)\
        .annotate(counts=models.Count('hit_count_generic__hit')
    ).order_by('-counts')


    for p in most_visited_in_7days.all()[:10]:

        image = ProductImage.objects.filter(product_id=p.product_id)
        image_count = image.count()
        try:
            image = image[image_count - 1].product_image.url
        except Exception as e:
            print(e)
            pass

        pridected_products.append({"p_id": p.product_id, "p_title": p.product_title, "p_price": p.product_selling_price,
                                    "p_image": image})
    return pridected_products
    # ctx = {"products": pridected_products}
    # # template=loader.get_template('products/rs.html')
    # # return render_to_response(template,ctx)
    # return ctx
    # return render(request, 'products/rs.html', ctx)




def productsfromsession(request):
    if request.session['Recents']:
        p_id = request.session['Recents']
        print('sessions',p_id)
        recent_products = Product.objects.filter(pk__in=p_id)[:10]


        for recent_product in recent_products:
            image2 = ProductImage.objects.filter(product_id=recent_product.product_id)
            image_count = image2.count()
            try:
                # set image in desription for saving memory or extra stuff
                recent_product.product_description = image2[image_count - 1].product_image.url
                print(recent_product.product_description)

            except Exception as exp:
                print(exp)
                pass
        return recent_products
    return None


def preprocess_contentRS(x):
    new_list = []
    for word in x.lower().split():
        #       print(word) word = word.lower()
        if word not in ['the', 'in', 'and'] and word not in new_list:
            new_list.append(word)

    return ' '.join(new_list)


def crs_recommendations(p_id):
    df = pd.DataFrame(list(Product.objects.all().values()))

    df = df[['product_id', 'product_description', 'product_title']]
    # discarding the commas between the actors' full names and getting only the first three names
    # df['Actors'] = df['Actors'].map(lambda x: x.split(',')[:3])
    df['product_title'] = df.product_title.map(lambda x: [x[:x.find('(')]] if ('(' in x) else [x.split(':')[0][:-4]])
    # putting the genres in a list of words
    # df['Genre'] = df['Genre'].map(lambda x: x.lower().split(','))
    df['product_description'] = df.product_description.map(lambda x: [i.split(':')[-1] for i in x.split('\n')])
    # df['Director'] = df['Director'].map(lambda x: x.split(' '))

    # merging together first and last name for each actor and director, so it's considered as one word
    # and there is no mix up between people sharing a first name
    for index, row in df.iterrows():
        row['product_title'] = [x.lower().replace(' ', '') for x in row['product_title']]
        row['product_description'] = ''.join(row['product_description']).lower()

    df.set_index('product_id', inplace=True)

    df['bag_of_words'] = ''
    columns = df.columns
    for index, row in df.iterrows():
        words = ''
        for col in columns:
            words = words + ' '.join(row[col]) + ' '

        row['bag_of_words'] = words

    df.drop(columns=[col for col in df.columns if col != 'bag_of_words'], inplace=True)
    df['bag_of_words'] = df.bag_of_words.apply(preprocess_contentRS)

    # instantiating and generating the count matrix
    count = CountVectorizer()
    count_matrix = count.fit_transform(df['bag_of_words'])

    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    # creating a Series for the products p_id so they are associated to an ordered numerical
    # list I will use later to match the indexes
    indices = pd.Series(df.index)

    recommended_products = []

    # gettin the index of the movie that matches the p_id
    idx = indices[indices == p_id].index[0]

    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending=False)

    # getting the indexes of the 10 most similar preoducts
    top_10_indexes = list(score_series.iloc[1:11].index)

    # populating the list with the p_id of the best 10 matching products
    for i in top_10_indexes:
        recommended_products.append(list(df.index)[i])

    return recommended_products