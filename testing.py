def swap(arr, i1, i2):
    temp = arr[i1]
    arr[i1] = arr[i2]
    arr[i2] = temp

def heapConstruct(arr):
    for x in range(len(arr)-1, 0, -1):
        if(ord(arr[(x+1) // 2]) < ord(arr[x])):
            swap(arr, x, (x+1) / 2)

def heapSort(arr):
    heapConstruct(arr)
    

arr = ['S', 'O', 'R', 'T', 'E', 'X', 'A', 'M', 'P', 'L', 'E']
heapConstruct(arr)