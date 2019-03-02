
# coding: utf-8

# Assuming a regular polygon with perimiter of 10 which regular polygon produces the maximum area.
# Equation derived to determine area based on amount of sides (n) and length of perimiter (p)

# In[2]:


import matplotlib.pyplot as plt
import numpy as np


# In[3]:


n = np.arange(3,100)
p = 10
plt.figure(figsize=(20,10))

A = (p**2) * 1/(4*n)*np.tan((n - 2)* np.pi/(2 * n))
plt.scatter(n , A)

plt.show()


# In[4]:


x = np.arange(3, 10)
print(x)


# In[5]:


np.tan(0)


# In[6]:


p = 70
n = 7
A = (p**2) * 1/(4*n)*np.tan((n - 2)* np.pi/(2 * n))
print(A)


# In[9]:


n = np.arange(3,400)
p = 10
A = (p**2) * 1/(4*n)*np.tan((n - 2)* np.pi/(2 * n))
for i in range(len(n)):
    if i > 0:
        delta = A[i] - A[i - 1]
    else:
        delta = 0
    print(n[i], "|||", A[i], "|||  delta:", delta)
    
    if delta < 0:
        print("heeyyyyy")


# In[8]:


np.pi * (10/(2*np.pi))**2  ## circle (aka infinitely sided regular polygon) area with p = 10

