# GPT3.5---------------------------------------------------------------------
import openai
import json

def question_generation(prompt):

    # 填写注册OpenAI接口账号时获取的 OpenAI API Key
    openai.api_key = "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"

# 提问
    #prompt = '請幫我出python的題目十題，內含程式碼的單選題，並附上詳解，範圍為資料結構的list和tuple之間的應用'

# 访问OpenAI接口
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "你是一位在大學教大學生如何寫python的教授"},
            {"role": "user", "content": prompt}
        ]
    )

    # 返回信息
    resText_qus = response.choices[0].message.content

    return resText_qus


def check(prompt):
    # 填写注册OpenAI接口账号时获取的 OpenAI API Key
    openai.api_key = "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"

# 提问
    #prompt = '請幫我出python的題目十題，內含程式碼的單選題，並附上詳解，範圍為資料結構的list和tuple之間的應用'

# 访问OpenAI接口
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "你是一位在大學教大學生如何寫python的教授"},
            {"role": "user", "content": '請幫我檢查下列程式碼分析題中的選項是否有出錯，若有出錯，請只回答YES就好，若無出錯，請只回答NO:\n'+prompt}
        ]
    )

    # 返回信息
    resText_check = response.choices[0].message.content

    return resText_check


def questions_split(question):
    question_option = question[1]
    question_option_split = question_option.split('\n')
    for i in question_option_split:         # 1st loop
        if '' in question_option_split:   # 2nd loop
            question_option_split.remove('')
    return question_option_split

def question_get(question):
    question_dic = json.loads(question)
    questions = question_dic['question']
    code = question_dic['code']
    answer = question_dic['answer']
    option_A = '(A) '+ question_dic['options']['A']
    option_B = '(B) '+ question_dic['options']['B']
    option_C = '(C) '+ question_dic['options']['C']
    option_D = '(D) '+ question_dic['options']['D']
    detailed_explanations = '(詳解)' + question_dic['detailed explanation']
    list_all = [questions ,code ,option_A, option_B, option_C, option_D, answer,detailed_explanations]
    
    return list_all