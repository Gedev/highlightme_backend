from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from api.models import HighlightDetails
import json

# Create your views here.


def get_highlights(request, **kwargs):
    try:
        report_code = kwargs.get('reportcode')
        print(report_code)
        if report_code:
            highlights = HighlightDetails.objects.filter(report_id=report_code).values()
            return JsonResponse(list(highlights), safe=False)
        else:
            return JsonResponse({'error': 'Report code not provided'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)



