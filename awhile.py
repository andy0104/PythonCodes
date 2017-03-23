#While Looping
i = 0
r = 0

#Empty list
elements = []

while i < 6:
    print ('Adding %d to the list' % i)
    elements.append(i)
    i += 1

#Loop through the list elements
for num in elements:
    print ('Element: %d' % num)

#While statement with a final else
#Else is executed after the while is done
x = 0
while x < 10:
    print ('x is currently: %d' % (x))
    x += 1

    if x >= 10:
        print ('Alert: x is greater than 10')
        break
else:
    print ('All Done!')
