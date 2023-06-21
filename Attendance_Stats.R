rm(list = ls())

library("ggplot2")

#read in all the data as a dataframe
raw_data <- read.csv("~/Projekte/Movie_Attendence_Prediction/Data/Raw_Data/CineAsta_Movie_Data_Raw.csv")
#convert the dates into date type
raw_data$Date <- as.Date(raw_data$Date, format = "%d.%m.%Y") 

#order the df by date
CineStats <- raw_data[order(raw_data$Date), ]

CineStats["Weekdays"] <- weekdays(CineStats$Date)
year(CineStats$Date)

#mean of visitors for every weekday
days <- c("Dienstag", "Mittwoch", "Donnerstag")
bar <- ggplot(data=CineStats, aes(x=Weekdays, y=Attendance)) +
  geom_boxplot() + 
  scale_x_discrete(limits = days)
bar

table(CineStats['Weekdays'])

plot(x = CineStats$Date, y = CineStats$Attendance, 
     xlab = "Zeit", ylab = "Besucherzahl", main = "SoSe 2023",
     type = "b", col = "darkblue")

points(x = CineStats$Date, y = CineStats$Attendance, pch = 16, col = "darkblue")
?plot


abline(h = median(CineStats$Attendance), col = "red", lwd = 2, lty  =2)
?axis

rm(list = ls())

?as.Date
