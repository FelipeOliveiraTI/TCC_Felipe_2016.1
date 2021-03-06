import igraph
from time import sleep

MAX_BASE=125
MIN_BASE=60

MAX_ALT =125
MIN_ALT =60

MAX_COMP =125
MIN_COMP =60

'''
MAX_BASE=105
MIN_BASE=80

MAX_ALT =105
MIN_ALT =80

MAX_COMP =105
MIN_COMP =80
'''

GARRA_A = 0
GARRA_F = 1

AUMENTA_5 = 5
DIMINUE_5  = 5

step = 5

ESTADO_INICIAL = [90,90,90,1]
PESO_INICIAL = 100

g = igraph.Graph()

def contar_nos():
    cont_nos = 0
    for x in xrange(MIN_BASE,MAX_BASE,step):
        for y in xrange(MIN_ALT,MAX_ALT,step):
            for z in xrange(MIN_COMP,MAX_COMP,step):
                cont_nos+=1

    return cont_nos*2

print contar_nos(), 'vertices calculados para o grafo'
sleep(1)
print 'criando vertices... aguarde um momento!'
g.add_vertices(contar_nos())
sleep(1)
print 'Todos os', contar_nos(), 'criados com sucesso...'
sleep(1)
print 'Criando status nas arestas...'
sleep(1)

TUPLA = [None,None,None,'']
g.vs['status'] = [TUPLA]
allVestices = g.vs.indices
allArestas = g.es.indices


def colocar_status(cont,TUPLA):
    g.vs[cont]['status'] = TUPLA

cont_indice_no_vizinho=-1
for x in xrange(MIN_BASE,MAX_BASE,step):
    for y in xrange(MIN_ALT,MAX_ALT,step):
        for z in xrange(MIN_COMP,MAX_COMP,step):
            cont_indice_no_vizinho+=1
            TUPLA = [x,y,z,GARRA_F]
            colocar_status(cont_indice_no_vizinho, TUPLA)
            for w in xrange(0,1):
                cont_indice_no_vizinho+=1
                TUPLA = [x,y,z,GARRA_A]
                colocar_status(cont_indice_no_vizinho, TUPLA)

def atribuir_arestas():
    for x in allVestices:

        no_index = g.vs.indices[x]
        no_favoravel_base   = g.vs[x]['status'][0]
        no_favoravel_altura = g.vs[x]['status'][1]
        no_favoravel_comp  =  g.vs[x]['status'][2]

        primeiro_valor = g.vs[x]['status'][0]
        segundo_valor  = g.vs[x]['status'][1]
        terceiro_valor = g.vs[x]['status'][2]
        quarto_valor   = g.vs[x]['status'][3]

        nos_favoraveis = g.vs.select(status_in=([(no_favoravel_base+AUMENTA_5),segundo_valor,terceiro_valor,quarto_valor],
                                                [(no_favoravel_base-DIMINUE_5),segundo_valor,terceiro_valor,quarto_valor],
                                                [primeiro_valor,(no_favoravel_altura+AUMENTA_5),terceiro_valor,quarto_valor],
                                                [primeiro_valor,(no_favoravel_altura-DIMINUE_5),terceiro_valor,quarto_valor],
                                                [primeiro_valor,segundo_valor,(no_favoravel_comp+AUMENTA_5),quarto_valor],
                                                [primeiro_valor,segundo_valor,(no_favoravel_comp-DIMINUE_5),quarto_valor],
                                                [primeiro_valor,segundo_valor,terceiro_valor,GARRA_A]))

        tam = len(nos_favoraveis)

        print g.vs.indices[x],'<- ID', g.vs[x]['status'],'| FAVORAVEIS - >',tam,\
            ' |',nos_favoraveis.indices,'->', nos_favoraveis.get_attribute_values('status')


        for no_final in nos_favoraveis.indices:
            if(no_index != no_final):
                g.add_edges([(no_index,no_final)])

atribuir_arestas()
sleep(1)
print 'Grafo criado com sucesso!'
sleep(1)
print len(g.es.indices),' arestas criadas com sucesso!'

'''
for x in allVestices:
    print x, g.vs[x]['status']
'''

g.es['weight'] = PESO_INICIAL

print pympler.asizeof.asizeof(g),'<-- TAMANHO DO GRAFO'

'''
print g.es['weight']

g.es[0]['weight'] = 1234567689

print g.es['weight']
'''

#menor_caminho = g.get_shortest_paths(0, contar_nos()-1, 'weight')
#print g.vs.degree(type='in')
#print 'Menor caminho ->',menor_caminho

#edges = g.es.select(_between = ([0, 1]))

#print  g.es[1:2]['weight'][0]-1
'''
arestas = g.es.select(_within=g.vs[0:10])
print 'pesos ->',arestas.get_attribute_values('weight')
print 'indices ->',arestas.indices
print 'Mudanca ->', arestas['weight']-1


inicio = g.vs.select(g.vs.indices[0])
fim    = g.vs.select(g.vs.indices[1])
print inicio.indices, inicio['status'],' ||||| ',fim.indices ,fim['status']
print g.es.select(_between=([inicio,fim]))['weight']


for x in g.es.indices:
    print x,g.es[x]['weight']
'''

#print g.es['weight']


