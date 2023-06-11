
CineStats <- read.csv("/home/tisinti/Projekte/Movie_Attendence_Prediction/Testing/Test_data.csv")

CineStats$Date <- as.Date(CineStats$Date, format = "%d.%m.%Y") #String zu Datum konvertieren

plot(x = CineStats$Date, y = CineStats$Attendance, 
     xlab = "Zeit", ylab = "Besucherzahl", main = "SoSe 2023",
     type = "b", col = "darkblue")

points(x = CineStats$Date, y = CineStats$Attendance, pch = 16, col = "darkblue")
?plot


abline(h = mean(CineStats$Attendance), col = "red", lwd = 2, lty  =2)#
?axis

rm(list = ls())

?as.Date
