# Create Numpy Array
array_literal = np.array([1, 2, 3, 4])

array_ones = np.ones((2, 3))

# scp -r /Users/spencersymington/Downloads/PNG/ pi@10.184.1.144:/home/pi/Documents

# Write/Read file
L = ["Geeks\n", "for\n", "Geeks\n"]
  
# writing to file
file1 = open('myfile.txt', 'w')
file1.writelines(L)
file1.close()
  
# Using readlines()
file1 = open('myfile.txt', 'r')
Lines = file1.readlines()
  
count = 0
# Strips the newline character
for line in Lines:
    count += 1
    print("Line{}: {}".format(count, line.strip()))