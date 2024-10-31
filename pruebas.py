from datetime import datetime
from datetime import date
hoy = date.today()
x = datetime.now()
ahora = x.strftime("%H")+":"+x.strftime("%M")
print(x.strftime("%H")+":"+x.strftime("%M"))
print(hoy)