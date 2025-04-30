---
description:
globs:
alwaysApply: false
---
# Development Rules for Crypto Trading Bot

This document outlines the comprehensive development rules and guidelines for the Crypto Trading Bot project, designed to maintain code quality, project structure, and development efficiency.

### 🔄 Project Awareness & Context
- **Always run `task-master list`** at the start of a new conversation to see current tasks, their status, and dependencies.
- **Immediately after listing tasks, view the contents of `docs/NEXT_STEPS.md` and `docs/PROGRESS_LOG.md`** to understand the specific action planned at the end of the previous session.
- **Next, view the contents of `docs/STRATEGY_OVERVIEW.md` and `README.md`** to refresh understanding of the overall strategy and project goals.
- **Synthesize information**: Determine the current focus based on the highest priority *actionable* step from `NEXT_STEPS.md`, ensuring it aligns with an active or pending task from `task-master` and the overall context from the overview/readme files. If `NEXT_STEPS.md` is empty or outdated, refer to the highest priority pending task in `task-master`.
- **Check specific task details** with `task-master show <id>` before starting implementation if the next step involves a specific task ID.
- **Use `sequential-thinking` MCP to break down complex tasks** from `task-master` into smaller, manageable implementation steps *before* writing code. Generate a plan outlining the steps, required files, potential library usage, and tests.
- **Proactively use `context7` MCP (`resolve-library-id` then `get-library-docs`)** to fetch relevant documentation for key libraries (`vectorbtpro`, `pandas`, `fastapi`, `coinbase`, etc.) identified during the planning phase or when implementing features using them.
- **Search `docs/VectorBTDocumentation` when working with vectorbtpro** using Exa AI MCP to find specific implementation details, examples, and parameter explanations from the archived documentation.
- **Use consistent naming conventions, file structure, and architecture patterns** as shown in existing files and task details. Maintain awareness of existing modules using `find_by_name` or `list_dir` if unsure.

### 🗂️ Directory Structure & File Placement
- **Before creating any new file, verify the directory structure** using `find_by_name` or `list_dir` to confirm the appropriate location.
- **Always use absolute paths when creating files** to avoid ambiguity.
- **Verify import compatibility** by checking how similar files in the same directory structure import related modules.
- **When creating test files, examine existing test files in the project** for patterns of fixture usage and import structure.
- **Print the full file path after creation** so the user can verify the correct location.

### 🧱 Code Structure & Modularity
- **Never create a file longer than 500 lines of code.** If a file approaches this limit, use `sequential-thinking` to plan refactoring into smaller modules or helper files.
- **Limit functions to 50 lines maximum** to ensure readability and testability.
- **Follow PEP 8 style guidelines** for all Python code, including consistent indentation, naming conventions, and whitespace.
- **Use type hints** for all function parameters and return values to improve code clarity and IDE support.
- **Organize code into clearly separated modules**, grouped by feature or responsibility.
- **Use clear, consistent imports** (prefer relative imports within packages). Verify imports using `grep_search` if needed.
- **Use project-specific naming conventions**:
  - Indicator functions: `calculate_*` or `add_*`
  - Signal generators: `generate_*_signals`
  - Regime detection: `classify_*` or `detect_*`
  - Optimization functions: `optimize_*` or `run_*_optimization`

### 🛠️ Environment & Library Management
- **Automatically verify environment and library installations** at the start of any VectorBTpro-related task:
  ```python
  # Check conda environment and libraries
  !conda list -n vectorbtpro talib -v
  !conda list -n vectorbtpro vectorbtpro -v
  ```
- **Verify VectorBTpro API compatibility** before implementing any new features:
  ```python
  # In the vectorbtpro environment
  import vectorbtpro as vbt
  print(f"VectorBTpro version: {vbt.__version__}")
  # Check for specific API features that will be used
  ```
- **Document any VectorBTpro or TA-Lib API changes** in comments and implementation notes, including version-specific workarounds.
- **Always include fallback mechanisms** for any version-specific VectorBTpro features.

