
# coding: utf-8

# In[22]:


get_ipython().run_line_magic('matplotlib', 'notebook')


# In[ ]:


get_ipython().run_line_magic('run', 'SP_lib.ipynb')


# In[14]:


##LOAD data
df = pd.read_excel("SNP_100_CX_ALT2.xlsx", index_col="Date")


# # PREPARE TRAINING

# In[299]:


for i in range(0,len(df.columns),9): print(df.columns[i:i+9]) 


# In[301]:


x_train, y_train, x_valid, y_valid, x_test, y_test, splits = setup_data(df[["SPY"]][800:], df["SPY"][800:], sample_size= 128,
                                                                  percent_split= [0.85, 0.1])


# In[302]:


[y_train, y_valid, y_test] = map(lambda x: BS(x), [y_train, y_valid, y_test])


# In[306]:


model = setup_OGsuper(x_train , binary = True)


# In[307]:


train_model(model , 1, True, x_train, y_train, x_valid, y_valid)


# In[309]:


model.evaluate(x_test, y_test)[1]


# In[308]:


demo(model.predict(x_valid) , y_valid)


# # Models

# In[34]:


def setup_OGsuper(x, dropout_value = 0.05, binary = False):
    d = dropout_value
    model = Sequential()
    model.add(LSTM(128, input_shape=(x.shape[1:]), return_sequences=True))
    model.add(Dropout(d))
    model.add(Conv1D(64, 10, strides = 5,  data_format="channels_first"))
    model.add(Conv1D(16, 5, strides = 2, data_format="channels_first"))
    model.add(Dropout(d))
    model.add(Flatten())
    model.add(Dense(64))
    model.add(Dropout(d))
    model.add(Dense(16))
    if binary == False:
        model.add(Dense(1))
        model.compile(optimizer="adam", loss="mse")
    else:
        model.add(Dense(2 , activation = "softmax"))
        model.compile(optimizer="adam", loss="binary_crossentropy" , metrics=["accuracy"])

    return model


# In[35]:


def setup_LSTM(x, dropout_value = 0.3 , binary = False):
    nodes = x.shape[2]
    d = dropout_value
    model = Sequential()
    model.add(LSTM(nodes, input_shape=x.shape[1:], return_sequences=True))
    model.add(Dropout(d))
    model.add(LSTM(nodes, return_sequences=True))
    model.add(Dropout(d))
    model.add(LSTM(nodes, return_sequences=True))
    model.add(Dropout(d))
    model.add(LSTM(nodes, return_sequences=False))
    model.add(Dropout(d))
    if binary == True:
        model.add(Dense(2 , name = "last" , activation = "softmax"))
        model.compile(optimizer="adam", loss="binary_crossentropy" , metrics=["accuracy"])
    else:
        model.add(Dense(1 , name = "last"))
        model.compile(optimizer="adam", loss="mse")

    return model


# In[36]:


def setup_simple(x, dropout_value = 0.1 , binary = False):
    d = dropout_value
    model = Sequential()
    model.add(LSTM(50, input_shape=x.shape[1:], return_sequences=False))
    model.add(Dropout(d))
    if binary == True:
        model.add(Dense(2 , name = "last" , activation = "softmax"))
        model.compile(optimizer="adam", loss="binary_crossentropy" , metrics=["accuracy"])
    else:
        model.add(Dense(1 , name = "last"))
        model.compile(optimizer="adam", loss="mse")

    return model


# In[37]:


def setup_deep(x, dropout_value = 0.1 , binary = False):
    d = dropout_value
    model = Sequential()
    model.add(Flatten())
    for n in range(9 , 3 , -1):
        model.add(Dense(2**n))
        model.add(Dropout(d))
    if binary == True:
        model.add(Dense(2 , name = "last" , activation = "softmax"))
        model.compile(optimizer="adam", loss="binary_crossentropy" , metrics=["accuracy"])
    else:
        model.add(Dense(1 , name = "last"))
        model.compile(optimizer="adam", loss="mse")

    return model


# In[38]:


def setup_super(x, dropout_value = 0.1, binary = False):
    nodes = x.shape[2] * 2
    d = dropout_value
    model = Sequential()
    model.add(LSTM(nodes, input_shape=x.shape[1:], return_sequences=True))
    model.add(Dropout(d))
    model.add(Conv1D(nodes, 3, strides = 2 , data_format="channels_first"))
    model.add(Conv1D(int(nodes/2), 2, strides = 1  ,data_format="channels_first"))
    model.add(Dropout(d))
    model.add(Flatten())
    model.add(Dense(64))
    model.add(Dropout(d))
    model.add(Dense(16))
    if binary == True:
        model.add(Dense(2 , name = "last" , activation = "softmax"))
        model.compile(optimizer="adam", loss="binary_crossentropy" , metrics=["accuracy"])
    else:
        model.add(Dense(1 , name = "last"))
        model.compile(optimizer="adam", loss="mse")

    return model

