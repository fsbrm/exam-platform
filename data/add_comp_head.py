import pymysql
conn = pymysql.connect(host='localhost', user='root', password='123456', database='exam_platform', charset='utf8mb4')
cursor = conn.cursor()

questions = []
