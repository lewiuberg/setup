---
author: "Lewi Lie Uberg"
---

# Pyenv-win

[Pyenv-win][1] is a Python version management tool for Windows. It is a port of the popular [pyenv][2] tool for Unix-like systems. It allows you to easily switch between multiple versions of Python. It is simple, unobtrusive, and follows the UNIX tradition of single-purpose tools that do one thing well.

## Install Pyenv-win

To [install pyenv-win][3], open a PowerShell window as an **administrator** and run the following command:

```powershell
choco install pyenv-win -y
```

Add the system environment variables PYENV, PYENV_HOME and PYENV_ROOT to your Environment Variables by running the following commands in PowerShell:

```powershell
[System.Environment]::SetEnvironmentVariable('PYENV',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")

[System.Environment]::SetEnvironmentVariable('PYENV_ROOT',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")

[System.Environment]::SetEnvironmentVariable('PYENV_HOME',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")
```

Then add the paths to USER PATH to be able to use the commands. In PowerShell, run the following command:

```powershell
[System.Environment]::SetEnvironmentVariable('path', $env:USERPROFILE + "\.pyenv\pyenv-win\bin;" + $env:USERPROFILE + "\.pyenv\pyenv-win\shims;" + [System.Environment]::GetEnvironmentVariable('path', "User"),"User")
```

To enable pyenv-win to run scripts in PowerShell, run the following command:

```powershell
Set-ExecutionPolicy RemoteSigned
```

If you cant set the Execution Policy by running PowerShell as Administrator, you can set it under the current user scope by running the following command:[^1]

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

[1]: https://github.com/pyenv-win/pyenv-win
[2]: https://github.com/pyenv/pyenv
[3]: https://github.com/pyenv-win/pyenv-win/blob/master/docs/installation.md#chocolatey
