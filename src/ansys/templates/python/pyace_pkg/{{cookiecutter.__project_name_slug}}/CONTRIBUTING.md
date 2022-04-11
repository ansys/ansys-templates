# Contributing to {{ cookiecutter.project_name }} project


## [Code of Conduct](...)


## Get Involved


### Join our Project Channel


### Triaging Issues and Pull Requests


## Our Development Process


### Branch Organization

## Proposing a Change


### Reporting New Issues

### Bugs


### Security Bugs


## Pull Requests


### Your First Pull Request


### Installation


### Online one-click setup for contributing


### Sending a Pull Request

#### Test Plan


#### Breaking Changes      

{% if cookiecutter.copyright != "None" -%}
        
#### Copyright Header for Source Code

Copy and paste this to the top of your new file(s):

```python
 # Copyright (c) {% now "utc", '%Y' %}, {{ cookiecutter.copyright }}. and its affiliates. Unauthorised use, distribution or duplication is prohibited
 # LICENSE file in the root directory of this source tree.
```

{% endif %}


### What Happens Next?

The core project team will be monitoring for pull requests. Do help us by keeping pull requests consistent by following the guidelines above.

## Style Guide


## Semantic Commit Messages

See how a minor change to your commit message style can make you a better programmer.

Format: `<type>(<scope>): <subject>`

`<scope>` is optional. If your change is specific to one/two packages, consider adding the scope. Scopes should be brief but recognizable, e.g. `content-docs`, `theme-classic`, `core`

The various types of commits:

- `feat`: a new API or behavior **for the end user**.
- `fix`: a bug fix **for the end user**.
- `docs`: a change to the website or other Markdown documents in our repo.
- `refactor`: a change to production code that leads to no behavior difference, e.g. splitting files, renaming internal variables, improving code style...
- `test`: adding missing tests, refactoring tests; no production code change.
- `chore`: upgrading dependencies, releasing new versions... Chores that are **regularly done** for maintenance purposes.
- `misc`: anything else that doesn't change production code, yet is not `test` or `chore`. e.g. updating GitHub actions workflow.

Do not get too stressed about PR titles, however. The maintainers will help you get them right, and we also have a PR label system that doesn't equate with the commit message types. Your code is more important than conventions!

### Example

```
feat(core): allow overriding of webpack config
^--^^----^  ^------------^
|   |       |
|   |       +-> Summary in present tense.
|   |
|   +-> The package(s) that this change affected.
|
+-------> Type: see below for the list we use.
```

Use lower case not title case!

## Code Conventions

### General


### Documentation

- Do not wrap lines at 100 characters - configure your editor to soft-wrap when editing documentation.

## License

By contributing to this project, you agree that your contributions will be licensed under its MIT license.
