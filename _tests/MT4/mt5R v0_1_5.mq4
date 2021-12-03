/* *******************************************************************************

mt5R Expert Advisor

Version: 
   
   0.1.5 (MAR-21)

Features:

   * More than 30 functions fully functional integrated with mt5R (R package).

NOTES
----------------------------------

   The mt5R code is mixed with the socket library. 
   
   To maintain the reading of some blocks of codes, the use of MT4 functions was preferred.
   
   It is still under work to remove any mention of portuguese in the name of variables and comments.
   
Oficial site:

   https://kinzel.github.io/mt5R/
   
Credits:

   JC  https://www.mql5.com/en/blogs/post/706665

Author:

   GKin https://www.mql5.com/en/users/kinzel

******************************************************************************* */

#property copyright "Guilherme Kinzel"
#property link      "https://www.mql5.com"
#property version   "0.1.5"
#property strict

#define SOCKET_LIBRARY_USE_EVENTS
#include <socket-library-mt4-mt5.mqh>
#include <Trade\Trade.mqh>

// --------------------------------------------------------------------
// Global variables and constants
// --------------------------------------------------------------------

// Users variables
input ushort ServerPort = 23456;  // Server port
input bool   bRemoveSymbolsAfterUse = false; //Remove afterward symbols added into Marketwatch
//input string SUB_REQUEST_DIVISOR = "?"; //Character used to subdivide requests
//input string REQUEST_DIVISOR = "@"; //Character used to divide entire requests (advanced)

// Frequency for EventSetMillisecondTimer(). Doesn't need to 
// be very frequent, because it is just a back-up for the 
// event-driven handling in OnChartEvent()
#define TIMER_FREQUENCY_MS    1000 //1000

// Server socket
ServerSocket * glbServerSocket = NULL;

// Array of current clients
ClientSocket * glbClients[];

// Watch for need to create timer;
bool glbCreatedTimer = false;

// Characters used in R functions
const string SUB_REQUEST_DIVISOR = "?";
const string REQUEST_DIVISOR = "@";

// Version
const string sVersion = "0.1.5";
const string sDateVersion = "MAR-2021";

/************************************************/
bool SymbolExists(string symbol)
/************************************************/
{
   if(SymbolInfoInteger(symbol, SYMBOL_TIME) <= 0) return false;
   return true;
}

/************************************************/
int TimeYearMQL4(datetime date)
/************************************************/
{
   MqlDateTime tm;
   TimeToStruct(date,tm);
   return(tm.year);
}

/************************************************/
int TimeMonthMQL4(datetime date)
/************************************************/
{
   MqlDateTime tm;
   TimeToStruct(date,tm);
   return(tm.mon);
}

/************************************************/
int TimeDayMQL4(datetime date)
/************************************************/
{
   MqlDateTime tm;
   TimeToStruct(date,tm);
   return(tm.day);
}

/************************************************/
int TimeHourMQL4(datetime date)
/************************************************/
{
   MqlDateTime tm;
   TimeToStruct(date,tm);
   return(tm.hour);
}

/************************************************/
int TimeMinuteMQL4(datetime date)
/************************************************/
{
   MqlDateTime tm;
   TimeToStruct(date,tm);
   return(tm.min);
}

/************************************************/
int TimeSecondsMQL4(datetime date)
/************************************************/
{
   MqlDateTime tm;
   TimeToStruct(date,tm);
   return(tm.sec);
}

/************************************************/
int Write(string sText, string sFile)
/************************************************/
{

   string Filename = sFile;
   int Handle = FileOpen(Filename, FILE_READ|FILE_WRITE|FILE_ANSI, "/t");
   
   if (Handle < 1)
   {
      Print("Error to open file: ", GetLastError());
      FileClose(Handle);
      return 0;
   }
   else if (!FileSeek(Handle, 0, SEEK_END))
   {
      Print("Error in organize file: ", GetLastError());
      FileClose(Handle);
      return 0;
   }
   else if (FileWrite(Handle, sText) < 1)
   {
      Print("Error in write file: ", GetLastError());
      FileClose(Handle);
      return 0;
   }

   FileClose(Handle);
   return 1;
}

/***********************************************/
void StructureOrders(string sRequest, string &sResult[], int &iQtyOrders, string sep)
/***********************************************/
{
   ushort u_sep;
   string result[];
   //--- Get the separator code 
   u_sep = StringGetCharacter(sep,0); 
   //--- Split the string to substrings 
   int k = StringSplit(sRequest,u_sep,result); 
   //--- Show a comment  
   //PrintFormat("sOrder: '%s'", sOrder);
   //PrintFormat("Strings obtained: %d. Used separator '%s' with the code %d",k,sep,u_sep); 
   
   // Return values
   ArrayCopy(sResult, result);
   iQtyOrders = k;
}

/***********************************************/
bool DownloadSymbol_csv (string sSymbol, string LabelArquivos, ENUM_TIMEFRAMES eWhichTF, int iBarsDownload)
/***********************************************/
{
      int k;
      string sFileName, sText;
      
      int iYear, iMonth, iDay, iHour, iMin; //iSeg;
      double fOpen, fHigh, fLow, fClose;
      long lVolume;
      iBarsDownload--;
      int iDigitosSymbol = SymbolInfoInteger(sSymbol, SYMBOL_DIGITS);
      
      //ENUM_TIMEFRAMES eWhichTF = CategorizeTimeFrames(iTF); 
      
      if(SymbolExists(sSymbol) == false)
      {
         Print("Symbol not recognized: "+sSymbol);
      }
      else 
      {
         sFileName = sSymbol + "_"+LabelArquivos+"_TABLE.csv";
         if(FileIsExist(sFileName))
         {
            FileDelete(sFileName);
         }
         
         Write(0,"PegandoDados.txt");
         
         Print("Downloading: "+sSymbol+" Bars: "+IntegerToString(iBarsDownload + 1)+" File: "+sFileName);
         for (k=iBarsDownload;k>=0;k--)
         {
            fOpen = iOpen(sSymbol,eWhichTF,k);
            fHigh = iHigh(sSymbol,eWhichTF,k);
            fLow = iLow(sSymbol,eWhichTF,k);
            fClose = iClose(sSymbol,eWhichTF,k);
               
            iDay = TimeDayMQL4(iTime(sSymbol,eWhichTF,k));
            iMonth = TimeMonthMQL4(iTime(sSymbol,eWhichTF,k));
            iHour = TimeHourMQL4(iTime(sSymbol,eWhichTF,k));
            iMin = TimeMinuteMQL4(iTime(sSymbol,eWhichTF,k));
            //iSeg = TimeSeconds(iTime(sSymbol,eWhichTF,k));
            iYear = TimeYearMQL4(iTime(sSymbol,eWhichTF,k));
            lVolume = iVolume(sSymbol,eWhichTF,k);   
            
            if(iYear == 1970)
            {
               continue; //Year that MT5 says: "there is no data, sorry!"
            }

            sText = IntegerToString(iYear)+";"+IntegerToString(iMonth)+";"+IntegerToString(iDay)+";"+IntegerToString(iHour)+";"+IntegerToString(iMin)+
                    ";"+DoubleToString(fOpen,iDigitosSymbol)+";"+DoubleToString(fHigh,iDigitosSymbol)+";"+DoubleToString(fLow,iDigitosSymbol)+";"+
                    DoubleToString(fClose,iDigitosSymbol)+";"+IntegerToString(lVolume);
            
            //printf(sText);
            Write(sText, sFileName);
         }
         FileDelete("PegandoDados.txt");
      }

   
   return true;
}

/***********************************************/
bool DownloadSymbol_socket (string sSymbol, ENUM_TIMEFRAMES eWhichTF, int iBarsDownload, string &sTextComplete)
/***********************************************/
{
      int k;
      string sText;
      
      int iYear, iMonth, iDay, iHour, iMin;
      double fOpen, fHigh, fLow, fClose, lVolume;
      
      iBarsDownload--;
      
      //ENUM_TIMEFRAMES eWhichTF = CategorizeTimeFrames(iTF); 
      
      int iDigitosSymbol = SymbolInfoInteger(sSymbol, SYMBOL_DIGITS);
      
      //if(SymbolExists(sSymbol) == false)
      //{
      //   Print("Symbol not recognized: "+sSymbol);
      //   return(false);
      //}
      //else 
      //{
         bool bAlreadyStarted = false;
         Print("Downloading: "+sSymbol+" Bars: "+IntegerToString(iBarsDownload + 1));
         for (k=iBarsDownload;k>=0;k--)
         {
            fOpen = iOpen(sSymbol,eWhichTF,k);
            fHigh = iHigh(sSymbol,eWhichTF,k);
            fLow = iLow(sSymbol,eWhichTF,k);
            fClose = iClose(sSymbol,eWhichTF,k);
               
            iDay = TimeDayMQL4(iTime(sSymbol,eWhichTF,k));
            iMonth = TimeMonthMQL4(iTime(sSymbol,eWhichTF,k));
            iHour = TimeHourMQL4(iTime(sSymbol,eWhichTF,k));
            iMin = TimeMinuteMQL4(iTime(sSymbol,eWhichTF,k));
            //iSeg = TimeSeconds(iTime(sSymbol,eWhichTF,k));
            iYear = TimeYearMQL4(iTime(sSymbol,eWhichTF,k));
            lVolume = iVolume(sSymbol,eWhichTF,k);   
            
            if(iYear == 1970)
            {
               continue; //Year that MT5 says: "there is no data, sorry!"
            }

            sText = IntegerToString(iYear)+" "+IntegerToString(iMonth)+" "+IntegerToString(iDay)+" "+IntegerToString(iHour)+" "+IntegerToString(iMin)+
                    " "+DoubleToString(fOpen,iDigitosSymbol)+" "+DoubleToString(fHigh,iDigitosSymbol)+" "+DoubleToString(fLow,iDigitosSymbol)+" "+
                    DoubleToString(fClose,iDigitosSymbol)+" "+IntegerToString(lVolume);

            if(!bAlreadyStarted)
            {
               sTextComplete = sText; //Start
               bAlreadyStarted = true;
            }else sTextComplete = sTextComplete + SUB_REQUEST_DIVISOR + sText;
            
         }
      //}

   return true;
}

