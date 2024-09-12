from django.core.management.base import BaseCommand
from discordbot.bot import run_bot

class Command(BaseCommand):
    help = 'Starts the Discord bot'

    def handle(self, *args, **kwargs):
        run_bot()