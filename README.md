# dirtydir

A command line tool for listing changed sub-directories compared to a defined
previous state. This can be used for only executing expensive operations 
on changed sub-directories while skipping unchanged ones.


## Usage

Initially, this will list all immediate sub-directories:

```
dirtydir ls
```

You can lock-down the contents of all sub-directories using

```
dirtydir lock --all
```

You will now get no output anymore when you run `dirtydir ls`.

As soon as you add, remove or change a file in a sub-directory, the sub-directory will be listed again.

If you want to lock a particular sub-directory, you can do that as well:

```
dirtydir lock somedir
```