/************************************************/
string Access_Book (string sSymbol, string sDivisorString, int iBidAsk, int iDeepLevel, string sErrorMsg)
/************************************************/
{
   //This function deserves a further update

   bool bThereAreBuyers = false;
   bool bThereAreSellers = false;

   MarketBookAdd(sSymbol);
   Sleep(100); //Needed 

   MqlBookInfo priceArray[]; 
   bool getBook = MarketBookGet(sSymbol,priceArray); 
   double fPrice;
   long lLot;
   int iStartBid = 0, i;
   
   //Print(iBidAsk);
   //Print(iDeepLevel);
   
   string sText = "";
   
   ENUM_BOOK_TYPE OrderType;
   if(getBook) 
   { 
      int size = ArraySize(priceArray); 
      Print("MarketBookInfo for ", Symbol(), " size: ", size); 
      for(i=0;i<size;i++) 
      { 
         OrderType = priceArray[i].type;
         
         if(OrderType == 1 || OrderType == 3)
         {
            bThereAreSellers = true;
         }else if((OrderType == 2 || OrderType == 4) && i>0)
         {
            bThereAreBuyers = true;
            iStartBid = i;
            break;
         }
      } 
      if(!bThereAreBuyers && !bThereAreSellers)
      {
         return(sErrorMsg);
      }else if(iStartBid == 0)
      {
         return(sErrorMsg);
      }
      Print(iStartBid);
      if(iBidAsk == 0)
      {
         // I want BID
         for(i=0; i<iDeepLevel; i++)
         {
            if(iStartBid+i > size - 1)
            {
               break;
            }
            fPrice = priceArray[iStartBid+i].price;
            lLot = priceArray[iStartBid+i].volume;
            sText = sText + DoubleToString(fPrice) + sDivisorString + IntegerToString(lLot) + sDivisorString;
         }
      }else if(iBidAsk == 1)
      {
         //I want ASK
         for(i=0; i<iDeepLevel; i++)
         {
            if(iStartBid-i-1<0)
            {
               break;
            }
            fPrice = priceArray[iStartBid-i-1].price;
            lLot = priceArray[iStartBid-i-1].volume;
            sText = sText + DoubleToString(fPrice) + sDivisorString + IntegerToString(lLot) + sDivisorString;
         }
      }else
      {
         Print("! Error: not specified. Do you want bid or ask?");
         return(sErrorMsg);
      }
      
      return(sText);
   } 
  else 
  { 
      printf(sSymbol+": Failed load market book price. Reason: " + (string)GetLastError());
  }

  return("O4ERROR");
}

/************************************************/
ENUM_TIMEFRAMES CategorizeTimeFrames(int iMin)
/************************************************/
{
   ENUM_TIMEFRAMES resp = _Period;
   switch(iMin)
   {
      case 1: resp = PERIOD_M1; break;
      case 2: resp = PERIOD_M2; break;
      case 5: resp = PERIOD_M5; break;
      case 15: resp = PERIOD_M15; break;
      case 30: resp = PERIOD_M30; break;
      case 60: resp = PERIOD_H1; break;
      case 120: resp = PERIOD_H2; break;
      case 240: resp = PERIOD_H4; break;
      case 480: resp = PERIOD_H8; break;
      case 1440: resp = PERIOD_D1; break;
      case 7200: resp = PERIOD_W1; break;
      case 216000: resp = PERIOD_MN1; break;
      default: resp = -1; break;
   }
   
   return(resp);
}

/***********************************************/
string GetTickDescription(MqlTick &tick) 
/***********************************************/
{    
//--- Checking flags 
   bool buy_tick = ((tick.flags&TICK_FLAG_BUY)==TICK_FLAG_BUY); 
   bool sell_tick = ((tick.flags&TICK_FLAG_SELL)==TICK_FLAG_SELL); 

   if(buy_tick == false && sell_tick == false) return("");
   string desc = StringFormat("%s.%03d ", TimeToString(tick.time), tick.time_msc%1000); 
   desc = desc+(buy_tick?StringFormat("0 %G %d", tick.last, tick.volume):""); 
   desc = desc+(sell_tick?StringFormat("1 %G %d", tick.last, tick.volume):"");    
   return desc; 
} 

