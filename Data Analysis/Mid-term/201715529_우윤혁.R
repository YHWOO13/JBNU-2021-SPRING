library(tidyr)
library(ggplot2)
library(plyr)
library(dplyr)
library(MASS)
library(treemap)
library(ggmap)
library(waffle)

# Read Data ---------------------------------------------------------------
setwd("C:\\Users\\syjy0\\OneDrive\\바탕 화면\\데이터 시각화 중간")
Base = read.csv("information.csv",quote="", sep="\t", stringsAsFactors = F, encoding='UTF-8')

# Change Col Name ---------------------------------------------------------------
colnames = c("식당ID","식당명","업종정보","테이크아웃여부","예약가능여부",
              "선결제여부","지번주소",
              "식당면적","식당위도","식당경도","어워드_글로벌","어워드_로컬",
              "트립어드바이저 인기도","씨트립 인기도","네이버 인기도","RTI 인덱스","온라인화 진행 여부",
              "다국어메뉴판 제공 여부","수용태세지수",
              "좌석수","좌석수(좌식)","베리어프리여부","반려동물출입가능여부"
              ,"주차가능여부","식당 홈페이지","등록일시","영업시간정보","휴식시간정보")
Base = separate(data = Base,col = X.U.FEFF.식당ID.식당명.업종.메뉴.정보.테이크아웃여부.예약가능여부.선결제여부.지번주소.식당면적.식당위도.식당경도.어워드_글로벌.어워드_로컬.트립어드바이저.인기도.씨트립.인기도.네이버.인기도.RTI.인덱스.온라인화.진행.여부.다국어메뉴판.제공.여부.수용태세.지수.좌석수.입식..좌석수.좌식..베리어프리여부.반려동물출입가능여부.주차가능여부.식당.홈페이지.등록일시.영업시간정보.휴식시간정보
,into =colnames,sep = ",")
Base = Base[-c(1800,1809,1844,2217,2552,2556,2717
               ,2719,2729,2764,2766,2770,2773,2959,2728),]

# Read Data ---------------------------------------------------------------
Base = separate(data = Base, col = 지번주소, into =c ("도","시","구","동","번"),sep = " ")
Base = separate(data = Base, col = 동, into =c ("동","가"),sep = "\\d")
Base = Base[,-c(11,12)]                

# 1. 덕진구 VS 완산구 ---------------------------------------------------------------
#숫자화
Base$구[Base$구=="완산구"]=1
Base$구[Base$구=="덕진구"]=2

#덕진구, 완산구 총 음식점 수
count_완산=Base[Base$구==1,]
nrow(count_완산)
count_덕진=Base[Base$구==2,]
nrow(count_덕진)

# 산점도 그래프
point = as.numeric(Base$구)
color = c("red","blue")
plot(Base$식당경도,Base$식당위도,xlab="식당경도",ylab="식당위도",data=Base,xlim=c(127.058,127.17),ylim=c(35.76,35.88),main = "Scatter Plot: 덕진구 vs. 완산구",pch=c(point),col=color[point])
legend("bottomleft",c("덕진구","완산구"),col=c("blue","red"),pch=c(2,1),box.lty=0,cex=0.5)
View(Base)

Base$식당위도 = as.numeric(Base$식당위도)
Base$식당경도 = as.numeric(Base$식당경도)
cent=c(127.122,35.828)

register_google(key='AIzaSyCRlNwnfgFhm6PvKdsNt33qlEUvR3YyTpo')
map_구 = ggmap(get_googlemap(center = cent,zoom=12, maptype="roadmap"))
map_구+geom_point(data=Base, aes(x=식당경도, y=식당위도,alpha=0.13, size=0.1, color=구))

map_동 = ggmap(get_googlemap(center = cent,zoom=12, maptype="roadmap"))
map_동+geom_point(data=Base, aes(x=식당경도, y=식당위도,alpha=0.13, size=0.1, color=동))

# 2. 인기있는 음식점 ---------------------------------------------------------------
WANSANFOOD = Base[Base$구==1,]
DEOKJINFOOD = Base[Base$구==2,]

#완산에서 가장 인기있는 음식점
WF=table(WANSANFOOD$업종정보)
print(WF)
count(WF)
WF=data.frame(WF)
colnames(WF)=c("업종","개수")
WF$Freq=as.numeric(WF$개수)
WF=WF[WF$개수>=40,]
print(WF)

