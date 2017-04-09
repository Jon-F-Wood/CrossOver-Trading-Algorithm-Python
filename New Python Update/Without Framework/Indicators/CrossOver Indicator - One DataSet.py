'''
All of this code would run bar by bar and plot information on the graph 
based on TS framework mode of interpretation

2 Excel Spreadsheets/ arrays and BarsBack is an array holding that information needed for the highest numbered indicator on the user input settings



'''

		
#Variables:
	JL1 = None 				   #JumpLine1 (Tenkan-Sen)
	JL2 = None 				   #JumpLine2	(Tenkan-Sen)
	_TrailingJL = None			   #JumpLine used for trailing
		
	TheEntryPriceS = None		   #Holds the Entry Price on Currently active Short Orders	
	TheEntryPriceL = None		   #Holds the Entry Price on Currently active Long Orders	
	
	TheStopPriceS = None		   #Holds the Stop Price on Currently active Short Orders
	TheStopPriceL = None	       #Holds the Stop Price on Currently active Long Orders
	
	TheBreakevenTgtS = None	   #Holds the Breakeven Target Price on Currently active Short Orders	
	TheBreakevenTgtL = None	   #Holds the Breakeven Target Price on Currently active Long Orders	
	
	TheTrailingTgtS = None		   #Holds the Trailing Target Price on Currently active Short Orders
	TheTrailingTgtL = None		   #Holds the Trailing Target Price on Currently active Long Orders
		
	TheTrailingPriceS = None	   #Holds the Price that the Trailing Stop Should be Placed on Short Orders
	TheTrailingPriceL = None	   #Holds the Price that the Trailing Stop Should be Placed on Long Orders
	
	TheTargetPriceS = None		   #Holds the Target Price on Currently active Short Orders
	TheTargetPriceL = None		   #Holds the Target Price on Currently active Long Orders
	
	PipsRiskS = None
	PipsRiskL = None
	
	MyJLCD = None
	JLCDAvg = None
	JLCDDiff = None
	
#Variables used to Tell use what MaxBarsBack needs to be set to	
	Counting = False
	NumBarsJLsEqual = None
	MaxBarsJLsEqual = None
	
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
	
	HasYetToHitTrailingS = False #The Low Of the Current Bar is Higher than the Currently Acive Short Position's Trailing Target (Trailing Tgt has yet to be Hit)
	HasYetToHitTrailingL = False #The High Of the Current Bar is Lower than the Currently Acive Long Position's Trailing Target (Trailing Tgt has yet to be Hit)
	
	HasYetToHitTargetS = False   #The Low Of the Current Bar is Higher than the Currently Acive Short Position's Target Price (It hasn't Hit Target Yet)
	HasYetToHitTargetL = False   #The High Of the Current Bar is Lower than the Currently Acive Long Position's Target Price (It hasn't Hit Target Yet) r
 	
 	CurrentlyInMarketS = False #Used to tell whether or not the system is currently in a Short position or not
 	CurrentlyInMarketL = False #Used to tell whether or not the system is currently in a Long position or not
 
 	StageOrder = False	
#Change PlotAddons from True/False input to On/Off input (1/On : 0/Off) 
	_PlotAddons = True      #Last Declaration of a Variable 

#Overall Functions of framework
	LastBarOnChart = False
#Arrays:
	_NumBarsJLsEqual = []
	arr_JL1 = []
	arr_JL2 = []

