#!/usr/bin/env python
# -*- coding: utf-8 -*-

#interpretador python de Brainfuck

#Implementação da especificação da linguagem

#Os 8 comandos

#comandos = {"+":"mais",          incrementa em 1 o valor da célula atual
#            "-":"menos",         decrementa em 1 o valor da célula atual
#            ">":"sobePonteiro",  incrementa em 1 a localização da célula atual
#            "<":"descePonteiro", decrementa em 1 a localização da célula atual
#
#            ".":"printASCII",    mostra na tela o valor da celula atual,
#                                 convertido pra ASCII
#
#            ",":"recebeASCII",   Recebe um valor em ASCII e posiciona o valor
#                                 inteiro na célula atua
#
#            "[":"loop",          se o valor na célula atual for zero, vai para
#                                 o "]" correspondente, se não faz a próxima
#                                 instrução
#
#            "]":"loopEnd"        se o valor  na célula atual for zero, vai para
#                                 a próxima instrução, se não volta para o "["
#                                 correspondente
#           }


import sys

__version__ = "1.0"
__author__ = "lucas.sabiao@hotmail.com"

estrutura = [0] * 30000 #um vetor com 30.000 posições, isso deve ser o programa
ponteiro = 0            #um ponteiro indicando qual é a célula atual do programa
programa = ""           #o programa deve estar contido nessa string
posicao = 0             #qual instrução está sendo interpretada

def checkLoop():
    #procura por uma quantidade par de '[' e ']'
    global programa
    aberto = programa.count("[")
    fechado = programa.count("]")
    if (aberto == fechado):
        return True
    else:
        print ("Quantidade estranha de '[]'")
        return False

#implementação de cada instrução como uma funcão

#não fiquei feliz com essa quantidade absurda de "global"s, mas não achei
#nenhuma saída bem didática para isso.
def mais():
    global estrutura
    global ponteiro
    estrutura[ponteiro]+=1

def menos():
    global estrutura
    global ponteiro
    estrutura[ponteiro]-=1

def sobePonteiro():
    global estrutura
    global ponteiro
    ponteiro+=1

def descePonteiro():
    global estrutura
    global ponteiro
    ponteiro-=1

def printASCII():
    global estrutura
    global ponteiro
    print chr(estrutura[ponteiro]),
    sys.stdout.flush()

def recebeASCII():
    global estrutura
    global ponteiro
    aux = raw_input()
    try:
        estrutura[ponteiro] = ord(aux)
    except:
        estrutura[ponteiro] = 0


#Fiquei muito em dúvida sobre como fazer os loops.
#uma abordagem de manter na memória os endereços de cada "abrir" e "fechar"
#seria muito mais performática e limpo, mas achei que ficaria mais ilegível.
def loop():
    global estrutura
    global ponteiro
    global posicao
    if(estrutura[ponteiro] == 0):
        posicao = procurarEnd()
    else:
        pass

def loopEnd():
    global estrutura
    global ponteiro
    global posicao
    if(estrutura[ponteiro] == 0):
        pass
    else:
        posicao = procurarLoop()-1

def procurarEnd():
    global programa
    global posicao
    aux = 1
    posicaoAtual = posicao
    for instrucao in programa[posicao:]:
        if(aux == 0):
            return posicaoAtual
        if(instrucao == "["):
            aux+=1
        elif(instrucao == "]"):
            aux-=1
        posicaoAtual+=1

def procurarLoop():
    global programa
    global posicao
    aux = 1
    posicaoAtual = posicao
    for p in range(len(programa[:posicao])-1,0,-1):
        if(programa[p] == "]"):
            aux+=1
        elif(programa[p] == "["):
            aux-=1
        if(aux == 0):
            return posicaoAtual
        posicaoAtual-=1

def validarCelula():
    #python não suporta variáveis como byte.
    #workaround

    global estrutura
    global ponteiro
    if (estrutura[ponteiro] > 255):
        estrutura[ponteiro] = 255
    elif (estrutura[ponteiro] < 0):
        estrutura[ponteiro] = 0

def runPrograma():
    global programa
    global estrutura
    global ponteiro
    global posicao
    if(checkLoop()):
        while True:
            validarCelula()
            try:
                #não é a saida mais elegante, mas funciona muito bem
                instrucao = programa[posicao]
            except IndexError:
                break
            if (instrucao == "+"):
                mais()
            elif (instrucao == "-"):
                menos()
            elif (instrucao == ">"):
                sobePonteiro()
            elif (instrucao == "<"):
                descePonteiro()
            elif (instrucao == "."):
                printASCII()
            elif (instrucao == ","):
                recebeASCII()
            elif (instrucao == "["):
                loop()
            elif (instrucao == "]"):
                loopEnd()
            posicao+=1

if __name__ == "__main__":

    #Uso:
    #sem argumentos: pede para você digitar o programa

    #exemplo ou exemplo.bfmostrar na tela o programa "Hello World"
    #baseado no artigo en.wikipedia.org/wiki/Brainfuck

    #como interpretador, recebe o caminho para o arquivo a ser interpretado

    from sys import argv
    from os import getcwd
    if(len(argv)>1):
        if (argv[1].lower() == "exemplo" or argv[1].lower() == "exemplo.bf"): #hello world
            programa = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>   \
                        .>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
        else:
            #pegar o arquivo para interpretar
            path = getcwd()+"/"+argv[1]
            try:
                programa = open(path,"r").read()
            except:
                print "Progama não encontrado"
    else:
        programa = raw_input("Escreva seu programa: ")
    runPrograma()
