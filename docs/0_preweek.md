# Preweek Technical Documentation

## Technical Goal
The technical goal of Preweek Explore is to determine how well do Agent Architectures fit our business use-case.

    What AI architecture should we be using?
    - An agent file with referenced files eg. AGENT.md, @~/docs/*.MD
    - Agent Skills driven by main agent eg. ~/.skills
    - Filesystem Subagent driven by a coding harness or Coding Agent SDK eg. ~/subagents
    - AI workflow automation platform eg. n8n
    - Use a generic AI Agent SDK that leverages plug and play generic AI packages
    - Use low level first party LLM SDKs and write our own agentic loop
    - Use REST APIs directly, write our own agentic loop
        - The agentic loop is model-driven orchestration with middleware programmatic guidance
        - The agentic loop is code driven orchestration

## Technical Uncertainty
- I am uncertain if a coding harnesses agentic loop is effective and productive enough to drive a non-coding workload.
- I am uncertain if LLM's reasoning mode and other model parameters are enough to maintain context, retain relevant memory, and make decisions for specific use cases.
- I am uncertain that a coding harnesses can interact with a MUD without an interface or SDK, particularly when managing a long telnet session.

## Technical Hypothesis
- I think that we will have issues with the coding harness driving the MUD without an interface because we don't have a defined API, we are driving commands over a protocol that we need to live monitor. Telnet communication seems like it would be a sticking point.

- I expect that we will need an interface because managing a long telnet sessions may prove difficult. This is the first time I attempt playing with Telnet sessions, so it is a still a learning curve to manage them correctly.

- I believe that only agent_architecture that will be able to drive our use case will be where we implement a specialized agentic loop, as I think generic model memory will not be capabale enough to remember and navigate the MUD world.

- I believe that we will need to build our own agent rather than rely on an SDK. Our requirements for observability, memory, session management and MUD specific behavior will likey require specialized implementation. We also want broad compatibility with models while many SDKs may not support every model or capability that we need.

## Technical Observations
- The AGENTS.md could not connect to the MUD. It was able to generate scripts but was unreliable when it came to creating a connection to the MUD. Furthermore, it needed knowledge of the deterministic text based interface of the MUD.
- Skills and Subagents performed better with a script that managed the telnet session. They were able to play the MUD, although not efficiently.


## Technical Conclusions
- Skills and Subagents are capable of operating the MUD.
- Specialized memory is required for map navigation, world state tracking, and persistent game data.
- We opened a new technical use case of it we should have our agent handle multiple sessions of multiple player, playing at the same time since co-op is a common factor in MUDs which we forgot to consider in our design.
- Implementing our own specialized loops remain technical uncertain and will need to be explored in depth in Week 2.
- Without a custommized agentic loop the agents could not perform goals efficiently. And did not have any keys meta strategies or journey player strategies.

## Key Takeaway
When we have a specialized use-case like playing a MUD, we likely cannot leverage generic SDKs because we need specialized tooling and agentic loops.