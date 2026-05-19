# main_fusion.py
from API_parser import APISchemeParser
from graph_builder import build_dependency_graph, visualize_graph
from traverser import AttackTraverser
from logger_config import log
import uuid
import random
import string
import requests

SPEC_URL = "https://raw.githubusercontent.com/erev0s/VAmPI/master/openapi_specs/openapi3.yml"
TARGET_HOST = "http://localhost:5000"

def ensure_victim_exists():
    try:
        requests.post(f"{TARGET_HOST}/users/v1/register", json={
            "username": "hacker", "password": "victim_pass", "email": "victim@test.com"
        })
    except:
        pass

def generate_random_creds():
    unique_id = uuid.uuid4().hex[:5]
    chars = string.ascii_letters + string.digits
    random_pass = ''.join(random.choice(chars) for _ in range(10))
    return {
        "username": f"user_{unique_id}",
        "password": random_pass,
        "email": f"test_{unique_id}@lab.com"
    }

def main():
    log.info("=== DIPLOMA: Stateful Fuzzer v1.0 (Final RC) ===")
    
    ensure_victim_exists()

    log.info("--- [PHASE 1] Static Analysis ---")
    parser = APISchemeParser(SPEC_URL)
    parser.fetch_spec()
    endpoints = parser.analyze_full_details()

    log.info("--- [PHASE 2] Logic Mapping ---")
    graph = build_dependency_graph(endpoints)

    log.info("--- [PHASE 3] Visualization ---")
    visualize_graph(graph)

    log.info("--- [PHASE 4] Attack Simulation ---")
    
    attacker_creds = generate_random_creds()
    log.info(f"[*] Generated dynamic attacker: {attacker_creds['username']}")

    attacker = AttackTraverser(graph, TARGET_HOST, attacker_creds)

    if attacker.login():
        start_nodes = [n for n in graph.nodes if "GET" in n and "{username}" in n]
        
        if start_nodes:
            attacker.run_dfs(start_nodes[0])
        else:
            log.warning("No suitable entry point found.")
    else:
        log.critical("Authentication failed.")

    log.info("\n" + "="*40)
    log.info("       SCANNING SUMMARY REPORT       ")
    log.info("="*40)
    if attacker.found_vulns:
        log.critical(f"TOTAL VULNERABILITIES FOUND: {len(attacker.found_vulns)}")
        for i, v in enumerate(attacker.found_vulns, 1):
            log.critical(f"{i}. {v}")
    else:
        log.info("No vulnerabilities found.")
    log.info("="*40)

if __name__ == "__main__":
    main()
