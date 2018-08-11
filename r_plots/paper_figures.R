
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
colnames(df_comb) = c('current','temperature')
df_comb$temperature = na.approx(df_comb$temperature,na.rm = FALSE)
df_comb = na.omit(df_comb)

sel_date = '2018-04-15 02:00/2018-04-15 23:00'
plot_data = df_comb[sel_date]
long_data = fortify(plot_data)

p <- ggplot(long_data,aes(Index,current)) + geom_line(aes(colour="Current"))
p <- p + geom_line(aes(y = temperature,colour="Temperature"))
p <- p + scale_y_continuous(sec.axis = sec_axis(~.*1, name = "Temperature (C)"))
p <- p + scale_colour_manual(values = c("blue", "red")) 
p <- p + labs(y = "Current (A)", x = "Day hour",colour = "")
p <- p + theme(legend.position = c(0.56,0.9),axis.text.x = element_text(color = "black")) + scale_x_datetime(breaks=scales::date_breaks("2 hour"),labels = scales::date_format("%H",tz="Asia/Kolkata"))
p <- p + theme(axis.text.y.left=element_text(colour = "blue"), axis.text.y.right=element_text(colour = "red"), axis.title.y.right=element_text(colour = "red"),axis.title.y.left = element_text(colour = "blue"))
p
savedirec = "/Volumes/MacintoshHD2/Users/haroonr/Dropbox/zenatix/pics/"
ggsave(paste0(savedirec,store,'-',as.Date(index(plot_data[1]),tz="Asia/Kolkata"),'.pdf'),height = 2,width = 4,units = c("in"))

