org=[]
new=[]
len=int(input("enter the size of the array"))
print("enter the elements into the array :")
for i in range(0,len,1):
    c=int(input("enter the value:"))
    org.append(c)
print("the orginal array:",org)
val=int(input("enter the element to be removed "))
for i in org:
    if i==val:
        continue
    else:
        new.append(i)
#org = [i for i in org if i != val]
print("the updated array:",new)