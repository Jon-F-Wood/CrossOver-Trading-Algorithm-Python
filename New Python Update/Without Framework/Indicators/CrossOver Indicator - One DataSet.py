'''
All of this code would run bar by bar and plot information on the graph 
based on TS framework mode of interpretation

2 Excel Spreadsheets/ arrays and BarsBack is an array holding that information needed for the highest numbered indicator on the user input settings



'''
#Plot all Setups even when in the Market.  1/On : 0/Off
	ShowMaxBarsBack = 0
		
#Variables:
	_JL1 = 0 				   #JumpLine1 (Tenkan-Sen)
	_JL2 = 0 				   #JumpLine2	(Tenkan-Sen)
	_TrailingJL = 0			   #JumpLine used for trailing
		
	TheEntryPriceS = 0		   #Holds the Entry Price on Currently active Short Orders	
	TheEntryPriceL = 0		   #Holds the Entry Price on Currently active Long Orders	
	
	TheStopPriceS = 0		   #Holds the Stop Price on Currently active Short Orders
	TheStopPriceL = 0	       #Holds the Stop Price on Currently active Long Orders
	
	TheBreakevenTgtS = 0	   #Holds the Breakeven Target Price on Currently active Short Orders	
	TheBreakevenTgtL = 0	   #Holds the Breakeven Target Price on Currently active Long Orders	
	
	TheTrailingTgtS = 0		   #Holds the Trialing Target Price on Currently active Short Orders
	TheTrailingTgtL = 0		   #Holds the Trialing Target Price on Currently active Long Orders
		
	TheTrailingPriceS = 0	   #Holds the Price that the Trailing Stop Should be Placed on Short Orders
	TheTrailingPriceL = 0	   #Holds the Price that the Trailing Stop Should be Placed on Long Orders
	
	TheTargetPriceS = 0		   #Holds the Target Price on Currently active Short Orders
	TheTargetPriceL = 0		   #Holds the Target Price on Currently active Long Orders
	
	PipsRiskS = 0
	PipsRiskL = 0
	
	MyJLCD = 0
	JLCDAvg = 0
	JLCDDiff = 0
	
#Variables used to Tell use what MaxBarsBack needs to be set to	
	Counting =False
	Counter = 0
	NumBarsJLsEqual = 0
	MaxBarsJLsEqual = 0
	
#Conditional Variables that Hold thier value until changed by a condition	
	ASetupIsActiveS = False 	 #This Records if a Short Setup has been Placed or if has been Entered or if it has been cancled
	ASetupIsActiveL = False 	 #This Records if a Long Setup has been Placed or if has been Entered or if it has been cancled
	
	StopIsAtBrkEvnS = False      #This Records if a Short Position's Stop is Currenly at Breakeven
	StopIsAtBrkEvnL = False      #This Records if a Long Position's Stop is Currenly at Breakeven
	
	TrailingIsOnS = False		 #The Short Trailing Tgt Has been hit
	TrailingIsOnL = False		 #The Long Trailing Tgt Has been hit
	
	NowTrailingS = False  	     #Short Position's Stop is Now Trailing
	NowTrailingL = False  	     #Long Position's Stop is Now Trailing
	
