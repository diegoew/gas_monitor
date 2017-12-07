# gas_monitor

Goal:
Better understand any fluctuations in air pollutants sourcing for natural gas operations:
- Natural Gas (a mix of gases*)
- Methane (main component of Natural Gas ~ 80 – 95%)
- CO2 (combustion output after gas is burnt)
- CO (combustion output after gas is burnt with lack of Oxygen)
– NOx (combustion by-product output after gas is burnt)
– Ammonia (used for emission control to reduce NOx)
- Formaldehyde
 
Expectations and Limitations:
-	While the sensors used for this are very fast reactive, there are not intended to give an exact value of the pollutants. None of the sensors is exclusively sensitive to just one type of gas. Therefor other gases might skew the values. 
 
Setup
The basic setup of this air gas monitor consist of: 
-	Raspberry Pi
-	MQ series sensors 
-	Python program
-	Cloud sharing program
-	Website.
 
*Natural Gas:
-	Natural gas is a fossil fuel composed almost of methane, but does contain amounts of other hydrocarbon gases, including but not limited to ethane, propane, butane and pentane. It also commonly includes varying amounts of other higher alkanes, and sometimes a small percentage of carbon dioxide, nitrogen, hydrogen sulfide, or helium. Natural gas that is derived from shale gas could include other chemical used in the extraction process of the gas. If mixed with biogas or landfill gas it can also contain acids and other corrosive substances.
-	In order to assist in detecting leaks, an odorizer is added to the otherwise colorless and almost odorless natural gas. The odor has been compared to the smell of rotten eggs, due to the added tert-Butylthiol (t-butyl mercaptan). Sometimes a related compound, thiophane, may be used in the mixture. These additives are also a deferent for humans to inhale the gas. The additives themselves are irritants that can cause nausea in humans and also have more severe health effects with prolonged exposure to the skin, eyes, kidneys, lungs and liver.
-	Natural gas extraction also produces radioactive isotopes of polonium (Po-210), lead (Pb-210) and radon (Rn-220). Radon is a gas with initial activity from 5 to 200,000 becquerels per cubic meter of gas. It decays rapidly to Pb-210 which can build up as a thin film in gas extraction equipment.


Gas Monitor

Orginal Version: follows the tutorial for most part - adjusted curve calculation
- example.py  <-- run this!
- mq.py
- mcp3008

- gas.py --> same as example.py but showing all sensitivities

2nd Version: 3 sensors.... I just duplicated the calcualtions. The values are nonsense, but it works to see if all sensors are reading
- gas-2.py  <-- run this!
- mq2.py
- mcp3008.py

3rd Version: not finished... working on cleaning code and adding correct calculations.
- mq3.py
