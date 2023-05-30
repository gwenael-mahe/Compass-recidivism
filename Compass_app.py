import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("src/compas-scores-raw.csv")

st.set_option('deprecation.showPyplotGlobalUse', False)

df['Ethnic_Code_Text'] = df['Ethnic_Code_Text'].replace('African-Am', 'African-American')

st.subheader("Bar Chart: Counts by Ethnicity and Score Text")
text_by_race = df.groupby(['Ethnic_Code_Text', 'ScoreText'], sort=True)['Person_ID'].size()
text_by_race.unstack().plot.bar(stacked=False)
st.pyplot()

st.subheader("Table: Counts and Percentages by Ethnicity and Score Text")
text_by_race = df.groupby(['Ethnic_Code_Text', 'ScoreText'], sort=True).size().reset_index()
text_by_race = text_by_race.rename(columns={0:'count'})
text_by_race[['count']] = text_by_race[['count']].apply(pd.to_numeric)
gb = df.groupby(['Ethnic_Code_Text']).size().reset_index()
gb_d = gb.set_index('Ethnic_Code_Text').to_dict().get(0)
text_by_race['count_percentage'] = text_by_race.apply(lambda x: ((int(x['count'])/int(gb_d.get(x['Ethnic_Code_Text']))) * 100), axis=1)
st.dataframe(text_by_race)

st.subheader("Bar Chart: Recidivism Rates by Ethnicity, Score Text, and Supervision Level")
recid_by_race = df.groupby(['Ethnic_Code_Text', 'ScoreText', 'RecSupervisionLevelText'], sort=True).size().reset_index()
recid_by_race = recid_by_race.rename(columns={0:'count'})
r_sum = df.groupby(['Ethnic_Code_Text', 'ScoreText']).size().reset_index()
r_sum = r_sum.rename(columns={0:'count'})
r_sum['index'] = r_sum.apply(lambda x: x['Ethnic_Code_Text'] + '-' + x['ScoreText'], axis=1)
r_sum = r_sum.drop(['Ethnic_Code_Text', 'ScoreText'], axis=1)
r_sum_dict = r_sum.set_index('index').to_dict().get('count')
recid_by_race['count_percentage'] = recid_by_race.apply(lambda x: ((int(x['count'])/int(r_sum_dict.get(x['Ethnic_Code_Text'] + '-' + x['ScoreText']))) * 100), axis=1)
pt = recid_by_race.pivot_table('count_percentage', ['Ethnic_Code_Text', 'ScoreText'], 'RecSupervisionLevelText')
pt.plot.bar()
st.pyplot()

st.subheader("Counts by Score Text and Supervision Level")
counts = df.groupby(['ScoreText','RecSupervisionLevelText'])['Person_ID'].count()
st.dataframe(counts)

st.subheader("Bar Chart: Mean Decile Score by Ethnicity")
decile_by_race = df.groupby(['Ethnic_Code_Text'], sort=True)['DecileScore'].mean()
decile_by_race.plot(kind='bar')
st.pyplot()

st.subheader("Bar Chart: Mean Prior Count by Ethnicity")
priors = df.groupby(['Ethnic_Code_Text'], sort=True)['RecSupervisionLevel'].mean()
my_colors = [(x/10.0, x/20.0, 0.75) for x in range(9)]
priors.plot(kind='bar', title='Mean Prior Count By Race', ylim=(0,6), color=my_colors)
st.pyplot()
