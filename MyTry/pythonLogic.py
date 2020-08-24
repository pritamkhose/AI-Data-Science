# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 12:29:54 2020

@author: Pritam
"""
def modify_list(arg_list):
    arg_list=arg_list + [60, 70, 80]
    print("Inside function:", arg_list)
    return arg_list
    
i_list=[10,20,30,40,50]
print("Before function call:", i_list)
i_list = modify_list(i_list)
print("After function call:", i_list)

my_list=[0]*5
for index in range(1,5):
    my_list[index]=(index-1)*index
                    
print(my_list)
 
FHW=open("data.txt","w")
FHW.write("written some thing")
print(FHW.tell())
print("closed?",FHW.closed)
FHW.close()
print("after closing the file closed?",FHW.closed)

set_1={1,2,3,1,2,4,5,3,4,8,9,7}
print((set_1))
print(len(set_1))
for index in range(len(set_1)):
    print(index,end=" ")

print('------------')  
def value(num1):
    list1=[]
    while num1!=0:
        if num1%2==0:
            list1.append(num1)
        else:
            break
        num1-=2
    print(list1)
value(10) 


def sample(value):
    sum1=0
    for i in value:
        print(i, value[i], i%2, sum1)
        if i%2!=0:
            sum1+=value[i]
        else:
            sum1-=i
    print(sum1)
dict1={1:2,2:4,3:6,5:8}
sample(dict1)


tuple1=(10)
print(tuple1)
print(type(tuple1))


sample_dict={'a':"apple",'b':"ball"}
sample_dict.update({'b':"boy", 'c':'cat' })
print(sample_dict['a'],sample_dict.get('b'),sample_dict.get('c'))


def find_sum(a,b):
    try:
        print(a+c)
    except ValueError:
        print("Function name error")
    finally:
        print("Sum finally")
try:
    find_sum(12,13)
except NameError:
    print("Invocation name error")
finally:
    print("Invocation finally")