####################################
####################################  special treatement for store 95 anomalies. Some sprous readings are cleaned before plottting
store95 { 
  dir = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/Dominos/"
  store = "Dominos-95"
  power_df = fread(paste0(dir,store,'/',"meter_makeline.csv"))
  power_df_xts = xts(power_df$current,fasttime::fastPOSIXct(power_df$Datetime)-19800)
  temp_df = fread(paste0(dir,store,'/',"temp_makeline.csv"))
  temp_df_xts = xts(temp_df$temperature,fasttime::fastPOSIXct(temp_df$Datetime)-19800)
  df_comb = cbind(power_df_xts,temp_df_xts)
  colnames(df_comb) = c('current','temperature')
  df_comb$temperature = na.approx(df_comb$temperature,na.rm = FALSE)
  df_comb = na.omit(df_comb)
  
  sel_date = '2018-04-16 02:00/2018-04-16 23:00'
  plot_data = df_comb[sel_date]
  plot_data$temperature[plot_data$temperature > 30] = NA
  plot_data$temperature = na.approx(plot_data$temperature,na.rm = FALSE)
  
long_data = fortify(plot_data)
p <- ggplot(long_data,aes(Index,current)) + geom_line(aes(colour="Current"))
p <- p + geom_line(aes(y = temperature,colour="Temperature"))
p <- p + scale_y_continuous(sec.axis = sec_axis(~.*1, name = "Temperature (C)"))
p <- p + scale_colour_manual(values = c("blue", "red")) 
p <- p + labs(y = "Current (A)", x = "Day hour",colour = "")
p <- p + theme(legend.position = c(0.8,0.9),axis.text.x = element_text(color = "black")) + scale_x_datetime(breaks=scales::date_breaks("2 hour"),labels = scales::date_format("%H",tz="Asia/Kolkata"))
p <- p + theme(axis.text.y.left=element_text(colour = "blue"), axis.text.y.right=element_text(colour = "red"), axis.title.y.right=element_text(colour = "red"),axis.title.y.left = element_text(colour = "blue"))
p
savedirec = "/Volumes/MacintoshHD2/Users/haroonr/Dropbox/zenatix/pics/"
ggsave(paste0(savedirec,store,'-',as.Date(index(plot_data[1]),tz="Asia/Kolkata"),'.pdf'),height = 2,width = 4,units = c("in"))
}
only_Makeline_current_consumption_signatures{
  # THIS SHOWS NORMAL CONSUMPTION OF ONE OF THE STORES/
  dir = "/Volumes/MacintoshHD2/Users/haroonr/Detailed_datasets/Dominos/"
  store = "Dominos-25"
  power_df = fread(paste0(dir,store,'/',"meter_makeline.csv"))
  power_df_xts = xts(power_df$current,fasttime::fastPOSIXct(power_df$Datetime)-19800)
  sel_date = '2018-04-15 12:00/2018-04-15 16:00'
  plot_data = power_df_xts[sel_date]
  long_data = fortify(plot_data)
  colnames(long_data) = c('Index','current')
  p <- ggplot(long_data,aes(Index,current)) + geom_line(color='blue')
  p <- p + labs(y = "Current (A)", x = "Day hour")
  p <- p + theme(axis.text = element_text(color = "black"))
  p
  savedirec = "/Volumes/MacintoshHD2/Users/haroonr/Dropbox/zenatix/paper/pics/"
  ggsave(paste0(savedirec,'cycle_pattern.pdf'),height = 2,width = 4,units = c("in"))
  
  # Lets plot now only current consumption of other stores too
  
  store = "Dominos-25"
  power_df = fread(paste0(dir,store,'/',"meter_makeline.csv"))
  power_df_xts = xts(power_df$current,fasttime::fastPOSIXct(power_df$Datetime)-19800)
  sel_date = '2018-04-15 12:00/2018-04-15 16:00'
  plot_data = power_df_xts[sel_date]
  long_data = fortify(plot_data)
  colnames(long_data) = c('Index','current')
  p <- ggplot(long_data,aes(Index,current)) + geom_line(color='blue')
  p <- p + labs(y = "Current (A)", x = "Day hour")
  p <- p + theme(axis.text = element_text(color = "black"))
  p
  savedirec = "/Volumes/MacintoshHD2/Users/haroonr/Dropbox/zenatix/paper/pics/"
  ggsave(paste0(savedirec,'cycle_pattern.pdf'),height = 2,width = 4,units = c("in"))
  
  
  store = "Dominos-22"
  power_df = fread(paste0(dir,store,'/',"meter_makeline.csv"))
  power_df_xts = xts(power_df$current,fasttime::fastPOSIXct(power_df$Datetime)-19800)
  sel_date = '2018-06-27 02:00/2018-06-27 23:00'
  plot_data = power_df_xts[sel_date]
  long_data = fortify(plot_data)
  colnames(long_data) = c('Index','current')
  p <- ggplot(long_data,aes(Index,current)) + geom_line(color='blue')
  p <- p + labs(y = "Current (A)", x = "Day hour")
  p <- p + theme(axis.text = element_text(color = "black")) + scale_x_datetime(breaks=scales::date_breaks("2 hour"),labels = scales::date_format("%H",tz="Asia/Kolkata"))
  p
  savedirec = "/Volumes/MacintoshHD2/Users/haroonr/Dropbox/zenatix/paper/pics/"
  ggsave(paste0(savedirec,'current-22.pdf'),height = 2,width = 4,units = c("in"))
  
  store = "Dominos-95"
  power_df = fread(paste0(dir,store,'/',"meter_makeline.csv"))
  power_df_xts = xts(power_df$current,fasttime::fastPOSIXct(power_df$Datetime)-19800)
  sel_date = '2018-02-16 02:00/2018-02-16 23:00'
  plot_data = power_df_xts[sel_date]
  long_data = fortify(plot_data)
  colnames(long_data) = c('Index','current')
  p <- ggplot(long_data,aes(Index,current)) + geom_line(color='blue')
  p <- p + labs(y = "Current (A)", x = "Day hour")
  p <- p + theme(axis.text = element_text(color = "black")) + scale_x_datetime(breaks=scales::date_breaks("2 hour"),labels = scales::date_format("%H",tz="Asia/Kolkata"))
  p
  savedirec = "/Volumes/MacintoshHD2/Users/haroonr/Dropbox/zenatix/paper/pics/"
  ggsave(paste0(savedirec,'current-95.pdf'),height = 2,width = 4,units = c("in"))
  
  store = "Dominos-187"
  power_df = fread(paste0(dir,store,'/',"meter_makeline.csv"))
  power_df_xts = xts(power_df$current,fasttime::fastPOSIXct(power_df$Datetime)-19800)
  sel_date = '2018-05-22 02:00/2018-05-22 23:00'
  plot_data = power_df_xts[sel_date]
  long_data = fortify(plot_data)
  colnames(long_data) = c('Index','current')
  p <- ggplot(long_data,aes(Index,current)) + geom_line(color='blue')
  p <- p + labs(y = "Current (A)", x = "Day hour")
  p <- p + theme(axis.text = element_text(color = "black")) + scale_x_datetime(breaks=scales::date_breaks("2 hour"),labels = scales::date_format("%H",tz="Asia/Kolkata"))
  p
  savedirec = "/Volumes/MacintoshHD2/Users/haroonr/Dropbox/zenatix/paper/pics/"
  ggsave(paste0(savedirec,'current-187.pdf'),height = 2,width = 4,units = c("in"))
  
  
}
