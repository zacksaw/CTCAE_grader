import numpy as np
import pandas as pd
import csv
import xlrd

#converting my excel document to csv
def csv_from_excel(file,sheet,new_name):
    wb = xlrd.open_workbook(file)
    sh = wb.sheet_by_name(sheet)
    your_csv_file = open(new_name, 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

# runs the csv_from_excel function:
csv_from_excel('CTCAEAE.xlsx', 'Sheet1', 'AECSV.csv')

#Convert the csv file into a dictionary to pull the definitions
with open('AECSV.csv') as f:
    next(f)  # Skip the header
    reader = csv.reader(f, skipinitialspace=True)
    def_dict = dict(reader)

csv_from_excel('CTCAEAE.xlsx', 'Sheet2', 'Rangevalues.csv')

with open('Rangevalues.csv') as f:
    next(f)  # Skip the header
    reader1 = csv.reader(f, skipinitialspace=True)
    range_dict = dict(reader1)

print("Hello, Welcome to Zacharia's Adverse Event calculator!")
print('')

#begin to define functions
#there are three types - two that use ranges from lab values (decreasing or increasing) and one that uses subjective terms

#this function will be used for values that increase in grade with an increase in lab values
#I defined the functions based on the AE term (x), and the refrence ranges
def grader_increasing(x, min_, min1, min2, min3):
    #the function operates based on the input of whether the user wants the definition
    if definition in ('yes', 'y'):
        #Based on the argument of AE term (x), this will use the dictionary from the CSV to print the definition
        print(def_dict[x])
        #using the AE term argument to build the question below
        print('What is the lab value for',x,'?')
        value = float(input(''))
        #the mins and max from the function arguments are used to build these responses
        if min_ > value :
            print("This is not an adverse event")
        if min_ <= value <= min1:
            print("Your AE is grade 1")
        if min1 < value <= min2:
            print("Your AE is grade 2")
        if min2 < value <= min3:
            print("Your AE is grade 3")
        if min3 < value:
            print("Your AE is grade 4")
    #ducplicated if the user doesn't want to read the definition
    elif definition in ('no', 'n'):
        print('What is the lab value for',x,'?')
        value = float(input(''))
        if min_ > value :
            print("This is not an adverse event")
        if min_ <= value <= min1:
            print("Your AE is grade 1")
        if min1 < value <= min2:
            print("Your AE is grade 2")
        if min2 < value <= min3:
            print("Your AE is grade 3")
        if min3 < value:
            print("Your AE is grade 4")

#this function will be used for values that increase in grade with a decrease in lab values
def grader_decreasing(x, min_, min1, min2, min3):
    if definition in ('yes', 'y'):
        print(def_dict[val])
        print('What is the lab value for',x,'?')
        value = float(input(''))
        if min_ < value :
            print("This is not an adverse event")
        if min1 <= value <= min_ :
            print("Your AE is grade 1")
        if min2 <= value < min1:
            print("Your AE is grade 2")
        if min3 <= value < min2:
            print("Your AE is grade 3")
        if min3 > value:
            print("Your AE is grade 4")
    elif definition in ('no', 'n'):
        print('What is the lab value for',x,'?')
        value = float(input(''))
        if min < value:
            print("This is not an adverse event")
        if min1 <= value <= min_:
            print("Your AE is grade 1")
        if min2 <= value < min1:
            print("Your AE is grade 2")
        if min3 <= value < min2:
            print("Your AE is grade 3")
        if min3 > value:
            print("Your AE is grade 4")

#this function will be used for values that increase in grade depending on subjective terms like 'mild' or 'severe'
def grader_characters(x):
    if definition in ('yes', 'y'):
        print(def_dict[x])
        print('How severe is',x,'?')
        value = input('')
        if value in ('mild', 'asympotomatic', 'Mild', 'Asymptomatic'):
            print("Your AE is grade 1")
        if value in ('moderate', 'sympotomatic'):
            print("Your AE is grade 2")
        if value in ('severe', 'ADL'):
            print("Your AE is grade 3")
        if value in ('hospitalization', 'life-threatening', 'urgent'):
            print("Your AE is grade 4")
    elif definition in ('no', 'n'):
        print('How severe is',x,'?')
        value = input('')
        if value in ('mild', 'asympotomatic', 'Mild', 'Asymptomatic'):
            print("Your AE is grade 1")
        if value in ('moderate', 'asympotomatic'):
            print("Your AE is grade 2")
        if value in ('severe', 'ADL'):
            print("Your AE is grade 3")
        if value in ('hospitalization', 'life-threatening', 'urgent'):
            print("Your AE is grade 4")

#function to turn the search values into keys for the range dictionary
def valuemaker(value, x):
    return value.strip() + x.strip()


# print(range_dict['Anemia_min_'])
# ran3 = [value for value, key in range_dict.items() if 'Anemia_min_' in (key)]
# print(ran3)

while True:
    inp = input('Would you like to search or input your AE term? ')
    if inp in ('search', 'Search'):
        search = input('Search with a key word:')
        term = ', '.join([key for key, value in def_dict.items() if search in (' ' + value + ' ')])
        if term in '':
            print('Sorry, nothing was found with that key word ')
            print("Let's try again")
            continue
        print ('Is this the AE you are looking for:',term)
        confirm = input('')
        if confirm in ('y','yes'):
            val = term
            print("Whould you like the definition for the",val,'?')
            definition = input('')
            if val in ('Anemia','White blood cell decreased','Platelet count decreased','Hyponatremia'):
                ran_ = float(range_dict[valuemaker(val, '_min_')])
                ran1 = float(range_dict[valuemaker(val, '_min1')])
                ran2 = float(range_dict[valuemaker(val, '_min2')])
                ran3 = float(range_dict[valuemaker(val, '_min3')])
                print(ran_,ran1,ran2,ran3)
                grader_decreasing(val, ran_, ran1, ran2, ran3)
            if val in ('Conjunctivitis', 'Myelitis', 'Kidney anastomotic leak', 'Flu like symptoms', 'Non-cardiac chest pain', 'Pain', 'Myalgia', 'Myositis'):
                print ("Would you like the definition for", val)
                definition = input('')
                grader_characters(val)
            else:
                ran_ = float(range_dict[valuemaker(val, '_min_')])
                ran1 = float(range_dict[valuemaker(val, '_min1')])
                ran2 = float(range_dict[valuemaker(val, '_min2')])
                ran3 = float(range_dict[valuemaker(val, '_min3')])
                print(ran_,ran1,ran2,ran3)
                grader_increasing(val, ran_, ran1, ran2, ran3)
        elif confirm in ('n', 'no'):
            print("Sorry, let's try again")
            continue

                # if val in 'Anemia':
            #     definition = input("Would you like the definition for the Anemia AE? ")
            #     grader_decreasing(val, 13.9, 10.0, 8.0, 5.0)
            #
            # if val in 'Fever':
            #     definition = input("Would you like the definition for the Fever AE? ")
            #     grader_increasing(val, 38.0, 39.0, 40.0, 43.0)
            #
            # if val in 'White blood cell decreased':
            #     definition = input("Would you like the definition for the Fever AE? ")
            #     grader_decreasing(val, 3.6, 3, 2, 1)
            #
            # if val in 'Hyperkalemia':
            #     definition = input("Would you like the definition for the Fever AE? ")
            #     grader_increasing(val, 5.1, 5.5, 6,7)
            #
            # if val in 'Alanine aminotransferase increased':
            #     definition = input("Would you like the definition for the Fever AE? ")
            #     grader_increasing(val, 351, 153, 255, 1020)
            #
            # if val in 'Aspartate aminotransferase increased':
            #     definition = input("Would you like the definition for the Aspartate aminotransferase increased AE? ")
            #     grader_increasing(val, 59, 177, 295, 1180)
            #
            # if val in 'Hyponatremia':
            #     definition = input("Would you like the definition for the Hyponatremia AE? ")
            #     grader_decreasing(val, 137, 125, 129, 120)
            #
            # if val in ('Hypernatremia', 'high sodium', 'increased sodium', 'elevated sodium'):
            #     definition = input("Would you like the definition for the Hypernatremia AE? ")
            #     grader_increasing('Hypernatremia', 141, 150, 155, 160)
            #
            # if val in 'Platelet count decreased' or search in ('high temperature', 'fever'):
            #     definition = input("Would you like the definition for the Platelet count decreased AE? ")
            #     grader_decreasing('Platelet count decreased',150, 75, 50, 25)
            #
            # if val in ('Electrocardiogram QT corrected interval prolonged') or search in ('QTC', 'elevated QTC', 'qtc'):
            #     definition = input("Would you like the definition for the Electrocardiogram QT corrected interval prolonged AE? ")
            #     grader_increasing('Electrocardiogram QT corrected interval prolonged', 450, 481, 500, 600)

    # if inp in ('input' or 'input AE term'):
    #     val = input('What is the AE? ')
    #     if val in ('Blood bilirubin increased','bilirubin increased', 'high bilirubin','bilirubin','Bilirubin'):
    #         definition = input("Whould you like the definition for the Blood bilirubin increased AE? ")
    #         grader_increasing('Blood bilirubin increased',1.30,1.95,3.90,13.00)
    #
    #     if val in ('Anemia', 'hemoglobin','anemia'):
    #         definition = input("Would you like the definition for the Anemia AE? ")
    #         grader_decreasing('Anemia',13.9,10.0,8.0,5.0)
    #
    #     if val in ('Fever', 'high temperature', 'fever'):
    #         definition = input("Would you like the definition for the Fever AE? ")
    #         grader_increasing('Fever',38.0,39.0,40.0,43.0)
    #
    #     if val in ('White blood cell decreased', 'low WBC', 'low wbc', 'low white blood cell count', 'low wbc count'):
    #         definition = input("Would you like the definition for the Fever AE? ")
    #         grader_increasing('Fever',38.0,39.0,40.0,43.0)
    #
    #     if val in ('Hyperkalemia', 'high potassium'):
    #         definition = input("Would you like the definition for the Fever AE? ")
    #         grader_increasing('Fever',38.0,39.0,40.0,43.0)
    #
    #     if val in ('Alanine aminotransferase increased', 'elevated ALT', 'high ALT', 'increased ALT'):
    #         definition = input("Would you like the definition for the Fever AE? ")
    #         grader_increasing('Alanine aminotransferase increased',38.0,39.0,40.0,43.0)
    #
    #     if val in ('Aspartate aminotransferase increased', 'elevated AST', 'high AST', 'increased AST'):
    #         definition = input("Would you like the definition for the Aspartate aminotransferase increased AE? ")
    #         grader_increasing('Aspartate aminotransferase increased',38.0,39.0,40.0,43.0)
    #
    #     if val in ('Hyponatremia', 'low sodium', 'decreased sodium'):
    #         definition = input("Would you like the definition for the Hyponatremia AE? ")
    #         grader_increasing('Hyponatremia',38.0,39.0,40.0,43.0)
    #
    #     if val in ('Hypernatremia', 'high sodium', 'increased sodium', 'elevated sodium'):
    #         definition = input("Would you like the definition for the Hypernatremia AE? ")
    #         grader_increasing('Hypernatremia',38.0,39.0,40.0,43.0)
    #
    #     if val in ('Platelet count decreased', 'high temperature', 'fever'):
    #         definition = input("Would you like the definition for the Platelet count decreased AE? ")
    #         grader_increasing('Platelet count decreased',38.0,39.0,40.0,43.0)
    #
    #     if val in ('Electrocardiogram QT corrected interval prolonged', 'QTC', 'elevated QTC', 'qtc'):
    #         definition = input("Would you like the definition for the Electrocardiogram QT corrected interval prolonged AE? ")
    #         grader_increasing('Electrocardiogram QT corrected interval prolonged',38.0,39.0,40.0,43.0)
    #
    #     if val in ('Conjunctivitis', 'inflamed conjunctiva'):
    #         definition = input("Would you like the definition for the Conjunctivitis AE? ")
    #         grader_increasing('Conjunctivitis',38.0,39.0,40.0,43.0)
    #
    #     if val in ('Myelitis', 'swollen spine', 'inflamed spine', 'spinal cord inflamation'):
    #         definition = input("Would you like the definition for the Myelitis AE? ")
    #         grader_increasing('Myelitis',38.0,39.0,40.0,43.0)
    #
    #     if val in ('Kidney anastomotic leak', 'kidney leak', 'urine leaking'):
    #         definition = input("Would you like the definition for the Kidney anastomotic leak AE? ")
    #         grader_increasing('Kidney anastomotic leak',38.0,39.0,40.0,43.0)
    #
    #     if val in ('Flu like symptoms', 'flu', 'influenza'):
    #         definition = input("Would you like the definition for the Flu like symptoms AE? ")
    #         grader_increasing('Flu like symptoms',38.0,39.0,40.0,43.0)
    #
    #     if val in ('Non-cardiac chest pain', 'chest pain', 'pain in chest'):
    #         definition = input("Would you like the definition for the Non-cardiac chest pain AE? ")
    #         grader_increasing('Non-cardiac chest pain',38.0,39.0,40.0,43.0)
    #
    #     if val in ('Pain', 'pain', 'general pain', 'in pain'):
    #         definition = input("Would you like the definition for the Pain AE? ")
    #         grader_increasing('Pain',38.0,39.0,40.0,43.0)
    #
    #     if val in ('Myalgia', 'muscles soreness', 'sore muscles', 'in pain'):
    #         definition = input("Would you like the definition for the Myalgia AE? ")
    #         grader_increasing('Myalgia',38.0,39.0,40.0,43.0)
    #
    #     if val in ('Myositis', 'inflamed eyes'):
    #         definition = input("Would you like the definition for the Myositis AE? ")
    #         grader_increasing('Myositis',38.0,39.0,40.0,43.0)
    print ('Thank you for using the calculator!')
    print ('Go again:')
    continue
