Stateful REST API Fuzzer (Bachelor Thesis PoC)

📌 About

This project is a Proof-of-Concept stateful REST API fuzzer developed as part of my Bachelor's thesis.

The main goal is to automatically detect Broken Object Level Authorization (BOLA / IDOR) vulnerabilities in REST APIs.

Unlike most traditional DAST tools that test endpoints in isolation, this fuzzer tries to understand API logic and state, and then abuse it by replaying requests against resources belonging to other users.

This is a PoC, not a full-scale scanner. Some assumptions are made to keep the implementation simple.


🧠 Core Idea

The fuzzer works in three main steps:

Parse the OpenAPI specification to extract endpoints, HTTP methods and parameters.

Build a dependency graph (using NetworkX) that represents logical flows between endpoints
(e.g. create → read → update → delete).

Traverse the graph and execute stateful attacks, such as modifying or deleting resources owned by a different user.

The focus is specifically on authorization logic, not input validation or injection vulnerabilities.


🚀 Features

Automated OpenAPI parsing (openapi.json / yaml)

Endpoint dependency graph

Dynamic authentication handling
(automatic user registration and JWT extraction)

BOLA / IDOR detection
by replaying privileged requests against foreign resources

Execution logs and graph visualization

Some endpoints may require manual adjustment if the OpenAPI definition is incomplete or ambiguous.


🛠️ Tech Stack

Python 3.10+

NetworkX — dependency graph construction

Matplotlib — graph visualization

Requests — HTTP client

PyYAML — OpenAPI parsing


📂 Project Structure

main_fusion.py — entry point, orchestrates the scan

api_parser.py — downloads and parses OpenAPI specs

graph_builder.py — builds the endpoint dependency graph

traverser.py — attack engine, performs DFS traversal and BOLA tests

logger_config.py — centralized logging setup


⚡ Usage

Install dependencies:

pip install requests networkx matplotlib pyyaml


Run the fuzzer:

python main_fusion.py


By default, the tool targets a local vulnerable API instance (e.g. VAmPI) running on port 5000.


📊 Sample Output

When tested against the VAmPI testbed, the fuzzer was able to detect multiple authorization issues:

[CRITICAL] TOTAL VULNERABILITIES FOUND: 2
[CRITICAL] 1. [BOLA/IDOR] Email change allowed on /users/v1/hacker/email
[CRITICAL] 2. [BOLA/IDOR] Password change allowed on /users/v1/hacker/password


⚠️ Limitations

The dependency graph is heuristic-based and mainly focused on CRUD-style APIs.

Complex authorization models are not inferred automatically.

The tool is intended for academic and educational use only.

