# What is goal for Week1?

We want to build a baseline agent that has all the common components for building any kind of agent. Things it should include:
- a simple agentic loop
- a tool registry along with tools
it should be able to handle multiple bakends
- it should be able to produce logs
- it should have a DSL so we can use the agent like an SDK
- it should have a global binary execution so we can interact via the CLI
- We should have an option CLI model
- it should manage context and compact messages when reaching out set limit
- it should have its own configuration directory

Some other things we should have:
- log visualizer so we can better view the logs in our browser

## What should the basline be able to do?
It should be able to play the MUD although we will have to give it specific commands.

## What will it not be able to do?
It will have poor perception since it does not have a way of managing memory, or decision making, or be token effective.

## Technical Design Considerations
- We will use REST APIs directly, this design chooice is so we are understanding how simple it is to interact with Managed APIs and how much they vary.
- Some SDKs even official ones do not expose all features and so REST APIs will give full access to feature sets
- We are using Ruby but the end user can port it over to another language
- We must use the Ruby MudManager to interact with MUD
- We should attempt to use the Standard Library (STDs) as much as possible and avoid introducing third party libraries

### What should we not use?
- We should avoid using Agent SDKs since they already implement features we are implementing by scratch they also might limit the ability to implment exactly what we need.
    - eg. Don't use OpenRouter, Don't use Amazon Strands or CoreAgent or LangChain
- We shouldn't be using the coding harness to drive the agent, since that is not purposed for our agent task

This is so you can:
- use the technical documentation and code references to generate out code in your preferred language and coding standards.
- easily understand each part added without having to navigate git history.

## Explain Structure Approach

The 'ruby/' folder contains each step-by-step iteration for our agent.

### Considerations
- We will need to make some manual adjustments since the original code did not exits in a Ruby sub-folder.
- AI affected the handwritten code so we will identify parts that should be rewritten but we may leave entact not to disturb future layers
- We can and will port the code over to Python, we will have to ensure the MudManager ruby version works with both Ruby and Python.

## Student Completion Approaches
As a student you have some flexibility in how you can get through this week:
- You can eactly follow along and make the ruby changes.
    - You can treat the ruby implementation as your main implementation.
- If you have no interest in the Python porting you can completely ignore those videos.
- You can watch all the videos and then do a single port of the last ruby interaction to your language of choice.
- You don't have to port the ruby but you'll have to use it in your Week 2 when we implement extra capabilities.

## Baseline Mud Agent

The baseline mud agent is a fully working MUD agent that can connect to a tbaMUD server, log in as a character, and control it through natural language.

** What the baseline gives you:**
- A persistent TCP session to the MUD server that stays connected across the agent's tool calls
    - Technically the MudManager is persisting the connection
- Five interchangeable LLM backends (Anthropic, OpenAI, Gemini, Ollama, Ollama Cloud) behind one normalized request/response shape, configured per-task in 'settings.yaml'
    - Andrew implements 5 backends, the student can use a single backend or multiple backends, it is up to them.
- MUD tools covering every core action: movement, combat, perception, inventory, magic, and communication
    - MudManager implements specific actions, but there are actions missing, eg. Thief commands, rest commands, the student needs to consider solving these at some point, In end of Week 1 or Week 2.
- A standard tool library for file I/O and shell commands so the agent can also read/write local state
    - These tools simply mirror the MudManager tools and likely need reworking which does occur in Week 1.
- A multi-turn REPL so you can have a back-and-forth conversation with the agent while it plays
- Full conversation history carried across turns so the agent remembers what it has seen and done
    - This is the sessions log files, but consider we can load previous conversations since we don't implement those feature in the Agent.
- Colored structured logging of every API call, tool dipatch, and response
    - Technically there is a bit of coloring, but the Web-browser provides more

** What it does not have yet ** (to be added in later iterations):
- Long term memory beyond the current conversation window
- A world model or map built from exploration
- Goal planning, tactical reasoning, or autonomous behavior
- Character progression tracking or strategy 


- For each of our steps often we wiull have a class for each eg. Configuration will have config, REPL will have repl.rb

### 0 Configuration

'Boukensha::Config' and ~/.boukensha directory stores all our configuration data including secrets, prompts, logging (aka sessions) and settings file.

'Boukensha::Config' - the single source of truth for all settings. Loads '~/.boukensha/' by default (override with 'BOUKENSHA_DIR'), Reads '.env' for secrets, 'settings.yaml' for options, and 'system.md' for the default system prompt.

We have an env var called BOUKENSHA_DIR that lets override its default location which is in the user's home directory.

We do use .dotenv standard for storinbg our secrets and we do need to include the dotenv library.

> If we are building an agent that can be deployed on multiple servers a configuration directory seems appropriate.


### 1 The Struct Skeleton

Define 'Boukensha::Tool', 'Boukensha::Message', and 'Boukensha::Context' as plain data containers. No logic yet, just the shapes.

We are defining the main data structures to pass around the data.

### 2 The Tool Registry

'Boukensha.tool' DSL method that registers a name + block. Add 'Boukensha.dispatch(name, args)' to call one. Runnable: register a fake tool and call it.

The Tool Registry is responsible for managing a data table of possible tools, and also dispatch tools when called. In other words it matches a prompt call to a an appropriate tool.

