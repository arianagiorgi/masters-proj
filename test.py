from xlrd import open_workbook
import os.path

wb = open_workbook('trace.xlsx')
s = wb.sheet_by_index(0)

correct = 0
total = 0

for j in range(1,466):
	# print j
	case = False
	for i in range(0,491):
		if s.cell(i,0).value == 'https://www.traceinternational2.org/compendium/view.asp?id='+str(j):
			perp_company = s.cell(i,1).value.upper()
			perp_indiv = s.cell(i,4).value.upper()
			perp_location = s.cell(i,9).value.upper()
			perp_rank = s.cell(i,5).value.upper()
			case = True
			# break
	if case == False:
		continue

	if os.path.isfile('files/id'+str(j)+'.results') == False:
		continue
	with open('files/id'+str(j)+'.results','r') as f:
		i = 0
		for line in f:
			#perp individuals
			if i == 1:
				parse_pi = line.replace('\n','').upper()

			#perp rank
			if i == 2:
				parse_pr = line.replace('\n','').upper()

			#perp company
			if i == 3:
				parse_pc = line.replace('\n','').upper()

			#perp location
			if i == 4:
				parse_pl = line.replace('\n','').upper()

			i = i+1

		##for evaluating perp individual
		# if perp_indiv == parse_pi:
		# 	# print "Perp individuals:", parse_pi
		# 	correct += 1
		# 	total += 1
		# else:
		# 	print j
		# 	print "Perp individuals: ", 'No agreement'
		# 	print perp_indiv, 'OR', parse_pi
		# 	total += 1

		##for evaluating perp rank
		if perp_rank == parse_pr:
			# print "Perp individuals:", parse_pi
			correct += 1
			total += 1
		else:
			print j
			print "Perp rank: ", 'No agreement'
			print perp_rank, 'OR', parse_pr
			total += 1

		##for evaluating perp location
		# if perp_location == parse_pl:
		# 	# print "Perp individuals:", parse_pi
		# 	correct += 1
		# 	total += 1
		# else:
		# 	print j
		# 	print "Perp location: ", 'No agreement'
		# 	print perp_location, 'OR', parse_pl
		# 	total += 1

		##for evaluating perp company		
		# if perp_company == parse_pc:
		# 	# print "Perp company:", parse_pc
		# 	correct += 1
		# 	total += 1

		# else:
		# 	a = False
		# 	for k in str(perp_company).split():
		# 		# print str(perp_company).split()
		# 		# print parse_pc.split()
		# 		if k in parse_pc.split():
		# 			# print True
		# 			correct += 1
		# 			total += 1
		# 			a = True
		# 			break

		# 	if a == False:
		# 		total += 1
		# 		print 'Case: ',j
		# 		print "Perp company: ", 'No agreement'
		# 		print perp_company, 'OR', parse_pc

print '----------'
print '# correct: ', correct
print 'total: ', total
print 'Percent correct: ', float(correct)/total

