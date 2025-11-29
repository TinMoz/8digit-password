# Repository Guidelines 
 
## Project Structure and Module Organization 
- Current contents: `README.md` with a project note; add app code under `src/` and shared utilities in `src/lib/`. 
- Place tests in `tests/` mirroring modules such as `src/auth/password.cs` to `tests/auth/password_tests.cs`. 
- Keep docs in `docs/` and small fixtures in `fixtures/` to avoid mixing with source. 
 
## Build, Test, and Development Commands 
- No build toolchain exists yet; choose a stack and document the command you add in `README.md` (examples: `dotnet build`, `npm run build`). 
- Run lint or format locally before opening a PR when a tool is introduced. 
- Expose helper scripts through `package.json`, `Makefile`, or `Justfile` for consistency. 
 
## Coding Style and Naming Conventions 
- Default to 2-space indentation for Markdown/JSON/YAML; follow language defaults elsewhere (4 spaces common in C#). 
- Use descriptive, lowercase-with-dashes filenames (`password-policy.md`); favor PascalCase for types and camelCase for functions and variables. 
- Keep functions small and explicit; prefer clear return types over implicit ones when it improves readability. 
- Run formatters such as `dotnet format` or `prettier` if their configs are added. 
 
## Testing Guidelines 
- Add unit tests alongside features; name files module_tests.ext and individual cases ShouldBehavior. 
- Use the framework native to the stack you pick (xUnit for .NET, vitest or jest for Node). 
- Cover critical flows: password generation, validation, entropy checks, and error handling. Document any new test command in `README.md`. 
 
## Commit and Pull Request Guidelines 
- Write concise, imperative commits (Add password generator, Tighten entropy check) and group related changes together. 
- Include a short PR description with intent, key changes, and how you tested; link issues when relevant. 
- Provide screenshots or terminal output for user-facing or CLI changes. Keep PRs scoped to a single concern. 
 
## Security and Configuration Tips 
- Do not commit secrets or sample passwords; rely on environment variables or a git-ignored `.env.local`. 
- Note defaults for password length and complexity in `README.md` whenever you change them, and validate entropy before merging.
