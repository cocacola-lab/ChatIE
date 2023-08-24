import json
import random
import ast
from revChatGPT.V1 import Chatbot
import re
import openai
import itertools

df_access = [
    ('@gYaKlfLGewYYkmZb7T3BlbkFJouvA5wegTYHbPcgWgI4D','sk-1Ni')
]

df_ret = {
    'english': {
            'location-located_in': ['location', 'location'],
            'administrative_division-country': ['location', 'country'],
            'person-place_lived': ['person', 'location'],
            'person-company': ['person', 'organization'],
            'person-nationality': ['person', 'country'],
            'company-founders': ['organization', 'person'],
            'country-administrative_divisions': ['country', 'location'],
            'person-children': ['person', 'person'],
            'country-capital': ['country', 'city'],
            'deceased_person-place_of_death': ['person', 'location'],
            'neighborhood-neighborhood_of': ['location', 'location'],
            'person-place_of_birth': ['person', 'location'],
            },
    'chinese': {'所属专辑': ['歌曲', '音乐专辑'], '成立日期': ['机构', 'Date'], '海拔': ['地点', 'Number'], '官方语言': ['国家', '语言'], '占地面积': ['机构', 'Number'], '父亲': ['人物', '人物'], 
                '歌手': ['歌曲', '人物'], '制片人': ['影视作品', '人物'], '导演': ['影视作品', '人物'], '首都': ['国家', '城市'], '主演': ['影视作品', '人物'], '董事长': ['企业', '人物'], '祖籍': ['人物', '地点'], 
                '妻子': ['人物', '人物'], '母亲': ['人物', '人物'], '气候': ['行政区', '气候'], '面积': ['行政区', 'Number'], '主角': ['文学作品', '人物'], '邮政编码': ['行政区', 'Text'], '简称': ['机构', 'Text'], 
                '出品公司': ['影视作品', '企业'], '注册资本': ['企业', 'Number'], '编剧': ['影视作品', '人物'], '创始人': ['企业', '人物'], '毕业院校': ['人物', '学校'], '国籍': ['人物', '国家'], 
                '专业代码': ['学科专业', 'Text'], '朝代': ['历史人物', 'Text'], '作者': ['图书作品', '人物'], '作词': ['歌曲', '人物'], '所在城市': ['景点', '城市'], '嘉宾': ['电视综艺', '人物'], '总部地点': ['企业', '地点'], 
                '人口数量': ['行政区', 'Number'], '代言人': ['企业/品牌', '人物'], '改编自': ['影视作品', '作品'], '校长': ['学校', '人物'], '丈夫': ['人物', '人物'], '主持人': ['电视综艺', '人物'], '主题曲': ['影视作品', '歌曲'], 
                '修业年限': ['学科专业', 'Number'], '作曲': ['歌曲', '人物'], '号': ['历史人物', 'Text'], '上映时间': ['影视作品', 'Date'], '票房': ['影视作品', 'Number'], '饰演': ['娱乐人物', '人物'], '配音': ['娱乐人物', '人物'], '获奖': ['娱乐人物', '奖项']
                }
}

df_nert = {
    'chinese': ['组织机构', '地点', '人物'],
    'english': ['PER', 'LOC', 'ORG', 'MISC'],
}
    