#Inputs:  	
	input_JL1 = 39		   	 	  	  #Length of JumpLine 1 (Typically is JL1 < JL2)
	input_JL2 = 10 			      	  #Length of JumpLine 2 (Typically is JL2 > JL1)
	input_CloseCancelsCross = True	  #A filter that if activated cancels a trade if the price closes in the oposite direction of the trade's side of JL2. 1/On : 0/Off 	
	input_UseJLCDFilter = False       
	input_JLCDLength = 7
	input_TargetLength = 4.882 	      #High + ((High - Low) * Tgt) = The Price that the Target is Placed
	input_BreakevenTarget = 1.37      #High + ((High - Low) * BreakevenTarget) = The Price Where the StopLoss is moved up to Breakeven
	input_TrailingJL = 11		   	  #JL used for Trailing
	input_TrailingTarget = 1.12       #The Point at which the trade begins to trail
	input_TrailingOffSetTics = 2      #How Many ticks Below the MA the Stop is Trailed	
	input_EntryOffsetTics = 13        #High + (EntryOffsetTics/PriceScale) = the Price where the Entry is Placed
	input_StopOffsetTics = -4         #Low - (StopOffsetTIcs/PriceScale) = The Price where the StopLoss is Placed	
	input_UseRiskFilter = 1		  	  #Used to Turn on and Off the Risk Filter.  1/On : 0/Off
	input_MaxTicsRisk = 790		  	  #Maximum tics risk for a trade to be considered valid
	input_MinTicsRisk = 120		  	  #Minimum tics risk for a trade to be considered valid
	input_PlotAddons = True     	  #Plot all Setups even when in the Market.  1/On : 0/Off
	input_Include_JLs_Equal = False	  #if true includes the length of JLs being equil in the calculation of bars_back
	input_PriceScale = 10000		  # 1/pricescale = number of decimals in the underlying asset
	input_ExpectedTicsSlippage = 10	  # this is the expected slippage used to offset the breakeven stop

	if Include_JLs_Equal:
		bars_back = process_function(data, MaxBarsBack)
	else:		
		#might need to be max + 1		
		bars_back = max(input_JL1, input_JL2, input_JLCDLength, input_TrailingJL)

	process_function(data, CO_Indicator)

def process_function(dataArray, functionName):
	'''
	!!!make this process a function and the last arugument is a function that runs inside the code
	!!!MAKE ORIGINAL DATA INTO TUPLE
	Loop through all data in multiples of 6 {i = (i+1)*6}
		push data onto respective arrays
			(push i onto arr_O,  i+1 onto arr_H, i+2 onto arr_L etc)
		if O length > bars_back
			take off first item in EVERY array
		
		if i/6 > bars_back and i + 1 is a multiple of 6:
			if dataArray[i+5] == dataArray[-1]:
				LastBarOnChart = True
			functionName(arr_O, arr_H, arr_L,arr_C, arr_Date, arr_Time, LastBarOnChart)
				print to an excel file
	'''
#Overall Functions
def Highest (price, length):
	return max(price[-length:])
def Lowest (price, length):
	return min(price[-length:])

def JL(high, low, length):
	return (Highest(high, length) + Lowest(low, length))/2

def maxBarsBack(arr_O, arr_H, arr_L, arr_C, arr_Date, arr_Time, LastBarOnChart):
	O = arr_O[-1]
	H = arr_H[-1]
	L = arr_L[-1]
	C = arr_C[-1]
	Date = arr_Date[-1]
	Time = arr_Time[-1]
	
	#prev_ = one bar ago value
	prev_JL1 = JL1
	prev_JL2 = JL2
	prev_Counting = Counting

	#JLs	
	JL1 = (Highest(H, input_JL1) + Lowest(L, input_JL1))/2 
	JL2 = (Highest(H, input_JL2) + Lowest(L, input_JL2))/2  
	TrailingJL = (Highest(H, input_TrailingJL) + Lowest(L, input_TrailingJL))/2  	

	if prev_JL1 != None:
		if (prev_JL1 != prev_JL2) and (JL1 == JL2):
			Counting = True
		elif (prev_JL1 != prev_JL2) and (JL1 != JL2):
			Counting = False	
			
		if Counting:
			NumBarsJLsEqual += 1				
		else:	
			if prev_Counting == True and Counting == False:	
				_NumBarsJLsEqual.append(NumBarsJLsEqual) 
				NumBarsJLsEqual = 0

		if LastBarOnChart:
			MaxBarsJLsEqual = HighestArray(_NumBarsJLsEqual)	
			#might need to be max + 1
			max_bars_back = max(input_JL1, input_JL2, input_JLCDLength, input_TrailingJL, MaxBarsJLsEqual) 
			return  max_bars_back

def CrossOver(arr1, arr2, BarsBack):
					CrossOver = False
								
				break	
			
			#Assume that if that if the last evaluated bar is reached and is still equal: there is a CrossOver
			if i == BarsBack and (arr1[i] == arr2[i]):
				CrossOver = True

	return CrossOver

def CrossUnder(arr1, arr2, BarsBack):
					CrossUnder = False
								
				break	
			
			#Assume that if that if the last evaluated bar is reached and is still equal: there is a CrossUnder
			if i == BarsBack and (arr1[i] == arr2[i]):
				CrossUnder = True
	
	return CrossUnder

def JLCD(high, low, JL1, JL2):
	return JL(high, low, JL1) - JL(high, low, JL2)

