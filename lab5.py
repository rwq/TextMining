#Task 2: Create a geochart that displays how often different locations 
#are mentioned in a text proportionally to each other.
from geotext import GeoText

with open('./europe_backpacker_index.txt', 'r') as f:
    geo = GeoText(f.read())

print(geo.country_mentions)

''' OrderedDict([('NL', 58), ('US', 50), ('HR', 24), ('NO', 17), ('ES', 14), ('DE', 14), ('CZ', 13), 
('GB', 12), ('IT', 12), ('LV', 8), ('PL', 7), ('MT', 7), ('FR', 7), ('AT', 7), ('UA', 7), ('FI', 6), 
('SI', 6), ('BE', 6), ('SE', 6), ('RO', 6), ('CH', 6), ('PT', 5), ('EE', 5), ('TR', 5), ('BG', 5), 
('RS', 5), ('IS', 5), ('RU', 5), ('LT', 5), ('HU', 5), ('SK', 4), ('VE', 4), ('DK', 4), ('UK', 3), 
('GR', 3), (), ('BA', 3), ('IN', 1), ('IE', 1), ('GH', 1), ('ZA', 1), ('IL', 1), ('LU', 1), ('MC', 1), ('SZ', 1)])
' '''