/***********************************************/
int ExecuteStackRequests(string Msg, string &sStatus)
/***********************************************/
{
   string sOrdem = StringSubstr(Msg,0,2); 
   string sSubOrdem = StringSubstr(Msg,3,StringLen(Msg));
   Print("Request: '"+sOrdem+"' Subrequest: '"+sSubOrdem, "'");

   if(sOrdem == "O0") 
   {
      /////////////////////////////////////////////////////////////////////////
      // Account Info
  
      int iTypeAcc = 0;
      switch((ENUM_ACCOUNT_TRADE_MODE)AccountInfoInteger(ACCOUNT_TRADE_MODE)) 
      { 
         case(ACCOUNT_TRADE_MODE_DEMO): iTypeAcc = 1;  break; 
         case(ACCOUNT_TRADE_MODE_CONTEST): iTypeAcc = 2; break; 
         default:iTypeAcc = 0; break; //Print("Real account!"); 
      } 
      
      int iMarginMode = 0;
      switch((ENUM_ACCOUNT_MARGIN_MODE)AccountInfoInteger(ACCOUNT_MARGIN_MODE)) 
      { 
         case(ACCOUNT_MARGIN_MODE_EXCHANGE): iMarginMode = 1;  break; 
         case(ACCOUNT_MARGIN_MODE_RETAIL_HEDGING): iMarginMode = 2; break; 
         default:iMarginMode = 0; break;
      } 
        
      sStatus = AccountInfoString(ACCOUNT_COMPANY) + SUB_REQUEST_DIVISOR +
                AccountInfoString(ACCOUNT_SERVER) + SUB_REQUEST_DIVISOR +
                IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN)) + SUB_REQUEST_DIVISOR +
                DoubleToString(AccountInfoDouble(ACCOUNT_BALANCE)) + SUB_REQUEST_DIVISOR +
                DoubleToString(AccountInfoDouble(ACCOUNT_EQUITY)) + SUB_REQUEST_DIVISOR +
                DoubleToString(AccountInfoDouble(ACCOUNT_PROFIT)) + SUB_REQUEST_DIVISOR +
                DoubleToString(AccountInfoDouble(ACCOUNT_CREDIT)) + SUB_REQUEST_DIVISOR +
                DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN)) + SUB_REQUEST_DIVISOR +
                DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN_FREE)) + SUB_REQUEST_DIVISOR +
                IntegerToString(iTypeAcc) + SUB_REQUEST_DIVISOR +
                IntegerToString(iMarginMode);
      

      return(1);
   }else if(sOrdem == "O1")
   {
      /////////////////////////////////////////////////////////////////////////
      // Pending Order Request
      
      string sDetails[];
      int iQtyDetails;
      StructureOrders(sSubOrdem, sDetails, iQtyDetails, SUB_REQUEST_DIVISOR);
      
      if(iQtyDetails != 7)
      {
         Print("Resquest dont have enough info ", IntegerToString(iQtyDetails));
         sStatus = "O1ERROR";
         return(1);
      }
      
      string sSymbol = sDetails[0];
      int iCmd = StringToInteger(sDetails[1]);
      double fVol = StringToDouble(sDetails[2]);
      double fPrice = StringToDouble(sDetails[3]);
      double fStop = StringToDouble(sDetails[4]);
      double fGain = StringToDouble(sDetails[5]);
      double iOrderFilling = StringToInteger(sDetails[6]);
      
      //double price;              
      double point = SymbolInfoDouble(sSymbol, SYMBOL_POINT);               
      int digits = SymbolInfoInteger(sSymbol, SYMBOL_DIGITS);       
      sStatus = "O1OK";
      
      if(iCmd != 0 && 
         iCmd != 1)
      {
         Print("Error CMD request ", IntegerToString(iCmd));
         sStatus = "O1ERROR";
         return(1);
      }    
      
      MqlTradeRequest request={0};
      MqlTradeResult  result={0};
      
      //--- parameters to place a pending order 
      request.symbol = sSymbol;                                       
      request.volume = fVol;                                         
      request.type_time = ORDER_TIME_DAY;   
      request.type_filling = ORDER_FILLING_RETURN; 
      
      if(fPrice > 0) request.price = NormalizeDouble(fPrice, digits);
      else if(iCmd == 0) request.price = NormalizeDouble(SymbolInfoDouble(sSymbol, SYMBOL_ASK), digits); //Buy
      else if(iCmd == 1) request.price = NormalizeDouble(SymbolInfoDouble(sSymbol, SYMBOL_BID), digits); //Sell
      
      if(fPrice > 0) request.action = TRADE_ACTION_PENDING;  
      else request.action = TRADE_ACTION_DEAL; 
      
      if(fStop > 0) request.sl = NormalizeDouble(fStop, digits);
      if(fGain > 0) request.tp = NormalizeDouble(fGain, digits);
      
      if(iCmd == 0 && fPrice > 0)  request.type = ORDER_TYPE_BUY_LIMIT;  
      else if(iCmd == 1 && fPrice > 0) request.type = ORDER_TYPE_SELL_LIMIT; 
      else if(iCmd == 0 && fPrice == 0) request.type = ORDER_TYPE_BUY;
      else if(iCmd == 1 && fPrice == 0) request.type = ORDER_TYPE_SELL;
      
      if(iOrderFilling == 1 || fPrice == 0) request.type_filling = ORDER_FILLING_FOK;
      else if(iOrderFilling == 2) request.type_filling = ORDER_FILLING_IOC;
      
      Print("Order request: ", request.symbol, " Cmd: ", IntegerToString(iCmd), " Vol: ", DoubleToString(request.volume), " Price: ",
      DoubleToString(request.price), " Stop: ", DoubleToString(fStop), " Gain: ", fGain, " Filling Type: ", IntegerToString(iOrderFilling));

      // OrderSendAsync //Maybe in the future? https://www.mql5.com/en/docs/trading/ordersendasync
      if(!OrderSend(request,result))
      {
         PrintFormat("OrderSend error %d",GetLastError());       
         sStatus = "O1ERROR";
      }
            
      PrintFormat("retcode=%u  deal=%I64u  order=%I64u",result.retcode,result.deal,result.order);
      ZeroMemory(request);
      ZeroMemory(result);
      
      return(1);
   }else if(sOrdem == "O2")
   {
      /////////////////////////////////////////////////////////////////////////
      // Show positions
      
      Print("Show positions");
      string sTextRes = "", sText;
      ulong  position_ticket;
      string position_symbol;
      int digits;
      ulong  magic;
      double volume;
      double fprice;
      double fstop;
      double fgain;
      double fProfit;
      //MqlTradeRequest request;
      //MqlTradeResult  result;
      int total=PositionsTotal(); 

      for(int i=total-1; i>=0; i--)
      {
         //--- Position details
         position_ticket      =PositionGetTicket(i);                                  // ticket
         position_symbol      =PositionGetString(POSITION_SYMBOL);                    // symbol
         digits               =(int)SymbolInfoInteger(position_symbol,SYMBOL_DIGITS);              
         magic                =PositionGetInteger(POSITION_MAGIC);                    // magic number
         volume               =PositionGetDouble(POSITION_VOLUME);                    // volume
         fprice               =PositionGetDouble(POSITION_PRICE_OPEN);                            
         fstop                =PositionGetDouble(POSITION_SL);
         fgain                =PositionGetDouble(POSITION_TP);
         fProfit              =PositionGetDouble(POSITION_PROFIT);
         
         ENUM_POSITION_TYPE type = (ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE);  // position type
         
	 // Position type
         int iTypePos = -1;
         if(type == POSITION_TYPE_BUY) iTypePos = 0;
         else iTypePos = 1;
         
         //--- output info
         PrintFormat("#%I64u %s  %s  %.2f  %s [%I64d]",
                     position_ticket,
                     position_symbol,
                     EnumToString(type),
                     volume,
                     DoubleToString(PositionGetDouble(POSITION_PRICE_OPEN),digits),
                     magic);
                     
         sText = position_ticket + SUB_REQUEST_DIVISOR + position_symbol + SUB_REQUEST_DIVISOR + IntegerToString(iTypePos) + SUB_REQUEST_DIVISOR + DoubleToString(volume) + SUB_REQUEST_DIVISOR + 
         DoubleToString(fprice,digits) + SUB_REQUEST_DIVISOR + DoubleToString(fstop,digits) + SUB_REQUEST_DIVISOR + DoubleToString(fgain,digits) + SUB_REQUEST_DIVISOR + DoubleToString(fProfit,digits) + REQUEST_DIVISOR;
         
         sTextRes = sTextRes + sText;           
      }
      sStatus = sTextRes;
      return(1);
   }else if(sOrdem == "O3")
   {
      /////////////////////////////////////////////////////////////////////////
      // Show orders
      
      Print("Show orders");
      string sTextRes = "", sText;
      ulong    ticket; 
      double   open_price; 
      double   fStop;
      double   fGain;
      double   initial_volume; 
      datetime time_setup; 
      string   symbol; 
      string   type; 
      long     order_magic; 
      long     positionID; 
      int digits;

      uint     total=OrdersTotal(); 
      for(uint i=0;i<total;i++) 
      { 
         //--- returns orders ticket
         if((ticket=OrderGetTicket(i)) > 0) 
         { 
            //--- returns orders property
            time_setup    =(datetime)OrderGetInteger(ORDER_TIME_SETUP); 
            symbol        =OrderGetString(ORDER_SYMBOL); 
            digits        =(int)SymbolInfoInteger(symbol,SYMBOL_DIGITS);  
            order_magic   =OrderGetInteger(ORDER_MAGIC); 
            positionID    =OrderGetInteger(ORDER_POSITION_ID); 
            initial_volume=OrderGetDouble(ORDER_VOLUME_CURRENT); 
            type          =EnumToString(ENUM_ORDER_TYPE(OrderGetInteger(ORDER_TYPE))); 
            open_price    =OrderGetDouble(ORDER_PRICE_OPEN); 
            fStop         =OrderGetDouble(ORDER_SL); 
            fGain         =OrderGetDouble(ORDER_TP); 

            /*
	    // Debug propuses
            printf("#ticket %d %s %G %s em %G was created %s", 
                   ticket,                 // order ticket
                   type,                   // type
                   initial_volume,         // volume
                   symbol,                 // symbol
                   open_price,             // open price
                   TimeToString(time_setup)// time elapsed to order
                   ); 
           */
           sText = IntegerToString(ticket) + SUB_REQUEST_DIVISOR + symbol + SUB_REQUEST_DIVISOR + IntegerToString(OrderGetInteger(ORDER_TYPE)) + SUB_REQUEST_DIVISOR + DoubleToString(initial_volume) + SUB_REQUEST_DIVISOR + 
           DoubleToString(open_price, digits) + SUB_REQUEST_DIVISOR + DoubleToString(fStop, digits) + SUB_REQUEST_DIVISOR + DoubleToString(fGain, digits) + REQUEST_DIVISOR; 
           sTextRes = sTextRes + sText;
           Print(sText);  
                                
         }
      }

      sStatus = sTextRes;
      return(1);
   }else if(sOrdem == "O4")
   {
      /////////////////////////////////////////////////////////////////////////
      // Access book
      
      bool bRemoveAfter = false;
      bool bDownloadAllowed = true;
      string sDetails[];
      int iQtyDetails;
      StructureOrders(sSubOrdem, sDetails, iQtyDetails, SUB_REQUEST_DIVISOR);
      
      string sSymbol = sDetails[0];
      
      string sText = "";
      int iBidAsk = StringToInteger(sDetails[1]);
      int iDeepLevel = StringToInteger(sDetails[2]);
      
      Print("Accessing book ", sSymbol);
      
      if(SymbolExists(sSymbol))
      {
        //printf("Mrketwatch has it");
      }
      else
      {
         //printf("Marketwatch haven't it");
         bRemoveAfter = true;
         if(!SymbolSelect(sSymbol, true))
         {
            bDownloadAllowed = false;
         }
      }     
      
      if(bDownloadAllowed)
      {
         Sleep(100); //Experimental
         sText = Access_Book(sSymbol, SUB_REQUEST_DIVISOR, iBidAsk, iDeepLevel, "O4ERROR");
      }
      if(bRemoveAfter && bRemoveSymbolsAfterUse)
      {
         SymbolSelect(sSymbol, false);
      } 
      
      sStatus = "O4OK"+SUB_REQUEST_DIVISOR+sSymbol+SUB_REQUEST_DIVISOR+sText;
      return(1);
   }else if(sOrdem == "O5")
   {
      /////////////////////////////////////////////////////////////////////////
      // Get simple spread
      
      bool bRemoveAfter = false;
      bool bDownloadAllowed = true;
      string sSymbol = sSubOrdem;
      string sText;
      
      if(SymbolExists(sSymbol))
      {
        printf("Marketwatch has it");
      }
      else
      {
         //printf("Marketwatch haven't it");
         bRemoveAfter = true;
         if(!SymbolSelect(sSymbol, true))
         {
            bDownloadAllowed = false;
         }
         Sleep(200); //Experimental
      }
      
      int iDigits = (int)SymbolInfoInteger(sSymbol,SYMBOL_DIGITS); 
      
      if(bDownloadAllowed)
      {
         sText = DoubleToString(SymbolInfoDouble(sSymbol, SYMBOL_BID), iDigits) + SUB_REQUEST_DIVISOR + DoubleToString(SymbolInfoDouble(sSymbol, SYMBOL_ASK), iDigits);
      }
      if(bRemoveAfter && bRemoveSymbolsAfterUse)
      {
         SymbolSelect(sSymbol, false);
      } 
      
      sStatus = "O5OK"+SUB_REQUEST_DIVISOR+sSymbol+SUB_REQUEST_DIVISOR+sText;
      return(1);
   }else if(sOrdem == "O6")
   {
      /////////////////////////////////////////////////////////////////////////
      // Modify pending order
      
      string sDetails[];
      int iQtyDetails;
      StructureOrders(sSubOrdem, sDetails, iQtyDetails, SUB_REQUEST_DIVISOR);
      
      string sTicket = sDetails[0];
      string sPrice = sDetails[1];
      string sStop = sDetails[2];
      string sGain = sDetails[3];
      //string sVol = sDetails[4];
      
      ulong iTicketAlvo = StringToInteger(sTicket);
      ulong  ticket; 
      //int iCmd = StringToInteger(sCmd);
      double fPrice = StringToDouble(sPrice);
      double fStop = StringToDouble(sStop);
      double fGain = StringToDouble(sGain);
      //double fVol = StringToDouble(sVol);
      
      if(fStop == fGain && fStop > 0)
      {
         Print("fStop cannot be equal to fGain?");
         sStatus = "O6ERROR";
         return(1);
      }

      sStatus = "O6ERROR";
      Print("Modifying pending order: ticket: '", sTicket, "' price: '", sPrice, "' stop: '", sStop, "' gain: '", sGain,"'");

      sStatus = "O6ERROR";
      bool bModified_SL_TP = false;
      bool bFoundOrder = false;
      for(int i = OrdersTotal()-1; i>=0; i--)
      {
         ticket = OrderGetTicket(i);
         if(ticket == iTicketAlvo)
         {
            bFoundOrder = true;
            //Print("Modifying order: " + IntegerToString(ticket));

            MqlTradeResult result={0};
            MqlTradeRequest request={0};
            request.order = OrderGetTicket(i);
            request.action = TRADE_ACTION_MODIFY;
            
            request.symbol = OrderGetString(ORDER_SYMBOL);
            request.magic = OrderGetInteger(ORDER_MAGIC);
            request.expiration = (ENUM_ORDER_TYPE_TIME)OrderGetInteger(ORDER_TYPE_TIME);
            request.type = (ENUM_ORDER_TYPE)OrderGetInteger(ORDER_TYPE);
            
            if(fStop == -1) request.sl = 0;
            else if(fStop > 0) request.sl = fStop;
            else request.sl = OrderGetDouble(ORDER_SL);
            
            if(fGain == -1) request.tp = 0;
            else if(fGain > 0) request.tp = fGain;
            else request.tp = OrderGetDouble(ORDER_TP);
            
            if(fPrice > 0)request.price = fPrice;
            else request.price = OrderGetDouble(ORDER_PRICE_OPEN);            

            //if(fVol > 0) request.volume = fVol; //For some reason some brokers do not allow it
            //else request.volume = OrderGetDouble(ORDER_VOLUME_CURRENT);
            
            if(OrderSend(request,result))
            {
               sStatus = "O6OK";
            }else sStatus = "O6ERROR2";
            
            Print(__FUNCTION__,": ",result.comment," reply code ",result.retcode);
            ZeroMemory(request);
            ZeroMemory(result);
            return(1);
         }
      }
     
      if(!bFoundOrder)
      {
         Print("Pending order was not found!");
      }
      
      return(1);      
   }else if(sOrdem == "O7")
   {
      /////////////////////////////////////////////////////////////////////////
      // Delete pending order
      
      string sDetails[];
      int iQtyDetails;
      StructureOrders(sSubOrdem, sDetails, iQtyDetails, SUB_REQUEST_DIVISOR);
      
      string sTicket = sDetails[0];
      ulong iTicketAlvo = StringToInteger(sTicket);
      ulong  ticket; 
      
      Print("Deleting pending order: ticket: ", sTicket);    

      //CTrade *trade=new CTrade();
      for(int i = OrdersTotal()-1; i>=0; i--)
      {
         ticket = OrderGetTicket(i);
         if(ticket == iTicketAlvo)
         {
            Print("Pending order found: ticket " + IntegerToString(ticket));

            // There are two ways to delete an order
            //First
            /*
            CTrade *trade=new CTrade();
            trade.OrderDelete(ticket);
            delete trade;  
            sStatus = "O7OK";
            return(1);  
            */ 

            //Second
            MqlTradeResult result={0};
            MqlTradeRequest request={0};
            request.action = TRADE_ACTION_REMOVE;
            request.order = ticket; 
            
            if(OrderSend(request,result))
            {
               sStatus = "O7OK";
            }else sStatus = "O7ERROR2";
            
            //--- write the server reply to log
            Print(__FUNCTION__,": ",result.comment," reply code ",result.retcode);
            ZeroMemory(request);
            ZeroMemory(result);
            return(1);
         }
      }

      sStatus = "O7ERROR";
      return(1);      
   }else if(sOrdem == "O8")
   {
      /////////////////////////////////////////////////////////////////////////
      // Modify position
      
      string sDetails[];
      int iQtyDetails;
      StructureOrders(sSubOrdem, sDetails, iQtyDetails, SUB_REQUEST_DIVISOR);
      
      string sTicket = sDetails[0];
      string sStop = sDetails[1];
      string sGain = sDetails[2];
      
      ulong iTicketAlvo = StringToInteger(sTicket);
      ulong  ticket; 
      double fStop = StringToDouble(sStop);
      double fGain = StringToDouble(sGain);
      
      if(fStop == fGain && fStop > 0)
      {
         Print("fStop cannot be equal to fGain?");
         sStatus = "O8ERROR";
         return(1);
      }

      Print("Modifying position: Ticket: '", sTicket, "' Stop: '", sStop, "' Gain: '", sGain,"'");

      int total=PositionsTotal(); 
      for(int i=total-1; i>=0; i--)
      {
         ticket = PositionGetTicket(i);
         if(ticket == iTicketAlvo)
         {
            Print("Position found: " + IntegerToString(ticket));
         
            //debugging purposes - start
            string position_symbol=PositionGetString(POSITION_SYMBOL); 
            int    digits = (int)SymbolInfoInteger(position_symbol,SYMBOL_DIGITS); 
            ulong  magic = PositionGetInteger(POSITION_MAGIC);
            double volume = PositionGetDouble(POSITION_VOLUME);    
            double sl = PositionGetDouble(POSITION_SL);  
            double tp = PositionGetDouble(POSITION_TP); 
            ENUM_POSITION_TYPE type=(ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE);
            //--- position info
            PrintFormat("Position was #%I64u %s  %s  %.2f  %s  sl: %s  tp: %s  [%I64d]",
                  ticket,
                  position_symbol,
                  EnumToString(type),
                  volume,
                  DoubleToString(PositionGetDouble(POSITION_PRICE_OPEN),digits),
                  DoubleToString(sl,digits),
                  DoubleToString(tp,digits),
                  magic);       
            //debugging purposes - end
		            
            //Some modifications commands only work when you declare those below requests
            MqlTradeResult result={0};
            MqlTradeRequest request={0};
            request.action  = TRADE_ACTION_SLTP; 
            request.position = ticket;   
            request.symbol = position_symbol;
            request.magic = magic;

            if(fStop == -1) request.sl = 0;
            else if(fStop > 0) request.sl = NormalizeDouble(fStop, digits);
            else request.sl = PositionGetDouble(POSITION_SL);
            
            if(fGain == -1) request.tp = 0;
            else if(fGain > 0) request.tp = NormalizeDouble(fGain, digits);   
            else request.tp = PositionGetDouble(POSITION_TP);
            
            if(OrderSend(request,result))
            {
               sStatus = "O8OK";
            }else sStatus = "O8ERROR2";
            
            Print(__FUNCTION__,": ",result.comment," reply code ",result.retcode);
            ZeroMemory(request);
            ZeroMemory(result);
            return(1);
         }
      }
     
      sStatus = "O8ERROR";
      return(1);      
   }else if(sOrdem == "O9")
   {
      /////////////////////////////////////////////////////////////////////////
      // Close position
      
      string sDetails[];
      int iQtyDetails;
      StructureOrders(sSubOrdem, sDetails, iQtyDetails, SUB_REQUEST_DIVISOR);
      
      string sTicket = sDetails[0];
      
      ulong iTicketAlvo = StringToInteger(sTicket);
      ulong  ticket; 

      sStatus = "O9ERROR";
      Print("Closing position: Ticket: '", sTicket);

      int total=PositionsTotal(); 
      for(int i=total-1; i>=0; i--)
      {
         ticket = PositionGetTicket(i);
         if(ticket == iTicketAlvo)
         {
            Print("Position found: " + IntegerToString(ticket));
         
            //debugging purposes - start
            string position_symbol=PositionGetString(POSITION_SYMBOL); 
            int    digits = (int)SymbolInfoInteger(position_symbol,SYMBOL_DIGITS); 
            ulong  magic = PositionGetInteger(POSITION_MAGIC);
            double volume = PositionGetDouble(POSITION_VOLUME);    
            double sl = PositionGetDouble(POSITION_SL);  
            double tp = PositionGetDouble(POSITION_TP); 
            ENUM_POSITION_TYPE type=(ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE);
            //--- position info
            PrintFormat("Position was #%I64u %s  %s  %.2f  %s  sl: %s  tp: %s  [%I64d]",
                  ticket,
                  position_symbol,
                  EnumToString(type),
                  volume,
                  DoubleToString(PositionGetDouble(POSITION_PRICE_OPEN),digits),
                  DoubleToString(sl,digits),
                  DoubleToString(tp,digits),
                  magic);       
            //debugging purposes - end
		            
            CTrade *trade=new CTrade();
            if(trade.PositionClose(ticket))
	         {
	    	      Print("Success: position closed! ResultRetcode: ", trade.ResultRetcode(), 
                     ". RetcodeDescription: ", trade.ResultRetcodeDescription());
               sStatus = "O9OK";
            }else
            {
               Print("Failure: position not closed! ResultRetcode: ", trade.ResultRetcode(), 
                     ". RetcodeDescription: ", trade.ResultRetcodeDescription());
               sStatus = "O9ERROR2";
            }
            delete trade;  

            return(1);
         }
      }
     
      return(1);      
   }else if(sOrdem == "M1") 
   {
      /////////////////////////////////////////////////////////////////////////
      // Download Table
      
      bool bRemoveAfter = false;
      bool bDownloadAllowed = true;
      
      string sDetalhes[];
      int iQtdDetalhes;
      StructureOrders(sSubOrdem, sDetalhes, iQtdDetalhes, SUB_REQUEST_DIVISOR);
      
      string sSymbol = sDetalhes[0];
      int iTF = StringToInteger(sDetalhes[1]);
      int iQtyBars = StringToInteger(sDetalhes[2]);
      
      ENUM_TIMEFRAMES eWhichTF = CategorizeTimeFrames(iTF); 
      if(eWhichTF == -1)
      {
         Print("Error: not recognized time frame");
         sStatus = "M1ERROR3"+SUB_REQUEST_DIVISOR+sSymbol;
         return(1);
      }
      
      if(SymbolExists(sSymbol))
      {
        //printf("Mrketwatch has it");
      }
      else
      {
         //printf("Marketwatch haven't it");
         bRemoveAfter = true;
         if(!SymbolSelect(sSymbol, true))
         {
            bDownloadAllowed = false;
         }
      }     
      if(bDownloadAllowed)
      {
         Sleep(100); //Experimental
         DownloadSymbol_csv(sSymbol, sDetalhes[1], eWhichTF, iQtyBars);
      }
      if(bRemoveAfter && bRemoveSymbolsAfterUse)
      {
         SymbolSelect(sSymbol, false);
      } 
      
      if(!bDownloadAllowed)sStatus = "M1ERROR2"+SUB_REQUEST_DIVISOR+sSymbol;
      else sStatus = "M1OK"+SUB_REQUEST_DIVISOR+sSymbol;
      
      return(1);
   }else if(sOrdem == "S1")
   {
      /////////////////////////////////////////////////////////////////////////
      // Ping Pong
   
      sStatus = "S1OK";
      return(1);
   }else if(sOrdem == "M3")
   {
      /////////////////////////////////////////////////////////////////////////
      // Symbol Class
      
      string sDetails[];
      int iQtyDetails;
      StructureOrders(sSubOrdem, sDetails, iQtyDetails, SUB_REQUEST_DIVISOR);
      
      string sSymbol = sDetails[0];
      
      MqlTick last_tick;
      SymbolInfoTick(sSymbol,last_tick);
      double fLastAsk = last_tick.last;
      ZeroMemory(last_tick);
      
      int iObjectType;
      int iCalcMode = SymbolInfoInteger(sSymbol, SYMBOL_TRADE_CALC_MODE);
      int iDigits = SymbolInfoInteger(sSymbol, SYMBOL_DIGITS);
      
      if(!SymbolExists(sSymbol)) //Not in marketwatch
      {
         sStatus = sSymbol + SUB_REQUEST_DIVISOR + IntegerToString(-1) + REQUEST_DIVISOR; //Undefined
         return(1);
      }
      
      if(iCalcMode == 2)
      {
         iObjectType = 4; // CFD
      }else if(fLastAsk < 0.01)
      {
         // Some FX brokers only gives last price. So need to be carefully here
         if(iDigits > 0)
         {
            iObjectType = 3; // FX
         }else
         {
            sStatus = sSymbol + SUB_REQUEST_DIVISOR + IntegerToString(-1) + REQUEST_DIVISOR; //Undefined
            return(1);
         }
      }else
      {
         datetime dtExp = SymbolInfoInteger(sSymbol,SYMBOL_EXPIRATION_TIME);
         MqlDateTime stm;
         TimeToStruct(dtExp,stm);
               
         Print(fLastAsk);
         iObjectType = 0; //Stock
         if(stm.year > 1970)
         {
            if(SymbolInfoDouble(sSymbol, SYMBOL_OPTION_STRIKE )> 0)
            {
               iObjectType = 1; //Options
            }else
            {
               iObjectType = 2; //Futures
            }
         }
      }
      

      
      sStatus = sSymbol + SUB_REQUEST_DIVISOR + IntegerToString(iObjectType) + REQUEST_DIVISOR; 
      return(1);
   }else if(sOrdem == "S2")
   {
      /////////////////////////////////////////////////////////////////////////
      // File MT5's folder
      
      string sWF = TerminalInfoString(TERMINAL_DATA_PATH)+"\\MQL5\\Files\\"; 
      //Print(sWF);
      sStatus = sWF + REQUEST_DIVISOR;
      return(1);
   }else if(sOrdem == "M2")
   {      
      /////////////////////////////////////////////////////////////////////////
      // List all options of an underlying asset
   
      if(StringLen(sSubOrdem) < 3)
      {
         sStatus = "M2ERROR";
         return(1);
      }
      
      string sDetails[];
      int iQtyDetails;
      
      StructureOrders(sSubOrdem, sDetails, iQtyDetails, SUB_REQUEST_DIVISOR);
      
      // Based into "Trader_Patinhas" code 2018.07.01
      // https://www.mql5.com/pt/forum/260966
      
      string UNDERLYING_STOCK = sDetails[0];     
      string sText;
      string sTextComplete = "";
      int iTotOptions = 0;

      for(int i = 0; i < SymbolsTotal(false); i++)
      {
         // Get target ticker
         string  sSymbol = SymbolName(i,false);
               
         if(StringSubstr(sSymbol,0,4) == UNDERLYING_STOCK && SymbolInfoDouble(sSymbol,SYMBOL_OPTION_STRIKE) > 0) 
         {
            sText = StringFormat(
               "%10s %4s %s %5.2f %s %s" , 
               sSymbol,
               StringSubstr(EnumToString((ENUM_SYMBOL_OPTION_RIGHT) SymbolInfoInteger(sSymbol, SYMBOL_OPTION_RIGHT)), 20),
               TimeToString(SymbolInfoInteger(sSymbol , SYMBOL_EXPIRATION_TIME ), TIME_DATE), 
               SymbolInfoDouble(sSymbol, SYMBOL_OPTION_STRIKE),
               StringSubstr(EnumToString((ENUM_SYMBOL_OPTION_MODE) SymbolInfoInteger(sSymbol, SYMBOL_OPTION_MODE)), 19),
               SymbolInfoString(sSymbol, SYMBOL_DESCRIPTION)
            );
            
            //Print(sText);
            sTextComplete = sTextComplete + SUB_REQUEST_DIVISOR + sText;
            iTotOptions++;
          }
      }
      if(iTotOptions == 0) sTextComplete = "0" + SUB_REQUEST_DIVISOR;
      
      Print("Total options: " + IntegerToString(iTotOptions));
      sStatus = sTextComplete + REQUEST_DIVISOR;
      return(1);
   }else if(sOrdem == "C1")
   {   
      /////////////////////////////////////////////////////////////////////////
      // Draw horizontal line
   
      string sDetalhes[];
      int iQtdDetalhes;
      
      StructureOrders(sSubOrdem, sDetalhes, iQtdDetalhes, SUB_REQUEST_DIVISOR);
      
      string sSymbol = sDetalhes[0];  
      string sName = sDetalhes[1];  
      string sPrice = sDetalhes[2];  
      string sWidth = sDetalhes[3];  
      string sColor = sDetalhes[4];
      string sTF = sDetalhes[5];
      
      double fPrice = StringToDouble(sPrice); 
      int iWidth = StringToInteger(sWidth);
      int iColor = StringToInteger(sColor);
      int iTF = StringToInteger(sTF);
      
      bool bFindAny = false;
      if(iWidth < 1)
      {
         iWidth = 1;
      }
      
      ENUM_TIMEFRAMES QualTF = CategorizeTimeFrames(iTF); 
      if(QualTF == -1)
      {
         QualTF = _Period;
         //sStatus = "C1ERROR";
      }
      
      // Colors
      // https://www.mql5.com/en/docs/constants/objectconstants/webcolors
      
      color ccColor = clrGreen;
      switch(iColor)
      {
         case 1: ccColor = clrGreen;break; //GREEN
         case 2: ccColor = clrBlue;break; //BLUE
         case 3: ccColor = clrRed;break; ///RED
         case 4: ccColor = clrNavy;break;
         case 5: ccColor = clrPurple;break;
         case 6: ccColor = clrIndigo;break;
         case 7: ccColor = clrOliveDrab;break;
         case 8: ccColor = clrDarkSlateBlue;break;
         case 9: ccColor = clrLawnGreen;break;
         case 10: ccColor = clrOrangeRed;break;
         case 11: ccColor = clrGold;break;
         case 12: ccColor = clrYellow;break;
         case 13: ccColor = clrAqua;break;
         case 14: ccColor = clrMagenta;break;
         case 15: ccColor = clrLightSlateGray;break;
         case 16: ccColor = clrPaleVioletRed;break;
         case 17: ccColor = clrHotPink;break;
         case 18: ccColor = clrKhaki;break;
         case 19: ccColor = clrSilver;break;
         case 20: ccColor = clrLightGray;break;
         case 21: ccColor = clrKhaki;break;
         case 22: ccColor = clrBeige;break;
         default: ccColor = clrGreen ;break;
      }
      
      PrintFormat("Drawing horizontal line: %6s price %5.2f widith %d color %d", 
                  sSymbol, fPrice, iWidth, iColor);

      for(long ch=ChartFirst();ch>0;ch=ChartNext(ch))
      {
         if(ChartSymbol(ch) == sSymbol)
         {
            if(iTF > 0 && ChartPeriod(ch) != QualTF) continue;
            
            ObjectCreate(ch, sName, OBJ_HLINE, 0, 0, fPrice); 
            ObjectSetInteger(ch, sName,OBJPROP_WIDTH, iWidth);            
            ObjectSetInteger(ch, sName, OBJPROP_COLOR, ccColor);
            ObjectSetInteger(ch, sName, OBJPROP_HIDDEN, false);      
            ObjectSetInteger(ch, sName, OBJPROP_SELECTABLE, true);
            ObjectSetInteger(ch, sName, OBJPROP_READONLY, false);
            ChartRedraw(ch);
            bFindAny = true;
         }
      }
      
      sStatus = "C1ERROR";
      if(bFindAny)
      {
         sStatus = "C1OK";
      }  
      
      return(1);
    }else if(sOrdem == "C2")
    {   
      /////////////////////////////////////////////////////////////////////////
      // Remove all objects of all charts of specific symbol and timeframe
      
      string sDetalhes[];
      int iQtdDetalhes;
      
      StructureOrders(sSubOrdem, sDetalhes, iQtdDetalhes, SUB_REQUEST_DIVISOR);
      
      string sSymbol = sDetalhes[0]; 
      string sTF = sDetalhes[1]; 
      
      int iTF = StringToInteger(sTF);     
      ENUM_TIMEFRAMES QualTF = CategorizeTimeFrames(iTF); 
      if(QualTF == -1)
      {
         QualTF = _Period;
      }
      
      if(iTF == 0)
      {
         Print("Removing all objects of all charts symbol: ", sSymbol);
      }else if(sSymbol != "0" && iTF != 0)
      {
         Print("Removing all objects of all charts symbol: ", sSymbol, " TF: ", iTF);
      }else if(iTF != 0)
      {
         Print("Removing all objects of all charts TF: ", iTF);
      }
      
      for(long ch=ChartFirst();ch>0;ch=ChartNext(ch))
      {
         if(ChartSymbol(ch) == sSymbol || sSymbol == "0")
         {
            if(iTF > 0 && ChartPeriod(ch) != QualTF) continue;
            ObjectsDeleteAll(ch);
         }
      }
      
      sStatus = "C2OK";     
      return(1);
         
   }else if(sOrdem == "C3")
   {   
      /////////////////////////////////////////////////////////////////////////
      // Remove all objects of all charts
      
      Print("Removing all objects of all charts");
      
      for(long ch=ChartFirst();ch>0;ch=ChartNext(ch))
      {
         ObjectsDeleteAll(ch);
      }
      
      sStatus = "C3OK";     
      return(1);
         
   }else if(sOrdem == "M4") 
   {
      /////////////////////////////////////////////////////////////////////////
      // Download Table Socket
      
      bool bRemoveAfter = false;
      bool bDownloadAllowed = true;
      
      string sDetalhes[];
      int iQtdDetalhes;
      StructureOrders(sSubOrdem, sDetalhes, iQtdDetalhes, SUB_REQUEST_DIVISOR);
      
      string sSymbol = sDetalhes[0], sResult = "";;
      int iTF = StringToInteger(sDetalhes[1]);
      int iQtyBars = StringToInteger(sDetalhes[2]);

      ENUM_TIMEFRAMES eWhichTF = CategorizeTimeFrames(iTF); 
      if(eWhichTF == -1)
      {
         Print("Error: not recognized time frame");
         sStatus = "M4ERROR3"+SUB_REQUEST_DIVISOR+sSymbol;
         return(1);
      }else if(SymbolExists(sSymbol))
      {
        //printf("Belongs to marketwatch");
      }else
      {
         //printf("Do not belong to marketwatch");
         bRemoveAfter = true;
         if(!SymbolSelect(sSymbol, true))
         {
            bDownloadAllowed = false;
         }
      }     
      
      if(bDownloadAllowed)
      {
         DownloadSymbol_socket(sSymbol, eWhichTF, iQtyBars, sResult);
         if(sResult == "")
         {
            Print("Error: not available data");
            sStatus = "M4ERROR4"+SUB_REQUEST_DIVISOR+sSymbol;
            return(1);
         }
      }
      if(bRemoveAfter && bRemoveSymbolsAfterUse) //If you want speed, you dont want executing this all the time
      {
         SymbolSelect(sSymbol, false);
      } 
      
      if(!bDownloadAllowed)sStatus = "M4ERROR2"+SUB_REQUEST_DIVISOR+sSymbol;
      else sStatus = sResult;
      
      return(1);
   }else if(sOrdem == "O0") 
   {
      /////////////////////////////////////////////////////////////////////////
      // Account Info
  
      int iTypeAcc = 0;
      switch((ENUM_ACCOUNT_TRADE_MODE)AccountInfoInteger(ACCOUNT_TRADE_MODE)) 
      { 
         case(ACCOUNT_TRADE_MODE_DEMO): iTypeAcc = 1;  break; 
         case(ACCOUNT_TRADE_MODE_CONTEST): iTypeAcc = 2; break; 
         default:iTypeAcc = 0; break; //Print("Esta é uma conta real!"); 
      } 
      
      int iMarginMode = 0;
      switch((ENUM_ACCOUNT_MARGIN_MODE)AccountInfoInteger(ACCOUNT_MARGIN_MODE)) 
      { 
         case(ACCOUNT_MARGIN_MODE_EXCHANGE): iMarginMode = 1;  break; 
         case(ACCOUNT_MARGIN_MODE_RETAIL_HEDGING): iMarginMode = 2; break; 
         default:iMarginMode = 0; break;
      } 
        
      sStatus = AccountInfoString(ACCOUNT_COMPANY) + SUB_REQUEST_DIVISOR +
                AccountInfoString(ACCOUNT_SERVER) + SUB_REQUEST_DIVISOR +
                IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN)) + SUB_REQUEST_DIVISOR +
                DoubleToString(AccountInfoDouble(ACCOUNT_BALANCE)) + SUB_REQUEST_DIVISOR +
                DoubleToString(AccountInfoDouble(ACCOUNT_EQUITY)) + SUB_REQUEST_DIVISOR +
                DoubleToString(AccountInfoDouble(ACCOUNT_PROFIT)) + SUB_REQUEST_DIVISOR +
                DoubleToString(AccountInfoDouble(ACCOUNT_CREDIT)) + SUB_REQUEST_DIVISOR +
                DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN)) + SUB_REQUEST_DIVISOR +
                DoubleToString(AccountInfoDouble(ACCOUNT_MARGIN_FREE)) + SUB_REQUEST_DIVISOR +
                IntegerToString(iTypeAcc) + SUB_REQUEST_DIVISOR +
                IntegerToString(iMarginMode);
      

      return(1);
   }else if(sOrdem == "H0") 
   {
      /////////////////////////////////////////////////////////////////////////
      // History positions
      
      // Under construction
      /*
      HistorySelect(0, TimeCurrent()); 
      ulong iTicket;            // bilhetagem da operação (deal)
      ulong order_ticket;           // ticket da ordem que o negócio foi executado em
      datetime transaction_time;    // tempo de execução de um negócio
      long deal_type ;              // tipo de operação comercial
      long position_ID;             // ID posição
      string deal_description;      // descrição da operação
      double volume;                // volume da operação
      string sSymbol;                // ativo da negociação
      double fProfit;

      int deals=HistoryOrdersTotal();
      int iTeste;
      for(int i=0;i<deals;i++)
      {
         iTicket = HistoryDealGetTicket(i);
         fProfit = HistoryDealGetDouble(iTicket, DEAL_PROFIT);
         sSymbol = HistoryDealGetString(iTicket, DEAL_SYMBOL);
         
         if(fProfit == 0)continue;
         if(sSymbol == "")continue;
         
         volume=                    HistoryDealGetDouble(iTicket,DEAL_VOLUME);
         transaction_time=(datetime)HistoryDealGetInteger(iTicket,DEAL_TIME);
         order_ticket=              HistoryDealGetInteger(iTicket,DEAL_ORDER);
         deal_type=                 HistoryDealGetInteger(iTicket,DEAL_TYPE);
         iTeste = HistoryDealGetInteger(iTicket, DEAL_ENTRY);
         
         position_ID=               HistoryDealGetInteger(iTicket,DEAL_POSITION_ID);
         //deal_description=          GetDealDescription(deal_type,volume,symbol,order_ticket,position_ID);
         //--- realizar uma boa formatação para o número de negócio
         string print_index=StringFormat("% 3d",i);
         //--- mostrar informações sobre o negócio
         Print(print_index+": deal #",iTicket," ",sSymbol," em ",transaction_time, " profit ", fProfit, " ", order_ticket);
        }
      */
     
      return(1);
   }else if(sOrdem == "P0") 
   {
      /////////////////////////////////////////////////////////////////////////
      // Market is open?
      
      datetime dtNowDelayed = TimeCurrent() - 0;
      string sSymbol;
      long lTime = (long)dtNowDelayed;
      bool bReturn = false;
      Sleep(1000);
      Print(lTime);
      Print("##");
      for(int i=0;i<SymbolsTotal(1);i++)
      {  
         sSymbol = SymbolName(i, true);
         Print(sSymbol);
         Print(SymbolInfoInteger(sSymbol, SYMBOL_TIME));
         if(SymbolInfoInteger(sSymbol, SYMBOL_TIME) > dtNowDelayed)
         {
            bReturn = true;
            break;
         }
      }

      /*
      MqlDateTime str1;
      TimeToStruct(dtNowDelayed,str1);

      ENUM_DAY_OF_WEEK day_of_week = (ENUM_DAY_OF_WEEK) str1.day_of_week;
      
      if(day_of_week == SATURDAY)
      {
         bReturn = false; //Saturday
      }
      */
      
      if(bReturn) sStatus = "P0OK";
      else sStatus = "P0ERROR";      
      
      return(1);
   }else if(sOrdem == "P1") 
   {
      /////////////////////////////////////////////////////////////////////////
      // Add symbols in MT5's Marketwatch
      
      string sSymbol;
      for(int i=0;i<SymbolsTotal(1);i++)
      {  
         sSymbol = SymbolName(i, true);
         if(i==0)sStatus = sSymbol;
         else sStatus = sStatus + SUB_REQUEST_DIVISOR + sSymbol;
      }
      return (1);
   }else if(sOrdem == "P2") 
   {
      /////////////////////////////////////////////////////////////////////////
      // Remove symbols of Marketwatch
      
      string sDetails[];
      int iQtyDetails;
      string sSymbol;
      
      StructureOrders(sSubOrdem, sDetails, iQtyDetails, SUB_REQUEST_DIVISOR);
      
      for(int i=0;i<iQtyDetails;i++)
      {
         sSymbol = sDetails[i];
         if(SymbolSelect(sSymbol, false))
         {
            if(i==0)sStatus = "P2OK";
            else sStatus = sStatus + SUB_REQUEST_DIVISOR + "P2OK";
         }else
         {
            if(i==0)sStatus = "P2ERROR";
            else sStatus = sStatus + SUB_REQUEST_DIVISOR + "P2ERROR";
         }
      }
      
   }else if(sOrdem == "P3") 
   {
      /////////////////////////////////////////////////////////////////////////
      // Add symbols in Marketwatch
      
      string sDetails[];
      int iQtyDetails;
      string sSymbol;
      
      StructureOrders(sSubOrdem, sDetails, iQtyDetails, SUB_REQUEST_DIVISOR);
      
      for(int i=0;i<iQtyDetails;i++)
      {
         sSymbol = sDetails[i];
         if(SymbolSelect(sSymbol, true))
         {
            if(i==0)sStatus = "P3OK";
            else sStatus = sStatus + SUB_REQUEST_DIVISOR + "P3OK";
         }else
         {
            if(i==0)sStatus = "P3ERROR";
            else sStatus = sStatus + SUB_REQUEST_DIVISOR + "P3ERROR";
         }
      }
      return(1);
   }else if(sOrdem == "M5") 
   {
      /////////////////////////////////////////////////////////////////////////
      // Get latest closes
      
      string sDetails[];
      int iQtyDetails, iTF;
      string sSymbol, sText;
      
      StructureOrders(sSubOrdem, sDetails, iQtyDetails, SUB_REQUEST_DIVISOR);
      
      iTF = StringToInteger(sDetails[0]);
      
      ENUM_TIMEFRAMES eWhichTF = CategorizeTimeFrames(iTF); 
      if(eWhichTF == -1)
      {
         Print("Error: not recognized time frame");
         sStatus = "M5ERROR3";
         return(1);
      }else if(iQtyDetails < 2)
      {
         Print("Error: no symbols?");
         sStatus = "M5ERROR";
         return(1);
      }
      for(int i=1;i<iQtyDetails;i++)
      {
         if(!DownloadSymbol_socket (sDetails[i], eWhichTF, 1, sText))
         {
            sText = "NA";
         }
         if(i==1)sStatus = sText;
         else sStatus = sStatus + SUB_REQUEST_DIVISOR + sText;
      }
      return(1);
   }else if(sOrdem == "Z1")
   {   
      /////////////////////////////////////////////////////////////////////////
      // Example function
   
      // Check MT5.zExample in mt5R
      // Use "MT5.zExample" into R console to see the code and follow the instructions
   
      string sDetails[];
      int iQtyDetails;
      
      StructureOrders(sSubOrdem, sDetails, iQtyDetails, SUB_REQUEST_DIVISOR);
      
      // We are reciving "Z1 Hello#World"
      // 'Z1' it was already removed
      // In this block we only have "Hello#World"
      // iQtyDetails will tell us how many sub request we have here.
      
      Print("How many subrequests: " + IntegerToString(iQtyDetails)); // two: "Hello", "World"
      
      // And already has been saved into sDetails
      
      Print("First sub request: '" + sDetails[0] + "'");
      Print("Second sub request '" + sDetails[1] + "'");
      
      // We send it back to R with sStatus
      
      sStatus = "Hello " + SUB_REQUEST_DIVISOR + "To" + SUB_REQUEST_DIVISOR + "You " + SUB_REQUEST_DIVISOR + "Too";
      
      // End
      return(1);
    }else if(sOrdem == "P4") 
    {
      /////////////////////////////////////////////////////////////////////////
      // Fetch all symbols
      
      string sSymbol;
      for(int i=0;i<SymbolsTotal(0);i++)
      {  
         sSymbol = SymbolName(i, 0);
         if(i==0)sStatus = sSymbol;
         else sStatus = sStatus + SUB_REQUEST_DIVISOR + sSymbol;
      }
      return (1);
    }else if(sOrdem == "P5") 
    {
      /////////////////////////////////////////////////////////////////////////
      // Check if symbol is in marketwatch   
      
      string sDetails[];
      int iQtyDetails;
      
      StructureOrders(sSubOrdem, sDetails, iQtyDetails, SUB_REQUEST_DIVISOR);
      
      string sSymbol = sDetails[0];
      
      for(int i=0;i<SymbolsTotal(1);i++)
      {  
         if(SymbolName(i, 1) == sSymbol)
         {
            sStatus = "P5OK1";
            return(1);
         }
      }
      
      sStatus = "P5OK2";
      return(1);
    }else if(sOrdem == "S3") 
    {
      /////////////////////////////////////////////////////////////////////////
      // Check if symbol is in marketwatch   
      
      sStatus = sVersion;
      return(1);
    }else if(sOrdem == "M6") 
    {
      /////////////////////////////////////////////////////////////////////////
      // Return when symbol expiration date (future, options, etc) 
      
      string sDetails[];
      int iQtyDetails;
      
      StructureOrders(sSubOrdem, sDetails, iQtyDetails, SUB_REQUEST_DIVISOR);
      
      string sSymbol = sDetails[0];
      string sReturn;
      
      if(!SymbolExists(sSymbol))
      {
        sStatus = "M6ERROR";
        return(1);
      }
      
      MqlDateTime mql_date;
      datetime dt = SymbolInfoInteger(sSymbol , SYMBOL_EXPIRATION_TIME);
      TimeToStruct(dt, mql_date);
      if(mql_date.year == 1970)
      {
         sStatus = "0";
         return(1);
      }
      
      sStatus = TimeToString(dt, TIME_DATE);
      return(1);
    }else if(sOrdem == "M7") 
    {
      /////////////////////////////////////////////////////////////////////////
      // Returns MT5 server time
      
      MqlDateTime mql_date;
      datetime dt = TimeCurrent();
      TimeToStruct(dt, mql_date);
      
      sStatus = IntegerToString(mql_date.year) + SUB_REQUEST_DIVISOR + IntegerToString(mql_date.mon) + SUB_REQUEST_DIVISOR + IntegerToString(mql_date.day) + SUB_REQUEST_DIVISOR +
                IntegerToString(mql_date.hour) + SUB_REQUEST_DIVISOR + IntegerToString(mql_date.min) + SUB_REQUEST_DIVISOR + IntegerToString(mql_date.sec);
      return(1);
      
    }else if(sOrdem == "P6")
    {   
      /////////////////////////////////////////////////////////////////////////
      // Get Time & Sales
      
      string sDetalhes[];
      int iQtdDetalhes;
      
      StructureOrders(sSubOrdem, sDetalhes, iQtdDetalhes, SUB_REQUEST_DIVISOR);
      
      string sSymbol = sDetalhes[0]; 
      int iRows = StringToInteger(sDetalhes[1]); 
      
      if(!SymbolSelect(sSymbol, true))
      {
         sStatus = "P6ERROR2";
         return(1);
      }
      
      // Using MetaQuotes code
      int     attempts = 0;     // Count of attempts 
      bool    success = false;  // The flag of a successful copying of ticks 
      MqlTick tick_array[];   // Tick receiving array 
   
      while(attempts<3) 
      { 
         uint start = GetTickCount(); 
         int received = CopyTicks(sSymbol,tick_array,COPY_TICKS_TRADE, 0, iRows); 
         if(received!=-1) 
         { 
            PrintFormat("%s: received %d ticks in %d ms", sSymbol, received,GetTickCount()); 
            if(GetLastError()==0) 
            { 
               success=true; 
               break; 
            } 
            else PrintFormat("%s: Ticks are not synchronized yet, %d ticks received for %d ms. Error=%d", sSymbol ,received,GetTickCount()-start,_LastError); 
         } 
           
         attempts++; 
         Sleep(100); 
      } 
   
      if(!success) 
      { 
         PrintFormat("Error! Failed to receive %d ticks of %s in three attempts", iRows, sSymbol); 
         sStatus = "P6ERROR";
         return(1);
      } 
      
      int ticks = ArraySize(tick_array); 
      int counter=0; 
      string sText, sTextComplete = "";
      bool bAlreadyStarted = false;
      for(int i=0;i<ticks;i++) 
      { 
         //datetime time=tick_array[i].time; 
         //counter++; 
         //PrintFormat("%d. %s",counter,GetTickDescription(tick_array[i])); 
         sText = GetTickDescription(tick_array[i]);
         if(sText == "")continue;
         if(!bAlreadyStarted)
         {
            sTextComplete = sText; //Start
            bAlreadyStarted = true;
         }else sTextComplete = sTextComplete + SUB_REQUEST_DIVISOR + sText;
      } 
      sStatus = sTextComplete; 
      
      if(sStatus == "") 
      { 
         Print("Error! This symbol maybe there is no Times & Sales table");
         sStatus = "P6ERROR3";
         return(1);
      } 
      
      return(1);
    }
   
   return(1);
}

