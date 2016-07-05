import pygame.joystick
from pygame.locals import * # This module contains various constants used by Pygame
import sys
sys.path.insert(0, "../lib")
from time import sleep
import time
import paho.mqtt.client as paho
import ssl
import grafo
import random
import serial
from statistics import mode

'''
ROOT_CA = "C:/Users/FELIPE/certs/VeriSign.pem"
CERTIFICATE = "C:/Users/FELIPE/certs/60b7fe5adc-certificate.pem.crt"
PRIVATE_KEY = "C:/Users/FELIPE/certs/60b7fe5adc-private.pem.key"
AWS_IOT_TOPIC = "$aws/things/LeapMotionThing/shadow/update"
AWS_IOT_ENDPOINT = "A1GLZ6XBSV9PUG.iot.us-west-2.amazonaws.com"

mqttc = paho.Client()

def on_mqtt_log(self, client, level, buf):
            print(str(level) + ": '" + str(buf))

def on_mqtt_connect(self, userdata, flags, rc):
    print("Connected with result code "+str(rc))

mqttc.tls_set(ROOT_CA, CERTIFICATE, PRIVATE_KEY, tls_version=ssl.PROTOCOL_TLSv1_2)
mqttc.on_log = on_mqtt_log
mqttc.on_connect = on_mqtt_connect
mqttc.connect(AWS_IOT_ENDPOINT, 8883, 10)
time.sleep(4)
mqttc.loop_start()
'''
ESTADO_INICIAL = grafo.ESTADO_INICIAL

base = ESTADO_INICIAL[0]
altura = ESTADO_INICIAL[1]
complemento = ESTADO_INICIAL[2]
garra = ESTADO_INICIAL[3]


ser = serial.Serial('COM5', 9600)
STEP = 5

no_inicial = grafo.g.vs.select(status_in=([ESTADO_INICIAL]))
no_final = 0


lista_nos_local = [no_inicial.indices]
lista_nos_global = []
lista_nos_finais = []


print ESTADO_INICIAL, '<- Status Vertice Inicial | ID do Vertice Inicial->', no_inicial.indices

cont_indice_no_vizinho=0
def input(events):
    for event in events:
        if event.type == JOYBUTTONDOWN:

            button0 = joystick.get_button(0)
            button1 = joystick.get_button(1)
            button2 = joystick.get_button(2)
            button3 = joystick.get_button(3)
            button4 = joystick.get_button(4)
            button5 = joystick.get_button(5)
            button6 = joystick.get_button(6)
            button7 = joystick.get_button(7)
            button8 = joystick.get_button(8)
            button9 = joystick.get_button(9)

            b = [button0,button1,button2,button3,button4,button5,button6,button7,button8,button9]
            global base
            global altura
            global complemento
            global garra
            global STEP
            global ESTADO_INICIAL
            global lista_nos_global
            global lista_nos_local
            global ser
            if b[5] == 1:
                #mqttc.publish(AWS_IOT_TOPIC, 'base_dir', 0, False)
                if base < grafo.MAX_BASE-STEP:
                    base+=STEP
                    configurar_passos(base,altura,complemento,garra)
            elif b[4] == 1:
                #mqttc.publish(AWS_IOT_TOPIC, 'base_esq', 0, False)
                if base > grafo.MIN_BASE:
                    base-=STEP
                    configurar_passos(base,altura,complemento,garra)
            elif b[0] == 1:
                #mqttc.publish(AWS_IOT_TOPIC, 'altura_aum', 0, False)
                if altura < grafo.MAX_ALT-STEP:
                    altura+=STEP
                    configurar_passos(base,altura,complemento,garra)
            elif b[2] == 1:
                #mqttc.publish(AWS_IOT_TOPIC, 'altura_dim', 0, False)
                if altura > grafo.MIN_ALT:
                    altura-=STEP
                    configurar_passos(base,altura,complemento,garra)
            elif b[3] == 1:
                #mqttc.publish(AWS_IOT_TOPIC, 'comp_aum', 0, False)
                if complemento < grafo.MAX_COMP-STEP:
                    complemento+=STEP
                    configurar_passos(base,altura,complemento,garra)
            elif b[1] == 1:
                #mqttc.publish(AWS_IOT_TOPIC, 'comp_dim', 0, False)
                if complemento > grafo.MIN_COMP:
                    complemento-=STEP
                    configurar_passos(base,altura,complemento,garra)
            elif b[6] == 1:
                #mqttc.publish(AWS_IOT_TOPIC, 'garra_fec', 0, False)
                garra+=1
                if garra == 2:
                    garra=0
                    configurar_passos(base,altura,complemento,garra)
                elif garra ==1:
                    garra=1
                    configurar_passos(base,altura,complemento,garra)

            elif b[7] == 1:
                #mqttc.publish(AWS_IOT_TOPIC, 'garra_abr', 0, False)
                '''garra='A'
                configurar_passos(base,altura,complemento,garra)'''
                sleep(1)
                print 'COLETA REALIZADA COM SUCESSO!'
                sleep(1)
                criar_lista_global()
                voltar_pro_inicio()

                print 'COLETA ATUAL',lista_nos_local
                sleep(.1)
                print 'COLETA GERAL',lista_nos_global
                sleep(1)
                if len(lista_nos_global) == 1:
                     print 'VOCE POSSUI',len(lista_nos_global),'COLETA! FORNECA OUTRAS!'
                else:
                    print 'VOCE POSSUI',len(lista_nos_global),'COLETAS! FORNECA OUTRAS!'



            elif b[8] == 1:
               #mqttc.publish(AWS_IOT_TOPIC, 'back_index', 0, False)
                sleep(1)
                #print 'INCIANDO A FASE DE TREINAMENTO...'
                #decrementar_pesos(lista_nos_global)

                caixa_de_dialogo1()

            elif b[9] == 0:
               #mqttc.publish(AWS_IOT_TOPIC, 'back_index', 0, False)
                #selecionar_nos_visitados()
                print 'BOTAO START QUE NAO FUNCIONA'
            else:
                print 'AQUI EH OUTRA COISA'

        '''
        if event.type == JOYAXISMOTION:
            #comando = [event.axis, event.value] # JOYAXISMOTION
            #print comando
            menor_caminho = grafo.g.get_shortest_paths(0,849 ,'weight')
            print 'Menor caminho ->',menor_caminho

            reiniciar_programa()'''