df_eet = {
    'chinese': {'灾害/意外-坠机': ['时间', '地点', '死亡人数', '受伤人数'], '司法行为-举报': ['时间', '举报发起方', '举报对象'], '财经/交易-涨价': ['时间', '涨价幅度', '涨价物', '涨价方'], '组织关系-解雇': ['时间', '解雇方', '被解雇人员'], '组织关系-停职': ['时间', '所属组织', '停职人员'], '财经/交易-加息': ['时间', '加息幅度', '加息机构'], '交往-探班': ['时间', '探班主体', '探班对象'], '人生-怀孕': ['时间', '怀孕者'], '组织关系-辞/离职': ['时间', '离职者', '原所属组织'], '组织关系-裁员': ['时间', '裁员方', '裁员人数'], '灾害/意外-车祸': ['时间', '地点', '死亡人数', '受伤人数'], 
                '人生-离婚': ['时间', '离婚双方'], '司法行为-起诉': ['时间', '被告', '原告'], '竞赛行为-禁赛': ['时间', '禁赛时长', '被禁赛人员', '禁赛机构'], '人生-婚礼': ['时间', '地点', '参礼人员', '结婚双方'], '财经/交易-涨停': ['时间', '涨停股票'], '财经/交易-上市': ['时间', '地点', '上市企业', '融资金额'], '组织关系-解散': ['时间', '解散方'], '财经/交易-跌停': ['时间', '跌停股票'], '财经/交易-降价': ['时间', '降价方', '降价物', '降价幅度'], '组织行为-罢工': ['时间', '所属组织', '罢工人数', '罢工人员'], '司法行为-开庭': ['时间', '开庭法院', '开庭案件'], 
                '竞赛行为-退役': ['时间', '退役者'], '人生-求婚': ['时间', '求婚者', '求婚对象'], '人生-庆生': ['时间', '生日方', '生日方年龄', '庆祝方'], '交往-会见': ['时间', '地点', '会见主体', '会见对象'], '竞赛行为-退赛': ['时间', '退赛赛事', '退赛方'], '交往-道歉': ['时间', '道歉对象', '道歉者'], '司法行为-入狱': ['时间', '入狱者', '刑期'], '组织关系-加盟': ['时间', '加盟者', '所加盟组织'], '人生-分手': ['时间', '分手双方'], '灾害/意外-袭击': ['时间', '地点', '袭击对象', '死亡人数', '袭击者', '受伤人数'], '灾害/意外-坍/垮塌': ['时间', '坍塌主体', '死亡人数', '受伤人数'], 
                '组织关系-解约': ['时间', '被解约方', '解约方'], '产品行为-下架': ['时间', '下架产品', '被下架方', '下架方'], '灾害/意外-起火': ['时间', '地点', '死亡人数', '受伤人数'], '灾害/意外-爆炸': ['时间', '地点', '死亡人数', '受伤人数'], '产品行为-上映': ['时间', '上映方', '上映影视'], '人生-订婚': ['时间', '订婚主体'], '组织关系-退出': ['时间', '退出方', '原所属组织'], '交往-点赞': ['时间', '点赞方', '点赞对象'], '产品行为-发布': ['时间', '发布产品', '发布方'], '人生-结婚': ['时间', '结婚双方'], '组织行为-闭幕': ['时间', '地点', '活动名称'], 
                '人生-死亡': ['时间', '地点', '死者年龄', '死者'], '竞赛行为-夺冠': ['时间', '冠军', '夺冠赛事'], '人生-失联': ['时间', '地点', '失联者'], '财经/交易-出售/收购': ['时间', '出售方', '交易物', '出售价格', '收购方'], '竞赛行为-晋级': ['时间', '晋级方', '晋级赛事'], '竞赛行为-胜负': ['时间', '败者', '胜者', '赛事名称'], '财经/交易-降息': ['时间', '降息幅度', '降息机构'], '组织行为-开幕': ['时间', '地点', '活动名称'], '司法行为-拘捕': ['时间', '拘捕者', '被拘捕者'], '交往-感谢': ['时间', '致谢人', '被感谢人'], '司法行为-约谈': ['时间', '约谈对象', '约谈发起方'], 
                '灾害/意外-地震': ['时间', '死亡人数', '震级', '震源深度', '震中', '受伤人数'], '人生-产子/女': ['时间', '产子者', '出生者'], '财经/交易-融资': ['时间', '跟投方', '领投方', '融资轮次', '融资金额', '融资方'], '司法行为-罚款': ['时间', '罚款对象', '执法机构', '罚款金额'], '人生-出轨': ['时间', '出轨方', '出轨对象'], '灾害/意外-洪灾': ['时间', '地点', '死亡人数', '受伤人数'], '组织行为-游行': ['时间', '地点', '游行组织', '游行人数'], '司法行为-立案': ['时间', '立案机构', '立案对象'], '产品行为-获奖': ['时间', '获奖人', '奖项', '颁奖机构'], '产品行为-召回': ['时间', '召回内容', '召回方']},
    'english': {'Justice:Appeal': ['Defendant', 'Adjudicator', 'Crime', 'Time', 'Place'], 'Justice:Extradite': ['Agent', 'Person', 'Destination', 'Origin', 'Crime', 'Time'], 'Justice:Acquit': ['Defendant', 'Adjudicator', 'Crime', 'Time', 'Place'], 'Life:Be-Born': ['Person', 'Time', 'Place'], 'Life:Divorce': ['Person', 'Time', 'Place'], 'Personnel:Nominate': ['Person', 'Agent', 'Position', 'Time', 'Place'], 'Life:Marry': ['Person', 'Time', 'Place'], 'Personnel:End-Position': ['Person', 'Entity', 'Position', 'Time', 'Place'], 
                'Justice:Pardon': ['Defendant', 'Prosecutor', 'Adjudicator', 'Crime', 'Time', 'Place'], 'Business:Merge-Org': ['Org', 'Time', 'Place'], 'Conflict:Attack': ['Attacker', 'Target', 'Instrument', 'Time', 'Place'], 'Justice:Charge-Indict': ['Defendant', 'Prosecutor', 'Adjudicator', 'Crime', 'Time', 'Place'], 'Personnel:Start-Position': ['Person', 'Entity', 'Position', 'Time', 'Place'], 'Business:Start-Org': ['Agent', 'Org', 'Time', 'Place'], 'Business:End-Org': ['Org', 'Time', 'Place'], 
                'Life:Injure': ['Agent', 'Victim', 'Instrument', 'Time', 'Place'], 'Justice:Fine': ['Entity', 'Adjudicator', 'Money', 'Crime', 'Time', 'Place'], 'Justice:Sentence': ['Defendant', 'Adjudicator', 'Crime', 'Sentence', 'Time', 'Place'], 'Transaction:Transfer-Money': ['Giver', 'Recipient', 'Beneficiary', 'Money', 'Time', 'Place'], 'Justice:Execute': ['Person', 'Agent', 'Crime', 'Time', 'Place'], 'Justice:Sue': ['Plaintiff', 'Defendant', 'Adjudicator', 'Crime', 'Time', 'Place'], 
                'Justice:Arrest-Jail': ['Person', 'Agent', 'Crime', 'Time', 'Place'], 'Justice:Trial-Hearing': ['Defendant', 'Prosecutor', 'Adjudicator', 'Crime', 'Time', 'Place'], 'Movement:Transport': ['Agent', 'Artifact', 'Vehicle', 'Price', 'Origin', 'Destination', 'Time'], 'Contact:Meet': ['Entity', 'Time', 'Place'], 'Personnel:Elect': ['Person', 'Entity', 'Position', 'Time', 'Place'], 'Business:Declare-Bankruptcy': ['Org', 'Time', 'Place'], 'Transaction:Transfer-Ownership': ['Buyer', 'Seller', 'Beneficiary', 'Artifact', 'Price', 'Time', 'Place'], 
                'Justice:Release-Parole': ['Person', 'Entity', 'Crime', 'Time', 'Place'], 'Conflict:Demonstrate': ['Entity', 'Time', 'Place'], 'Contact:Phone-Write': ['Entity', 'Time'], 'Justice:Convict': ['Defendant', 'Adjudicator', 'Crime', 'Time', 'Place'], 'Life:Die': ['Agent', 'Victim', 'Instrument', 'Time', 'Place']},
}

