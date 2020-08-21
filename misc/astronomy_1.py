
# coding: utf-8

# Samples light from space in 5 filters u,g,r,i,z to determine which type of light is most prominent in space

# In[1]:


import urllib.parse
import urllib.request
from astropy.table import Table, Column
import numpy as np


# In[2]:


SEARCH_API_BASE = "http://cas.sdss.org/dr7/en/tools/search/x_sql.asp"

def run_query(sql):
    url = SEARCH_API_BASE + '?' + urllib.parse.urlencode({
        'format': 'csv',
        'cmd': sql,
    })
    with urllib.request.urlopen(url) as conn:
        return conn.read().decode('ascii')


# In[3]:


def params(ra1,ra2,dec1,dec2):
    param = ra1,ra2,dec1,dec2
    select = "SELECT p.objid,p.ra,p.dec,p.u,p.g,p.r,p.i,p.z"
    from_ = "FROM PhotoObj AS p"
    where = "WHERE p.ra BETWEEN {0} AND {1} AND p.dec BETWEEN {2} AND {3}".format(*param)
    query = select + "\n"  + from_ + "\n"  + where
    return query


# In[4]:


def data_organize(data):
    data = data.splitlines()
    names = data[0].split(",")
    numbers = data[1:]
    data_org = {names[j]:[] for j in range(len(names))}
    for i in numbers:
        u = i.split(",")
        for j in range(len(names)):
            data_org[names[j]].append(u[j])
    return data_org


# In[5]:


def make_table(data_org):
    data_table = Table(data_org)
    return data_table


# In[6]:


def amt_flux(mags):
    mag_list = list(map(float, mags))
    flux = 0
    for mag in mag_list:
        if mag > 0:
            flux = flux +  0.398**mag  # in reference fluxes of magnitude 0
    return flux


# In[7]:


ra = 23
dec = 25
query = params(ra, ra + 2 , dec , dec + 1)
data = run_query(query)


# In[8]:


data_org = data_organize(data)


# In[9]:


data = data.splitlines()
names = data[0].split(",")
names


# In[10]:


total = 0
for i in range(3,len(names)):
    res = amt_flux(data_org[names[i]])
    total += res

print(ra , dec, len(data_org["u"]))
for i in range(3,len(names)):
    res_perc = [names[i] , amt_flux(data_org[names[i]])/total]
    print(res_perc[0] + ":  " + "{0:f}".format(100 * res_perc[1]) + "%")


# 0 0
# u:  3.164808%
# g:  15.246707%
# r:  25.659541%
# i:  27.533295%
# z:  28.395650%
# 
# 1 1
# u:  10.440330%
# g:  11.149212%
# r:  21.862592%
# i:  23.080103%
# z:  33.467763%
# 
# 2 1 6445
# u:  4.922033%
# g:  9.950156%
# r:  34.936273%
# i:  22.389618%
# z:  27.801920%
# 
# 2 0 25660
# u:  3.801093%
# g:  14.324746%
# r:  23.655816%
# i:  25.237648%
# z:  32.980697%
# 
# 3 0 25877
# u:  2.951091%
# g:  11.653821%
# r:  25.555379%
# i:  30.004270%
# z:  29.835438%
# 
# 20+8 30 37399
# u:  2.966457%
# g:  12.721524%
# r:  25.850285%
# i:  27.916860%
# z:  30.544875%
