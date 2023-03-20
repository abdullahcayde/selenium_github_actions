
print('--------------------------------------- Connect to Database for alldata ---------------------------------------')
log('connected_database')
conn = psycopg2.connect(database="JOB",
			user='postgres', password=1984,
			host='127.0.0.1', port='5432'
)

conn.autocommit = True
cursor = conn.cursor()


sql = '''CREATE TABLE IF NOT EXISTS alldata(id serial PRIMARY KEY,
job_title text ,\
publish varchar(30),\
company text,\
city varchar(300),\
description text,\
link text,\
website varchar(30),\
date timestamp,\
search_title varchar(30));'''


cursor.execute(sql)


# connection string: driver://username:password@server/database
engine = create_engine('postgresql+psycopg2://postgres:1984@localhost/JOB')


#  Note:  if_exists can be append, replace, fail.  
df01.to_sql('alldata', engine, if_exists='append', index = False)
df02.to_sql('alldata', engine, if_exists='append', index = False)


sql2 = '''SELECT company FROM alldata WHERE publish LIKE '%Stunde%' ORDER BY publish LIMIT 5'''
cursor.execute(sql2)
for i in cursor.fetchall():
	print(i)

# Commit 
conn.commit()
log('finish_all') 


# Save Dataframes to Csv
path = '/Users/macbook/Desktop/projects/Github_Repositories/Trainings/web_scpraing_portfolio_deneme/data'
today_ = datetime.today().strftime('%Y-%m-%d')
#df01.to_csv(f'{path}/{job_name}.csv', header=True) >> First time
df01.to_csv(f'{path}/{job_name}_{today_}.csv', mode='a', header=False)
df02.to_csv(f'{path}/{job_name}_{today_}.csv', mode='a', header=False)


print(f'Today {today_} mycode Runned.')
