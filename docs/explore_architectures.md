1. An agent file with reference files eg. AGENT.md, @~/docs/*.MD

Observations:
- Coding Harness will initially attempt to establish connection using telnet, needed to be corrected to using nc to establish connection. [Needed approval to connect]
- Coding Harness will update data/player.md abd data/world.md with information even though it was unable to complete task due to inability to connect.
- Initially had issues connecting to the session since I had not launched Docker. Thankfully, it explained what the issue was and provided solutions to resolving this.
- Coding Harness was able to connect after running docker compose up and was able to complete task gracefully and stopped as expected. [gpt-5.4-mini meidum]

- Increasing the model intelligence resulted in a faster completion time and achieved the goal as expected. It read and updated information within the data/player.md abd data/world.md files. It did stutter a bit when logging in since it said that there was another session active with the same character logged in, however, after some attempts it was able to login succesfully. [gpt-5.6-luna medium]