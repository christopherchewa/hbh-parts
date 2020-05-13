from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import User, UserProfile, PropertyEntry, Request, Match

def paginator_util(request, queryset, items_per_page=10):
	page = request.GET.get('page', 1)
	paginator = Paginator(queryset, items_per_page)
	try:
		matches = paginator.page(page)
	except PageNotAnInteger:
		matches = paginator.page(1)
	except EmptyPage:
		matches = paginator.page(paginator.num_pages)

	return matches


def sort_tables_util(request, queryset):
	sort_get = request.GET.get('sort', None)
	dir_get = request.GET.get('dir', None)

	if sort_get and dir_get:
		if dir_get == "asc":
			queryset = queryset.order_by("-"+sort_get)
		elif dir_get == "desc":
			queryset = queryset.order_by(sort_get)
		else:
			pass
	return queryset


def ksh_inside(price_unformatted, shorthand=None, divisor=None):
	p = price_unformatted/divisor
	price_str = "{:.2f}".format(p)
	price_parts = price_str.split('.')#returns a list of 2, before and after decimal points
	if price_parts[1] == "00":
		price_format = "{}".format(price_parts[0])#no need for decimal points if its .00
	else:
		price_format = "{}".format(price_str)#if there's decimal points, dont remove them

	price = "{} {}".format(price_format, shorthand)

	return price

def kshs_formatter(price_value):

	price_unformatted = price_value
	price_len = len(str(price_unformatted))
	#convert million to M
	if price_len >=7 and price_len <=9:
		 price = ksh_inside(price_unformatted, shorthand="M", divisor=1000000)
	#convert billion to B
	elif price_len >=10 and price_len <=12:
		price = ksh_inside(price_unformatted, shorthand="B", divisor=1000000000)
	#leave commas if less than a million
	elif price_len <= 6:
		price = f"{price_unformatted:,d}"
	#add Kshs. to final value
	price_final = "{} {}".format("Kshs. ", price)

	return price_final


def match_util():
	pass
