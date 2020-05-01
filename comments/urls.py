from django.shortcuts import render
from django.urls import path
from . import views
# Create your views here.

urlpatterns = [
    		
    	path('property/<int:id>/', views.property_comments, name="property-comments"),#new url
    	path('seller-reviews/<int:id>/', views.seller_reviews, name="seller-reviews"),#new url
		
    ]