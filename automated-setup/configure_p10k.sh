#!/usr/bin/env bash

source functions.sh

line uncomment first "    # os_icon               # os identifier" in ~/.p10k.zsh
line add "    os_icon                 # os identifier" below "    # =========================[ Line #1 ]=========================" in ~/.p10k.zsh
line add "    # =========================[ Line #2 ]=========================" below "    vcs                     # git status" in ~/.p10k.zsh
line replace first "    # newline               # \n" with "    newline                 # \n" in ~/.p10k.zsh
line add "    newline                 # \n" below "    # prompt_char           # prompt symbol" in ~/.p10k.zsh
line add "    prompt_char             # prompt symbol" below "    newline                 # \n" in ~/.p10k.zsh
line comment first "    vi_mode                 # vi mode (you don't need this if you've enabled prompt_char)" in ~/.p10k.zsh
line comment first "    pyenv                   # python environment (https://github.com/pyenv/pyenv)" in ~/.p10k.zsh
line uncomment first "    # battery               # internal battery" in ~/.p10k.zsh
line add "  # Multiple Homebrews on Apple Silicon
  function prompt_show_arch() {
    if [ \"\$(arm64)\" = \"arm64\" ]; then
        architecture=\"arm64\"
    elif [ \"\$(arm64)\" = \"x86_64\" ]; then
        architecture=\"x86_64\"
    elif [ \"\$(arm64)\" = \"i386\" ]; then
        architecture=\"i386\"
    else
        architecture=\"x86\"
    fi
    p10k segment -b 2 -f 'black' -t \$architecture
  }
  # Time without seconds
  function prompt_show_time() {
    p10k segment -b 2 -f 'black' -i '' -t '%D{%H:%M}'
    # _p9k_prompt_segment \"\$0\" \"green\" \"\$_p9k_color1\" 'TIME_ICON' 0 '' \"%D{%H:%M}\"
  }
  # Modified dotnet_version
  function prompt_dotnet_ver() {
    if (( _POWERLEVEL9K_DOTNET_VERSION_PROJECT_ONLY )); then
      _p9k_upglob 'project.json|global.json|packet.dependencies|*.csproj|*.fsproj|*.xproj|*.sln' -. && return
    fi

    local cfg
    _p9k_upglob global.json -. || cfg=\$_p9k__parent_dirs[\$?]/global.json
    _p9k_cached_cmd 0 \"\$cfg\" dotnet --version || return
    # _p9k_prompt_segment \"\$0\" \"blue\" \"white\" 'DOTNET_ICON' 0 '' \"\$_p9k__ret\"
    p10k segment -b 7 -f 'black' -i '' -t \"\$_p9k__ret\"
  }
  # Modified pyenv
  function prompt_pyenv_ver() {
    _p9k_pyenv_compute || return
    p10k segment -b 7 -f 'black' -i '' -t \"\${_p9k__pyenv_version//\%/%%}\"
  }
  # Modified virtualenv
  function prompt_show_venv() {
    if [[ -n \$VIRTUAL_ENV ]]; then
      p10k segment -b 248 -f 'black' -i '' -t \"\${VIRTUAL_ENV##*/}\"
    fi
  }
" above "  # User-defined prompt segments may optionally provide an instant_prompt_* function. Its job" in ~/.p10k.zsh
line comment first "    virtualenv              # python virtual environment (https://docs.python.org/3/library/venv.html)" in ~/.p10k.zsh
line add "    show_venv               # python virtual environment (https://docs.python.org/3/library/venv.html)" below "    # virtualenv              # python virtual environment (https://docs.python.org/3/library/venv.html)" in ~/.p10k.zsh
line add "    show_arch               # custom architecture promt" above "    # example               # example user-defined segment (see prompt_example function below)" in ~/.p10k.zsh
line add "    pyenv_ver              # custom pyenv version promt" below "    # time                  # current time" in ~/.p10k.zsh
line add "    dotnet_ver             # custom dotnet version promt" below "    pyenv_ver              # custom pyenv version promt" in ~/.p10k.zsh
line add "    show_time               # custom time promt" below "    dotnet_ver             # custom dotnet version promt" in ~/.p10k.zsh
line replace first "  typeset -g POWERLEVEL9K_MODE=compatible" with "  typeset -g POWERLEVEL9K_MODE=nerdfont-complete" in ~/.p10k.zsh
line replace first "  typeset -g POWERLEVEL9K_PROMPT_ADD_NEWLINE=false" with "  typeset -g POWERLEVEL9K_PROMPT_ADD_NEWLINE=true" in ~/.p10k.zsh
line replace first "  typeset -g POWERLEVEL9K_MULTILINE_FIRST_PROMPT_PREFIX='%242F╭─'" with "  typeset -g POWERLEVEL9K_MULTILINE_FIRST_PROMPT_PREFIX=" in ~/.p10k.zsh
line replace first "  typeset -g POWERLEVEL9K_MULTILINE_NEWLINE_PROMPT_PREFIX='%242F├─'" with "  typeset -g POWERLEVEL9K_MULTILINE_NEWLINE_PROMPT_PREFIX=" in ~/.p10k.zsh
line replace first "  typeset -g POWERLEVEL9K_MULTILINE_LAST_PROMPT_PREFIX='%242F╰─'" with "  typeset -g POWERLEVEL9K_MULTILINE_LAST_PROMPT_PREFIX=" in ~/.p10k.zsh
line replace first "  typeset -g POWERLEVEL9K_MULTILINE_FIRST_PROMPT_SUFFIX='%242F─╮'" with "  typeset -g POWERLEVEL9K_MULTILINE_FIRST_PROMPT_SUFFIX=" in ~/.p10k.zsh
line replace first "  typeset -g POWERLEVEL9K_MULTILINE_NEWLINE_PROMPT_SUFFIX='%242F─┤'" with "  typeset -g POWERLEVEL9K_MULTILINE_NEWLINE_PROMPT_SUFFIX=" in ~/.p10k.zsh
line replace first "  typeset -g POWERLEVEL9K_MULTILINE_LAST_PROMPT_SUFFIX='%242F─╯'" with "  typeset -g POWERLEVEL9K_MULTILINE_LAST_PROMPT_SUFFIX=" in ~/.p10k.zsh
line replace first "  typeset -g POWERLEVEL9K_MULTILINE_FIRST_PROMPT_GAP_CHAR=' '" with "  typeset -g POWERLEVEL9K_MULTILINE_FIRST_PROMPT_GAP_CHAR='─'" in ~/.p10k.zsh
line replace first "  typeset -g POWERLEVEL9K_LEFT_SUBSEGMENT_SEPARATOR='\u2502'" with "  typeset -g POWERLEVEL9K_LEFT_SUBSEGMENT_SEPARATOR='\uE0B1'" in ~/.p10k.zsh
line replace first "  typeset -g POWERLEVEL9K_RIGHT_SUBSEGMENT_SEPARATOR='\u2502'" with "  typeset -g POWERLEVEL9K_RIGHT_SUBSEGMENT_SEPARATOR='\uE0B3'" in ~/.p10k.zsh
line replace first "  typeset -g POWERLEVEL9K_LEFT_SEGMENT_SEPARATOR=''" with "  typeset -g POWERLEVEL9K_LEFT_SEGMENT_SEPARATOR='\uE0B0'" in ~/.p10k.zsh
line replace first "  typeset -g POWERLEVEL9K_RIGHT_SEGMENT_SEPARATOR=''" with "  typeset -g POWERLEVEL9K_RIGHT_SEGMENT_SEPARATOR='\uE0B2'" in ~/.p10k.zsh
line replace first "  typeset -g POWERLEVEL9K_LEFT_PROMPT_LAST_SEGMENT_END_SYMBOL=''" with "  typeset -g POWERLEVEL9K_LEFT_PROMPT_LAST_SEGMENT_END_SYMBOL='\uE0B0'" in ~/.p10k.zsh
line replace first "  typeset -g POWERLEVEL9K_RIGHT_PROMPT_FIRST_SEGMENT_START_SYMBOL=''" with "  typeset -g POWERLEVEL9K_RIGHT_PROMPT_FIRST_SEGMENT_START_SYMBOL='\uE0B2'" in ~/.p10k.zsh
line replace first "  typeset -g POWERLEVEL9K_DIR_BACKGROUND=4" with "  typeset -g POWERLEVEL9K_DIR_BACKGROUND=0" in ~/.p10k.zsh
line replace first "  typeset -g POWERLEVEL9K_DIR_TRUNCATE_BEFORE_MARKER=true" with "  typeset -g POWERLEVEL9K_DIR_TRUNCATE_BEFORE_MARKER=false" in ~/.p10k.zsh
line replace first "  typeset -g POWERLEVEL9K_VCS_BRANCH_ICON=" with "  typeset -g POWERLEVEL9K_VCS_BRANCH_ICON='\uF126 '" in ~/.p10k.zsh
line replace first "  typeset -g POWERLEVEL9K_INSTANT_PROMPT=verbose" with "  typeset -g POWERLEVEL9K_INSTANT_PROMPT=quiet" in ~/.p10k.zsh
