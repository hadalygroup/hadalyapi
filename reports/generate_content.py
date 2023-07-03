from reports.sections.General_description import general_description #done
from reports.sections.Performance import portfolio_performance #done
#events missing

from reports.sections.Events import get_upcomming_events
def generate_report():
    return get_upcomming_events()