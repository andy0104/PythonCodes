#Lists in python are a collection of values stored in the order
#of their arrival, data items can be of multiple data types like an array
#Index starts from 0
hairs = ['brown', 'blonde', 'red']
weights = [1, 3, 4, 2, 5]

print (hairs)
print (weights[4])

fruits = ['apple', 'orange', 'banana', 'apricots', 'pears']

#Mixed List
change = [1, 'pennies', 'dimes', 2, 'quarters']

#Looping through the list using for loop
for fruit in fruits:
    print ('A fruit of type: %s' % fruit)

#Looping through a mixed list
for as_change in change:
    print ('I got %r as change.' % as_change)

#Creating a list from an empty list
elements = []

#Using range function to loop through a range of numbers
for num in range(10, 25):
    print ('Adding %d to the new list' % num)
    #Appending value to list
    elements.append(num)

#Print the newly created list
print ('New list')
print (elements)

#Size of new list
print ('Size of new list: {x} ' . format(x = len(elements)))

#Slicing a list

#slice from 3rd element
print (elements[2:])

#slice upto 5th element
print (elements[:5])

#Concatenate lists
list5 = []
list5 = fruits + elements
print (list5)

#Double list
print (list5 * 2)

#Grab the last item
last_item = list5.pop()
print (last_item, list5)

#Sort the list
fruits.sort()
print (fruits)

#Reverse the list
fruits.reverse()
print (fruits)

#Dimensional Lists
l_1 = [1, 2, 3]
l_2 = [4, 5, 6]
l_3 = [7, 8, 9]
matrix = [l_1, l_2, l_3]
print (matrix)

#Length of matrix
print (len(matrix))

#Printing all the elements of matrix
mat_len = len(matrix)
i = 0
j = 0

print ('-' * 10)
print ('Printing Matrix')
while i < mat_len:
    j = 0
    while j < mat_len:
        print ('matrix[%d][%d]: %r ' % (i, j, matrix[i][j]))
        j += 1

    print ('\n')
    i += 1

#List comprehensions
x = 'word'
l = []
for item in x:
    print (x)
    l.append(item)

print (l)

#List comprehensions
lst = [item for item in x]
print (lst)

lst = [x**2 for x in range(0, 11)]
print (lst)

#Print even numbers in a range
lst = [number for number in range(11) if number % 2 == 0]
print (lst)

#Celsius to Fahrenheit
celsius = [0, 10, 45, 13, 20.1, 10.5]
farhenheit = [(far * (9/5.0) + 32) for far in celsius]
print (farhenheit)

#Nested list comprehensions
lst = [x**2 for x in [x**2 for x in range(11)]]
print (lst)
