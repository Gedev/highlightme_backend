# services/report_eligibility_service.py

class ReportEligibilityService:
    """
    Service responsible for validating the eligibility of a report for highlight creation.
    """
    def is_report_eligible(events_data, global_info_data):
        """
        Checks if the report is eligible for highlight creation.
        This includes detecting boost groups and other potential disqualifications.
        """

        if is_boost_group_detected(events_data, global_info_data):
            return False

        # Add other eligibility checks here as needed

        return True


def is_boost_group_detected(events_data, global_info_data):
    fights = global_info_data['data']['reportData']['report']['fightsEncounters']
    death_events = events_data['data']['reportData']['report']['table']['data']['deathEvents']

    death_counts = {}

    for fight in fights:
        fight_id = fight['id']
        fight_deaths = [event for event in death_events if event['fight'] == fight_id]

        for death in fight_deaths:
            player_name = death['name']
            death_time = death['timestamp'] - fight['startTime']

            if death_time < 10000:  # 10 seconds threshold
                if player_name not in death_counts:
                    death_counts[player_name] = 0
                death_counts[player_name] += 1

    if len(death_counts) > len(fights) * 0.5:  # Arbitrary threshold: more than 50% of the raid dies early
        return True

    return False