def voltar_pro_inicio():
    global base, altura, complemento, garra
    base = grafo.ESTADO_INICIAL[0]
    altura = grafo.ESTADO_INICIAL[1]
    complemento = grafo.ESTADO_INICIAL[2]
    garra = grafo.ESTADO_INICIAL[3]
    INICIO = str(base)+','+str(altura)+','+str(complemento)+','+str(garra)+'\n'
    ser.write(INICIO)


def caixa_de_dialogo1():
    global lista_nos_global
    switcher = raw_input("ESCOLHA UMA DAS OPCOES:\n"
                         "[1] - INICIAR A FASE DE TREINAMENTO\n"
                         "[2] - REINICIAR FASE DE COLETA\n"
                         "[3] - SELECIONAR QUANTIDADE DE COLETAS PARA TREINAMENTO\n"
                         "[4] - SAIR\n")
    if int(switcher) == 1:

        decrementar_pesos(lista_nos_global)



    elif int(switcher) == 2:
        reiniciar_programa()
    elif int(switcher) == 3:
        treino_baseado_em_coletas()
    elif int(switcher) == 4:
        print
    else:
        print 'FORNECA UMA ENTRADA VALIDA!'
        caixa_de_dialogo1()


def atualizar_lista_local(comando):
    global lista_nos_local
    lista_nos_local.append(comando)

def criar_lista_global():
    global lista_nos_local
    global lista_nos_global
    global cont_indice_no_vizinho
    tam = len(lista_nos_local)
    if tam !=1:
        lista_nos_global.append(lista_nos_local)
        lista_nos_local = [no_inicial.indices]
        cont_indice_no_vizinho=0

def configurar_passos(ba,al,co,ga):
    PASSO = [ba,al,co,ga]
    indice_local = grafo.g.vs.select(status_in=([PASSO]))
    atualizar_lista_local(indice_local.indices)
    print PASSO,'<-- STATUS ATUAL | VERTICE ATUAL -->',indice_local.indices
    angulos = criar_mensagem_angulos(PASSO)

    ser.write(angulos)

def criar_mensagem_angulos(PASSO):

    if len(str(PASSO[0])) == 2:
        ang_base = '0'+str(PASSO[0])
    else: ang_base = str(PASSO[0])
    if len(str(PASSO[1])) == 2:
        ang_altura = '0'+str(PASSO[1])
    else: ang_altura = str(PASSO[1])
    if len(str(PASSO[2])) == 2:
        ang_complemento = '0'+str(PASSO[2])
    else: ang_complemento = str(PASSO[2])

    return ang_base+','+ang_altura+','+ang_complemento+','+str(PASSO[3])+'\n'


