# This file contains the options that you should modify to solve Question 2

# IMPORTANT NOTE:
# Comment your code explaining why you chose the values you chose.
# Uncommented code will be penalized.

def question2_1():
    #TODO: Choose options that would lead to the desired results 
    return {
        "noise": 0,
        "discount_factor": 1,
        "living_reward": -5
        #living reward is a big negative number to make the agent prefer the dangerous path over the safe path
        #also noise is 0 to make the environment deterministic so the agent always chooses the shortest path
    }


def question2_2():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.2,
        "discount_factor": 0.5,
        "living_reward": -1
         #living reward is a small negative number to make the agent prefer the safe path over the dangerous path
         #discount factor is 0.5 to make the agent choose the first small exit reward over the second large exit reward
        #noise is 0.2 to make the environment stochastic to make the agent choose the safe path
    }


def question2_3():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 1,
        "living_reward": -2
        #living reward is a big negative number to make the agent prefer the dangerous path over the safe path
        #also noise is 0 to make the environment deterministic so the agent always chooses the shortest path
        #discount factor is 1 to make the agent choose the far large exit reward over the near small exit reward
    }

def question2_4():
    #TODO: Choose options that would lead to the desired results
        return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -0.1
        #living reward is a small negative number to make the agent prefer the safe path over the dangerous path
        #noise is 0.2 to make the environment stochastic to make the agent choose the safe path
        #discount factor is 1 to make the agent choose the far large exit reward over the near small exit reward

    }

def question2_5():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 1,
        "living_reward": 5
        #living reward is a positive number to make the policy avoid any terminal state and keep the episode going on forever
         #also noise is 0 to make the environment deterministic

    }

def question2_6():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 1,
        "living_reward": -20
        #living reward is a big negative number to make the agent prefer any terminal state over the safe path
        #also noise is 0 to make the environment deterministic


    }
