import glob
import subprocess
from datetime import date

year_start = date(2010, 1, 1)

for fn in glob.glob('*.sqlite'):
    dat, tm = fn.split("T")
    if tm.startswith('00:00'):
        y, m, d = [int(x) for x in dat.split("-")]
        d = date(y,m,d)
        p = subprocess.Popen(["sqlite3", "-noheader", fn], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = p.communicate("select sum(number_machines), platform.id, platform.short_name from centre_capacity join platform on centre_capacity.platform_id = platform.id group by platform_id;")

        for ln in out.split("\n"):
            if ln:
                print "%s|%s" % (d.isocalendar()[1], ln)