> We did discover that some point the AI regressed the implementation and Context is still responsible for managing tools which is not correct and the tools[] need to be moved to the Tool Registry.

### 3 The Prompt Builder

Since we are calling multiple backends via direct REST API requests, we need to know exactly their schema structure. So we need to build those expected structures.

We also need the prompt builder to normalize the responses into a single standard.

> We have to consider the thinking option models, some models have thinking turn on default where others do not, some cannot turn off thinking. There are other parameters we can fine tune, but we didn't much time exploring them in the video.

### 4 The API Client

The API Client is simply a low-level http-server making a direct API call to the REST API.

> We end up hardcoding the exact OpenSSL path, and this changes based on Windows, Mac or Linuc, a third party http-server like HTTPParty or Faraday would solve this but it will abstract more and make it harder to see the moving parts and we would have to take a library so we just fix the code for where we run it. 

### 5 The Agent Loop

`Boukensha::Agent` — the core agentic loop. Calls the API, checks `stop_reason`, dispatches tool calls back into the registry, appends results to the context, and repeats until `end_turn` or `MAX_ITERATIONS` is hit. Adds `Boukensha::Errors` (`LoopError`, `ApiError`) and wires everything together in `Boukensha.run`.

Also brings the OpenAI, Gemini, and Ollama Cloud backends online alongside Anthropic and Ollama — each implements `parse_response` to convert its raw reply into one normalized `{stop_reason:, content:}` shape so `Agent` never has to know which provider it's talking to.

> So we mentioned earlier we need to normalize the responses in the prompt backend, and so it occurs here. I believe we implement that normalization within the prompt builder and their backends.

### 6 The Logger

We create a logger which will record the logs of a session in `~/.boukensha/sessions/<date>-<session_id>.jsonl`.

> We have a `log_viz` app which is a simple Sinatra app to visualize the sessions. We should really, in the future, port it to TypeScript and have it update in real time.

We make sure we store exactly which model, which provider, and cost, trying to uplift as much information on each call for detailed reporting and also allowing us to mid-conversation switch agents (despite lacking commands to do so in the CLI).

### 7 The Run DSL

Up to the point we have multiple classes we need to create instances of and it becomes a mess of code, so we implement a single `.run` command to abstract away the complexity and give us an SDK-like interface to our agent.

`Boukensha::RunDSL` — the object `self` becomes inside a `Boukensha.run { }` block. Exposes a single `tool` method so callers can register ad-hoc tools inline alongside the task, keeping the DSL surface small and the main `Boukensha.run` signature clean.

### 8 The REPL Loop

It lets us have an interactive loop for the terminal.

`Boukensha::Repl` — an interactive session that stays alive across turns. Reads user input, runs the agent, prints the reply, and loops back to the prompt. A single `Context` is shared across all turns so the agent sees full conversation history. Built-in commands: `/quiet`, `/loud`, `/clear` (wipe history, keep tools), `/exit`, `/quit`, `/help`. Adds `Boukensha::VERSION`.

### 9 Global Executable

It lets us call `boukensha` anywhere in the terminal to start using our agent.

> Here we introduce a `.boukensharc`, which allows us to set the configuration path and the current gem path for the `boukensha` binary to load, and we end up having to carry that code into future steps.

Packages everything as an installable gem so the `boukensha` command is available anywhere on the machine. Adds `boukensha.gemspec`, `bin/boukensha`, and `lib/boukensha_loader.rb`. The loader resolves which step folder to use in priority order: `BOUKENSHA_PATH` environment variable → `~/.boukensharc` file → bundled default. `BOUKENSHA_DEBUG=1` prints the resolved path on startup.

```sh
cd 09_global_executable
gem build boukensha.gemspec
gem install boukensha-0.9.0.gem

BOUKENSHA_PATH=~/Sites/boukensha/09_global_executable boukensha
```

Each step from here on ships its own gem the same way (gem build boukensha.gemspec && gem install boukensha-<version>.gem) — point BOUKENSHA_PATH at whichever step folder you want to run.

> We skip this step for Python port, Not sure if that was a bad idea but we do that.

### 10 Standard Tool Library - MCP Host

We are implementing a mapping of tools for the agent from the MudManager.

However, when we went to port the code to Python, the Python app had no way of accessing the MudManager Ruby version, so we ended up implementing MCP.

> The MCP implementation is a 2-hour video and it's worth watching, but not doing. I would recommend copying over the MudManager and the `10_standard_tool_library` from the OmenKing repository.

> Also due to major code changes we end up having to carry forward code which makes the ruby step more involved.

### 11 Terminal UI

TUI is just a nicer REPL, so it has advanced display features within the terminal.

> We use Charm's Bubble Tea for the TUI in Ruby. AI thinks Bubble Tea is not available for Python, so it ends up using Textual. In all honesty, since we have the log visualization, we don't really need a TUI, but in my original implementation I implemented `log_viz` later.

### 12 Context Management

There is no auto-compacting when you call an LLM directly — you're responsible for the context window. This step adds proper token tracking, visual warnings, and automatic compaction on top of the MCP-host tool model and TUI carried forward from steps 10–11.

> There should be settings exposed to increase the 600 (e.g. 60,000) max token limit, as that is a very low amount. We never tested that in Week 1, but it can probably be adjusted.