def CO_Indicator (arr_O, arr_H, arr_L, arr_C, arr_Date, arr_Time):
	O = arr_O[-1]
	H = arr_H[-1]
	L = arr_L[-1]
	C = arr_C[-1]
	Date = arr_Date[-1]
	Time = arr_Time[-1]
	#Push to excell file O,H,L,C,Date,Time
	
	#prev_ = one bar ago value
	prev_CurrentlyInMarketL = CurrentlyInMarketL 
	prev_CurrentlyInMarketS	= CurrentlyInMarketS
	prev_ASetupIsActiveL = ASetupIsActiveL
	prev_ASetupIsActiveS = ASetupIsActiveS
	prev_TheTrailingPriceL = TheTrailingPriceL
	prev_TheTrailingPriceS = TheTrailingPriceS
	prev_TheStopPriceL = TheStopPriceL
	prev_TheStopPriceS = TheStopPriceS

	#JLs	
	JL1 = JL(arr_H, arr_L, input_JL1) 
	JL2 = JL(arr_H, arr_L, input_JL2) 
	arr_JL1.append(JL1)
	arr_JL2.append(JL2) 
	if len(arr_JL1) > input_JL1:
		del arr_JL1[0]
	if len(arr_JL2) > input_JL2:
		del arr_JL2[0]

	TrailingJL = JL(arr_H, arr_L, input_TrailingJL) 

	#Push to excell file _JL1,_JL2,_TrailingJL

	#!!!Time needs to be close time of the bars
	#Exit Trade if market close on weekends
	if (CurrentlyInMarketL == True or CurrentlyInMarkets == True) and DayofWeek(Date) == Friday and Time == 1500:
		#Indicate to excell file that the trade was exited on close of this bar (possibly also indicate it was due to it being the weekend)
		
	if DayofWeek(Date) == Friday and Time >= 1500:
			CurrentlyInMarketL = False 
			CurrentlyInMarketS = False
			ASetupIsActiveS = False
			ASetupIsActiveL = False
			JL1CrossedUnderJL2 = False
			JL1CrossedOverJL2 = False
	elif (DayofWeek(Date) > Sunday) or (DayofWeek(Date) = Sunday and Time >= 1800) or (DayofWeek(Date) = Friday and Time < 1500):
				
		#Set the Trailing Price
		TrailingOffSetTics = input_TrailingOffSetTics/input_PriceScale
		TheTrailingPriceS = TrailingJL + TrailingOffSetTics
		TheTrailingPriceL = TrailingJL - TrailingOffSetTics


		#Conditions
		RedBar = C < O
		GreenBar = C > O

		CloseLessThanJL2 = C < JL2
		CloseHigherThanJL2 = C > JL2

		if CrossOver(arr_JL1, arr_JL2, bars_back):
			JL1CrossedOverJL2 = True
			JL1CrossedUnderJL2 = False
		elif CrossUnder(arr_JL1, arr_JL2, bars_back):
			JL1CrossedOverJL2 = False
			JL1CrossedUnderJL2 = True

		HasNotEnteredYetS = L > TheEntryPriceS
		HasYetToHitStopS = H < TheStopPriceS
		HasYetToHitTargetS = L > TheTargetPriceS
		HasYetToHitBrkEvnS = L > TheBreakevenTgtS
		HasYetToHitTrailingS = L > TheTrailingTgtS

		HasNotEnteredYetL = H < TheEntryPriceL
		HasYetToHitStopL = L > TheStopPriceL
		HasYetToHitTargetL = H < TheTargetPriceL
		HasYetToHitBrkEvnL = H < TheBreakevenTgtL
		HasYetToHitTrailingL = H < TheTrailingTgtL

		if CurrentlyInMarketL == False and CurrentlyInMarketS == False and (prev_CurrentlyInMarketL == True or prev_CurrentlyInMarketS == True): 
			JL1CrossedOverJL2 = False
			JL1CrossedUnderJL2 = False
			
		#Close Cancels Cross
		if CloseCancelsCross:
			if ASetupIsActiveS and not ASetupIsActiveL and CloseHigherThanJL2:
				ASetupIsActiveS = False
			if ASetupIsActiveL and not ASetupIsActiveS and CloseLessThanJL2:
				ASetupIsActiveL = False	

		if UseJLCDFilter:
			JLCD = JLCD(H, L, input_JL1, input_JL2)
			JLCDAvg = JL(JLCD, JLCD, JLCDLength) 
			JLCDDiff = JLCD - JLCDAvg
					
		#Short ENTRY
		if ASetupIsActiveS and not ASetupIsActiveL:
			if HasNotEnteredYetS:
				#Cancled?
				if JL1CrossedOverJL2 = False:
					#Idicate to excel that there is still an entry available at TheEntryPriceS
				else:
					ASetupIsActiveS = False
			else:
				#if the setup has entered:... 			
				CurrentlyInMarketS = True
				ASetupIsActiveS = False	

		#Long ENTRY
		if ASetupIsActiveL and not ASetupIsActiveS:
			if HasNotEnteredYetL:
				#Cancled?
				if JL1CrossedUnderJL2 = False:
					#Idicate to excel that there is still an entry available at TheEntryPriceL
				else:
					ASetupIsActiveL = False
			else:
				#if the setup has entered:... 				
				CurrentlyInMarketL = True
				ASetupIsActiveL = False	
			
		#Short STOPLOSS	
		if ASetupIsActiveS or CurrentlyInMarketS and ( not ASetupIsActiveL or not CurrentlyInMarketL ):
			#if There is a trade that has entered...	
			if CurrentlyInMarketS and not CurrentlyInMarketL:	
				#Evaluate if Stop has been Hit	
				if HasYetToHitStopS == False:
					CurrentlyInMarketS = False	
					StopIsAtBrkEvnS = False						
					NowTrailingS = False
						
					#Is the Trade A Breakeven Or Trailing	
					if TheStopPriceS <= TheEntryPriceS: 	
						#Gapping?	
						if O > TheStopPriceS:									
							if TheStopPriceS == TheTrailingPriceS:
								#indicate to excel that the trade was exited on the Open of this bar due to gapping
								#and was due to the trailing stoploss
							else:
								#indicate to excel that the trade was exited on the Open of this bar due to gapping
								#and was due to the breakeven stoploss

						#No Gapping
						else: 
							if TheStopPriceS == TheTrailingPriceS:
								#indicate to excel that the trade was exited on this bar at TheStopPriceS 
								#and was due to the trailing stoploss
							else:
								#indicate to excel that the trade was exited on this bar at TheStopPriceS 
								#and was due to the breakeven stoploss

					#Fixed Stop	
					else:
						#Gapping?	
						if O > TheStopPriceS:
							if StopIsAtBrkEvnS == False:								
								#indicate to excel that the trade was exited on the Open of this bar due to gapping
								#and was due to the fixed stoploss	
						#No Gapping
						else:
							if StopIsAtBrkEvnS == False:								
								#indicate to excel that the trade was exited on this bar at TheStopPriceS 
								#and was due to the fixed stoploss
		
				#Begin Using Breakeven or Trailing Stop?	
				#BREAKEVEN - Evaluate if Breakeven Target has been hit
				if HasYetToHitBrkEvnS == False:
					TheStopPriceS = (TheEntryPriceS - (input_ExpectedTicsSlippage/input_PriceScale))
					#Does the bar hit Breakeven Target: get stopped out on the Same Bar?	
					if C >= TheStopPriceS:
						CurrentlyInMarketS = False
						#indicate to excel that the trade was exited on this bar at TheStopPriceS 
						#and was due to the breakeven stoploss (possibly indicate it was in the same bar as well)
						StopIsAtBrkEvnS = False						
						NowTrailingS = False	
					else:					
						StopIsAtBrkEvnS = True	
				
				#if breakeven target was hit but not trailing target yet	
				if StopIsAtBrkEvnS and NowTrailingS == False:
					TheStopPriceS = (TheEntryPriceS - (input_ExpectedTicsSlippage/input_PriceScale))
						
				#TRAILING - Evaluate if Trailing Target has been hit
				if HasYetToHitTrailingS == False:
					TrailingIsOnS = True
				
				#Insure that even though the trailing target has been hit that it doesn't start actually trailing until the 
				#trailing price is above the entry price (preferably with the spread accounted for)				
				if (TheTrailingPriceS < TheEntryPriceS) and TrailingIsOnS:					
					NowTrailingS = True	
				
				if NowTrailingS:
					#Insure that trailing price never goes backwards with a JL
					if TheTrailingPriceS > prev_TheTrailingPriceS:
						TheTrailingPriceS = prev_TheTrailingPriceS		
					
					#If trailingPrice is beyond the entry and the current stop price				
					if TheTrailingPriceS < TheEntryPriceS and TheTrailingPriceS < TheStopPriceS:
						if C < TheTrailingPriceS:
							TheStopPriceS = TheTrailingPriceS
						else:
							TheStopPriceS = prev_TheStopPriceS
				
			#Plot Stop as long as the Target hasn't been hit yet
			if HasYetToHitTargetS and (ASetupIsActiveS or CurrentlyInMarketS) and not CurrentlyInMarketL:
				#Normally I would plot the stop price even if the setup was active and not entered but idk 
				#if I'll be doing that with the excell file.  We'll see. Plot9 (TheStopPriceS, "Stop", Cyan)
		
		#Long STOPLOSS	
		if ASetupIsActiveL or CurrentlyInMarketL and ( not ASetupIsActiveS or not CurrentlyInMarketS ):
			#if There is a trade that has entered...	
			if CurrentlyInMarketL and not CurrentlyInMarketS:	
				#Evaluate if Stop has been Hit	
				if HasYetToHitStopL == False:
					CurrentlyInMarketL = False	
					StopIsAtBrkEvnL = False						
					NowTrailingL = False
						
					#Is the Trade A Breakeven Or Trailing	
					if TheStopPriceL >= TheEntryPriceL: 	
						#Gapping?	
						if O < TheStopPriceL:									
							if TheStopPriceL == TheTrailingPriceL:
								#indicate to excel that the trade was exited on the Open of this bar due to gapping
								#and was due to the trailing stoploss
							else:
								#indicate to excel that the trade was exited on the Open of this bar due to gapping
								#and was due to the breakeven stoploss

						#No Gapping
						else: 
							if TheStopPriceL == TheTrailingPriceL:
								#indicate to excel that the trade was exited on this bar at TheStopPriceS 
								#and was due to the trailing stoploss
							else:
								#indicate to excel that the trade was exited on this bar at TheStopPriceS 
								#and was due to the breakeven stoploss

					#Fixed Stop	
					else:
						#Gapping?	
						if O < TheStopPriceL:
							if StopIsAtBrkEvnL == False:								
								#indicate to excel that the trade was exited on the Open of this bar due to gapping
								#and was due to the fixed stoploss	
						#No Gapping
						else:
							if StopIsAtBrkEvnL == False:								
								#indicate to excel that the trade was exited on this bar at TheStopPriceS 
								#and was due to the fixed stoploss
		
				#Begin Using Breakeven or Trailing Stop?	
				#BREAKEVEN - Evaluate if Breakeven Target has been hit
				if HasYetToHitBrkEvnL == False:
					TheStopPriceL = (TheEntryPriceL + (input_ExpectedTicsSlippage/input_PriceScale))
					#Does the bar hit Breakeven Target: get stopped out on the Same Bar?	
					if C <= TheStopPriceL:
						CurrentlyInMarketL = False
						#indicate to excel that the trade was exited on this bar at TheStopPriceS 
						#and was due to the breakeven stoploss (possibly indicate it was in the same bar as well)
						StopIsAtBrkEvnL = False						
						NowTrailingL = False	
					else:					
						StopIsAtBrkEvnL = True	
				
				#if breakeven target was hit but not trailing target yet	
				if StopIsAtBrkEvnL and NowTrailingL == False:
					TheStopPriceL = (TheEntryPriceL + (input_ExpectedTicsSlippage/input_PriceScale))
						
				#TRAILING - Evaluate if Trailing Target has been hit
				if HasYetToHitTrailingL == False:
					TrailingIsOnL = True
				
				#Insure that even though the trailing target has been hit that it doesn't start actually trailing until the 
				#trailing price is above the entry price (preferably with the spread accounted for)				
				if (TheTrailingPriceL > TheEntryPriceL) and TrailingIsOnL:					
					NowTrailingL = True	
				
				if NowTrailingL:
					#Insure that trailing price never goes backwards with a JL
					if TheTrailingPriceL < prev_TheTrailingPriceL:
						TheTrailingPriceL = prev_TheTrailingPriceL		
					
					#If trailingPrice is beyond the entry and the current stop price				
					if TheTrailingPriceL > TheEntryPriceL and TheTrailingPriceL < TheStopPriceL:
						if C > TheTrailingPriceL:
							TheStopPriceL = TheTrailingPriceL
						else:
							TheStopPriceL = prev_TheStopPriceL
				
			#Plot Stop as long as the Target hasn't been hit yet
			if HasYetToHitTargetL and (ASetupIsActiveL or CurrentlyInMarketL) and not CurrentlyInMarketL:
				#Normally I would plot the stop price even if the setup was active and not entered but idk 
				#if I'll be doing that with the excell file.  We'll see. TheStopPriceS


