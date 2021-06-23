library(ggmap)
library(ggplot2)
register_google(key='AIzaSyCRlNwnfgFhm6PvKdsNt33qlEUvR3YyTpo')
#-------------Read data-------------
data_2005 = read.csv("C:\\Users\\syjy0\\OneDrive\\바탕 화면\\데시 기말\\서울시 연평균기온 2005년 위치정보 (좌표계_ WGS1984).csv")
data_2006 = read.csv("C:\\Users\\syjy0\\OneDrive\\바탕 화면\\데시 기말\\서울시 연평균기온 2006년 위치정보 (좌표계_ WGS1984).csv")
data_2007 = read.csv("C:\\Users\\syjy0\\OneDrive\\바탕 화면\\데시 기말\\서울시 연평균기온 2007년 위치정보 (좌표계_ WGS1984).csv")
data_2008 = read.csv("C:\\Users\\syjy0\\OneDrive\\바탕 화면\\데시 기말\\서울시 연평균기온 2008년 위치정보 (좌표계_ WGS1984).csv")
#-------------1) 데이터 셋 만들기-------------
data_2005['고유번호'] = 2005
data_2006['고유번호'] = 2006
data_2007['고유번호'] = 2007
data_2008['고유번호'] = 2008

colnames(data_2005)=c('year','o.code','o.name','o.addr','t2005','long','lat')
colnames(data_2006)=c('year','o.code','o.name','o.addr','t2006','long','lat')
colnames(data_2007)=c('year','o.code','o.name','o.addr','t2007','long','lat')
colnames(data_2008)=c('year','o.code','o.name','o.addr','t2008','long','lat')

#seoul = merge(data_2005, data_2006, by = c('year','o.code','o.name','o.addr'))
seoul = cbind(data_2005,data_2006['t2006'])
seoul = cbind(seoul,data_2007['t2007'])
seoul = cbind(seoul,data_2008['t2008'])

seoul = seoul[,-1]
seoul = seoul[, c(1,2,3,5,6,4,7,8,9)]

View(seoul)

#-------------2) 관측소별 2005~2008 평균 기온-------------
seoul_temp = seoul[,'t2005'] + seoul[,'t2006'] + seoul[,'t2007'] + seoul[,'t2008']
seoul_temp = cbind(seoul['o.name'],seoul_temp)
colnames(seoul_temp) = c('o.name','temp')
seoul_temp['temp'] = seoul_temp['temp'] / 4
seoul_temp = seoul_temp[order(seoul_temp$o.name),]

View(seoul_temp)

#-------------3) 관측소별 2005~2008 평균 기온 막대그래프-------------
seoul_temp['temp'] = seoul_temp['temp']
print(c(1:13))
avg_bargraph = barplot(seoul_temp$temp, names=seoul_temp$o.name, col = rainbow(27))
text(x = avg_bargraph, y = 14-2.1,labels=paste(round(seoul_temp$temp, digits=2)))
title('서울지역 연평균 기온')

#-------------4) 평균 기온 높은 상위 3개, 하위 3개-------------
seoul_temp = seoul_temp[c(order(seoul_temp$temp)),]
top_3 = seoul_temp[c(25,26,27),]
top_3 = top_3[c(order(top_3$temp,decreasing = TRUE)),]
bottom_3 = seoul_temp[c(1,2,3),]

par(mfrow = c(1,2))
top_3_graph = barplot(top_3$temp, names = top_3$o.name)
text(x = top_3_graph, y = 14-1.3,labels = paste(round(top_3$temp,digits=3)))
title('Top 3')
bottom_3_graph = barplot(bottom_3$temp, names = bottom_3$o.name)
text(x = bottom_3_graph, y = 12-1.3,labels = paste(round(bottom_3$temp,digits=3)))
title('Bottom 3')

#-------------5) 4년간 서울지역 연평균 기온의 추이-------------
during_4 = seoul[,c(6,7,8,9)]
colnames(during_4) = c('2005','2006','2007','2008')
during_4 = colMeans(during_4)
temp_trend = barplot(during_4, col = rainbow(4))
text(x = temp_trend, y = 14-1.3,labels=paste(round(during_4, digits=4)))
title('연평균기온 변화')
during_4 = data.frame(during_4)
colnames(during_4)='temp'
x = as.numeric(rownames(during_4))
y = as.numeric(during_4[,1])
temp_line = plot(x,y, xlab='year',ylab='temp',type='l')
title('연평균기온 변화')

during_4 = seoul[,c(6,7,8,9)]
colnames(during_4) = c('2005','2006','2007','2008')
during_4 = colMeans(during_4)
during_4 = data.frame(during_4)
colnames(during_4)='temp'
during_4['year'] = c('2005','2006','2007','2008')
row.names(during_4) = c(1,2,3,4)
x = as.numeric(rownames(during_4))
y = as.numeric(during_4[,1])

#-------------6) 관측소별 위치 지도에 표시-------------
# criteria = seoul[,c(4,5)]
# criteria = colMeans(criteria)
# criteria = data.frame(criteria)
# View(criteria) # 평균, 위도 평균값 관측
# cent = c(126.98330,37.55102)
map_loc = ggmap(get_googlemap(center = 'seoul',zoom=11, maptype="roadmap", color ='bw'))
map_loc+geom_point(data=seoul, aes(x=long, y=lat,alpha=0.13, size=0.1, color=o.name))

#-------------7) 관측소별 평균기온 및 관측소명 지도에 표시-------------
seoul_temp_loc = seoul_temp
seoul_temp_loc['long'] = seoul[,4]
seoul_temp_loc['lat'] = seoul[,5]
seoul_temp_loc['temp'] = (seoul_temp_loc['temp']-11)^3
map_loc = ggmap(get_googlemap(center = 'seoul',zoom=11, maptype="roadmap", color ='bw'))
map_loc+geom_point(data=seoul_temp_loc, aes(x=long, y=lat,alpha=0.33, size=temp, color='red'))+
  geom_text(data = seoul_temp_loc, aes(x=long, y=lat,alpha=0.33, size=0.21), size = 4.9, hjust=1.3, fontface='bold'
            ,label=seoul_temp_loc$o.name,colour = 'blue')

