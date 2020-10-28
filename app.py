import os
from flask import Flask, render_template, request, session, redirect,flash,url_for
from werkzeug.utils import secure_filename
# from flask_mail import Mail
import json
import os
import math
from datetime import datetime
from flask_caching import Cache
from flask import jsonify
from flask import json
import requests
from flask import send_from_directory
import docx
import docx2txt
import sys 
import math 
import pdfplumber # pip install tika
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyPDF2 import PdfFileReader
from flask import Flask
import re
import json
import jinja2
#from spellchecker import SpellChecker
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from pickle import dump, load
from nltk.corpus import brown
from itertools import dropwhile
from nltk import word_tokenize, pos_tag
# =============================================================================
# from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams
# from pdfminer.pdfpage import PDFPage
from io import StringIO
# =============================================================================
#import codecs
import pandas as pd
from pdfminer.high_level import extract_text
import spacy
nlp = spacy.load('en_core_web_sm')
from spacy.matcher import Matcher
import datetime
import numpy as np
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt

import base64
from io import BytesIO
import plotly.io as pio

#spell = SpellChecker()
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('brown')
nltk.download('punkt')

#nltk.download('all')

UPLOAD_FOLDER='./uploads/'
ALLOWED_EXTENSIONS ={'pdf','docx','doc','png'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.secret_key = 'development key'

# app.config['MYSQL_HOST'] = 'dataly.database.windows.net'
# app.config['MYSQL_USER'] = 'dataly'
# app.config['MYSQL_PASSWORD'] = 'uG5qMZxv'
# app.config['MYSQL_DB'] = 'dataly'
#mysql = MySQL(app)





def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower()in ALLOWED_EXTENSIONS



keyword = "N"
text_main=""
length = 0
match=0
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    try:
        f_name = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        # return f_name
        global text_main,length,match,keyword
        file_name = f_name
        print(f_name)
        impact = 0
        pres =0
        text_main = ""
        edu_msg =0 
        vol_msg=0
        pro_msg=0
        jd_msg=""
        if(file_name[-3:]=="pdf"):
            print("File is in pdf")
            jd_score=pdf(file_name)
            #print(text_main)
            #text_main=re.sub(r'[^\\x00-\x7f]',r'', text_main)
            #text_main=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', text_main)
            # if (float(match) == 0):
            #     jd_msg = "If it shows zero, probably you have not specified the JD in it field. Try adding a JD to check how accurately your resume matches with the Job."
            # elif (float(match) < 50):
            #     jd_msg = "With " +str(match) + "% score you might need to add more skills related to the Job you have been looking for. Try aiming for a score above 80%"
            # else:
            #     jd_msg ="With " +str(match) + "% score you seem to be an apt fit for the Job you have been looking for. "
        elif(file_name[-4:] == "docx"):
            print("File is in docx")
            jd_score=docx1(file_name)
            #text_main=re.sub(r'[^\x00-\x7f]',r'', text_main)
            # if (float(match) == 0.0):
            #     jd_msg = "If it shows zero, probably you have not specified the JD in it field. Try adding a JD to check how accurately your resume matches with the Job."
            # elif (float(match) < 50):
            #     jd_msg = "With " +str(match) + " % score you might need to add more skills related to the Job you have been looking for. Try aiming for a score above 80%"
            # else:
            #     jd_msg ="With " +str(match) + " % score you seem to be an apt fit for the Job you have been looking for. "
        else:
            print("Invalid Fileformat - Supported docx or pdf")
            return render_template('unsupported.html')
        #print (text_main)
        
        text_count=text_main.split(" ")
        word_count=len(text_count)
        liness=[]
        line=""
        line1=[]
    # =============================================================================
    #     for i in text_main:
    #             
    #         if(i!='\n'):
    #             line+=i
    #         else:
    #             liness.append(line)
    #             line=""
    #         
    #     for line in liness:
    #         if len(line)!=0:
    #             line1.append(line)
    # =============================================================================
    # =============================================================================
        if(file_name[-4:] == "docx" ):
            for i in text_main:
                
                if(i!='\n'):
                    line+=i
                else:
                    liness.append(line)
                    line=""
            
            for line in liness:
                if len(line)!=0:
                    line1.append(line)
        elif(file_name[-3:]=="pdf"):
            liness=text_main.split("\\n")
    # =============================================================================
    #         for i in range(len(text_main)-1):
    #             if(text_main[i]=="\\" ):
    #                if(text_main[i+1]=='n'):
    #                    liness.append(line)
    #                    line=""
    #                else:
    #                    line+=text_main[i]
    # =============================================================================
                    
            
            for line in liness:
                if len(line)!=0:
                    line1.append(line)

        
        
        phone=re.findall(r"(?<!\d)\d{10}(?!\d)", text_main)
        email=re.findall(r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)",text_main)
        #print(email)
        links= re.findall(r"(^(http\:\/\/|https\:\/\/)?([a-z0-9][a-z0-9\-]*\.)+[a-z0-9][a-z0-9\-]*)",text_main)
        mlink=[]
        for link in links:
            if 'facebook' in link:
                mlink.append(link)
            elif 'github' in link:
                mlink.append(link)
            elif 'linkedin' in link:
                mlink.append(link)
            else:
                links.remove(link)
        links=list(set(mlink))
        section=[]
        sections={}
        line2=[]
        titles=['education','Licensures', 'Professional Qualification', 'academic qualification', 'Educational Qualification', 'academia', 'education and professional development', 'academic credentials', 'educational summary', 'academic profile', 'Experience', 'work experience', 'Job Titles held', 'Position Description and purpose', 'Professional Experience', 'Professional Summary', 'Profile', 'Qualifications', 'Employment History', 'history', 'previous employment', 'organisational experience', 'employers', 'positions of responsibility','Position of Responsibilities', 'employment scan', 'past experience', 'organizational experience', 'career', 'experience and qualification summary', 'relevant experience', 'experience summary', 'career synopsis', 'career timeline', 'banking IT experience', 'AML & FCM Suite Experience', 'employment details', 'Skill','skills', 'Technical Skills', 'Soft Skills', 'Key Skills', 'Design Skills', 'Expertise', 'Abilities', 'Area of Expertise', 'Key attributes', 'Computer Skills', 'IT Skills', 'Technical Expertise', 'Technical Skills Set', 'Functional Skill Set', 'functional skills', 'strengths', 'areas of expertise', 'banking knowledge', 'Award', 'Honours and awards', 'Key achievements', 'Accomplishments', 'Highlights', 'Affiliations', 'Achievements', 'Extra Curricular activities and achievements', 'awards and recognition','awards/achievements', 'Certificate', 'Most proud of', 'Specialization', 'Certifications', 'Certification/training','Coursework','other credentials', 'professional accomplishments', 'certification & trainings', 'scholastics', 'professional credentials and certifications','Project','projects', 'Additional Activities', 'Activities', 'Major Tasks', 'Responsibilities', 'key accountabilities', 'Contributions', 'Personal Projects', 'Key Contributions', 'Strategic Planning and execution', 'Academic projects', 'Key projects', 'projects/trainings', 'key implementations','Volunteer', 'Volunteer Experience', 'Affiliations', 'Misc','Extra Curricular Activities', 'Community Service','EDUCATIONAL BACKGROUND','INTERNSHIPS EXPERIENCE','WINNING PORTFOLIO','AWARDS & RECOGNITIONS','CORE COMPETENCIES','PROJECTS ADMINISTERED','TECHNICAL SKILLS','CERTIFICATIONS','VOLUNTEERING','PERSONAL DOSSIER','Licensure', 'Professional Qualifications', 'academic qualifications', 'academics qualification', 'academics qualifications',  'Educational Qualifications', 'education and professional developments', 'academic credential', 'academics credential', 'academics credentials', 'educational summaries', 'academic profiles', 'academics profile','Experiences', 'work experiences', 'Position Descriptions and purpose', 'Positions Description and purpose', 'Positions Descriptions and purpose', 'Professional Experiences', 'Profiles', 'Qualification', 'Employment Histories', 'previous employments', 'organisational experiences', 'organizational experiences', 'organizational experience', 'employer', 'positions of responsibilities', 'position of responsibility', 'position of responsibilities', 'employment scans', 'past experiences', 'organizational experiences', 'organisational experience', 'organisational experiences', 'careers', 'experiences and qualifications summary', 'experience and qualifications summary', 'experiences and qualification summary', 'relevant experiences', 'career timelines', 'banking IT experiences', 'AML & FCM Suite Experiences', 'employment details', 'employment detail','Skills', 'Technical Skill', 'Soft Skill', 'Key Skill', 'Design Skill', 'Expertises', 'Ability', 'Areas of Expertises', 'Areas of Expertise', 'Area of Expertises', 'Key attribute', 'Computer Skill', 'IT Skill', 'Technical Expertises', 'Technical Skill Set', 'Technical Skill Sets', 'Functional Skills Set', 'Functional Skill Sets', 'Functional Skills Sets', 'functional skill', 'strength', 'area of expertise', 'area of expertises','Awards', 'Key achievement', 'Accomplishment', 'Highlight', 'Affiliation', 'Achievement', 'Extra Curricular activities and achievements',  'Extra Curricular activity and achievements',  'Extra Curricular activities and achievement',  'Extra Curricular activity and achievement', 'awards and recognitions',  'award and recognition',  'award and recognitions', 'Certificates', 'Specializations', 'Certification', 'Certifications/trainings', 'Certifications/training', 'Certification/trainings', 'other credential', 'professional accomplishment', 'certifications & trainings', 'certifications & training', 'certification & training', 'scholastic', 'professional credential and certification', 'professional credential and certifications', 'professional credentials and certification','Project', 'Additional Activity', 'Activity', 'Major Task', 'Responsibily', 'key accountability', 'Contribution', 'Personal Project', 'Key Contribution', 'Strategic Plannings and executions', 'Strategic Plannings and execution', 'Strategic Planning and executions', 'Academic project', 'Key project', 'project/training', 'projects/training', 'project/trainings', 'key implementation','Volunteer', 'Volunteer Experiences', 'Affiliation', 'Community Services' ]
        titles1=[x.lower() for x in titles]
        for i in line1:
            if i[-1]==" ":
                line2.append(i[:-1])
            else:
                line2.append(i)
        #print(titles1)
        line1=line2
        temp = '\t'.join(titles1)
        for x in line1:
            #print(x.lower() in titles1, x.lower())
            global keyword
            if(x==line1[-1]):
            
                section.append(x)
                sections[keyword] = section
                keyword = x
                    #print(sections)
                section =[]
                break
            elif x.lower() not in temp:
                section.append(x)
                #print(x)
                #print(section)
            elif (len(x.split(" "))>=4):
                section.append(x)
                #print(section)  
            
                
            else :
                if(len(section)!=0):
                    sections[keyword] = section
                    keyword = x
                    #print(sections)
                    section =[]
                else:
                    sections[keyword]=[]
                    keyword=x
                    section =[]
                    #print(sections)
        #print(sections.keys())
        sections['phone']=list(set(phone))
        sections['links']=mlink
        if (len(mlink) != 0):
            impact+=5
        #imp_sec=["education","experience","expertise","role","career","skill","award","certificat","projects",'volunteer']
        ed_list=['Education', 'Education Details','Licensures', 'Professional Qualification', 'academic qualification', 'Educational Qualification', 'academia', 'education and professional development', 'academic credentials', 'educational summary', 'academic profile','EDUCATIONAL BACKGROUND','Licensure', 'Professional Qualifications', 'academic qualifications', 'academics qualification', 'academics qualifications',  'Educational Qualifications', 'education and professional developments', 'academic credential', 'academics credential', 'academics credentials', 'educational summaries', 'academic profiles', 'academics profile']
        ex_list=['Experience', 'Experience Details','work experience', 'Job Titles held', 'Position Description and purpose', 'Professional Experience', 'Professional Summary', 'Profile', 'Qualifications', 'Employment History', 'history', 'previous employment', 'organisational experience', 'employers', 'positions of responsibility', 'employment scan','past experience', 'organizational experience', 'career', 'experience and qualification summary', 'relevant experience', 'experience summary', 'career synopsis', 'career timeline', 'banking IT experience', 'AML & FCM Suite Experience', 'employment details','INTERNSHIPS EXPERIENCE','Experiences', 'work experiences', 'Position Descriptions and purpose', 'Positions Description and purpose', 'Positions Descriptions and purpose', 'Professional Experiences', 'Profiles', 'Qualification', 'Employment Histories', 'previous employments', 'organisational experiences', 'organizational experiences', 'organizational experience', 'employer', 'positions of responsibilities', 'position of responsibility', 'position of responsibilities', 'employment scans', 'past experiences', 'organizational experiences', 'organisational experience', 'organisational experiences', 'careers', 'experiences and qualifications summary', 'experience and qualifications summary', 'experiences and qualification summary', 'relevant experiences', 'career timelines', 'banking IT experiences', 'AML & FCM Suite Experiences', 'employment details', 'employment detail', 'career progression']
        sk_list=['Skill', 'Technical Skills', 'Soft Skills', 'Key Skills', 'Design Skills', 'Expertise', 'Abilities', 'Area of Expertise', 'Key attributes', 'Computer Skills', 'IT Skills', 'Technical Expertise', 'Technical Skills Set', 'Functional Skill Set', 'functional skills', 'strengths', 'areas of expertise', 'banking knowledge','WINNING PORTFOLIO','CORE COMPETENCIES','TECHNICAL SKILLS','skills','Skills', 'Technical Skill', 'Soft Skill', 'Key Skill', 'Design Skill', 'Expertises', 'Ability', 'Areas of Expertises', 'Areas of Expertise', 'Area of Expertises', 'Key attribute', 'Computer Skill', 'IT Skill', 'Technical Expertises', 'Technical Skill Set', 'Technical Skill Sets', 'Functional Skills Set', 'Functional Skill Sets', 'Functional Skills Sets', 'functional skill', 'strength', 'area of expertise', 'area of expertises']
        aw_list=['Award' , 'Achievement Details','Honours and awards', 'Key achievements', 'Accomplishments', 'Highlights', 'Affiliations', 'Achievements', 'Extra Curricular activities and achievements', 'awards and recognition','AWARDS & RECOGNITIONS','awards','achievements','Awards', 'Key achievement', 'Accomplishment', 'Highlight', 'Affiliation', 'Achievement', 'Extra Curricular activities and achievements',  'Extra Curricular activity and achievements',  'Extra Curricular activities and achievement',  'Extra Curricular activity and achievement', 'awards and recognitions',  'award and recognition',  'award and recognitions']
        ce_list=['Certificate', 'Certification Details','Most proud of', 'Specialization', 'Certifications', 'Certification/training', 'other credentials', 'professional accomplishments', 'certification & trainings', 'scholastics', 'professional credentials and certifications','CERTIFICATION','coursework', 'competencies', 'Certificates', 'Specializations', 'Certification', 'Certifications/trainings', 'Certifications/training', 'Certification/trainings', 'other credential', 'professional accomplishment', 'certifications & trainings', 'certifications & training', 'certification & training', 'scholastic', 'professional credential and certification', 'professional credential and certifications', 'professional credentials and certification',  'key accountability', 'Contribution', 'Personal Project', 'Key Contribution', 'Strategic Plannings and executions', 'Strategic Plannings and execution', 'Strategic Planning and executions',]
        pe_list=['Project', 'Project Details','Additional Activities', 'Activities', 'Major Tasks', 'Responsibilities', 'key accountabilities', 'Contributions', 'Personal Projects', 'Key Contributions', 'Strategic Planning and execution', 'Academic projects', 'Key projects', 'projects/trainings', 'key implementations','PROJECTS ADMINISTERED','projects','Project', 'Additional Activity', 'Activity', 'Major Task', 'Responsibily', 'key accountability', 'Contribution', 'Personal Project', 'Key Contribution', 'Strategic Plannings and executions', 'Strategic Plannings and execution', 'Strategic Planning and executions', 'Academic project', 'Key project', 'project/training', 'projects/training', 'project/trainings', 'key implementation','Additional Activity', 'Activity', 'Major Task', 'Responsibily', 'Academic project', 'Key project', 'project/training', 'projects/training', 'project/trainings', 'key implementation']
        vo_list=['Volunteer', 'Volunteer Details','Volunteer Experience', 'Affiliations', 'Misc', 'Community Service','VOLUNTEERING','extra curricular activities','EXTRA-CURRICULAR INVOLVEMENT','Volunteer', 'Volunteer Experiences', 'Affiliation', 'Community Services']
        ed1_list=[x.lower() for x in ed_list]
        temp_ed= '\t'.join(ed1_list)
        ex1_list=[x.lower() for x in ex_list]
        temp_ex='\t'.join(ex1_list)
        sk1_list=[x.lower() for x in sk_list]
        temp_sk='\t'.join(sk1_list)
        aw1_list=[x.lower() for x in aw_list]
        temp_aw='\t'.join(aw1_list)
        ce1_list=[x.lower() for x in ce_list]
        temp_ce='\t'.join(ce1_list)
        pe1_list=[x.lower() for x in pe_list]
        temp_pe='\t'.join(pe1_list)
        vo1_list=[x.lower() for x in vo_list]
        temp_vol='\t'.join(vo1_list)
        #print(vo1_list)
        score = 0
        msg = []
        edu=0
        ed=0
        ex=0
        sk=0
        aw=0
        ce=0
        pe=0
        vo=0
        ed_date_format_list=[0,0]
        ex_date_format_list=[0,0]
        ach_msg = 0 #achievement variable message
        cert_msg = 0 #certification message flag
        sections['edu_year']=""
        sections['exp_year']=""
        sections['paragraph']=0
        checkfornos=0
        alphanum=""
        checkfornos2=0
        #print(sections)
        for key in sections.keys():
            #print(repr(key))
            #for sec in titles1:
                #if sec == key.lower():
                    #print(sec,type(sec),"Hi")
            for i in ed1_list:
                if(i in key.lower() and ed==0 and key.lower()!='n'):
                    score +=10
                    pres+=10
                    edu = 1
                    ed=1
                    edu_msg =1
                    ed_date_format_list=date_format(sections[key])
                    if ed_date_format_list>0:
                        score-=10
                        pres-=10
                    #print(ed_date_format_list)
                    sections['edu_year']=extract(sections[key])
                    sections['paragraph']+=paragraph_check(sections[key])
                    #print(key,temp_ed)
                    msg.append("Education Section is Present")
                    break
                #print(score)
            for i in ex1_list:    
                if(i in key.lower() and ex==0 and key.lower()!='n'):
                    score +=20
                    ex=1
                    sections['exp_year']=extract(sections[key])
                    ex_date_format_list=date_format(sections[key])
                    impact+=20
                    sections['paragraph']+=paragraph_check(sections[key])
                            #print(dummy_exp)
                    msg.append("Experience Section is Present")
                    #print(score)
                    #print(key,temp_ex)
                    break
                
            for i in sk1_list:
                if(i in key.lower() and sk==0 and key.lower()!='n'):
                    score +=20
                    sk=1
                    msg.append("Skills Section is Present")
                    sections['paragraph']+=paragraph_check(sections[key])
                    break
            for i in aw1_list:    
                if(i in key.lower() and aw==0 and key.lower()!='n'):
                    score +=5
                    impact+=5
                    aw=1
                    ach_msg = 1
                    alpha_num = ['one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen','twenty','thirty','fourty','fifty','sixty','seventy','eighty','ninety','hundred','thousand']
                    checkfornos = checknos(sections[key],alpha_num)
                    sections['paragraph']+=paragraph_check(sections[key])
                    msg.append("Awards/Achievement Section is Present")
                    #print(score)
                    #print(key)
                    break
            for i in vo1_list:    
                if(i in key.lower() and vo==0 and key.lower()!='n'):
                    pres+=5
                    score +=5
                    vo=1
                    vol_msg =1
                    msg.append("Volunteering Section is Present")
                    #print(score)
                    #print(key)
                    break
            for i in ce1_list:    
                if(i in key.lower() and ce==0 and key.lower()!='n'):
                    impact+=5
                    score +=10
                    cert_msg=1
                    ce=1
                    msg.append("Certificate Section is Present")
                    #print(score)
                    #print(key)
                    break
            for i in pe1_list:    
                if(i in key.lower() and pe==0 and key.lower()!='n'):
                    pres+=10
                    pe=1
                    score +=10
                    pro_msg=1
                    sections['paragraph']+=paragraph_check(sections[key])
                    alpha_num = ['one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen','twenty','thirty','fourty','fifty','sixty','seventy','eighty','ninety','hundred','thousand']
                    checkfornos2 = checknos(sections[key],alpha_num)
                    msg.append("Projects Section is Present")
                    #print(score)
                    #print(key)
                    break
        list_present=[ed,ex,sk,aw,ce,pe,vo]
        fed=0
        fex=0
        fsk=0
        faw=0
        fce=0
        fpe=0
        fvo=0
        sect=[]
        
        #import os
        if os.path.exists("./templates/file.html"):
            os.remove("./templates/file.html")
        else:
            print("The file does not exist") 
        for i in range(len(list_present)):
            if i ==0 and list_present[i]==0:
                #print("education" + "is absent")
                for ik in ed1_list:
                    if ik in text_main.lower():
                        fed=1
                score+=5
            if i ==1 and list_present[i]==0:
                #print("experience" + "is absent")
                for ik in ex1_list:
                    if ik in text_main.lower():
                        fex=1
                score+=10
            if i ==2 and list_present[i]==0:
                print("skill" + "is absent")
                for ik in sk1_list:
                    if ik in text_main.lower():
                        fsk=1
                score+=10
            if i ==3 and list_present[i]==0:
                #print("achievement/award" + "is absent")
                for ik in aw1_list:
                    if ik in text_main.lower():
                        faw=1
                score+=2
            if i ==4 and list_present[i]==0:
                #print("certification" + "is absent")
                for ik in ce1_list:
                    if ik in text_main.lower():
                        fce=1
                score+=5
            if i ==5 and list_present[i]==0:
                #print("project" + "is absent")
                for ik in pe1_list:
                    if ik in text_main.lower():
                        fpe=1
                score+=5
            if i ==6 and list_present[i]==0:
                #print("volunteer" + "is absent")
                for ik in vo1_list:
                    if ik in text_main.lower():
                        fvo=1
                score+=2
        print(fed,fex,fsk,fsk,faw,fce,fpe,fvo)
        improper_format=[]
        if(fed==1 and ed==0):
            improper_format.append('education')
        if(fex==1 and ex==0):
            improper_format.append('experience')
        if(fsk==1 and sk==0):
            improper_format.append('skill')
        if(faw==1 and aw==0):
            improper_format.append('achievement')
        if(fce==1 and ce==0):
            improper_format.append('certification')
        if(fpe==1 and pe==0):
            improper_format.append('project')
        if(fvo==1 and vo==0):
            improper_format.append('volunteer')
        print(improper_format)
            
        #print("EDU MSG",edu_msg)
        sections['Message']=msg
        # sections['Score']=round(((score/98)*100),2)
        rev=""
        '''misspelled = spell.unknown(text_main)
        sections["Errors"]=[]
        for word in misspelled :
            if(len(word))>3:
                sections["Errors"].append(word)'''
                
        stop_words = set(stopwords.words('english')) 
        d=""
        skillsets=0
        filtered_sentence=[]
        
    
        for i in sections.keys():
            if(i.lower()=="work experience"):
                score +=5
            if(i.lower()=="core competencies"):
                score +=5            
            if 'skill' in i.lower():
                skillsets=len(sections[i])
                for j in sections[i]:
                     
                    d=d+" "+j
                d = word_tokenize(d)
                 # print("I am here 2")
                 #print(d)
                for w in d: 
                    if w not in stop_words: 
                        if(len(w)>3):
                            filtered_sentence.append(w)
    
        sections['SkCount']=skillsets
        #sections['original']=filtered_sentence
        sections['linkedin']=Find(text_main)
        ck=sections['linkedin']
        link_msg=1
        if(len(ck) == 0):
            link_msg=0
        #print(type(len(ck)))
        #print('Heyo',sections['linkedin'])
        ac=0
        rd=0
        action_list=[]
        act_msg=0
        if actionwords(text_main)[0] > 5 :
            act_msg =1
            action_list=actionwords(text_main)[1]
            ac=10
            sections['action_word']="Your resume contains Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful."
        elif actionwords(text_main)[0]<=5:
            act_msg =0
            sections['action_word']="Your resume doesnt contain much Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful. "
        elif actionwords(text_main)[0]==0:
            
            act_msg =0
            sections['action_word']="Your resume doesnt contain any Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful. "
        fct_msg=0
        filler_list=[]
        if fillerwords(text_main)[0] > 1 :
            fct_msg =1
            filler_list=fillerwords(text_main)[1]
            
            #sections['action_word']="Your resume contains Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful."
        # elif fillerwords(text_main)[0]<=5:
        #     fct_msg =0
        #     filler_list=fillerwords(text_main)[1]
        
        elif fillerwords(text_main)[0]==0:
            
            fct_msg =0
            #sections['action_word']="Your resume doesnt contain any Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful. "
        
        #print(sections['action_word'])
        
        if redundancy(text_main) > 10:
            rd=5
            sections['redundancy']="1"
        elif redundancy(text_main)<=10:
            sections['redundancy']="0"
            
        
        #sections['edu_year']=extract(sections[dummy_edu])
        #print(sections['exp_year'])
        #print(sections['edu_year'])
        #print(sections['redundancy'])
        #print(filtered_sentence)
        sections['match']=match
        # Checking of resume score for message
        if(score == 100):
            rev="the score looks perfect but to get a more accurate comparison with the job you are looking for try analysing by adding Job Description"
        elif(score < 60):
            rev="this score suggests there is a lot of room for improvement. But don't worry! We have highlighted a number of quick fixes you can make to improve your resume's score and your success rate. Try adding more skills or experience into your resume to increase your resume score to 80% or above."
        else:
            rev="your score looks good however we have highlighted a number of quick fixes you can make to improve your resume's score. Try adding more skills or experience into your resume to increase your resume score."
        sections["Review"]=rev
        sections["Length"]=length
        sections["WordCount"]=word_count
        if sections["WordCount"] <= 600 and sections["WordCount"] > 1:
            score += 5
            sections['Message'].append("Word Count of the Resume is Optimal")
        else:
            sections['Message'].append("Word Count should be less than 600")

        if sections["Length"] and sections["WordCount"] > 1:
            score += 5
            sections['Message'].append("Length of Resume is Optimal")
        else:
            sections['Message'].append("Length of Resume should not exceed 2 pages")
        sections['Score']=round(((score/100)*100),2) #calculating score out of overall score.
        if(sections['Score'] >=90 and sections['Score'] <100):
            sections["Review"]="The Resume is correctly Parsed and Optimal. There may be some room for Improvement"
        if(sections['Score'] >=75 and sections['Score']<90):
            sections["Review"]="The Resume may be Correctly Parsed and Optimal. It is advised to pass DOCX Format in ATS Checker. There is certainly Some Room For Improvement"        
        count_passive1=[]
        count_passive=0
        co_pa=0
        for i in line1:
            if(is_passive(re.sub(r'[^\x00-\x7f]',r'', i))):
                count_passive += 1
                count_passive1.append(re.sub(r'[^\x00-\x7f]',r'', i))
        
                
        if(count_passive > 0):
            co_pa= 1
        elif(len(line1)==0):
            co_pa= 1
            
        else:
            co_pa=0
            ac += 5
        #print(impact)
        count_tense1=[]
        co_ta=0
        count_tenses=0
        for i in line1:
            if(tenses_res(re.sub(r'[^\x00-\x7f]',r'', i))):
                count_tenses += 1
                count_tense1.append(re.sub(r'[^\x00-\x7f]',r'', i))
                
        if(count_tenses >= 5):
            co_ta= 1
        elif(len(line1)==0):
            co_ta= 1
            
        else:
            co_ta=0
            ac += 5
            
        if(len(line1)==0):
            sections['paragraph']=0 
        elif sections['paragraph'] <= 2:
            ac += 5
            
        
        #print(sections.keys())
        
        cont=[]
        contact_all=contact_details(text_main)
        for elem in contact_all:
            if elem:
                if len(contact_all[0]) == 0:
                    cont.append('email')
                if len(contact_all[1]) == 0:
                    cont.append('phone')
                if len(contact_all[2]) == 0:
                    cont.append('linkedin')
                if len(contact_all[0]) !=0 and len(contact_all[1])!=0 and len(contact_all[2])!=0:
                    cont.append('all')
                    break

            if elem not in contact_all:
                cont.append("none")
            
            
        # management = ['budgeting', 'business planning', 'business re-engineering',
        # 'change management', 'consolidation', 'cost control',
        # 'decision making', 'developing policies', 'diversification',
        # 'employee evaluation', 'financing', 'government relations',
        # 'hiring', 'international management' ,'investor relations',
        # 'ipo' ,'joint ventures', 'labour relations',
        # 'merger & acquisitions', 'multi-sites management', 'negotiation',
        # 'profit & loss', 'organizational development', 'project management',
        # 'staff development', 'strategic partnership', 'strategic planning',
        # 'supervision' ]
        
        # operations = ['bidding', 'call centre operations', 'continuous improvement',
        # 'contract management', 'environmental protection', 'facility management',
        # 'inventory control', 'manpower planning','operations research',
        # 'outsourcing', 'policies & procedures', 'project co-ordination',
        # 'project management'] 
        
        # production = [
        # 'equipment design', 'equipment maintenance & repair',
        # 'equipment management', 'iso 9xxx / 1xxxxx', 'tqm',
        # 'order processing', 'plant design & layout', 'process engineering',
        # 'production planning', 'quality assurance', 'safety engineering']
        
        # logistics= [
        # 'distribution', 'transportation', 'jit',
        # 'purchasing & procurement', 'shipping', 'traffic management',
        # 'warehousing']
        
        # researchanddevelopment = ['design & specification', 'diagnostics', 'feasibility studies',
        # 'field studies', 'lab management', 'lab design',
        # 'new equipment design', 'patent application', 'product development',
        # 'product testing', 'prototype development', 'r&d management',
        # 'simulation dev.',' statistical analysis', 'technical writing']
        
        # sales= ['account management', 'b2b', 'contract negotiation',
        # 'customer relations', 'customer service', 'direct sales',
        # 'distributor relations', 'e-commerce', 'forecasting',
        # 'incentive programs', 'international business development',
        # 'international expansion', 'new account development', 'proposal writing',
        # 'product demonstrations', 'telemarketing', 'trade shows',
        # 'sales administration', 'sales analysis', 'sales kits',
        # 'sales management', 'salespersons recruitment', 'show room management',
        # 'sales support', 'sales training']
        
        # marketing = ['advertising', 'brand management', 'channel marketing',
        # 'competitive analysis', 'copywriting', 'corporate identity',
        # 'image development', 'logo development', 'market research & analysis',
        # 'marketing communication', 'marketing plan', 'marketing promotions',
        # 'media buying/evaluation', 'media relations', 'merchandising',
        # 'new product development', 'online marketing','packaging',
        # 'pricing', 'product launch']
        
        # administration = [
        # 'contract negotiation', 'equipment purchasing', 'forms and methods',
        # 'leases', 'mailroom management', 'office management',
        # 'policies & procedures', 'reception', 'records management',
        # 'security', 'space planning', 'word processing']
        
        # legal = [
        # 'contract preparation', 'copyrights & trademarks', 'corporate law',
        # 'company secretary', 'employment ordinance', 'ipo',
        # 'intellectual property', 'international agreements', 'licensing',
        # 'mergers & acquisitions', 'patents', 'shareholder proxies',
        # 'stock administration']
        
        # financeandaccounting = [
        # 'accounting management', 'accounts payable', 'venture capital relations',
        # 'accounts receivable', 'acquisitions & mergers', 'actuarial/rating analysis',
        # 'auditing','banking relations', 'budget control',
        # 'capital budgeting', 'capital investment', 'cash management',
        # 'cost accounting', 'cost control', 'credit/collections',
        # 'debt negotiations', 'equity/debt management', 'feasibility studies',
        # 'financial analysis', 'financial reporting', 'financing',
        # 'forecasting', 'foreign exchange', 'general ledger',
        # 'insurance', 'internal controls', 'investor relations',
        # 'ipo', 'lending', 'lines of credit',
        # 'management reporting', 'payroll', 'fund management',
        # 'profit planning', 'risk management', 'stockholder relations',
        # 'tax treasury', 'investor presentations']
        
        # humanresources = [
        # 'arbitration/mediation', 'career counseling', 'career coaching',
        # 'classified advertisements', 'company orientation', 'workforce forecast/planning',
        # 'compensation & benefits', 'corporate culture', 'training administration',
        # 'employee discipline', 'employee selection', 'executive recruiting',
        # 'grievance resolution', 'human resources management',
        # 'industrial relations', 'job analysis', 'labour negotiations',
        # 'outplacement', 'performance appraisal', 'salary administration',
        # 'succession planning', 'team building', 'training']
        
        # informationandtechnology = [
        # 'algorithm development', 'application database administration',
        # 'applications development', 'business systems planning', 'web site editor',
        # 'capacity planning', 'crm', 'cad',
        # 'edi', 'enterprise asset management', 'eap',
        # 'enterprise resource planning', 'erp', 'hardware management',
        # 'information management', 'integration software', 'intranet development',
        # 'java', 'c+++', 'c language','python','r language','ruby','html','javascript','c#','objective-c','php',
        #     'sql','shift','portal design/development',
        # 'software customization', 'software development', 'system analysis',
        # 'system design', 'system development', 'technical evangelism',
        # 'technical support', 'technical writing', 'telecommunications',
        # 'tracking system', 'unix', 'usability engineering',
        # 'user education', 'user documentation', 'user interface',
        # 'vendor sourcing', 'voice & data communications',
        # 'web development/design', 'web site content writer', 'word processing']
        
        # creative = [
        # 'character development' ,'creative writing', 'drawing',
        # 'musical composition', 'story line development', 'visual composition']
        
        # design= [
        # 'colour theory', 'dreamweaver', 'flash',
        # 'freehand', 'illustrator', 'photoshop',
        # 'picasa', 'corel draw', 'typography',
        # 'print design & layout', 'photography']
        
        # publicrelation = [
        # 'b2b communication', 'community relations', 'speech writing',
        # 'corporate image', 'corporate philanthropy', 'corporate publications',
        # 'corporate relations', 'employee communication', 'event planning',
        # 'fund raising', 'government relations', 'investor collateral',
        # 'media presentations', 'press release', 'risk mgt communication']

        analytical =['Research', 'collected', 'conducted', 'defined', 'detected', 'discovered', 'examined',
        'experimented', 'explored', 'extracted', 'found', 'gathered', 'identified', 'inquired', 'inspected',
        'investigated', 'located', 'measured', 'modelled', 'observed', 'researched', 'reviewed', 'searched',
        'studied',' surveyed', 'tested', 'tracked', 'Analyse', 'Evaluate', 'analysed', 'assessed', 'calculated',
        'catalogued', 'categorized', 'clarified', 'classified', 'compared', 'compiled', 'critiqued', 
        'derived', 'determined', 'diagnosed', 'estimated', 'evaluated', 'formulated', 'interpreted',
        'prescribed', 'organized', 'rated', 'recommended', 'reported', 'summarized', 'systematized', 
        'tabulated', 'assembled', 'built', 'coded', 'computed', 'constructed', 'converted', 'debugged',
        'designed', 'engineered', 'fabricated', 'installed', 'maintained', 'operated',
        'printed', 'programmed', 'proved', 'rectified', 'regulated', 'repaired', 'resolved',
        'restored', 'specified', 'standardized', 'upgraded', 'adjusted', 'allocated', 'appraised',
        'audited', 'balanced', 'budgeted', 'conserved', 'controlled', 'disbursed', 'figured', 'financed',
        'forecasted', 'netted', 'projected', 'reconciled']

        communication = ['addressed', 'articulated', 'authored', 'briefed', 'clarified', 
        'conveyed', 'composed', 'condensed', 'corresponded', 'debated', 'delivered', 'described',
        'discussed', 'drafted', 'edited', 'expressed', 'formulated', 'informed', 'instructed',
        'interacted', 'interpreted', 'lectured', 'negotiated', 'notified', 'outlined', 'reconciled',
        'reinforced', 'reported', 'presented', 'proposed', 'specified', 'spoke', 'translated',
        'wrote', 'advertised', 'influenced', 'marketed', 'solicited', 'contacted', 'convinced',
        'represented', 'persuaded', 'motivated',' communicated', 'elicited', 
        'recruited', 'promoted', 'publicized', 'enlisted', 'arbitrated', 'consulted', 'conferred',
        'interviewed', 'mediated', 'moderated', 'listened', 'responded', 'suggested']

        leadership = ['administered', 'appointed', 'approved', 'assigned', 'authorized', 'chaired',
        'conducted', 'contracted', 'controlled', 'coordinated', 'decided', 'delegated', 'directed',
        'developed', 'enforced', 'ensured', 'evaluated', 'executed', 'headed', 'hired', 'hosted', 
        'implemented', 'instituted', 'led', 'managed', 'overhauled', 'oversaw', 'prioritized', 
        'recruited', 'represented', 'strategized', 'supervised', 'trained', 'anticipated', 'arranged',
        'contacted', 'convened', 'logged', 'obtained', 'ordered', 'planned',
        'prepared', 'processed', 'purchased', 'recorded', 'registered', 'reserved', 'scheduled', 
        'verified', 'consolidated', 'distributed', 'eliminated', 'filed', 'grouped', 'incorporated',
        'merged', 'monitored', 'organized', 'regulated', 'reviewed', 'routed', 'standardized',
        'structured', 'submitted', 'systematized', 'updated']

        teamwork = ['aided', 'answered', 'arranged', 'catalogued', 'categorized', 'collated', 'collected',
        'coordinated', 'distributed', 'emailed', 'ensured', 'expedited', 'explained', 'filed', 'greeted',
        'handled', 'informed', 'implemented', 'maintained', 'offered', 'ordered', 'organized', 'performed',
        'prepared', 'processed', 'provided', 'purchased', 'recorded', 'received', 'resolved', 'scheduled', 'served',
        'supported', 'tabulated', 'collaborated', 'consulted', 'cooperated', 'liaised', 'reached', 
        'out']

        initiative = ['authored', 'began', 'built', 'changed', 'combined', 'conceived', 'constructed',
        'created', 'customized', 'designed', 'developed', 'devised', 'established', 'formed',
        'formulated', 'founded', 'generated', 'initiated', 'integrated', 'introduced', 'invented',
        'launched', 'originated', 'produced', 'shaped', 'staged', 'visualized', 'modified', 'revamped',
        'revised', 'updated', 'advocated', 'aided', 'assisted', 'cared', 'contributed', 'cooperated',
        'coordinated', 'ensured', 'furthered', 'guided', 'intervened', 'offered', 'referred',
        'rehabilitated', 'supplied', 'supported', 'volunteered', 'served', 'adapted', 'advised',
        'clarified', 'coached', 'counselled', 'demonstrated', 'educated', 'enabled',
        'encouraged', 'evaluated', 'explained', 'facilitated', 'familiarized', 'individualized',
        'instructed', 'mentored', 'modelled' ] 


        ab = text_main.lower()
        sentence = nltk.tokenize.sent_tokenize(ab)
        comp1 = check(sentence,analytical)
        #converting list of lists to a flat list
        # comp1 = [item for elem in comp1 for item in elem]
        try:
            comp1_count = len(comp1)
        except:
            comp1_count = 0
        comp2 = check(sentence,communication)
        try:
            comp2_count = len(comp2)
        except:
            comp2_count = 0
        
        comp3 = check(sentence,leadership)
        try:
            comp3_count = len(comp3)
        except:
            comp3_count = 0
        
        comp4 = check(sentence,teamwork)
        try:
            comp4_count = len(comp4)
        except:
            comp4_count = 0
        
        comp5 = check(sentence,initiative)
        try:
            comp5_count = len(comp5)
        except:
            comp5_count = 0
        # comp6 = check(sentence,sales)
        # try:
        #     comp6_count = len(comp6)
        # except:
        #     comp6_count = 0
        
        # comp7 = check(sentence,marketing)
        # try:
        #     comp7_count = len(comp7)
        # except:
        #     comp7_count = 0
        
        # comp8 = check(sentence,administration)
        # try:
        #     comp8_count = len(comp8)
        # except:
        #     comp8_count = 0
        # comp9 = check(sentence,legal)
        # try:
        #     comp9_count = len(comp9)
        # except:
        #     comp9_count = 0
        
        # comp10 = check(sentence,financeandaccounting)
        # try:
        #     comp10_count = len(comp10)
        # except:
        #     comp10_count = 0
        # comp11 = check(sentence,humanresources)
        # try:
        #     comp11_count = len(comp11)
        # except:
        #     comp11_count = 0
        
        # comp12 = check(sentence,informationandtechnology)
        # try:
        #     comp12_count = len(comp12)
        # except:
        #     comp12_count = 0
        
        # comp13 = check(sentence,creative)
        # try:
        #     comp13_count = len(comp13)
        # except:
        #     comp13_count = 0
        
        # comp14 = check(sentence,design)
        # try:
        #     comp14_count = len(comp14)
        # except:
        #     comp14_count = 0
        
        # comp15 = check(sentence,publicrelation)
        # try:
        #     comp15_count = len(comp15)
        # except:
        #     comp15_count = 0

        
        
        
        match_dict = {'analytical' : comp1, 'communication': comp2, 'leadership': comp3, 'teamwork': comp4,
                    'initiative': comp5} 
        
        count_dict = {'analytical' : comp1_count, 'communication': comp2_count, 'leadership': comp3_count, 
                    'teamwork': comp4_count, 'initiative': comp5_count}


        count_competancies=[]
        for i in count_dict.keys():
            if(count_dict[i]!=0):
                count_competancies.append(i)
        sumaa=0
        for key in count_dict.keys():
            sumaa+=count_dict[key]

        nl=[]
        quant=0
        if checkfornos==1 or checkfornos2==1:
            quant=1
        elif checkfornos!=1 and checkfornos2!=1:
            nl=quan(text_main,aw1_list+pe1_list )
        if(nl[1]):
            quant=1
                
        print(sentence)
        print("Hey",len(match_dict))
        print(count_dict)
        print(count_competancies)
        ab = text_main.lower()
        sentence = nltk.tokenize.sent_tokenize(ab)

        barplot(count_dict)
        
        session['bared'] = count_dict
        count_dict_dict={}
        stop_words = set(stopwords.words('english')) 
        filtered_sentence = [w for w in sentence if not w in stop_words] 
        for i in filtered_sentence:
            count_dict_dict[i]=filtered_sentence.count(i)

        #wordcloud(count_dict_dict)
                
        if ed_date_format_list==1:
            pres-=5
        # if ex_date_format_list[1]==1:
        #     pres-=10
        skillmatch=skillsMatch(text_main)

        namee=extract_name(text_main)
        empty_competency=""
        cot=0
        for i in match_dict.keys():
            cot=cot+len(match_dict[i])

        if(cot==0):
            empty_competency = "You might want to add few competencies in your resume as it's an efficient way to provide comprehensive proof that you are qualified for a certain job. "

        # if (len(match_dict['management'] == 0) and (len(match_dict['operations'] == 0):
        #     print("Yo")
        #namee=' '.join(w.capitalize() for w in namee.split())
        #print(namee,cont,count_tense1,count_passive1,sections['edu_year'],sections['exp_year'])    
        #end of check
        print(pro_msg,edu_msg,sections['redundancy'],vol_msg,cert_msg,link_msg,ach_msg,act_msg,co_pa)
        return render_template('services.html', results=sections,skillmatch=skillmatch, quant=quant, empty_competency=empty_competency,name=namee,fct_msg=fct_msg,filler_list=filler_list,wc=word_count,pro_msg=pro_msg,edu_msg=edu_msg,matched_comment= rev,jd_msg=jd_msg,score= sections['Score'],email=email,education=edu,rud_mdg=sections['redundancy'],vol_msg=vol_msg,cert_msg=cert_msg,link_msg=link_msg,ach_msg = ach_msg,count_pass=co_pa,count_tense=co_ta,act_msg=act_msg,para=sections['paragraph'],action_list=list(set(action_list)),count_tense1=count_tense1,count_passive1=count_passive1,contacts=cont,edu_year=sections['edu_year'],exp_year=sections['exp_year'],imp_for=improper_format,fed=fed,fex=fex,fsk=fsk,fce=fce,fpe=fpe,faw=faw,fvo=fvo,ed_correct_year=ed_date_format_list,ex_correct_year=ex_date_format_list,count_dict=count_dict,match_dict=match_dict,count_competancies=count_competancies,sumaa=sumaa, depth=int(((ac+rd)/30*100)),pres=int(pres/25*100),impact=int(impact/45 *100))
        #return render_template('display.html', results=sections)   
    except Exception as e:
        print(e)
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print(exc_type, fname, exc_tb.tb_lineno)
        return render_template('error.html')


def docx1(name):
    global text_main,length
    resume= docx2txt.process(name)
        # f = open('jd.txt', 'r')
        # jd= f.read()
    jd=session['data']
        # print(jd)
    # print(resume)
    res = len(resume.split())
    page = math.ceil(res/700)
    length = page
    print("Number of Pages ",page) 
    if(page > 2):
        print("Try to shorten CV below 2 pages")
    text =[resume, jd]
        # print(get_year(resume,resume))
    text_main = resume
    kk = analyser(text)
    return kk
    

def pdf(name):
    global text_main,length
    c=repr(extract_text(name))
        
        #print(c)

        # f = open('jd.txt', 'r')
    jd= session['data']  
        # print(txt)
    text =[c, jd]
        
    pdf = PdfFileReader(open(name,'rb'))
    page = pdf.getNumPages()
    length = page
    print("Number of Pages ",page)
    if(page > 2):
        print("Try to shorten your CV below 2 pages")
    kk = analyser(text)
    text_main = c
    return kk
        
    


def analyser(text):
    cv =CountVectorizer()
    count_matrix = cv.fit_transform(text)
    matched= cosine_similarity(count_matrix)[0][1]*100
    matched= round(matched,2)
    doc1 = nlp(text[0])
    doc2 = nlp(text[1])
    sim = doc1.similarity(doc2)*100
    sim= round(sim,1)
    # print("Your resume is about "+str(sim)+"%")
    if(sim > 80):
        sim=sim*0.9

    l = sim
    return l

def Find(string): 
    regex = r"(?:https?:)?\/\/(?:[\w]+\.)?linkedin\.com\/in\/(?P<permalink>[\w\-\_À-ÿ%]+)\/?"
    url = re.findall(regex,string)
    return url

def actionwords(string):
    #count=0
    No_of_actionVerbs=[]
    test_list = ['accelerated', 'achieved', 'attained', 'completed', 'conceived', 'convinced',
             'discovered', 'doubled', 'effected', 'eliminated', 'expanded', 'expedited', 
             'founded', 'improved', 'increased', 'initiated', 'innovated', 'introduced', 
             'invented', 'launched', 'mastered', 'overcame', 'overhauled', 'pioneered', 
             'reduced', 'resolved', 'revitalized', 'spearheaded', 'strengthened', 
             'transformed', 'upgraded', 'tripled', 'addressed', 'advised', 'arranged', 
             'authored', 'co-authored', 'co-ordinated', 'communicated', 'corresponded', 
             'counselled', 'developed', 'demonstrated', 'directed', 'drafted', 'enlisted',
             'facilitated', 'formulated', 'guided', 'influenced', 'interpreted',
             'interviewed', 'instructed', 'lectured', 'liased', 'mediated', 
             'moderated', 'motivated', 'negotiated', 'persuaded', 'presented', 'promoted', 
             'proposed', 'publicized', 'recommended', 'reconciled', 'recruited', 
             'resolved', 'taught', 'trained', 'translated', 'composed','conceived','created',
             'designed', 'developed', 'devised', 'established', 'founded', 'generated', 
             'implemented', 'initiated', 'instituted', 'introduced', 'launched','opened',
             'originated','pioneered', 'planned', 'prepared', 'produced','promoted', 
             'started', 'released', 'administered', 'analyzed', 'assigned', 'chaired', 
             'consolidated', 'contracted', 'co-ordinated', 'delegated', 'developed',
             'directed', 'evaluated', 'executed', 'organized', 'planned', 'prioritized',
             'produced', 'recommended', 'reorganized', 'reviewed', 'scheduled', 'supervised', 
             'managed', 'guided', 'advised', 'coached', 'conducted', 'directed', 'guided',
             'demonstrated', 'illustrated','managed', 'organized', 'performed', 
             'presented', 'taught', 'trained', 'mentored', 'spearheaded', 'authored', 
             'accelerated', 'achieved', 'allocated', 'completed', 'awarded', 'persuaded',
             'revamped', 'influenced', 'assessed', 'clarified', 'counseled', 'diagnosed',
             'educated', 'facilitated', 'familiarized', 'motivated', 'referred', 
             'rehabilitated', 'reinforced', 'represented', 'moderated', 'verified', 
             'adapted', 'coordinated', 'developed', 'enabled', 'encouraged', 'evaluated',
             'explained', 'informed', 'instructed', 'lectured', 'stimulated', 'analyzed',
             'assessed', 'classified', 'collated', 'defined', 'devised', 'established', 
             'evaluated', 'forecasted', 'identified', 'interviewed', 'investigated', 
             'researched', 'tested', 'traced', 'designed', 'interpreted', 'verified', 
             'uncovered', 'clarified', 'collected', 'critiqued', 'diagnosed', 'examined',
             'extracted', 'inspected', 'inspired', 'organized', 'reviewed', 'summarized', 
             'surveyed', 'systemized', 'arranged', 'budgeted', 'composed', 'conceived', 
             'conducted', 'controlled', 'co-ordinated', 'eliminated', 'improved', 'investigated', 
             'itemised', 'modernised', 'operated', 'organised', 'planned', 'prepared', 'processed', 
             'produced', 'redesigned', 'reduced', 'refined', 'researched', 'resolved', 'reviewed',
             'revised', 'scheduled', 'simplified', 'solved', 'streamlined', 'transformed', 
             'examined', 'revamped', 'combined', 'consolidated', 'converted', 'cut', 'decreased', 
             'developed', 'devised', 'doubled', 'tripled', 'eliminated', 'expanded', 'improved', 
             'increased', 'innovated', 'minimised', 'modernised', 'recommended', 'redesigned', 
             'reduced', 'refined', 'reorganised', 'resolved', 'restructured', 'revised', 'saved', 
             'serviced', 'simplified', 'solved', 'streamlined', 'strengthened', 'transformed', 
             'trimmed', 'unified', 'widened', 'broadened', 'revamped', 'administered', 'allocated', 
             'analyzed', 'appraised', 'audited', 'balanced', 'budgeted', 'calculated', 'computed', 'developed', 
             'managed', 'planned', 'projected', 'researched', 'restructured', 'modelled', 'acted',
             'conceptualized', 'created', 'customized', 'designed', 'developed', 'directed', 'redesigned',
             'established', 'fashioned', 'illustrated', 'instituted', 'integrated', 'performed', 'planned', 
             'proved', 'revised', 'revitalized', 'set up', 'shaped', 'streamlined', 'structured', 'tabulated',
             'validated', 'approved', 'arranged', 'catalogued', 'classified', 'collected', 
             'compiled', 'dispatched', 'executed', 'generated', 'implemented', 'inspected',
             'monitored', 'operated', 'ordered', 'organized', 'prepared', 'processed', 'purchased', 
             'recorded', 'retrieved', 'screened', 'specified', 'systematized']
    test_string=string.lower()
    res = [ele for ele in test_list if(ele in test_string)]
    No_of_actionVerbs.append(len(res))
    No_of_actionVerbs.append(res)
    print("Total number of action verbs used: ",No_of_actionVerbs[0],type(No_of_actionVerbs[0]))
    return(No_of_actionVerbs)

def fillerwords(string):
    #count=0
    No_of_fillerwords=[]
    test_list = ['capable','scalable', 'hard-work', 'hard work', 'problem-solve', 'creative', 'problem solve', 'innovative','motivated', 'skillful', 'communication-skill','coommunication skill','highly qualified', 'highly-qualified', 'results-focussed', 'result-focussed','results focussed', 'result focussed', 'effectual leader', 'effectual-leader','energetic','confident','professional','successfully', 'team player', 'team-player','responsible for','entrepreunerial','best of breed','detail oriented','detail-oreinted','seasoned','referances available by request','ambitious','punctual','go-getter','go getter','honest','strategic thinker','synnergy']
    test_string=string.lower()
    res = [ele for ele in test_list if(ele in test_string)]
    No_of_fillerwords.append(len(res))
    No_of_fillerwords.append(res)
    #print("Total number of action verbs used: ",No_of_actionVerbs[0],type(No_of_actionVerbs[0]))
    return(No_of_fillerwords)


def redundancy(string):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    text=string.lower()
    no_punct = ""
    for char in text:
        if char not in punctuations:
            no_punct = no_punct + char
    text_tokens = word_tokenize(no_punct)

    text = [word for word in text_tokens if not word in stopwords.words()]
    dictOfElems = RedundancyCheck(text)
    redundant_words = list(dictOfElems.values())
    count = sum(redundant_words) - len(redundant_words)
    return count
    
    
def RedundancyCheck(listOfElems):
    dictOfElems = dict()
    for elem in listOfElems:
        if elem in dictOfElems:
            dictOfElems[elem] += 1
        else:
            dictOfElems[elem] = 1    
 
    dictOfElems = { key:value for key, value in dictOfElems.items() if value > 5}
    return dictOfElems

def extract(text):
    c=""
    year=[]
    for i in text:
        c+=i+" "
    for key in c:
        year = re.findall('((?:19|20)\d\d)', c)
    year.sort()
    return(year)

def is_passive(sentence):
    matcher = Matcher(nlp.vocab)
    doc = nlp(sentence)
    passive_rule = [{'DEP': 'nsubjpass'}, {'DEP': 'aux', 'OP': '*'}, {'DEP': 'auxpass'}, {'TAG': 'VBN'}]
    matcher.add('Passive', None, passive_rule)
    matches = matcher(doc)
    count =0
    if matches:
        return True
    else:
        return False
    

def check_for_tense(sentence):
    text = word_tokenize(sentence)
    tagged = pos_tag(text)

    tense = dict()
    tense["future"] = len([word for word in tagged if word[1] == "MD"])
    tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
    tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]]) 
    return(tense)

