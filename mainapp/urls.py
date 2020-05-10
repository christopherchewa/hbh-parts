from django.shortcuts import render
from django.urls import path
from . import views
from comments import views as comments_views
# Create your views here.

urlpatterns = [
    path('', views.index, name="home"),
    path('buy/', views.index, name="home-buy"),
    path('sell/', views.index, name="home-sell"),
    path('faqs/', views.faqs, name="faqs"),
    path('contact/', views.contact, name="contact"),
    path('faqs/', views.faqs, name="faqs"),
    path('terms/', views.terms, name="terms"),
    path('contact/', views.contact, name="contact"),
    path('account/', views.account, name="account"),
    path('sign-in/', views.sign_in, name="sign-in"),
    path('sign-out/', views.sign_out, name="sign-out"),
    path('select-type/<str:user_type>/', views.select_type, name="select-type"),
    path('register/', views.register, name="register"),
    path('pricing/', views.pricing, name="pricing"),
    path('add-listing/', views.add_listing, name="add-listing"),
    path('edit-listing/<int:id>/', views.edit_listing, name="edit-listing"),#new url
    path('explore/', views.explore, name="explore"),
    path('unmatched-requests/', views.unmatched_requests, name="unmatched-requests"),
    path('all-requests/', views.all_requests, name="all-requests"),
    path('all-properties/', views.all_properties, name="all-properties"),
    path('all-requests/remove/<int:id>/', views.remove_request, name="remove-request"),
    path('all-requests/activate/<int:id>/', views.activate_request, name="activate-request"),
    path('view-match/', views.view_match, name="view-match"),
    path('engage/<int:id>/', views.engage, name="engage"),
    path('view-contact/', views.view_contact, name="view-contact"),
    path('decline-offer/<int:id>/', views.decline_offer, name="decline-offer"),
    
    path('list-inside/<int:id>/', views.list_inside, name="list-inside"),
    path('account/', views.account, name="account"),
    path('matches/', views.matches, name="matches"),
    path('news/', views.news, name="news"),

    path('favourite/', views.favourite, name="favourite"),
    path('add-review/', comments_views.add_review, name="add-review"),
    path('set-rating/', comments_views.set_rating, name="set-rating"),
    

    path('listings/', views.listings, name="listings"),#to favourites page

    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),


    #temporary urls for errors: 400, 403, 404, 500
    path('E400/', views.error_400, name="error_400"),
    path('E403/', views.error_403, name="error_403"),
    path('E404/', views.error_404, name="error_404"),
    path('E500/', views.error_500, name="error_500"),
]