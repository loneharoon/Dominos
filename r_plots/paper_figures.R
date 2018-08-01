
# here I plot figure which I think work for the paper. 
#%%
#
rm(list=ls())
library(xts)
library(data.table)
library(ggplot2)
Sys.setenv(TZ='Asia/Kolkata')

dir = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/Dominos/"
store = "Dominos-25"
power_df = fread(paste0(dir,store,'/',"meter_makeline.csv"))
power_df_xts = xts(power_df$current,fasttime::fastPOSIXct(power_df$Datetime)-19800)
temp_df = fread(paste0(dir,store,'/',"temp_makeline.csv"))
temp_df_xts = xts(temp_df$temperature,fasttime::fastPOSIXct(temp_df$Datetime)-19800)
df_comb = cbind(power_df_xts,temp_df_xts)
df_comb$temperature = na.approx(df_comb$temperature)
df_comb = na.omit(df_comb)

sel_date = '2018-02-10 02:00/2018-02-10 23:00'
plot_data = df_comb[sel_date]
long_data = fortify(plot_data)

p <- ggplot(long_data,aes(Index,current)) + geom_line(aes(colour="Current"))
p <- p + geom_line(aes(y = temperature,colour="Temperature"))
p <- p + scale_y_continuous(sec.axis = sec_axis(~.*1, name = "Temperature (C)"))
p <- p + scale_colour_manual(values = c("blue", "red")) 
p <- p + labs(y = "Current (A)", x = "Day hour",colour = "")
p <- p + theme(legend.position = c(0.7,0.9),axis.text.x = element_text(color = "black")) + scale_x_datetime(breaks=scales::date_breaks("2 hour"),labels = scales::date_format("%H",tz="Asia/Kolkata"))
p <- p + theme(axis.text.y.left=element_text(colour = "blue"), axis.text.y.right=element_text(colour = "red"), axis.title.y.right=element_text(colour = "red"),axis.title.y.left = element_text(colour = "blue"))
p
savedirec = "/Volumes/MacintoshHD2/Users/haroonr/Dropbox/zenatix/pics/"
ggsave(paste0(savedirec,store,'-',as.Date(index(plot_data[1]),tz="Asia/Kolkata"),'.pdf'),height = 2,width = 4,units = c("in"))

