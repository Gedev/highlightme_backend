from django.http import JsonResponse
from api.models import HighlightDetails
import json

from report.translations import TRANSLATIONS


def detect_language(request):

    accept_language = request.headers.get('Accept-Language', '')
    languages = [lang.split(';')[0] for lang in accept_language.split(',')]

    supported_languages = ['fr', 'en']

    for lang in languages:
        if lang[:2] in supported_languages:
            return lang[:2]

    return 'en'


def translate(highlights, language="fr"):
    if language == "fr":
        for item in highlights:
            item['title'] = TRANSLATIONS.get(item['title'], item['title'])
            item['description'] = TRANSLATIONS.get(item['description'], item['description'])
    return highlights


def get_highlights(request, **kwargs):
    try:
        report_code = kwargs.get('reportcode')
        if report_code:
            highlights = HighlightDetails.objects.filter(report_id=report_code).values()
            highlights_list = list(highlights)

            language = detect_language(request)
            translated_highlights = translate(highlights_list, language=language)
            return JsonResponse(translated_highlights, safe=False)
        else:
            return JsonResponse({'error': 'Report code not provided'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