### 🔍 Strategy Research & Optimization
- **Use Exa AI MCP for strategy research** at the beginning of any new strategy implementation:
  ```
  # Research workflow
  1. Use `mcp3_web_search_exa` to search for "latest vectorbtpro trading strategies [current year]"
  2. Use `mcp3_web_search_exa` for "best technical indicators for [market type] markets"
  3. Use `mcp3_web_search_exa` to find "vectorbtpro optimization techniques for [strategy type]"
  4. Use `mcp3_research_paper_search` for academic validation of proposed techniques
  ```
- **Create evidence-based strategy selection** by comparing 3+ different approaches found in research.
- **Document all research findings** in `docs/research_notes/[strategy_name]_research.md`.
- **Always validate novel strategies** against standard benchmarks (buy-and-hold, SMA crossover).

### 🧪 Testing & Reliability
- **Always create Pytest unit tests for new features** as specified in each task's test strategy or planned during the `sequential-thinking` phase.
- **Use `sequential-thinking` to outline test cases** (expected use, edge cases, failure cases) *before* writing test code.
- **After updating any logic**, use `sequential-thinking` to explicitly review if existing unit tests need updates. If so, update them.
- **Tests should live in a `/tests` folder** mirroring the main app structure.
  - Include at least:
    - 1 test for expected use
    - 1 edge case
    - 1 failure case
- **Run tests frequently** using `run_command` (with conda environment prefix) after implementing features or fixing bugs.
- **Test strategies in both trending and ranging markets** to verify regime-aware functionality.
- **Add performance testing** for computationally intensive functions like signal generation and regime detection.
- **Implement quick test flags** for all major scripts to enable rapid verification during development.
- **Use synthetic data for initial validation** before testing with historical market data.

### ✅ Task Completion & Version Control
- **Use `github` MCP (`create_branch`)** to create a feature branch for each significant task or feature, ideally named after the task ID or a short descriptor (e.g., `feature/task-13-sd-zones`).
- **Mark tasks as in_progress** with `task-master set-status --id=<id> --status=in_progress` when starting work on the designated branch.
- **Commit changes regularly** using meaningful messages. Consider using `github` MCP (`create_or_update_file` or `push_files`) for commits, potentially summarizing `sequential-thinking` steps in the message.
- **Use `sequential-thinking` for self-review** of code changes against requirements, style guides (PEP8, docstrings), and planned tests before committing.
- **After implementation and testing are complete on the feature branch:**
    - **Use `github` MCP (`create_pull_request`)** to create a PR merging the feature branch into the main branch. Reference the `task-master` ID in the PR title/body.
    - **Optionally use `github` MCP (`create_pull_request_review`)** for a final AI review summary before merging (if applicable/desired).
    - **Merge the PR** (Manually or potentially using `github` MCP `merge_pull_request` if checks pass).
    - **Mark tasks as done** with `task-master set-status --id=<id> --status=done` *after* the PR is merged.
- **Add new subtasks** to `task-master` if implementation requires additional steps beyond the original plan, identified during the `sequential-thinking` process.
- **Automatically delete old/obsolete files** when refactoring or replacing functionality. Use `sequential-thinking` to identify files that are no longer needed (e.g., `.bak` files, superseded implementations, or unused test scripts).

### 🪵 Logging & Documentation
- **Update `docs/PROGRESS_LOG.md` automatically or semi-automatically.** Aim to use information from `task-master` updates (status changes) and GitHub events (PR creation/merge) to generate log entries. *This might require a custom script or further refinement of the workflow.* For now, prompt me to update it after marking a task done or merging a PR, summarizing the completed work.
- **Use structured log entries** with consistent sections: "Goal", "Improvements", "Issues Fixed", "Results & Observations", and "Next Steps".
- **Record all debugging insights** immediately when discovered in `PROGRESS_LOG.md`.
- **Maintain `docs/NEXT_STEPS.md` via `sequential-thinking`.** The output of the planning phase using `sequential-thinking` should define the immediate next steps. Prompt me to update `NEXT_STEPS.md` based on the finalized plan for the current task or after completing a task to outline the next priority.
- **Update `README.md`** when new features are added, dependencies change, or setup steps are modified, as identified during development or planning.
- **Write Google-style docstrings** for every function using the format:
  ```python
  def example():
      """
      Brief summary.

      Args:
          param1 (type): Description.

      Returns:
          type: Description.
      """
  ```
