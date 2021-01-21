import numpy as np
def det (num_serie,presion_old,temperatura_old,humedad_old,presion_new,temperatura_new,humedad_new,temperatura_cont,humedad_cont):
    
    umbral_pres = 0.3
    umbral_temp = 2.2
    umbral_hum = 5
    umbral_sis = 0.2
    anormal = 0

    #convertir vector de presion actual a matriz de 7x20
    if int(num_serie[2]) % 2 != 0:
        vacio = [0 ,4, 5, 6, 12, 13, 20, 27, 34, 56, 63, 70, 71, 77, 78, 84, 85, 91, 92, 98, 99, 105, 106, 112, 113, 119, 120, 126, 127, 132, 133, 134, 139]
    else:
         vacio = [0, 1, 2, 6, 7, 8, 14, 21, 28, 62, 69, 75, 76, 82, 83, 89, 90, 96, 97, 103, 104, 110, 111, 117, 118, 124, 125, 126, 131, 132, 133, 138, 139]
    
    k = 0
    presion = np.zeros((140,1))
    for i in range (len(presion)):
        if i in vacio:
            presion[i] = 0
        else:
            presion[i] = presion_new[k]
            k = k + 1

    presion = np.reshape(presion,(20,7))

    #convertir vector de presion pasada a matriz de 7x20
    if int(num_serie[2]) % 2 != 0:
            vacio = [0 ,4, 5, 6, 12, 13, 20, 27, 34, 56, 63, 70, 71, 77, 78, 84, 85, 91, 92, 98, 99, 105, 106, 112, 113, 119, 120, 126, 127, 132, 133, 134, 139]
    else:
            vacio = [0, 1, 2, 6, 7, 8, 14, 21, 28, 62, 69, 75, 76, 82, 83, 89, 90, 96, 97, 103, 104, 110, 111, 117, 118, 124, 125, 126, 131, 132, 133, 138, 139]
        
    k = 0
    presionold = np.zeros((140,1))
    for i in range (140):
        if i in vacio:
            presionold[i] = 0
        else:
            presionold[i] = presion_old[k]
            k = k + 1

    presionold = np.reshape(presionold,(20,7))

    # Verificar valores dentro de los rangos "sanos"
    suma_pres = 0
    promedio = 0
    for i in range (np.size(presion_new)):
        #verificar pisada completa
        suma_pres = presion_new[i] + suma_pres
    promedio = suma_pres/(np.size(presion_new))
    umbral_pres = (umbral_pres / promedio) * 0.63
    if promedio<umbral_sis:
        #print(promedio)
        caso = 27
        anormal = 1
        return(caso, anormal)
        # verificar presion en rango normal mayor a 0 y menor a 10 kgf
    for i in range(np.size(presion)):    
        if (presion[ i%np.size(presion,0), i//np.size(presion,0) ]>10):
            caso = 28
            anormal = 1
            return(caso, anormal)
    # verificar temperatura en rango normal entre 27 y 34.5°C
    for i in range(len(temperatura_new)):
        if (temperatura_new[i]>34.5 or temperatura_new[i]<18):
            caso = 28
            anormal = 1
            return(caso, anormal)
    # verificar humedad en rango optimo entre 40 y 60%
    for i in range(len(humedad_new)):
        if (humedad_new[i]> 90 or  humedad_new[i]<40):
            caso = 28
            anormal = 1
            return(caso, anormal)

    #Analisis de sistema de presion
    caso = 0
    if promedio >= umbral_sis:
        indicadorpres = 0
        signopres = []
        sens_pres = []
        for i in range(np.size(presion)):
            psc=i//np.size(presion,0)
            psf=i%np.size(presion,0)
            vecindad = 0
            cont_pres = 0
            #comparar valor contra momento anterior
            if abs(presion[psf,psc]-presionold[psf, psc])>=umbral_pres:
                # Se obtiene el promedio de la vecindad para registrar el cambio promedio
                for j in range(9):
                    if psf == 0:
                        if psc == 0:
                            if (j == 5 or j == 7 or j == 8):
                                vecindad = vecindad + presion[psf-1+j//3,psc-1+j%3]
                        elif psc == 6:
                            if (j == 3 or j == 6 or j == 7):
                                vecindad = vecindad + presion[psf-1+j//3,psc-1+j%3]
                        else:
                            if (j!=0 and j!=1 and j!=2):
                                vecindad = vecindad + presion[psf-1+j//3,psc-1+j%3]
                    elif psf == 19:
                        if psc == 0:
                            if (j == 1 or j == 2 or j == 5):
                                vecindad = vecindad + presion[psf-1+j//3,psc-1+j%3]
                        elif psc == 6:
                            if (j == 0 or j == 1 or j == 3):
                                vecindad = vecindad + presion[psf-1+j//3,psc-1+j%3]
                        else:
                            if (j!=6 and j!=7 and j!=8):
                                vecindad = vecindad + presion[psf-1+j//3,psc-1+j%3]
                    else:
                        if psc == 0:
                            if (j!=0 and j!=3 and j!=6):
                                vecindad = vecindad + presion[psf-1+j//3,psc-1+j%3]
                        elif psc == 6:
                            if (j!=2 and j!=5 and j!=8):
                                vecindad = vecindad + presion[psf-1+j//3,psc-1+j%3]
                        else:
                            vecindad = vecindad + presion[psf-1+j//3,psc-1+j%3]
            
                vecindad = (vecindad-presion[psf,psc])/8
                cambio = abs(vecindad-presion[psf,psc])
                # comparar cambio contra cada punto de la vecindad, si varia mucho el rango contra pocos puntos de
                # sensado se considera como un espacio de riesgo
                for j in range(9):
                    if psf == 0:
                        if psc == 0:
                            if (j == 5 or j == 7 or j == 8):
                                if (presion[psf-1+j//3,psc-1+j%3]>cambio):
                                    cont_pres = 1 + cont_pres
                        elif psc == 6:
                            if (j == 3 or j == 6 or j == 7):
                                if (presion[psf-1+j//3,psc-1+j%3]>cambio):
                                    cont_pres = 1 + cont_pres
                        else:
                            if (j!=0 and j!=1 and j!=2):
                                if (presion[psf-1+j//3,psc-1+j%3]>cambio):
                                    cont_pres = 1 + cont_pres
                    elif psf == 19:
                        if psc == 0:
                            if (j == 1 or j == 2 or j == 5):
                                if (presion[psf-1+j//3,psc-1+j%3]>cambio):
                                    cont_pres = 1 + cont_pres
                        elif psc == 6:
                            if (j == 0 or j == 1 or j == 3):
                                if (presion[psf-1+j//3,psc-1+j%3]>cambio):
                                    cont_pres = 1 + cont_pres
                        else:
                            if (j!=6 and j!=7 and j!=8):
                                if (presion[psf-1+j//3,psc-1+j%3]>cambio):
                                    cont_pres = 1 + cont_pres
                    else:
                        if psc == 0:
                            if (j!=0 and j!=3 and j!=6):
                                if (presion[psf-1+j//3,psc-1+j%3]>cambio):
                                    cont_pres = 1 + cont_pres
                        elif psc == 6:
                            if (j!=2 and j!=5 and j!=8):
                                if (presion[psf-1+j//3,psc-1+j%3]>cambio):
                                    cont_pres = 1 + cont_pres
                        else:
                            if (presion[psf-1+j//3,psc-1+j%3]>cambio):
                                cont_pres = 1 + cont_pres
            #si existen muchos puntos de sensado con cambio entonces se ignora                   
            if (cont_pres>0 and cont_pres<6):
                indicadorpres = 1
                sens_pres.append(i)
                signopres.append(presion[psf,psc]-presionold[psf,psc])

                
        #Analisis del sistema de temperatura
        cont_temp = 0
        sens_temp = []
        indicadortemp = 0
        signotemp = []
        for i in range(len(temperatura_new)):
            #por cada sensor de temperatura se compara con el momento anterior
            if abs(temperatura_new[i]-temperatura_old[i])>=umbral_temp:
                #al registrar un cambio de 2.2, se compara contra los sensores más próximos
                if i == 0: 
                    ct= abs(temperatura_new[i] - temperatura_new[i+1])
                    if ct >= umbral_temp:
                        ctc= abs(temperatura_cont[i] - temperatura_new[i])
                        if ctc >= umbral_temp:
                            indicadortemp = 1
                            cont_temp = cont_temp + 1
                            sens_temp.append(i)
                            signotemp.append(temperatura_new[i]-temperatura_old[i])
                elif i == 6:
                    ct= abs(temperatura_new[i] - temperatura_new[i-1])
                    if ct >= umbral_temp:
                        ctc = abs(temperatura_cont[i] - temperatura_new[i])
                        if ctc >= umbral_temp:
                            indicadortemp = 1
                            cont_temp = cont_temp + 1
                            sens_temp.append(i)
                            signotemp.append(temperatura_new[i]-temperatura_old[i])
                else:
                    ct1 = abs(temperatura_new[i] - temperatura_new[i+1])
                    ct2 = abs(temperatura_new[i] - temperatura_new[i-1])
                    ct = ct1 + ct2 / 2 
                    if ct >= umbral_temp:
                #comparar sensor contra sensor contralateral
                        ctc= abs(temperatura_cont[i] - temperatura_new[i])
                        if ctc >= umbral_temp:
                            indicadortemp = 1
                            cont_temp = cont_temp + 1
                            sens_temp.append(i)
                            signotemp.append(temperatura_new[i]-temperatura_old[i])
        #si muchos sensores registran cambio entonces se ignoran los cambios              
        if cont_temp>2:
            sens_temp = []
            indicadortemp = 0
            signotemp = []
            
        #analisis de los sensores de humedad    
        indicadorhum = 0
        cont_hum = 0
        sens_hum = []
        signohum = []
        # se comparan los sensores de humedad contra un momento previo
        for i in range(len(humedad_new)):
            if abs(humedad_new[i]-humedad_old[i])>=umbral_hum:
                # si existe cambio de 5 entonces se compara contra el otro sensor
                if i == 0: 
                    ch = abs(humedad_new[i] - humedad_new[i+1])
                    if ch >= umbral_hum:
                #si el valor es constante en el pie se compara contra pie contralateral       
                        sch = abs(humedad_cont[i]-humedad_new[i])
                        if sch >= umbral_hum:
                            indicadorhum = 1
                            cont_hum = cont_hum + 1
                            sens_hum.append(i)
                            signohum.append(humedad_new[i]-humedad_old[i])
                            
                
        # inicio de evaluacion de riesgo usando los indicadores pres,temp y hum, así como sus signos
        #obtenemos un promedio de los cambios registrados para indicar si fue cambio incremental o decremental
        psigpr = 0
        if len(signopres)> 1:
            for i in range(len(signopres)):
                psigpr = psigpr + signopres[i]
                psigpr = psigpr/len(signopres)
        elif np.size(signopres) == 1:
            psigpr = signopres[0]
        else:
            psigpr = 0

        psigtm = 0
        if len(signotemp)>1:
            for i in range(len(signotemp)):
                psigtm = psigtm + signotemp[i]
                psigtm = psigtm/len(signotemp)
        elif np.size(signotemp) == 1:
            psigtm = signotemp[0]

        if len(signohum) != 0:
             signohum = signohum[0]
        
        # Condicionales de riesgo combinaciones
        if indicadorpres == 1 :
            if psigpr > 0:
                if indicadortemp == 1:
                    if psigtm > 0:
                        if indicadorhum == 1:
                            if signohum > 0:
                                caso = 1
                            elif signohum < 0:
                                caso = 2
                        if indicadorhum == 0:
                                caso = 3
                    if psigtm < 0:
                        if indicadorhum == 1:
                            if signohum > 0:
                                caso = 4
                            elif signohum < 0:
                                caso = 5
                        if indicadorhum == 0:
                            caso = 6
                            
                if indicadortemp == 0:
                    if indicadorhum == 1:
                        if signohum > 0:
                            caso = 27
                        elif signohum < 0:
                            caso = 8
                    if indicadorhum == 0:
                        caso = 9
                        
            if psigpr < 0:
                if indicadortemp == 1:
                    if psigtm > 0:
                        if indicadorhum == 1:
                            if signohum > 0:
                                caso = 27
                            elif signohum < 0:
                                caso = 11
                        if indicadorhum == 0:
                                caso = 27
                    if psigtm < 0:
                        if indicadorhum == 1:
                            if signohum > 0:
                                caso = 13
                            elif signohum < 0:
                                caso = 27
                        if indicadorhum == 0:
                            caso = 27
                            
                if indicadortemp == 0:
                    if indicadorhum == 1:
                        if signohum > 0:
                            caso = 27
                        elif signohum < 0:
                            caso = 27
                    if indicadorhum == 0:
                        caso = 27
                        
        elif indicadorpres == 0 :
            if indicadortemp == 1:
                if psigtm > 0:
                    if indicadorhum == 1:
                        if signohum > 0:
                            caso = 27
                        elif signohum < 0:
                            caso = 20
                    if indicadorhum == 0:
                        caso = 21
                        
                if psigtm < 0:
                    if indicadorhum == 1:
                        if signohum > 0:
                            caso = 22
                        elif signohum < 0:
                            caso = 27
                    if indicadorhum == 0:
                        caso = 24
                        
            if indicadortemp == 0:
                if indicadorhum == 1:
                    if signohum > 0:
                        caso = 25
                    elif signohum < 0:
                        caso = 26
                else: 
                    caso = 27
    return(caso, anormal)