// --------------------------------------------------------------------
// Initialisation - set up server socket
// --------------------------------------------------------------------

void OnInit()
{
   Comment("mt5R platform");
   Print("mt5R platform initiated. Version: " + sVersion + " " + sDateVersion);
  
   // If the EA is being reloaded, e.g. because of change of timeframe,
   // then we may already have done all the setup. See the 
   // termination code in OnDeinit.
   if (glbServerSocket) {
      Print("Reloading EA with existing server socket");
   } else {
      // Create the server socket
      glbServerSocket = new ServerSocket(ServerPort, false);
      if (glbServerSocket.Created()) {
         Print("Server socket created");
   
         // Note: this can fail if MT4/5 starts up
         // with the EA already attached to a chart. Therefore,
         // we repeat in OnTick()
         glbCreatedTimer = EventSetMillisecondTimer(TIMER_FREQUENCY_MS);
      } else {
         Print("Server socket FAILED - is the port already in use?");
      }
   }
}


// --------------------------------------------------------------------
// Termination - free server socket and any clients
// --------------------------------------------------------------------

void OnDeinit(const int reason)
{
   switch (reason) {
      case REASON_CHARTCHANGE:
         // Keep the server socket and all its clients if 
         // the EA is going to be reloaded because of a 
         // change to chart symbol or timeframe 
         break;
         
      default:
         // For any other unload of the EA, delete the 
         // server socket and all the clients 
         glbCreatedTimer = false;
         
         // Delete all clients currently connected
         for (int i = 0; i < ArraySize(glbClients); i++) {
            delete glbClients[i];
         }
         ArrayResize(glbClients, 0);
      
         // Free the server socket. *VERY* important, or else
         // the port number remains in use and un-reusable until
         // MT4/5 is shut down
         delete glbServerSocket;
         glbServerSocket = NULL;
         Print("Server socket terminated");
         break;
   }
}


