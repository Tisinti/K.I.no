rm(list = ls())

library("ggplot2")

#read in all the data as a dataframe
raw_data <- read.csv("~/Projekte/Movie_Attendence_Prediction/Uni_Data_Semesters/sommer_06.csv")
#convert the dates into date type
raw_data$Date <- as.Date(raw_data$Date, format = "%Y-%m-%d") 

#order the df by date
CineStats <- raw_data[order(raw_data$Date), ]

CineStats["Weekdays"] <- weekdays(CineStats$Date)

#full dataframe
CineStats

#mean of visitors for every weekday
days <- c("Dienstag", "Mittwoch", "Donnerstag")
boxpl <- ggplot(data=CineStats, aes(x=Weekdays, y=Attendance)) +
  geom_boxplot() + 
  scale_x_discrete(limits = days)
boxpl

table(CineStats['Weekdays'])

plot(x = CineStats$Date, y = CineStats$Attendance, 
     xlab = "Zeit", ylab = "Besucherzahl", main = "SoSe 2007",
     type = "b", col = "darkblue")

points(x = CineStats$Date, y = CineStats$Attendance, pch = 16, col = "darkblue")
?plot

abline(h = median(CineStats$Attendance), col = "green", lwd = 2, lty  =2)
abline(h = mean(CineStats$Attendance), col = "red", lwd = 2, lty  =2)
?axis

rm(list = ls())

?as.Date
