
from math import *
from random import *
import Reza
import numpy
import random
import math
import sys
import xlsxwriter
import pandas as pd
import itertools



def Harmony_search(input_name ,model_type=None ,method=None , HMCR=None, PAR=None ,pitch=None, 
                    loss_type=None, it_1=None , it_2=None ,it_3=None ,it_4=None ,it_5 = None,
                    Maximum_HMS=None, Initial_Search_limit =None ):
    

    Input = pd.read_excel(input_name)

    if it_1==None:  it_1 = 1000
    if it_2==None:  it_2 = 10
    if it_3==None:  it_3 = 10
    if it_4==None:  it_4 = 10
    if it_5==None:  it_5 = 10

    if Maximum_HMS==None:   Maximum_HMS = 10

    if HMCR==None:  HMCR = 0.8
    if PAR==None:   PAR  = 0.2

    if pitch==None: 
        δ =0.1
    else :
        δ =pitch
    
    if model_type==None:model_type = "a*x+b"
        
    if loss_type==None : loss_type = "RMSE"
    
    if model_type == "a*x+b" :
        number_of_parameter_type = 1
    elif model_type == "ax+bx^c+d" :
        number_of_parameter_type = 3
    elif model_type ==  "a*x+b*exp(x)+c":
        number_of_parameter_type = 2
    elif model_type == "a*x+b*x^2+c":
        number_of_parameter_type = 2
    elif model_type == "a*x+b*x^3+c":
        number_of_parameter_type = 2
    
    if method == None  : method = "Orginal"
    if Initial_Search_limit==None : Initial_Search_limit=(-2,2)
    
    infinity = 99999999999999999999
    
    def EXP(List):
        EL = []
        for a in List:
            EL.append(exp(a))
        EL = numpy.array(EL)
        return EL

    def _Model_F(V, Coef , M_Type,Constant):
        V= numpy.array(V)
        Coef =numpy.array(Coef)
        if M_Type=="a*x+b":
            Modeled = numpy.zeros(len(V[0]))
            for jj in range(len(V)) :
                Modeled= Modeled + numpy.array(V[jj])*Coef[0][jj]
            Modeled = Modeled + Constant
        
        elif M_Type=="a*x+b*x^c+d":
            Modeled = numpy.zeros(len(V[0]))
            for jj in range(len(V)) :
                arr = numpy.array(V[jj])
                arr_2 = arr**int(Coef[2,jj])
                Modeled= Modeled + arr*Coef[0,jj]+Coef[1,jj]*arr_2
            Modeled = Modeled + Constant
        elif M_Type== "a*x+b*exp(x)+c" :
            Modeled = numpy.zeros(len(V[0]))
            for jj in range(len(V)) :
                Modeled= Modeled + numpy.array(V[jj])*Coef[0][jj]+Coef[1][jj]*EXP( V[jj] )
            Modeled = Modeled + Constant
        elif M_Type=="a*x+b*x^2+c":
            Modeled = numpy.zeros(len(V[0]))
            for jj in range(len(V)) :
                arr = numpy.array(V[jj])
                arr_2 = arr**2
                Modeled= Modeled + arr*Coef[0,jj]+Coef[1,jj]*arr_2
            Modeled = Modeled + Constant
        elif M_Type=="a*x+b*x^3+c":
            Modeled = numpy.zeros(len(V[0]))
            for jj in range(len(V)) :
                arr = numpy.array(V[jj])
                arr_2 = arr**3
                Modeled= Modeled + arr*Coef[0,jj]+Coef[1,jj]*arr_2
            Modeled = Modeled + Constant
        return list(Modeled)

    def Sort_F(Harmony_Memory,size)   :   
        Sorted=[]
        for i in range(size):
            Sorted.append(Harmony_Memory[len(Harmony_Memory)-i-1])
        return Sorted



    def Loss_func(Obs,Model,loss_type):
        if loss_type =='RMSE':
            Li= (numpy.array(Model)-numpy.array(Obs))**2
            loss_result = (sum(list(Li))/float(len(Li)))**0.5
        elif loss_type=='RMSE-exp(CSI)':
            Li= (numpy.array(Model)-numpy.array(Obs))**2
            loss_result = (sum(list(Li))/float(len(Li)))**0.5-exp(Reza.CSI(Obs,Model))
        elif loss_type == "MSE":
            Li= (numpy.array(Model)-numpy.array(Obs))**2
            loss_result = (sum(list(Li))/float(len(Li)))
        elif loss_type == "SE" :
            Li= (numpy.array(Model)-numpy.array(Obs))**2
            loss_result = sum(list(Li))
        elif loss_type == "MB":
            Li= (numpy.array(Model)-numpy.array(Obs))**2
            loss_result = sum(list(Li))/float(len(Li))
        return loss_result

    Keys = list(pd.DataFrame.keys(Input))

    Obs = list(Input[Keys[0]])
    Obs = Reza.Float(Obs)
    variables = Keys
    variables.pop(0)


    

    Predictors = [ ]
    for pre in variables:
        Predictors.append(Reza.Float(list(Input[pre])))

    Means=[]
    stdv=[]

    for i in range(len(Predictors)):
        μ=sum(Predictors[i])/len(Predictors[i])
        σ=numpy.std(Predictors[i])
        Means.append(μ)
        stdv.append(σ)
        if method == "Standard" :
            Predictors[i]=(numpy.array(Predictors[i])-μ)/σ
        if method == "Orginal":
            Predictors[i]=numpy.array(Predictors[i])



    Predictors=numpy.array(Predictors)

    print("Means=" , Means)
    print("stdv=" , stdv)

    Loss_opt=1000
    Loss_list= [ ]
    Memory = []
    list_bias = []
    criteria = "Unsatisfied"
    #for kk in range(it_1):
    numerator =0
    
    num =0
    while criteria == "Unsatisfied":
        num+=1
        import xlsxwriter
        workbook = xlsxwriter.Workbook(input_name+"_"+"Improvisation.xlsx")
        numerator +=1
        print('New Harmony creation')
        for k in range(it_2):
            print(k,end="\r")
            Cof= list(numpy.zeros((number_of_parameter_type, (len(Predictors)))))
            for i in range(number_of_parameter_type):
                for j in range(len(Predictors)):
                    rr = randint(Initial_Search_limit[0]*10000, Initial_Search_limit[1]*10000)/10000.0
                    Cof[i][j]= rr
            bb=  randint(Initial_Search_limit[0]*10000, Initial_Search_limit[1]*10000)/10000.0
            Model=[]
            Model = _Model_F(V= Predictors , Coef= Cof ,  M_Type=model_type , Constant=bb)
            try:
                loss = Loss_func(Obs,Model,loss_type)
            except:
                loss = infinity
            if loss < Loss_opt:
                print("loss :"  , loss )
                print([list(Cof),bb])
                Loss_opt = loss
                Memory.append( list(Cof) )
                list_bias.append(bb)
                Loss_list.append(loss)

        it_2=1
        Memory = Sort_F(Memory, size=min(Maximum_HMS,len(Memory)))
        list_bias= Sort_F(list_bias,size=min(Maximum_HMS,len(Memory)))

        print("\n---------Improvisation---------\n")
        
        
        N_mem= int(len(Memory))
        
        for I in range(len(Memory)):
            Cof= list(numpy.zeros((number_of_parameter_type, (len(Predictors)))))
            for row in range(number_of_parameter_type):
                for col in range( len(Predictors) ):
                    Cof[row][col]=Memory[I][row][col]
            bb = list_bias[I]
            print("I = " , I)
            try:
                del(short_term_memory)
            except :
                pass 
            
            for i in range(number_of_parameter_type):
                for j in range(len(Predictors)):
                    GR=False
                    ITT=-1
                    ran_1 = random.random()
                    while ITT < it_3:
                        ITT+=1
                        try:
                            Cof =short_term_memory[0]
                            bb = short_term_memory[1]
                        except :
                            pass 
                        
                        if ran_1 < HMCR :

                            vector = []
                            for i_hs in range(N_mem): vector.append(Memory[I][i][j])
                            rr = random.choice(vector)
                            ran_2 = random.random()
                            Cof[i][j] = rr
                            if ran_2<PAR :
                                if GR==False:
                                    grad = random.choice([-1,1])*δ
                                rr = Cof[i][j] + random.random()*grad
                                Cof[i][j] = rr
                        else:
                            rr = randint(Initial_Search_limit[0]*10000, Initial_Search_limit[1]*10000)/10000.0
                            Cof[i][j] = rr
                        
                        Model = _Model_F(V= Predictors , Coef= Cof ,  M_Type=model_type , Constant=bb)
                            # Li= (numpy.array(Model)-numpy.array(Obs))**2
                            # loss= (sum(list(Li))/float(len(Li)))**0.5
                        try:
                            loss = Loss_func(Obs,Model,loss_type)
                        except:
                            loss = infinity
                        if loss < Loss_opt:
                            if ran_2<PAR and ran_1<HMCR :
                                GR = True
                            print("loss :"  , loss )
                            print( Cof,bb )
                            Loss_opt = loss
                            num = num+1
                            worksheet = workbook.add_worksheet(str(num))
                            for col in range( len(Predictors) ):
                                    worksheet.write( 0 , col, variables[col])
                            for row in range(number_of_parameter_type):
                                for col in range( len(Predictors) ):
                                    worksheet.write( row+1 , col, Cof[row][col])
                            worksheet.write(number_of_parameter_type+1 , len(Predictors)-1, bb )
                            Loss_list.append(loss)
                            short_term_memory =(Cof ,bb)
                            ITT=0

                        
                        if loss >= Loss_opt:
                            GR=False
                            try:
                                Cof = short_term_memory[0]
                                bb  = short_term_memory[1]
                            except : 
                                Cof= list(numpy.zeros((number_of_parameter_type, (len(Predictors)))))
                                for row in range(number_of_parameter_type):
                                    for col in range( len(Predictors) ):
                                        Cof[row][col]=Memory[I][row][col]
            ITT=-1
            GR=False
            ran_1 = random.random()
            while ITT < it_3:
                ITT+=1
                try:
                    Cof = short_term_memory[0]
                    bb=short_term_memory[1]
                except :
                    pass
                if ran_1 < HMCR :
                    vector = []
                    for i_hs in range(N_mem): vector.append(Memory[I][-1][-1])
                    vector = list(vector for vector,_ in itertools.groupby(vector))
                    bb = random.choice(vector)
                    ran_2 = random.random()
                    if ran_2<PAR :
                        if GR==False:
                            grad = random.choice([-1,1])*δ
                        bb = bb + random.random()*grad
                else:
                    bb = random.randint(Initial_Search_limit[0]*10000,Initial_Search_limit[1]*10000)/10000.0
                Model = _Model_F(V= Predictors , Coef= Cof ,  M_Type=model_type , Constant=bb)
                try:
                    loss = Loss_func(Obs,Model,loss_type)
                except:
                    loss = infinity
                if loss < Loss_opt:
                    if ran_2<PAR and ran_1<HMCR :
                        GR = True
                    print("loss :"  , loss )
                    print( Cof ,bb)
                    Loss_opt = loss
                    short_term_memory =(Cof ,bb)
                    num+=1
                    worksheet = workbook.add_worksheet(str(num))
                    for col in range( len(Predictors) ):
                        worksheet.write( 0 , col, variables[col])
                    for row in range(number_of_parameter_type):
                        for col in range( len(Predictors) ):
                            worksheet.write( row+1 , col, Cof[row][col])
                    worksheet.write(number_of_parameter_type+1 , len(Predictors)-1, bb )
                    Loss_list.append(loss)
                    ITT=0
                if loss >= Loss_opt:
                    GR=False
                    try:
                        Cof = short_term_memory[0]
                        bb  = short_term_memory[1]
                    except : 
                        Cof= list(numpy.zeros((number_of_parameter_type+1, (len(Predictors)))))
                        for row in range(number_of_parameter_type):
                            for col in range( len(Predictors) ):
                                Cof[row][col]=Memory[I][row][col]
        workbook.close()
        if numerator == it_1: criteria="Satisfied" 
        HMCR_excel = Reza.Matread_all_Sheets(input_name+"_"+"Improvisation.xlsx")
        list_bias = []
        for ii in range(num,0,-1) :
            try:
                list_bias.append(float(HMCR_excel[ii-1][-1][-1]))
            except:
                pass
        Memory = []
        for ii in range(num,0,-1):
            ans=[]
            for row in range(number_of_parameter_type):
                try:
                    ans.append(Reza.Float(HMCR_excel[ii-1][row]))
                except:
                    pass
            Memory.append(ans)


    HMCR_excel = Reza.Matread_all_Sheets(input_name+"_"+"Improvisation.xlsx")
    list_bias = []
    for ii in range(num,0,-1) :
        try:
            list_bias.append(float(HMCR_excel[ii-1][-1][-1]))
        except:
            pass
    Memory = []
    for ii in range(num,0,-1):
        ans=[]
        for row in range(number_of_parameter_type):
            try:
                ans.append(Reza.Float(HMCR_excel[ii-1][row]))
            except:
                pass
    Memory.append(ans)
    print( "Cof = " , Memory[0])

    txt_file = open(input_name+"_"+method+"HS.txt" , "w")

    txt_file.write("model_type : ") 
    txt_file.write(model_type) 
    txt_file.write("\nmethod :")
    txt_file.write(method)
    txt_file.write("\nHMCR :")
    txt_file.write(str(HMCR))
    txt_file.write("\nPAR :")
    txt_file.write(str(PAR))
    txt_file.write("\npitch :")
    txt_file.write(str(pitch))
    txt_file.write("\nloss_type :")
    txt_file.write(loss_type)
    txt_file.write("\nvariables : ")
    txt_file.write(str(variables))
    txt_file.write("\nCof=")
    txt_file.write(str(list(Memory[0])))
    txt_file.write("\nbias=")
    txt_file.write(str(list_bias[0]))
    txt_file.write("\nMeans=")
    txt_file.write(str(Means))
    txt_file.write("\nstdv=")
    txt_file.write(str(stdv))
    txt_file.close()

    import xlsxwriter

    workbook = xlsxwriter.Workbook(input_name+"_"+"loss_list.xlsx")
    worksheet = workbook.add_worksheet()
    for i in range(len(Loss_list)):
        worksheet.write( i , 0, Loss_list[i])
    workbook.close()





