# Milli Piyango Package

This is a package for getting lottery related data from [Milli Piyango](http://www.mpi.gov.tr/).

## Installation
```bash
pip install milli-piyango
```

## Usage

For most case:
```python
from milli_piyango import MilliPiyango as mP


# Getting available game list
print(mP.GAME_LIST)

# Get available drawing dates for given games
# Available game names
# - mp.PIYANGO
# - mp.SAYISAL
# - mp.SANS_TOPU
# - mp.ON_NUMARA
# - mp.SUPER_LOTO
dates = mP().get_draw_dates(mP.ON_NUMARA)
# [ {'tarih': '20180730', 'tarihView': '30-07-2018'}, ... ]

# Get game result for given date
last_drawing_result = mP().get_result(mP.ON_NUMARA, dates[0]['tarih']) # For the last drawing result

# Winner numbers in order 
print(last_drawing_result['data']['rakamlarNumaraSirasi'])
# '08 - 11 - 15 - 16 - 17 - 18 - 20 - 25 - 28 - 30 - 34 - 39 - 40 - 43 - 48 - 53 - 59 - 64 - 66 - 67 - 71 - 79'
```

If you want to search a number (ticket number) is winner or not in `Piyango` game;
```python
from milli_piyango import MilliPiyango as mP


mP().get_result_for_piyango("20180729", "179604") # First parameter is Date, second one is Ticket Number
# {'kazandi': True, 'tip': '$6_RAKAM', 'ikramiye': 2500000, 'kacBildi': 6, 'numara': '179604', 'biletNo': '179604'}
mP().get_result_for_piyango("20180729", "178630")
# {'kazandi': True, 'tip': 'SON_BES_RAKAM', 'ikramiye': 400, 'kacBildi': 5, 'numara': '78630', 'biletNo': '178630'}
mP().get_result_for_piyango("20180729", "189604")
# {'kazandi': True, 'tip': 'AMORTI', 'ikramiye': 24, 'kacBildi': 1, 'numara': '4', 'biletNo': '189604'}
mP().get_result_for_piyango("20180729", "123452")
# {'kazandi': False, 'biletNo': '123452'}
```