// --------------------------------------------------------------------
// Timer - accept new connections, and handle incoming data from clients.
// Secondary to the event-driven handling via OnChartEvent(). Most
// socket events should be picked up faster through OnChartEvent()
// rather than being first detected in OnTimer()
// --------------------------------------------------------------------

void OnTimer()
{
   // Accept any new pending connections
   AcceptNewConnections();
   
   // Process any incoming data on each client socket,
   // bearing in mind that HandleSocketIncomingData()
   // can delete sockets and reduce the size of the array
   // if a socket has been closed

   for (int i = ArraySize(glbClients) - 1; i >= 0; i--) {
      HandleSocketIncomingData(i);
   }
}


// --------------------------------------------------------------------
// Accepts new connections on the server socket, creating new
// entries in the glbClients[] array
// --------------------------------------------------------------------

void AcceptNewConnections()
{
   // Keep accepting any pending connections until Accept() returns NULL
   ClientSocket * pNewClient = NULL;
   do {
      pNewClient = glbServerSocket.Accept();
      if (pNewClient != NULL) {
         int sz = ArraySize(glbClients);
         ArrayResize(glbClients, sz + 1);
         glbClients[sz] = pNewClient;
         Print("New client connection");
         
         //strCommand = pNewClient.Receive("\r\n");
         //Print("TEMEU '"+strCommand+"'");
         
         //pNewClient.Send("Hello\r\n");
      }
      
   } while (pNewClient != NULL);
}



