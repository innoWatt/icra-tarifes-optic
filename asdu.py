ASDU
{
    dataUnitIdentifier 
    {
        typeIdentifier              # 1 byte
            '''
                  1: M_SP_TA_2
                  8: M_IT_TG_2
                 11:
                 71:
                 72:
                100:
                102:
                103:
                122:
                123:
                128:
                129:
                130:
                131:
                132:
                133:
                134:
                135:
                136:
                137:
                138:
                139:
                140:
                141:
                142:
                143:
                144:
                145:
                146:
                147:
                148:
                149:
                180:
                181:
                182:
                183:
                184:
                185:
                186:
                187:
                188:
                189:
                190:
            '''
        variableStructureQualifier  # 1 byte
            '''
                ["SQ","N"]
                SQ : 1 bit (sempre 0)
                N  : 7 bits
                    nombre d'objectes d'informació
            '''
        causeOfTransmission         # 1 byte
            '''
                ["T","P/N","Causa"]
                T     : 1 bit (sempre 0)
                P/N   : 1 bit (sempre 0)
                Causa : 6 bits
                     4: Inicialitzada               (000100)
                     5: Petició o solicitada        (000101)
                     6: Activació                   (000110)
                     7: Confirmació                 (000111)
                     8: Desactivació                (001000)
                     9: Desactivació confirmada     (001001)
                    10: Finalització activació      (001010)
                    13: Registre no disponible      (001101)
                    14: ASDU no disponible          (001110)
                    15: Registre desconegut         (001111)
                    16: Direcció desconeguda        (010000)
                    17: Objecte info no disp.       (010001)
                    18: Període integració no disp. (010010)
            '''
        commonAddress               # 3 bytes
            '''
                direccio comptador
            '''
    }

    InformationObjects #array
    {
        direction
        element
        etiqueta temps (tipus a (5bytes), tipus b (7bytes) )
    }
    
    EtiquetaTempsComu # 5 bytes
}
