# from flask import Flask, Response, request
# import subprocess

# app = Flask(__name__)

# # Paths to scripts and files
# SIMULATION_SCRIPT = "examples/collision.py"
# TEST_FLIGHT_SCRIPT = "examples/test_flight.py"
# GENERATION_SCRIPT = "generation/generate_collision.py"
# DEFAULT_SAVE_PATH = "data/environments/generated_collision_5_debr.env"

# # Action table paths for training
# ACTION_TABLE_PATHS = {
#     "CE": "training/agents_tables/CE/action_table_CE_for_generated_collision_5_debr.csv",
#     "ES": "training/agents_tables/ES/action_table_ES_for_generated_collision_5_debr.csv",
#     "Baseline": "training/agents_tables/baseline/action_table_baseline_for_generated_collision_5_debr.csv",
#     "MCTS": "training/agents_tables/MCTS/action_table_MCTS_for_generated_collision_5_debr.csv",
#     "Collinear_GS": "training/agents_tables/collinear_GS/action_table_collinear_GS_for_generated_collision_5_debr.csv"
# }

# # Training script paths
# TRAIN_SCRIPTS = {
#     "CE": "training/CE/CE_train_for_collision.py",
#     "ES": "training/ES/ES_train_for_collision.py",
#     "Baseline": "training/baseline/baseline_train_for_collision.py",
#     "MCTS": "training/MCTS/MCTS_ahead_train_for_collision.py",
#     "Collinear_GS": "training/collinear_GS/collinear_GS_train_for_collision.py"
# }


# @app.route('/')
# def home():
#     return """
#     <h1>Satellite Collision Monitoring Dashboard</h1>
#     <button onclick="runTestFlight()">Run Test Flight</button>
#     <button onclick="runCollisionSimulation()">Run Collision Simulation</button>
#     <button onclick="showGenerateEnvironmentForm()">Generate Collision Environment</button>
#     <button onclick="showTrainModelDropdown()">Train Model</button>
#     <button onclick="runGeneratedSimulation()">Run Generated Simulation</button>
#     <div id="simulation-output" style="margin-top: 20px; white-space: pre-wrap; background: #f8f9fa; padding: 10px; border: 1px solid #ddd;"></div>
#     <div id="generate-environment-form" style="display: none; margin-top: 20px;">
#         <h2>Generate Collision Environment</h2>
#         <form onsubmit="generateEnvironment(event)">
#             <label>Number of Debris (Default: 5):</label><br>
#             <input type="number" id="numDebris" name="numDebris" value="5"><br><br>
#             <label>Collision Start Time (Default: 6601):</label><br>
#             <input type="number" id="startTime" name="startTime" value="6601"><br><br>
#             <label>Collision End Time (Default: 6601.1):</label><br>
#             <input type="number" id="endTime" name="endTime" value="6601.1"><br><br>
#             <button type="submit">Generate</button>
#         </form>
#     </div>
#     <div id="train-model-dropdown" style="display: none; margin-top: 20px;">
#         <h2>Select Training Model</h2>
#         <select id="trainingModel" name="trainingModel">
#             <option value="CE">Cross Entropy (CE)</option>
#             <option value="ES">Evolution Strategies (ES)</option>
#             <option value="Baseline">Baseline</option>
#             <option value="MCTS">Monte Carlo Tree Search (MCTS)</option>
#             <option value="Collinear_GS">Collinear Grid Search (Collinear_GS)</option>
#         </select>
#         <button onclick="trainModel()">Train</button>
#     </div>
#     <script>
#         function showGenerateEnvironmentForm() {
#             document.getElementById('generate-environment-form').style.display = 'block';
#         }
#         function showTrainModelDropdown() {
#             document.getElementById('train-model-dropdown').style.display = 'block';
#         }
#         async function runTestFlight() {
#             const response = await fetch('/run-test-flight');
#             const result = await response.text();
#             document.getElementById('simulation-output').innerText = result;
#         }
#         async function runCollisionSimulation() {
#             const response = await fetch('/run-collision-example');
#             const result = await response.text();
#             document.getElementById('simulation-output').innerText = result;
#         }
#         async function generateEnvironment(event) {
#             event.preventDefault();
#             const numDebris = document.getElementById('numDebris').value || 5;
#             const startTime = document.getElementById('startTime').value || 6601;
#             const endTime = document.getElementById('endTime').value || 6601.1;
#             const response = await fetch(`/generate-environment?n_d=${numDebris}&start=${startTime}&end=${endTime}`);
#             const result = await response.text();
#             document.getElementById('simulation-output').innerText = result;
#         }
#         async function trainModel() {
#             const selectedModel = document.getElementById('trainingModel').value;
#             const source = new EventSource(`/train-model?model=${selectedModel}`);
#             source.onmessage = function(event) {
#                 document.getElementById('simulation-output').innerHTML += `<pre>${event.data}</pre>`;
#             };
#             source.onerror = function() {
#                 source.close();
#             };
#         }
#         async function runGeneratedSimulation() {
#             const response = await fetch('/run-generated-simulation');
#             const result = await response.text();
#             document.getElementById('simulation-output').innerText = result;
#         }
#     </script>
#     """


