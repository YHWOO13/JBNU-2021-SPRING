'''
 Author: Yoonhyuck WOO, Yongseong Moon / JBNU_Industrial Information system Engineering
 Date; 05.03.2021- 6.14.2021
 Title: Database Design Term project: Expect a soccer player's annual value
 Professor: Joon-Soo, BAE '''

import numpy as np
import pandas as pd
import pymysql
import random
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn import model_selection
from sklearn.tree import plot_tree
from tkinter import *

# Call the data Set
conn= pymysql.connect(host = "210.117.165.86", user ='dbuser09', password = 'dbuser2021', db ='dbuser09_schema',port = 3306, charset = 'utf8', cursorclass = pymysql.cursors.DictCursor)
curs= conn.cursor()
sql = "select * from soccer_player"
curs.execute(sql)
rows = curs.fetchall()
conn.close()

# ============= 'age','reputation', 'stat_overall', 'stat_potential', 'stat_skill_moves' =============
def scaling(df, columns):
    for col in columns:
        mean = df[col].mean()
        print(columns, mean)
        std = df[col].std()
        print(columns, std)
        df[col] = df[col].apply(lambda x: (x-mean)/std)

    return df

data = pd.DataFrame(rows)

#====================== ST ==============================
def ST_DCT(data):
    ST_df = data['position'] == 'ST'
    ST_df = data[ST_df]
    ST_train = ST_df[['age','reputation', 'stat_overall', 'stat_potential', 'stat_skill_moves', 'value']]
    columns_tra = ['age','reputation', 'stat_overall', 'stat_potential', 'stat_skill_moves']

    ST_train = scaling(ST_train, columns_tra)
    ST_train['value'] = ST_train['value'] / 100000

    # plt.hist(ST_train['value'], bins=40)
    # # plt.boxplot(ST_train['value'])
    # plt.show()

    # 구간화_1
    bins = [0,100,200,300,400,500,600,700,800,1300]
    # bins_lable = ['C','B','B+','A','A+','S','S+']
    bins_lable = ['9','8','7','6','5','4','3','2','1']

    #스켈링 후
    # bins = [-5,0,2,4,6,8,15,19]
    # bins_lable = ['7','6','5','4','3','2','1']
    #
    ST_train['level'] = pd.cut(ST_train['value'], bins, right = False , labels=bins_lable)
    # print(ST_train)

    x_var = ST_train[['age','reputation', 'stat_overall', 'stat_potential', 'stat_skill_moves']].values
    y_var = ST_train['level'].values
    x_train,x_test, y_train, y_test = model_selection.train_test_split(x_var, y_var, train_size = 0.8)

    feauture_name = ST_train.columns[:6]
    target_name = ST_train['level'].unique().tolist()
# ================================== DCT ==================================
    clf = tree.DecisionTreeClassifier(criterion="entropy",max_depth = 7)
    clf = clf.fit(x_train, y_train)

    pred = clf.predict(x_test)
    acc= clf.score(x_test, pred )
    print('acc:', acc)

    plt.figure(figsize=(50,50))
    plot_tree(clf,feature_names = feauture_name,
              class_names = target_name,
              filled = True, rounded = True)

    # plt.show()
    plt.savefig('ST.png')
