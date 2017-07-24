# -*- coding: UTF-8 -*-
import sys

def verifica_afd(palavra, estadoInicial, transicoes):
	# Estabelece o estado inicial para efetuar a primeira verificação de troca de estado
    estadoAtual = estadoInicial 

	# Lê a palavra simbolo a simbolo
    if palavra != '-': # Para palavra vazia não realiza movimento
        for simbolo in palavra:
	        # Busca o estado resultante da troca de estado no dicionario da afd Ex.: estadoAtual = 1 retorna '{'a':'1','b':'2'}'
            transicoesDir = transicoes[estadoAtual] 
	    	# Verifica se para este estado existe passo com o simbolo
            if simbolo in transicoesDir:
	    	# Busca qual estado de destino quando lendo determinada simbolo Ex.: b = 'a' retorna 1
                estadoAtual = transicoesDir[simbolo]
            else: # Caso não esteja definido transição com este símbolo rejeita a palavra
                estadoAtual = 'NONE'
                break		

    # Verifica se a palavra foi aceita ou nao pelo AFD 
	# Olhando se o ultimo estado está presente em um dos estados finais definidos no vetor de estados finais
    if estadoAtual in estadosFinais:
        pF = palavra + ' aceita'
    else:
        pF = palavra + ' rejeita'
    return pF
	
	
	
try:
    descricao = sys.argv[1]
except IndexError:
    descricao = 'descricao.txt'
try:
    entrada = sys.argv[2]
except IndexError:
    entrada = 'entrada.txt'  
try:
    saida = sys.argv[3]
except IndexError:
    saida = 'saida.txt'	

# Abrindo arquivo de descrição
arqDescricao = open(descricao, "r")	  
# Abrindo arquivo de entrada    
arqEntrada   = open(entrada,"r")
# Abrindo arquivo de saida
arqSaida     = open(saida,"w")

linhas = arqDescricao.readlines()

# Define o Formalismo
linha      = linhas[0]
formalismo = linha[0:linha.index('#')]	

# Define os estados
estados = []
linha   = linhas[1]
linha   = linha[1:linha.index('#')]
for coluna in linha:
    if coluna != ' ':
        estados.append(coluna)
	
# Define o alfabeto
alfabeto = []
linha    = linhas[2]
linha    = linha[1:linha.index('#')]
for coluna in linha:
    if coluna != '':
        alfabeto.append(coluna)

# Define o estado inicial	
linha         = linhas[3]
estadoInicial = linha[0]

# Define estados finais
estadosFinais = []
linha         = linhas[4]
linha         = linha[1:linha.index('#')]
for coluna in linha:
    if coluna != '':
        estadosFinais.append(coluna)
	
# Define as transições
# variável movimento receberá a cada interação objetos do tipo {'a': '1'}, concatenando a cada interação Ex.: {'a': '1', 'b':'2'}
# variável transicoes recebe a o resultado de movimento a cada interação Ex.: {'1': {'a': '1', 'b':'2'}...}
transicoes = {'NONE':''}
for i in estados:
    movimento = {}
    for l in linhas[5:]:
        if i == l[0]:
            movimento[l[2]] = l[4]
    transicoes[i] = movimento

# entrada recebe primeira linha do arquivo lido 
entrada = arqEntrada.readline()
while len(entrada) > 0:
	# Chama a função de validação do AFD
    palavraFinal = verifica_afd(entrada.strip(), estadoInicial, transicoes) # strip Remove espaços antes e depois da palavra e envia dados para verifica_afd
    arqSaida.write(palavraFinal+"\n")   # Grava a palavra final no arquivo de saida e muda de linha    
    entrada = arqEntrada.readline() # Passa para próxima linha 

# Fecha os arquivos abertos    
arqDescricao.close()
arqEntrada.close()
arqSaida.close()