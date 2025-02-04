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

import math
import random
from collections import defaultdict
import util
import json


# **********************************************************
# **            PART 01 Modeling BlackJack                **
# **********************************************************


class BlackjackMDP(util.MDP):
    """
    The BlackjackMDP class is a subclass of MDP that models the BlackJack game as a MDP
    """
    def __init__(self, valores_cartas, multiplicidade, limiar, custo_espiada):
        """
        valores_cartas: list of integers (face values for each card included in the deck)
        multiplicidade: single integer representing the number of cards with each face value
        limiar: maximum number of points (i.e. sum of card values in hand) before going bust
        custo_espiada: how much it costs to peek at the next card
        """
        self.valores_cartas = valores_cartas
        self.multiplicidade = multiplicidade
        self.limiar = limiar
        self.custo_espiada = custo_espiada

    def startState(self):
        """
         Return the start state.
         Each state is a tuple with 3 elements:
           -- The first element of the tuple is the sum of the cards in the player's hand.
           -- If the player's last action was to peek, the second element is the index
              (not the face value) of the next card that will be drawn; otherwise, the
              second element is None.
           -- The third element is a tuple giving counts for each of the cards remaining
              in the deck, or None if the deck is empty or the game is over (e.g. when
              the user quits or goes bust).
        """
        return (0, None, (self.multiplicidade,) * len(self.valores_cartas))

    def actions(self, state):
        """
        Return set of actions possible from |state|.
        You do not must to modify this function.
        """
        return ['Pegar', 'Espiar', 'Sair']

    def succAndProbReward(self, state, action):
        """
        Given a |state| and |action|, return a list of (new_state, prob, reward) tuples
        corresponding to the states reachable from |state| when taking |action|.
        A few reminders:
         * Indicate a terminal state (after quitting, busting, or running out of cards)
           by setting the deck to None.
         * If |state| is an end state, you should return an empty list [].
         * When the probability is 0 for a transition to a particular new state,
           don't include that state in the list returned by succAndProbReward.
        """
        reachable_states = []
        if state[2] == None:
            return []
        if action == 'Sair':
            new_state = (state[0], None, None)
            if state[0] <= self.limiar:
                reward = state[0]
            reachable = (new_state, 1, reward)
            reachable_states.append(reachable)
        if action == 'Pegar':
            if state[1] != None:
                card_index = state[1]                
                prob = 1
                if self.valores_cartas[card_index] + state[0] > self.limiar:
                    reward = 0
                    new_state = (state[0] + self.valores_cartas[card_index], None, None)
                else:
                    new_amount = state[2][card_index] - 1
                    new_deck = state[2][:card_index] + (new_amount,) + state[2][card_index+1:]
                    if sum(new_deck) == 0:
                        new_deck = None
                        reward = self.valores_cartas[card_index] + state[0]
                    else:
                        reward = 0
                    new_state = (self.valores_cartas[card_index] + state[0], None, new_deck)
                reachable = (new_state, prob, reward)
                reachable_states.append(reachable)
            else:
                for i in range(len(state[2])):
                    amount = state[2][i]
                    reward = 0
                    if amount != 0:
                        new_amount = amount - 1
                        if state[0] + self.valores_cartas[i] > self.limiar:
                            reward = 0
                            new_state = (0, None, None)    
                        else:
                            new_deck = state[2][:i] + (new_amount,) + state[2][i+1:]
                            if sum(new_deck) == 0:
                                new_deck = None
                                reward = self.valores_cartas[i] + state[0]
                            new_state = (state[0] + self.valores_cartas[i], None, new_deck)
                        total_amount = sum(state[2])
                        prob = amount / total_amount
                        reachable = (new_state, prob, reward)
                        reachable_states.append(reachable)
        if action == 'Espiar':
            if state[1] != None:
                return []
            total_amount = sum(state[2])
            for i in range(len(state[2])):
                if state[2][i] != 0:
                    new_state = (state[0], i, state[2])
                    reachable = (new_state, state[2][i] / total_amount, -self.custo_espiada)
                    reachable_states.append(reachable)
        return reachable_states

    def discount(self):
        """
        Return the descount  that is 1
        """
        return 1

# **********************************************************
# **                    PART 02 Value Iteration           **
# **********************************************************

class ValueIteration(util.MDPAlgorithm):
    """ Asynchronous Value iteration algorithm """
    def __init__(self):
        self.pi = {}
        self.V = {}

    def solve(self, mdp, epsilon=0.001):
        """
        Solve the MDP using value iteration.  Your solve() method must set
        - self.V to the dictionary mapping states to optimal values
        - self.pi to the dictionary mapping states to an optimal action
        Note: epsilon is the error tolerance: you should stop value iteration when
        all of the values change by less than epsilon.
        The ValueIteration class is a subclass of util.MDPAlgorithm (see util.py).
        """
        mdp.computeStates()
        def computeQ(mdp, V, state, action):
            return sum(prob * (reward + mdp.discount() * V[new_state]) \
                            for new_state, prob, reward in mdp.succAndProbReward(state, action))

        def computeOptimalPolicy(mdp, V):
            # Return the optimal policy given the values V.
            pi = {}
            for state in mdp.states:
                pi[state] = max((computeQ(mdp, V, state, action), action) for action in mdp.actions(state))[1]
            return pi

        V = {}
        for state in mdp.states:
            V[state] = 0
        while True:
            Vp = {}
            for state in mdp.states:
                Vp[state] = max(computeQ(mdp, V, state, action) for action in mdp.actions(state))
            if max(abs(V[state] - Vp[state]) for state in mdp.states) < epsilon:
                    V = Vp
                    break
            V = Vp
        # Extract the optimal policy now
        pi = computeOptimalPolicy(mdp, V)
        self.pi = pi
        self.V = V

