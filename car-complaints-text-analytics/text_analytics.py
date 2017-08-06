import csv
import re
from stemming.porter2 import stem
from check_list import *
from data_learner import *

# csv_path = "sample.csv"
# colom = 'Complaint Text'
output = [['Complaint area']]
unwanted_words_list = conjuctions + prepositions + pronouns + omit_verbs + ordinals +  months + omit_words
known_words_list = unwanted_words_list + negative_words + service_related_words + damage_related_words + car_parts

def get_unique(list1, list2):
    unique = []
    for item in list1:
        if item not in list2:
            unique.append(item)
    return unique

def preprocess(data):
    # Remove special characters
    data = re.sub('\W+',' ', data)
    # Remove digits
    data = ''.join(filter(lambda x: not x.isdigit(), data))
    # Remove unwanted words - conjuctions, ordinals etc.
    return get_unique(data.split(), unwanted_words_list)

def data_analyser(data):
    output.append([])
    if len(data) < 3:
        output[-1].append('Incomplete complaint')
        return
    complaints = {
        'dealer': 'Feedback against Dealer / showroom',
        'dealer_neg': 'Complaint against Dealer / showroom',
        'service': 'Complaint against service by Dealer / showroom',
        'damage': 'Car part damage / repair realted complaint',
        'generic': 'Customer Dissatisfaction',
        'unable': 'Unable to analyze the complaint from the given data'
    }
    service_complaint_added = False
    for each_word in data:
        word = stem(each_word)
        pos = data.index(each_word)
        if word in service_related_words and not service_complaint_added:
            service_complaint_added = True
            # Find if the comment is negative about the dealer
            key = 'dealer_neg' if (set(data[pos-1:pos+3]).intersection(negative_words)) else 'dealer'
            output[-1].append(complaints.get(key))
        # Add showroom / dealer name
            if 'motors' in data:
                output[-1][-1] + (': ' + data[data.index('motors') -1])
        if word in damage_related_words:
            output[-1].append(complaints.get('damage'))
    damage = set(data).intersection(car_parts)
    if len(damage) > 0:
        output[-1].append(complaints.get('damage') + ': ' + ','.join(damage))
        if complaints.get('damage') in output[-1]:
            output[-1].remove(complaints.get('damage'))

    if len(output[-1]) == 0 and len(set(data).intersection(negative_words)) > 0:
        output[-1].append(complaints.get('generic'))
    if len(output[-1]) == 0:
        output[-1].append(complaints.get('unable'))

def complaints_reader(file_obj, colom):
    data = []
    reader = csv.reader(file_obj)
    selected_colom = next(reader).index(colom)
    for row in reader:
        # Reduce the data as much as possible
        content = preprocess(row[selected_colom].lower())
        # Analyse each data
        data_analyser(content)

        # Learn from each data
        data_learner(content)
    data.append(content)
    return data

if __name__ == "__main__":
    
    csv_path = raw_input("Please enter the path of csv file")
    colom = raw_input("Please enter the heading of colom to be analyzed")
    with open(csv_path, "rb") as f_obj:
        complaints = complaints_reader(f_obj, colom)

    with open(csv_path, 'r+') as f_obj:
        reader = csv.reader(f_obj, delimiter=',')
        out_lines = [row + [','.join(output[i])] for i, row in enumerate(reader)]
        f_obj.seek(0)
        csv.writer(f_obj, delimiter=',').writerows(out_lines)
    new_list = get_new_words_list()

    # Write list of all new words with count to a file
    with open('new_words.csv', 'wb') as f_obj:
        writer = csv.writer(f_obj, delimiter=',')
        for data in new_list:
            writer.writerow(data)