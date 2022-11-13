HEADERSIZE = 32
data_packet = {
    'envelope' : {
        'from ' : None, 
        'to' : None
        },
    'body' : None
    }

def all_keys(dictionary):
    for key, value in dictionary .items():
        yield key
        if isinstance(value, dict):
            yield from all_keys(value)

 