from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn import neighbors
from sklearn.ensemble import RandomForestClassifier
from xlrd import open_workbook
import sys

#vectorize the training set
def vectorize(begin,end):
	context = []
	j_list = []
	for j in range(begin,end):
		if j == 42 or j == 99: #these cases don't exist
			continue

		with open("files/id"+str(j)+".txt", 'r') as f:
			text = f.read()
		f.closed

		soup = BeautifulSoup(text)

		if len(soup.find_all('div', class_='msgBody')) == 0:
			for i in range(len(soup.find_all('h2'))):
				if 'ENFORCEMENT RESULT' in soup.find_all('h2')[i]: #result-convict
				# if 'HOW CONDUCT WAS DISCOVERED' in soup.find_all('h2')[i]: #investigation initiated by company

					next = True
					n = soup.find_all('h2')[i]
					
					#this retrieves all text before the next heading
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
					
					#if this case has already been accounted for, break out
					if j in j_list:
						break
					else:
						j_list.append(j)

					context.append((instance.encode('utf-8')))
		else:
			continue
	# print j_list
	vectorizer = TfidfVectorizer(min_df=1,stop_words='english') #sklearn vectorizer
	X = vectorizer.fit_transform(context)
	return X.toarray(),vectorizer,j_list

def results(j_list,begin,end):
	wb = open_workbook('trace.xlsx')
	s = wb.sheet_by_index(0)

	labels = []
	i_list = []
	for i in range(begin,end):

		if len(j_list) != 0:
			#make sure we have the vector for this case (since this is the training case)
			if i not in j_list:
				continue

		for j in range(0,491):
			if s.cell(j,0).value == 'https://www.traceinternational2.org/compendium/view.asp?id='+str(i):  
				result = s.cell(j,28).value  #result-conviction
				# result = s.cell(j,53).value #investigation initiated by company
				if i not in i_list:
					i_list.append(i)
				
				#assign label values
				if result == 'Yes':
					l = 1
				elif result == 'No':
					l = 0
				else:
					l = 2
				labels.append(l)
				break
	# print i_list
	return labels,i_list

def train(j_list,i_list,vectors,labels):
	# training the data with training vectors and labels
	new_vectors = []
	for j in range(len(j_list)):
		if j_list[j] in i_list:
			new_vectors.append(vectors[j])
	# print len(new_vectors)
	# print len(labels)


	# clf = neighbors.KNeighborsClassifier()
	# clf = svm.LinearSVC()
	clf = RandomForestClassifier()
	clf.fit(new_vectors,labels)
	return clf

def predict_by_word(begin,end):
	#used for result-conviction only

	predictions = []
	a = []
	j_list = []
	labels = []
	for j in range(begin,end):
		if j == 42:
			continue

		with open("files/id"+str(j)+".txt", 'r') as f:
			text = f.read()
		f.closed

		soup = BeautifulSoup(text)

		if len(soup.find_all('div', class_='msgBody')) == 0:
			for i in range(len(soup.find_all('h2'))):
				if 'ENFORCEMENT RESULT' in soup.find_all('h2')[i]:
					next = True
					n = soup.find_all('h2')[i]
					
					instance = ''
					inst = []
					while next == True:
						sib = n.next_sibling
						if sib.name == 'h2':
							next = False
						elif sib.name != 'br' and sib != '\n':
							instance = instance + sib.lstrip()
							n = sib
						else:
							n = sib
					
					if j in j_list:
						break
					else:
						j_list.append(j)
		else:
			continue	

		# print instance
		if 'convict' in instance or 'conviction' in instance:
			labels.append(1)
		else:
			labels.append(0)
	
	return labels, j_list

def predict(clf,vectorizer,begin,end):
	#prediction based on classifier 
	predictions = []
	a = []
	j_list = []
	labels = []
	for j in range(begin,end):
		if j == 42:
			continue

		with open("files/id"+str(j)+".txt", 'r') as f:
			text = f.read()
		f.closed

		soup = BeautifulSoup(text)

		if len(soup.find_all('div', class_='msgBody')) == 0:
			for i in range(len(soup.find_all('h2'))):
				if 'ENFORCEMENT RESULT' in soup.find_all('h2')[i]:
				# if 'HOW CONDUCT WAS DISCOVERED' in soup.find_all('h2')[i]:
					next = True
					n = soup.find_all('h2')[i]
					
					instance = ''
					inst = []
					while next == True:
						sib = n.next_sibling
						if sib.name == 'h2':
							next = False
						elif sib.name != 'br' and sib != '\n':
							instance = instance + sib.lstrip()
							n = sib
						else:
							n = sib
					
					if j in j_list:
						break
					else:
						j_list.append(j)
					# print 'predictions', j
					inst.append(instance.encode('utf-8'))
					a = vectorizer.transform(inst).toarray()
					label = clf.predict(a)
					labels.append(label[0])
		else:
			continue
	return labels,j_list

if __name__ == '__main__':
	train_end = 300
	test_end = 465
	# predicted1,j_list1 = predict_by_word(train_end,test_end) #predict by word

	vectors,vectorizer,j_list = vectorize(1,train_end)
	labels,k_list = results(j_list,1,train_end)
	# print len(vectors)
	# print len(labels)
	clf = train(j_list,k_list,vectors,labels)
	
	predicted,j_list = predict(clf,vectorizer,train_end,test_end)
	# print predicted
	
	real,i_list = results(j_list,train_end,test_end)
	# print real
	
	#not all 'real' information was provided on the 
	new_p = []
	for j in range(len(j_list)):
		if j_list[j] in i_list:
			new_p.append(predicted[j])
	# print len(new_p)
	# print len(real)

	#predict by word
	# new_p1 = []
	# for j in range(len(j_list1)):
	# 	if j_list1[j] in i_list:
	# 		new_p1.append(predicted1[j])

	#accuracy
	incorrect = 0
	for i in range(len(new_p)):
		if new_p[i] != real[i]:
			incorrect = incorrect + 1

	#predict by word
	# incorrect1 = 0
	# for i in range(len(new_p1)):
	# 	if new_p1[i] != real[i]:
	# 		incorrect1 = incorrect1 + 1


	# print "Test error, SVM:", 1 - float(incorrect)/len(new_p)
	# print "Percent correct, predict by word:", 1 - (float(incorrect1)/len(new_p1))
	print "Percent correct, Random Forest:", 1 - (float(incorrect)/len(new_p))

