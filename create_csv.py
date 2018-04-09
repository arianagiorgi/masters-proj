import csv
from bs4 import BeautifulSoup
import unicodedata
from xlrd import open_workbook

#function used to replace accented characters in the case file
def replace_accented(input_str):
	#from baseline.py
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

#main action
def create_turk_csv():
	with open('turk-convict.csv','wb') as csvfile:
		filewriter = csv.writer(csvfile, delimiter=',')

		# filewriter.writerow(['CASE','COMPANY','HOW CONDUCT WAS DISCOVERED'])
		filewriter.writerow(['CASE','ENFORCEMENT RESULT']) #conviction

		for j in range(1,466):
			with open("files/id"+str(j)+".txt", 'r') as f:
				text = f.read()
			f.closed

			if j == 391:
				continue
				#391 is just an overview case.. there are other individual cases

			soup = BeautifulSoup(text)

			#see if the case exists
			if len(soup.find_all('div', class_='msgBody')) == 0:

				#company name
				# perp_company = replace_accented(soup.h1.string)

				#how conduct was discovered
				for i in range(len(soup.find_all('h2'))):
					# if 'HOW CONDUCT WAS DISCOVERED' in soup.find_all('h2')[i]:
					if 'ENFORCEMENT RESULT' in soup.find_all('h2')[i]: #conviction
						next = True
						n = soup.find_all('h2')[i]
						
						instance = ''
						while next == True:
							sib = n.next_sibling
							if sib.name == 'h2':
								next = False
							elif sib.name != 'br' and sib != '\n':
								instance = instance + sib.lstrip()
								n = sib
							else:
								n = sib
				if len(instance) == 0:
					continue

				# #If the category is unspecified, then check the summary of allegations
				# if 'Unspecified' in instance.split() or 'Unspecified.' in instance.split() or 'Unknown' in instance.split() or 'Not known.' == instance.strip() or 'Not yet known.' == instance.strip() or 'Please see above.' == instance.strip():
				# 	for i in range(len(soup.find_all('h2'))):
				# 		if 'SUMMARY OF ALLEGATIONS' in soup.find_all('h2')[i]:

				# 			next = True
				# 			n = soup.find_all('h2')[i]
							
				# 			instance = ''
				# 			while next == True:
				# 				sib = n.next_sibling
				# 				if sib.name == 'h2':
				# 					next = False
				# 				elif sib.name != 'br' and sib != '\n':
				# 					instance = instance + sib.lstrip()
				# 					n = sib
				# 				else:
				# 					n = sib
				instance = replace_accented(instance).encode('utf-8').strip()
				# print instance
				# print j
				# filewriter.writerow([j,perp_company,instance])
				filewriter.writerow([j,instance]) #conviction
			else: 
				continue

def student_csv():
	with open('conviction1.csv','wb') as csvfile:

		filewriter = csv.writer(csvfile, delimiter=',')
		filewriter.writerow(['CASE','RESULT-CONVICTION'])


		wb = open_workbook('trace.xlsx')
		s = wb.sheet_by_index(0)

		for i in range(0,465):
			for j in range(0,491):
				if s.cell(j,0).value == 'https://www.traceinternational2.org/compendium/view.asp?id='+str(i):  
					# result = s.cell(j,53).value
					result = s.cell(j,28).value

					if len(result) == 0:
						continue

					filewriter.writerow([i,result])
					break

				else:
					continue

def compare():
	with open('turk_results_initiated2.csv') as csvfile:
		filereader = csv.DictReader(csvfile.read().splitlines(), delimiter=',')
		results = []
		for row in filereader:
			# results.append((row['CASE'],row['Answer'])) #for turk results with one worker
			ans = []
			if row['Agreement'] == 'Yes' and row['Answer3'] == row['Answer']:
				results.append((row['CASE'],row['Answer']))
			else: #take the majority vote
				ans.append(row['Answer1'])
				ans.append(row['Answer2'])
				ans.append(row['Answer3'])

				majority = max(set(ans), key=ans.count)
				results.append((row['CASE'],majority))


	with open('investigation.csv') as csvfile:
		filereader = csv.DictReader(csvfile.read().splitlines(), delimiter=',')
		predictions = []
		for row in filereader:
			predictions.append((row['CASE'],row['INITIATION BY COMPANY']))

	correct = 0 #number correct
	total = 0 #total matched
	for r in results:
		for p in predictions:
			if r[0] == p[0]: #cases match
				if r[1] == p[1]: #answers match
					correct += 1
				total += 1

	print 'Percent correct from Mechanical Turk: ', float(correct)/total
	print 'Correct: ', correct
	print 'Total: ', total

if __name__ == '__main__':
	# create_turk_csv()
	# student_csv()
	compare()


