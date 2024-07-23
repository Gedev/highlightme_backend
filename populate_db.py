import os
import django

from highlightme import settings

# Configurez Django pour utiliser les paramètres de votre projet
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'highlightme.settings')
django.setup()

from api.models import Highlight, HighlightDetails

from django.db import connections
from django.db.utils import ConnectionHandler

# Optionnel : Assurez-vous que la connexion à PostgreSQL est utilisée
default_db = 'postgres'

objets = [
    Highlight(name='max_upgrade'),
    Highlight(name='max_healthstones'),
    Highlight(name='max_deaths'),
    Highlight(name='speedrunner'),
    Highlight(name='most_damage_dealt'),
    Highlight(name='less_trash_damage'),
    Highlight(name='max_potions'),
    Highlight(name='pull_before_tanks'),
    Highlight(name='lava_death'),
    Highlight(name='potion_death'),
    Highlight(name='first_death'),
    Highlight(name='solo_healing'),
    Highlight(name='solo_tanking'),

]
Highlight.objects.using(default_db).bulk_create(objets)


print("Données insérées avec succès.")