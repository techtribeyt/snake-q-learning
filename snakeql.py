import numpy as np
import random
from snake_no_visual import LearnSnake
import pickle

class SnakeQAgent():
    def __init__(self):
        # define initial parameters
        self.discount_rate = 0.95
        self.learning_rate = 0.01
        self.eps = 1.0
        self.eps_discount = 0.9992
        self.min_eps = 0.001
        self.num_episodes = 10000
        self.table = np.zeros((2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4))
        self.env = LearnSnake()
        self.score = []
        self.survived = []
        
    # epsilon-greedy action choice
    def get_action(self, state):
        # select random action (exploration)
        if random.random() < self.eps:
            return random.choice([0, 1, 2, 3])
        
        # select best action (exploitation)
        return np.argmax(self.table[state])
    
    def train(self):
        for i in range(1, self.num_episodes + 1):
            self.env  = LearnSnake()
            steps_without_food = 0
            length = self.env.snake_length
            
            # print updates
            if i % 25 == 0:
                print(f"Episodes: {i}, score: {np.mean(self.score)}, survived: {np.mean(self.survived)}, eps: {self.eps}, lr: {self.learning_rate}")
                self.score = []
                self.survived = []
               
            # occasionally save latest model
            if (i < 500 and i % 10 == 0) or (i >= 500 and i < 1000 and i % 200 == 0) or (i >= 1000 and i % 500 == 0):
                with open(f'pickle/{i}.pickle', 'wb') as file:
                    pickle.dump(self.table, file)
                
            current_state = self.env.get_state()
            self.eps = max(self.eps * self.eps_discount, self.min_eps)
            done = False
            while not done:
                # choose action and take it
                action = self.get_action(current_state)
                new_state, reward, done = self.env.step(action)
                
                # Bellman Equation Update
                self.table[current_state][action] = (1 - self.learning_rate)\
                    * self.table[current_state][action] + self.learning_rate\
                    * (reward + self.discount_rate * max(self.table[new_state])) 
                current_state = new_state
                
                steps_without_food += 1
                if length != self.env.snake_length:
                    length = self.env.snake_length
                    steps_without_food = 0
                if steps_without_food == 1000:
                    # break out of loops
                    break
            
            # keep track of important metrics
            self.score.append(self.env.snake_length - 1)
            self.survived.append(self.env.survived)
        
        
