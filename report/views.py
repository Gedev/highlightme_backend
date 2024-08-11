from django.http import JsonResponse
from api.models import HighlightDetails, IndividualHighlight
import json

from api.utils.difficulties import get_difficulty_name
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
        difficulty = request.GET.get('difficulty')
        if report_code:
            # Fetch combat highlights
            combat_highlights = HighlightDetails.objects.filter(report_id=report_code, difficulty=difficulty).values()
            combat_highlights_list = list(combat_highlights)

            # Fetch individual highlights
            individual_highlights = IndividualHighlight.objects.filter(report_id=report_code, difficulty=difficulty).values()
            individual_highlights_list = list(individual_highlights)

            # Extract zone name and difficulty from combat highlights (assuming all have the same zone and difficulty)
            if combat_highlights_list:
                zone_name = combat_highlights_list[0].get('zone_name', 'Unknown Zone')
                difficulty_value = combat_highlights_list[0].get('difficulty', 'Unknown Difficulty')
                difficulty_name = get_difficulty_name(difficulty_value)
            else:
                zone_name = 'Unknown Zone'
                difficulty_name = 'Unknown Difficulty'

            # Detect language and translate highlights
            language = detect_language(request)

            # Ensure translation function handles list of dicts properly
            translated_combat_highlights = translate(combat_highlights_list, language=language)

            return JsonResponse({
                "zone_name": zone_name,
                "difficulty": difficulty_name,
                "combat_highlights": translated_combat_highlights,
                "individual_highlights": individual_highlights_list
            }, safe=False)
        else:
            return JsonResponse({'error': 'Report code not provided'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        # Capture and log any exceptions for better debugging
        # logger.error(f'Unexpected error in get_highlights: {e}')
        return JsonResponse({'error': str(e)}, status=500)
