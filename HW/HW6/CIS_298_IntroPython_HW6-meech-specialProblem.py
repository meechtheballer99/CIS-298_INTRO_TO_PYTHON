#Author: Demetrius Johnson
#CIS-298 Intro to Python with Professor Robert Mann
#HW6 - Algorithmic Efficiency
#Remember to copy/paste your code for each question separately. 
#Then, follow it with a snippet showing the output.
#Due: Thu March 09, 2023 4:00pm


#Question 6 (from hw5 question 10) - Make it work.  Then make it better.
 
#Here is my original solution from hw5, question 10
def even_nums_MySol_1():
    for number in range(1000, 3001, 2): # range [1000, 3001] and only return a number every 2 values (step = 2)
        print(number, ', ', end = '')
#note: range function returns an iterable list with only even numbers based on the parameters I passed to the function
#even_nums_MySol_1() #call my function


#From Professor: 
#In grading homework 5 I noticed a variety of solutions 
#to question 10 (print all numbers between 1000 and 3000,inclusive, where each digit is even). 
#I appreciate questions like this for it allows me to see a range of thinking on how to solve a problem.  

#Here are two solutions that were given:

#Solution 1:
#print(*[n for n in range(1000, 3001) if all([(int(c) % 2 == 0) for c in str(n)])], sep=',')

#Solution 2:
#numbers = []
#for i in range(1000, 3001):
#    is_even = True
#    for j in str(i):
#        if int(j) %2 == 1:
#            is_even = False
#    if is_even:
#        numbers.append(i)
#print(numbers)



#The second solution takes more coding but essentially does the same thing.  
#Part of writing software (or doing analysis, at least) is identifying patterns of what needs to be done.  
#Making a problem generic can sometimes help in this regard (find numbers between x and y, etc.).  
#Looking at a problem in a different way (thinking outside of the box) can provide a unique solution as well. 
#One thing to always remember is that just because something is a number doesn't mean it has to be treated as a number.  
#Think of phone numbers or social security numbers. 
#While they contain only digits, one almost never performs mathematical operations against them 
#so they could just as easily be strings, and probably should be.

#The two solutions above are more efficient than examining every number between 1000 (or x) and 3000 (or y), 
#but they could be more efficient yet.  Think about what problem we're trying to solve.  
#The first solution is probably a good one, but is there a better one?  If the 10's position contains an odd number, 
#does it matter what the digit is in the one's position? No, so we should move to the next 10's position value. 
#The same holds true for 100's and 1000's positions.

#Q6.1[10 pts]. Determine how to time programs in Python.
#   A) Run 3 tests of each of the first two solutions given above 
#       and average the results.  

def even_nums_sol_1():
    print(*[n for n in range(1000, 3001) if all([(int(c) % 2 == 0) for c in str(n)])], sep=',')

#even_nums_sol_1()

def even_nums_sol_2():
    numbers = []
    for i in range(1000, 3001):
        is_even = True
        for j in str(i):
            if int(j) %2 == 1:
                is_even = False
        if is_even:
            numbers.append(i)
    print(numbers)

#even_nums_sol_2()


#   B) Come up with a solution that is more efficient (faster). 
#       Run 3 tests on it and record the average. 
#   C) Supply your faster algorithm and the average result of all three algorithms.





#Q6.22[50]. Deep dive into logically cutting corners in a solution through analysis. 
#Find a solution to this problem that executes in under 1 second (can it be even faster?) without hardcoding the answer.
#Displaying values takes a long time so remove most output statements once you’re getting close. 
#I'll spare you the long version of the question. 
#Simply do this: find the price of four items who's sum and who's product both equal 7.11.  So, a+b+c+d == a*b*c*d == 7.11.  
#There may be more than one answer.  I originally solved this problem 37 years ago (in C). My initial algorithm ran for over 12 hours.  
#My deep dive analysis produced one that solved it in about 1 second.  Supply your final algorithm and how long it takes to solve the problem.

#Find the price of four items who's sum and who's product both equal to 7.11.
#So, a+b+c+d == a*b*c*d == 7.11

#I will adapt my random number generator code from hw4 question 3 to generate 4 random numbers
#
from distutils import bcppcompiler
import random
def get_randmon_num(positive_range=100, negative_range=100):
   #random() function returns a number between 0 and 1
   #multiply 100*random() and subtract 100*random() in order to make the values have a range of Minimum [100, -100]
   #cast as int just to get integer random number values  
   #return the random number if it is nonzero, else return 1 --> thus making our range [100, -100, exclude 0]
    random_num = int( positive_range * random.random() - negative_range * random.random() )
    return random_num if random_num else 1

linear_combination_val = 7.11
#set negative range = 0 since prices of items must be nonzero
a = get_randmon_num(negative_range=0)
b = get_randmon_num(negative_range=0)
c = get_randmon_num(negative_range=0)
d = get_randmon_num(negative_range=0)
print(a,b,c,d, sep='\n')
print('linear combination value: ', linear_combination_val, end='\n\n')

#now I will normalize each number --> number = number/sum_of_numbers; then all numbers summed after this sum to 1
sum_of_numbers = a + b + c + d
a /= sum_of_numbers
b /= sum_of_numbers
c /= sum_of_numbers
d /= sum_of_numbers

#now we can take those normalized values and multiply by linear_combination value to get expected value
#then all numbers will sum to  linear_combination value; thus a+b+c+d = linear_comb value is solved
a *= linear_combination_val
b *= linear_combination_val
c *= linear_combination_val
d *= linear_combination_val
print('linear combination value: ', a+b+c+d, a*b*c*d)

#now we have to solve the problem a*b*c*d = linear_combination value
#we need to find weights x1,x2,x3, and x4, such that: ax1 * bx2 * cx3 * dx4 = a+b+c+d = linear_combination_val
    #we could write it as: (x1*x2*x3*x4) * (a*b*c*d) = a+b+c+d = linear_combination_val
    #or as:  (x1*x2*x3*x4) * (a*b*c*d) = linear_combination_val
    #which can be written as: (x1*x2*x3*x4) = linear_combination_val / (a*b*c*d)
#we first need to check by what factor larger or smaller is linear_combination compared to all numbers multiply by each other:
overall_size_factor = linear_combination_val / (a*b*c*d)
a *= overall_size_factor * linear_combination_val
b *= overall_size_factor * linear_combination_val
c *= overall_size_factor * linear_combination_val
d *= overall_size_factor * linear_combination_val


#So after further analysis, I can actually stop solving the above problems by simplifying the problem!
#let c = d = 1. Then the problem is simplified from:
    #abcd=7.11 and a+b+c+d=7.11 
    #to ab*1*1 = 7.11 and a+b+1+1 = 7.11
    #which simplifies to: ab=7.11 and a+b=5.11
    #thus we simply need to solve a system of questions:
    #a = 7.11/b, a=5.11-b --> 7.11/b = 5.11-b --> 7.11 = 5.11b - b^2
    #now solve using quadratic formula --> b^2 -5.11b +7.11 = 0
    #quadratic formula, which yields 2 solutions for b:
    # solution 1: -(-5.11) (+) sqrt(-5.11^2 - 4*1*7.11) * (1/(2*1))
    # solution 2: -(-5.11) (-) sqrt(-5.11^2 - 4*1*7.11) * (1/(2*1))
#once we use one of the solutions for be, we simply plug in b's value to any one of our system of equations to solve for a
c = d = 1


print("overall size factor =",overall_size_factor)
print(a,b,c,d,sep='\n')
print('linear combination value: ', a+b+c+d, a*b*c*d)