# First MDP
MDP1 = BlackjackMDP(valores_cartas=[1, 5], multiplicidade=2, limiar=10, custo_espiada=1)

# Second MDP
MDP2 = BlackjackMDP(valores_cartas=[1, 5], multiplicidade=2, limiar=15, custo_espiada=1)
def geraMDPxereta():
    """
    Return an instance of BlackjackMDP where peeking is the
    optimal action for at least 10% of the states.
    """
    # BEGIN_YOUR_CODE
    return BlackjackMDP(valores_cartas=[4, 5, 22], multiplicidade=1, limiar=20, custo_espiada=1)
    # return MDP
    # END_YOUR_CODE


# **********************************************************
# **                    PART 03 Q-Learning                **
# **********************************************************

class QLearningAlgorithm(util.RLAlgorithm):
    """
    Performs Q-learning.  Read util.RLAlgorithm for more information.
    actions: a function that takes a state and returns a list of actions.
    discount: a number between 0 and 1, which determines the discount factor
    featureExtractor: a function that takes a state and action and returns a
    list of (feature name, feature value) pairs.
    explorationProb: the epsilon value indicating how frequently the policy
    returns a random action
    """
    def __init__(self, actions, discount, featureExtractor, explorationProb=0.2):
        self.actions = actions
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    def getQ(self, state, action):
        """
         Return the Q function associated with the weights and features
        """
        score = 0
        for f, v in self.featureExtractor(state, action):
            score += self.weights[f] * v
        return score

    def getAction(self, state):
        """
        Produce an action given a state, using the epsilon-greedy algorithm: with probability
        |explorationProb|, take a random action.
        """
        self.numIters += 1
        if random.random() < self.explorationProb:
            return random.choice(self.actions(state))
        return max((self.getQ(state, action), action) for action in self.actions(state))[1]

    def getStepSize(self):
        """
        Return the step size to update the weights.
        """
        return 1.0 / math.sqrt(self.numIters)

    def incorporateFeedback(self, state, action, reward, new_state):
        """
         We will call this function with (s, a, r, s'), which you should use to update |weights|.
         You should update the weights using self.getStepSize(); use
         self.getQ() to compute the current estimate of the parameters.

         HINT: Remember to check if s is a terminal state and s' None.
        """
        if new_state is None:
            return
        v_max = max((self. getQ(new_state, new_action) for new_action in self.actions(state)))
        difference = (reward + self.discount * v_max) - self.getQ(state, action)
        alpha = self.getStepSize()
        for f, v in self.featureExtractor(state, action):
            self.weights[f] += alpha*(difference)*v
            

def identityFeatureExtractor(state, action):
    """
    Return a single-element list containing a binary (indicator) feature
    for the existence of the (state, action) pair.  Provides no generalization.
    """
    featureKey = (state, action)
    featureValue = 1
    return [(featureKey, featureValue)]

# Large test case
largeMDP = BlackjackMDP(valores_cartas=[1, 3, 5, 8, 10], multiplicidade=3, limiar=40, custo_espiada=1)

# **********************************************************
# **        PART 03-01 Features for Q-Learning             **
# **********************************************************

def blackjackFeatureExtractor(state, action):
    """
    You should return a list of (feature key, feature value) pairs.
    (See identityFeatureExtractor() above for a simple example.)
    """
    # BEGIN_YOUR_CODE
    total, peek_card, deck = state
    if deck == None:
        return []

    features = []
    # Exemplo 1
    features.append(((total, action), 1))

    # Exemplo 2
    presence = ()
    for card in deck:
        if card > 0:
            presence = presence + (1,)
    features.append(((presence, action), 1))

    # Exemplo 3
    for i in range(len(deck)):
        features.append(((i, deck[i], action), 1))

    # Feature extra - ((cartaEspiada, action). 1):
    # if peek_card != None:
        # features.append(((peek_card, action), 1))

    return features
    # END_YOUR_CODE

def simulaMDP(mdp, extractor, explorationProb):
    value_iterator = ValueIteration()
    value_iterator.solve(mdp)
    policyVi = value_iterator.pi
    mdp.computeStates()

    qLearning = QLearningAlgorithm(mdp.actions, mdp.discount(), extractor, explorationProb)
    util.simulate(mdp,qLearning, 30000, 10, False, False)
    mdp.explorationProb = 0
    actionsQ = {}

    for state in mdp.states:
        actionsQ[state] = qLearning.getAction(state)

    differentActions = 0
    for state in actionsQ.keys():
        if actionsQ[state] != policyVi[state]:
            differentActions += 1
    return differentActions


# SIMULAÇÕES (Descomentar para testar)
# 1 - MDP1 com expProb 0.2
# print("Diferença em MDP1:", simulaMDP(MDP1, identityFeatureExtractor, 0.2))

# 2 - largeMDP com expProb 0
# print("Diferença em largeMDP:", simulaMDP(largeMDP, identityFeatureExtractor, 0))

# 3 - largeMDP com expProb 0 e blackJackFeature
# print("Diferença em largeMDP:", simulaMDP(largeMDP, blackjackFeatureExtractor, 0.2))

# 4 - largeMDP com expProb 0.2 e blackJackFeature
# print("Diferença em largeMDP:", simulaMDP(largeMDP, blackjackFeatureExtractor, 0.2))