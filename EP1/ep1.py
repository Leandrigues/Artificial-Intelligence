"""
  AO PREENCHER ESSE CABECALHO COM O MEU NOME E O MEU NUMERO USP,
  DECLARO QUE SOU A UNICA PESSOA AUTORA E RESPONSAVEL POR ESSE PROGRAMA.
  TODAS AS PARTES ORIGINAIS DESSE EXERCICIO PROGRAMA (EP) FORAM
  DESENVOLVIDAS E IMPLEMENTADAS POR MIM SEGUINDO AS INSTRUCOES
  DESSE EP E, PORTANTO, NAO CONSTITUEM ATO DE DESONESTIDADE ACADEMICA,
  FALTA DE ETICA OU PLAGIO.
  DECLARO TAMBEM QUE SOU A PESSOA RESPONSAVEL POR TODAS AS COPIAS
  DESSE PROGRAMA E QUE NAO DISTRIBUI OU FACILITEI A
  SUA DISTRIBUICAO. ESTOU CIENTE QUE OS CASOS DE PLAGIO E
  DESONESTIDADE ACADEMICA SERAO TRATADOS SEGUNDO OS CRITERIOS
  DIVULGADOS NA PAGINA DA DISCIPLINA.
  ENTENDO QUE EPS SEM ASSINATURA NAO SERAO CORRIGIDOS E,
  AINDA ASSIM, PODERAO SER PUNIDOS POR DESONESTIDADE ACADEMICA.

  Nome : Leandro Rodrigues da Silva
  NUSP : 10723944

  Referencias: Com excecao das rotinas fornecidas no enunciado
  e em sala de aula, caso voce tenha utilizado alguma referencia,
  liste-as abaixo para que o seu programa nao seja considerado
  plagio ou irregular.

  Exemplo:
  - O algoritmo Quicksort foi baseado em:
  https://pt.wikipedia.org/wiki/Quicksort
  http://www.ime.usp.br/~pf/algoritmos/aulas/quick.html
"""

import util

############################################################
# Part 1: Segmentation problem under a unigram model

class SegmentationProblem(util.Problem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def isState(self, state):
        """ Metodo que implementa verificacao de estado """
        return True

    def initialState(self):
        """ Metodo que implementa retorno da posicao inicial """
        initialState = (self.query,)
        return initialState

    def actions(self, state):
        """ Metodo que implementa retorno da lista de acoes validas
        para um determinado estado
        """
        actions = ()
        for i in range(len(state[-1])):
            actions += (i, )

        return actions

    def nextState(self, state, action):
        """ Metodo que implementa funcao de transicao """

        if len(state) == 1:
            nextState = (state[0][:action+1], state[0][action+1:])
            return nextState

        nextState = state[:-1] + (state[-1][:action+1],) + (state   [-1][action + 1:],) 
        
        return nextState

    def isGoalState(self, state):
        """ Metodo que implementa teste de meta """
        return len(state[-1]) == 0

    def stepCost(self, state, action):
        """ Metodo que implementa funcao custo """
        nextState = self.nextState(state, action)

        return self.unigramCost(nextState[-2])


def segmentWords(query, unigramCost):

    if len(query) == 0:
        return ''
     

    problem = SegmentationProblem(query, unigramCost)
    goalNode = util.uniformCostSearch(problem)
    solution = ' '.join(goalNode.state[:-1])

    return solution

    # BEGIN_YOUR_CODE 
    # Voce pode usar a função getSolution para recuperar a sua solução a partir do no meta
    # valid,solution  = util.getSolution(goalNode,problem)


    # END_YOUR_CODE

############################################################
# Part 2: Vowel insertion problem under a bigram cost

class VowelInsertionProblem(util.Problem):
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def isState(self, state):
        """ Metodo  que implementa verificacao de estado """
        return True

    def initialState(self):
        """ Metodo  que implementa retorno da posicao inicial """
        initialState = (util.SENTENCE_BEGIN,)
        for item in self.queryWords:
            initialState += (item,)

        return initialState

    def actions(self, state):
        """ Metodo  que implementa retorno da lista de acoes validas
        para um determinado estado
        """
        actions = ()
        for i in range(1, len(state)):
            possSize = len(self.possibleFills(state[i]))
            for j in range(possSize):
                newAction = (i, j)
                actions += (newAction,)
        
        return actions

    def nextState(self, state, action):
        """ Metodo que implementa funcao de transicao """
        wordPosition = action[0]
        choicePosition = action[1]
        array = [i for i in self.possibleFills(self.initialState()[action[0]])]
        choice = array[choicePosition]
        nextState = state[:wordPosition] + (choice,) + state[wordPosition + 1:]

        return nextState

    def isGoalState(self, state):
        """ Metodo que implementa teste de meta """
        actions = self.actions(state)

        return len(actions) == 0

    def stepCost(self, state, action):
        """ Metodo que implementa funcao custo """
        nextState = self.nextState(state, action)
        cost = self.bigramCost(nextState[action[0]-1], nextState[action[0]])
        return cost


def insertVowels(queryWords, bigramCost, possibleFills):
    problem = VowelInsertionProblem(queryWords, bigramCost, possibleFills)
    goalNode = util.uniformCostSearch(problem)
    finalState = goalNode.state
    solutionArray = [i for i in finalState[1:]]
    solution = ' '.join(solutionArray)
    return solution

############################################################



def getRealCosts(corpus):
    """ Retorna as funcoes de custo unigrama, bigrama e possiveis fills obtidas a partir do corpus."""
    
    _realUnigramCost, _realBigramCost, _possibleFills = None, None, None
    if _realUnigramCost is None:
        print('Training language cost functions [corpus: '+ corpus+']... ')
        
        _realUnigramCost, _realBigramCost = util.makeLanguageModels(corpus)
        if corpus == "corpus.txt":
            _possibleFills = util.makeInverseRemovalDictionary(corpus, 'aeiou')
        else:
            _possibleFills = util.makeInverseRemovalDictionary(corpus, 'aáàãâeéêiíoõôóuú')

        print('Done!')

    return _realUnigramCost, _realBigramCost, _possibleFills

def main():
    """ Voce pode/deve editar o main() para testar melhor sua implementacao.

    A titulo de exemplo, incluimos apenas algumas chamadas simples para
    lhe dar uma ideia de como instanciar e chamar suas funcoes.
    Descomente as linhas que julgar conveniente ou crie seus proprios testes.
    """
    # Para alterar o corpus, basta trocar o valor da variável:    
    corpus = 'corpus.txt'
    # Para tornar o recebimento do corpus iterativo, remova os comentários:
    #############################################################
    # lang = input("Qual idioma deseja utilizar? (Português=PT, Inglês=EN)")

    # if lang == 'PT':
    #     corpus = 'corpusPT.txt'
    # else:
    #     corpus = 'corpus.txt'
    #############################################################
    param1 = 'believeinyourselfhavefaithinyourabilities'
    param2 = 'smtms ltr bcms nvr'

    unigramCost, bigramCost, possibleFills  =  getRealCosts(corpus)
    
    resultSegment = segmentWords(param1, unigramCost)
    print(resultSegment)

    resultInsert = insertVowels(param2.split(), bigramCost, possibleFills)
    print(resultInsert)

if __name__ == '__main__':
    main()
