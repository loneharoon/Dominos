# in this I plot frequncy-plots for the paper. These show the frequency of faults

library(ggplot2)
# plot related to long compressor cycles
# the data is calucalated from ground truth file first and then arranged on a notebook
days = seq(1,8,1)
freq = c(19,5,4,3,1,0,2,1)
df_lf = data.frame(days,freq)
g <- ggplot(df_lf,aes(days,freq)) + geom_bar(stat='identity',fill='blue',width = 0.1)
g <- g + labs(x="Days",y="Frequency")   
g <- g + theme(axis.text =element_text(colour="black")) + scale_x_continuous(breaks=seq(1,8,1))
g
savedirec = "/Volumes/MacintoshHD2/Users/haroonr/Dropbox/zenatix/paper/pics/"
ggsave(paste0(savedirec,'long_cycle.pdf'),height = 2,width = 4,units = c("in"))


# plot related to long compressor shutdown case
days = seq(1,7,1)
freq = c(2,2,0,2,0,0,1)
df_lf = data.frame(days,freq)
h <- ggplot(df_lf,aes(days,freq)) + geom_bar(stat='identity',fill='blue',width = 0.1)
h <- h + labs(x="Days",y="Frequency")   
h <- h + theme(axis.text =element_text(colour="black")) + scale_x_continuous(breaks=seq(1,8,1))
h
savedirec = "/Volumes/MacintoshHD2/Users/haroonr/Dropbox/zenatix/paper/pics/"
ggsave(paste0(savedirec,'compressor_down.pdf'),height = 2,width = 4,units = c("in"))
