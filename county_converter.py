from csvkit import unicsv

COUNTIES = ['Adams','Allen','Ashland','Ashtabula','Athens','Auglaize','Belmont','Brown','Butler','Carroll','Champaign','Clark','Clermont','Clinton','Columbiana','Coshocton','Crawford','Cuyahoga','Darke','Defiance','Delaware','Erie','Fairfield','Fayette','Franklin','Fulton','Gallia','Geauga','Greene','Guernsey','Hamilton','Hancock','Hardin','Harrison','Henry','Highland','Hocking','Holmes','Huron','Jackson','Jefferson','Knox','Lake','Lawrence','Licking','Logan','Lorain','Lucas','Madison','Mahoning','Marion','Medina','Meigs','Mercer','Miami','Monroe','Montgomery','Morgan','Morrow','Muskingum','Noble','Ottawa','Paulding','Perry','Pickaway','Pike','Portage','Preble','Putnam','Richland','Ross','Sandusky','Scioto','Seneca','Shelby','Stark','Summit','Trumbull','Tuscarawas','Union','Van Wert','Vinton','Warren','Washington','Wayne','Williams','Wood','Wyandot']

with open('/Users/derekwillis/Downloads/republican.csv', 'rb') as csvfile:
    reader = unicsv.UnicodeCSVReader(csvfile)
    offices = next(reader)
    fixed_offices = []
    for office in offices[5:]:
        if office != '':
            o = office.strip()
            fixed_offices.append(office.strip())
        else:
            fixed_offices.append(o)
    headers = next(reader)
    fixed_cols = headers[0:5]
    fixed_cols.extend(['office', 'district', 'party', 'candidate', 'votes'])
    cands = headers[5:]
    l = list(reader)
    for county in COUNTIES:
        results = []
        filename = "20160315__oh__primary__republican__%s.csv" % county.lower()
        rows = [x for x in l if x[0] == county]
        for row in rows:
            county = row[0].strip()
            for idx, cand in enumerate(cands):
                if row[0] == 'Percentage' or row[0] == 'Total':
                    continue
                office = fixed_offices[idx]
                if ' - District' in office:
                    office, district = office.split(' - District')
                else:
                    district = None
                votes = row[idx+5]
                results.append([county, row[1], row[2], row[3], row[4], office, district, 'R', cand.replace(' (R)', '').replace('  ', ' '), votes])

        with open(filename, 'wb') as outfile:
            writer = unicsv.UnicodeCSVWriter(outfile)
            writer.writerow(fixed_cols)
            writer.writerows(results)