#Conditional Variables that are evaluated bar by bar		
	RedBar = False 			     #Is the Current Bar an Down(Red) Bar
	GreenBar = False 			 #Is the Current Bar an Up(Green) Bar	
	
	CloseLessThanJL2 = False     #The Close price of the Current Bar is Lower Than the JL2 Value
	CloseHigherThanJL2 = False   #The Close price of the Current Bar is Higher Than the JL2 Value

	JL1CrossedOverJL2 = False	 #Shows there is a Cross Over and no setup has been activated 
	JL1CrossedUnderJL2 = False	 #Shows there is a Cross Under and no setup has been activated
	
	HasNotEnteredYetS = False    #The Low of the Current Bar Is Higher Than the Currently Active Short Position's Entry Price (It hasn't Entered Yet)
	HasNotEnteredYetL = False    #The High of the Current Bar Is Less Than the Currently Active Long Position's Entry Price (It hasn't Entered Yet)	
	
	HasYetToHitStopS = False     #The High of the Current Bar is Lower than the Currently Active Short Position's Stop Price (It hasn't Stopped Out Yet)
	HasYetToHitStopL = False     #The Low of the Current Bar is Higher than the Currently Active Long Position's Stop Price (It hasn't Stopped Out Yet)
	
	HasYetToHitBrkEvnS = False	 #The Low Of the Current Bar is Higher than the Currently Acive Short Position's Breakeven Target (BrkEvn Tgt has yet to be Hit)
	HasYetToHitBrkEvnL = False	 #The High Of the Current Bar is Lower than the Currently Acive Long Position's Breakeven Target (BrkEvn Tgt has yet to be Hit)
	
	HasYetToHitTrialingS = False #The Low Of the Current Bar is Higher than the Currently Acive Short Position's Trailing Target (Trailing Tgt has yet to be Hit)
	HasYetToHitTrialingL = False #The High Of the Current Bar is Lower than the Currently Acive Long Position's Trailing Target (Trailing Tgt has yet to be Hit)
	
	HasYetToHitTargetS = False   #The Low Of the Current Bar is Higher than the Currently Acive Short Position's Target Price (It hasn't Hit Target Yet)
	HasYetToHitTargetL = False   #The High Of the Current Bar is Lower than the Currently Acive Long Position's Target Price (It hasn't Hit Target Yet) r
 	
 	CurrentlyInMarketS = False #Used to tell whether or not the system is currently in a Short position or not
 	CurrentlyInMarketL = False #Used to tell whether or not the system is currently in a Long position or not
 
 	StageOrder = False	
#Change PlotAddons from True/False input to On/Off input (1/On : 0/Off) 
	_PlotAddons = True      #Last Declaration of a Variable 


#Inputs:  	
	JL1 = 39		   	 	  #Length of JumpLine 1 (Typically is JL1 < JL2)
	JL2 = 10 			      #Length of JumpLine 2 (Typically is JL2 > JL1)
	CloseCancelsCross = 1	  #A filter that if activated cancels a trade if the price closes in the oposite direction of the trade's side of JL2. 1/On : 0/Off 	
	UseJLCDFilter = 0 
	JLCDLength = 7
	TargetLength = 4.882 	  #High + ((High - Low) * Tgt) = The Price that the Target is Placed
	BreakevenTarget = 1.37    #High + ((High - Low) * BreakevenTarget) = The Price Where the StopLoss is moved up to Breakeven
	TrailingJL = 11		   	  #JL used for Trailing
	TrailingTarget = 1.12     #The Point at which the trade begins to trail
	TrailingOffSetTics = 2    #How Many ticks Below the MA the Stop is Trailed	
	EntryOffsetTics = 13      #High + (EntryOffsetTics/PriceScale) = the Price where the Entry is Placed
	StopOffsetTics = -4       #Low - (StopOffsetTIcs/PriceScale) = The Price where the StopLoss is Placed	
	UseRiskFilter = 1		  #Used to Turn on and Off the Risk Filter.  1/On : 0/Off
	MaxTicsRisk = 790		  #Maximum tics risk for a trade to be considered valid
	MinTicsRisk = 120		  #Minimum tics risk for a trade to be considered valid
	PlotAddons = True     

	bar_back = max(JL1,JL2,JLCDLength,TrailingJL)
	'''
	Loop through all data in multiples of 6 {i = (i+1)*6}
		push data onto respective arrays
			(push i onto arr_O,  i+1 onto arr_H, i+2 onto arr_L etc)
		if O length > bars_back
			take off first item in EVERY array
		
		if i/6 > bars_back and i + 1 is a multiple of 6 then
			CO_Indicator(arr_O, arr_H, arr_L,arr_C, arr_Date, arr_Time)
				print to an excel file
	'''
#Overall Functions
def Highest (price, length):
	max(price[-length:])
def Lowest (price, length):
	min(price[-length:])

