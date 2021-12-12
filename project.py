import pandas as pd
import requests
import datetime
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
pd.options.display.float_format= '{:.3f}'.format
plt.rc('font',family='Malgun Gothic')#한글 깨짐 방지

KboRank = []
now = datetime.datetime.now()
nowyear = now.strftime('%Y')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#20년 간 결과 가져오기
for year in range(2002,2022):
    url='https://sports.news.naver.com/kbaseball/record/index?category=kbo&year='+str(year)
    req=requests.get(url,headers=headers)

    soup = BeautifulSoup(req.content, "html.parser")

    # select를 이용해서, tr들 불러오기
    baseball = soup.select('#regularTeamRecordList_table > tr')

    # tr들 반복문 돌리기
    for baseballteam in baseball:
        rank = baseballteam.select_one('th') #th태그의 값 가져오기     
        team = baseballteam.select_one('span') #span태그 사이의 값 가져오기
        rate = baseballteam.select_one('td > strong') #strong 태그 사이의 값 가져오기
        KboRank.append([year,rank.text,team.text,rate.text])
       
data = pd.DataFrame(KboRank)
data.columns=['Year','Rank','Team','Winning rate']
data.to_csv('KboRankingFor20years.csv', encoding='cp949')

#----------groupby 이용 통계----------
df = pd.read_csv('KboRankingFor20years.csv',encoding='cp949')
df['Team']= df['Team'].replace(['SK','넥센','kt','현대'],['SSG','키움','KT','현대(2008년 해체)'])#팀명이 중간에 바뀐 경우
winner = df[df.Rank==1]#연도 별 1위 팀만 추출
numOfWins = winner.groupby('Team')['Rank'].count()
print(numOfWins) #팀 별 1위 횟수
print(df.groupby('Team')['Winning rate'].mean()) #팀 별 20년 간 승률 평균

#----------그래프 그리기 1----------
#팀 별로 기록 따로 추출
HW = df[df['Team'].str.contains('한화')]
KIA = df[df['Team'].str.contains('KIA')]
KT = df[df['Team'].str.contains('KT')]
LG = df[df['Team'].str.contains('LG')]
NC = df[df['Team'].str.contains('NC')]
SSG = df[df['Team'].str.contains('SSG')]
DB =df[df['Team'].str.contains('두산')]
LT = df[df['Team'].str.contains('롯데')]
SS = df[df['Team'].str.contains('삼성')]
KW = df[df['Team'].str.contains('키움')]
HD = df[df['Team'].str.contains('현대')]

fig = plt.figure(figsize=(20,10))
fig.suptitle('Winning rate of each team for 20 years (현대 제외)', size=20)

ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax1)

ax1.set_title('Top 5 team with winning rate', size=15)
ax2.set_title('Bottom 5 team with winning rate',size=15)

ax1.set_xlabel('Year', size=10,loc='left')
ax2.set_xlabel('Year',size=10,loc='left')

ax1.set_ylabel('Winning rate',size=10)
ax2.set_ylabel('Winning rate',size=10)

plt.xticks(range(2002,2022))
ax1.plot(DB['Year'],DB['Winning rate'],label='두산',color='red',marker='o')
ax1.plot(SS['Year'],SS['Winning rate'],label='삼성',color='blueviolet',marker='o')
ax1.plot(NC['Year'],NC['Winning rate'],label='NC',color='darkorange',marker='o')
ax1.plot(SSG['Year'],SSG['Winning rate'],label='SSG',color='green',marker='o')
ax1.plot(KW['Year'],KW['Winning rate'],label='키움',color='blue', marker='o')

ax2.plot(KIA['Year'],KIA['Winning rate'],label='KIA',color='red',marker='o')
ax2.plot(LG['Year'],LG['Winning rate'],label='LG',color='blueviolet',marker='o')
ax2.plot(LT['Year'],LT['Winning rate'],label='롯데',color='darkorange',marker='o')
ax2.plot(KT['Year'],KT['Winning rate'],label='KT',color='green',marker='o')
ax2.plot(HW['Year'],HW['Winning rate'],label='한화',color='blue', marker='o')

ax1.legend()
ax2.legend()
plt.show()

#----------그래프 그리기 2----------
ind = numOfWins.index
labels = [str(i) for i in ind]

fig2 = plt.figure(figsize=(20,10))
ax3 = fig2.add_subplot(1,2,1)
ax4 = fig2.add_subplot(1,2,2)

fig2.suptitle('The winner from 2002 to 2021', size=20)
ax3.pie(numOfWins, labels=labels, autopct='%.1f%%', colors = ['#FDD370','#C9CE6A','#F37D71','#6AB2ED','#D3D3D3','#7B7A7C','pink'],
       counterclock=False, startangle=90)
ax4.bar(labels, numOfWins, color = ['#FDD370','#C9CE6A','#F37D71','#6AB2ED','#D3D3D3','#7B7A7C','pink'])
plt.show()