def decrementar_pesos(lista_global):
    inicioTreinamento = time.time()
    print lista_global
    global cont_indice_no_vizinho
    for lista_local in lista_global:
        for cont_indice_no_vizinho in range(len(lista_local)):
            nos_vizinhos_lista_atual = lista_local[cont_indice_no_vizinho:cont_indice_no_vizinho + 2]
            if len(nos_vizinhos_lista_atual) != 1:
                #print cont_indice_no_vizinho,len(nos_vizinhos_lista_atual)
                cont_indice_no_vizinho+=1
                #sleep(1)
                if len(nos_vizinhos_lista_atual)>=2:
                    id_no_index = nos_vizinhos_lista_atual[0][0]
                    id_no_final = nos_vizinhos_lista_atual[1][0]

                    id_aresta = grafo.g.get_eid(id_no_index,id_no_final)
                    aresta = grafo.g.es.find(id_aresta)
                    #peso = grafo.g.es[id_aresta]['weight']
                    print aresta.attributes()
                    grafo.g.es[id_aresta]['weight']-=1
                    print 'ARESTA -->',id_aresta,'|| ENTRE OS VERTICES -->',id_no_index, id_no_final,'|| TREINADA COM SUCESSO!',aresta.attributes()

                    #peso1 = aresta.attributes()
                    #print id_aresta
                    #print grafo.g.es[id_aresta]['weight']
        no_final = lista_local[-1]
        criar_lista_nos_finais(no_final)
        print 'TREINAMENTO REALIZADO COM SUCESSO!'
    sleep(1)
    print 'FASE DE TREINAMENTO FINALIZADA!'
    voltar_pro_inicio()
    #print '\n'*5
    sleep(1)
    fimTreinamento = time.time()
    print (fimTreinamento - inicioTreinamento), '<-- TEMPO TREINAMENTO ############'
    caixa_de_dialogo2()




def caixa_de_dialogo2():
    switcher = raw_input("ESCOLHA UMA DAS OPCOES:\n"
                    "[1] - INICIAR A FASE DE EXECUCAO\n"
                    "[2] - REINICIAR FASE DE COLETA\n"
                    "[3] - SELECIONAR QUANTIDADE DE COLETAS PARA TREINAMENTO\n"
                    "[4] - SAIR\n")

    if int(switcher)   == 1:
        iniciar_fase_execucao()
    elif int(switcher) == 2:
        reiniciar_programa()
    elif int(switcher) == 3:
        treino_baseado_em_coletas()
    elif int(switcher) == 4:
        print
    else:
        print 'FORNECA UMA ENTRADA VALIDA!'
        caixa_de_dialogo2()


def treino_baseado_em_coletas():
    global lista_nos_local
    global lista_nos_global

    treinos = len(lista_nos_global)
    print 'VOCE POSSUI', treinos, 'COLETAS ATUALMENTE'
    quant = raw_input('FORCENA DENTRE SUAS COLETAS UMA QUANTIDADE PARA O TREINAMENTO\n')
    if int(quant) <= treinos:
        amostra = random.sample(lista_nos_global, int(quant))
        quant=0
        sleep(1)
        print 'QUANTIDADE DE COLETAS PARA TREINAMENTO SELECIONADA COM SUCESSO!'
        grafo.g.es['weight'] = grafo.PESO_INICIAL
        decrementar_pesos(amostra)
    else:
        print 'FORNECA UMA QUANTIDADE VALIDA!'
        print quant, '<- Quant', 'Coletas',treinos
        sleep(1)
        treino_baseado_em_coletas()


