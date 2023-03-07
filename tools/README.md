# ChatIETool
**NOTICE:** because official api is not available in domestic, so we use api from [revChatGPT](https://github.com/acheong08/ChatGPT) and v1 version. But it's **too slow**, so we advise you use the tool offline for study. We will update the api further in the future (**TODO**).  
**Corresponding:**  
- Paper: ["Zero-Shot Information Extraction via Chatting with ChatGPT"](https://arxiv.org/pdf/2302.10205.pdf) 

![](https://img.shields.io/badge/Languages-%20English%2C%20Chinese-brightgreen) 
![](https://img.shields.io/badge/ChatGPT-IETool%2C%20zeroshot-blue)  
we also provide a IE tool based on GPT3.5, you can see in [GPT4IE](https://github.com/cocacola-lab/GPT4IE)
## Description
ChatIE (Zero-Shot Information Extraction via Chatting with ChatGPT) is a open-source and powerful IE tool [demo](http://124.221.16.143:5000/). Enhanced by ChatGPT and prompting, it aims to automatically extract **structured information** from a **raw sentence** and make a valuable in-depth analysis of the input sentence. Harnessing valuable structured information helps corporations make incisive and business–improving decisions.  
![Present](examples/RE-chi.gif)

We support the following functions:
| Task | Name| Lauguages |
|---| ---| --- |
| RE | entity-relation joint extraction | Chinese, English|
|NER |named entity recoginzation | Chinese, English|
|EE| event extraction | Chinese, English|

### RE
This task aims to extract triples from plain texts, such as **(China, capital, Beijing)** , **(《如懿传》, 主演, 周迅)**.
#### Input
- sentence: a plain text.
- relation type list (rtl)* : {'relation type 1': ['subject1', 'object1'], 'relation type 2': ['subject2', 'object2'], ...}

PS: * denote optional, we set default value for them. But for better extraction, you should specify the three list according to application scenarios.
#### Examples
**sentence:** Four other Google executives the chief financial officer , George Reyes ; the senior vice president for business operations , Shona Brown ; the chief legal officer , David Drummond ; and the senior vice president for product management , Jonathan Rosenberg earned salaries of $ 250,000 each .  
**rtl:** default, see file "default-types"  
**ouptut:**  
![ouptut](examples/RE-eng.png)  

**sentence:** 第五部：《如懿传》《如懿传》是一部古装宫廷情感电视剧，由汪俊执导，周迅、霍建华、张钧甯、董洁、辛芷蕾、童瑶、李纯、邬君梅等主演。  
**rtl:** default, see file "default-types"  
**ouptut:**  
![ouptut](examples/RE-zh.png) 

---
### NER
This task aims to extract entities from plain texts, such as **(LOC, Beijing)** , **(人物, 周恩来)**.
#### Input
- sentence: a plain text.
- entity type list (etl)* : ['entity type 1', 'entity type 2', ...]  

#### Examples
**sentence:** James worked for Google in Beijing, the capital of China. 
**etl:**  ['LOC', 'MISC', 'ORG', 'PER']  
**ouptut:**  
![ouptut](examples/NER-eng.png)  

**sentence:** 中国共产党创立于中华民国大陆时期，由陈独秀和李大钊领导组织。   
**etl:** ['组织机构', '地点', '人物']  
**ouptut:**  
![ouptut](examples/NER-zh.png) 

---
### EE
This task aims to extract event from plain texts, such as **{Life-Divorce: {Person: Bob, Time: today, Place: America}}** , **{竞赛行为-晋级: {时间: 无, 晋级方: 西北狼, 晋级赛事: 中甲榜首之争}}**.
#### Input
- sentence: a plain text.
- event type list (etl)* : {'event type 1': ['argument role 1', 'argument role 2', ...], ...}  

**sentence:** Yesterday Bob and his wife got divorced in Guangzhou.  
**etl:**  default, see file "default-types"     
**ouptut:**  
![ouptut](examples/EE-eng.png)  

**sentence:** 在2022年卡塔尔世界杯决赛中，阿根廷以点球大战险胜法国。  
**etl:** default, see file "default-types"  
**ouptut:**  
![ouptut](examples/EE-zh.png) 

---

## Setup

1. cd `front-end` and Run `npm install` to download required dependencies.  
2. Run `npm run start`. GPT4IE should open up in a new browser tab.  
3. cd `back-end` and Run `python run.py`.  
4. note: node-version v14.17.4  npm-version 9.6.0  
5. we use api from [revChatGPT](https://github.com/acheong08/ChatGPT) and v1 version,
you can see how to get access token.

