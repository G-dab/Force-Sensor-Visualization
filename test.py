import numpy as np

a = np.array([1,2,3,4,5,6,7,8,9,10])
print(a)
# 在a前面插入一个元素,末尾元素舍弃
a = np.insert(a, 0, 0)
a = a[:-1]
print(a)
a = np.insert(a, 0, 1)
a = a[:-1]
print(a)
a = np.insert(a, 0, 1)
a = a[:-1]
print(a)
a = np.insert(a, 0, 1)
a = a[:-1]
print(a)

