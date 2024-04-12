## Discord Connections Example
A simple example for [DiscordConnections package](https://github.com/imPDA/DiscordConnections).

### Features
- Containerized
- FastAPI based

### Usage
Copy repo, fill `.env` and run with `make run` command.

### Commands in `Makefile`
Build image with
```shell
make build 
```
Run app (also automatically runs `make logs`)
```shell
make up
```
Run app in attached mode
```shell
make up-a
```
Open logs (in _follow_ mode)
```shell
make logs
```
Down app
```shell
make down
```
Restart (=`make down && make up`)
```shell
make restart
```
Exec (shell)
```shell
make exec
```
