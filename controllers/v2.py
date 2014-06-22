# coding: utf8
# try something like
def index(): return dict(message="hello from v2.py")

auth.settings.allow_basic_login = True
@auth.requires_login()
def catalog():
    from gluon.tools import Auth
    import yaml
    import json
    with open('/settings.yml', 'r') as f:
        yaml_settings = yaml.load(f)
    json_settings = json.dumps(yaml_settings)
    data = json.loads(json_settings)
    return data['catalog']

@auth.requires_login()
def service_instances():
    import uuid, mysql.connector, yaml, json
    id = request.args
    with open('/settings.yml', 'r') as f:
        yaml_settings = yaml.load(f)
    json_settings = json.dumps(yaml_settings)
    data = json.loads(json_settings)
    mysql_host = str(data['custom-mysql']['host'])
    mysql_user = str(data['custom-mysql']['username'])
    mysql_password = str(data['custom-mysql']['password'])
    conn = mysql.connector.connect(user=mysql_user, host=mysql_host, database='mysql', password=mysql_password)
    cursor = conn.cursor()
    dbname = "db_"+str(hash(id[0][0-10]))
    username = "user_"+str(hash(id[0][0-10]))
    password = "passwd_"+str(hash(id[0][0-10]))
    create_db_stmt = "create database "+dbname+";"
    create_user_stmt = "grant usage on *.* to "+username+"@'%' identified by '"+password+"';"
    priv_user_stmt = "grant all privileges on "+dbname+".* to "+username+"@'%' ;"
    url = "mysql://"+username+":"+password+"@www.rcsousa.com.br/db_"+dbname
    if len(id) == 1:
        if request.env.request_method == "PUT":
            cursor.execute(create_db_stmt)
            cursor.execute(create_user_stmt)
            cursor.execute(priv_user_stmt)
            response = { "dashboard_url": url }
            return response
        if request.env.request_method == "DELETE":
            try:
                delete_db_stmt = "drop database if exists "+dbname+";"
                delete_user_stmt = "drop user "+username+";"
                cursor.execute(delete_db_stmt)
                cursor.execute(delete_user_stmt)
                response = {}
                return response
            except:
                raise HTTP(410, "Gone")
                response = {}
                return response
    if len(id) > 1:
        if request.env.request_method == "PUT":
            response = {"credentials": {"uri": url,"username": username,"password": password,"host": "www.rcsousa.com.br","port": 3306,"database": dbname}}
            return response
        if request.env.request_method == "DELETE":
            response = {}
            return response
