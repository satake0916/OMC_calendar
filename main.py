import fetchContestDate
import addGoogleCalendar

updoming_contests = fetchContestDate.fetch()
addGoogleCalendar.addContests(updoming_contests)