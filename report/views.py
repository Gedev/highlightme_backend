import logging

from django.http import JsonResponse
from api.models import HighlightDetails, IndividualHighlight
import json

from api.utils.difficulties import get_difficulty_name
from highlightme.settings import BASE_URL_FRONT
from report.translations import TRANSLATIONS
logger = logging.getLogger('django.request')


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
    logger.info({request})
    try:
        report_code = kwargs.get('report_code')
        difficulty = request.GET.get('difficulty')

        if report_code:
            # Récupérer les highlights de fight
            fight_highlights = HighlightDetails.objects.filter(report_id=report_code, difficulty=difficulty, fight_id__isnull=False).values()
            fight_highlights_list = list(fight_highlights)

            # Récupérer les highlights de raid
            raid_highlights = HighlightDetails.objects.filter(report_id=report_code, difficulty=difficulty, fight_id__isnull=True).values()
            raid_highlights_list = list(raid_highlights)

            # Récupérer les highlights individuels
            individual_highlights = IndividualHighlight.objects.filter(report_id=report_code, difficulty=difficulty).values()
            individual_highlights_list = list(individual_highlights)

            # Extraction du nom de la zone et difficulté à partir des fight highlights (ou raid si pas disponible)
            if fight_highlights_list:
                zone_name = fight_highlights_list[0].get('zone_name', 'Unknown Zone')
                difficulty_value = fight_highlights_list[0].get('difficulty', 'Unknown Difficulty')
            elif raid_highlights_list:
                zone_name = raid_highlights_list[0].get('zone_name', 'Unknown Zone')
                difficulty_value = raid_highlights_list[0].get('difficulty', 'Unknown Difficulty')
            else:
                zone_name = 'Unknown Zone'
                difficulty_value = 'Unknown Difficulty'

            difficulty_name = get_difficulty_name(difficulty_value)

            # Détection de la langue et traduction des highlights
            language = detect_language(request)

            # Traduire les highlights par type
            translated_fight_highlights = translate(fight_highlights_list, language=language)
            translated_raid_highlights = translate(raid_highlights_list, language=language)

            return JsonResponse({
                "zone_name": zone_name,
                "difficulty": difficulty_name,
                "raid_highlights": translated_raid_highlights,  # Highlights de raid
                "fight_highlights": translated_fight_highlights,  # Highlights par fight
                "individual_highlights": individual_highlights_list  # Highlights individuels
            }, safe=False)
        else:
            return JsonResponse({'error': 'Report code not provided'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        # Capture and log any exceptions for better debugging
        logger.error(f'Unexpected error in get_highlights: {e}')
        return JsonResponse({'error': str(e)}, status=500)



def check_highlights_existence(request, report_code):
    """
    Vérifie si des highlights existent pour un report_code donné, indépendamment de la difficulté.
    """
    try:
        # Vérification si les highlights existent déjà pour le report_code
        if HighlightDetails.objects.filter(report_id=report_code).exists():
            frontend_url = f"{BASE_URL_FRONT}/report/{report_code}"
            return JsonResponse({'status': 'exists', 'url': frontend_url})
        else:
            return JsonResponse({'status': 'not_exists'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