#next work on Short Target and below
		#Short TARGET
		if CurrentlyInMarketS = True and not CurrentlyInMarketL:
			Begin
				if HasYetToHitTargetS = False:
					Begin
					#Gapping	
						if Open of Data2 < TheTargetPriceS:
							Begin
								CurrentlyInMarketS = False				
								Plot12(Open of Data2,"Exit", DarkGreen)
								StopIsAtBrkEvnS = False
								NowTrailingS = False
							End
						else:
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
		if CurrentlyInMarketL = True and not CurrentlyInMarketS:
			Begin
				if HasYetToHitTargetL = False:
					Begin
					#Gapping	
						if Open > TheTargetPriceL:
							Begin
								CurrentlyInMarketL = False				
								Plot12(Open,"Exit", DarkGreen)
								StopIsAtBrkEvnL = False
								NowTrailingL = False
							End
						else:
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
		if JL1CrossedUnderJL2 and RedBar and CloseLessThanJL2 and CurrentlyInMarketS = False and CurrentlyInMarketL = False and ASetupIsActiveL = False and ASetupIsActiveS = False: 
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
								
				if TheBreakevenTgtS > (TheEntryPriceS - Spread(5)) or TheTrailingTgtS > (TheEntryPriceS - Spread(5)):
					Begin
						StageOrder = False	
						ASetupIsActiveS = False
					End			
										
				PipsRiskS = ((TheStopPriceS - TheEntryPriceS) + Spread(20) + (20/Pricescale))*(PriceScale/10)
				
				if (UseRiskFilter = 1 and ((PipsRiskS*10) < MinTicsRisk) or ((PipsRiskS*10) > MaxTicsRisk)) or (UseJLCDFilter and JLCDDiff > 0) :
					Begin
						ASetupIsActiveS = False
						StageOrder = False	
					End
					
				if StageOrder:
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
		if JL1CrossedOverJL2 and CloseHigherThanJL2 and GreenBar and CurrentlyInMarketL = False and CurrentlyInMarketS = False and ASetupIsActiveL = False and ASetupIsActiveS = False: 
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
												
				if TheBreakevenTgtL < (TheEntryPriceL + Spread(5)) or TheTrailingTgtL < (TheEntryPriceL + Spread(5)):
					Begin	
						StageOrder = False
						ASetupIsActiveL = False
					End		
				
				PipsRiskL = ((TheEntryPriceL - TheStopPriceL) + Spread(20) + (20/Pricescale))*(PriceScale/10)		
					
				if (UseRiskFilter = 1 and ((PipsRiskS*10) < MinTicsRisk) or ((PipsRiskS*10) > MaxTicsRisk)) or (UseJLCDFilter and JLCDDiff < 0) :
					Begin
						ASetupIsActiveL = False
						StageOrder = False	
					End
						
				if StageOrder:
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
		if JL1CrossedUnderJL2 and RedBar and CloseLessThanJL2: 
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
					
				if Value1 > Value4 or Value2 > Value4 or Value3 > Value4 :
					StageOrder = False	
				
				if UseRiskFilter = 1 and ((((Value5 - Value4)*PriceScale) < MinTicsRisk) or	(((Value5 - Value4)*PriceScale) > MaxTicsRisk)):
					StageOrder = False
					
				if _PlotAddons and StageOrder:
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
		if JL1CrossedOverJL2 and CloseHigherThanJL2 and GreenBar: 
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
								
				if Value6 < Value9 or Value7 < Value9 or Value8 < Value9:
					 StageOrder = False
				
				if UseRiskFilter = 1 and ((((Value9 - Value10)*PriceScale) < MinTicsRisk) or (((Value9 - Value10)*PriceScale) > MaxTicsRisk)):
					StageOrder = False
				
				if _PlotAddons and StageOrder:
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
		if High = 99999999999: 
			Begin	
				Plot4(0,"=========")
				Plot10(0,"=========")
				Plot13(0,"=========")
				Plot16(0,"=========")
				Plot50(0,"=========")	
				
			End
				
		if prev_ASetupIsActiveL or prev_CurrentlyInMarketL:
			Begin	
				SetPlotColor[1](11, Green)
				Plot11[1]("Long", "Type")
			End
			
		if prev_ASetupIsActiveS or prev_CurrentlyInMarketS:
			Begin	
				SetPlotColor[1](11, Red)
				Plot11[1]("Short", "Type")				
			End	

	#End of Code	