def CO_Indicator (arr_O, arr_H, arr_L, arr_C, arr_Date, arr_Time):
	O = arr_O[-1]
	H = arr_H[-1]
	L = arr_L[-1]
	C = arr_C[-1]
	Date = arr_Date[-1]
	Time = arr_Time[-1]
	#Push to excell file O,H,L,C,Date,Time

	#JLs	
	_JL1 = (Highest(H, JL1) + Lowest(L, JL1))/2 
	_JL2 = (Highest(H, JL2) + Lowest(L, JL2))/2  
	_TrailingJL = (Highest(H3, TrailingJL) + Lowest(L3, TrailingJL))/2  

	#Push to excell file _JL1,_JL2,_TrailingJL

	'''
	This Section is used to tell the user what to set MaxBarsBack to 
	by displaying a number in the print log that should be rounded 
	up to nearest hundred which is what MaxBarsBack should be set to.
	''' 
	Array:
		_NumBarsJLsEqual[](0)

	Array_setmaxindex(_NumBarsJLsEqual,10000)
		
	if (_JL1[1] <> _JL2[1]) and (_JL1 = _JL2)then
		Counting = True
	else if (_JL1[1] = _JL2[1]) and (_JL1 <> _JL2) then
		Counting = False	
		
	if Counting then
		Begin
			NumBarsJLsEqual = NumBarsJLsEqual + 1
		End
	else
		Begin		
			if Counting[1] = True and Counting = False then
				Begin				
					_NumBarsJLsEqual[Counter] = NumBarsJLsEqual 
					Counter = Counter + 1	
					NumBarsJLsEqual = 0
				End
		End	

	if LastBarOnChart then
		Begin	
			if ShowMaxBarsBack = 1 then
				Begin
					ClearPrintLog
					MaxBarsJLsEqual = HighestArray(_NumBarsJLsEqual, Counter)
					Print("Max Bars in a row that JL are Equal:  ",MaxBarsJLsEqual:5:0)
				End	
		End

	if CurrentlyInMarketL = True and DayofWeek(Date) = Friday and Time = 1500 then
		Plot12(Close,"Exit", Magenta)
	if CurrentlyInMarkets = True and DayofWeek(Date) = Friday and Time = 1500 then
		Plot12(Close of Data2,"Exit", Magenta)
		
	if DayofWeek(Date) = Friday and Time >= 1500 then
		Begin
			CurrentlyInMarketL = False 
			CurrentlyInMarketS = False
			ASetupIsActiveS = False
			ASetupIsActiveL = False
			JL1CrossedUnderJL2 = False
			JL1CrossedOverJL2 = False
		End
	else if (DayofWeek(Date) > Sunday) or (DayofWeek(Date) = Sunday and Time >= 1800) or (DayofWeek(Date) = Friday and Time < 1500) then	
		Begin#End of Code
				
	#Set the Trailing Price
	TheTrailingPriceS = _TrailingJL + (TrailingOffSetTics/PriceScale)
	TheTrailingPriceL = _TrailingJL - (TrailingOffSetTics/PriceScale)

	#Conditions
	RedBar = Close of Data3 < Open of Data3
	GreenBar = Close of Data3 > Open of Data3

	CloseLessThanJL2 = Close of Data3 < _JL2
	CloseHigherThanJL2 = Close of Data3 > _JL2

	if CrossOver(_JL1,_JL2,Maxbarsback) then
		Begin	
			JL1CrossedOverJL2 = True
			JL1CrossedUnderJL2 = False		
		End	
	else if CrossUnder(_JL1,_JL2,Maxbarsback) then
		Begin	
			JL1CrossedOverJL2 = False
			JL1CrossedUnderJL2 = True
		End
		
	HasNotEnteredYetS = Low > TheEntryPriceS
	HasYetToHitStopS = High < TheStopPriceS
	HasYetToHitTargetS = Low > TheTargetPriceS
	HasYetToHitBrkEvnS = Low > TheBreakevenTgtS
	HasYetToHitTrialingS = Low > TheTrailingTgtS

	HasNotEnteredYetL = High < TheEntryPriceL
	HasYetToHitStopL = Low > TheStopPriceL
	HasYetToHitTargetL = High < TheTargetPriceL
	HasYetToHitBrkEvnL = High < TheBreakevenTgtL
	HasYetToHitTrialingL = High < TheTrailingTgtL

	if CurrentlyInMarketL = False and CurrentlyInMarketS = False and 
	(CurrentlyInMarketL[1] = True or CurrentlyInMarketS[1] = True) then	
		Begin
			JL1CrossedOverJL2 = False
			JL1CrossedUnderJL2 = False
		End
		
	#Close Cancels Cross
	if CloseCancelsCross = 1 then
		Begin
			if ASetupIsActiveS and Not ASetupIsActiveL and CloseHigherThanJL2 then
				ASetupIsActiveS = False
			if ASetupIsActiveL and Not ASetupIsActiveS and CloseLessThanJL2 then
				ASetupIsActiveL = False	
		End

	if UseJLCDFilter = 1 then
		Begin
			MyJLCD = JLCD(JL1, JL2)
			JLCDAvg = (Highest(MyJLCD, JLCDLength) + Lowest(MyJLCD, JLCDLength))/2 
			JLCDDiff = MyJLCD - JLCDAvg
		End
				
	#Short ENTRY
	if ASetupIsActiveS and Not ASetupIsActiveL then
		Begin
			if HasNotEnteredYetS then
				Begin
					#Cancled?
					if JL1CrossedOverJL2 = False then
						Begin
							Plot8(TheEntryPriceS, "Entry", Cyan)
						End	
					else
						Begin
							ASetupIsActiveS = False
						End	
				End
			else
				#if the setup has entered then... 
				Begin				
					CurrentlyInMarketS = True
					ASetupIsActiveS = False													
				End		
		End	

	#Long ENTRY
	if ASetupIsActiveL and Not ASetupIsActiveS then
		Begin
			if HasNotEnteredYetL then
				Begin
					#Cancled?
					if JL1CrossedUnderJL2 = False then
						Begin
							Plot8(TheEntryPriceL, "Entry", Cyan)
						End	
					else
						Begin
							ASetupIsActiveL = False
						End	
				End
			else
				#if the setup has entered then... 
				Begin				
					CurrentlyInMarketL = True
					ASetupIsActiveL = False													
				End		
		End
		
	#Short STOPLOSS	
	if ASetupIsActiveS or CurrentlyInMarketS and ( Not ASetupIsActiveL or Not CurrentlyInMarketL ) then
		Begin	
		#if There is a trade that has entered...	
			if CurrentlyInMarketS and Not CurrentlyInMarketL then		
				Begin		
				#Evaluate if Stop has been Hit	
					if HasYetToHitStopS = False then
						Begin
							CurrentlyInMarketS = False	
							StopIsAtBrkEvnS = False						
							NowTrailingS = False
							
						#Is the Trade A Breakeven Or Trailing	
							if TheStopPriceS <= TheEntryPriceS then 
								Begin		
								#Gapping?	
									if Open > TheStopPriceS then
										Begin									
											if TheStopPriceS = TheTrailingPriceS then
												SetPlotColor(12,Rgb(0,0,170))
											else
												SetPlotColor(12,Yellow)
												
										#Exit at Open		
											Plot12(Open, "Exit")
										End
									else
									#No Gapping	
										Begin	
											if TheStopPriceS = TheTrailingPriceS then
												SetPlotColor(12,Rgb(0,0,170))
											else
												SetPlotColor(12,Yellow)
												
											Plot12(TheStopPriceS, "Exit")
										End
								End
						#Fixed Stop	
							else
								Begin
								#Gapping?	
									if Open > TheStopPriceS then
										Begin
											if StopIsAtBrkEvnS = False then								
												SetPlotColor(12,Rgb(166,0,0))												
										
										#Exit at Open	
											Plot12(Open, "Exit")
										End
									else
									#No Gapping	
										Begin
											if StopIsAtBrkEvnS = False then								
												SetPlotColor(12,Rgb(166,0,0))	
												
											Plot12(TheStopPriceS, "Exit")
										End		
								End	
						End		
				End
		
		#Breakeven and Trailing Stop	
			if CurrentlyInMarketS and Not CurrentlyInMarketL then		
				Begin	
				#Breakeven
					#Evaluate if Breakeven Target has been hit
					if HasYetToHitBrkEvnS = False then
						Begin	
							TheStopPriceS = (TheEntryPriceS - Spread(60)-(10/Pricescale))
						#Does the bar hit Breakeven Target then get stopped out on the Same Bar?	
							if Close >= TheStopPriceS then
								Begin
									CurrentlyInMarketS = False
									SetPlotColor(12,Yellow)
									Plot12(TheStopPriceS, "Exit")
									StopIsAtBrkEvnS = False						
									NowTrailingS = False	
								End
							else
								Begin							
									StopIsAtBrkEvnS = True	
								End
						End		
						
					if StopIsAtBrkEvnS and NowTrailingS = False then
						Begin
							TheStopPriceS = (TheEntryPriceS - Spread(60)-(10/Pricescale))
						End
						
				#Trailing	
					#Evaluate if Trailing Target has been hit
					if HasYetToHitTrialingS = False then
						TrailingIsOnS = True
									
					if (TheTrailingPriceS < (TheEntryPriceS - Spread(20))) and TrailingIsOnS  = True then					
						NowTrailingS = True	
					
					if NowTrailingS and TheTrailingPriceS > TheTrailingPriceS[1] then
						TheTrailingPriceS = TheTrailingPriceS[1]		
										
					if NowTrailingS = True and TheTrailingPriceS < TheEntryPriceS and TheTrailingPriceS < TheStopPriceS then
						Begin
							if Close < TheTrailingPriceS then
								TheStopPriceS = TheTrailingPriceS
							else
								TheStopPriceS = TheStopPriceS[1]
						End					
				End
				
		#Plot Stop a long as the Target hasn't been hit yet
			if HasYetToHitTargetS and Not CurrentlyInMarketL then
				Begin
					if ASetupIsActiveS or CurrentlyInMarketS = True then
					Plot9 (TheStopPriceS, "Stop", Cyan)
				End
		End

	#Long STOPLOSS	
	if ASetupIsActiveL or CurrentlyInMarketL and ( Not ASetupIsActiveS or Not CurrentlyInMarketS ) then
		Begin	
		#if There is a trade that has entered...	
			if CurrentlyInMarketL and Not CurrentlyInMarketS then		
				Begin		
				#Evaluate if Stop has been Hit	
					if HasYetToHitStopL = False then
						Begin
							CurrentlyInMarketL = False	
							StopIsAtBrkEvnL = False						
							NowTrailingL = False
											
						#Is the Trade A Breakeven Or Trailing?	
							if TheStopPriceL >= TheEntryPriceL then 
								Begin
								#Gapping?	
									if Open < TheStopPriceL then
										Begin	
											if TheStopPriceL = TheTrailingPriceL then
												SetPlotColor(12,Rgb(0,0,170))
											else
												SetPlotColor(12,Yellow)
												
										#if so Exit at the Open of the next bar		
											Plot12(Open, "Exit")
										End
									else
									#No Gapping	
										Begin
											if TheStopPriceL = TheTrailingPriceL then
												SetPlotColor(12,Rgb(0,0,170))
											else
												SetPlotColor(12,Yellow)
												
										#if so Exit at the Open of the next bar		
											Plot12(TheStopPriceL, "Exit")
										End
								End		
						#Fixed Stop 	
							else
								Begin
								#Gapping?	
									if Open < TheStopPriceL Then
										Begin				
											if StopIsAtBrkEvnL = False then								
												SetPlotColor(12,Rgb(166,0,0))
												
											Plot12(Open, "Exit")
										End
									else
									#No Gapping	
										Begin
											if StopIsAtBrkEvnL = False then								
												SetPlotColor(12,Rgb(166,0,0))
												
											Plot12(TheStopPriceL, "Exit")
										End		
								End	
						End		
				End
		#Breakeven and Trailing Stop	
			if CurrentlyInMarketL and Not CurrentlyInMarketS then		
				Begin	
				#Breakeven
					#Evaluate if Breakeven Target has been hit
					if HasYetToHitBrkEvnL = False then
						Begin	
							TheStopPriceL = (TheEntryPriceL + Spread(20)+(10/Pricescale))
						#Does the bar hit Breakeven Target then get stopped out on the Same Bar?	
							if Close <= TheStopPriceL then
								Begin
									CurrentlyInMarketL = False
									SetPlotColor(12,Yellow)
									Plot12(TheStopPriceL, "Exit")
									StopIsAtBrkEvnL = False						
									NowTrailingL = False	
								End
							else
								Begin							
									StopIsAtBrkEvnL = True	
								End
						End
					
					if StopIsAtBrkEvnL and NowTrailingL = False then
						Begin
							TheStopPriceL = (TheEntryPriceL + Spread(20)+(10/Pricescale))
						End			
						
				#Trailing	
				#Evaluate if Trailing Target has been hit				
					if HasYetToHitTrialingL = False then
						TrailingIsOnL = True
									
					if (TheTrailingPriceL > (TheEntryPriceL + Spread(20))) and TrailingIsOnL = True then					
						NowTrailingL = True								
					
					if NowTrailingL and TheTrailingPriceL < TheTrailingPriceL[1] then
						TheTrailingPriceL = TheTrailingPriceL[1]
						
					if NowTrailingL and TheTrailingPriceL > TheEntryPriceL and TheTrailingPriceL > TheStopPriceL then
						Begin		
							if Close > TheTrailingPriceL then
								TheStopPriceL = TheTrailingPriceL
							else
								TheStopPriceL = TheStopPriceL[1]
						End						
				End
				
		#Plot Stop a long as the Target hasn't been hit yet
			if HasYetToHitTargetL and Not CurrentlyInMarketS then
				Begin
					if ASetupIsActiveL or CurrentlyInMarketL = True then
						Plot9(TheStopPriceL, "Stop", Cyan)
				End
		End


	#Short TARGET
	if CurrentlyInMarketS = True and Not CurrentlyInMarketL then
		Begin
			if HasYetToHitTargetS = False then
				Begin
				#Gapping	
					if Open of Data2 < TheTargetPriceS then
						Begin
							CurrentlyInMarketS = False				
							Plot12(Open of Data2,"Exit", DarkGreen)
							StopIsAtBrkEvnS = False
							NowTrailingS = False
						End
					else
					#No Gapping	
						Begin	
							CurrentlyInMarketS = False				
							Plot12(TheTargetPriceS,"Exit", DarkGreen)
							StopIsAtBrkEvnS = False
							NowTrailingS = False
						End	
				End
		End		

	#Long TARGET
	if CurrentlyInMarketL = True and Not CurrentlyInMarketS then
		Begin
			if HasYetToHitTargetL = False then
				Begin
				#Gapping	
					if Open > TheTargetPriceL then
						Begin
							CurrentlyInMarketL = False				
							Plot12(Open,"Exit", DarkGreen)
							StopIsAtBrkEvnL = False
							NowTrailingL = False
						End
					else
					#No Gapping	
						Begin	
							CurrentlyInMarketL = False				
							Plot12(TheTargetPriceL,"Exit", DarkGreen)
							StopIsAtBrkEvnL = False
							NowTrailingL = False
						End	
				End
		End	
		
	#Looks for a New Short Position	
	if JL1CrossedUnderJL2 and RedBar and CloseLessThanJL2 and CurrentlyInMarketS = False and CurrentlyInMarketL = False and ASetupIsActiveL = False and ASetupIsActiveS = False then 
		Begin
		#Reset Setting	
			JL1CrossedUnderJL2 = False	
			ASetupIsActiveS = True	
			StopIsAtBrkEvnS = False
			TrailingIsOnS = False
			NowTrailingS = False
			StageOrder = True
			
		#Set values and Plot the point							
			TheTargetPriceS = L3 - ((High of Data4 - L3) * TargetLength)     #Target				
			TheTrailingTgtS = L3 - ((High of Data4 - L3) * TrailingTarget)   #Trailing Target
			TheBreakevenTgtS = L3 - ((High of Data4 - L3) * BreakevenTarget) #Breakeven Target	
			TheEntryPriceS = L3 - (EntryOffsetTics/PriceScale)   	  		  		  #Entry 
			TheStopPriceS = High of Data4  + (StopOffsetTics/PriceScale)     	   				  #Stop	
							
			if TheBreakevenTgtS > (TheEntryPriceS - Spread(5)) or TheTrailingTgtS > (TheEntryPriceS - Spread(5)) then
				Begin
					StageOrder = False	
					ASetupIsActiveS = False
				End			
									
			PipsRiskS = ((TheStopPriceS - TheEntryPriceS) + Spread(20) + (20/Pricescale))*(PriceScale/10)
			
			if (UseRiskFilter = 1 and ((PipsRiskS*10) < MinTicsRisk) or ((PipsRiskS*10) > MaxTicsRisk)) or (UseJLCDFilter = 1 and JLCDDiff > 0)  then
				Begin
					ASetupIsActiveS = False
					StageOrder = False	
				End
				
			if StageOrder then
				Begin
					Plot5(TheTargetPriceS, "Target", Cyan)
					Plot6(TheTrailingTgtS, "TrailTgt", Cyan)				
					Plot7(TheBreakevenTgtS, "BrkEvnTgt", Cyan)
					Plot8(TheEntryPriceS, "Entry", Cyan)
					Plot9(TheStopPriceS, "Stop", Cyan)	
					Plot14(PipsRiskS,"Pips Risk ", Cyan)
					Plot15(((TheEntryPriceS - TheTargetPriceS + Spread(20))/PipsRiskS)*(Pricescale/10"R:R ", Cyan)	
					StageOrder = False
				End	
		End		

	#Looks for a New Long Position	
	if JL1CrossedOverJL2 and CloseHigherThanJL2 and GreenBar and CurrentlyInMarketL = False and CurrentlyInMarketS = False and ASetupIsActiveL = False and ASetupIsActiveS = False then 
		Begin
		#Reset Setting		
			JL1CrossedOverJL2 = False		
			ASetupIsActiveL = True	
			StopIsAtBrkEvnL = False
			TrailingIsOnL = False
			NowTrailingL = False
			StageOrder = True		
			
		#Set values and Plot the point
			TheTargetPriceL = High of Data4 + ((High of Data4 - L3) * TargetLength)     #Target
			TheTrailingTgtL = High of Data4 + ((High of Data4 - L3) * TrailingTarget)   #Trailing Target
			TheBreakevenTgtL = High of Data4 + ((High of Data4 - L3) * BreakevenTarget) #Breakeven Target
			TheEntryPriceL = High of Data4 + (EntryOffsetTics/PriceScale)   			  		   #Entry 
			TheStopPriceL = L3 - (StopOffsetTics/PriceScale)     	   				   #Stop				
											
			if TheBreakevenTgtL < (TheEntryPriceL + Spread(5)) or TheTrailingTgtL < (TheEntryPriceL + Spread(5)) then
				Begin	
					StageOrder = False
					ASetupIsActiveL = False
				End		
			
			PipsRiskL = ((TheEntryPriceL - TheStopPriceL) + Spread(20) + (20/Pricescale))*(PriceScale/10)		
				
			if (UseRiskFilter = 1 and ((PipsRiskS*10) < MinTicsRisk) or ((PipsRiskS*10) > MaxTicsRisk)) or (UseJLCDFilter = 1 and JLCDDiff < 0)  then
				Begin
					ASetupIsActiveL = False
					StageOrder = False	
				End
					
			if StageOrder then
				Begin
					Plot5(TheTargetPriceL, "Target", Cyan)
					Plot6(TheTrailingTgtL, "TrailTgt", Cyan)	
					Plot7(TheBreakevenTgtL, "BrkEvnTgt", Cyan)					
					Plot8(TheEntryPriceL, "Entry", Cyan)
					Plot9(TheStopPriceL, "Stop", Cyan)	
					Plot14(PipsRiskL, "Pips Risk ", Cyan)
					Plot15(((TheTargetPriceL - TheEntryPriceL + Spread(20))/PipsRiskL)*(Pricescale/10 "R:R ", Cyan)
					StageOrder = False
				End	
		End

	#Addon Trades		
	if JL1CrossedUnderJL2 and RedBar and CloseLessThanJL2 then 
		Begin
		#Stop looking for now
			JL1CrossedUnderJL2 = False
			StageOrder = True
			
		#Plot the point 
			Value1 = L3 - ((High of Data4 - L3) * TargetLength) 				
			Value2 = L3 - ((High of Data4 - L3) * TrailingTarget)							
			Value3 = L3 - ((High of Data4 - L3) * BreakevenTarget)
			Value4 = L3 - (EntryOffsetTics/PriceScale)  
			Value5 = High of Data4 + (StopOffsetTics/PriceScale) 			
				
			if Value1 > Value4 or Value2 > Value4 or Value3 > Value4  then
				StageOrder = False	
			
			if UseRiskFilter = 1 and ((((Value5 - Value4)*PriceScale) < MinTicsRisk) or	(((Value5 - Value4)*PriceScale) > MaxTicsRisk)) then
				StageOrder = False
				
			if _PlotAddons and StageOrder then
				Begin	
					Plot17(Value1, "*Tgt")						
					Plot18(Value2, "*TrailTgt")
					Plot19(Value3, "*BrkEvnTgt")
					Plot20(Value4, "*Entry")
					Plot21(Value5, "*Stop")
					StageOrder = False						
				End
										
		End				

	#Addon Trades		
	if JL1CrossedOverJL2 and CloseHigherThanJL2 and GreenBar then 
		Begin
		#Stop looking for now
			JL1CrossedOverJL2 = False
			StageOrder = True
			
		#Plot the point 
			Value6 = High of Data4 + ((High of Data4 - L3) * TargetLength) 				
			Value7 = High of Data4 + ((High of Data4 - L3) * TrailingTarget)
			Value8 = High of Data4 + ((High of Data4 - L3) * BreakevenTarget)
			Value9 = High of Data4 + (EntryOffsetTics/PriceScale)  
			Value10 = L3 - (StopOffsetTics/PriceScale) 
							
			if Value6 < Value9 or Value7 < Value9 or Value8 < Value9 then
				 StageOrder = False
			
			if UseRiskFilter = 1 and ((((Value9 - Value10)*PriceScale) < MinTicsRisk) or (((Value9 - Value10)*PriceScale) > MaxTicsRisk)) then
				StageOrder = False
			
			if _PlotAddons and StageOrder then
				Begin	
					Plot17(Value6, "*Tgt")
					Plot18(Value7, "*TrailTgt")						
					Plot19(Value8, "*BrkEvnTgt")
					Plot20(Value9, "*Entry")
					Plot21(Value10, "*Stop")
					StageOrder = False						
				End						
		End			

	#Misc	
	if High = 99999999999 then 
		Begin	
			Plot4(0,"=========")
			Plot10(0,"=========")
			Plot13(0,"=========")
			Plot16(0,"=========")
			Plot50(0,"=========")	
			
		End
			
	if ASetupIsActiveL[1] or CurrentlyInMarketL[1] then
		Begin	
			SetPlotColor[1](11, Green)
			Plot11[1]("Long", "Type")
		End
		
	if ASetupIsActiveS[1] or CurrentlyInMarketS[1] then
		Begin	
			SetPlotColor[1](11, Red)
			Plot11[1]("Short", "Type")				
		End	

	End#End of Code	