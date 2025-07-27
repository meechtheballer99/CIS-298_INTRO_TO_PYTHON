import time #import time ahead of time so no wasted time on imports on the first call to some of the functions used for timing

#define a timing function that I can use to easily pass in any function to test it and for a desired number of iterations:
def timing_function(function_to_time, num_iterations=1):
    ##import time function in order to time our functions
    import time
    time_sum = 0
    total_iterations = num_iterations
    print("Number of iterations function will run:", num_iterations)
    while(num_iterations > 0):
        print("\nIteration#%d:"%(total_iterations - num_iterations + 1))
        start = time.perf_counter()
        function_to_time()
        end = time.perf_counter()
        elapsed_time = end - start
        print("----Time elapsed for iteration#%d:"% (total_iterations - num_iterations + 1),elapsed_time, sep='')
        time_sum += elapsed_time #track sum of time for all iterations
        num_iterations -= 1 #track iteration value
    print(  "----Total Time: %f----Average Time: %f"%( time_sum,(time_sum/total_iterations) )  )
    return (time_sum/total_iterations)
##Now, time given solutions, and develop my own solutions to time as well:


#soliution 1:
def even_nums_sol_1():
    print(*[n for n in range(1000, 3001) if all([(int(c) % 2 == 0) for c in str(n)])], sep=',')
#call timing function for solution 1:
print("\n---------TIMING FOR SOLUTION 1:")
timing_function(even_nums_sol_1,num_iterations=3)



#soliution 2:
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
#call timing function for solution 2:
print("\n---------TIMING FOR SOLUTION 2:")
timing_function(even_nums_sol_2,num_iterations=3)


#   B) Come up with a solution that is more efficient (faster).
#       Run 3 tests on it and record the average.

#my_solution_1:
def my_solution_1(lower_range=1000, upper_range=3000):
    lower_range_digits = list(map(int, str(lower_range))) #convert lower_range into a list of digits
    #cut down range of numbers to check in half by starting at the first even number in the range,
        #then only gathering all even numbers:
    if (lower_range % 2) == 1:
        lower_range += 1
    halved_search_list = range(lower_range, upper_range, 2)

    def check_all_digits_even(digits_list): #use this function to check for an odd digit in a list, if any
        for digit in digits_list:
            if digit % 2 == 1:
                return False #found an odd digit
        return True #if all digits are even
    for number in halved_search_list:
        if check_all_digits_even( list(map(int, str(number))) ): #map function maps elements in a string to integers in a list
            print(number,end=',')
    print() #print newline at end of function for cleaner output           
       
#call timing function for my_solution_1:
print("\n---------TIMING FOR MY_SOLUTION_1:")
timing_function(my_solution_1,num_iterations=3)
#timing_function(my_solution_1,num_iterations=3)


#   C) Supply your faster algorithm and the average result of all three algorithms.

#time all algorithms 3 times:
solution_1_avg = timing_function(even_nums_sol_1,num_iterations=3)
solution_2_avg = timing_function(even_nums_sol_2,num_iterations=3)
my_solution_1_avg = timing_function(my_solution_1,num_iterations=3)
print('\n***Average for all 3 functions = ',(solution_1_avg + solution_2_avg + my_solution_1_avg) / 3)


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
        b = (  -(c2) + (Discriminant)**(1/2)  ) / (2*c1)
        a = linear_combination_val - (c+d) - b 
        num_iterations_full += 1 #full iteration completed...
        print('Iteration_#_%d:'%(num_iterations_partial + num_iterations_full),
              'a=%f'%a,
              'b=%f'%b,
              'c=%f -> randomnly selected from range: (%f,%f]'%(c,lower_range,upper_range),
              'd=%f -> randomnly selected from range: (%f,%f]'%(d,lower_range,upper_range), sep='\n' )
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


##now time my function
import time
sum_elapsed_times = 0
num_runs = 100
num_runs_constant = num_runs
while num_runs > 0:
    start = time.perf_counter()

    mult_eq_sum_FourNums(linear_combination_val=7.11, precision=2, upper_range=1.8, lower_range=1.4)

    end = time.perf_counter()
    elapsed_time = end - start
    sum_elapsed_times += elapsed_time
    num_runs -= 1
    print("time elapsed:",elapsed_time, '\n')
print("\nAVERAGE TIME FOR %d RUNS:"%num_runs_constant, (sum_elapsed_times / 3))



''' #ALTERNATIVE SOLUTION TO QUESTION 6.2 #That I was working on that is competatively fast 
                                         #and maybe I can adapt some of it to my above algorithm to make it faster
import random
a= 0
b= 0
c= 0
d= 0
a_avg = 0
b_avg = 0
c_avg = 0
d_avg = 0
#a*b*c*d = 7.11
#a+b+c+d = 7.11
#random returns a number between 0 and 1 (inclusive)
#pick random numbers for a, b, and c, which ranges depend on each other and that are determined by a+b+c+d;
    #we know starting out that 'a' cannot be > 7.11, since that would leave no range for the other numbers.
    #then b has remaining range 7.11 - a
    #and c has remaining range 7.11 - a - b
    #and d is determined by what a, b, and c are because it will take whatever is left from total 7.11 range.
    #a+b+c+d will always = 7.11; but a*b*c*d may not be 7.11
#Then, we use a loop for brute force by using random numbers to satisfy the a*b*c*d=7.11 constraint:


num_iterations = 1
num_solutions = 0
find_n_solutions = 1
while round(a*b*c*d,2) != 7.11 or round(a+b+c+d, 2) != 7.11 or find_n_solutions > 0:
    a= 7.11 * random.random()
    b= (7.11 - a) * random.random()
    c= (7.11 - a - b) * random.random()
    d= (7.11 - a - b - c)
    print('a=%f\nb=%f\nc=%f\nd=%f'%(a,b,c,d))
    print("iteration - ", num_iterations,"sum=", a+b+c+d,"multiplication=", a*b*c*d)
    num_iterations += 1
    if(round(a*b*c*d,2) == 7.11 and round(a+b+c+d, 2) == 7.11):
        print("***SOLUTION FOUND!***")
        num_solutions += 1
        print('number of solutions found: ', num_solutions)
        #calculate in place average --> (curr_avg*curr_num_solutions + new_val) / (curr_num_solutions + 1):
        a_avg = ((a_avg * num_solutions) + a) / (num_solutions + 1)
        b_avg = ((b_avg * num_solutions) + b) / (num_solutions + 1)
        c_avg = ((c_avg * num_solutions) + c) / (num_solutions + 1)
        d_avg = ((d_avg * num_solutions) + d) / (num_solutions + 1)
        print("Averages: a_avg=%f, b_avg=%f, c_avg=%f, d_avg=%f"%(a_avg,b_avg,c_avg,d_avg))
        find_n_solutions -= 1
        num_iterations = 1 #reset num iterations
'''