# @app.route('/run-test-flight', methods=['GET'])
# def run_test_flight():
#     return execute_script(TEST_FLIGHT_SCRIPT, "Test Flight")


# @app.route('/run-collision-example', methods=['GET'])
# def run_collision_example():
#     return execute_script(SIMULATION_SCRIPT, "Collision Simulation")


# @app.route('/generate-environment', methods=['GET'])
# def generate_environment():
#     n_d = request.args.get('n_d', '5')
#     start = request.args.get('start', '6601')
#     end = request.args.get('end', '6601.1')
#     command = [
#         "python", GENERATION_SCRIPT,
#         "-save_path", DEFAULT_SAVE_PATH,
#         "-n_d", n_d,
#         "-start", start,
#         "-end", end,
#         "-before", "0.1"
#     ]
#     return execute_command(command, "Environment Generation")


# @app.route('/train-model', methods=['GET'])
# def train_model():
#     model = request.args.get('model', 'CE')
#     if model not in TRAIN_SCRIPTS:
#         return f"<pre>Invalid model: {model}</pre>"
#     script = TRAIN_SCRIPTS[model]
#     action_table = ACTION_TABLE_PATHS[model]
#     command = ["python", script, "--env", DEFAULT_SAVE_PATH, "--print", "True", "--save_action_table_path", action_table]
#     if model == "CE":
#         command.extend(["--r", "False", "--n_m", "1"])
#     elif model == "ES":
#         command.extend(["--n", "1", "--i", "10", "--population_size", "10", "--learning_rate", "0.1", "--d", "0.99", "--sigma_coef", "0.5", "--step", "0.000001", "--show_progress", "True", "--out", "training/ES/plots/"])
#     elif model == "Baseline":
#         command.extend(["--r", "False", "--n_s", "1"])
#     elif model == "MCTS":
#         command.extend(["--n_i", "200", "--n_s", "1", "--n_random_sessions_for_eval_action", "5"])
#     elif model == "Collinear_GS":
#         command.extend(["--n_s", "100", "--step", "0.000001", "--reverse", "True"])
#     return stream_output(command)


# @app.route('/run-generated-simulation', methods=['GET'])
# def run_generated_simulation():
#     model = request.args.get('model', 'CE')
#     command = ["python", SIMULATION_SCRIPT, "--env", DEFAULT_SAVE_PATH, "--model", ACTION_TABLE_PATHS.get(model, ACTION_TABLE_PATHS["CE"])]
#     return execute_command(command, "Generated Simulation")


# def execute_script(script, description):
#     command = ["python", script]
#     return execute_command(command, description)


# def execute_command(command, description):
#     try:
#         result = subprocess.run(
#             command,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             universal_newlines=True  # Replaces `text=True`
#         )
#         if result.returncode == 0:
#             return f"<pre>{description} completed successfully:\n\n{result.stdout}</pre>"
#         else:
#             return f"<pre>Error during {description}:\n\n{result.stderr}</pre>"
#     except Exception as e:
#         return f"<pre>An error occurred during {description}:\n{str(e)}</pre>"


# def stream_output(command):
#     def generate():
#         process = subprocess.Popen(
#             command,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.STDOUT,
#             universal_newlines=True  # Replaces `text=True`
#         )
#         for line in iter(process.stdout.readline, ''):
#             yield f"data: {line}\n\n"
#         process.stdout.close()
#         process.wait()
#     return Response(generate(), mimetype='text/event-stream')

# if __name__ == '__main__':
#     app.run(debug=True)





from flask import Flask, Response, request
import subprocess

app = Flask(__name__)

# Paths to scripts and files
SIMULATION_SCRIPT = "examples/collision.py"
TEST_FLIGHT_SCRIPT = "examples/test_flight.py"
GENERATION_SCRIPT = "generation/generate_collision.py"
DEFAULT_SAVE_PATH = "data/environments/generated_collision_5_debr.env"

