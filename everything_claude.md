<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Give me real cases from hackathons with claude code that had an outstanding working folder with added skills, folder structures and a memory system setup

Here's the standout real-world case you're looking for:

## The "Everything Claude Code" Hackathon Winner

**Affaan Mustafa** entered an Anthropic × Forum Ventures hackathon, built a complete AI product called **Zenith Chat** in under a day, won, then open-sourced his entire Claude Code `.claude/` setup as [`everything-claude-code`](https://github.com/affaan-m/everything-claude-code). It hit **100K+ GitHub stars** and is widely considered the gold standard.[^1][^2]

## What's Inside the Folder

The repo is structured as a full "operating system" for AI-assisted development, not just a prompt pack:[^2]

- **27 specialized agents** — feature planning, architecture decisions, security reviews, build error resolution, Playwright E2E testing, code review[^3]
- **64 skills** — covering TDD, token optimization, memory persistence, and recurring workflow patterns[^3]
- **33 slash commands** — `/plan`, `/tdd`, `/security-scan`, `/refactor-clean`, etc.[^3]
- **Trigger-based hooks** — automate full workflow sequences[^2]
- **Prebuilt MCP configs** — GitHub, Supabase, Vercel, Railway connected out of the box[^2]


## Memory System

The memory architecture is layered and intentional:[^4]

- **Layer 1** — A single snapshot file capturing the current state of everything
- **Layer 2** — Daily session logs
- **Layer 3** — Full accumulated history

A separate community-refined pattern adds a `/session-context` skill (auto-prunes to 5 entries) and a `/wrap-up` devlog skill so Claude picks up exactly where you left off next session — no re-introduction needed.[^5]

## Continuous Learning System

One of its most unique features: it reads your **git history**, identifies coding patterns, and converts them into **new reusable skills** with confidence scoring. The system essentially improves itself from your own project history.[^2]

## Real-World Adoption

Kakao (the Korean tech giant) publicly documented adopting this recipe for their open-source `actionbase` project after their engineers used Claude Code (Opus 4.5) to solve a core engine issue in hours that would have taken a week manually. They forked and customized the `.claude/` config for their Kotlin/Java + Go stack.[^6]
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^29][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://www.augmentcode.com/learn/everything-claude-code-github

[^2]: https://www.reddit.com/r/techbootcamp/comments/1s1eaaw/sharing_this_anthropic_hackathon_winner_open/

[^3]: https://www.linkedin.com/posts/how-to-ai-guide_claude-code-setup-just-went-open-source-activity-7446164678457643009-wA5t

[^4]: https://www.reddit.com/r/ClaudeAI/comments/1s6v41a/the_agentic_frame_work_i_built_with_claude_got/

[^5]: https://www.instagram.com/reel/DWM97TEDP4z/

[^6]: https://github.com/kakao/actionbase/discussions/90

[^7]: https://www.instagram.com/reel/DWMPTvCDXcn/

[^8]: https://news.ycombinator.com/item?id=47543139

[^9]: https://www.tiktok.com/@codenameposhan/video/7613971308807834888

[^10]: https://www.reddit.com/r/ClaudeCode/comments/1sfynq3/how_do_you_structure_your_claude_code_projects/

[^11]: https://www.instagram.com/reel/DXrZAahCgsg/

[^12]: https://support.claude.com/en/articles/14116274-organize-your-tasks-with-projects-in-claude-cowork

[^13]: https://www.facebook.com/groups/1292754479356753/posts/1355283566437177/

[^14]: https://uxplanet.org/claude-code-project-structure-best-practices-5a9c3c97f121

[^15]: https://www.reddit.com/r/ClaudeAI/comments/1rfwmlh/how_i_structure_claude_code_projects_claudemd/

[^16]: https://www.youtube.com/watch?v=YtFf5ULb_Tw

[^17]: https://anthropic-usc-hackathon.devpost.com/project-gallery

[^18]: https://www.instagram.com/reel/DWb0Py5kxS0/

[^19]: https://github.com/affaan-m/ecc

[^20]: https://github.com/arabicapp/everything-claude-code

[^21]: https://blog.stackademic.com/build-your-first-claude-code-agent-skill-a-simple-project-memory-system-df5df7e3698d

[^22]: https://ai.sulat.com/the-claude-code-setup-that-won-a-hackathon-a75a161cd41c

[^23]: https://www.instagram.com/reel/DU-CkJLjTMP/?hl=en

[^24]: https://www.facebook.com/theaiempire/posts/complete-claude-code-configuration-collection-agents-skills-hooks-commands-rules/122154148862733053/

[^25]: https://github.com/FlorianBruniaux/claude-code-ultimate-guide/blob/main/docs/resource-evaluations/015-everything-claude-code-github-repo.md

[^26]: https://www.instagram.com/reel/DVClb42iFIT/

[^27]: https://www.facebook.com/techieprogrammer016/videos/everything-claude-code-github-repository-httpsgithubcomaffaan-meverything-claude/1332856312007721/

[^28]: https://skillsllm.com/skill/everything-claude-code

[^29]: https://github.com/ysyecust/everything-claude-code

