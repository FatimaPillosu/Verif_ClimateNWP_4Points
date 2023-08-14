from datetime import datetime, timedelta


DateTimeS = datetime(2000,1,1,0,0)
DateTimeF = datetime(2019,12,31,0,0)

TheDateTime_ref = DateTimeS
while TheDateTime_ref <= DateTimeF:
    
    print(TheDateTime_ref)

    TheDateTime_ref += timedelta(days=1)