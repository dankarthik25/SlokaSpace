import os 
from static.SqliteModel import SqliteModel
current_path = os.getcwd()
parrent_dir = os.path.dirname(current_path)
# print(current_path, parrent_dir)
db_path = file_path = os.path.join(parrent_dir, 'slokabase', 'database', 'slokabase.db')
# print(db_path)


from jinja2 import Environment, FileSystemLoader
import json
# Load templates from the "templates" folder
env = Environment(loader=FileSystemLoader("templates"))

# template = env.get_template("index.html")
template = env.get_template("index.html")
SongIndex_sql = SqliteModel(db_path,'SongIndex')
song_list2 = SongIndex_sql.read_entry(*['song_idx', 'song_name', 'devotion_god','author'])
# print(song_list2)
output = template.render(song_list=song_list2)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(output)
print("Static HTML generated: output.html")

def get_linewise_synonym(my_sloka):
#    print('get linewise synonym: my_sloka:',my_sloka)
    if my_sloka['synonyms'] !=None:
#        print(my_sloka['synonyms'])
#        print('before split: ',my_sloka['synonyms'].split('\n') )
        #####################################################
        synonym_list=[]
        for line in my_sloka['synonyms'].split('\n'):
            linewise_synonym_list =[]
            linewise_synonym = line.split(';')
            # linewise_synonym_list.append(line.split(';'))
            for item_string in linewise_synonym: 
                if len(item_string.split('='))==2:
                    pairs = item_string.split('=')
                    temp_dic = dict()
                    temp_dic[pairs[0].strip()] = pairs[1].strip()
                    linewise_synonym_list.append(temp_dic)
            synonym_list.append(linewise_synonym_list)
        
#        print('\n ### synonym_list',synonym_list)
        #####################################################
        filtered_synonyms = ' '.join(my_sloka['synonyms'].split('\n')).split(';')
#        print('# '*10)
#        print('Temp synonyms : ',filtered_synonyms) 
        new_synonyms=[]
        for item in filtered_synonyms:
            if item != '':
                temp_dic = dict()
#                print('item: ',item)                
                pairs = item.split('=')
                if len(pairs) == 2:
#                    print('pairs:',pairs)
                    # temp_dic=dict()
                    temp_dic[pairs[0].strip()] = pairs[1].strip()
                    new_synonyms.append(temp_dic)
            # new_synonyms.append(temp_dic)
#        print('# # # new_synonyms :', new_synonyms)
        my_sloka['synonyms']    = new_synonyms
    else :
#        print('synonmy_list empty')
        synonym_list = None

    return synonym_list

song_list = SongIndex_sql.read_entry(*['song_idx'])
SongIndex_sql = SqliteModel(db_path,'SongIndex')
mySongs_sql = SqliteModel(db_path,'Songs')
for song_id in range(1,len(song_list)+1):
    mysong_metadata = SongIndex_sql.read_entry(song_idx=song_id)
    sloka_list =  mySongs_sql.read_entry("slokas_no", song_idx=song_id)
    NoOf_Slokas = len(sloka_list)
    

    my_song = mySongs_sql.read_entry(song_idx=song_id)
    
    for my_sloka in my_song:
        if my_sloka['sloka_eng'] !=None: 
            my_sloka['sloka_eng']   = my_sloka['sloka_eng'].split('\n')
    
        # synonym_list = get_linewise_synonym(my_sloka)
        my_sloka['synonyms'] = get_linewise_synonym(my_sloka)
    
        if my_sloka['translation'] !=None:    
            my_sloka['translation'] = my_sloka['translation'].split('\n')
    
    # template = env.get_template("index.html")
    template = env.get_template("song.html")
    output = template.render(song_meta=my_song, info=mysong_metadata)
    with open(f"SongLib/{song_id}.html", "w", encoding="utf-8") as f:
        f.write(output)
    print(f"Static HTML generated: SongLib/{song_id}.html")