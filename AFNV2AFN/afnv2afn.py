# -*- coding: UTF-8 -*-
import sys

def AFNV_para_AFN(estados, alfabeto, estado_Inicial, estados_Finais, transicoes, transicoes_AFNV):
    transicao_afn = {}
	
	# Transforma AFNV em AFN
	# Para cada estado, para cada simbolo
    for estado in estados:
        for simbolo in alfabeto:
		    # Verifica se existe transição com este movimento
            if (estado, simbolo) in transicoes:
			    # Caso exista percorre os destinos que levam esta transição Ex.: 0 a 1 2
                for estado_destino in transicoes[(estado, simbolo)]:	
                    # Percorre a lista das transições para vazio para cada destino da transição normal				
                    for transicao_vazia in transicoes_AFNV[estado_destino]:
                        if (estado, simbolo) in transicao_afn: 
						    # Verifica se é um estado não existente nas transições do afn final
                            if transicao_vazia not in transicao_afn[(estado, simbolo)]:
                                transicao_afn[(estado, simbolo)].append(transicao_vazia)
                        else:
                            transicao_afn[(estado, simbolo)] = [transicao_vazia]									
							
    finais = [] 
	# Define os novos estados finais
    for estado in estados:
        for simbolo in alfabeto:
            if (estado, simbolo) in transicao_afn:
                for estado_destino in transicao_afn[(estado, simbolo)]:
                    if (estado_destino in estados_Finais) and (estado not in finais):
                        finais.append(estado)

	# Guarda os dados para impressão						
    saida = {}
    saida['estados']    = list(map(str, estados))
    saida['terminais']  = alfabeto
    saida['inicial']    = estado_Inicial
    saida['finais']     = list(map(str, finais))
    saida['transicoes'] = transicao_afn
    return saida   

	
def salva_saida(saida_Final):
    # Salva arquivo de saida
    arqSaida.write('AFN' + '\n')
    arqSaida.write(str(len(saida_Final['estados'])) + ' ' + ' '.join(saida_Final['estados']) + '\n')
    arqSaida.write(str(len(saida_Final['terminais'])) + ' ' + ' '.join(saida_Final['terminais']) + '\n')
    arqSaida.write(str(saida_Final['inicial']) + '\n')
    arqSaida.write(str(len(saida_Final['finais'])) + ' ' + ' '.join(sorted(saida_Final['finais'])) + '\n')
    
    for estado in saida_Final['estados']:
        for simbolo in saida_Final['terminais']:
            if (estado, simbolo) in saida_Final['transicoes']: 
                transicao = map(str, sorted(saida_Final['transicoes'][(estado, simbolo)]))
                arqSaida.write(estado + ' ' + simbolo + ' ' + ' '.join(transicao) + '\n')	


				
try:
    descricao = sys.argv[1]
except IndexError:
    descricao = 'descricao.txt'
try:
    saida = sys.argv[3]
except IndexError:
    saida = 'saida.txt'
				
# Abrindo arquivo de descrição
arqDescricao = open(descricao, "r")	  
# Abrindo arquivo de saida
arqSaida     = open(saida,"w")

linhas = arqDescricao.readlines()

# 1: Define o Formalismo
linha      = linhas[0]
formalismo = linha[0:linha.index('#')]		

# 2: Define os estados
estados = []
linha   = linhas[1]
linha   = linha[1:linha.index('#')]
linha   = linha.split()
for coluna in linha:
    if coluna:
        estados.append(coluna)
		
# 3: Define o alfabeto
alfabeto = []
linha    = linhas[2]
linha    = linha[1:linha.index('#')]
linha    = linha.split()
for coluna in linha:
    if coluna:
        alfabeto.append(coluna)		
		
# 4: Define o estado inicial	
linha         = linhas[3]
estado_Inicial = linha[0]

# 5: Define estados finais
estados_Finais = []
linha         = linhas[4]
linha         = linha[1:linha.index('#')]
linha         = linha.split()
for coluna in linha:
    if coluna:
        estados_Finais.append(coluna)		

# 6+: Funcoes de transicao
trancicoes = {}
trancicoes_AFNV = {}

# Inicializa o vetor de Transições por Vazio com todos os estados levando ao próprio estado
for estado in estados:
    trancicoes_AFNV[(estado)] = [estado]

# Todas as transições
for i in range(5, len(linhas)):
    linha          = linhas[i]
    linha          = linha[0:linha.index('#')]
    linha          = linha.split()
    estado_partida = linha[0]
    simbolo        = linha[1]
    for l in linha[2:len(linha)]:
        estado_destino = l
        if simbolo in '-':
			# Transições por Vazio
            trancicoes_AFNV[(estado_partida)].append(estado_destino)
			
			# Transições por Vazio também contam como uma transição
            for simb in alfabeto:
                if (estado_partida, simb) in trancicoes:
                    trancicoes[(estado_partida, simb)].append(estado_destino)
                else:
                    trancicoes[(estado_partida, simb)] = [estado_destino]
        else:
            if (estado_partida, simbolo) in trancicoes:
                trancicoes[(estado_partida, simbolo)].append(estado_destino)
            else:
                trancicoes[(estado_partida, simbolo)] = [estado_destino]

# Passa os dados para o	AFNV_para_AFN
saida_Final = AFNV_para_AFN(estados, alfabeto, estado_Inicial, estados_Finais, trancicoes, trancicoes_AFNV)
salva_saida(saida_Final)

# Fecha os arquivos abertos    
arqDescricao.close()
arqSaida.close()