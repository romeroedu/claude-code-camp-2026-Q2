# Explore Agent Architectures

The largest confusion tech professionals have in applying the correct agent solution because many solutions appear to overlap responsibilities. We will explore multiple agent architectures to determine fit for our agent workload.

## 1. An agent file with reference files eg. AGENT.md, @~/docs/*.MD

The simplest agent is creating an "agent file" and possibly importing other files that are read conditionally when needed.

We should attempt to create an "agent file" and see if it can connect to the MUD and complete a simple goal: eg. "Find the bakery and list the menu".

We want to use the smallest and least intelligent model and scale up. In my case, I will be using the gpt-5.4-mini model at medium effort.

### Technical Observations

Using gpt-5.4-mini model at medium effort, I created a AGENTS.md with a simple prompt, and told it will need to manage its own local memory via simple markdown files. I provided it with the location of the MUD and the players credentials.

Coding Harness initially attempted to establish connection using telnet but, needed to be corrected to using nc to establish connection. [Needed approval to connect]
Coding Harness updated data/player.md abd data/world.md with information even though it was unable to complete task due to inability to connect.
Coding Harness initially had issues connecting to the session since I had not launched Docker. Thankfully, it explained what the issue was and provided solutions to resolving this.
Coding Harness was able to connect after running docker compose up and was able to complete task gracefully and stopped as expected. [gpt-5.4-mini meidum]

Increasing the model intelligence resulted in a faster completion time and achieved the goal as expected. It read and updated information within the data/player.md abd data/world.md files. It did stutter a bit when logging in since it said that there was another session active with the same character logged in, however, after some attempts it was able to login succesfully. [gpt-5.6-luna medium]

### Technical Conclusions

We could probably write a better prompt or create and artifact that would give the agent full knowledge of the MUD's Text User Interface to succesfully login, but since this experience is so fixed, it would be better to have a script that exactly knows how to login so we are not wasting token/usage and deterministic user flows.

Coding harnesses ten to go off task and try to write code which we do not need our agent to do. Coding harnesses at least at this specific architecture stage does not appear to be a good fit.

We are justified to build our own MUD SDK to connect to the MUD since clearly the agent wants to manage the connection via script and execute common commands over the port.

If we had an MCP server to our MUD SDJ then maybe we could drive the agent better at this architectural level.

I believe that due to the commplexity of the world and player state data, I simply do not think updating markdown files will be sufficient but we never concluded whether the current agentic loop of the coding harness could handle said task.

> Use coding harnesses for coding and make your own loop for specialized agents.