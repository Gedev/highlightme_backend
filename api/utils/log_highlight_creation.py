from api.models import HighlightLogs


def log_creation(discord_pseudo, report_owner, realm, highlight_type, guild_name, creation_status):
    HighlightLogs.objects.create(
        discord_user=discord_pseudo,
        report_owner=report_owner,
        realm=realm,
        highlight_type=highlight_type,
        guild_name=guild_name,
        creation_status=creation_status,
    )
