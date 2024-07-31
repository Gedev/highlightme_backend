from django.shortcuts import render
from api.models import HighlightLogs


def dashboard(request):
    return render(request, 'admin_app/templates/admin_app/dashboard.html')


def highlight_logs(request):
    logs = HighlightLogs.objects.all().order_by('-timestamp')
    print("=========== LOOOOGS ===========: ", logs)

    for log in logs:
        print(log.realm)
        if log.realm == 'Europe':
            log.realm_icon = 'europe.png'
        elif log.realm == 'United States':
            log.realm_icon = 'usa.png'
        elif log.realm == 'Korea':
            log.realm_icon = 'korea.png'
        elif log.realm == 'Taiwan':
            log.realm_icon = 'taiwan.png'
        elif log.realm == 'China':
            log.realm_icon = 'china.png'
        else:
            log.realm_icon = 'default.png'  # Par défaut

        # Nettoyer le nom de la guilde si nécessaire
        if isinstance(log.guild_name, str) and log.guild_name.startswith("{'name':"):
            log.guild_name = eval(log.guild_name).get('name', log.guild_name)
        if isinstance(log.report_owner, str) and log.report_owner.startswith("{'name':"):
            log.report_owner = eval(log.report_owner).get('name', log.report_owner)

    return render(request, 'admin_app/templates/admin_app/logs.html', {'logs': logs})
