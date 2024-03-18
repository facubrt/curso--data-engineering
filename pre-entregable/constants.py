from datetime import datetime, timedelta

DAYS_TO_SUBTRACT = 7
TODAY = datetime.now().strftime('%Y-%m-%d')
START_DATE = (datetime.now() - timedelta(days=DAYS_TO_SUBTRACT)).strftime('%Y-%m-%d')
END_DATE = datetime.now().strftime('%Y-%m-%d')