def tenses_res(str):
    tenses_check = check_for_tense(str)
    new_list = list(tenses_check.values())
    if new_list[0] == 0 and new_list[1] == 0:
        return False
    elif new_list[1] == 0 and new_list[2] == 0:
        return False
    elif new_list[0] == 0 and new_list[2] == 0:
        return False
    else:
        return True
    
def paragraph_check(str):
    Counter = 0
    for i in str: 
        if i: 
            Counter += 1
            
    if Counter > 5:
        return 0
    else:
        return 1
    
def contact_details(string):
    contact = []
    phone=re.findall('(?:\+[1-9]\d{0,2}[- ]?)?[1-9]\d{9}', string)
    email=re.findall(r"([a-zA-Z0-9.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9_-]+)",string)
    linkedin_username = re.findall(r"(?:https?:)?\/\/(?:[\w]+\.)?linkedin\.com\/in\/(?P<permalink>[\w\-\_À-ÿ%]+)\/?",string)
    if len(linkedin_username) != 0:
        linkedin_username[0] = 'https://www.linkedin.com/in/'+ linkedin_username[0]
    contact.append(email)
    contact.append(phone)
    contact.append(linkedin_username)
    return contact



def extract_name(resume_text):
    nlp_text = nlp(resume_text)
    matcher = Matcher(nlp.vocab)
    
    # First name and Last name are always Proper Nouns
    pattern = [[{'POS': 'PROPN'}, {'POS': 'PROPN'}]]
    
    matcher.add('NAME', None, *pattern)
    
    matches = matcher(nlp_text)
    
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text    
def date_format(str1): 
    c=""
    for i in str1:
        c+=i+" "
    #print(str1)
    #print(c)
    keywords = ['jan', 'feb', 'mar','apr', 'may','jun', 'jul', 'aug', 'sep', 'oct','nov', 'dec']
    string = '20'
    punctuations = '''!()-[]{;:'"}\,<>./?@#$%^&*_~'''
    
    text=c
    lii = list(text.split(" "))
    Text = ""
    for char in text:
        if char not in punctuations:
            Text = Text + char
            
    two_dig = re.findall(r"\b\d{2}\b", Text)
    four_dig = re.findall(r'((?:19|20)\d\d)', text)
    current_time=datetime.datetime.now()
    
    
    month_yyyy = []
    month_yy = []
    only_year = []

    # declaring flag variables for different date formats
    correct_format = 0
    wrong_mmyy = 0
    wrong_year = 0
    
    yyyy_mm1 = re.findall(r'\d{4}-\d{2}', text)
    mm_yyyy1 = re.findall(r'\d{2}-\d{4}', text)
    mm_yyyy2 = re.findall(r'\d{2}/\d{4}', text)
    yyyy_mm2 = re.findall(r'\d{4}/\d{2}', text)
    # print(yyyy_mm1)
    # print(yyyy_mm2)
    # print(mm_yyyy1)
    # print(mm_yyyy2)

    
    
    try:
        if four_dig:
            for i in four_dig:
                var = i
                li = list(Text.split(" "))
                #print(li)
    
                if var in li:
                    indexx = li.index(var)
                    prev = li[indexx-1]
                    #print(prev)
                    li.remove(i)
                    for j in keywords:
                         #print(j)
                         if j in prev:
                             month_yyyy.append(var)
                             #print(string + var)
                             break
                         else:
                             wrong_format=1
                             continue
    
        # print(month_yyyy)
        
        if two_dig:
            for i in two_dig:
                a = i
                #print(a)
                li = list(Text.split(" "))
    
                indexx = li.index(a)
                prev = li[indexx-1]
                #print(prev)
                li.remove(i)
                for j in keywords:
                    #print(j)
                    if j in prev:
                        if a>int(str(current_time)[2:4]):
                            month_yy.append('19' + a)
                            #print(string + a)
                            break
                        else:
                            month_yy.append(string + a)
                     
                    else:
                        continue
   
    except:
        correct_format = 0
        wrong_mmyy = 0          
    # print(month_yy)

    if four_dig:
        only_year.append(four_dig)
    only_year = [ item for elem in only_year for item in elem]
    
    year_only = []
    if only_year:
        for elem in only_year:
            if elem not in month_yyyy and elem in lii:
                year_only.append(elem)
   
    if yyyy_mm1 or yyyy_mm2 or mm_yyyy1 or mm_yyyy2 or month_yyyy:
        correct_format = 1
    if month_yy:
        wrong_mmyy = 1
    if year_only:
        wrong_year = 1

    c=[]
    c.append(correct_format)
    c.append(wrong_mmyy)
    c.append(wrong_year)

    #identify the format of dates present
    if(c[0] == 0 and c[1]==0 and c[2] == 0):
        print('No dates found')
        k=2
        print(k)
    else:
        if(c[0] == 1):
            if (c[1] == 1 and c[2] == 1) or (c[1] == 1 and c[2] == 0) or (c[1] == 0 and c[2] == 1):
                print('Correct and wrong format dates found')
                k=1
                print(k)
            else:
                print('correct format')
                k=0
                print(k)
        
        else:
            print('Wrong format dates found')
            k=2
            print(k)

    return k    
    # return correct_format,wrong_mmyy,wrong_year,not_present


