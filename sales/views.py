from django.http import JsonResponse
from .models import PurchasedInline

def get_sold_unit_price(request):
    item_type_id = request.GET.get('item_type')
    purchased = PurchasedInline.objects.filter(item_type_id=item_type_id).first()
    data = {
        'price': purchased.sold_unit_price if purchased else 0
    }
    return JsonResponse(data)
