import ijson 
from datetime import datetime 
from .models import FilmComments

def save_from_json(file_path):
    with open(file_path, 'r') as f:
        for item in ijson.items(f, 'item'):
            fn = ''.join(item['film_name'])
            cn = ''.join(item['cus_name']).encode('utf-16', 'surrogatepass').decode('utf-16').encode('utf-8').decode('utf-8')
            ct = ''.join(item['comment']).encode('utf-16', 'surrogatepass').decode('utf-16').encode('utf-8').decode('utf-8')
            gr = None if(len(item['grade']) == 0) else ''.join(item['grade'])
            se = item['source']
            ti = datetime.strptime(','.join(item['time'][0].split('- :')), '%Y-%m-%d %H:%M:%S')
            if not (FilmComments.is_existed(ti)):
                fc = FilmComments(cus_name=cn, film_name=fn, comment=ct, grade=gr, source=se, time=ti)
                fc.save()
