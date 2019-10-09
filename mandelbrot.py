
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import math as ma


# In[2]:


def bico(n,r):
    if n - r >= 0 and r <= n:
        return ma.factorial(n)/(ma.factorial(n - r) * ma.factorial(r))
    else:
        return 0
    


# In[3]:


def imsq(arr):
    x = arr[0]**2 - arr[1]**2
    y = 2 * arr[0] * arr[1]
    return np.array([x , y])


# In[4]:


def imall(n,arr):
    x = arr[0]
    y = arr[1]
    R = 0
    I = 0
    for run in range(int(n//2 + 1)):
        r = 2*run
        R = R + (x**(n - r)) * (y ** r) * bico(n, r) * (-1)**run
    
    for Irun in range(round(n/2)):
        k = (2 * Irun) + 1
        I = I + (x**(n - k)) * (y ** k) * bico(n , k) * (-1)**Irun
    return np.array([R, I])


# In[5]:


def imcu(arr):
    x = arr[0]
    y = arr[1]
    R = x**3 - 3*x*y**2
    I = 3*y*x**2 - y**3
    return np.array([R , I])


# In[8]:


n = 300
x = []
y = []
for xvar in range(n):
    for yvar in range(n):
        a = -2 + 4*xvar/(n)
        b = -2 + 4*yvar/(n)
        z = np.array([0,0])
        c = np.array([a,b])
        for var in range(0,10):
            #z = imsq(z) + c
            z = imall(2 , z) + c
            if z[0]**2 + z[1]**2 > 4:
                x.append(a)
                y.append(b)
                break
                
plt.figure(figsize=(15,15))                
plt.scatter(x , y,s= 4,c="purple")

plt.show()

