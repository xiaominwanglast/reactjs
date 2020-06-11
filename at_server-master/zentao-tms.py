import pymysql, re

conn = pymysql.Connect(host='172.17.16.51', port=3306, user='root', password="1qaz2wsx", database="tower",
                       charset='utf8mb4')
cursor = conn.cursor()

v = cursor.execute("""

SELECT 
id,title,product_docs,min(create_time),max(create_time)

FROM (
SELECT flowapp_testtask.id,flowapp_testtask.title,product_docs, flowapp_testtaskoperation.create_time,change_action
FROM
 flowapp_testtaskoperation,flowapp_testtask
WHERE testtask_id = flowapp_testtask.id and flowapp_testtask.status='已上线'
ORDER BY testtask_id) a


GROUP BY id

""")
result = cursor.fetchall()
cursor.close()
conn.close()

conn = pymysql.Connect(host='172.16.0.146', port=33060, user='dev', password="dev", database="zentao",
                       charset='utf8')
cursor = conn.cursor()

for row in result:
    pat = re.findall('zentao/(.*?)-(.*?)-(.*?)[\.|-]', row[2], re.I)
    if len(pat) != 0:
        sql = f"select * from zt_action where objectType='{pat[0][0]}' and  objectID='{pat[0][2]}' order by date desc"
        v = cursor.execute(sql)
        action_result = cursor.fetchall()
        story_time = None
        for action in action_result:
            if action[6] in ('reviewed', 'opened'):
                story_time = action[7]
                break
        # print(row[0], row[1], "http://172.16.0.146:58080/zentao/"+"-".join(pat[0])+".html", row[3], row[4], story_time)
        print(f"{row[0]}.{row[1].replace('.','-')}.{'-'.join(pat[0])}.{row[3].strftime('%Y-%m-%d %H:%M:%S')}.{row[4].strftime('%Y-%m-%d %H:%M:%S')}.{story_time.strftime('%Y-%m-%d %H:%M:%S')}")

    else:
        print(f"{row[0]}.{row[1].replace('.','-')}.{pat}.{row[3].strftime('%Y-%m-%d %H:%M:%S')}.{row[4].strftime('%Y-%m-%d %H:%M:%S')}.{row[3].strftime('%Y-%m-%d %H:%M:%S')}")

cursor.close()
conn.close()
