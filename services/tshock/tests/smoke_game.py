"""Real Terraria 1.4.5.8 password handshake against a Docker or Railway test."""
import os
import socket
import struct
import uuid


def net_string(value):
    encoded = value.encode('utf-8')
    size = len(encoded)
    prefix = bytearray()
    while size >= 128:
        prefix.append((size & 127) | 128)
        size >>= 7
    prefix.append(size)
    return bytes(prefix) + encoded


def send(sock, kind, payload):
    sock.sendall(struct.pack('<HB', len(payload) + 3, kind) + payload)


def exact(sock, count):
    result = b''
    while len(result) < count:
        chunk = sock.recv(count - len(result))
        if not chunk:
            raise RuntimeError('Connection closed before complete packet')
        result += chunk
    return result


def receive(sock):
    header = exact(sock, 3)
    length, kind = struct.unpack('<HB', header)
    return kind, exact(sock, length - 3)


def check(password, expected):
    address = (os.environ.get('GAME_TEST_HOST', '127.0.0.1'), int(os.environ.get('GAME_TEST_PORT', '17777')))
    with socket.create_connection(address, timeout=10) as sock:
        send(sock, 1, net_string('Terraria326'))
        kind, payload = receive(sock)
        assert kind == 3, f'Expected slot assignment, got {kind}'
        slot = payload[0]
        appearance = bytes([slot, 0, 0]) + struct.pack('<f', 0.0) + bytes([0]) + net_string('Probe' + uuid.uuid4().hex[:12]) + bytes(1 + 2 + 1 + 21 + 3)
        send(sock, 4, appearance)
        send(sock, 68, net_string('b74f6d0e-c244-43a6-b194-69e6830b4ca4'))
        send(sock, 6, b'')
        kind, payload = receive(sock)
        assert kind == 37, f'Expected password prompt (37), got {kind}: {payload!r}'
        send(sock, 38, net_string(password))
        kind, payload = receive(sock)
        assert kind == expected, f'Expected {expected}, got {kind}: {payload!r}'
        return kind


if __name__ == '__main__':
    assert check('incorrect-password-123456', 2) == 2
    print('Wrong password rejected with disconnect packet 2.')
    assert check('', 2) == 2
    print('Empty password rejected with disconnect packet 2.')
    assert check(os.environ['GAME_TEST_PASSWORD'], 7) == 7
    print('Correct password accepted with world information packet 7.')
