from ep3 import *
from util import *

class ExampleMDP(util.MDP):
    def startState(self):
        return 0

    # Return set of actions possible from |state|.
    def actions(self, state):
        return ['Left', 'Right']

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.
    def succAndProbReward(self, state, action):
        if state == -2 or state == 2:
            return []
        
        leftReward = -5
        rightReward = -5

        if state - 1 == -2:
            leftReward = 20
        if state + 1 == 2:
            rightReward = 100
        
        if action == 'Left':
            results = [(state-1, 0.8, leftReward), (state+1, 0.2, rightReward)]
        elif  action == 'Right':
            results = [(state-1, 0.7, leftReward), (state+1, 0.3, rightReward)]
        else:
            results = []
        
        return results
            
    def discount(self):
        return 1


def main():
    try:
        print('\n========== Problem A ==========')
        mdp = ExampleMDP()
        algorithm = ValueIteration()
        algorithm.solve(mdp) # when epsilon=20, the algorithm repeats 2 iterations
        for i in [-2, -1, 0, 1, 2]:
            print("Value of the state '%d' : %f"%(i, algorithm.V[i]))

        for i in [-1, 0, 1]:
            print("Plicy at the state '%d' : %s"%(i, algorithm.pi[i]))

        print('\n========== Problem C ==========')
        mdp1 = BlackjackMDP(valores_cartas=[1, 5], multiplicidade=2, limiar=10, custo_espiada=1)
        startState = mdp1.startState()
        preBustState = (6, None, (1, 1))
        postBustState = (11, None, None)

        mdp2 = BlackjackMDP(valores_cartas=[1, 5], multiplicidade=2, limiar=15, custo_espiada=1)
        preEmptyState = (11, None, (1,0))

        print('\n---------- Test c1 ----------')
        # Make sure the succAndProbReward function is implemented correctly.

        vanilla_tests = [
            ([((1, None, (1, 2)), 0.5, 0), ((5, None, (2, 1)), 0.5, 0)], mdp1, startState, 'Pegar'),
            ([((0, None, None), 1, 0)], mdp1, startState, 'Sair'),
            ([((7, None, (0, 1)), 0.5, 0), ((11, None, None), 0.5, 0)], mdp1, preBustState, 'Pegar'),
            ([], mdp1, postBustState, 'Pegar'),
            ([], mdp1, postBustState, 'Sair'),
            ([((12, None, None), 1., 12)], mdp2, preEmptyState, 'Pegar'),
        ]

        print('Vanilla Blackjack')
        for no, (answer, mdp, state, action) in enumerate(vanilla_tests):
            print('No %d'%(no+1), end=' ')
            if answer != mdp.succAndProbReward(state, action):
                print('=> wrong')
            else:
                print('=> right')
            print('- state: {}, action: {}'.format(state, action))
            print('- true answer =', answer)
            print('- your answer =', mdp.succAndProbReward(state, action))

        print('\n---------- Test c2 ----------')
        Espiar_tests = [
            ([((0, 0, (2, 2)), 0.5, -1), ((0, 1, (2, 2)), 0.5, -1)], mdp1, startState, 'Espiar'),
            ([((1 , None, (1, 2) ), 1, 0)] , mdp1, (0, 0, (2, 2)), 'Pegar'),
            ([], mdp1, postBustState, 'Espiar'),
            ]

        print('Espiaring Blackjack')
        for no, (answer, mdp, state, action) in enumerate(Espiar_tests):
            print('No %d'%(no+1), end=' ')
            if answer != mdp.succAndProbReward(state, action):
                print('=> wrong')
            else:
                print('=> right')
            print('- state: {}, action: {}'.format(state, action))
            print('- true answer =', answer)
            print('- your answer = ', mdp.succAndProbReward(state, action))

        print('\n---------- Test c3 ----------')
        algorithm = ValueIteration()
        algorithm.solve(mdp1)
        for s in algorithm.V:
            print('V(%s) = %f'%(s, algorithm.V[s]))
        print('------------')
        for s in algorithm.pi:
            print('pi(%s) = %s'%(s, algorithm.pi[s]))
        print('------------')
        print('Q1 (6, None, (1, 1) => %s'%(algorithm.pi[(6, None, (1, 1))]))
        print('Q2 (6, 0, (1, 1) => %s'%(algorithm.pi[(6, 0, (1, 1))]))

        print('\n========== Problem D ==========')
        mdp = util.NumberLineMDP()
        rl = QLearningAlgorithm(mdp.actions, mdp.discount(), identityFeatureExtractor, 0)

        # We call this here so that the stepSize will be 1
        rl.numIters = 1

        rl.incorporateFeedback(0, 1, 0, 1)
        print('Q-value for (state = 0, action = -1) : Answer %.1f, Output %.1f'%(0, rl.getQ(0, -1)))
        print('Q-value for (state = 0, action =  1) : Answer %.1f, Output %.1f'%(0, rl.getQ(0, 1)))

        rl.incorporateFeedback(1, 1, 1, 2)
        print('Q-value for (state = 0, action = -1) : Answer %.1f, Output %.1f'%(0, rl.getQ(0, -1)))
        print('Q-value for (state = 0, action =  1) : Answer %.1f, Output %.1f'%(0, rl.getQ(0, 1)))
        print('Q-value for (state = 1, action = -1) : Answer %.1f, Output %.1f'%(0, rl.getQ(1, -1)))
        print('Q-value for (state = 1, action =  1) : Answer %.1f, Output %.1f'%(1, rl.getQ(1, 1)))

        rl.incorporateFeedback(2, -1, 1, 1)
        print('Q-value for (state = 2, action = -1) : Answer %.1f, Output %.1f'%(1.9, rl.getQ(2, -1)))
        print('Q-value for (state = 2, action =  1) : Answer %.1f, Output %.1f'%(0, rl.getQ(2, 1)))

        print('\n========== Problem E ==========')
        # Small test case
        smallMDP = BlackjackMDP(valores_cartas=[1, 5], multiplicidade=2, limiar=10, custo_espiada=1)
        # compareQLandVI(smallMDP, identityFeatureExtractor)

        # Large test case
        largeMDP = BlackjackMDP(valores_cartas=[1, 3, 5, 8, 10], multiplicidade=3, limiar=40, custo_espiada=1)
        # compareQLandVI(largeMDP, identityFeatureExtractor)
        print('\n========== Problem F ==========')

        mdp = BlackjackMDP(valores_cartas=[1, 5], multiplicidade=2, limiar=10, custo_espiada=1)
        rl = QLearningAlgorithm(mdp.actions, mdp.discount(), blackjackFeatureExtractor, 0)

        # We call this here so that the stepSize will be 1
        rl.numIters = 1

        rl.incorporateFeedback((7, None, (0, 1)), 'Sair', 7, (7, None, None))
        print("Q-value for (state = (7, None, (0, 1)), action = 'Sair') : Answer %.1f, Output %.1f"%(28, rl.getQ((7, None, (0, 1)), 'Sair')))
        print("Q-value for (state = (7, None, (1, 0)), action = 'Sair') : Answer %.1f, Output %.1f"%(7, rl.getQ((7, None, (1, 0)), 'Sair')))
        print("Q-value for (state = (2, None, (0, 2)), action = 'Sair') : Answer %.1f, Output %.1f"%(14, rl.getQ((2, None, (0, 2)), 'Sair')))
        print("Q-value for (state = (2, None, (0, 2)), action = 'Pegar') : Answer %.1f, Output %.1f"%(0, rl.getQ((2, None, (0, 2)), 'Pegar')))

        # Large test case
        largeMDP = BlackjackMDP(valores_cartas=[1, 3, 5, 8, 10], multiplicidade=3, limiar=40, custo_espiada=1)
        compareQLandVI(largeMDP, blackjackFeatureExtractor)

    except NotImplementedError as err:
        # print err
        print("\nNotImplementedError: you didn't implement the function.")


if __name__ == '__main__':
    main()