#====================== MF ==============================
def MF_DCT(data):
    MF_df = data['position'] == 'MF'
    MF_df = data[MF_df]
    MF_train = MF_df[['age','reputation', 'stat_overall', 'stat_potential', 'stat_skill_moves', 'value']]
    columns_tra = ['age','reputation', 'stat_overall', 'stat_potential', 'stat_skill_moves']

    MF_train = scaling(MF_train, columns_tra)
    MF_train['value'] = MF_train['value'] / 100000

    # plt.hist(MF_train['value'], bins=40)
    # # plt.boxplot(ST_train['value'])
    # plt.show()
    # exit()
    # 구간화_1
    bins = [0,50,100,150,200,250,300,350,400,1300]
    # bins_lable = ['C','B','B+','A','A+','S','S+']
    bins_lable = ['9','8','7','6','5','4','3','2','1']

    #스켈링 후
    # bins = [-5,0,2,4,6,8,15,19]
    # bins_lable = ['7','6','5','4','3','2','1']
    #
    MF_train['level'] = pd.cut(MF_train['value'], bins, right = False , labels=bins_lable)
    # print(ST_train)

    x_var = MF_train[['age','reputation', 'stat_overall', 'stat_potential', 'stat_skill_moves']].values
    y_var = MF_train['level'].values
    x_train,x_test, y_train, y_test = model_selection.train_test_split(x_var, y_var, train_size = 0.8)

    feauture_name = MF_train.columns[:6]
    target_name = MF_train['level'].unique().tolist()
# ================================== DCT ==================================
    clf = tree.DecisionTreeClassifier(criterion="entropy",max_depth = 6)
    clf = clf.fit(x_train, y_train)

    pred = clf.predict(x_test)
    acc= clf.score(x_test, pred )
    print('acc:', acc)

    plt.figure(figsize=(85,85))
    plot_tree(clf,feature_names = feauture_name,
              class_names = target_name,
              filled = True, rounded = True)

    # plt.show()
    plt.savefig('MF.png')
#====================== DF ==============================
def DF_DCT(data):
    DF_df = data['position'] == 'DF'
    DF_df = data[DF_df]
    DF_train = DF_df[['age', 'reputation', 'stat_overall', 'stat_potential', 'stat_skill_moves', 'value']]
    columns_tra = ['age', 'reputation', 'stat_overall', 'stat_potential', 'stat_skill_moves']

    DF_train = scaling(DF_train, columns_tra)
    DF_train['value'] = DF_train['value'] / 100000

    # plt.hist(DF_train['value'], bins=40)
    # # plt.boxplot(DF_train['value'])
    # plt.show()
    # exit()
    # 구간화_1
    bins = [0, 100, 200, 300, 400, 500, 600, 1300]
    # bins_lable = ['C','B','B+','A','A+','S','S+']
    bins_lable = ['7','6', '5', '4', '3', '2', '1']

    # 스켈링 후
    # bins = [-5,0,2,4,6,8,15,19]
    # bins_lable = ['7','6','5','4','3','2','1']
    #
    DF_train['level'] = pd.cut(DF_train['value'], bins, right=False, labels=bins_lable)

    x_var = DF_train[['age', 'reputation', 'stat_overall', 'stat_potential', 'stat_skill_moves']].values
    y_var = DF_train['level'].values
    x_train, x_test, y_train, y_test = model_selection.train_test_split(x_var, y_var, train_size=0.8)

    feauture_name = DF_train.columns[:6]
    target_name = DF_train['level'].unique().tolist()

    clf = tree.DecisionTreeClassifier(criterion="entropy", max_depth = 6)
    clf = clf.fit(x_train, y_train)

    pred = clf.predict(x_test)
    acc = clf.score(x_test, pred)
    print('acc:', acc)

    plt.figure(figsize=(40, 40))
    plot_tree(clf, feature_names=feauture_name,
              class_names=target_name,
              filled=True, rounded=True)

    # plt.show()
    plt.savefig('DF.png')