ggplot(WF,aes(x=업종,y=개수))+
geom_bar(stat="identity")+
ggtitle("완산구 음식점")

#덕진에서 가장 인기있는 음식점
DF = table(DEOKJINFOOD$업종정보)
DF=data.frame(DF)
count(DF)
colnames(DF)=c("업종","개수")
DF$Freq=as.numeric(DF$개수)
DF=DF[DF$개수>=30,]
print(DF)

ggplot(DF,aes(x=업종,y=개수))+
geom_bar(stat="identity")+
ggtitle("덕진구 음식점")

# 3. 좌석수(가게크기)가 인기도와 관련이 있을까?  ---------------------------------------------------------------
Base$`네이버 인기도`= as.numeric(Base$`네이버 인기도`)
radius=sqrt(Base$`네이버 인기도`)
symbols(Base$식당면적, Base$좌석수,circles=radius,inches=0.3,bg="lightgray", xlab="식당면적",ylab="좌석수",main="식당크기&좌석수, 인기도의 상관관계")

# 4. 월별 등록된 가게---------------------------------------------------------------
Base = separate(data = Base, col = 등록일시, into =c ("년","월","일_시간"),sep = "-")
Base = unite(data=Base, col="년_월",년,월,sep="_")

Year_Month = table(Base$년_월)
Year_Month = data.frame(Year_Month)
Year_Month = Year_Month[-c(1,6),]
Year_Month = data.frame(Year_Month)
colnames(Year_Month) = c("년_월","개수")
Year_Month$상대도수 = round(Year_Month$개수/(252+1997+697+54),3)
print(Year_Month)

pie(Year_Month$개수,labels=paste(Year_Month$년_월,"  (",round(Year_Month$상대도수*100,5),")%"), main="월별 등록된 음식점 퍼센트")

w= c("2020_10" =252,"2020_11" =1997,
     "2020_12" =697,"2021_01" =54)
waffle(w,rows=50)

# 5. 어느 시간이 음식점이 제일 많이 쉴까?---------------------------------------------------------------
rest_time = Base
rest_time=rest_time[!(is.na(rest_time$휴식시간정보) | rest_time$휴식시간정보==""), ]
View(rest_time)

total_rest = table(rest_time$휴식시간정보)
total_rest=data.frame(total_rest)
colnames(total_rest) = c("휴식시간","수")
total_rest=total_rest[total_rest$수>=11,]
View(total_rest)

Time = read.csv("Time.csv",header=T, encoding='UTF-8')
colnames(Time) = c("t","var","val")
View(Time)
ggplot(Time,aes(x=t, y= val, group=var, fill=var))+geom_area()

# 6. 이 데이터에 가장 적합한 그래프---------------------------------------------------------------
Total=table(Base$업종정보)
Total=data.frame(Total)
Total2=table(Base$동)
#View(Total)
View(Total2) #각 동에 분포한 음식점 개수

Base$식당면적=as.numeric(Base$식당면적)
Base$좌석수=as.numeric(Base$좌석수)

treemap(Base,index=c("동","업종정보"),
        vSize="식당면적",
        type="value",bg.labels="gray", title="동, vSize:식당면적, vColor: 업종정보")


treemap(Base,index=c("구","업종정보"),
        vSize="식당면적", vColor="좌석수",
        type="value",bg.labels="gray",
        title="구, vSize:식당면적, vColor: 업종정보")

treemap(Base,index=c("동","업종정보"),
        vSize="식당면적", vColor="좌석수",
        type="value",bg.labels="gray")

treemap(Base,index=c("업종정보","테이크아웃여부"),
        vSize="네이버 인기도",
        type="value",bg.labels="gray",
        title="vSize:네이버 인기도, vColor: 테이크아웃 여부")

Base$수용태세지수 = as.numeric(Base$수용태세지수)
treemap(Base,index=c("업종정보","테이크아웃여부"),
        vSize="수용태세지수",
        type="value",bg.labels="gray",
        title="vSize:네이버 인기도, vColor: 테이크아웃 여부")


treemap(Base,index=c("구","동"),
        vSize="식당면적",
        type="value",bg.labels="gray", title="구,동, vSize:식당면적")
