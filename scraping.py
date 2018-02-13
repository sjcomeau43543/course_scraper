import requests, re, csv

# GLOBALS --------------------------------------------------------------------------------------------------------------------------------------------

# define the reg expressions for the day of week and time
# ex: MT-RF-, --W---, M--R--
weekday = re.compile('[MTWRF\-]{6}') 

# ex: 10:00-10:50, 9:00-9:50
# note: we know classes only run between 8:00 AM and 6:00 PM for undergraduate courses
timeofday = re.compile('[0-9]{1,2}:[0-9]{2}-[0-9]{1,2}:[0-9]{2}') 

# manually adding the files for now
master = {  'A17' : 'https://bannerweb.wpi.edu/pls/prod/hwwkrnbw.P_GetDepts?sel_term=201801&sel_ptrm=A&sel_level=01&sel_campus=x',
			'B17' : 'https://bannerweb.wpi.edu/pls/prod/hwwkrnbw.P_GetDepts?sel_term=201801&sel_ptrm=B&sel_level=01&sel_campus=x',
			'C18' : 'https://bannerweb.wpi.edu/pls/prod/hwwkrnbw.P_GetDepts?sel_term=201802&sel_ptrm=C&sel_level=01&sel_campus=x',
			'D18' : 'https://bannerweb.wpi.edu/pls/prod/hwwkrnbw.P_GetDepts?sel_term=201802&sel_ptrm=D&sel_level=01&sel_campus=x' }

# FUNCTIONS ------------------------------------------------------------------------------------------------------------------------------------------

# to_csv
#   inputs
#       site - the website to visit and scrape
#       dept - the department the website is for
#       term - the year and term it corresponds to   
def to_csv(site, dept, term):
	# open the file
	with open(r'course_data.csv', 'a') as csv_file:

		# notes to console
		print "scraping", site, "..."

		curr_weekday = ""

		# get the webpage
		res = requests.get(site)

		# loop through the lines of the webpage and search for our regex's
		for line in res.iter_lines():
		    
		    # get the days the class is run, this is always right before the tod
			if weekday.search(line) is not None:
				curr_weekday = re.sub('<[\/]{0,1}TD>', '', line)
		    
		    # get the time of the class
			if timeofday.search(line) is not None:
				print dept, term, curr_weekday, re.sub('<[\/]{0,1}TD>', '', line)
				csv.writer(csv_file, delimiter=',').writerow([dept, term, curr_weekday, re.sub('<[\/]{0,1}TD>', '', line)])



def scrape(term, url):
	# get the webpage data
	mas_txt = requests.get(url)

	# add the updated data
	for line in mas_txt.iter_lines():
		if "/pls/prod" in line:
			# original length in the line
			origlen = len(line)

			# crop the 'A HREF="'
			line = line[9:origlen]

			# get just the URL beginning at /pls/prod
			url = line[:line.find('"')]
			url = "https://bannerweb.wpi.edu" + url

			# get the department this site is for
			dept = line[line.find('"')+2:origlen]
			dept = dept[:dept.find("<")]

			# we don't care about co-ops
			if "*Unknown*" not in dept:
				to_csv(url, dept, term)

def main():
	# empty our current data
	open('course_data.csv', 'w+').close()
	
	# add the header lines
	with open(r'course_data.csv', 'a') as csv_file:
		csv.writer(csv_file, delimiter=',').writerow(['Department', 'Term', 'Weekdays', 'Hours'])

	# scrap the data
	for key in master.iterkeys():
		scrape(key, master.get(key))

if __name__ == '__main__':
	main()





#---------------------------------------- sandbox #

# IMPROVEMENT - adding grad / undergrad division
# to get the other years just change it in the sel_term = 2018 to the previous years
		# 801 and A, A17
		# 801 and B, B17
		# 802 and C, C18
		# 803 and D, D18













