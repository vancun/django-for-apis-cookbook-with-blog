# django-for-apis-cookbook-with-blog
Django for APIs Cookbook with Blog Example

# Setup Python Project

```bash
mkdir blogapi
cd blogapi
```

Create `.gitignore`

You could use the [Github example](https://github.com/github/gitignore/blob/main/Python.gitignore), adding some more entries:

```
.venv*/
.dev*/
.vscode/
```

* The `.venv*/` entry allows us to create Python virtual environments within the project folder without getting them into the repository.
* The `.dev*/` entry allows us to have a sandbox directory within the project folder without getting it into the repository.
* The `.vscode/` entry makes sure that the VSCode workspace settings are not getting into the repository.

