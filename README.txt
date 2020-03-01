################################################
##### NEUROEVOLUTION AGENT TRAINING SYSTEM #####
#####                                      #####
##### AUTHOR: ERYK PROKOPCZUK              #####
################################################

The program was coded on Python 3.6.8.
It is HIGHLY RECOMMENDED to run trainings which use OpenAI Gym
(all of included except the Xor one) on Linux operating system.
The package seemed to run a lot faster on Ubuntu than on Windows.

1. Prepare environment using Conda in terminal:
   a. conda create --name nevEnv
   b. conda activate nevEnv
   c. go to Neuroevolution folder
   d. pip install requirements.txt

2. Running options:
   a. New neuroevolution instance:

      python run_system.py [config_file_name]
      e.g.:
      python run_system.py config.json

   b. Resume neuroevolution from file:

      python run_system.py [config_file_name] resume [nev_file_name]
      e.g.:
      python run_system.py config.json resume nev123.pkl

   c. Run demo of agent from file:

      python run_system.py [config_file_name] demo [bestGenome_file_name]
      e.g.:
      python run_system.py config.json demo bestGenome123.pkl

3. Running example training:
   a. choose environment in "EXAMPLES" folder
   b. copy config file up to the Neuroevolution folder
   c. open terminal in Neuroevolution folder and run:

      python run_system.py [config_file_name]

4. Running agent demo:
   example agents are included for following environments:
   Xor, Pong, Lander
   a. choose one of the above environments from "EXAMPLES" folder
   b. copy config and bestGenome file up to Neuroevolution folder
   c. open terminal in Neuroevolution folder and run:

      python run_system.py [config_file_name] demo [bestGenome_file_name]

5. Estimated times for trainings

################################
#   CPU    #  2-core #  4-core #
#----------#---------#---------#
#   XOR    #    10s  #   6s    #
#----------#---------#---------#
#   PONG   #  2m-15m #  1m-8m  #
#----------#---------#---------#
# BREAKOUT # 1h-2.5h #0.5h-1.5h#
#----------#---------#---------#
#  LANDER  #    2h   #    1h   #
#----------#---------#---------#
# ATLANTIS # 12h-24h #  6h-12h #
################################
