from openbb_terminal.sdk import openbb

def get_events(startDate, endDate):
    return openbb.economy.events(
      start_date= startDate,
      end_date= endDate,
      countries= ['Canada', 'United States']
      )