import pandas as pd
import numpy as np
import altair as alt

f = open("chest_pain.txt", encoding='utf-8')
lines = f.readlines()


for line in lines:
    print(line)


f.close()
print(lines[0])# CC
print(lines[1])# DD
print(lines[2])# PI list start
print("length of lines: ",len(lines))

# split strings into single list
mdic = {}
ls = []
for i in range(2,len(lines)-2):
    y1 = lines[i].split(": ")[0]
    y2 = lines[i].split(": ")[1].split("\n")[0].split(", ")
    for j in y2:
        y3 = j
        y4 = y1
        ls.append([y3,y4])
    # print("y1 = ", y1, type(y1))# dd
    # print("y2 = ", y2, type(y2))# pi list
    mdic.update({y1:y2})
    # print("----")
    
print(ls)

ls_1 = []
ls_2 = []
for z in ls:
    ls_1.append(z[0])
    ls_2.append(z[1])
    
mdic_1 = pd.DataFrame({
    'symptom': ls_1,
    "disease": ls_2
})

mdic_1.sort_values(by="symptom",inplace=True)
print(mdic_1)

# opt_ls = ["dyspnea", "sharp pain", "substernal pressure"]# replace to streamlit
import streamlit as st
st.title("DDDD (Data-Drive Differential Diagnosis)")
st.subheader(lines[0])

opt_ls = st.multiselect(label="Choose your present illness:", 
options = mdic_1.symptom.unique(),
default=[]
)



df = mdic_1
df = df.loc[df['symptom'].isin(opt_ls)]
print(df)

print("====")
# dfg = df.groupby('symptom')
# print(dfg["disease"].value_counts()[opt_ls[0]])
# print(dfg["disease"].value_counts()[opt_ls[0]].to_list())
print(df.shape[0]-1)
print(np.repeat(1,df.shape[0]))# 設定值
f_temp = np.repeat(1,df.shape[0]).tolist()

df['freq'] = f_temp
print(df)

df_long = df.copy()

df = df.pivot('symptom','disease','freq')
cl = df.columns
print(df)
# df = df.to_numpy()
df = df.T
df.fillna(0, inplace=True)# 缺失直

print(df)   

# apply

def cal_sum(x):
    return x.sum()

df['sum'] = df.apply(cal_sum,axis=1)
df = df.sort_values(by='sum',ascending=False)


print(df_long)
bar = alt.Chart(df_long).mark_bar().encode(
    x = 'freq',
    y = alt.Y('disease', sort='-x'),# y = alt.Y('disease', sort='-x'),
    color= alt.Color('symptom', scale=alt.Scale(scheme='Reds')),
    tooltip = ['symptom']

).interactive()

st.altair_chart(bar,use_container_width=True)


df
# print(df.pivot('symptom','disease'))


# print(dfg["disease"].value_counts())
# import streamlit as st
# streamlit 
# st.title("Idioctor")
# st.subheader(lines[0])
# options = st.multiselect(label="Choose your fucking present illnes:", options = mdic_1)
# st.write(options)
