from centres.views import get_centres_with_count
import sys
import codecs

# fh = open(sys.argv[3], "w")
fh = sys.stdout

def doublequote(fields):
	return [unicode("\"" + f.replace("\"", "\"\"")) + "\"" for f in fields]


platforms = [['Roche/454', '454'], ['GA2x', 'GA2', 'Illumina GA2'], ['Illumina HiSeq', 'HiSeq'],  ['Illumina MiSeq', 'MiSeq'], ['Ion Torrent', 'Proton'], ['SOLiD', 'SOLiD3/4'], ['PacBio']]

field_names = ['as_of_date', 'centre_name', 'country', 'locality', 'is_service_facility', 'is_genome_centre', 'location', 'number_sequencers', 'number_454', 'number_ga2', 'number_hiseq', 'number_miseq', 'number_ion_torrent', 'number_solid', 'number_pacbio']

print ",".join(doublequote(field_names))

plats = set()

for c in get_centres_with_count():
	fields = [sys.argv[2], c.name]
	fields.append(c.country.name)
	fields.append("%s, %s" % (c.locality, c.country.name))
	fields.append(str(c.service_facility))
	fields.append(str(c.dedicated_genome_centre))
	fields.append("%s,%s" % (c.lat, c.long))
	fields.append(str(c.n))

	caps = {}
	for cap in c.centrecapacity_set.all():
		if cap.number_machines:
			caps[cap.platform.short_name] = cap.number_machines
		else:
			caps[cap.platform.short_name] = 1

		plats.add(cap.platform.short_name)

	for p in platforms:
		field_to_add = "0"	
		for a in p:
			if a in caps:
				field_to_add = str(caps[a])
		fields.append(field_to_add)

        q = doublequote(fields)
	s = u",".join(q)
	fh.write(s.encode('utf-8'))
	fh.write("\n")

print >>sys.stderr, plats
