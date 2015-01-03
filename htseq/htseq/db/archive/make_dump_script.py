
import glob

files = glob.glob("*T00:00.sqlite")

dates = ["".join(f.split("T")[0].split("-"))  for f in files]
dates = [int(d) for d in dates]

dates.sort()

last = 0

dump_dates = []

for d in dates:
	month = int(str(d)[3:6])

	if month - last > 2:
		print month
		last = int(month)
		dump_dates.append(d)

for d in dump_dates:
	d = str(d)
	print "python dump.py %s-%s-%sT00:00.sqlite \"%s-%s-%s\" | tail -n +2 >>full_dump.txt" % (d[0:4], d[4:6], d[6:8], d[0:4], d[4:6], d[6:8])

