---
author: "Lewi Lie Uberg"
---

# Pyenv-win

To install the Python version you want to use in your project. For example, to install Python 3.10.5, run the following command:

```powershell
pyenv install 3.10.5
```

After it is installed navigate to the root of your project and run the following command to set the local Python version:

```powershell
pyenv local 3.10.5
```

A file named `.python-version` will be created in the root of your project. This file contains the Python version that will be used when you run the `python` command in your project.

Now, to test that the desired Python version is being used, run the following command:

```powershell
python --version
```

You should see the following output:

```powershell
Python 3.10.5
```
