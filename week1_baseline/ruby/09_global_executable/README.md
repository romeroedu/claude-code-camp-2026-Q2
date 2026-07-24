# Step 8 — Global Executable

Package BOUKENSHA as a gem so the `boukensha` command works from anywhere on your machine.

## What this step adds

- `boukensha.gemspec` — declares the gem: name, version, which files to include, and the `bin/boukensha` executable
- `bin/boukensha` — the shebang script that becomes the global command
- `lib/boukensha_loader.rb` — resolves *which step folder* to load from, then boots the REPL
- `lib/boukensha.rb` + `lib/boukensha/` — step 7's lib, bundled as the default

## Install

```bash
cd 09_global_executable
gem build boukensha.gemspec
gem install boukensha-0.9.0.gem
```

After that, `boukensha` is on your `$PATH` and works from any directory.

## Switching steps and config with BOUKENSHA_PATH

The loader resolves the code path in this order:

| Priority | Source | Example |
|----------|--------|---------|
| 1 | `BOUKENSHA_PATH` env var | `BOUKENSHA_PATH=~/Sites/boukensha/07_the_repl_loop boukensha` |
| 2 | `~/.boukensharc` `boukensha_path` | `boukensha_path: ~/Sites/boukensha/07_the_repl_loop` |
| 3 | Bundled default | just run `boukensha` |

`BOUKENSHA_PATH` must point to a step folder that contains `lib/boukensha.rb`.

The config directory resolves separately:

| Priority | Source | Example |
|----------|--------|---------|
| 1 | `BOUKENSHA_DIR` env var | `BOUKENSHA_DIR=~/projects/mybot/.boukensha boukensha` |
| 2 | `~/.boukensharc` `boukensha_dir` | `boukensha_dir: ~/projects/mybot/.boukensha` |
| 3 | Default | `~/.boukensha` |

`~/.boukensharc` is YAML:

```yaml
boukensha_path: ~/Sites/boukensha/09_global_executable
boukensha_dir: ~/.boukensha
```

For compatibility, a `~/.boukensharc` file containing only a path is still treated as `boukensha_path`.

## Running a specific step

```bash
# step 7 (interactive REPL)
BOUKENSHA_PATH=~/Sites/boukensha/07_the_repl_loop boukensha

# step 6 doesn't have a REPL — loader tells you how to run it
BOUKENSHA_PATH=~/Sites/boukensha/06_the_run_dsl boukensha
# => boukensha: the step at .../06_the_run_dsl does not support the interactive REPL
#    Run its examples directly, e.g.: ruby .../06_the_run_dsl/examples/*.rb
```

## Debug mode

```bash
BOUKENSHA_DEBUG=1 boukensha
# => [boukensha] loading from: /path/to/step
```

## The key idea

The gem is just a **wrapper and a default**. All the teaching material stays in the numbered step folders exactly as it was. The gem doesn't copy or symlink anything — it just knows where to look.
