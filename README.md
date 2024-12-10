On-orbit Satellite Collision Avoidance System

Overview

The On-orbit Satellite Collision Avoidance System is a comprehensive project designed to simulate, train, and execute collision avoidance strategies for satellites in orbit. Using advanced algorithms such as Monte Carlo Tree Search (MCTS), Evolution Strategies (ES), and others, this system provides a robust platform for mitigating the risks of satellite collisions in space.

Features

Collision Simulation: Simulate potential collision scenarios using realistic environment parameters.

Environment Generation: Dynamically generate collision scenarios with configurable debris count, start, and end times.

Model Training: Train collision avoidance models using various algorithms including:

Cross Entropy (CE)

Evolution Strategies (ES)

Baseline

Monte Carlo Tree Search (MCTS)

Collinear Grid Search (Collinear_GS)

Visualization: Web-based interface with interactive controls for running simulations and training models.

Satellite Movement Simulation: Visual representation of satellites and debris motion in a space-themed UI.

Installation

Clone the repository:

git clone https://github.com/HanuAkula/satellite-collision-avoidance.git
cd satellite-collision-avoidance

Set up a virtual environment:

python -m venv satellite_env
source satellite_env/bin/activate  # On Windows: satellite_env\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the Flask application:

python dashboard.py

Open the application in your browser:

http://127.0.0.1:5000

Usage

Web Interface

The system features an interactive web-based dashboard where you can:

Run test flights.

Simulate collision scenarios.

Generate new environments for testing.

Train various models with your choice of algorithm.

Execute simulations using trained models.
