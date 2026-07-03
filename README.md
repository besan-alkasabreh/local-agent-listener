# Localhost Socket Lab

A simple Python project for practicing socket communication between two programs. The project includes:

- `listener_simple_server.py`: A local listener that waits on `127.0.0.1:4444` and sends commands.
- `agent_simple_client.py`: A client that connects to the listener and responds to a limited set of educational commands.

> Warning: This project is intended for learning in environments you own or have explicit permission to use. Do not run it on devices or networks without authorization.

## Requirements

- Python 3.8 or newer
- Windows, Linux, or macOS

No external packages are required. The project uses only Python's standard library.

## How To Run

Open two terminal windows inside the project folder.

In the first terminal, start the listener:

```bash
python listener_simple_server.py
```

In the second terminal, start the agent:

```bash
python agent_simple_client.py
```

After the connection is established, the listener will show this prompt:

```text
listener>
```

Type `help` to display the available commands.

## Supported Commands

| Command | Description |
| --- | --- |
| `help` | Show the command list |
| `ping` | Test the connection and return `PONG` |
| `time` | Show the current time on the agent machine |
| `whoami` | Show the current username |
| `sysinfo` | Show basic system and Python information |
| `pwd` | Show the current working directory inside the agent |
| `ls [path]` | List files in the current directory or a provided path |
| `cd <path>` | Change the agent's current working directory |
| `cat <file>` | Read a small text file, up to 8KB |
| `size <file>` | Show a file size in bytes |
| `mkdir <name>` | Create a folder inside the current directory |
| `history` | Show the last commands sent |
| `quit` | Close the session |