re_s1_p = {
    'chinese': '''给定的句子为："{}"\n\n给定关系列表：{}\n\n在这个句子中，可能包含了哪些关系？\n请给出关系列表中的关系。\n如果不存在则回答：无\n按照元组形式回复，如 (关系1, 关系2, ……)：''',
    'english': '''The given sentence is "{}"\n\nList of given relations: {}\n\nWhat relations in the given list might be included in this given sentence?\nIf not present, answer: none.\nRespond as a tuple, e.g. (relation 1, relation 2, ......):''',
}

re_s2_p = {
    'chinese': '''根据给定的句子，两个实体的类型分别为（{}，{}）且之间的关系为{}，请找出这两个实体，如果有多组，则按组全部列出。\n如果不存在则回答：无\n按照表格形式回复，表格有两列且表头为（{}，{}）：''',
    'english': '''According to the given sentence, the two entities are of type ('{}', '{}') and the relation between them is '{}', find the two entities and list them all by group if there are multiple groups.\nIf not present, answer: none.\nRespond in the form of a table with two columns and a header of ('{}', '{}'):''',
}

# -------------
ner_s1_p = {
    'chinese': '''给定的句子为："{}"\n\n给定实体类型列表：{}\n\n在这个句子中，可能包含了哪些实体类型？\n如果不存在则回答：无\n按照元组形式回复，如 (实体类型1, 实体类型2, ……)：''',
    'english': '''The given sentence is "{}"\n\nGiven a list of entity types: {}\n\nWhat entity types may be included in this sentence?\nIf not present, answer: none.\nRespond as a list, e.g. [entity type 1, entity type 2, ......]:'''
}

