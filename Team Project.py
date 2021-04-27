#!/usr/bin/env python
# coding: utf-8

# Cameron Wright  
# Dr. William Shoaff  
# CSE4081 - Analysis of Algorithms\
# 21st of April 2021  
# <center> <h1>Team Project: Quick Sort Analysis</h1> </center>

# In[1]:


from sys import stdout, stderr, getrecursionlimit, _getframe # Standard Out, Error Out, Stack limit, Current frame
from itertools import count                                  # Get number of element in variable 
from copy import deepcopy                                    # Copy content instead of pointing
from random import choice, sample, randrange                 # Random int list, Unqiue random int array, Random int [a,b]


# In[2]:


# Display all versions being used
get_ipython().run_line_magic('load_ext', 'watermark')
get_ipython().run_line_magic('watermark', '-v -iv')


# ## Scaffolding Functions

# ### Input

# In[3]:


# Generating sets of input arrays of length n (100, 1,000, ..., 10,000,000)
# containing integers 0 to (n-1).

# Unique random elements
uRandomArrays = [sample(range(0, 100), 100), 
                 sample(range(0, 1000), 1000), 
                 sample(range(0, 10000), 10000),
                 sample(range(0, 100000), 100000),
                 sample(range(0, 1000000), 1000000), 
                 sample(range(0, 10000000), 10000000)]

# Duplicate random elements
dRandomArrays = [[choice(range(100)) for i in range(100)], 
                 [choice(range(1000)) for i in range(1000)], 
                 [choice(range(10000)) for i in range(10000)],
                 [choice(range(100000)) for i in range(100000)],
                 [choice(range(1000000)) for i in range(1000000)], 
                 [choice(range(10000000)) for i in range(10000000)]]

# Sorted elements
sortedArrays = [sorted(sample(range(0, 100), 100)), 
                sorted(sample(range(0, 1000), 1000)), 
                sorted(sample(range(0, 10000), 10000)),
                sorted(sample(range(0, 100000), 100000)),
                sorted(sample(range(0, 1000000), 1000000)), 
                sorted(sample(range(0, 10000000), 10000000))]


# In[4]:


# Check if array is sorted
def isSorted(array):
    for e in range(len(array) - 1):
        if array[e] > array[e + 1]:
            stderr.write("Array not sorted: %d > %d\n" % (array[e], array[e + 1]) )
            return


# ### Stack (space )

# In[5]:


# Get current stack depth
def stackSize(size=2):
    frame = _getframe(size)

    for size in count(size):
        # Stop kernel from dying from stack overflow
        if size > limit[0] - 500:
            stderr.write("Stopped approaching max depth.")
            return -1
        
        frame = frame.f_back
        if not frame:
            return size


# In[6]:


# Redeclared to record stacksize
def qsStack(array, lower, upper):
    if lower < upper:
        if stackSize() == -1:
            return
        elif maxStack[0] < stackSize():
            maxStack[0] = stackSize()

        pivot = hoaresPartition(array, lower, upper)

        qsStack(array, lower, pivot)
        qsStack(array, pivot + 1, upper)


# In[7]:


# Run quickSort & return max depth
def getDepths(arrays):
    for x in range(len(arrays)):
        maxStack[0] = stackSize()
        qsStack(arrays[x], 0, len(arrays[x]) - 1)
        stdout.write("%d\n" % maxStack[0])


# ## Sorting Functions

# ### Quicksort

# In[8]:


def hoaresPartition(array, lower, upper):
    pivot = array[lower]
    i = lower - 1
    j = upper + 1

    while True:
        j -= 1
        while array[j] > pivot:
            j -= 1

        i += 1
        while array[i] < pivot:
            i += 1

        if i < j:
            array[i], array[j] = array[j], array[i]
        else:
            return j

# Original Hoares Partition Quicksort
def quickSort(array, lower, upper):
    if lower < upper:
        pivot = hoaresPartition(array, lower, upper)

        quickSort(array, lower, pivot)
        quickSort(array, pivot + 1, upper)


# In[9]:


