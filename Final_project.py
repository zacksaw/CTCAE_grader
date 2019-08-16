import numpy as np
import pandas as pd
import csv
import xlrd

#a function that converts excel to csv based on sheet in the spreadsheet
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

# runs csv converter again to make a range dictionary
csv_from_excel('CTCAEAE.xlsx', 'Sheet2', 'Rangevalues.csv')

#Convert the csv file into a dictionary to get definitions
with open('Rangevalues.csv') as f:
    next(f)  # Skip the header
    reader1 = csv.reader(f, skipinitialspace=True)
    range_dict = dict(reader1)

print("Hello, Welcome to Zacharia's Adverse Event calculator!")
print('')

#begin to define functions
#there are three types - two that use ranges from lab values (decreasing or increasing) and one that uses subjective terms

x = ''
min_ = ''
min1 = ''
min2 = ''
min3 = ''
#this function will be used for values that increase in grade with an increase in lab values
#I defined the functions based on the AE term (x), and the refrence ranges
def grader_increasing(x):
    #pull min and max values from the range dictionary
    min_ = float(range_dict[valuemaker(x, '_min_')])
    min1 = float(range_dict[valuemaker(x, '_min1')])
    min2 = float(range_dict[valuemaker(x, '_min2')])
    min3 = float(range_dict[valuemaker(x, '_min3')])
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
def grader_decreasing(x):
    min_ = float(range_dict[valuemaker(x, '_min_')])
    min1 = float(range_dict[valuemaker(x, '_min1')])
    min2 = float(range_dict[valuemaker(x, '_min2')])
    min3 = float(range_dict[valuemaker(x, '_min3')])
    if definition in ('yes', 'y'):
        print(def_dict[x])
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
        if min_ < value:
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
def valuemaker(range_key, min_val):
    return range_key.strip() + min_val.strip()




#While loop to run all input commands
while True:
    #define variables
    inp = ''
    term = ''
    confirm = ''
    val = ''
    inp = input('Would you like to search or input your AE term? (s/i) ')
    #the user can search the definition dictionary
    if inp in ('search', 'Search', 'search ', 's'):
        search = input('Search with a key word: ')
        #Using the search value above to find the word in any of the definitions in the defintion dictionary
        val = ' and '.join([key for key, value in def_dict.items() if search in (' ' + value + ' ')])
        #If there is nothing, it will loop back
        if val in '':
            print('Sorry, nothing was found with that key word ')
            print("Let's try again")
            continue
        #I am using the 'and' from the list comprehension function to identify if there are multiple AE terms
        elif (' ' + 'and' + ' ') in val:
            while True:
                print('There are multiple AEs found, please choose enter the exact one desired:', val)
                val_input = input('')
                try:
                    def_dict[val_input]
                    val = val_input #I want to test the input without changing val
                    break
                #In case the user doesnt enter the exact code it will jump back
                except KeyError:
                    print('This is not a valid AE, please try again')
                    continue
        print ('Is this the AE you are looking for:',val)
        confirm = input('')
        if confirm in ('y','yes'): #to allow the user to go back if it is not
            print("Would you like the definition for",val,'?')
            definition = input('')
            #for AEs that decrease in range
            if val in ('Anemia','White blood cell decreased','Platelet count decreased','Hyponatremia'):
                #using the grader function which will also pull the definition and make the keys for the range dictionary
                grader_decreasing(val)
                continue
            # for AEs that use descriptive words
            elif val in ('Conjunctivitis', 'Myelitis', 'Kidney anastomotic leak', 'Flu like symptoms', 'Non-cardiac chest pain', 'Pain', 'Myalgia', 'Myositis'):
                grader_characters(val)
                continue
            else:
                #for the AE that are not in decreasing ranges and do not use discriptive words
                grader_increasing(val)
                continue
        elif confirm in ('n', 'no'):
            print("Sorry, let's try again")
            continue
    #if the user decides to input the term
    if inp in ('input', 'input AE term', 'input ', 'i'):
        val = input('What is the exact AE term? ')
        #parameters to return input if the term is incorrect
        try:
            def_dict[val]
        except KeyError:
            print('This is not a valid AE, please try again')
            continue
        print("Would you like the definition for",val,'?')
        definition = input('')
        if val in ('Anemia','White blood cell decreased','Platelet count decreased','Hyponatremia'):
            grader_decreasing(val)
            continue
        # for AEs that use descriptive words
        if val in ('Conjunctivitis', 'Myelitis', 'Kidney anastomotic leak', 'Flu like symptoms', 'Non-cardiac chest pain', 'Pain', 'Myalgia', 'Myositis'):
            grader_characters(val)
            continue
        else:
            #for the AE that are not in decreasing ranges and do not use discriptive words
            grader_increasing(val)
            continue
    print ('Thank you for using the calculator!')
    print ('Go again:')
    continue