ner_s2_p = {
    'chinese': '''根据给定的句子，请识别出其中类型是"{}"的实体。\n如果不存在则回答：无\n按照表格形式回复，表格有两列且表头为（实体类型，实体名称）：''',
    'english': '''According to the given sentence, please identify the entity whose type is "{}".\nIf not present, answer: none.\nRespond in the form of a table with two columns and a header of (entity type, entity name):'''
}

# --------------------
ee_s1_p = {
    'chinese': '''给定的句子为："{}"\n\n给定事件类型列表：{}\n\n在这个句子中，可能包含了哪些事件类型？\n请给出事件类型列表中的事件类型。\n如果不存在则回答：无\n按照元组形式回复，如 (事件类型1, 事件类型2, ……)：''',
    'english': '''The given sentence is "{}"\n\nGiven a list of event types: {}\n\nWhat event types in the given list might be included in this given sentence?\nIf not present, answer: none.\nRespond as a tuple, e.g. (event type 1, event type 2, ......):'''
}
    
ee_s2_p = {
    'chinese': '''事件类型"{}"对应的论元角色列表为：{}。\n在给定的句子中，根据论元角色提取出事件论元。\n如果论元角色没有相应的论元内容，则论元内容回答：无\n按照表格形式回复，表格有两列且表头为（论元角色，论元内容）：''',
    'english': '''The list of argument roles corresponding to event type "{}" is: {}.\nIn the given sentence, extract event arguments according to their role.\nIf the argument role does not have a corresponding argument content, then the argument content answer: None\nRespond in the form of a table with two columns and a header of (argument role, argument content):'''
}     


def chat_re(inda, chatbot):
    print("---RE---")
    mess = [{"role": "system", "content": "You are a helpful assistant."},] # chatgpt对话历史

    typelist = inda['type']
    sent = inda['sentence']
    lang = inda['lang']

    out = [] # 输出列表 [(e1,r1,e2)]

    try:
        print('---stage1---')
        # 构造prompt
        stage1_tl = list(typelist.keys())
        s1p = re_s1_p[lang].format(sent, str(stage1_tl))
        print(s1p)

        # 请求chatgpt
        mess.append({"role": "user", "content": s1p})
        text1 = chatbot(mess)
        mess.append({"role": "assistant", "content": text1})
        print(text1)

        # 正则提取结果
        res1 = re.findall(r'\(.*?\)', text1)
        print(res1)
        if res1!=[]:
            rels = [temp[1:-1].split(',') for temp in res1]
            rels = list(set([re.sub('[\'"]','', j).strip() for i in rels for j in i]))
            #print(rels)
        else: # 说明正则没提取到，可能是单个类型的情况
            text1 = text1.strip().rstrip('.')
            rels = [text1]
        print(rels)
    except Exception as e:
        print(e)
        print('re stage 1 none out or error')
        return ['error-stage1:' + str(e)], mess

    print('---stage2')
    try:
        for r in rels:
            if r in typelist:
                # 构造prompt
                st, ot = typelist[r]
                s2p = re_s2_p[lang].format(st, ot, r, st, ot)
                print(s2p)

                # 请求chatgpt
                mess.append({"role": "user", "content": s2p})
                text2 = chatbot(mess)
                mess.append({"role": "assistant", "content": text2})
                print(text2)

                # 正则提取结果
                res2 = re.findall(r'\|.*?\|.*?\|', text2)
                print(res2)

                if res2==[]:
                    res2 = re.findall(r'.*\|.*', text2)
                    print(res2)

                # 进一步处理结果
                count=0
                for so in res2:
                    count+=1
                    if count <=2: # 过滤表头
                        continue

                    so = so.strip('|').split('|')
                    so = [re.sub('[\'"]','', i).strip() for i in so]
                    if len(so)==2:
                        s, o = so
                        #if st in s and ot in o or '---' in s and '---' in o:
                        #    continue 
                        out.append((s, r, o))
                #break
    
    except Exception as e:
        print(e)
        print('re stage 2 none out or error')
        if out == []:
            out.append('error-stage2:' + str(e))
        return out, mess

    if out == []:
        out.append('none-none')
    else:
        out = list(set(out))
    
    print(mess)
    # out = [('滴答', '歌手', '陈思成'), ('兰花指', '歌手', '阿里郎'), ('滴答', '歌手', '张碧晨')]
    return out, mess