def quan(sent_text,list_):
    sent = nltk.tokenize.sent_tokenize(sent_text)
    alpha_num = ['one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen','twenty','thirty','fourty','fifty','sixty','seventy','eighty','ninety','hundred','thousand']
    ress=[]
    keyw=0
    keyw_no=0
    s=""
    for i in sent:
        for j in list_:
#             print('j is',j)
            s = i.split(" ")
            for k in s:
#                 print('k is',k)
                if(k==j):
                    keyw = 1
                    keyw_no = checknos(i,alpha_num)
#                     return True
            continue
    ress.append(keyw)
    ress.append(keyw_no)
    return ress

def checknos(tex,noslist):
    sa = tex
    res = [int(i) for i in sa if i.isdigit()]
    with_num=0
    if res:
        with_num = 1
        return with_num
    else:
        with_num = 0

    for h in noslist:
        for a in sa:
            if (a==h):
                with_num = 1
                return with_num
        continue
    with_num = 0


def check(sent,wrd):
    c=[]
    for i in sent:
        for j in wrd:
            if j in i:
                c.append(j)
    
    return list(set(c))

def barplot(count_dict):
    #count_dict = {'informationandtechnology': 14, 'administration': 10, 'humanresources': 3, 'financeandaccounting': 6, 'legal': 3}
    length = len(count_dict)
    li =[]
    for i in range(1,length):
        li.append(i)

    keys = [k for k in count_dict]
    # print(a)
    values = [count_dict[k] for k in count_dict]
    # print(b)

    fig = go.Figure([go.Bar(x=keys, y=values)])
    fig.write_html("./templates/file.html")
    