# Time & check quickSort
def timeQS(arrays):
    for x in range(len(arrays)):
        # %timeit -<loops> -<repeats> -<precision>
        get_ipython().run_line_magic('timeit', '-n1 -r1 -p8 quickSort(arrays[x], 0, len(arrays[x])-1)')
        
        # Ensure array sorted
        isSorted(arrays[x])


# ### Caparison Sorting Algorithms

# **Standard Merge Sort**

# In[10]:


def mergeSort(array):
    if len(array) > 1:
        # Divide array
        middle = len(array)//2
        lower, upper = array[:middle], array[middle:]

        # Sort subarray
        mergeSort(lower)
        mergeSort(upper)
 
        i = j = k = 0
 
        while i < len(lower) and j < len(upper):
            if lower[i] < upper[j]:
                array[k] = lower[i]
                i += 1
            else:
                array[k] = upper[j]
                j += 1
            k += 1
 
        while i < len(lower):
            array[k] = lower[i]
            k += 1
            i += 1
 
        while j < len(upper):
            array[k] = upper[j]
            k += 1
            j += 1      


# In[11]:


# Time & check mergeSort
def timeMerge(arrays):
    for x in range(len(arrays)):
        # %timeit -<loops> -<repeats> -<precision>
        get_ipython().run_line_magic('timeit', '-n1 -r1 -p8 mergeSort(arrays[x])')

        # Ensure array sorted
        isSorted(arrays[x])


# **Randomized Pivot Hoares Parition Quicksort**

# In[12]:


# Hoare partition using a random pivot
def partitionRand(array , lower, upper):
    # Picking random pivot location
    pivot = randrange(lower, upper)

    array[lower], array[pivot] = array[pivot], array[lower]
    
    pivot = lower
    i, j  = lower - 1, upper + 1
    while True:
            i += 1
            if array[i] >= array[pivot]:
                
            j -= 1
            if array[j] <= array[pivot]:
                
        if i >= j:
            return j
        
        array[i] , array[j] = array[j] , array[i]

def quickSortRand(array, lower, upper):
    if(lower < upper):
        pivotIndex = partitionRand(array, lower, upper)

        quickSortRand(array , lower , pivotIndex)
        quickSortRand(array, pivotIndex + 1, upper)


# In[13]:


# Time & check quickSortRand
def timeQSR(arrays):
    for x in range(len(arrays)):
        # %timeit -<loops> -<repeats> -<precision>
        get_ipython().run_line_magic('timeit', '-n1 -r1 -p8 quickSortRand(arrays[x], 0, len(arrays[x])-1)')

        # Ensure array sorted
        isSorted(arrays[x])


# **Insertion Sort + Lomuto Partition Quicksort**

# In[14]:


def insertionSort(array, lower, upper):
    for i in range(lower + 1, upper + 1):
        currentValue = array[i]
        j = i
        while j > lower and array[j - 1]> currentValue:
            array[j] = array[j - 1]
            j -= 1
        array[j] = currentValue

# Partition using upper as pivot
def partition(array, low, upper):
    pivot = array[upper]
    i = j = low
    
    for i in range(low, upper):
        if array[i] < pivot:
            array[i], array[j] = array[j], array[i]
            j+= 1
    
    array[j], array[upper] = array[upper], array[j]
    return j

# Hybrid sort that uses quick sort on sub arrays lenght > threshold, else interstion sort
# only calls quick sort on smaller parition
def quickInsertion(array, lower, upper):
    while lower < upper:
        # Begin iterative solution if subarray < threshold
        if upper - lower + 1 < 11:
            insertionSort(array, lower, upper)
            break
  
        else:
            pivot = partition(array, lower, upper)
            
            # Call on smaller subarrayay
            if pivot - lower < upper - pivot:
                quickInsertion(array, lower, pivot - 1)
                lower = pivot + 1
            else:
                quickInsertion(array, pivot + 1, upper)
                upper = pivot - 1


# In[15]:


# Time & check quickInsertion
def timeQI(arrays):
    for x in range(len(arrays)):
        # %timeit -<loops> -<repeats> -<precision>
        get_ipython().run_line_magic('timeit', '-n1 -r1 -p8 quickInsertion(arrays[x], 0, len(arrays[x])-1)')

        # Ensure array sorted
        isSorted(arrays[x])