// --------------------------------------------------------------------
// Handles any new incoming data on a client socket, identified
// by its index within the glbClients[] array. This function
// deletes the ClientSocket object, and restructures the array,
// if the socket has been closed by the client
// --------------------------------------------------------------------

void HandleSocketIncomingData(int idxClient)
{
   ClientSocket * pClient = glbClients[idxClient];

   int iQuantidadeDeOrdens = 1, iMandarMensagemDeVolta = 0, iOrdem, iQualOrdem = 0;
   string sLeitura, sOrdens[], sOrdem, sStatus, sResposta = "";
   
   do
   {
      sLeitura = pClient.Receive("\r\n");
      if(sLeitura == "")
      {
         continue;
      }else
      {
         PrintFormat("Reading: '%s'", sLeitura);
         if(StringFind(sLeitura, REQUEST_DIVISOR, 0) != -1)//Verify existence of @: more than 1 order
         {
            StructureOrders(sLeitura, sOrdens, iQuantidadeDeOrdens, REQUEST_DIVISOR);
            sOrdem = sOrdens[iQualOrdem];//careful here
         }
         else // only one
         {
            sOrdem = sLeitura;
         }
         
         PrintFormat("requests: %d", iQuantidadeDeOrdens);
         
         Print("+++++++++++++++++++++++");
         while(iQuantidadeDeOrdens>0)
         {
            iOrdem = ExecuteStackRequests(sOrdem, sStatus);
            if(iOrdem>0)
            {
               if(StringLen(sStatus)>0)//it has answer to give
               {
                  if(iMandarMensagemDeVolta==0)
                     sResposta = sStatus;
                  else 
                     sResposta = sResposta+REQUEST_DIVISOR+sStatus;
                     
                  iMandarMensagemDeVolta++;  
                  sStatus="";
               }
            }else if(iOrdem<0)
            {
               Print("Erro iOrdem<0");
               sResposta = "ERRO";
            }

            iQuantidadeDeOrdens--;
            if(iQuantidadeDeOrdens>0)
            {
               sOrdem = sOrdens[++iQualOrdem];
            }     
         }
         Print(sResposta);
         pClient.Send(sResposta + "\r\n");
      }
      
      
   }while (sLeitura != "");   
   

   // If the socket has been closed, or the client has sent a close message,
   // release the socket and shuffle the glbClients[] array
   if (!pClient.IsSocketConnected()) {
      Print("Client has disconnected");

      // Client is dead. Destroy the object
      delete pClient;
      
      // And remove from the array
      int ctClients = ArraySize(glbClients);
      for (int i = idxClient + 1; i < ctClients; i++) {
         glbClients[i - 1] = glbClients[i];
      }
      ctClients--;
      ArrayResize(glbClients, ctClients);
   }
}