def wordcloud(count_dict):
    wordcloud = WordCloud(width=800, height=400, background_color="black",colormap="Blues").generate_from_frequencies(frequencies=count_dict)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.margins(x=0, y=0)
    #plt.show()
    fig = plt.figure()
#plot sth

    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

    html = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Document</title></head><body>' + '<img src=\'data:image/png;base64,{}\'>'.format(encoded) + '</body></html>'

    with open('./templates/wrdcloud.html','w') as f:
        f.write(html)

def skillsMatch(text):
    df = pd.read_excel('Hard skill keywords.xlsx')
#     df.head()
    l = df.values.tolist()
    skills = [item for sublist in l for item in sublist]
    res_words = list(text.split(" "))
    matched = []
    for i in res_words:
        if i in skills:
            matched.append(i)
    print(matched)
################to remove duplicate matched skills#########################
    matched = list(dict.fromkeys(matched))
    print(matched)
    return matched







    
    
@app.route('/details')
def detailed():
    return render_template('detailed.html')


@app.route('/',methods= ["GET",'POST'])
@app.route('/home',methods= ["GET",'POST'])
def resume():
    return render_template('index.html')

@app.route('/demo',methods= ["GET",'POST'])
def demo():
    return render_template('services.html')


@app.route('/barploted')
def barploted():
    return render_template('file.html')

