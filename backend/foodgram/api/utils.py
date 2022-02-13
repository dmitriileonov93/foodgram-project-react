import io

from django.db.models import Sum
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import permissions
from rest_framework.decorators import action

from app.models import IngredientInRecipe


def get_shopping_cart(user):
    shopping_cart_queryset = IngredientInRecipe.objects.filter(
        recipe__recipe_in_cart__user=user)
    shopping_cart_list = shopping_cart_queryset.values(
        'ingredient__name',
        'ingredient__measurement_unit'
    ).annotate(amount=Sum('amount'))
    return shopping_cart_list


class RecpieDownloadPDFMixin:
    @action(
        detail=False,
        permission_classes=[permissions.IsAuthenticated, ],
    )
    def download_shopping_cart(self, request):
        pdfmetrics.registerFont(TTFont(
            'Helvetica2', '/app/fonts/Helvetica.ttc'))
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
        text_obj = c.beginText()
        text_obj.setTextOrigin(inch, inch)
        text_obj.setFont('Helvetica2', 14)
        text_obj.textLine('Список покупок:')
        shopping_cart_list = get_shopping_cart(request.user)
        lines = ['', ]
        for ingr in shopping_cart_list:
            lines.append(
                f"{ingr['ingredient__name']} - {ingr['amount']} "
                f"{ingr['ingredient__measurement_unit']}")
        for line in lines:
            text_obj.textLine(line)
        c.drawText(text_obj)
        c.showPage()
        c.save()
        buffer.seek(0)
        return FileResponse(
            buffer, as_attachment=True, filename='shopping_cart.pdf'
        )
