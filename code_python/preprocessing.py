cd C:\Users\angoran\Documents\Job application\Satalia Optimisation Challenge

df = pd.read_excel('whc-sites-2019.xls')
f = pd.DataFrame({'unique_number':df['unique_number'], 'name_en': df['name_en'], 'danger':df['danger'], 'longitude':df['longitude'], 'latitude':df['latitude'], 'category':df['category'], 'states_name_en':df['states_name_en']})
f = f.sort_values(by=['states_name_en'])
f = f.reset_index(drop=True)
f['states_name_en'][4] = 'Slovakia'
f['states_name_en'][5] = 'Albania'
f['states_name_en'][24] = 'Chile'
f['states_name_en'][70] = 'Estonia'
f['states_name_en'][82] = 'France'
f['states_name_en'][83] = 'Switzerland'
f['states_name_en'][86] = 'Benin'
f['states_name_en'][95] = 'Bosnia and Herzegovina'
f['states_name_en'][135] = 'Congo'
f['states_name_en'][218] = 'China'
f['states_name_en'][230] = 'Costa Rica'
f['states_name_en'][238] = 'Italy'
f['states_name_en'][264] = 'Czechia'
f['states_name_en'][268] = "Côte d'Ivoire"
f['states_name_en'][285] = "Germany"
f['states_name_en'][317] = "Finland"
f['states_name_en'][359] = "France"
f['states_name_en'][362] = "Sénégal"
f['states_name_en'][405] = "Germany"
f['states_name_en'][406] = "United Kingdom of Great Britain and Northern Ireland"
f['states_name_en'][432] = "Italy"
f['states_name_en'][441] = "Hungary"
f['states_name_en'][581] = 'Switzerland'
f['states_name_en'][582] = 'Italy'
f['states_name_en'][615] = 'Kyrgyzstan'
f['states_name_en'][634] = 'Lesotho'
f['states_name_en'][642] = 'Russian Federation'
f['states_name_en'][800] = 'Poland'
f['states_name_en'][817] = 'Spain'
f['states_name_en'][865] = 'Russian Federation'
f['states_name_en'][866] = 'Mongolia'
f['states_name_en'][894] = 'Spain'
f['states_name_en'][1116] = 'Zimbabwe'
f = f.sort_values(by=['states_name_en'])
f = f.reset_index(drop=True)
f['states_name_en'][23] = 'Brazil'
f['states_name_en'][55] = 'Hungary'
f['states_name_en'][68] = 'Belarus'
f['states_name_en'][54] = 'Switzerland'
f = f.sort_values(by=['states_name_en'])
f = f.reset_index(drop=True)