// --------------------------------------------------------------------
// Use OnTick() to watch for failure to create the timer in OnInit()
// --------------------------------------------------------------------

void OnTick()
{
   if (!glbCreatedTimer) glbCreatedTimer = EventSetMillisecondTimer(TIMER_FREQUENCY_MS);
}

// --------------------------------------------------------------------
// Event-driven functionality, turned on by #defining SOCKET_LIBRARY_USE_EVENTS
// before including the socket library. This generates dummy key-down
// messages when socket activity occurs, with lparam being the 
// .GetSocketHandle()
// --------------------------------------------------------------------

void OnChartEvent(const int id, const long& lparam, const double& dparam, const string& sparam)
{
   if (id == CHARTEVENT_KEYDOWN) {
      // If the lparam matches a .GetSocketHandle(), then it's a dummy
      // key press indicating that there's socket activity. Otherwise,
      // it's a real key press
         
      if (lparam == glbServerSocket.GetSocketHandle()) {
         // Activity on server socket. Accept new connections
         Print("New server socket event - incoming connection");
         AcceptNewConnections();

      } else {
         // Compare lparam to each client socket handle
         for (int i = 0; i < ArraySize(glbClients); i++) {
            if (lparam == glbClients[i].GetSocketHandle()) {
               HandleSocketIncomingData(i);
               return; // Early exit
            }
         }
         
         // If we get here, then the key press does not seem
         // to match any socket, and appears to be a real
         // key press event...
      }
   }
}
