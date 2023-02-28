# sellorm's bin

Some small scripts and utilities that make sellorm's life easier.

## Installation

```bash
git clone https://github.com/sellorm/sellorm_bin.git ~/.bin
```

## Configuration

Add to your bash profile:

```bash
export PATH=~/.bin:~/.bin_packages:${PATH}
```

## packages

There's a package manager at `packages.py`. It's driven by the file `packages.json`.

The json file looks like this:

```
[
	{
		"repo": "https://github.com/sellorm/monotony.git",
		"command": "monotony"
	},
	{
		"repo": "https://github.com/sellorm/bashdown.git",
		"command": "bashdown"
	}
]
```

* `repo` is the URI of the git repo of the command line tool
* `command` is the command within the repo to link back to `~/.bin_profile`

