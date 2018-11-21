# Teoria-da-Computação Automatos

#### Reconhecimento AFD:
    Armazena as transições no formato {q0:{a:q1, b:q2}}
	Possibilitando a cada leitura da palavra, ver o estado destino para determinado simbolo.
	Também verificando se existe transição do estado com o símbolo lido, caso não exista sai do laço de verificação e rejeita levando a um estado que não existe nos estados
	Ao fim ve se o ultimo estado da leitura existe nos estados finais
	Para caso de palavra vazia não entra no laço e verifica se o estado inicial é estado final
	
#### AFN para AFD:  
    Monta as transições no formato {(q0, a):[q0, q1], (q0, b):[q0]}
	Lê para cada um dos estados existentes todos os símbolos, criando um novo dicionario 
	Verifica se é um estado dos existentes no afn e passa por todas as saidas da leitura e cria novos estados para os casos em que retorne
	mais de um destino para determinado simbolo lido.
	Se for um estado dos novos criados fará a leitura de todos os estados para o símbolo e após remove as repetições transformando em um novo estado,
	caso seja um estado não existente nos estados do afn + estados novos criados adiciona a lista para verificação
	Descobre os estados finais vendo os estados que tem na descrição do nome um estado final
	Ao fim renomeia todos os estados 
	
#### AFNV para AFN: 
    Monta as transições todas as transições em um dicionario e as transições lendo vazio em outro
	Fazendo com que para saber quais as novas transições é só buscar para cada estado e símbolo lido, ver quais os estados destino e 
	cada estado destino buscar a correspondencia nas transições do dicionário dos vazios.
	Descobre os estados finais vendo os estados que levam até um estado final