# Action table paths for training
ACTION_TABLE_PATHS = {
    "CE": "training/agents_tables/CE/action_table_CE_for_generated_collision_5_debr.csv",
    "ES": "training/agents_tables/ES/action_table_ES_for_generated_collision_5_debr.csv",
    "Baseline": "training/agents_tables/baseline/action_table_baseline_for_generated_collision_5_debr.csv",
    "MCTS": "training/agents_tables/MCTS/action_table_MCTS_for_generated_collision_5_debr.csv",
    "Collinear_GS": "training/agents_tables/collinear_GS/action_table_collinear_GS_for_generated_collision_5_debr.csv"
}

# Training script paths
TRAIN_SCRIPTS = {
    "CE": "training/CE/CE_train_for_collision.py",
    "ES": "training/ES/ES_train_for_collision.py",
    "Baseline": "training/baseline/baseline_train_for_collision.py",
    "MCTS": "training/MCTS/MCTS_ahead_train_for_collision.py",
    "Collinear_GS": "training/collinear_GS/collinear_GS_train_for_collision.py"
}



@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>On-orbit Satellite Collision Avoidance System</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"></script>
        <style>
            body {
                background-image: url('https://images.unsplash.com/photo-1477176127572-39d4bfc217bc?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDF8fHNwYWNlfGVufDB8fHx8MTY4NjE5MjMwNQ&ixlib=rb-1.2.1&q=80&w=1920');
                background-size: cover;
                background-attachment: fixed;
                background-repeat: no-repeat;
                color: #f8f9fa;
            }
            .container {
                background: rgba(0, 0, 0, 0.8);
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
            }
            h1 {
                color: #ffd700;
            }
            button {
                font-size: 16px;
            }
        </style>
    </head>
    <body>
        <div class="container my-5">
            <h1 class="text-center mb-4">On-orbit Satellite Collision Avoidance System</h1>
            
            <div class="d-flex flex-wrap justify-content-center gap-3">
                <button class="btn btn-primary" onclick="runTestFlight()">Run Test Flight</button>
                <button class="btn btn-secondary" onclick="runCollisionSimulation()">Run Collision Simulation</button>
                <button class="btn btn-success" onclick="showGenerateEnvironmentForm()">Generate Collision Environment</button>
                <button class="btn btn-warning text-white" onclick="showTrainModelDropdown()">Train Model</button>
                <button class="btn btn-info text-white" onclick="runGeneratedSimulation()">Run Generated Simulation</button>
            </div>

            <div id="simulation-output" class="mt-4 p-3 border bg-white rounded" style="min-height: 100px; overflow-y: auto; color: #000;"></div>

            <div id="generate-environment-form" class="mt-4" style="display: none;">
                <div class="card">
                    <div class="card-header bg-success text-white">Generate Collision Environment</div>
                    <div class="card-body">
                        <form onsubmit="generateEnvironment(event)">
                            <div class="mb-3">
                                <label for="numDebris" class="form-label">Number of Debris (Default: 5):</label>
                                <input type="number" id="numDebris" name="numDebris" class="form-control" value="5">
                            </div>
                            <div class="mb-3">
                                <label for="startTime" class="form-label">Collision Start Time (Default: 6601):</label>
                                <input type="number" id="startTime" name="startTime" class="form-control" value="6601">
                            </div>
                            <div class="mb-3">
                                <label for="endTime" class="form-label">Collision End Time (Default: 6601.1):</label>
                                <input type="number" id="endTime" name="endTime" class="form-control" value="6601.1">
                            </div>
                            <button type="submit" class="btn btn-success">Generate</button>
                        </form>
                    </div>
                </div>
            </div>

            <div id="train-model-dropdown" class="mt-4" style="display: none;">
                <div class="card">
                    <div class="card-header bg-warning text-white">Select Training Model</div>
                    <div class="card-body">
                        <div class="mb-3">
                            <label for="trainingModel" class="form-label">Choose Model:</label>
                            <select id="trainingModel" name="trainingModel" class="form-select">
                                <option value="CE">Cross Entropy (CE)</option>
                                <option value="ES">Evolution Strategies (ES)</option>
                                <option value="Baseline">Baseline</option>
                                <option value="MCTS">Monte Carlo Tree Search (MCTS)</option>
                                <option value="Collinear_GS">Collinear Grid Search (Collinear_GS)</option>
                            </select>
                        </div>
                        <button class="btn btn-warning text-white" onclick="trainModel()">Train</button>
                    </div>
                </div>
            </div>
        </div>

        <script>
            function showGenerateEnvironmentForm() {
                document.getElementById('generate-environment-form').style.display = 'block';
            }
            function showTrainModelDropdown() {
                document.getElementById('train-model-dropdown').style.display = 'block';
            }
            async function runTestFlight() {
                const response = await fetch('/run-test-flight');
                const result = await response.text();
                document.getElementById('simulation-output').innerText = result;
            }
            async function runCollisionSimulation() {
                const response = await fetch('/run-collision-example');
                const result = await response.text();
                document.getElementById('simulation-output').innerText = result;
            }
            async function generateEnvironment(event) {
                event.preventDefault();
                const numDebris = document.getElementById('numDebris').value || 5;
                const startTime = document.getElementById('startTime').value || 6601;
                const endTime = document.getElementById('endTime').value || 6601.1;
                const response = await fetch(`/generate-environment?n_d=${numDebris}&start=${startTime}&end=${endTime}`);
                const result = await response.text();
                document.getElementById('simulation-output').innerText = result;
            }
            async function trainModel() {
                const selectedModel = document.getElementById('trainingModel').value;
                const source = new EventSource(`/train-model?model=${selectedModel}`);
                source.onmessage = function(event) {
                    document.getElementById('simulation-output').innerHTML += `<pre>${event.data}</pre>`;
                };
                source.onerror = function() {
                    source.close();
                };
            }
            async function runGeneratedSimulation() {
                const response = await fetch('/run-generated-simulation');
                const result = await response.text();
                document.getElementById('simulation-output').innerText = result;
            }
        </script>
    </body>
    </html>
    """




@app.route('/run-test-flight', methods=['GET'])
def run_test_flight():
    return execute_script(TEST_FLIGHT_SCRIPT, "Test Flight")


@app.route('/run-collision-example', methods=['GET'])
def run_collision_example():
    return execute_script(SIMULATION_SCRIPT, "Collision Simulation")


@app.route('/generate-environment', methods=['GET'])
def generate_environment():
    n_d = request.args.get('n_d', '5')
    start = request.args.get('start', '6601')
    end = request.args.get('end', '6601.1')
    command = [
        "python", GENERATION_SCRIPT,
        "-save_path", DEFAULT_SAVE_PATH,
        "-n_d", n_d,
        "-start", start,
        "-end", end,
        "-before", "0.1"
    ]
    return execute_command(command, "Environment Generation")


@app.route('/train-model', methods=['GET'])
def train_model():
    model = request.args.get('model', 'CE')
    if model not in TRAIN_SCRIPTS:
        return f"<pre>Invalid model: {model}</pre>"
    script = TRAIN_SCRIPTS[model]
    action_table = ACTION_TABLE_PATHS[model]
    command = ["python", script, "--env", DEFAULT_SAVE_PATH, "--print", "True", "--save_action_table_path", action_table]
    if model == "CE":
        command.extend(["--r", "False", "--n_m", "1"])
    elif model == "ES":
        command.extend(["--n", "1", "--i", "10", "--population_size", "10", "--learning_rate", "0.1", "--d", "0.99", "--sigma_coef", "0.5", "--step", "0.000001", "--show_progress", "True", "--out", "training/ES/plots/"])
    elif model == "Baseline":
        command.extend(["--r", "False", "--n_s", "1"])
    elif model == "MCTS":
        command.extend(["--n_i", "200", "--n_s", "1", "--n_random_sessions_for_eval_action", "5"])
    elif model == "Collinear_GS":
        command.extend(["--n_s", "100", "--step", "0.000001", "--reverse", "True"])
    return stream_output(command)


@app.route('/run-generated-simulation', methods=['GET'])
def run_generated_simulation():
    model = request.args.get('model', 'CE')
    command = ["python", SIMULATION_SCRIPT, "--env", DEFAULT_SAVE_PATH, "--model", ACTION_TABLE_PATHS.get(model, ACTION_TABLE_PATHS["CE"])]
    return execute_command(command, "Generated Simulation")


def execute_script(script, description):
    command = ["python", script]
    return execute_command(command, description)


def execute_command(command, description):
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True  # Replaces `text=True`
        )
        if result.returncode == 0:
            return f"<pre>{description} completed successfully:\n\n{result.stdout}</pre>"
        else:
            return f"<pre>Error during {description}:\n\n{result.stderr}</pre>"
    except Exception as e:
        return f"<pre>An error occurred during {description}:\n{str(e)}</pre>"


def stream_output(command):
    def generate():
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True  # Replaces `text=True`
        )
        for line in iter(process.stdout.readline, ''):
            yield f"data: {line}\n\n"
        process.stdout.close()
        process.wait()
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)