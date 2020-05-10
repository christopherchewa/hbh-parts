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

	sort_get = request.GET.get('sort')
	dir_get = request.GET.get('dir')

	if request.GET.get('sort') is not None and request.GET.get('dir') is not None:
		if dir_get == "asc":
			queryset = queryset.order_by("-"+sort_get)
		elif dir_get == "desc":
			queryset = queryset.order_by(sort_get)
		return queryset
	else:
		queryset = queryset.order_by("-updated_at")

	return queryset

def match_util():

	pass

def kshs_formatter(price_value):

	price_unformatted = price_value
	price_len = len(str(price_unformatted))
	if price_len >=7 and price_len <=9:
		p = price_unformatted/1000000
		price_str = "{:.2f}".format(p)
		price_parts = price_str.split('.')
		if price_parts[1] == "00":
			price_format = "{}".format(price_parts[0])
		else:
			price_format = "{}".format(price_str)
		price = "{} {}".format(price_format, "M")
	elif price_len >=10 and price_len <=12:
		p = price_unformatted/1000000000
		price_str = "{:.2f}".format(p)
		price_parts = price_str.split('.')
		if price_parts[1] == "00":
			price_format = "{}".format(price_parts[0])
		else:
			price_format = "{}".format(price_str)
		price = "{} {}".format(price_format, "B")

	elif price_len <= 6:
		price = f"{price_unformatted:,d}"

	price_final = "{} {}".format("Kshs. ", price)

	return price_final
