# Stocks-Data-Loader-Flask
Screenshot:
![Image 2](https://github.com/ano-ny-mous/Stocks-Data-Loader-Flask/assets/91519560/cdb4a2c0-04cf-4b36-8886-33365a7cab54)

Add/Remove company tickers in config.txt file  
Ticker : a unique combination of letters and numbers that represent a particular stock or security listed on an exchange.  
All stocks data is downloaded into finance_data.db  
  
Can use postman to test api calls  
Default port:5000  
Get all stock data for a particular company  
http://127.0.0.1:5000/stocks_of/IBM  
Using get method  

Get all stock data for a particular company for a particular day  
http://127.0.0.1:5000/stocks_of_on/IBM/1962-01-02  
Using get method  

Get all companies’ stock data for a particular day  
http://127.0.0.1:5000/stocks_on/1962-01-02  
Using get method  

Update stock data for a company by date  
http://127.0.0.1:5000/stocks_update/IBM/1962-01-02  
Send variables values from body using post method  
