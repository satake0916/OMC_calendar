import datetime
from googleapiclient.discovery import build
from google.auth import load_credentials_from_file

SCOPES = ['https://www.googleapis.com/auth/calendar']
calendar_id = '6ijaol6slbo3bqtv5d4cvigubc@group.calendar.google.com'

def formatTime(start, during):
    date, time = start.split(' ')
    y, m, d = date.split('-')
    h, ms, second = time.split(':')
    start_time =  datetime.datetime(year=int(y), month=int(m), day=int(d), hour=int(h), minute=int(ms))

    ctime = during.split(' ')[0]
    dt = datetime.timedelta(minutes=int(ctime))
    end_time = start_time + dt
    return start_time.isoformat(), end_time.isoformat()

def addContests(upcoming):
    # Load credential file for service account
    creds = load_credentials_from_file(
      'credentials_service.json', SCOPES
    )[0]
    service = build('calendar', 'v3', credentials=creds)

    # check already registerd events
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    event_list = service.events().list(
        calendarId=calendar_id,
        timeMin=now,
        maxResults=10
    ).execute()
    events = event_list.get('items', [])
    events_summary = [event['summary'] for event in events]

    for index, row in upcoming.iterrows():
        name = row['名前']
        start = row['開始時刻']
        during = row['時間']
        isRegisterd = False

        for summary in events_summary:
            if summary == name:
                isRegisterd = True

        if isRegisterd:
            continue
        
        ft = formatTime(start, during)
        body = {
            # 予定のタイトル
            'summary': name,
            # 予定の開始時刻
            'start': {
                'dateTime': ft[0],
                'timeZone': 'Japan'
            },
            # 予定の終了時刻
            'end': {
                'dateTime': ft[1],
                'timeZone': 'Japan'
            },
        }

        # 用意した予定を登録する
        event = service.events().insert(calendarId=calendar_id, body=body).execute()