- **Comment non-obvious code** and ensure everything is understandable to a mid-level developer. Add inline `# Reason:` comments for complex logic.
- **Document strategy parameters** including acceptable ranges and impact on performance in both code comments and `STRATEGY_OVERVIEW.md`.
- **Maintain a "Lessons Learned" section** in `PROGRESS_LOG.md` to capture key insights.

### 📊 Session-Based Development
- **Start each day with defined session goals** - Document 2-3 specific objectives at the beginning of each development session in `PROGRESS_LOG.md`.
- **Use structured log entries** with consistent sections: "Goal", "Improvements", "Issues Fixed", "Results & Observations", and "Next Steps".
- **Record all debugging insights** immediately when discovered - patterns in debugging help solve similar issues later.
- **End every session by updating `NEXT_STEPS.md`** with the immediate next actions based on what you learned.
- **Compare key metrics before/after** changes to verify improvements and document the results.

### 🐛 Preemptive Error Prevention
- **Create validation checkpoints** after each major function change using quick test scripts.
- **Default safely** - Always implement fallback behavior (e.g., default to "ranging" when regime detection fails).
- **Use standard error handling patterns** consistently across the codebase, such as decorators for similar error types.
- **Add parameter validation** at function entry points to catch configuration errors early.
- **Test parameter edge cases** (e.g., empty dataframes, extreme values) before integrating new functions.
- **Never assume missing context. Ask questions or use tools (`codebase_search`, `view_file_outline`, `context7`) if uncertain.**
- **Never hallucinate libraries or functions.** Verify existence or usage patterns using `context7`, `exa`, `brave-search`, or codebase searching tools.
- **Always confirm file paths and module names** using `find_by_name` or `list_dir` before referencing them in code, tests, or commands.
- **Never delete or overwrite existing code** unless explicitly instructed to or as part of a planned refactoring step identified by `sequential-thinking` and approved.
- **Check task dependencies** using `task-master show <id>` before starting work.
- **Leverage `sequential-thinking` for error diagnosis.** If a command fails or tests don't pass, use `sequential-thinking` to analyze the error, form hypotheses, and plan debugging steps.

### 🔒 Trading Strategy & Risk Management
- **Implement multiple stop-loss mechanisms** for all strategies (fixed percentage, ATR-based, zone-based).
- **Add circuit breakers** to automatically halt trading when drawdown exceeds thresholds.
- **Require position sizing limits** based on account risk percentage, volatility, and regime.
- **Secure API credentials** using environment variables, never hardcode sensitive information.
- **Log all trade decisions** with rationale for forensic analysis.
- **Track robustness ratio** for all optimizations to detect overfitting.
- **Always test strategies in both trending and ranging markets** explicitly.
- **Verify regime detection accuracy** before testing regime-aware features.
- **Compare signal counts** across different modes as a quick validation (e.g., STRICT < BALANCED < RELAXED).

### 🛠️ Development Environment
- **Always use the `vectorbtpro` conda environment** when running scripts: `conda run -n vectorbtpro --no-capture-output --live-stream`.
- **When adding new dependencies** update both `requirements.txt` and document any conda-specific installations.
- **Test on multiple timeframes** (at least daily, 4h, 1h) before considering a feature complete.
- **Automate WFO parameter grid exploration** for any significant strategy change.
- **Implement incremental checkpointing** for long optimization runs to save progress.

