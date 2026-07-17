#!/usr/bin/env python3
"""Small socket client for the local MUD."""

from __future__ import annotations

import argparse
import socket
import select
import sys
from pathlib import Path

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 4000
DEFAULT_USERNAME = "player"
DEFAULT_PASSWORD = "helloworld"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Connect to the local MUD, log in, and run commands."
    )
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--username", default=DEFAULT_USERNAME)
    parser.add_argument("--password", default=DEFAULT_PASSWORD)
    parser.add_argument(
        "--command",
        action="append",
        default=[],
        help="Command to send after login. Repeat for multiple commands.",
    )
    parser.add_argument(
        "--command-file",
        help="File containing one command per line. Blank lines and # comments are ignored.",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Keep the session open after login and proxy stdin/stdout.",
    )
    parser.add_argument(
        "--connect-timeout",
        type=float,
        default=5.0,
        help="Socket connect timeout in seconds.",
    )
    parser.add_argument(
        "--idle-timeout",
        type=float,
        default=0.35,
        help="How long to wait for additional output before flushing a response.",
    )
    return parser.parse_args()


def load_command_file(path: str | None) -> list[str]:
    if not path:
        return []

    commands: list[str] = []
    for raw_line in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        commands.append(line)
    return commands


IAC = 255
DO = 253
DONT = 254
WILL = 251
WONT = 252
SB = 250
SE = 240


def process_incoming(data: bytes, sock: socket.socket) -> bytes:
    """Strip common Telnet negotiation bytes and respond best-effort."""
    out = bytearray()
    i = 0
    length = len(data)

    while i < length:
        byte = data[i]
        if byte != IAC:
            out.append(byte)
            i += 1
            continue

        if i + 1 >= length:
            break

        command = data[i + 1]
        if command == IAC:
            out.append(IAC)
            i += 2
            continue

        if command in {DO, DONT, WILL, WONT}:
            if i + 2 >= length:
                break
            option = data[i + 2]
            if command == WILL:
                sock.sendall(bytes([IAC, DONT, option]))
            elif command == DO:
                sock.sendall(bytes([IAC, WONT, option]))
            i += 3
            continue

        if command == SB:
            i += 2
            while i + 1 < length:
                if data[i] == IAC and data[i + 1] == SE:
                    i += 2
                    break
                i += 1
            continue

        i += 2

    return bytes(out)


def drain_output(sock: socket.socket, idle_timeout: float) -> bytes:
    chunks: list[bytes] = []
    while True:
        ready, _, _ = select.select([sock], [], [], idle_timeout)
        if not ready:
            break

        while True:
            data = sock.recv(4096)
            if not data:
                return b"".join(chunks)
            chunks.append(process_incoming(data, sock))
            ready, _, _ = select.select([sock], [], [], 0)
            if not ready:
                break

    return b"".join(chunks)


def write_output(data: bytes) -> None:
    if not data:
        return
    sys.stdout.write(data.decode("utf-8", errors="replace"))
    sys.stdout.flush()


def send_line(sock: socket.socket, text: str) -> None:
    sock.sendall((text.rstrip("\r\n") + "\n").encode("utf-8"))


def login(sock: socket.socket, username: str, password: str, idle_timeout: float) -> None:
    write_output(drain_output(sock, idle_timeout))
    send_line(sock, username)
    write_output(drain_output(sock, idle_timeout))
    send_line(sock, password)
    write_output(drain_output(sock, idle_timeout))


def run_commands(sock: socket.socket, commands: list[str], idle_timeout: float) -> None:
    for command in commands:
        send_line(sock, command)
        write_output(drain_output(sock, idle_timeout))


def interactive_session(sock: socket.socket, idle_timeout: float) -> None:
    while True:
        write_output(drain_output(sock, 0))

        readers = [sys.stdin, sock]
        ready, _, _ = select.select(readers, [], [], idle_timeout)
        if sys.stdin in ready:
            line = sys.stdin.readline()
            if line == "":
                return
            send_line(sock, line)
        if sock in ready:
            write_output(drain_output(sock, 0))


def main() -> int:
    args = parse_args()
    commands = args.command + load_command_file(args.command_file)

    try:
        sock = socket.create_connection((args.host, args.port), timeout=args.connect_timeout)
    except OSError as exc:
        print(f"Failed to connect to {args.host}:{args.port}: {exc}", file=sys.stderr)
        return 1

    try:
        login(sock, args.username, args.password, args.idle_timeout)
        if commands:
            run_commands(sock, commands, args.idle_timeout)
        if args.interactive:
            interactive_session(sock, args.idle_timeout)
        else:
            write_output(drain_output(sock, args.idle_timeout))
    finally:
        sock.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
