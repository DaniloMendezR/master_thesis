##################################
##Argimiro Arratia @2022 Computational Finance
## Handling Acuity sentiment datasets 
## 
##################################
## Set working directory to current script's location.
fileloc <- dirname(rstudioapi::getSourceEditorContext()$path)
setwd(fileloc)
rm(fileloc)

#load libraries
lib <- c('data.table', 'xts','zoo', 'doParallel',
         'timeSeries', 'quantmod', 'plyr', 'caret','stringr',
         'xtable','tidyverse','ggplot2','fBasics','readr' )
loading.lib <- lapply(lib, require, character.only = TRUE)

#----------------------------------------------#
## 1. Handling Sentiment data 
#----------------------------------------------#
##############sample Good North American market 2012-2021 data: 

dirdata<-"dataSent12_21Good/"

## Stocks classification (by capitalization)
## small cap: 300*e6 to 2*e9;  mid cap 2e9 to 10e9; big > 10e9 
mrktcap <- read.csv(paste(dirdata,"CompaniesrankedMarketCap.csv",sep=""))
colnames(mrktcap)[5] <- "priceUSD"
##Extract US companies only
USco <- dplyr::filter(mrktcap, country %in% "United States")

years <- c("2012","2013","2014","2015","2016","2017","2018","2019","2020","2021")

##Upload sentiment data for each class of stocks selected (US big, med, small cap)
sentdata <- read.csv(paste(dirdata,"USbig_Sent12_21.csv",sep=""))
## USmed_Sent12_21.csv    USsmall_Sent12_21.csv
stocks <- unique(sentdata$stock)

## The sentiment dataset is in long format, so we split them into familiar wide format
## this will align all stocks by date and those which has no data for given date will be fill with NA
##
#1. Grab sentiments
names(sentdata)
sentiment_type = names(sentdata)[3:8] 
#2. form datasets with all the sentiments
year="12_21"
for (i in sentiment_type) {
  #create datasets
  x <- data.frame(date = as.Date(sentdata$date),         
                  ticker = as.character(sentdata$stock),
                  i = sentdata[i])
  # #convert to wide
  x <- reshape(x, idvar = "date", timevar="ticker", direction = "wide")
  #convert to time series
  x <- as.xts(zoo(as.matrix(x[,-1]), as.Date(as.character(x[,1]))))
  #name the columns in dataset
  colnames(x) <- unique(sentdata$stock)
  #assign a name to the dataset
  assign(  paste(i,year, sep = ""),x )
}

##The following sentiment tables are created:
##RCV12_21  RVT12_21  positivePartscr12_21  negativePartscr12_21  
##splogscr12_21   linscr12_21
## splogscr = 1/2*log((1+pos)/(1+neg); linscr = 100* pos /(pos + neg)
# RVT= Relative Volume = Volume of news of Company / Volume of news of ALL (per day) 

DataSent <- RCV12_21
##2. Data cleaning+preprocessing (fill in NAs)
basicStats(DataSent)

##remove stocks in some year with very few data (e.g. ABBV in year 2012 seem sparse)

##Fill in missing values: 1. with next observation carried backward; then 
## 2: with last obs carried forwrd (to fill last rows in case there are NA and hence have no next obs) 
##must do this column by column. 
## TO DO: a more clever interpolation of missing values
for(i in 1:ncol(DataSent)){
  DataSent[,i] <- nafill(DataSent[,i],"nocb")
}
for(i in 1:ncol(DataSent)){
  DataSent[,i] <- nafill(DataSent[,i],"locf")
}


#----------------------------------------------#
## 2. Obtain price data 
#----------------------------------------------#
# set begin-end date and stock namelist
begin_date <- "2013-01-01"
end_date <- "2017-08-31"
period <- paste(begin_date,"/",end_date,sep="")
stock_namelist <- stocks ##use all stocks or a subset

# download data from YahooFinance (quantmod)
## this only retrives Adjusted Close prices
prices <- xts()
for (stock_index in 1:length(stock_namelist))
  prices <- cbind(prices, Ad(getSymbols(stock_namelist[stock_index], 
                                        from = begin_date, to = end_date, auto.assign = FALSE)))
colnames(prices) <- stock_namelist
tclass(prices) <- "Date"

# compute data matrix with log-returns
X <- diff(log(prices))[-1]
N <- ncol(X)  # number of stocks
T <- nrow(X)  # number of days

##We can take a look at the prices of the stocks
plot(prices/rep(prices[1, ], each = nrow(prices)), col =1:N , legend.loc = "topleft",
     main = "Normalized prices")

##Now obtain sample mean and sample covariance
mu <- colMeans(X)
Sigma <- cov(X)

##############################################