@app.route('/wordclouded')
def wordclouded():
    return render_template('wrdcloud.html')
    

@app.route('/analyse',methods= ["GET",'POST'])
def analyse():
    if request.method == 'POST':
        session.pop('data', None)
        session['data'] = request.form['jd']
        
        print(session['data'])
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No Selected File')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename= secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print('Success')
            return redirect (url_for('uploaded_file',filename=filename))
    return render_template('elements.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploadfile():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'

@app.route('/jd',methods= ["GET",'POST'])
def jd_analyse():
    if request.method == 'POST':
        session.pop('data', None)
        session['data'] = request.form['jd']
        
        print(session['data'])
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No Selected File')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename= secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print('Success')
            return redirect (url_for('jd_file',filename=filename))
    return render_template('jd.html')

@app.route('/jd/<filename>')
def jd_file(filename):
    try:
        f_name = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        # return f_name
        global text_main,length,match,keyword
        file_name = f_name
        print(f_name)
        impact = 0
        pres =0
        text_main = ""
        edu_msg =0 
        vol_msg=0
        pro_msg=0
        jd_msg=""
        typee=0
        if(file_name[-3:]=="pdf"):
            print("File is in pdf")
            jd_score=pdf(file_name)
            typee=0
            #print(text_main)
            #text_main=re.sub(r'[^\\x00-\x7f]',r'', text_main)
            #text_main=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', text_main)
            # if (float(match) == 0):
            #     jd_msg = "If it shows zero, probably you have not specified the JD in it field. Try adding a JD to check how accurately your resume matches with the Job."
            # elif (float(match) < 50):
            #     jd_msg = "With " +str(match) + "% score you might need to add more skills related to the Job you have been looking for. Try aiming for a score above 80%"
            # else:
            #     jd_msg ="With " +str(match) + "% score you seem to be an apt fit for the Job you have been looking for. "
        elif(file_name[-4:] == "docx"):
            print("File is in docx")
            jd_score=docx1(file_name)
            typee=1
            #text_main=re.sub(r'[^\x00-\x7f]',r'', text_main)
            # if (float(match) == 0.0):
            #     jd_msg = "If it shows zero, probably you have not specified the JD in it field. Try adding a JD to check how accurately your resume matches with the Job."
            # elif (float(match) < 50):
            #     jd_msg = "With " +str(match) + " % score you might need to add more skills related to the Job you have been looking for. Try aiming for a score above 80%"
            # else:
            #     jd_msg ="With " +str(match) + " % score you seem to be an apt fit for the Job you have been looking for. "
        else:
            print("Invalid Fileformat - Supported docx or pdf")
            return render_template('unsupported.html')
        #print (text_main)
        
        text_count=text_main.split(" ")
        word_count=len(text_count)
        liness=[]
        line=""
        line1=[]
    # =============================================================================
    #     for i in text_main:
    #             
    #         if(i!='\n'):
    #             line+=i
    #         else:
    #             liness.append(line)
    #             line=""
    #         
    #     for line in liness:
    #         if len(line)!=0:
    #             line1.append(line)
    # =============================================================================
    # =============================================================================
        if(file_name[-4:] == "docx" ):
            for i in text_main:
                
                if(i!='\n'):
                    line+=i
                else:
                    liness.append(line)
                    line=""
            
            for line in liness:
                if len(line)!=0:
                    line1.append(line)
        elif(file_name[-3:]=="pdf"):
            liness=text_main.split("\\n")
    # =============================================================================
    #         for i in range(len(text_main)-1):
    #             if(text_main[i]=="\\" ):
    #                if(text_main[i+1]=='n'):
    #                    liness.append(line)
    #                    line=""
    #                else:
    #                    line+=text_main[i]
    # =============================================================================
                    
            
            for line in liness:
                if len(line)!=0:
                    line1.append(line)

        
        
        phone=re.findall(r"(?<!\d)\d{10}(?!\d)", text_main)
        email=re.findall(r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)",text_main)
        #print(email)
        links= re.findall(r"(^(http\:\/\/|https\:\/\/)?([a-z0-9][a-z0-9\-]*\.)+[a-z0-9][a-z0-9\-]*)",text_main)
        mlink=[]
        for link in links:
            if 'facebook' in link:
                mlink.append(link)
            elif 'github' in link:
                mlink.append(link)
            elif 'linkedin' in link:
                mlink.append(link)
            else:
                links.remove(link)
        links=list(set(mlink))
        section=[]
        sections={}
        line2=[]
        titles=['education','Licensures', 'Professional Qualification', 'academic qualification', 'Educational Qualification', 'academia', 'education and professional development', 'academic credentials', 'educational summary', 'academic profile', 'Experience', 'work experience', 'Job Titles held', 'Position Description and purpose', 'Professional Experience', 'Professional Summary', 'Profile', 'Qualifications', 'Employment History', 'history', 'previous employment', 'organisational experience', 'employers', 'positions of responsibility','Position of Responsibilities', 'employment scan', 'past experience', 'organizational experience', 'career', 'experience and qualification summary', 'relevant experience', 'experience summary', 'career synopsis', 'career timeline', 'banking IT experience', 'AML & FCM Suite Experience', 'employment details', 'Skill','skills', 'Technical Skills', 'Soft Skills', 'Key Skills', 'Design Skills', 'Expertise', 'Abilities', 'Area of Expertise', 'Key attributes', 'Computer Skills', 'IT Skills', 'Technical Expertise', 'Technical Skills Set', 'Functional Skill Set', 'functional skills', 'strengths', 'areas of expertise', 'banking knowledge', 'Award', 'Honours and awards', 'Key achievements', 'Accomplishments', 'Highlights', 'Affiliations', 'Achievements', 'Extra Curricular activities and achievements', 'awards and recognition','awards/achievements', 'Certificate', 'Most proud of', 'Specialization', 'Certifications', 'Certification/training','Coursework','other credentials', 'professional accomplishments', 'certification & trainings', 'scholastics', 'professional credentials and certifications','Project','projects', 'Additional Activities', 'Activities', 'Major Tasks', 'Responsibilities', 'key accountabilities', 'Contributions', 'Personal Projects', 'Key Contributions', 'Strategic Planning and execution', 'Academic projects', 'Key projects', 'projects/trainings', 'key implementations','Volunteer', 'Volunteer Experience', 'Affiliations', 'Misc','Extra Curricular Activities', 'Community Service','EDUCATIONAL BACKGROUND','INTERNSHIPS EXPERIENCE','WINNING PORTFOLIO','AWARDS & RECOGNITIONS','CORE COMPETENCIES','PROJECTS ADMINISTERED','TECHNICAL SKILLS','CERTIFICATIONS','VOLUNTEERING','PERSONAL DOSSIER','Licensure', 'Professional Qualifications', 'academic qualifications', 'academics qualification', 'academics qualifications',  'Educational Qualifications', 'education and professional developments', 'academic credential', 'academics credential', 'academics credentials', 'educational summaries', 'academic profiles', 'academics profile','Experiences', 'work experiences', 'Position Descriptions and purpose', 'Positions Description and purpose', 'Positions Descriptions and purpose', 'Professional Experiences', 'Profiles', 'Qualification', 'Employment Histories', 'previous employments', 'organisational experiences', 'organizational experiences', 'organizational experience', 'employer', 'positions of responsibilities', 'position of responsibility', 'position of responsibilities', 'employment scans', 'past experiences', 'organizational experiences', 'organisational experience', 'organisational experiences', 'careers', 'experiences and qualifications summary', 'experience and qualifications summary', 'experiences and qualification summary', 'relevant experiences', 'career timelines', 'banking IT experiences', 'AML & FCM Suite Experiences', 'employment details', 'employment detail','Skills', 'Technical Skill', 'Soft Skill', 'Key Skill', 'Design Skill', 'Expertises', 'Ability', 'Areas of Expertises', 'Areas of Expertise', 'Area of Expertises', 'Key attribute', 'Computer Skill', 'IT Skill', 'Technical Expertises', 'Technical Skill Set', 'Technical Skill Sets', 'Functional Skills Set', 'Functional Skill Sets', 'Functional Skills Sets', 'functional skill', 'strength', 'area of expertise', 'area of expertises','Awards', 'Key achievement', 'Accomplishment', 'Highlight', 'Affiliation', 'Achievement', 'Extra Curricular activities and achievements',  'Extra Curricular activity and achievements',  'Extra Curricular activities and achievement',  'Extra Curricular activity and achievement', 'awards and recognitions',  'award and recognition',  'award and recognitions', 'Certificates', 'Specializations', 'Certification', 'Certifications/trainings', 'Certifications/training', 'Certification/trainings', 'other credential', 'professional accomplishment', 'certifications & trainings', 'certifications & training', 'certification & training', 'scholastic', 'professional credential and certification', 'professional credential and certifications', 'professional credentials and certification','Project', 'Additional Activity', 'Activity', 'Major Task', 'Responsibily', 'key accountability', 'Contribution', 'Personal Project', 'Key Contribution', 'Strategic Plannings and executions', 'Strategic Plannings and execution', 'Strategic Planning and executions', 'Academic project', 'Key project', 'project/training', 'projects/training', 'project/trainings', 'key implementation','Volunteer', 'Volunteer Experiences', 'Affiliation', 'Community Services' ]
        titles1=[x.lower() for x in titles]
        for i in line1:
            if i[-1]==" ":
                line2.append(i[:-1])
            else:
                line2.append(i)
        #print(titles1)
        line1=line2
        temp = '\t'.join(titles1)
        for x in line1:
            #print(x.lower() in titles1, x.lower())
            global keyword
            if(x==line1[-1]):
            
                section.append(x)
                sections[keyword] = section
                keyword = x
                    #print(sections)
                section =[]
                break
            elif x.lower() not in temp:
                section.append(x)
                #print(x)
                #print(section)
            elif (len(x.split(" "))>=4):
                section.append(x)
                #print(section)  
            
                
            else :
                if(len(section)!=0):
                    sections[keyword] = section
                    keyword = x
                    #print(sections)
                    section =[]
                else:
                    sections[keyword]=[]
                    keyword=x
                    section =[]
                    #print(sections)
        #print(sections.keys())
        sections['phone']=list(set(phone))
        sections['links']=mlink
        if (len(mlink) != 0):
            impact+=5
        #imp_sec=["education","experience","expertise","role","career","skill","award","certificat","projects",'volunteer']
        ed_list=['Education', 'Education Details','Licensures', 'Professional Qualification', 'academic qualification', 'Educational Qualification', 'academia', 'education and professional development', 'academic credentials', 'educational summary', 'academic profile','EDUCATIONAL BACKGROUND','Licensure', 'Professional Qualifications', 'academic qualifications', 'academics qualification', 'academics qualifications',  'Educational Qualifications', 'education and professional developments', 'academic credential', 'academics credential', 'academics credentials', 'educational summaries', 'academic profiles', 'academics profile']
        ex_list=['Experience', 'Experience Details','work experience', 'Job Titles held', 'Position Description and purpose', 'Professional Experience', 'Professional Summary', 'Profile', 'Qualifications', 'Employment History', 'history', 'previous employment', 'organisational experience', 'employers', 'positions of responsibility', 'employment scan','past experience', 'organizational experience', 'career', 'experience and qualification summary', 'relevant experience', 'experience summary', 'career synopsis', 'career timeline', 'banking IT experience', 'AML & FCM Suite Experience', 'employment details','INTERNSHIPS EXPERIENCE','Experiences', 'work experiences', 'Position Descriptions and purpose', 'Positions Description and purpose', 'Positions Descriptions and purpose', 'Professional Experiences', 'Profiles', 'Qualification', 'Employment Histories', 'previous employments', 'organisational experiences', 'organizational experiences', 'organizational experience', 'employer', 'positions of responsibilities', 'position of responsibility', 'position of responsibilities', 'employment scans', 'past experiences', 'organizational experiences', 'organisational experience', 'organisational experiences', 'careers', 'experiences and qualifications summary', 'experience and qualifications summary', 'experiences and qualification summary', 'relevant experiences', 'career timelines', 'banking IT experiences', 'AML & FCM Suite Experiences', 'employment details', 'employment detail', 'career progression']
        sk_list=['Skill', 'Technical Skills', 'Soft Skills', 'Key Skills', 'Design Skills', 'Expertise', 'Abilities', 'Area of Expertise', 'Key attributes', 'Computer Skills', 'IT Skills', 'Technical Expertise', 'Technical Skills Set', 'Functional Skill Set', 'functional skills', 'strengths', 'areas of expertise', 'banking knowledge','WINNING PORTFOLIO','CORE COMPETENCIES','TECHNICAL SKILLS','skills','Skills', 'Technical Skill', 'Soft Skill', 'Key Skill', 'Design Skill', 'Expertises', 'Ability', 'Areas of Expertises', 'Areas of Expertise', 'Area of Expertises', 'Key attribute', 'Computer Skill', 'IT Skill', 'Technical Expertises', 'Technical Skill Set', 'Technical Skill Sets', 'Functional Skills Set', 'Functional Skill Sets', 'Functional Skills Sets', 'functional skill', 'strength', 'area of expertise', 'area of expertises']
        aw_list=['Award' , 'Achievement Details','Honours and awards', 'Key achievements', 'Accomplishments', 'Highlights', 'Affiliations', 'Achievements', 'Extra Curricular activities and achievements', 'awards and recognition','AWARDS & RECOGNITIONS','awards','achievements','Awards', 'Key achievement', 'Accomplishment', 'Highlight', 'Affiliation', 'Achievement', 'Extra Curricular activities and achievements',  'Extra Curricular activity and achievements',  'Extra Curricular activities and achievement',  'Extra Curricular activity and achievement', 'awards and recognitions',  'award and recognition',  'award and recognitions']
        ce_list=['Certificate', 'Certification Details','Most proud of', 'Specialization', 'Certifications', 'Certification/training', 'other credentials', 'professional accomplishments', 'certification & trainings', 'scholastics', 'professional credentials and certifications','CERTIFICATION','coursework', 'competencies', 'Certificates', 'Specializations', 'Certification', 'Certifications/trainings', 'Certifications/training', 'Certification/trainings', 'other credential', 'professional accomplishment', 'certifications & trainings', 'certifications & training', 'certification & training', 'scholastic', 'professional credential and certification', 'professional credential and certifications', 'professional credentials and certification',  'key accountability', 'Contribution', 'Personal Project', 'Key Contribution', 'Strategic Plannings and executions', 'Strategic Plannings and execution', 'Strategic Planning and executions',]
        pe_list=['Project', 'Project Details','Additional Activities', 'Activities', 'Major Tasks', 'Responsibilities', 'key accountabilities', 'Contributions', 'Personal Projects', 'Key Contributions', 'Strategic Planning and execution', 'Academic projects', 'Key projects', 'projects/trainings', 'key implementations','PROJECTS ADMINISTERED','projects','Project', 'Additional Activity', 'Activity', 'Major Task', 'Responsibily', 'key accountability', 'Contribution', 'Personal Project', 'Key Contribution', 'Strategic Plannings and executions', 'Strategic Plannings and execution', 'Strategic Planning and executions', 'Academic project', 'Key project', 'project/training', 'projects/training', 'project/trainings', 'key implementation','Additional Activity', 'Activity', 'Major Task', 'Responsibily', 'Academic project', 'Key project', 'project/training', 'projects/training', 'project/trainings', 'key implementation']
        vo_list=['Volunteer', 'Volunteer Details','Volunteer Experience', 'Affiliations', 'Misc', 'Community Service','VOLUNTEERING','extra curricular activities','EXTRA-CURRICULAR INVOLVEMENT','Volunteer', 'Volunteer Experiences', 'Affiliation', 'Community Services']
        ed1_list=[x.lower() for x in ed_list]
        temp_ed= '\t'.join(ed1_list)
        ex1_list=[x.lower() for x in ex_list]
        temp_ex='\t'.join(ex1_list)
        sk1_list=[x.lower() for x in sk_list]
        temp_sk='\t'.join(sk1_list)
        aw1_list=[x.lower() for x in aw_list]
        temp_aw='\t'.join(aw1_list)
        ce1_list=[x.lower() for x in ce_list]
        temp_ce='\t'.join(ce1_list)
        pe1_list=[x.lower() for x in pe_list]
        temp_pe='\t'.join(pe1_list)
        vo1_list=[x.lower() for x in vo_list]
        temp_vol='\t'.join(vo1_list)
        #print(vo1_list)
        score = 0
        msg = []
        edu=0
        ed=0
        ex=0
        sk=0
        aw=0
        ce=0
        pe=0
        vo=0
        ed_date_format_list=[0,0]
        ex_date_format_list=[0,0]
        ach_msg = 0 #achievement variable message
        cert_msg = 0 #certification message flag
        sections['edu_year']=""
        sections['exp_year']=""
        sections['paragraph']=0
        checkfornos=0
        alphanum=""
        checkfornos2=0
        #print(sections)
        for key in sections.keys():
            #print(repr(key))
            #for sec in titles1:
                #if sec == key.lower():
                    #print(sec,type(sec),"Hi")
            for i in ed1_list:
                if(i in key.lower() and ed==0 and key.lower()!='n'):
                    score +=10
                    pres+=10
                    edu = 1
                    ed=1
                    edu_msg =1
                    ed_date_format_list=date_format(sections[key])
                    if ed_date_format_list>0:
                        score-=10
                        pres-=10
                    #print(ed_date_format_list)
                    sections['edu_year']=extract(sections[key])
                    sections['paragraph']+=paragraph_check(sections[key])
                    #print(key,temp_ed)
                    msg.append("Education Section is Present")
                    break
                #print(score)
            for i in ex1_list:    
                if(i in key.lower() and ex==0 and key.lower()!='n'):
                    score +=20
                    ex=1
                    sections['exp_year']=extract(sections[key])
                    ex_date_format_list=date_format(sections[key])
                    impact+=20
                    sections['paragraph']+=paragraph_check(sections[key])
                            #print(dummy_exp)
                    msg.append("Experience Section is Present")
                    #print(score)
                    #print(key,temp_ex)
                    break
                
            for i in sk1_list:
                if(i in key.lower() and sk==0 and key.lower()!='n'):
                    score +=20
                    sk=1
                    msg.append("Skills Section is Present")
                    sections['paragraph']+=paragraph_check(sections[key])
                    break
            for i in aw1_list:    
                if(i in key.lower() and aw==0 and key.lower()!='n'):
                    score +=5
                    impact+=5
                    aw=1
                    ach_msg = 1
                    alpha_num = ['one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen','twenty','thirty','fourty','fifty','sixty','seventy','eighty','ninety','hundred','thousand']
                    checkfornos = checknos(sections[key],alpha_num)
                    sections['paragraph']+=paragraph_check(sections[key])
                    msg.append("Awards/Achievement Section is Present")
                    #print(score)
                    #print(key)
                    break
            for i in vo1_list:    
                if(i in key.lower() and vo==0 and key.lower()!='n'):
                    pres+=5
                    score +=5
                    vo=1
                    vol_msg =1
                    msg.append("Volunteering Section is Present")
                    #print(score)
                    #print(key)
                    break
            for i in ce1_list:    
                if(i in key.lower() and ce==0 and key.lower()!='n'):
                    impact+=5
                    score +=10
                    cert_msg=1
                    ce=1
                    msg.append("Certificate Section is Present")
                    #print(score)
                    #print(key)
                    break
            for i in pe1_list:    
                if(i in key.lower() and pe==0 and key.lower()!='n'):
                    pres+=10
                    pe=1
                    score +=10
                    pro_msg=1
                    sections['paragraph']+=paragraph_check(sections[key])
                    alpha_num = ['one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen','twenty','thirty','fourty','fifty','sixty','seventy','eighty','ninety','hundred','thousand']
                    checkfornos2 = checknos(sections[key],alpha_num)
                    msg.append("Projects Section is Present")
                    #print(score)
                    #print(key)
                    break
        list_present=[ed,ex,sk,aw,ce,pe,vo]
        fed=0
        fex=0
        fsk=0
        faw=0
        fce=0
        fpe=0
        fvo=0
        sect=[]
        
        #import os
        if os.path.exists("./templates/file.html"):
            os.remove("./templates/file.html")
        else:
            print("The file does not exist") 
        for i in range(len(list_present)):
            if i ==0 and list_present[i]==0:
                #print("education" + "is absent")
                for ik in ed1_list:
                    if ik in text_main.lower():
                        fed=1
                score+=5
            if i ==1 and list_present[i]==0:
                #print("experience" + "is absent")
                for ik in ex1_list:
                    if ik in text_main.lower():
                        fex=1
                score+=10
            if i ==2 and list_present[i]==0:
                print("skill" + "is absent")
                for ik in sk1_list:
                    if ik in text_main.lower():
                        fsk=1
                score+=10
            if i ==3 and list_present[i]==0:
                #print("achievement/award" + "is absent")
                for ik in aw1_list:
                    if ik in text_main.lower():
                        faw=1
                score+=2
            if i ==4 and list_present[i]==0:
                #print("certification" + "is absent")
                for ik in ce1_list:
                    if ik in text_main.lower():
                        fce=1
                score+=5
            if i ==5 and list_present[i]==0:
                #print("project" + "is absent")
                for ik in pe1_list:
                    if ik in text_main.lower():
                        fpe=1
                score+=5
            if i ==6 and list_present[i]==0:
                #print("volunteer" + "is absent")
                for ik in vo1_list:
                    if ik in text_main.lower():
                        fvo=1
                score+=2
        print(fed,fex,fsk,fsk,faw,fce,fpe,fvo)
        improper_format=[]
        if(fed==1 and ed==0):
            improper_format.append('education')
        if(fex==1 and ex==0):
            improper_format.append('experience')
        if(fsk==1 and sk==0):
            improper_format.append('skill')
        if(faw==1 and aw==0):
            improper_format.append('achievement')
        if(fce==1 and ce==0):
            improper_format.append('certification')
        if(fpe==1 and pe==0):
            improper_format.append('project')
        if(fvo==1 and vo==0):
            improper_format.append('volunteer')
        print(improper_format)
            
        #print("EDU MSG",edu_msg)
        sections['Message']=msg
        # sections['Score']=round(((score/98)*100),2)
        rev=""
        '''misspelled = spell.unknown(text_main)
        sections["Errors"]=[]
        for word in misspelled :
            if(len(word))>3:
                sections["Errors"].append(word)'''
                
        stop_words = set(stopwords.words('english')) 
        d=""
        skillsets=0
        filtered_sentence=[]
        
    
        for i in sections.keys():
            if(i.lower()=="work experience"):
                score +=5
            if(i.lower()=="core competencies"):
                score +=5            
            if 'skill' in i.lower():
                skillsets=len(sections[i])
                for j in sections[i]:
                     
                    d=d+" "+j
                d = word_tokenize(d)
                 # print("I am here 2")
                 #print(d)
                for w in d: 
                    if w not in stop_words: 
                        if(len(w)>3):
                            filtered_sentence.append(w)
    
        sections['SkCount']=skillsets
        #sections['original']=filtered_sentence
        sections['linkedin']=Find(text_main)
        ck=sections['linkedin']
        link_msg=1
        if(len(ck) == 0):
            link_msg=0
        #print(type(len(ck)))
        #print('Heyo',sections['linkedin'])
        ac=0
        rd=0
        action_list=[]
        act_msg=0
        if actionwords(text_main)[0] > 5 :
            act_msg =1
            action_list=actionwords(text_main)[1]
            ac=10
            sections['action_word']="Your resume contains Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful."
        elif actionwords(text_main)[0]<=5:
            act_msg =0
            sections['action_word']="Your resume doesnt contain much Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful. "
        elif actionwords(text_main)[0]==0:
            
            act_msg =0
            sections['action_word']="Your resume doesnt contain any Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful. "
        fct_msg=0
        filler_list=[]
        if fillerwords(text_main)[0] > 1 :
            fct_msg =1
            filler_list=fillerwords(text_main)[1]
            
            #sections['action_word']="Your resume contains Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful."
        # elif fillerwords(text_main)[0]<=5:
        #     fct_msg =0
        #     filler_list=fillerwords(text_main)[1]
        
        elif fillerwords(text_main)[0]==0:
            
            fct_msg =0
            #sections['action_word']="Your resume doesnt contain any Action Verbs! Strong, unique action verbs show hiring managers that you have held different roles and skill sets. They also help your accomplishments stand out and make them more impactful. "
        
        #print(sections['action_word'])
        
        if redundancy(text_main) > 10:
            rd=5
            sections['redundancy']="1"
        elif redundancy(text_main)<=10:
            sections['redundancy']="0"
            
        
        #sections['edu_year']=extract(sections[dummy_edu])
        #print(sections['exp_year'])
        #print(sections['edu_year'])
        #print(sections['redundancy'])
        #print(filtered_sentence)
        sections['match']=match
        # Checking of resume score for message
        if(score == 100):
            rev="the score looks perfect but to get a more accurate comparison with the job you are looking for try analysing by adding Job Description"
        elif(score < 60):
            rev="this score suggests there is a lot of room for improvement. But don't worry! We have highlighted a number of quick fixes you can make to improve your resume's score and your success rate. Try adding more skills or experience into your resume to increase your resume score to 80% or above."
        else:
            rev="your score looks good however we have highlighted a number of quick fixes you can make to improve your resume's score. Try adding more skills or experience into your resume to increase your resume score."
        sections["Review"]=rev
        sections["Length"]=length
        sections["WordCount"]=word_count
        if sections["WordCount"] <= 600 and sections["WordCount"] > 1:
            score += 5
            sections['Message'].append("Word Count of the Resume is Optimal")
        else:
            sections['Message'].append("Word Count should be less than 600")

        if sections["Length"] and sections["WordCount"] > 1:
            score += 5
            sections['Message'].append("Length of Resume is Optimal")
        else:
            sections['Message'].append("Length of Resume should not exceed 2 pages")
        sections['Score']=round(((score/100)*100),2) #calculating score out of overall score.
        if(sections['Score'] >=90 and sections['Score'] <100):
            sections["Review"]="The Resume is correctly Parsed and Optimal. There may be some room for Improvement"
        if(sections['Score'] >=75 and sections['Score']<90):
            sections["Review"]="The Resume may be Correctly Parsed and Optimal. It is advised to pass DOCX Format in ATS Checker. There is certainly Some Room For Improvement"        
        count_passive1=[]
        count_passive=0
        co_pa=0
        for i in line1:
            if(is_passive(re.sub(r'[^\x00-\x7f]',r'', i))):
                count_passive += 1
                count_passive1.append(re.sub(r'[^\x00-\x7f]',r'', i))
        
                
        if(count_passive > 0):
            co_pa= 1
        elif(len(line1)==0):
            co_pa= 1
            
        else:
            co_pa=0
            ac += 5
        #print(impact)
        count_tense1=[]
        co_ta=0
        count_tenses=0
        for i in line1:
            if(tenses_res(re.sub(r'[^\x00-\x7f]',r'', i))):
                count_tenses += 1
                count_tense1.append(re.sub(r'[^\x00-\x7f]',r'', i))
                
        if(count_tenses >= 5):
            co_ta= 1
        elif(len(line1)==0):
            co_ta= 1
            
        else:
            co_ta=0
            ac += 5
            
        if(len(line1)==0):
            sections['paragraph']=0 
        elif sections['paragraph'] <= 2:
            ac += 5
            
        
        #print(sections.keys())
        
        cont=[]
        contact_all=contact_details(text_main)
        for elem in contact_all:
            if elem:
                if len(contact_all[0]) == 0:
                    cont.append('email')
                if len(contact_all[1]) == 0:
                    cont.append('phone')
                if len(contact_all[2]) == 0:
                    cont.append('linkedin')
                if len(contact_all[0]) !=0 and len(contact_all[1])!=0 and len(contact_all[2])!=0:
                    cont.append('all')
                    break

            if elem not in contact_all:
                cont.append("none")
            
            
        # management = ['budgeting', 'business planning', 'business re-engineering',
        # 'change management', 'consolidation', 'cost control',
        # 'decision making', 'developing policies', 'diversification',
        # 'employee evaluation', 'financing', 'government relations',
        # 'hiring', 'international management' ,'investor relations',
        # 'ipo' ,'joint ventures', 'labour relations',
        # 'merger & acquisitions', 'multi-sites management', 'negotiation',
        # 'profit & loss', 'organizational development', 'project management',
        # 'staff development', 'strategic partnership', 'strategic planning',
        # 'supervision' ]
        
        # operations = ['bidding', 'call centre operations', 'continuous improvement',
        # 'contract management', 'environmental protection', 'facility management',
        # 'inventory control', 'manpower planning','operations research',
        # 'outsourcing', 'policies & procedures', 'project co-ordination',
        # 'project management'] 
        
        # production = [
        # 'equipment design', 'equipment maintenance & repair',
        # 'equipment management', 'iso 9xxx / 1xxxxx', 'tqm',
        # 'order processing', 'plant design & layout', 'process engineering',
        # 'production planning', 'quality assurance', 'safety engineering']
        
        # logistics= [
        # 'distribution', 'transportation', 'jit',
        # 'purchasing & procurement', 'shipping', 'traffic management',
        # 'warehousing']
        
        # researchanddevelopment = ['design & specification', 'diagnostics', 'feasibility studies',
        # 'field studies', 'lab management', 'lab design',
        # 'new equipment design', 'patent application', 'product development',
        # 'product testing', 'prototype development', 'r&d management',
        # 'simulation dev.',' statistical analysis', 'technical writing']
        
        # sales= ['account management', 'b2b', 'contract negotiation',
        # 'customer relations', 'customer service', 'direct sales',
        # 'distributor relations', 'e-commerce', 'forecasting',
        # 'incentive programs', 'international business development',
        # 'international expansion', 'new account development', 'proposal writing',
        # 'product demonstrations', 'telemarketing', 'trade shows',
        # 'sales administration', 'sales analysis', 'sales kits',
        # 'sales management', 'salespersons recruitment', 'show room management',
        # 'sales support', 'sales training']
        
        # marketing = ['advertising', 'brand management', 'channel marketing',
        # 'competitive analysis', 'copywriting', 'corporate identity',
        # 'image development', 'logo development', 'market research & analysis',
        # 'marketing communication', 'marketing plan', 'marketing promotions',
        # 'media buying/evaluation', 'media relations', 'merchandising',
        # 'new product development', 'online marketing','packaging',
        # 'pricing', 'product launch']
        
        # administration = [
        # 'contract negotiation', 'equipment purchasing', 'forms and methods',
        # 'leases', 'mailroom management', 'office management',
        # 'policies & procedures', 'reception', 'records management',
        # 'security', 'space planning', 'word processing']
        
        # legal = [
        # 'contract preparation', 'copyrights & trademarks', 'corporate law',
        # 'company secretary', 'employment ordinance', 'ipo',
        # 'intellectual property', 'international agreements', 'licensing',
        # 'mergers & acquisitions', 'patents', 'shareholder proxies',
        # 'stock administration']
        
        # financeandaccounting = [
        # 'accounting management', 'accounts payable', 'venture capital relations',
        # 'accounts receivable', 'acquisitions & mergers', 'actuarial/rating analysis',
        # 'auditing','banking relations', 'budget control',
        # 'capital budgeting', 'capital investment', 'cash management',
        # 'cost accounting', 'cost control', 'credit/collections',
        # 'debt negotiations', 'equity/debt management', 'feasibility studies',
        # 'financial analysis', 'financial reporting', 'financing',
        # 'forecasting', 'foreign exchange', 'general ledger',
        # 'insurance', 'internal controls', 'investor relations',
        # 'ipo', 'lending', 'lines of credit',
        # 'management reporting', 'payroll', 'fund management',
        # 'profit planning', 'risk management', 'stockholder relations',
        # 'tax treasury', 'investor presentations']
        
        # humanresources = [
        # 'arbitration/mediation', 'career counseling', 'career coaching',
        # 'classified advertisements', 'company orientation', 'workforce forecast/planning',
        # 'compensation & benefits', 'corporate culture', 'training administration',
        # 'employee discipline', 'employee selection', 'executive recruiting',
        # 'grievance resolution', 'human resources management',
        # 'industrial relations', 'job analysis', 'labour negotiations',
        # 'outplacement', 'performance appraisal', 'salary administration',
        # 'succession planning', 'team building', 'training']
        
        # informationandtechnology = [
        # 'algorithm development', 'application database administration',
        # 'applications development', 'business systems planning', 'web site editor',
        # 'capacity planning', 'crm', 'cad',
        # 'edi', 'enterprise asset management', 'eap',
        # 'enterprise resource planning', 'erp', 'hardware management',
        # 'information management', 'integration software', 'intranet development',
        # 'java', 'c+++', 'c language','python','r language','ruby','html','javascript','c#','objective-c','php',
        #     'sql','shift','portal design/development',
        # 'software customization', 'software development', 'system analysis',
        # 'system design', 'system development', 'technical evangelism',
        # 'technical support', 'technical writing', 'telecommunications',
        # 'tracking system', 'unix', 'usability engineering',
        # 'user education', 'user documentation', 'user interface',
        # 'vendor sourcing', 'voice & data communications',
        # 'web development/design', 'web site content writer', 'word processing']
        
        # creative = [
        # 'character development' ,'creative writing', 'drawing',
        # 'musical composition', 'story line development', 'visual composition']
        
        # design= [
        # 'colour theory', 'dreamweaver', 'flash',
        # 'freehand', 'illustrator', 'photoshop',
        # 'picasa', 'corel draw', 'typography',
        # 'print design & layout', 'photography']
        
        # publicrelation = [
        # 'b2b communication', 'community relations', 'speech writing',
        # 'corporate image', 'corporate philanthropy', 'corporate publications',
        # 'corporate relations', 'employee communication', 'event planning',
        # 'fund raising', 'government relations', 'investor collateral',
        # 'media presentations', 'press release', 'risk mgt communication']

        analytical =['Research', 'collected', 'conducted', 'defined', 'detected', 'discovered', 'examined',
        'experimented', 'explored', 'extracted', 'found', 'gathered', 'identified', 'inquired', 'inspected',
        'investigated', 'located', 'measured', 'modelled', 'observed', 'researched', 'reviewed', 'searched',
        'studied',' surveyed', 'tested', 'tracked', 'Analyse', 'Evaluate', 'analysed', 'assessed', 'calculated',
        'catalogued', 'categorized', 'clarified', 'classified', 'compared', 'compiled', 'critiqued', 
        'derived', 'determined', 'diagnosed', 'estimated', 'evaluated', 'formulated', 'interpreted',
        'prescribed', 'organized', 'rated', 'recommended', 'reported', 'summarized', 'systematized', 
        'tabulated', 'assembled', 'built', 'coded', 'computed', 'constructed', 'converted', 'debugged',
        'designed', 'engineered', 'fabricated', 'installed', 'maintained', 'operated',
        'printed', 'programmed', 'proved', 'rectified', 'regulated', 'repaired', 'resolved',
        'restored', 'specified', 'standardized', 'upgraded', 'adjusted', 'allocated', 'appraised',
        'audited', 'balanced', 'budgeted', 'conserved', 'controlled', 'disbursed', 'figured', 'financed',
        'forecasted', 'netted', 'projected', 'reconciled']

        communication = ['addressed', 'articulated', 'authored', 'briefed', 'clarified', 
        'conveyed', 'composed', 'condensed', 'corresponded', 'debated', 'delivered', 'described',
        'discussed', 'drafted', 'edited', 'expressed', 'formulated', 'informed', 'instructed',
        'interacted', 'interpreted', 'lectured', 'negotiated', 'notified', 'outlined', 'reconciled',
        'reinforced', 'reported', 'presented', 'proposed', 'specified', 'spoke', 'translated',
        'wrote', 'advertised', 'influenced', 'marketed', 'solicited', 'contacted', 'convinced',
        'represented', 'persuaded', 'motivated',' communicated', 'elicited', 
        'recruited', 'promoted', 'publicized', 'enlisted', 'arbitrated', 'consulted', 'conferred',
        'interviewed', 'mediated', 'moderated', 'listened', 'responded', 'suggested']

        leadership = ['administered', 'appointed', 'approved', 'assigned', 'authorized', 'chaired',
        'conducted', 'contracted', 'controlled', 'coordinated', 'decided', 'delegated', 'directed',
        'developed', 'enforced', 'ensured', 'evaluated', 'executed', 'headed', 'hired', 'hosted', 
        'implemented', 'instituted', 'led', 'managed', 'overhauled', 'oversaw', 'prioritized', 
        'recruited', 'represented', 'strategized', 'supervised', 'trained', 'anticipated', 'arranged',
        'contacted', 'convened', 'logged', 'obtained', 'ordered', 'planned',
        'prepared', 'processed', 'purchased', 'recorded', 'registered', 'reserved', 'scheduled', 
        'verified', 'consolidated', 'distributed', 'eliminated', 'filed', 'grouped', 'incorporated',
        'merged', 'monitored', 'organized', 'regulated', 'reviewed', 'routed', 'standardized',
        'structured', 'submitted', 'systematized', 'updated']

        teamwork = ['aided', 'answered', 'arranged', 'catalogued', 'categorized', 'collated', 'collected',
        'coordinated', 'distributed', 'emailed', 'ensured', 'expedited', 'explained', 'filed', 'greeted',
        'handled', 'informed', 'implemented', 'maintained', 'offered', 'ordered', 'organized', 'performed',
        'prepared', 'processed', 'provided', 'purchased', 'recorded', 'received', 'resolved', 'scheduled', 'served',
        'supported', 'tabulated', 'collaborated', 'consulted', 'cooperated', 'liaised', 'reached', 
        'out']

        initiative = ['authored', 'began', 'built', 'changed', 'combined', 'conceived', 'constructed',
        'created', 'customized', 'designed', 'developed', 'devised', 'established', 'formed',
        'formulated', 'founded', 'generated', 'initiated', 'integrated', 'introduced', 'invented',
        'launched', 'originated', 'produced', 'shaped', 'staged', 'visualized', 'modified', 'revamped',
        'revised', 'updated', 'advocated', 'aided', 'assisted', 'cared', 'contributed', 'cooperated',
        'coordinated', 'ensured', 'furthered', 'guided', 'intervened', 'offered', 'referred',
        'rehabilitated', 'supplied', 'supported', 'volunteered', 'served', 'adapted', 'advised',
        'clarified', 'coached', 'counselled', 'demonstrated', 'educated', 'enabled',
        'encouraged', 'evaluated', 'explained', 'facilitated', 'familiarized', 'individualized',
        'instructed', 'mentored', 'modelled' ] 


        ab = text_main.lower()
        sentence = nltk.tokenize.sent_tokenize(ab)
        comp1 = check(sentence,analytical)
        #converting list of lists to a flat list
        # comp1 = [item for elem in comp1 for item in elem]
        try:
            comp1_count = len(comp1)
        except:
            comp1_count = 0
        comp2 = check(sentence,communication)
        try:
            comp2_count = len(comp2)
        except:
            comp2_count = 0
        
        comp3 = check(sentence,leadership)
        try:
            comp3_count = len(comp3)
        except:
            comp3_count = 0
        
        comp4 = check(sentence,teamwork)
        try:
            comp4_count = len(comp4)
        except:
            comp4_count = 0
        
        comp5 = check(sentence,initiative)
        try:
            comp5_count = len(comp5)
        except:
            comp5_count = 0
        # comp6 = check(sentence,sales)
        # try:
        #     comp6_count = len(comp6)
        # except:
        #     comp6_count = 0
        
        # comp7 = check(sentence,marketing)
        # try:
        #     comp7_count = len(comp7)
        # except:
        #     comp7_count = 0
        
        # comp8 = check(sentence,administration)
        # try:
        #     comp8_count = len(comp8)
        # except:
        #     comp8_count = 0
        # comp9 = check(sentence,legal)
        # try:
        #     comp9_count = len(comp9)
        # except:
        #     comp9_count = 0
        
        # comp10 = check(sentence,financeandaccounting)
        # try:
        #     comp10_count = len(comp10)
        # except:
        #     comp10_count = 0
        # comp11 = check(sentence,humanresources)
        # try:
        #     comp11_count = len(comp11)
        # except:
        #     comp11_count = 0
        
        # comp12 = check(sentence,informationandtechnology)
        # try:
        #     comp12_count = len(comp12)
        # except:
        #     comp12_count = 0
        
        # comp13 = check(sentence,creative)
        # try:
        #     comp13_count = len(comp13)
        # except:
        #     comp13_count = 0
        
        # comp14 = check(sentence,design)
        # try:
        #     comp14_count = len(comp14)
        # except:
        #     comp14_count = 0
        
        # comp15 = check(sentence,publicrelation)
        # try:
        #     comp15_count = len(comp15)
        # except:
        #     comp15_count = 0

        
        
        
        match_dict = {'analytical' : comp1, 'communication': comp2, 'leadership': comp3, 'teamwork': comp4,
                    'initiative': comp5} 
        
        count_dict = {'analytical' : comp1_count, 'communication': comp2_count, 'leadership': comp3_count, 
                    'teamwork': comp4_count, 'initiative': comp5_count}


        count_competancies=[]
        for i in count_dict.keys():
            if(count_dict[i]!=0):
                count_competancies.append(i)
        sumaa=0
        for key in count_dict.keys():
            sumaa+=count_dict[key]

        nl=[]
        quant=0
        if checkfornos==1 or checkfornos2==1:
            quant=1
        elif checkfornos!=1 and checkfornos2!=1:
            nl=quan(text_main,aw1_list+pe1_list )
        if(nl[1]):
            quant=1
                
        print(sentence)
        print("Hey",len(match_dict))
        print(count_dict)
        print(count_competancies)
        ab = text_main.lower()
        sentence = nltk.tokenize.sent_tokenize(ab)

        barplot(count_dict)
        
        session['bared'] = count_dict
        count_dict_dict={}
        stop_words = set(stopwords.words('english')) 
        filtered_sentence = [w for w in sentence if not w in stop_words] 
        for i in filtered_sentence:
            count_dict_dict[i]=filtered_sentence.count(i)

        #wordcloud(count_dict_dict)
                
        if ed_date_format_list==1:
            pres-=5
        # if ex_date_format_list[1]==1:
        #     pres-=10
        skillmatch=skillsMatch(text_main)

        namee=extract_name(text_main)
        empty_competency=""
        cot=0
        for i in match_dict.keys():
            cot=cot+len(match_dict[i])

        if(cot==0):
            empty_competency = "You might want to add few competencies in your resume as it's an efficient way to provide comprehensive proof that you are qualified for a certain job. "

        # if (len(match_dict['management'] == 0) and (len(match_dict['operations'] == 0):
        #     print("Yo")
        #namee=' '.join(w.capitalize() for w in namee.split())
        #print(namee,cont,count_tense1,count_passive1,sections['edu_year'],sections['exp_year'])    
        #end of check
        print(pro_msg,edu_msg,sections['redundancy'],vol_msg,cert_msg,link_msg,ach_msg,act_msg,co_pa)
        a_list = nltk.tokenize.sent_tokenize(text_main)

        #softskill = softskills(a_list)
        hardskill = hardskills(a_list)
        phonenumber = phone1(text_main)
        emailid = email1(text_main)
        LinkedIn = linkedin1(text_main)
    # print(softskill)
    # print(hardskill)
    # print(phonenumber)
    # print(emailid)
    # print(LinkedIn)
        job_description = session['data']
        job_description = job_description.lower()
        jd = nltk.tokenize.sent_tokenize(job_description)
        #softskill_jd = softskills(jd)
        hardskill_jd = hardskills(jd)
    # print(hardskill_jd)
    # print(softskill_jd)
        #matching_hs=matching(hardskill,hardskill_jd)
        matching_hs=[hardskill,hardskill_jd]
        print(matching_hs)
        #matching_ss=matching(softskill,softskill_jd)
        matching_ed=matching(edmatch(text_main),edmatch(job_description))

        a_l=edmatch(text_main)
        b_l=edmatch(session['data'])
        c_l=list(set(a_l).intersection(set(b_l)))
        comp1_jd = check(jd,analytical)
        #converting list of lists to a flat list
        # comp1 = [item for elem in comp1 for item in elem]
        try:
            comp1_jd_count = len(comp1_jd)
        except:
            comp1_jd_count = 0
        comp2_jd = check(jd,communication)
        try:
            comp2_jd_count = len(comp2_jd)
        except:
            comp2_jd_count = 0
        
        comp3_jd = check(jd,leadership)
        try:
            comp3_jd_count = len(comp3_jd)
        except:
            comp3_jd_count = 0
        
        comp4_jd = check(jd,teamwork)
        try:
            comp4_jd_count = len(comp4_jd)
        except:
            comp4_jd_count = 0
        
        comp5_jd = check(jd,initiative)
        try:
            comp5_jd_count = len(comp5_jd)
        except:
            comp5_jd_count = 0

        match_dict_jd = {'analytical' : [comp1,comp1_jd], 'communication': [comp2,comp2_jd], 'leadership': [comp3,comp3_jd], 'teamwork': [comp4,comp4_jd],
                    'initiative': [comp5,comp5_jd]} 
        
        count_dict_jd = {'analytical' : comp1_jd_count, 'communication': comp2_jd_count, 'leadership': comp3_jd_count, 
                    'teamwork': comp4_jd_count, 'initiative': comp5_jd_count}

        print(jd_score)
        try:

            ss_score=(len(list(set(comp1).intersection(set(comp1_jd))))+len(list(set(comp2).intersection(set(comp2_jd))))+len(list(set(comp3).intersection(set(comp3_jd))))+len(list(set(comp4).intersection(set(comp4_jd))))+len(list(set(comp5).intersection(set(comp5_jd)))))/(comp1_jd_count+comp2_jd_count+comp3_jd_count+comp4_jd_count+comp5_jd_count)
            print(ss_score)
        except:
            ss_score=0

        print(type(ac))
        print(type(rd))
        print(type(pres))
        print(type(impact))
        print(type(ss_score))
        print(type(jd_score))
        try:
            matcc=len(c_l)/len(matching_hs[1])*100
        except:
            matcc=0


        #end of check
        #print(pro_msg,edu_msg,sections['redundancy'],vol_msg,cert_msg,link_msg,ach_msg,act_msg)
        return render_template('jd-service.html', results=sections, ss_score=int(ss_score*100), matcc=matcc, jd_score = int(jd_score), c_l=c_l, matching_hs=matching_hs, phonenumber=phonenumber, emailid=emailid, linkedin=LinkedIn, typee=typee, pro_msg=pro_msg,edu_msg=edu_msg,matched_comment= rev,jd_msg=jd_msg,score= sections['Score'],email=email,education=edu,rud_mdg=sections['redundancy'],vol_msg=vol_msg,cert_msg=cert_msg,link_msg=link_msg,ach_msg = ach_msg,count_pass=co_pa,count_tense=co_ta,act_msg=act_msg,para=sections['paragraph'],depth=int(((ac+rd)/30*100)),pres=int(pres/25*100),impact=int(impact/45 *100), scor= (ac+rd+pres+impact), match_dict_jd=match_dict_jd, count_dict_jd=count_dict_jd )
        #return render_template('display.html', results=sections)   
    except Exception as e:
        print(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return render_template('error.html')

        
def hardskills(text):
    m = ['.net', 'fashion', 'process improvement', 'account management', 'fda', 'process improvements', 'accounting', 'field sales', 'procurement', 'accounts payable', 'filing', 'product design', 'accounts receivable', 'finance', 'product development', 'acquisition', 'financial analysis', 'product knowledge', 'acquisitions', 'financial management', 'product line', 'administrative support', 'financial performance', 'product management', 'admissions', 'financial reporting', 'product marketing', 'Adobe', 'financial reports', 'product quality', 'Adobe Creative Suite', 'financial services', 'program development', 'advertising', 'financial statements', 'program management', 'affiliate', 'financing', 'programming', 'agile', 'fitness', 'project delivery', 'algorithms', 'Flex', 'project management', 'alliances', 'forecasting', 'project management skills', 'analysis', 'forecasts', 'project plan', 'analytical', 'frameworks', 'project planning', 'analytical skills', 'front-end', 'proposal', 'analytics', 'fulfillment', 'prospecting', 'analyze data', 'fundraising', 'protocols', 'analyzing data', 'GAAP', 'prototype', 'android', 'general ledger', 'psychology', 'annual budget', 'German', 'public health', 'API', 'GIS', 'public policy', 'APIs', 'governance', 'public relations', 'architecture', 'graphic design', 'publications', 'architectures', 'hardware', 'publishing', 'assembly', 'health', 'purchase orders', 'asset management', 'healthcare', 'purchasing', 'audio', 'help desk', 'Python', 'audit', 'higher education', 'QA', 'auditing', 'hing', 'quality assurance', 'AutoCAD', 'hospital', 'quality control', 'automation', 'hospitality', 'quality management', 'aviation', 'hotel', 'quality standards', 'AWS', 'hotels', 'R (programming language)', 'banking', 'HRIS', 'raw materials', 'benchmark', 'HTML', 'real estate', 'beverage', 'HTML5', 'real-time', 'BI', 'human resource', 'reconcile', 'big data', 'I-DEAS', 'reconciliation', 'billing', 'IBM', 'recruit', 'biology', 'immigration', 'recruiting', 'brand', 'in-store', 'recruitment', 'branding', 'InDesign', 'regulations', 'broadcast', 'industry experience', 'regulatory', 'budget', 'industry trends', 'regulatory compliance', 'budget management', 'information management', 'regulatory requirements', 'budgeting', 'information security', 'relationship building', 'build relationships', 'information system', 'relationship management', 'business administration', 'information systems', 'repairs', 'business analysis', 'information technology', 'reporting', 'business cases', 'installation', 'research', 'business continuity', 'instructional design', 'research projects', 'business development', 'instrumentation', 'researching', 'business intelligence', 'internal audit', 'resource management', 'business issues', 'internal communications', 'retail', 'business management', 'internal controls', 'retention', 'business planning', 'internal customers', 'revenue growth', 'business plans', 'internal stakeholders', 'RFP', 'business process', 'international', 'RFPs', 'business requirements', 'internship', 'risk assessment', 'business stakeholders', 'intranet', 'risk assessments', 'business strategy', 'inventory', 'risk management', 'business systems', 'inventory management', 'root cause', 'C\xa0(programming language)', 'investigate', 'root cause', 'C#', 'investigation', 'routing', 'C++', 'investigations', 'SaaS', 'CAD', 'invoices', 'safety', 'call center', 'invoicing', 'sales', 'case management', 'iOS', 'sales experience', 'cash flow', 'iPhone', 'sales goals', 'certification', 'ISO', 'sales management', 'CFA', 'IT infrastructure', 'sales operations', 'change management', 'ITIL', 'Salesforce', 'chemicals', 'Java', 'SAP', 'chemistry', 'Javascript', 'SAS', 'circuits', 'JIRA', 'scheduling', 'Cisco', 'journal entries', 'SCI', 'client relationships', 'journalism', 'scripting', 'client service', 'key performance indicators', 'scrum', 'client services', 'KPI', 'SDLC', 'cloud', 'KPIs', 'security clearance', 'CMS', 'LAN', 'segmentation', 'co-op', 'law enforcement', 'SEO', 'coaching', 'leadership development', 'service delivery', 'coding', 'lean', 'SharePoint', 'commissioning', 'legal', 'six sigma', 'complex projects', 'legislation', 'small business', 'compliance', 'licensing', 'social media', 'computer applications', 'life cycle', 'software development', 'computer science', 'lifecycle', 'software development life cycle', 'computer software', 'lighting', 'software engineering', 'construction', 'Linux', 'SolidWorks', 'consulting', 'litigation', 'SOPs', 'consulting experience', 'logistics', 'sourcing', 'consulting services', 'machine learning', 'specifications', 'consumers', 'man resources', 'spelling', 'content', 'manage projects', 'sports', 'continuous improvement', 'management consulting', 'spreadsheets', 'contract management', 'management experience', 'SQL', 'contracts', 'market research', 'SQL server', 'controls', 'marketing', 'staffing', 'conversion', 'marketing materials', 'stakeholder management', 'correspondence', 'marketing plans', 'standard operating procedures', 'cost effective', 'marketing programs', 'standardization', 'cost reduction', 'marketing strategy', 'start-up', 'counsel', 'mathematics', 'startup', 'counseling', 'MATLAB', 'statistical analysis', 'CPG', 'matrix', 'statistics', 'CPR', 'mechanical engineering', 'status reports', 'CRM', 'media relations', 'strategic direction', 'cross-functional team', 'medical device', 'strategic initiatives', 'CSS', 'merchandising', 'strategic planning', 'customer experience', 'metrics', 'strategic plans', 'customer facing', 'Microsoft Office', 'strategy', 'customer requirements', 'Microsoft Office Suite', 'strong analytical skills', 'customer service', 'Microsoft Word', 'supervising', 'customer-facing', 'migration', 'supervisory experience', 'D (programming language)', 'mining', 'supply chain', 'daily operations', 'MIS', 'supply chain management', 'data analysis', 'mobile', 'support services', 'data center', 'modeling', 'Tableau', 'data collection', 'mortgage', 'tablets', 'data entry', 'MS Excel', 'talent acquisition', 'data management', 'MS Office', 'talent management', 'data quality', 'MS Project', 'tax', 'database', 'negotiation', 'technical', 'datasets', 'networking', 'technical issues', 'deposits', 'non-profit', 'technical knowledge', 'design', 'nursing', 'technical skills', 'development activities', 'office software', 'technical support', 'digital marketing', 'on-boarding', 'telecom', 'digital media', 'on-call', 'test cases', 'distribution', 'operating systems', 'test plans', 'DNS', 'operational excellence', 'testing', 'documentation', 'operations', 'therapeutic', 'documenting', 'operations management', 'trade shows', 'drafting', 'oracle', 'training', 'drawings', 'ordering', 'transactions', 'driving record', 'OS', 'transport', 'due diligence', 'outreach', 'transportation', 'dynamic environment', 'outsourcing', 'travel', 'e-commerce', 'partnership', 'travel arrangements', 'ecommerce', 'partnerships', 'troubleshooting', 'economics', 'payments', 'TV', 'editing', 'payroll', 'Twitter', 'editorial', 'PeopleSoft', 'UI', 'electrical', 'performance improvement', 'underwriting', 'electrical engineering', 'performance management', 'Unix', 'electronics', 'performance metrics', 'usability', 'EMEA', 'pharmaceutical', 'user experience', 'employee engagement', 'pharmacy', 'UX', 'employee relations', 'phone calls', 'valid drivers license', 'end user', 'photography', 'value proposition', 'engagement', 'Photoshop', 'variances', 'engineering', 'physical security', 'vendor management', 'ERP', 'physics', 'vendors', 'ETL', 'PMP', 'video', 'event planning', 'policies', 'VMware', 'expenses', 'portfolio management', 'warehouse', 'experimental', 'positioning', 'web services', 'experiments', 'PR', 'windows', 'external partners', 'presentation', 'workflows', 'fabrication', 'presentations', 'writing', 'Facebook', 'process development']
    matched=[]
    for i in text:
        li = [e for e in m if(e in i)]
        if li:
            matched.append(li)
    result = [item for sublist in matched for item in sublist]
    return result

def phone1(string):
    phone=re.findall(r"(?<!\d)\d{10}(?!\d)", string)
    phn=0
    if phone:
        phn = 1
    else:
        phn =0
    return phn

def email1(string):
    email_=re.findall(r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)",string)
    mail=0
    if email_:
        mail =1
    else:
        mail=0
    return mail

def linkedin1(string):
    linkedin_username = re.findall(r"(?:https?:)?\/\/(?:[\w]+\.)?linkedin\.com\/in\/(?P<permalink>[\w\-\_À-ÿ%]+)\/?",string)
#     if len(linkedin_username) != 0:
#         linkedin_username[0] = 'https://www.linkedin.com/in/'+ linkedin_username[0]
    if linkedin_username:
        linkedIn = 1
    else:
        linkedIn = 0
    return linkedIn

def matching(li1,li2):
    common = []
    for i in li1:
        if i in li2:
            common.append(i)
    final_list = [] 
    for x in common: 
        if x not in final_list: 
            final_list.append(x) 
    # print(final_list)
    count_res = {}
    count_jd ={}
    for i in final_list:
        if i not in count_res:
            count_res.update({i: li1.count(i)})
        if i not in count_jd:
            count_jd.update({i: li2.count(i)})
    print(count_res)
    print(count_jd)
    return [count_res,count_jd]
#     return count_res, count_jd

def edmatch(text):
   
    m = ['AA','AS','AAS','AE','AB','AAA','ALM','AGS','AMIE','ASN','AF','AT','AAB','AAS','AAT','ABS','ABA','AES','ADN','AET','AFA','APE','AIT','AOS','ASPT-APT','APS',
    'BE', 'BS', 'BFA','BAS','BSBA','BFA','BCom', 'BMOS','BComm','B.Acy','B.Acc','B. Accty','BBusSc','BSN', 'BBus','BSC','BSET','BCOM','BMS','BA','BIBE','BCA','BBA','BBM','BIBE','BTECH','BARCH','BAA','BAAS','BAppSc(IT)','BDES','BENG','BSE','BESC','BSEng', 'BASc','BAccSci''BCompt', 'BEc', 'BEconSc' , 'BAOM', 'BCompSc','BComp','BCA','BBIS','BMedSci','BSPH','BMedBiol','BN', 'BNSc', 'BScN', 'BSN', 'BNurs', 'BSN', 'BHSc',
    'BHS','BHSc','BKin', 'BHK','BAT','BAvn','BD', 'BDiv','BTh','Th.B.','BTech' 'BTheol','BRE','BRS','BIS','BJ', 'BAJ', 'BSJ','BJourn','BLArch','B.L.A.','BGS', 'BSGS','BAPSY','BSocSc','BMathSc','BURP','BPlan',
    'BPAPM','B.S.F.', 'B.Sc.F.','BMus',
    'CA','CDCS','CBSE',
    'DDS','DELF','DBA',
    'EdD',
    'GED','GradIETE',
    'HSC','HSSC',
    'ICSE',
    'JD',
    'MD','MCA','ME','MS','MTECH', 'MBA','MCOM','MA','MFA','MCAT','MAcc', 'MAc', 'MAcy',
    'MAS','MEcon','MArch','MASc', 'MAppSc', 'MApplSc', 'MASc', 'MAS','MA', 'MAT','MLA', 'MLS', 'MALS',
    'MBus','MBA','MBI','MChem','MCom','MCA','MCJ','MDes', 'MDesign','MDiv','MEcon','MEd', 'EdM', 'MAEd', 'MSEd', 'MSE', 'MEdL',
    'MEnt','MEng', 'ME', 'MEM','MFin','MFA','MHA','MHS','MH','MILR','MIS','MISM', 'MSIM', 'MIS','MSIT', 'MScIT', 'MJ','MJur',
    'LLM','MSL','MArch','MLitt','MA', 'ALM', 'MLA', 'MLS', 'MALS','MLIS','MM','MMath','MMus','MPharm','MPhil','MPhys','MPS',
    'MPA','MPAff','MPH','MPP','MRb','MSc','STM','MSM','MSc','MSci', 'MSi', 'ScM', 'MS', 'MSHS','SM','MSE','MFin','HRD','MSHRD',
    'MSMIS','MSIS','MSIT', 'MScIT', 'MSN','MSPM','MSc','MSM','MSL','SCM','MSSCM','MST','MSW','MSSc','ChM','MS','MCh','MChir',
    'MSt','ThM', 'MTh','MTS','MVSC','MVSc'
    'PGD','PGDB','PFDFM','PGDIM','PGDBO','PHD','PharmD',
    'SSC','SCB','SB','SDes'
    'X', 'XII']
    matched=[]
    li = [e for e in m if(e.lower() in text.lower())]
    if li:
        matched.append(li)
    result = [item for sublist in matched for item in sublist]
    return result



   

@app.route('/about',methods= ["GET",'POST'])
def about():
    return render_template('about.html')

@app.route('/hi',methods= ["GET",'POST'])
def hi():
    return render_template('unsupported.html')




@app.route('/contact',methods= ["GET",'POST'])
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