#====================== GK ==============================
def GK_DCT(data):
    GK_df = data['position'] == 'GK'
    GK_df = data[GK_df]
    GK_train = GK_df[['age', 'reputation', 'stat_overall', 'stat_potential', 'stat_skill_moves', 'value']]
    columns_tra = ['age', 'reputation', 'stat_overall', 'stat_potential']

    GK_train = scaling(GK_train, columns_tra)
    GK_train['value'] = GK_train['value'] / 100000

    # plt.hist(GK_train['value'], bins=40)
    # plt.show()
    # exit()

    # 구간화_1
    bins = [0, 50, 100, 150, 200, 250, 1000]
    # bins_lable = ['C','B','B+','A','A+','S','S+']
    bins_lable = ['6', '5', '4', '3', '2', '1']

    # 스켈링 후
    # bins = [-5,0,2,4,6,8,15,19]
    # bins_lable = ['7','6','5','4','3','2','1']
    #
    GK_train['level'] = pd.cut(GK_train['value'], bins, right=False, labels=bins_lable)

    x_var = GK_train[['age', 'reputation', 'stat_overall', 'stat_potential', 'stat_skill_moves']].values
    y_var = GK_train['level'].values
    x_train, x_test, y_train, y_test = model_selection.train_test_split(x_var, y_var, train_size=0.8)

    feauture_name = GK_train.columns[:6]
    target_name = GK_train['level'].unique().tolist()

    clf = tree.DecisionTreeClassifier(criterion="entropy", max_depth = 5)
    clf = clf.fit(x_train, y_train)

    pred = clf.predict(x_test)
    acc = clf.score(x_test, pred)
    print('acc:', acc)

    plt.figure(figsize=(40, 40))
    plot_tree(clf, feature_names=feauture_name,
              class_names=target_name,
              filled=True, rounded=True)

    # plt.show()
    plt.savefig('GK.png')

