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


#I found from my analysis that using range of number from [5,0) yields a fast result since solutions seem to be very small numbers.
#thus, that is why I make default upper and lower range to be 5, 0 respectively. Precision is 2 by default because of problem requirements.
def mult_eq_sum_FourNums(linear_combination_val=7.11, precision=2, upper_range=5, lower_range=0):
    #I will adapt my random number generator code from hw4 question 3 to generate 2 random numbers
    import random
    def get_randmon_num(positive_range=100, negative_range=100):
       #random() function returns a number between 0 and 1
       #Multiply 100*random() and subtract 100*random() in order to make the values have a range of [-100, 100]
       #Return the random number if it is nonzero, else return 1 --> thus making our range [-100, 100, exclude 0]
        random_num = positive_range * random.random() - negative_range * random.random()
        return random_num if random_num else 1

    #need to find a solution for items a and b
    a = 0
    b = 0
    c = 0
    d = 0
    #use these just for metric purposes
    num_iterations_partial = 0
    num_iterations_full = 0
    num_iterations_total = 0

    #Now use this loop to find a solution for a and b that does not include the complex number solutions:
    while (a <= 0) or (b <= 0) or \
          ( round(a*b*c*d,precision) != round(linear_combination_val,precision) ) or \
          ( round(a+b+c+d,precision) != round(linear_combination_val,precision)
    ):
        #So after further analysis, I realize I can simplify the problem!
        #let c and d be any (random) number, then the problem is simplified from:
        #now generate 2 random values (we will use range (0,100]) that will be used)
        #set negative range = 0 since prices of items must be nonzero
        c = get_randmon_num(positive_range=upper_range,negative_range=lower_range)
        d = get_randmon_num(positive_range=upper_range,negative_range=lower_range)
            #abcd=7.11 and a+b+c+d=7.11 
            #to ab*c*d = 7.11 and a+b+c+d = 7.11, where c and d are known (chosen/selected).
            #which simplifies to: ab=7.11/cd and a+b=7.11-(c+d)
            #thus we simply need to solve a system of equations for terms a and b:
                #EQUATION_1: a = (7.11/cd)/b, 
                #EQUATION_2: a = 7.11 - (c+d) - b 
            #--> (7.11/cd)/b = 7.11 - (c+d) - b 
            #--> (7.11/cd) = 7.11b - (c+d)b - b^2
            #--> -(7.11/cd) = -7.11b + (c+d)b + b^2
            #--> b^2 + (c+d)b - 7.11b = -(7.11/cd)
            #--> b^2 + (c+d-7.11)b + (7.11/cd) = 0
            #now solve using quadratic formula: x = (-c2 (+/-) sqrt[c2^2 -4*c1*C]) / 2*c1, 
                #where c_i is a coefficient of ith-power term, C is a constant
        c1 = 1
        c2 = (c+d-linear_combination_val)
        C = (linear_combination_val/(c*d))
        Discriminant = c2**2 - 4*c1*C 
            #use quadratic formula, which yields 2 possible solutions for b:
            # solution 1 for b: (  - (c+d-7.11) (+) sqrt[(c+d-7.11)^2 - 4*1*(7.11/cd)]  ) / (2*1)
            # solution 2 for b: (  - (c+d-7.11) (-) sqrt[(c+d-7.11)^2 - 4*1*(7.11/cd)]  ) / (2*1)
        #once we use one of the solutions for b, we simply plug in b's value to any one of our system equations to solve for a
        #We first need to do a special check on the discriminant D = c2^2-4*c1*C :
            #if D < 0, then sqrt(c2^2-4*c1*C) will be a complex number since it will take sqrt of a negative number (complex solution);
            #if D > 0, then there are two real roots (thus 2 real number solution)
            #if D == 0, then there is one real root (thus one real number solution)
        #A simpler way of saying this is that if c2^2 < 4*c1*C, then sqrt(c2^2-4*c1*C) will be a complex number;
            #thus, we need to check for this and skip this loop since values chosen for c and d will produce complex solutions:
        if Discriminant < 0:
            num_iterations_partial += 1
            continue #move to next loop and try with 2 new values for c and d
        #otherwise, continue the algorithm (I will use solution 1 equation to solve for b):
        b = (  -(c2) + ( (c2)**2 - 4*c1*C )**(1/2)  ) / (2*c1)
        a = linear_combination_val - (c+d) - b 
        num_iterations_full += 1 #full iteration completed...
        print('Iteration_#_%d:'%(num_iterations_partial + num_iterations_full),
              'a=%f'%a,'b=%f'%b,'c=%f'%c,'d=%f'%d, sep='\n' )
        print('Is a+b+c+d == a*b*c*d?: ', a+b+c+d, '==', a*b*c*d, '?')
    ##end of WHILE loop##
    
    #set total number of iterations metric
    num_iterations_total = num_iterations_partial + num_iterations_full

    #print final results:
    print('\n\n**SOLUTION FOUND WITH ALL POSTIVE VALUES**:', 'a=%f'%a,'b=%f'%b,'c=%f'%c,'d=%f'%d, 
          'partial_iterations:%d (due to Discriminant < 0)'%num_iterations_partial,
          'full_iterations:%d'%num_iterations_full,
          'total_iterations:%d'%num_iterations_total, sep='\n' )
    print('Is a+b+c+d == a*b*c*d?: ', a+b+c+d, '==', a*b*c*d, '? --> YES, solution found (rounded to %d decimal places)!'%precision)
##end of mult_eq_sum_FourNums() function##

import time

start = time.perf_counter()

mult_eq_sum_FourNums(linear_combination_val=7.11, precision=1, upper_range=1.2, lower_range=0)

end = time.perf_counter()
elapsed_time = end - start

print("time elapsed:",elapsed_time)

