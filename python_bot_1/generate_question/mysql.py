import app
import time
import json

for i in range(10):
    question = app.question_generation(
        "請幫我出python的題目一題，為A,B,C,D四選項之單選題，範圍為變數，題型為程式碼分析題，格式為JSON，Key分為question,code,options,answer，A,B,C,D之四個選項在options中作為獨立的key，題目之程式碼會位於code之中")
    checker = app.check(
        question)
    time.sleep(1)
    if checker == "NO":
        #question_ans = question.split("？")
        # ------------------------------測試用
        print(app.question_get(question))
        #json_question = json.loads(question)
        #print(json_question['options'])
        #print(question)
        # ------------------------------
        #print(question_ans[0])  # 題目(str)
        #print(app.questions_split(  # 選項(list)
            #question_ans))
        import mysql.connector

        # 建立 MySQL 連線
        mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        port ='3306',
        password='mysql0913-4157',
        charset = "utf8"
        )

        cursor = mydb.cursor()

        def get_data():
            return app.question_get(question)
        result = get_data()
    

        # 插入資料庫
        cursor.execute("use `test`;")
        sql = "INSERT INTO `變數` (`question`, `code`, `a`, `b`, `c`, `d`, `ans`,`answer`) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
        val = tuple(app.question_get(question))
        cursor.execute(sql, val)

        # 查詢資料
        # cursor.execute("SELECT * FROM `python_new`")
        # records = cursor.fetchall()
        # for r in records:
        #     print(r)

        
        mydb.commit()
        cursor.close()
        mydb.close()
    else:
        NEW_question = app.question_generation(
            "請幫我訂正下題，並用JSON格式重新輸出題目:\n"+question)
        #question_ans = NEW_question.split("？")
        # ------------------------------測試用
        print(app.question_get(NEW_question))
        #json_question =json.loads(NEW_question)
        #print(json_question['options'])
        
        # ------------------------------
        #print(question_ans[0])  # 題目(str)
        #print(app.questions_split(  # 選項(list)
            #question_ans))
        import mysql.connector


        # 建立 MySQL 連線
        mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        port ='3306',
        password='mysql0913-4157',
        charset = "utf8"
        )

        cursor = mydb.cursor()

        def get_data():
            return app.question_get(NEW_question)
        result = get_data()
        #print(result)

        # 插入資料庫
        cursor.execute("use `test`;")
        sql = "INSERT INTO `變數` (`question`, `code`, `a`, `b`, `c`, `d`, `ans`,`answer`) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
        val =  tuple(app.question_get(NEW_question))
        cursor.execute(sql, val)

        # 查詢資料
        # cursor.execute("SELECT * FROM `python_new`")
        # records = cursor.fetchall()
        # for r in records:
        #     print(r)

        
        mydb.commit()
        cursor.close()
        mydb.close()