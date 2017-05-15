#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Funcions que permeten crear trames (en format bytearray) 

ASDUS:
- ASDU 190: permet llegir curva carga (kW) (registre 11) en bloc
- ASDU 123: permet llegir curva carga (kW) (registre 11)
- ASDU 122: permet llegir acumulats (energia, kWh)
- ASDU 183: inici sessió
- ASDU 187: final sessió
- 162
- 123
- 122 
- 134

Els asdus es creen cadascun amb la seva funció i es posen dins les funcions:
- creaTramaFix: crea trames fixes (6 bytes)
- creaTramaVar: crea trames variables (n bytes)

Utilitats:
- creaTemps: crea etiquetes de temps (5 bytes)
'''
#add parent folder to path
import sys
sys.path.insert(0,"..") 

#punt mesura, direccio i password
import config
pm   = config.puntMesura # 2 bytes maxim
di   = config.direccio   # 2 bytes maxim
clau = config.password   # 4 bytes maxim

'''TIPUS ASDU implementats'''
def creaASDU162(direccio):
    '''
        A162: Read Instantaneous Values, obj inf=192,193,194
        la resposta és un A163
    '''
    asdu=[None]*7
    asdu[0]=162 #idt identificador de tipo
    asdu[1]=1   #qev: byte [SQ=0 (1 bit), N=1 (7 bits)] 00000001
    asdu[2]=5   #cdt: causa=petición (5)
    asdu[3]=(pm&0x00ff)    #punt mesura (2 bytes)
    asdu[4]=(pm&0xff00)>>8 #punt mesura (2 bytes)
    asdu[5]=0   #registre=0
    asdu[6]=direccio 
    '''
        direccio 192: Elem. Info.: Totalizadores de energías (Agrup: V / Dir. Obj.: 192)
        direccio 193: Elem. Info.: Potencias activas (Agrup: V / Dir. Obj.: 193)
        direccio 194: Contiene los valores instantáneos de las tensiones y corrientes, referidos a valores secundarios..
    '''
    return bytearray(asdu)

def creaASDU190(registre,objecte,data_inici,data_final):
    '''
        A190:"LEER BLOQUES DE TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE POR INTERVALO DE TIEMPO Y DIRECCIÓN",
        la resposta és un A140. És germà del A189

        Estructura:
            17-12           11        10-6         5-1
        +---------------+---------+------------+------------+
        | IUD (6 bytes) | objecte | data inici | data final |
        +---------------+---------+------------+------------+

        * registre = 11(curva carga) o 21(resumen diario)
        * objecte = (9,10,11)
        La dirección de objeto selecciona la obtención de:
        9: bloques de puntos de medida genéricos con reservas 
        10: bloques de puntos de medida genéricos sin reservas 
        11: bloques de puntos de medida de consumo sin reservas"

        data_inici = bytearray (tipus a)
        data_final = bytearray (tipus a)
    '''
    asdu=[None]*17
    asdu[0]=190 #idt identificador de tipo
    asdu[1]=1   #qev: byte [SQ=0 (1 bit), N=1 (7 bits)] 00000001
    asdu[2]=6   #cdt: causa=activación (6)
    asdu[3]=(pm&0x00ff)    #punt mesura (2 bytes)
    asdu[4]=(pm&0xff00)>>8 #punt mesura (2 bytes)
    asdu[5]=registre
    asdu[6]=objecte
    asdu[7:12]=data_inici
    asdu[12:17]=data_final
    return bytearray(asdu)

def creaASDU123(registre,integrat_inici,integrat_final,data_inici,data_final):
    '''
        A123:"LEER TOTALES INTEGRADOS OPERACIONALES REPUESTOS PERIÓDICAMENTE POR INTERVALO DE TIEMPO Y RANGO DE DIRECCIONES",

        registre = byte. 11:curva de carga, 21: resumen diario
        integrat_inici = byte. l'interessant es l'integrat 1.
        integrat_final = byte
        data_inici = bytearray
        data_final = bytearray

            18-13           12               11               10-6         5-1 
        +---------------+----------------+----------------+------------+------------+
        | IUD (6 bytes) | integrat inici | integrat final | data inici | data final |
        +---------------+----------------+----------------+------------+------------+
    '''
    asdu=[None]*18
    asdu[0]=123 #idt identificador de tipo
    asdu[1]=1   #qev: byte [SQ=0 (1 bit), N=1 (7 bits)] 00000001
    asdu[2]=6   #cdt: causa=activación (6)
    asdu[3]=(pm&0x00ff)    #punt mesura (2 bytes)
    asdu[4]=(pm&0xff00)>>8 #punt mesura (2 bytes)
    asdu[5]=registre #exemple:: 11: Totales integrados con período de integración 1 (curva de carga)
    asdu[6]=integrat_inici
    asdu[7]=integrat_final
    asdu[8:13]=data_inici
    asdu[13:18]=data_final
    return bytearray(asdu)

def creaASDU122(registre,integrat_inici,integrat_final,data_inici,data_final):
    '''
        122:"LEER TOTALES INTEGRADOS OPERACIONALES POR INTERVALO DE TIEMPO Y RANGO DE DIRECCIONES",

            18-13           12               11               10-6         5-1 
        +---------------+----------------+----------------+------------+------------+
        | IUD (6 bytes) | integrat inici | integrat final | data inici | data final |
        +---------------+----------------+----------------+------------+------------+

        integrat inici: byte (l'interessant és l'1)
        integrat final: byte
        data inici: etiqueta temps tipus a (5 bytes)
        data final: etiqueta temps tipus a (5 bytes)
    '''
    asdu=[None]*18
    asdu[0]=122 #idt identificador de tipo
    asdu[1]=1   #qev: byte [SQ=0 (1 bit), N=1 (7 bits)] 00000001
    asdu[2]=6   #cdt: causa=activación (6)
    asdu[3]=(pm&0x00ff)    #punt mesura (2 bytes)
    asdu[4]=(pm&0xff00)>>8 #punt mesura (2 bytes)
    asdu[5]=registre #exemple:: 11: Totales integrados con período de integración 1 (curva de carga)
    asdu[6]=integrat_inici
    asdu[7]=integrat_final
    asdu[8:13]=data_inici
    asdu[13:18]=data_final
    return bytearray(asdu)

def creaASDU134(data_inici,data_final):
    '''
        A134: LEER INFORMACIÓN DE TARIFICACIÓN (VALORES MEMORIZADOS)
        És una petició dels valors de la tarifa.  la resposta és un A136

            16 bytes
        +---------------+----------------------+----------------------+
        | IUD (6 bytes) | data inici (5 bytes) | data final (5 bytes) |
        +---------------+----------------------+----------------------+
        
        data inici i data final són etiquetes de temps tipus a (5 bytes)
    '''
    asdu=[None]*16
    asdu[0]=134 #idt identificador de tipo
    asdu[1]=1   #qev: byte [SQ=0 (1 bit), N=1 (7 bits)] 00000001
    asdu[2]=5   #cdt: causa=peticion o solicitada (5)
    asdu[3]=(pm&0x00ff)    #punt mesura (2 bytes)
    asdu[4]=(pm&0xff00)>>8 #punt mesura (2 bytes)
    asdu[5]=136 #direccio registre: 136: Información de Tarificación relativa al Contrato III
    asdu[6:11]=data_inici
    asdu[11:16]=data_final
    return bytearray(asdu)

def creaASDU183():
    '''
        A183: INICIAR SESIÓN Y ENVIAR CLAVE DE ACCESO
        És una petició

            10 bytes
        +---------------+----------------+
        | IUD (6 bytes) | clau (4 bytes) |
        +---------------+----------------+
    '''
    asdu=[None]*10
    asdu[0]=183 #idt identificador de tipo
    asdu[1]=1   #qev: byte [SQ=0 (1 bit), N=1 (7 bits)] 00000001
    asdu[2]=6   #cdt: causa=activación (6)
    asdu[3]=(pm&0x00ff)    #punt mesura (2 bytes)
    asdu[4]=(pm&0xff00)>>8 #punt mesura (2 bytes)
    asdu[5]=0 #direccio registre: 0: cap registre
    asdu[6]=(clau & 0x000000ff)
    asdu[7]=(clau & 0x0000ff00)>>8
    asdu[8]=(clau & 0x00ff0000)>>16
    asdu[9]=(clau & 0xff000000)>>24
    return bytearray(asdu)

def creaASDU187():
    '''
        A187: Finalitzar sessió (request)
        ASDU buit, només té el camp IUD (6 bytes)
    '''
    asdu=[None]*6
    asdu[0]=187 #idt identificador de tipo
    asdu[1]=0   #qev: byte [SQ=0 (1 bit), N=0 (7 bits)]
    asdu[2]=5   #cdt: causa=peticion (5)
    asdu[3]=(pm&0x00ff)    #punt mesura (2 bytes)
    asdu[4]=(pm&0xff00)>>8 #punt mesura (2 bytes)
    asdu[5]=0 #direccio registre: 0: cap registre
    return bytearray(asdu)

def creaASDU103():
    '''
        A103: Llegeix l'hora de l'equip
        ASDU buit, només té el camp IUD (6 bytes)
    '''
    asdu=[None]*6
    asdu[0]=103 #idt identificador de tipo
    asdu[1]=0   #qev: byte [SQ=0 (1 bit), N=0 (7 bits)]
    asdu[2]=5   #cdt: causa=peticion (5)
    asdu[3]=(pm&0x00ff)    #punt mesura (2 bytes)
    asdu[4]=(pm&0xff00)>>8 #punt mesura (2 bytes)
    asdu[5]=0 #direccio registre: 0: cap registre
    return bytearray(asdu)

def creaTemps(year,mes,diames,hora=0,minut=0,estiu=0):
    '''
        minut:int, hora:int, diames:int, mes:int, year:int (0-99)
        estiu:<0,1> (0 default, if not specified)

        returns: objecte bytearray

        tipus a: 5 bytes == 40 bits:

        1-6     7     8    9-13   14-15   16   17-21    22-24       25-28   29-30   31-32   33-39   40
        +-------+-----+----+------+-------+----+--------+-----------+-------+-------+-------+-------+------+
        | minut | TIS | IV | hora |  RES1 | SU | diames | diasemana |  mes  |  ETI  |  PTI  |  year | RES2 |
        +-------+-----+----+------+-------+----+--------+-----------+-------+-------+-------+-------+------+

        minut     = UI6 - 0..59 
        TIS       = BS1 - tariff information switch
        IV        = BS1 - is invalid?
        hora      = UI5 - 0..23
        RES1      = BS2 - 00
        SU        = BS1 - Summer time?
        diames    = UI5 - 1..31
        diasemana = UI3 - 1..7
        mes       = UI3 - 1..12
        ETI       = UI2 - energi tariff information
        PTI       = UI2 - power tariff information
        year      = UI7 - 0..99
        RES2      = BS1 - 0
    '''
    trama=[None]*5
    trama[0] = minut
    trama[1] = hora
    trama[2] = diames
    trama[3] = mes
    trama[4] = year

    #suma el bit 16 (summer time, SU) al byte 1
    if estiu: trama[1] | 0b10000000

    return bytearray(trama)

def creaTramaFix(control):
    trama=[None]*6
    trama[0]=0x10 #inici            1   1   1   1   4   (bits)
    trama[1]=control #byte control [RES,PRM,FCB,FCV,FUN]
    trama[2]=(di & 0xff)
    trama[3]=(di & 0xff00)>>8
    trama[4]=(trama[1]+trama[2]+trama[3])%256 #checksum
    trama[5]=0x16 #fi
    return bytearray(trama)
    ''' tests trames fixes
        trama=creaTramaFix(0b01001001,1) #solicitud d'estat d'enllaç
        Pro.processa(trama)
        trama=creaTramaFix(0b01000000,1) #reset d'enllaç remot
        Pro.processa(trama)
    '''

def creaTramaVar(control,asdu):
    trama=[None]*8
    trama[0]=0x68 #inici
    trama[1]=0x00 #longitud
    trama[2]=0x00 #longitud
    trama[3]=0x68 #inici
    trama[4]=control
    trama[5]=(di & 0xff)
    trama[6]=(di & 0xff00)>>8
    trama[7:7+len(asdu)]=asdu
    checksum=0
    for i in range(4,len(trama)): checksum+=trama[i]
    checksum%=256
    trama.append(checksum)
    trama.append(0x16)
    trama[1]=3+len(asdu)
    trama[2]=3+len(asdu)
    return bytearray(trama)

'''tests
import processa as Pro
trama=creaTramaFix(0x49)
trama=creaTramaVar(0x73,creaASDU122(21,1,2,creaTemps(16,1,25,6,5,0),creaTemps(16,1,25,8,5,0)))
trama=creaTramaVar(0x73,creaASDU134(creaTemps(14,1,23,0,0,0),creaTemps(14,1,26,0,0,0)))
trama=creaTramaVar(0x53,creaASDU187())
trama=creaTramaVar(0x73,creaASDU183())
Pro.processa(trama)
'''