def chat_ner(inda, chatbot):
    print("---NER---")
    mess = [{"role": "system", "content": "You are a helpful assistant."},] # chatgpt对话历史

    typelist = inda['type']
    sent = inda['sentence']
    lang = inda['lang']

    out = [] # 输出列表 [(e1,et1)]

    try:
        print('---stage1---')
        # 构造prompt
        stage1_tl = typelist
        s1p = ner_s1_p[lang].format(sent, str(stage1_tl))
        print(s1p)

        # 请求chatgpt
        mess.append({"role": "user", "content": s1p})
        text1 = chatbot(mess)
        mess.append({"role": "assistant", "content": text1})
        print(text1)

        # 正则提取结果, ner特殊
        if lang == 'chinese':
            res1 = re.findall(r'\(.*?\)', text1)
        else:
            res1 = re.findall(r'\[.*?\]', text1)
        print(res1)
        if res1!=[]:
            rels = [temp[1:-1].split(',') for temp in res1]
            rels = list(set([re.sub('[\'"]','', j).strip() for i in rels for j in i]))
            #print(rels)
        else: # 说明正则没提取到，可能是单个类型的情况
            text1 = text1.strip().rstrip('.')
            rels = [text1]
        print(rels)
    except Exception as e:
        print(e)
        print('ner stage 1 none out or error')
        return ['error-stage1:' + str(e)], mess

    print('---stage2')
    try:
        for r in rels:
            if r in typelist:
                # 构造prompt
                s2p = ner_s2_p[lang].format(r)
                print(s2p)

                # 请求chatgpt
                mess.append({"role": "user", "content": s2p})
                text2 = chatbot(mess)
                mess.append({"role": "assistant", "content": text2})
                print(text2)

                # 正则提取结果
                res2 = re.findall(r'\|.*?\|.*?\|', text2)
                print(res2)

                if res2==[]:
                    res2 = re.findall(r'.*\|.*', text2)
                    print(res2)

                # 进一步处理结果
                count=0
                for so in res2:
                    count+=1
                    if count <=2: # 过滤表头
                        continue

                    so = so.strip('|').split('|')
                    so = [re.sub('[\'"]','', i).strip() for i in so]
                    if len(so)==2:
                        s, o = so
                        #if st in s and ot in o or '---' in s and '---' in o:
                        #    continue 
                        out.append((o, r))
    
    except Exception as e:
        print(e)
        print('ner stage 2 none out or error')
        if out == []:
            out.append('error-stage2:' + str(e))
        return out, mess
    

    if out == []:
        out.append('none-none')
    else:
        out = list(set(out))
    
    print(mess)
    #out = [('陈思成', 'PER'), ('北京', 'LOC')]
    return out, mess

def chat_ee(inda, chatbot):
    print("---EE---")
    mess = [{"role": "system", "content": "You are a helpful assistant."},] # chatgpt对话历史

    typelist = inda['type']
    sent = inda['sentence']
    lang = inda['lang']

    out = [] # 输出列表 [(e1,r1,e2)]

    try:
        print('---stage1---')
        # 构造prompt
        stage1_tl = list(typelist.keys())
        s1p = ee_s1_p[lang].format(sent, str(stage1_tl))
        print(s1p)

        # 请求chatgpt
        mess.append({"role": "user", "content": s1p})
        text1 = chatbot(mess)
        mess.append({"role": "assistant", "content": text1})
        print(text1)

        # 正则提取结果
        res1 = re.findall(r'\(.*?\)', text1)
        print(res1)
        if res1!=[]:
            rels = [temp[1:-1].split(',') for temp in res1]
            rels = list(set([re.sub('[\'"]','', j).strip() for i in rels for j in i]))
            #print(rels)
        else: # 说明正则没提取到，可能是单个类型的情况
            text1 = text1.strip().rstrip('.')
            rels = [text1]

        print(rels)
    except Exception as e:
        print(e)
        print('re stage 1 none out or error')
        return ['error-stage1:' + str(e)], mess
    
    print('---stage2')
    try:
        for r in rels:
            if r in typelist:
                # 构造prompt
                t = typelist[r]
                s2p = ee_s2_p[lang].format(r, t)
                print(s2p)

                # 请求chatgpt
                mess.append({"role": "user", "content": s2p})
                text2 = chatbot(mess)
                mess.append({"role": "assistant", "content": text2})
                print(text2)

                # 正则提取结果
                res2 = re.findall(r'\|.*?\|.*?\|', text2)
                print(res2)
                
                if res2==[]:
                    res2 = re.findall(r'.*\|.*', text2)
                    print(res2)

                # 进一步处理结果
                single_out = {r: {}}
                count=0
                for so in res2:
                    count+=1
                    if count <=2: # 过滤表头
                        continue

                    so = so.strip('|').split('|')
                    so = [re.sub('[\'"]','', i).strip() for i in so]
                    if len(so)==2:
                        s, o = so
                        #if st in s and ot in o or '---' in s and '---' in o:
                        #    continue 
                        single_out[r][s] = o

                out.append(single_out)
                #break
    
    except Exception as e:
        print(e)
        print('re stage 2 none out or error')
        if out == []:
            out.append('error-stage2:' + str(e))
        return out, mess

    if out == []:
        out.append('none-none')
    
    print(mess)
    #out = [{'晋级':{'晋级方': '阿根廷', '时间': '2022年'}}]
    return out, mess

