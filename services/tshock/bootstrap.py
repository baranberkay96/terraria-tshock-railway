"""Persistent, password-protected TShock launcher for Railway."""
import http.server
import json
import os
from pathlib import Path
import re
import secrets
import signal
import socket
import subprocess
import threading
import time


def warn(message):
    print(f"[tshock-template] {message}", flush=True)


def integer(env, name, default, low, high):
    try:
        value = int(env.get(name, str(default)))
        if low <= value <= high:
            return value
    except (ValueError, TypeError):
        pass
    warn(f"Invalid {name}; using {default}.")
    return default


def valid_password(value):
    return isinstance(value, str) and 16 <= len(value) <= 128 and all(32 <= ord(c) < 127 for c in value)


def prepare(data, env):
    for directory in ('tshock', 'worlds', 'plugins', 'tshock/logs', 'tshock/crashes'):
        (data / directory).mkdir(parents=True, exist_ok=True)
    config_path = data / 'tshock/config.json'
    config = {}
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text())
            if not isinstance(config, dict) or not isinstance(config.get('Settings', {}), dict):
                raise ValueError('Invalid object')
        except (ValueError, TypeError):
            config_path.rename(config_path.with_name(f'config.invalid-{time.time_ns()}.json'))
            warn('Invalid config preserved as config.invalid-*.json; restoring safe defaults.')
            config = {}
    settings = config.setdefault('Settings', {})
    password = env.get('SERVER_PASSWORD', '')
    if not valid_password(password):
        password = settings.get('ServerPassword', '')
        if valid_password(password):
            warn('Invalid SERVER_PASSWORD; retaining the persisted server password.')
        else:
            password = secrets.token_urlsafe(32)
            warn('Invalid SERVER_PASSWORD; access locked with an undisclosed random password. Set SERVER_PASSWORD to 16–128 printable ASCII characters and redeploy.')
    players = integer(env, 'MAX_PLAYERS', 8, 1, 32)
    settings.update(ServerPassword=password, ServerPort=7777, MaxSlots=players,
                    ReservedSlots=0, RestApiEnabled=False, DisableUUIDLogin=True,
                    DisableLoginBeforeJoin=True, AutoSave=True,
                    SaveWorldOnLastPlayerExit=True, SaveWorldOnCrash=True,
                    LogPath=str(data / 'tshock/logs'))
    temporary = config_path.with_suffix('.tmp')
    temporary.write_text(json.dumps(config, indent=2) + '\n')
    temporary.chmod(0o600)
    temporary.replace(config_path)
    name = env.get('WORLD_NAME', 'Railway')
    if not re.fullmatch(r'[A-Za-z0-9 _-]{1,40}', name):
        warn('Invalid WORLD_NAME; using Railway.')
        name = 'Railway'
    size = integer(env, 'WORLD_SIZE', 1, 1, 3)
    difficulty = integer(env, 'DIFFICULTY', 0, 0, 3)
    dedicated = data / 'serverconfig.txt'
    dedicated.write_text(f'world={data}/worlds/world.wld\nworldpath={data}/worlds\nworldname={name}\nautocreate={size}\ndifficulty={difficulty}\nmaxplayers={players}\nport=7777\nupnp=0\nsecure=1\nlanguage=en-US\n')
    dedicated.chmod(0o600)
    port = integer(env, 'PORT', 8080, 1024, 65535)
    if port == 7777:
        warn('PORT cannot use the game port; using 8080 for health checks.')
        port = 8080
    return port


def main():
    os.umask(0o077)
    data = Path('/data')
    port = prepare(data, os.environ)
    if os.getuid() == 0:
        for root, dirs, files in os.walk(data):
            os.chown(root, 10001, 10001)
            for name in dirs + files:
                os.chown(os.path.join(root, name), 10001, 10001, follow_symlinks=False)
        os.setgroups([])
        os.setgid(10001)
        os.setuid(10001)
    os.chdir('/opt/tshock')
    child = subprocess.Popen([
        './TShock.Server', '-config', '/data/serverconfig.txt',
        '-configpath', '/data/tshock', '-logpath', '/data/tshock/logs',
        '-crashdir', '/data/tshock/crashes', '-worldselectpath', '/data/worlds',
        '-additionalplugins', '/data/plugins', '-ip', '0.0.0.0', '-noupnp',
    ], stdin=subprocess.PIPE, text=True)
    stopping = threading.Event()

    def stop(_signum, _frame):
        stopping.set()

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)

    class Health(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            healthy = False
            if self.path == '/health' and child.poll() is None and not stopping.is_set():
                try:
                    with socket.create_connection(('127.0.0.1', 7777), timeout=1):
                        healthy = True
                except OSError:
                    pass
            self.send_response(200 if healthy else 503)
            self.end_headers()
            self.wfile.write(b'ready\n' if healthy else b'starting\n')

        def log_message(self, *_args):
            pass

    health = http.server.ThreadingHTTPServer(('0.0.0.0', port), Health)
    threading.Thread(target=health.serve_forever, daemon=True).start()
    warn('Starting TShock 6.2.1 / Terraria 1.4.5.8. Small worlds recommended; allow 1–2 GiB RAM. REST disabled; game TCP 7777.')
    while child.poll() is None and not stopping.wait(0.5):
        pass
    if child.poll() is None:
        warn('Saving world and stopping TShock.')
        try:
            child.stdin.write('exit\n')
            child.stdin.flush()
            child.wait(timeout=150)
        except (BrokenPipeError, subprocess.TimeoutExpired):
            child.kill()
            child.wait()
    health.shutdown()
    raise SystemExit(child.returncode)


if __name__ == '__main__':
    main()
