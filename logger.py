import os
import hashlib
from datetime import datetime

class IntegrityError(Exception):
    def __init__(self, message):
        super().__init__(message)

class ActionLogger:
    def __init__(self, log_file="action_log.txt"):
        self.log_file = log_file
        self.init_log()

    def init_log(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'a+') as log:
                genesis_entry = "GENESIS_ENTRY"
                genesis_hash = hashlib.sha256(genesis_entry.encode()).hexdigest()
                timestamp = datetime.now().isoformat()
                log.write(f"[{timestamp}] GENESIS {genesis_hash}\n")

    def log_action(self, action):
        with open(self.log_file, 'r') as log:
            last_line = log.readlines()[-1]

        last_hash = last_line.strip().split()[-1]
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {action}"
        log_hash = hashlib.sha256(f"{log_entry} {last_hash}".encode()).hexdigest()

        with open(self.log_file, 'a') as log:
            log.write(f"{log_entry} {log_hash}\n")

    def verify_genesis_log_integrity(self):
        genesis_entry = "GENESIS_ENTRY"
        if open(self.log_file, 'r').readline().strip().split()[-1] != hashlib.sha256(genesis_entry.encode()).hexdigest():
            raise IntegrityError(f"Log integrity failed: GENESIS_ENTRY")

    def verify_log_integrity(self):
        self.verify_genesis_log_integrity()
        with open(self.log_file, 'r') as log:
            lines = log.readlines()
            lines = [line.strip() for line in lines]

        for i in range(1, len(lines)):
            prev_line = lines[i - 1].strip()
            curr_line = lines[i].strip()

            prev_hash = prev_line.split()[-1]
            curr_entry = " ".join(curr_line.split()[:-1])
            curr_hash = curr_line.split()[-1]

            computed_hash = hashlib.sha256(f"{curr_entry} {prev_hash}".encode()).hexdigest()

            if computed_hash != curr_hash:
                raise IntegrityError(f"Log integrity failed: Line {i+1}")

        return True

    def print_logs(self):
        with open(self.log_file, 'r') as log:
            print("=== LOG START ===")
            for line in log:
                print(line.strip())
            print("=== LOG END ===")