# 封装openai Create,实现换key功能
with open("tokens.txt", "r") as f:
    keys = f.readlines()
    keys = [key.strip() for key in keys]

all_keys = itertools.cycle(keys)

def create(**args):
    global all_keys
    openai.api_key = next(all_keys)

    try:
        result = openai.ChatCompletion.create(**args)
    except openai.error.RateLimitError:
        result = create(**args)
    
    return result


def chat(mess):
    #openai.proxy = 'http://127.0.0.1:10809' # 根据自己服务器的vpn情况设置proxy；如果是在自己电脑线下使用，可以在电脑上开vpn然后不加此句代码。
    openai.api_base = "https://chatie.deno.dev/v1" #或者利用反向代理openai.com（代理获取：https://github.com/justjavac/openai-proxy）（注释掉上面那句代码）
    responde = create(
        model="gpt-3.5-turbo",
        messages=mess
    )

    res = responde['choices'][0]['message']['content']
    return res


def chatie(input_data):
    print('input data type:{}'.format(type(input_data)))
    print('input data:{}'.format(input_data))

    # 参数处理，默认参数
    task = input_data['task']
    lang = input_data['lang']
    typelist = input_data['type']
    access = input_data['access']

    ## account
    if access=="":
        print('using default access token')
        tempes = random.choice(df_access)
        input_data['access'] = tempes[1]+tempes[0][1:]

    ## chatgpt
    try:
        #openai.api_key = input_data['access']
        chatbot = chat
    except Exception as e:
        print('---chatbot---')
        print(e)
        input_data['result'] = ['error-chatbot']
        return input_data # 没必要进行下去
    
    ## typelist, 空或者出错就用默认的
    try:
        typelist = ast.literal_eval(typelist)
        input_data['type'] = typelist
    except Exception as e:
        print('---typelist---')
        print(e)
        print(typelist)
        print('using default typelist')
        if task == 'RE':
            typelist = df_ret[lang]
            input_data['type'] = typelist
        elif task == 'NER':
            typelist = df_nert[lang]
            input_data['type'] = typelist
        else:
            typelist = df_eet[lang]
            input_data['type'] = typelist

    # get output from chatgpt        
    if task == 'RE':
        input_data['result'], input_data['mess'] =  chat_re(input_data, chatbot)
    elif task == 'NER':
        input_data['result'], input_data['mess'] =  chat_ner(input_data, chatbot)
    else:
        input_data['result'], input_data['mess'] =  chat_ee(input_data, chatbot)
    
    print(input_data)

    with open('access_record.json', 'a') as fw:
        fw.write(json.dumps(input_data, ensure_ascii=False)+'\n')

    return input_data

if __name__=="__main__":
    p = '''第五部：《如懿传》《如懿传》是一部古装宫廷情感电视剧，由汪俊执导，周迅、霍建华、张钧甯、董洁、辛芷蕾、童瑶、李纯、邬君梅等主演'''
    #p = '''Mr. Johnson retired before the 2005 season and briefly worked as a football analyst for WBZ-TV in Boston .'''
    #'''Four other Google executives the chief financial officer , George Reyes ; the senior vice president for business operations , Shona Brown ; the chief legal officer , David Drummond ; and the senior vice president for product management , Jonathan Rosenberg earned salaries of $ 250,000 each .'''
    # -------
    #p = '''中国共产党创立于中华民国大陆时期，由陈独秀和李大钊领导组织。'''
    #p = '''James worked for Google in Beijing, the capital of China.'''
    # --------
    #p = '''在2022年卡塔尔世界杯决赛中，阿根廷以点球大战险胜法国。'''
    #p = '''Yesterday Bob and his wife got divorced in Guangzhou.'''

    ind = {
      "sentence": p,
      "type": "",
      "access": "",
      "task": "RE",
      "lang": "chinese",
    }
    post_data=chatie(ind)
    print(post_data)