def GUI():
    win = Tk()
    win.geometry('445x445')
    win.title('Value_expect')

    lab1 = Label(win)
    lab1.config(text='Name')
    lab1.pack()
    ent1 = Entry(win)
    ent1.pack()

    lab2 = Label(win)
    lab2.config(text='Age')
    lab2.pack()
    ent2 = Entry(win)
    ent2.pack()

    lab3 = Label(win)
    lab3.config(text='continent')
    lab3.pack()
    ent3 = Entry(win)
    ent3.pack()

    lab4 = Label(win)
    lab4.config(text='Position \n  (1. ST 2. MF 3. DF 4. GK)')
    lab4.pack()
    ent4 = Entry(win)
    ent4.pack()

    lab5 = Label(win)
    lab5.config(text='Prefer_foot')
    lab5.pack()
    ent5 = Entry(win)
    ent5.pack()

    lab6 = Label(win)
    lab6. config(text='Reputation')
    lab6.pack()
    ent6 = Entry(win)
    ent6.pack()

    lab7 = Label(win)
    lab7. config(text='stat_overall')
    lab7.pack()
    ent7 = Entry(win)
    ent7.pack()


    lab8 = Label(win)
    lab8. config(text='stat_potential')
    lab8.pack()
    ent8 = Entry(win)
    ent8.pack()


    lab9 = Label(win)
    lab9. config(text='stat_skill_moves')
    lab9.pack()
    ent9 = Entry(win)
    ent9.pack()

    lab10 = Label(win)

    def Value_expect():
        name = str(ent1.get())
        continent = str(ent3.get())
        foot = str(ent5.get())
        position = int(ent4.get())
        age = int(ent2.get())
        reputation = int(ent6.get())
        overall = int(ent7.get())
        potential = int(ent8.get())
        skill = int(ent9.get())

        def ST_expect(age, reputation, overall, potential, skill):
            age = (age - 24.82) / 4.57
            reputation = (reputation - 1.16) / 0.48
            overall = (overall - 67.4) / 6.9
            potential = (potential - 72.55) / 6.07
            skill = (skill - 2.78) / 0.65
            if overall <= 1.463:
                if overall <= 1.029:
                    return 9
                else:
                    if potential <= 0.816:
                        return 9
                    else:
                        if potential <= 1.31:
                            if overall <= 1.173:
                                return 9
                            else:
                                if potential <= 1.145:
                                    if age <= 0.149:
                                        return 8
                                    else:
                                        return 9
                                else:
                                    return 9
                        else:
                            if age <= -0.07:
                                if age <= -0.726:
                                    if overall <= 1.173:
                                        return 8
                                    else:
                                        return 8
                                else:
                                    if overall <= 1.173:
                                        return 9
                                    else:
                                        return 8
                            else:
                                return 8

            else:
                if overall <= 2.042:
                    if overall <= 1.897:
                        if age <= 1.9:
                            if age <= -0.507:
                                if overall <= 1.752:
                                    return 8
                                else:
                                    return 6
                            else:
                                return 8
                        else:
                            if potential <= 1.145:
                                if age <= 2.119:
                                    return 8
                                else:
                                    return 9
                            else:
                                return 9
                    else:
                        if age <= 0.259:
                            return 6
                        else:
                            if age <= 2.009:
                                return 8
                            else:
                                return 6
                else:
                    if overall <= 2.766:
                        if potential <= 2.134:
                            if age <= 1.791:
                                if overall <= 2.331:
                                    return 6
                                else:
                                    if age <= 1.025:
                                        return 7
                                    else:
                                        return 6
                            else:
                                if overall <= 2.259:
                                    if age <= 2.557:
                                        return 6
                                    else:
                                        return 9
                                else:
                                    return 8
                        else:
                            if overall <= 2.331:
                                if potential <= 2.298:
                                    return 6
                                else:
                                    return 7
                            else:
                                if potential <= 2.957:
                                    if potential <= 2.793:
                                        return 5
                                    else:
                                        return 6
                                else:
                                    if overall <= 2.621:
                                        return 4
                                    else:
                                        return 5
                    else:
                        if reputation <= 6.933:
                            if potential <= 2.793:
                                if reputation <= 4.857:
                                    return 2
                                else:
                                    if age <= 1.243:
                                        return 4
                                    else:
                                        return 2
                            else:
                                if skill <= 1.109:
                                    return 5
                                else:
                                    if overall <= 3.055:
                                        return 3
                                    else:
                                        return 4
                        else:
                            return 1
        def DF_expect(age, reputation, overall, potential, skill):
            age = (age - 25.61) / 4.47
            reputation = (reputation - 1.12) / 0.4
            overall = (overall - 67.33) / 6.4
            potential = (potential - 71.7) / 5.74
            skill = (skill - 2.34) / 0.45
            if overall <= 1.434:
                return 6
            else:
                if overall <= 2.06:
                    if potential <= 1.184:
                        if skill <= 2.819:
                            return 6
                        else:
                            if age <= 0.758:
                                return 6
                            else:
                                if reputation <= 0.954:
                                    return 3
                                else:
                                    return 6
                    else:
                        if potential <= 1.881:
                            if overall <= 1.59:
                                return 6
                            else:
                                if age <= 0.646:
                                    return 3
                                else:
                                    return 6
                        else:
                            return 3
                else:
                    if potential <= 2.404:
                        if age <= 1.542:
                            if reputation <= 3.466:
                                if overall <= 2.372:
                                    return 3
                                else:
                                    return 4
                            else:
                                if overall <= 2.529:
                                    return 4
                                else:
                                    return 4
                        else:
                            if overall <= 2.216:
                                return 6
                            else:
                                if reputation <= 5.978:
                                    return 4
                                else:
                                    return 6
                    else:
                        if overall <= 2.841:
                            if overall <= 2.529:
                                return 4
                            else:
                                if overall <= 2.685:
                                    return 2
                                else:
                                    return 4
                        else:
                            if skill <= 0.591:
                                if age <= 1.542:
                                    return 1
                                else:
                                    return 1
                            else:
                                if age <= 0.982:
                                    return 2
                                else:
                                    return 1
        def GK_expect(age, reputation, overall, potential, skill):
            age = (age - 25.24) / 4.63
            reputation = (reputation - 1.13) / 0.43
            overall = (overall - 67.17) / 6.86
            potential = (potential - 72.03) / 6.03
            skill = (skill - 2.40) / 0.78
            if overall <= 1.305:
                if overall <= 0.921:
                    return 5
                else:
                    if potential <= 1.073:
                        if potential <= 0.917:
                            return 5
                        else:
                            if age <= 0.278:
                                return 5
                            else:
                                return 4
                    else:
                        if overall <= 1.049:
                            if potential <= 1.851:
                                return 5
                            else:
                                return 4
                        else:
                            if potential <= 1.384:
                                return 4
                            else:
                                return 4
            else:
                if overall <= 1.945:
                    if potential <= 1.384:
                        if potential <= 1.073:
                            if age <= 0.639:
                                return 4
                            else:
                                return 4
                        else:
                            if age <= 0.819:
                                return 4
                            else:
                                return 4
                    else:
                        if overall <= 1.689:
                            if potential <= 2.007:
                                return 4
                            else:
                                return 3
                        else:
                            if age <= 2.08:
                                return 3
                            else:
                                return 5
                else:
                    if potential <= 2.63:
                        if potential <= 2.007:
                            if potential <= 1.851:
                                return 3
                            else:
                                return 2
                        else:
                            if overall <= 2.329:
                                return 6
                            else:
                                return 1
                    else:
                        if age <= 1.9:
                            return 1
                        else:
                            return 5
        def MF_expect(age, reputation, overall, potential, skill):
            age = (age - 24.92) / 4.63
            reputation = (reputation - 1.13) / 0.43
            overall = (overall - 67.15) / 6.85
            potential = (potential - 72.02) / 6.02
            skill = (skill - 2.40) / 0.78
            if overall <= 0.88:
                if overall <= 0.589:
                    return 9
                else:
                    if potential <= 0.502:
                        return 9
                    else:
                        if potential <= 1.493:
                            if overall <= 0.735:
                                return 9
                            else:
                                if age <= -0.767:
                                    return 9
                                else:
                                    return 9
                        else:
                            if potential <= 1.658:
                                return 7
                            else:
                                if potential <= 1.989:
                                    return 7
                                else:
                                    return 7
            else:
                if overall <= 1.463:
                    if overall <= 1.172:
                        if age <= 1.253:
                            if potential <= 1.824:
                                if skill <= -0.428:
                                    return 9
                                else:
                                    return 7
                            else:
                                if overall <= 1.026:
                                    return 7
                                else:
                                    return 8
                        else:
                            if overall <= 1.026:
                                return 9
                            else:
                                if age <= 1.701:
                                    return 9
                                else:
                                    return 9
                    else:
                        if potential <= 0.833:
                            if age <= 1.701:
                                if age <= 1.477:
                                    return 7
                                else:
                                    return 7
                            else:
                                if skill <= -0.428:
                                    return 9
                                else:
                                    return 9
                        else:
                            if potential <= 1.163:
                                if potential <= 0.998:
                                    return 8
                                else:
                                    return 7
                            else:
                                if potential <= 1.989:
                                    return 8
                                else:
                                    return 7
                else:
                    if overall <= 2.046:
                        if overall <= 1.755:
                            if potential <= 1.163:
                                if age <= 1.028:
                                    return 8
                                else:
                                    return 7
                            else:
                                if overall <= 1.609:
                                    return 8
                                else:
                                    return 8
                        else:
                            if potential <= 1.824:
                                if age <= 1.477:
                                    return 5
                                else:
                                    return 8
                            else:
                                if potential <= 2.154:
                                    return 3
                                else:
                                    return 3
                    else:
                        if overall <= 2.629:
                            if potential <= 1.824:
                                if age <= 1.253:
                                    return 3
                                else:
                                    return 4
                            else:
                                if age <= 1.701:
                                    return 4
                                else:
                                    return 5
                        else:
                            if age <= 1.701:
                                return 1
                            else:
                                return 5

        if position == 1:
            position = 'ST'
            result = ST_expect(age,reputation,overall,potential,skill)
            lab10.config(text='Result => ST_class:' + str(result))
            lab10.pack(side="right")

            if result == 9:
                result = random.randrange(0,10000000,1000000)
            elif result == 8:
                result = random.randrange(10000000, 20000000, 1000000)
            elif result == 7:
                result = random.randrange(20000000, 30000000, 1000000)
            elif result == 6:
                result = random.randrange(30000000, 40000000, 1000000)
            elif result == 5:
                result = random.randrange(40000000, 50000000, 1000000)
            elif result == 4:
                result = random.randrange(50000000, 60000000, 1000000)
            elif result == 3:
                result = random.randrange(60000000, 70000000, 1000000)
            elif result == 2:
                result = random.randrange(70000000, 80000000, 1000000)
            elif result == 1:
                result = random.randrange(80000000, 130000000, 1000000)
        elif position == 2:
            position = 'MF'
            result = MF_expect(age, reputation, overall, potential, skill)
            lab10.config(text='Result => MF_class:' + str(result))
            lab10.pack(side="right")

            if result == 9:
                result = random.randrange(0, 5000000, 1000000)
            elif result == 8:
                result = random.randrange(5000000, 10000000, 1000000)
            elif result == 7:
                result = random.randrange(10000000, 15000000, 1000000)
            elif result == 6:
                result = random.randrange(15000000, 20000000, 1000000)
            elif result == 5:
                result = random.randrange(20000000, 25000000, 1000000)
            elif result == 4:
                result = random.randrange(25000000, 30000000, 1000000)
            elif result == 3:
                result = random.randrange(30000000, 35000000, 1000000)
            elif result == 2:
                result = random.randrange(35000000, 40000000, 1000000)
            elif result == 1:
                result = random.randrange(40000000, 130000000, 1000000)
        elif position == 3:
            position = 'DF'
            result = DF_expect(age, reputation, overall, potential, skill)
            lab10.config(text='Result => DF_class:' + str(result))
            lab10.pack(side="right")

            if result == 7:
                result = random.randrange(0, 10000000, 1000000)
            elif result == 6:
                result = random.randrange(10000000, 20000000, 1000000)
            elif result == 5:
                result = random.randrange(10000000, 20000000, 1000000)
            elif result == 4:
                result = random.randrange(20000000, 30000000, 1000000)
            elif result == 3:
                result = random.randrange(30000000, 40000000, 1000000)
            elif result == 2:
                result = random.randrange(40000000, 50000000, 1000000)
            elif result == 1:
                result = random.randrange(50000000, 130000000, 1000000)
        elif position == 4:
            position = 'GK'
            result = GK_expect(age, reputation, overall, potential, skill)
            lab10.config(text='Result => GK_class:' + str(result))
            lab10.pack(side="right")
            if result == 6:
                result = random.randrange(0, 5000000, 1000000)
            elif result == 5:
                result = random.randrange(5000000, 10000000, 1000000)
            elif result == 4:
                result = random.randrange(10000000, 15000000, 1000000)
            elif result == 3:
                result = random.randrange(15000000, 20000000, 1000000)
            elif result == 2:
                result = random.randrange(20000000, 25000000, 1000000)
            elif result == 1:
                result = random.randrange(25000000, 30000000, 1000000)
        else:
            print('You enter wrongly. Please enter rightly position number.')

        conn = pymysql.connect(host="210.117.165.86", user='dbuser09', password='dbuser2021', db='dbuser09_schema',
                               port=3306, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        curs = conn.cursor()
        sql = "insert into soccer_player(name, age, continent, position,prefer_foot,reputation,stat_overall,stat_potential,stat_skill_moves,value)" \
              "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        curs.execute(sql,(name, age, continent, position, foot, reputation, overall, potential, skill, result))
        conn.commit()
        conn.close()


    btn = Button(win)
    btn.config(text = "Expect")
    btn.config(command = Value_expect)
    btn.pack(side="left")

    win.mainloop()

# GK_DCT(data)
# ST_DCT(data)
# MF_DCT(data)
# DF_DCT(data)

GUI()