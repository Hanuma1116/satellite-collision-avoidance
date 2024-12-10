# Train agent for collision at time 6600.

import argparse
import sys

import numpy as np
import pykep as pk

from space_navigator.api import MAX_FUEL_CONSUMPTION
from space_navigator.api import Environment
from space_navigator.models import ProgressPlotter
from space_navigator.models.ES import PytorchES
from space_navigator.utils import read_environment
from space_navigator.agent import convert_state_to_numpy

SIMULATION_STEP = 0.0001
ACTION_SIZE = 4


def main(args):
    parser = argparse.ArgumentParser()

    # train parameteres
    parser.add_argument("-n", "--n_actions", type=int,
                        default=1, required=False)
    parser.add_argument("-i", "--iterations", type=int,
                        default=10, required=False)
    parser.add_argument("-pop_size", "--population_size", type=int,
                        default=10, required=False)
    parser.add_argument("-lr", "--learning_rate", type=float,
                        default=0.1, required=False)
    parser.add_argument("-d", "--decay", type=float,
                        default=0.99, required=False)
    parser.add_argument("-sigma", "--sigma_coef", type=float,
                        default=0.1, required=False)

    # output parameteres
    parser.add_argument("-progress", "--show_progress", type=str,
                        default="False", required=False)
    parser.add_argument("-print", "--print_out", type=str,
                        default="False", required=False)
    parser.add_argument("-out", "--output_path", type=str,
                        default=".", required=False, help="Output folder for progress plots.")

    # simulation parameteres
    parser.add_argument("-save_path", "--save_model_path", type=str,
                        default="training/pytorch_models/PytorchES.pth", required=False)
    parser.add_argument("-env", "--environment", type=str,
                        default="data/environments/collision.env", required=False)
    parser.add_argument("-s", "--step", type=float,
                        default=SIMULATION_STEP, required=False)

    args = parser.parse_args(args)

    iterations = args.iterations
    population_size = args.population_size
    n_actions = args.n_actions
    learning_rate, decay, sigma_coef,  = args.learning_rate, args.decay, args.sigma_coef

    step = args.step
    model_path = args.save_model_path
    print_out = args.print_out.lower() == "true"
    show_progress = args.show_progress.lower() == "true"
    output_path = args.output_path

    # create environment
    env_path = args.environment
    env = read_environment(env_path)

    num_inputs = convert_state_to_numpy(env.get_state()).size
    num_outputs = ACTION_SIZE * n_actions
    hidden_size = 64

    model = PytorchES(env, step, num_inputs=num_inputs, num_outputs=num_outputs, hidden_size=hidden_size,
                      population_size=population_size, sigma=sigma_coef, learning_rate=learning_rate, decay=decay)
    model.train(iterations, print_out=print_out)
    model.save(model_path)

    if show_progress:
        plotter = ProgressPlotter(output_path, model)
        plotter.plot_all_rewards("training/ES/plots/pytorch_all_rewards.png")
        plotter.plot_mean_reward_per_iteration(
            "training/ES/plots/pytorch_mean_rewards.png")

    return


if __name__ == "__main__":
    main(sys.argv[1:])