# ___
# # Results

# **Output Format:** \
# *100 Array* \
# *1,000 Array* \
# *...* \
# *10,000,000 Array*

# ### Time

# **Quicksort**

# In[16]:


# Unique random arrays
hundred, thous, tenthous, hunderedthous, mill, tenmill = deepcopy(uRandomArrays)
timeQS([hundred, thous, tenthous, hunderedthous, mill, tenmill])


# In[17]:


# Duplicate random elements
hundred, thous, tenthous, hunderedthous, mill, tenmill = deepcopy(dRandomArrays)
timeQS([hundred, thous, tenthous, hunderedthous, mill, tenmill])


# In[18]:


# Sorted arrays (10,000+ exceeds call stack depth, see space results)
hundred, thous, tenthous, hunderedthous, mill, tenmill = deepcopy(sortedArrays)
timeQS([hundred, thous])


# **Merge Sort**

# In[19]:


# Unique random arrays
hundred, thous, tenthous, hunderedthous, mill, tenmill = deepcopy(uRandomArrays)
timeMerge([hundred, thous, tenthous, hunderedthous, mill, tenmill])


# In[20]:


# Duplicate random elements
hundred, thous, tenthous, hunderedthous, mill, tenmill = deepcopy(dRandomArrays)
timeMerge([hundred, thous, tenthous, hunderedthous, mill, tenmill])


# In[21]:


# Sorted arrays
hundred, thous, tenthous, hunderedthous, mill, tenmill = deepcopy(sortedArrays)
timeMerge([hundred, thous, tenthous, hunderedthous, mill, tenmill])


# **Random Pivot Quicksort**

# In[22]:


# Unique random arrays
hundred, thous, tenthous, hunderedthous, mill, tenmill = deepcopy(uRandomArrays)
timeQSR([hundred, thous, tenthous, hunderedthous, mill, tenmill])


# In[23]:


# Duplicate random elements
hundred, thous, tenthous, hunderedthous, mill, tenmill = deepcopy(dRandomArrays)
timeQSR([hundred, thous, tenthous, hunderedthous, mill, tenmill])


# In[24]:


# Sorted arrays (10,000+ exceeds call stack depth also)
hundred, thous, tenthous, hunderedthous, mill, tenmill = deepcopy(sortedArrays)
timeQSR([hundred, thous])


# **Insert-Quicksort (Lomuto Partition)**

# In[25]:


# Unique random arrays
hundred, thous, tenthous, hunderedthous, mill, tenmill = deepcopy(uRandomArrays)
timeQI([hundred, thous, tenthous, hunderedthous, mill, tenmill])


# In[26]:


# Duplicate random elements
hundred, thous, tenthous, hunderedthous, mill, tenmill = deepcopy(dRandomArrays)
timeQI([hundred, thous, tenthous, hunderedthous, mill, tenmill])


# In[27]:


# Sorted arrays
hundred, thous, tenthous, hunderedthous, mill, tenmill = deepcopy(sortedArrays)
timeQI([hundred, thous, tenthous])


# ___
# ### Space

# **Quicksort**

# In[28]:


limit = [getrecursionlimit()] # Maximum call stack depth of kernel
maxStack = [0]                # Deepest stack point of function


# In[29]:


# Unique random arrays
hundred, thous, tenthous, hunderedthous, mill, tenmill= deepcopy(uRandomArrays)
getDepths([hundred, thous, tenthous, hunderedthous, mill, tenmill])


# In[30]:


# Duplicate random arrays
hundred, thous, tenthous, hunderedthous, mill, tenmill = deepcopy(dRandomArrays)
getDepths([hundred, thous, tenthous, hunderedthous, mill, tenmill])


# In[31]:


# Sorted arrays
hundred, thous, tenthous, hunderedthous, mill, tenmill = deepcopy(sortedArrays)
getDepths([hundred, thous, tenthous, hunderedthous, mill, tenmill])


# <br>
