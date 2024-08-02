# Setup Repository


Starting with new project folder:

```bash
mkdir blogapi
cd blogapi
```

### Create `.gitignore`

Create `.gitignore` file to tell git which files should not be maintained by the repository.

You could use the [Github example](https://github.com/github/gitignore/blob/main/Python.gitignore), adding some more entries:

```
.venv*/
.dev*/
.vscode/
```

* The `.venv*/` entry allows us to create Python virtual environments within the project folder without getting them into the repository.
* The `.dev*/` entry allows us to have a sandbox directory within the project folder without getting it into the repository.
* The `.vscode/` entry makes sure that the VSCode workspace settings are not getting into the repository.

### Create `LICENSE`

You could use [Choose an open source license](https://choosealicense.com/) to choose a license for your project.

### Create `README.md`

Create a `README.md` file for your project. To help you with getting started with README file, you could use ChatGPT with, for example, following prompt _How to write a README.md file for a GitHub Python project?_

There are also some great resources that might help you with creating readme for your project:

* [Creating a README file](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-on-github/creating-a-new-repository#creating-a-readme-file) GitHub guide
* [Making README Files Awesome](https://github.com/matiassingers/awesome-readme)

You could also give a try to readme generators:

* [README Generator](https://readme.so/)
* [Make a README](https://www.makeareadme.com/)
* [ChatGPT](https://chatgpt.com/) of course

I used following prompt with ChatGPT to get started:

> I am creating a python project - a blog api with Django Rest Freamework. The project is going to be used for training purposes and is providing recipes about completing various activities during the implementation of a typical API with Django Rest Framework. Documentation folder stores a book-like documentaiton. Each recipe has a github branch. Create a README.md file for the project.

### Setup the Project Folder as git Respository

For this recipe you need an empty remote repository. For example you could create one in GitHub.

Let's now initialize a git repository in the project folder:

```bash
git init
```

```bash
git init
# Commit current files
git add .
git commit -m "first commit"
# Tell git that we want our main branch to be main
git branch -M main
# Tell git what is the remote repsitory - put your repository url here
git remote add origin https://github.com/vancun/django-for-apis-cookbook-with-blog
# Publish the local changes
git push -u origin main
```
