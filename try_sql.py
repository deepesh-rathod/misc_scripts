import json
def insert_sql(table, data, conn):
    query = 'insert into ' + table + '('
    keys = list(data.keys())
    query += ', '.join(keys) + ') values ('
    itr = 0
    for key in keys:
        itr += 1
        val = data[key]
        print(key, val, type(val))
        if type(val) == str:
            val = val.replace("''","'").replace("'","''").replace("%%","%").replace("%","%%")
            query += "'" + val + "'"
        elif type(val) == dict:
            val = json.dumps(val).replace("''","'").replace("'","''").replace("%%","%").replace("%","%%")
            query += "'" + val + "'"
        elif type(val) == int:
            query += str(val)
        elif type(val) == float:
            query += str(val)
        elif val is None:
            query += "null"
        if itr == len(keys):
            query += ')'
        else:
            query += ', '
    try:
        print(query)
        conn.commit()
    except:
        print("error")

data = {'biz_name': 'Celestial Beauty & Wellness Bar', 'place_id': 'ChIJd2wW8b2pK4cR57a-jsF8Gzc', 'form_data': {'name': 'natalie snook', 'phone': '4804590377'}, 'customer_type': 'New Client', 'initial_referrer': '$direct'}

insert_sql("any",data,None)