def iniciar_fase_execucao():
    print 'FASE DE EXECUCAO INICIALIZADA COM SUCESSO!'
    global no_inicial
    global no_final
    global lista_nos_finais
    global lista_nos_global
    inicioInferenia = time.time()


    '''
        NO FINAL EH SEMPRE O PRIMEIRO DA LISTA
        MELHORAR ESSA SELACAO DEPOIS
    '''
    if lista_nos_global:

        sleep(0.2)
        print 'PERCORRENDO O MELHOR CAMINHO...'
        print lista_nos_finais,'<-LISTA NOS FINAIS'
        lista_para_eleicao = []
        for x in lista_nos_finais:
            lista_para_eleicao.append(x[0])

        try:
          no_eleito = mode(lista_para_eleicao)
          no_final= no_eleito
        except:
            no_final = lista_nos_finais[0][0]

        subir_pesos_antigos()

        menor_caminho = grafo.g.get_shortest_paths(no_inicial.indices[0],no_final ,'weight')

        fimInferencia = time.time()
        print (fimInferencia - inicioInferenia), '<--- TEMPO DA INFERENCIA! ############'

        print menor_caminho,'<- MENOR CAMINHO!'
        switcher = raw_input("ESCOLHA UMA DAS OPCOES:\n"
                    "[1] - EXECUTAR MODO LOOP\n"
                    "[2] - ESCOLHER QUANTIDADE PARA EXECUCAO\n"
                    "[4] - SAIR\n")

        if int(switcher)   == 1:
            sleep(1)
            while True:
                for indice_melhor_caminho in menor_caminho[0]:
                    status_melhor_caminho = grafo.g.vs[indice_melhor_caminho]['status']
                    print 'STATUS DO VERTICE ->',status_melhor_caminho,'|',indice_melhor_caminho,'<- INDICE DO VERTICE |','MODO LOOP ATIVADO'
                    angulos = criar_mensagem_angulos(status_melhor_caminho)
                    print angulos
                    ser.write(angulos)
                    sleep(.2)
        elif int(switcher) == 2:
            sleep(1)
            quantidade = raw_input("DIGITE A QUANTIDADE DE VEZES PARA EXECUCAO DA TAREFA\n")
            sleep(1)
            print 'A TAREFA SERA REALIZADA',quantidade,'VEZES'
            for x in xrange(int(quantidade)):
                for indice_melhor_caminho in menor_caminho[0]:
                    status_melhor_caminho = grafo.g.vs[indice_melhor_caminho]['status']
                    print 'STATUS DO VERTICE ->',status_melhor_caminho,'|',indice_melhor_caminho,'<- INDICE DO VERTICE |','EXECUCAO NUMERO',x+1,'/',quantidade
                    angulos = criar_mensagem_angulos(status_melhor_caminho)
                    print angulos
                    ser.write(angulos)
                    sleep(.2)
            voltar_pro_inicio()
            caixa_de_dialogo2()
        elif int(switcher) == 3:
            sleep(1)
            quantidade = raw_input("PARA PARAR APERTE [P] E PRESSIONE ENTER\n")
            while not quantidade:
                for indice_melhor_caminho in menor_caminho[0]:
                    status_melhor_caminho = grafo.g.vs[indice_melhor_caminho]['status']

                    print 'STATUS DO VERTICE ->',status_melhor_caminho,'|',indice_melhor_caminho,'<- INDICE DO VERTICE'
                    angulos = criar_mensagem_angulos(status_melhor_caminho)
                    ser.write(angulos)
                    sleep(1)
                if quantidade == 'P':
                    break

        elif switcher == '4':
            print
        else:
            print 'FORNECA UMA ENTRADA VALIDA!'

def pegarTempoTreno(iniTre,fimTre):
    return iniTre - fimTre
def pegarTempoInferencia(iniInf,fimInf):
    return iniInf - fimInf



def subir_pesos_antigos():
    pesos_antigos = grafo.g.es.select(weight_eq=(grafo.PESO_INICIAL))
    for x in pesos_antigos.indices:
        grafo.g.es[x]['weight'] = (grafo.PESO_INICIAL * 200)


def criar_lista_nos_finais(no_final):
    global lista_nos_finais
    lista_nos_finais.append(no_final)


def reiniciar_programa():
    global lista_nos_global, lista_nos_local, lista_nos_finais
    print 'REINICIANDO PROGRAMA...'
    lista_nos_global = []
    lista_nos_local = [no_inicial.indices]
    grafo.g.es['weight'] = grafo.PESO_INICIAL
    lista_nos_finais = []
    voltar_pro_inicio()
    sleep(1)
    print 'PROGRAMA REINICIADO COM SUCESSO!!!'
    sleep(1)
    print 'FASE DE COLETA INICIALIZADA! FORNECA OS COMANDOS PELO JOYSTICK!'
    #print grafo.g.es['weight']


#print grafo.g.es.get_attribute_values('weight')
# Initialize all imported Pygame modules (a.k.a., get things started)
pygame.init()

# Enable joystick support
pygame.joystick.init()

# Detect if joystick is available
joysticks = pygame.joystick.get_count()
if joysticks:
    sleep(1)
    print str(joysticks) + " joystick(s) detected!"

# Initialize the joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()
name = joystick.get_name()
#print "Joystick " + str(0) + " name: " + name
sleep(1)
print 'FASE DE COLETA INICIALIZADA! FORNECA OS COMANDOS PELO JOYSTICK!'

# The game loop
while True:
    input(pygame.event.get())