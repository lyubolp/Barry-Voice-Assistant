# Barry daemon examples

Start the daemon

```
sudo ./barryd.py start
```

Stop the daemon

```
sudo ./barryd.py stop
```

Set global configuration variable `location` = Bulgaria

```
./barryd.py config set location Bulgaria
```

Get global configuration variable `location`

```
./barryd.py config get location
```

Add script to be executed when given a phrase. phrase = `hello`, script = `../data/hello.sh`
```
./barryd.py add hello ../data/hello.sh
./barryd.py exec hello
```

Execute a script with arguments supplied on the console. All the arguments provided after the `phrase` to `exec` are passed to the script

```
./barryd.py add say ../data/say.sh
./barryd.py exec say "Hello there" ", General Kenobi"
```

Execute a script to check what user is executing it, even though the daemon is root

```
./barryd.py add "whoami" ../data/user.sh
./barryd.py exec "whoami"
```

Execute a script which uses global variables from the daemon. Here `:location:` is the global variable stored inside the daemon config, which the daemon will provide as first argument to the script when running it.

```
./barryd.py add "tell me the location" ../data/sayLocation.sh :location:
./barryd.py exec "tell me the location"
```

When executing a script with global variables and command line arguments the global variables are provided first and then the command line arguments are passed to the script
```
./barryd.py add "location and say" ../data/sayLocation\ and\ echo.sh :location:
./barryd.py exec "location and say" "HELLO FROM THE SCRIPT"
```

List all the available `phrases` with their `scripts` and `argsuments` in the form of JSON array of objects. The object key is the `phrase` while the value is an object with `script` and `args` fields.
```
./barryd.py list
```
