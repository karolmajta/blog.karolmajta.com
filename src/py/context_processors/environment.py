import os

def inject_environment():
    return dict(
        GOOGLE_ANALYTICS_ACCOUNT_ID=os.environ['GOOGLE_ANALYTICS_ACCOUNT_ID']
    )
