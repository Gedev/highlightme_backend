from django.db import models


# Create your models here.


class Highlight(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Difficulties(models.IntegerChoices):
    LFR = 1, "LFR"
    FLEX = 2, "Flex"
    NORMAL = 3, "Normal"
    HEROIC = 4, "Heroic"
    MYTHIC = 5, "Mythic"


class HighlightDetails(models.Model):
    report_id = models.CharField(max_length=255)
    type = models.ForeignKey(Highlight, on_delete=models.CASCADE)
    fight_id = models.IntegerField(null=True)
    boss_name = models.IntegerField(null=False, default=0)
    player_name = models.CharField(max_length=255)
    player_class = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    img = models.CharField(max_length=255, blank=True)
    difficulty = models.IntegerField(choices=Difficulties.choices, null=True, blank=True)
    zone_name = models.CharField(max_length=255, null=True, blank=True)
    highlight_value = models.FloatField()

    def __str__(self):
        return f"{self.title} ({self.get_difficulty_display()})"


class CREATION_STATUS(models.TextChoices):
    CREATED = "CREATED", "Created"
    FAILED = "FAILED", "Failed"
    REFUSED = "REFUSED", "Refused"


class HighlightLogs(models.Model):
    discord_user = models.CharField(max_length=255, null=True)
    report_owner = models.CharField(max_length=255)
    realm = models.CharField(max_length=255)
    highlight_type = models.CharField(max_length=255)
    guild_name = models.CharField(max_length=255, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    creation_status = models.CharField(max_length=20, choices=CREATION_STATUS.choices)

    def __str__(self):
        return f"{self.report_owner} - {self.highlight_type} - {self.timestamp}"


class IndividualHighlight(models.Model):
    report_id = models.CharField(max_length=255)
    player_name = models.CharField(max_length=255)
    player_class = models.CharField(max_length=255)
    difficulty = models.IntegerField(choices=Difficulties.choices, null=True, blank=True)

    # Highlights for legendary parses
    total_legendary_parses = models.IntegerField(default=0)
    best_legendary_parse = models.FloatField(null=True, blank=True)

    # Average parses
    best_rank_avg_dps_parses = models.FloatField(null=True, blank=True)
    best_ilvl_avg_dps_parses = models.FloatField(null=True, blank=True)
    best_rank_avg_hps_parses = models.FloatField(null=True, blank=True)
    best_ilvl_avg_hps_parses = models.FloatField(null=True, blank=True)

    # Optional fields for detailed parse highlights
    fight_id = models.IntegerField(null=True, blank=True)
    encounter_name = models.CharField(max_length=255, null=True, blank=True)

    # These fields are for capturing individual parse details, if needed
    dps_rank_percent = models.FloatField(null=True, blank=True)
    dps_bracket_percent = models.FloatField(null=True, blank=True)
    hps_rank_percent = models.FloatField(null=True, blank=True)
    hps_bracket_percent = models.FloatField(null=True, blank=True)
    dtps = models.FloatField(null=True, blank=True)  # Damage taken per second, can be used for tanks

    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player_name} - {self.report_id} - Best DPS Rank Avg: {self.best_rank_avg_dps_parses}%, Best HPS Rank Avg: {self.best_rank_avg_hps_parses}%"


class Boss(models.Model):
    id = models.IntegerField(primary_key=True)
    zone_name = models.CharField(max_length=255, null=True, blank=True)
    expansion_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.expansion_name}"


class BossTranslation(models.Model):
    boss = models.ForeignKey(Boss, related_name='translations', on_delete=models.CASCADE)
    language_code = models.CharField(max_length=10)
    translated_name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('boss', 'language_code')  # Empêche les doublons pour la même langue et boss

    def __str__(self):
        return f"{self.translated_name} ({self.language_code})"