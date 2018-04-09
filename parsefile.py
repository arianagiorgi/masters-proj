from bs4 import BeautifulSoup
from calais import Calais
import re
import dateutil.parser as dparser
from datetime import datetime
import unicodedata

#api key for calais
API_KEY = "g8gnzpdz52gkwyduv75zecem"
calais = Calais(API_KEY, submitter = "Parsing TRACE Files")

def replace_accented(input_str):
	#from baseline.py
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])


for num in range(1,172):
	print num

	with open("files/id"+str(num)+".txt", 'r') as f:
		text = f.read()
	f.closed

	soup = BeautifulSoup(text)

	if len(soup.find_all('div', class_='msgBody')) == 0:
		# print "Not a case" #only files containing a div class with the name "msgBody" are non case files.
	# else: #now just the cases
		#PERP COMPANY
		perp_company = soup.h1.string

		for i in range(len(soup.find_all('h2'))):
			
			#ENFORCEMENT AGENCY
			if 'ENFORCEMENT AGENCY' in soup.find_all('h2')[i]:
				next = True
				n = soup.find_all('h2')[i]
				enforce_agency = []
				while next == True:
					sib = n.next_sibling
					if sib.name == 'h2':
						next = False
					elif sib.name != 'br' and sib != '\n':
						enforce_agency.append(sib.lstrip())
						n = sib
					else:
						n = sib


			#PERP - INDIVIDUALS
			if 'ENTITIES/INDIVIDUALS INVOLVED' in soup.find_all('h2')[i]:
				next = True
				n = soup.find_all('h2')[i]
				perp_indivs = []
				perp_rank = []
				while next == True:
					sib = n.next_sibling
					if sib.name == 'h2':
						next = False
					elif sib.name != 'br' and sib != '\n' not in sib:

						#test to see if it's a person using calais
						r = calais.analyze(sib.encode('utf-8').strip())
						if hasattr(r,'entities'):
							for j in range(len(r.entities)):
								if r.entities[j]['_type'] == 'Person': 
									perp_indivs.append(r.entities[j]['name'])
								if r.entities[j]['_type'] == 'Position':
									position = r.entities[j]['name']
							
							
									#PERP RANK
									fit = False
									if 'President' in position or 'Chairman' in position or 'CEO' in position or 'Chief Executive Officer' in position:
										if 'CEO/Chairman/President' not in perp_rank:
											perp_rank.append('CEO/Chairman/President')
											fit = True
									if 'Founder' in position:
										if 'Founder' not in perp_rank:
											perp_rank.append('Founder')
											fit = True
									if 'Vice President' or 'vice' in position:
										if 'Vice President' not in perp_rank:
											perp_rank.append('Vice President')
											fit = True
									if 'officer' in position:
										if 'Company Official' not in perp_rank:
											perp_rank.append('Company Official')
											fit = True
									if 'shareholder' in position.lower():
										if 'Board of Directors' not in perp_rank:
											perp_rank.append('Board of Directors')
											fit = True
									if 'division' in position.lower():
										if 'Director of a Division' not in perp_rank:
											perp_rank.append('Director of a Division')
											fit = True
									if fit == False:
										perp_rank.append('Other')
						else:
							perp_indivs.append('?')
							perp_rank.append('?')

						
						n = sib
					else:
						n = sib

				if len(perp_indivs) == 1:
					perp_indiv = perp_indivs[0]
					perp_indivs = []
				else:
					perp_indiv = ''


			#PERP LOCATION
			if 'CORPORATE HEADQUARTERS' in soup.find_all('h2')[i]:
				location = soup.find_all('h2')[i].next_sibling.lstrip().rstrip()
				#lstrip/rstrip removes unnecessary spaces before/after word
				location = replace_accented(location)
				r = calais.analyze(location)
				if hasattr(r,'entities'):
					for j in range(len(r.entities)):
						if r.entities[j]['_type'] == 'Country': 
							perp_location = r.entities[j]['name']
				else:
					perp_location = '?'

			#BRIBE LOCATION
			if 'NATIONALITY OF FOREIGN OFFICIALS' in soup.find_all('h2')[i]:
				next = True
				n = soup.find_all('h2')[i]
				bribe_locations = []
				while next == True:
					sib = n.next_sibling
					if sib.name == 'h2':
						next = False
					elif sib.name != 'br' and sib != '\n':
						bribe_locations.append(sib.lstrip())
						n = sib
					else:
						n = sib

			#CASE START YEAR
			if 'HOW CONDUCT WAS DISCOVERED' in soup.find_all('h2')[i]:
				s = soup.find_all('h2')[i].next_sibling.lstrip().rstrip() + '1000' #adding 1000 so a 'year' will be found no matter what
				match = re.search(r'\d{4}', s)
				start_year = datetime.strptime(match.group(),'%Y').year
				if start_year == 1000:
					start_year = None
				

		with open('files/id'+str(num)+'.results','w') as f:
			# print soup.prettify()
			p_i = ''
			for p in range(len(perp_indivs)):
				if p != len(perp_indivs) - 1:
					p_i = p_i + perp_indivs[p] + ', '
				else:
					p_i = p_i + perp_indivs[p]

			p_r = ''
			for p in range(len(perp_rank)):
				if p != len(perp_rank) - 1:
					p_r = p_r + perp_rank[p] + ', '
				else:
					p_r = p_r + perp_rank[p]

			answers = [enforce_agency,p_i,p_r,perp_company,perp_location,bribe_locations,start_year]
		
			for a in answers:
				if type(a) is list:
					for b in a:
						b = replace_accented(unicode(b))
				else:
					a = replace_accented(unicode(a)).encode('utf-8').strip()
				s = str(a) + '\n'
				f.write(s)



