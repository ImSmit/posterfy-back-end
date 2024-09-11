

from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Product
from base.serializers import ProductSerializer
from .utils import get_or_none

@api_view(["GET"])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)

@api_view(['GET', 'POST'])
def getProduct(request, pk):

    product = get_or_none(Product, pk)
    if product:
        serializer = ProductSerializer(product, many=False)
    else:
        return Response({"status": False, "detail": "Product not found"}, status=404)
    
    return Response({"status":True, "data":serializer.data})