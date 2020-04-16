
# export FCM_KEY='AIzaSyB3v7F_iLoLINN99nrHY1IHtt1E9Ar260A'
# export SECRET_KEY='d+!d=(n(m&$&7+db(&ad-_lfeyw2%3=_sr1$_zo^9y0o3!$utv'
# export twilio_acc_sid='ACc1f8db0bd85b30ca84af0f974d12ff30'
# export twilio_auth_token='78e68a058f1628662e4a3f0786fff7a1'
# export DEBUG=True


from operations.models import *

User.objects.create_superuser(username='admin',email='some_email@email.com',password='Pass@123').save()

# Delhi
# Region ID: 1

HealthCare(name='Airport Health Organization', address='Airport Health Organization, New Building, Mahipalpur, Near Radisson Blu Hotel, On Approach Road to T-3 New Delhi-110037', email='', region=1, lat=28.545136, lng=77.115808).save()
HealthCare(name='Armed Force Clinic, New Delhi', address='Dalhousie Road, New Delhi-110011', email='del1.phc.com', region=1, lat=28.6107483, lng=77.1999387).save()

HealthCare(name='Public Health Lab Building, Delhi', address='Near Gate 3, Vidhan Sabha Metro Station, Opp. Civil Lines Police Station, Alipur Road, Delhi', email='del2.phc.com', region=1, 
lat=28.6884462, lng=77.2187899).save()

# Kolkata
# Region ID: 2
HealthCare(name='Port Health Organization', address='Port Health Organization Marine House, Kolkata700022', email='kol1.phc.com', region=2, lat=22.551364, lng=88.326790).save()
HealthCare(name='All India Institute of Hygiene and Public Health (AIIH&PH), Kolkata', address='Department of Microbiology All India Institute Of Hygiene & Public Health Bidhannagar Campus 27 & 27B J.C. Block, Sector III Salt Lake700098 (Near Tank No.14), Kolkata', email='kol2.phc.com', region=2, lat=22.5695109, lng=88.4128554).save()

# Maharashtra
# Region ID: 3
HealthCare(name='AIRPORT HEALTH ORGANISATION', address='Airport Health Organization C.S.I. Airport, Next to Ambassador Sky Chef, Sahar, Andheri (E), Mumbai-400099', email='mum1.phc.com', region=3, lat=19.1034235, lng=72.8746483).save()

HealthCare(name='Family Welfare Regional Training Centre, Mumbai', address='332, S.V.P. Road, Khetwadi, Mumbai, Maharashtra 400004', email='mum2.phc.com', region=3, lat=18.9583009, lng=72.820298).save()

HealthCare(name='B.J. Govt. Medical College (BJMC), Pune', address='Jai Prakash Narayan Road, Near Pune Railway Station, Pune, Maharashtra 411001', email='pun1.phc.com', region=3, lat=18.5269605, lng=73.8710668).save()
