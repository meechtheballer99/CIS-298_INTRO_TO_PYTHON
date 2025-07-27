#Author: Demetrius Johnson
#CIS-298 Intro to Python with Professor Robert Mann
#HW8 - Working with matplotlib
#Remember to copy/paste your code for each question separately. 
#Then, follow it with a snippet showing the output.
#Due: Thu March 28, 2023 4pm



#Description

#For this project you will be reading a file, counting occurrences of all letters and numbers, 
#and displaying the results in a histogram.

 

#Requirements:

#Your input file is the syllabus for this course, found on Canvas under files. 
#Use the text version (you may read the docx version if you’d like but it needs a library).  
#Read the file, counting the number of times each letter
#(not differentiating between uppercase and lowercase) and number appears (a-z, A-Z, 0-9; 36 total items).  
#Display the results as a histogram with appropriate title and labels for x-axis and y-axis.

Syllabus_File = open("Syllabus_CIS298_001MannW23.txt")
print(Syllabus_File.read())

#seek back to beginning of file since I already read all lines and current pos is EOF:
Syllabus_File.seek(0) 
#Now store the contents of the file as a string, 
file_data_char_tokens = Syllabus_File.read()

#First, identify every unique character in the string to create a list of unique characters:
unique_chars = []
for character in file_data_char_tokens:
    if unique_chars.count(character) == 0:
        unique_chars.append(character)
print(unique_chars)

#create list of the ASCII decimal equivalent of the unique chars for easier comparisons:
unique_chars_ord_nums = [ord(character) for character in unique_chars]
print(unique_chars_ord_nums)

#now, we can check criteria by using the unique chars string:
for ord_character in unique_chars_ord_nums:
    if ( 
        not (ord_character >= 48 and ord_character <= 57) #characters 0-9
        and
        not (ord_character >= 65 and ord_character <= 90) #characters A-Z
        and
        not (ord_character >= 97 and ord_character <= 122) #characters a-z
       ): 
        #if character is not in each of the above ranges,
        #then the character is non-alphabetical AND non-numeric, and we need to remove it
        file_data_char_tokens = file_data_char_tokens.replace(chr(ord_character), '')
       

print(file_data_char_tokens)
#now we need to handle ignore upper and lower case condition (treat lower and upper as the same char);
#use the upper() function to change all lower case char to upper case:
file_data_char_tokens = file_data_char_tokens.upper()
print(file_data_char_tokens)

#Now we create a list, where each element is --> [char, frequency]:

#48-57 decimal = ascii char 0-9
char_frequencies = [ [chr(ord_character),0] for ord_character in range(48,58) ]
#65-90 decimal = ascii char A-Z
char_frequencies += [ [chr(ord_character),0] for ord_character in range(65,91) ]
#now go to each [char, freq] list in char_frequencies and get num of occurences in our string,
#storing the result in the respective freq in [char, freq] element:
for element_num, element in enumerate(char_frequencies):
    char_frequencies[element_num][1] = file_data_char_tokens.count(element[0])
print(char_frequencies)

#Now, we have the frequencies of each 0-9, A-Z, and a-z characters where A-Z == a-z characters of the file.
#We can now create a histogram using matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

#change the columns of char_frequency list into numpy arrays so we can pass it to pyplot histogram function
char_array=np.array([characters[0] for characters in char_frequencies])
freq_array=np.array([freq[1] for freq in char_frequencies])
print(char_array)
print(freq_array)



#now we can plot a bar graph (prof said we can use histogram OR bar gaph; 
#in this situtation it makes no sense to create a histogram based on the frequencies of the frequencies, rather
#we only need to plot the category (letter/num) and associated frequency (stored in y):
plt.bar(char_array, freq_array)
# Set the x and y axis labels and title
plt.xlabel('Letter/Numbers')
plt.ylabel('Frequency')
plt.title("Syllabus_CIS298_001MannW23.txt - letter and number Frequencies")
plt.show()

#print as an array so you can see the letter/number and associated frequency:
print(np.array(char_frequencies))



#Report:

#Submit a report listing your script and a snippet (snipping tool) showing your histogram.  
#Make sure your snippet demonstrates all program requirements as having been met.

