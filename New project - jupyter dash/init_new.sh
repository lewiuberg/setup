#!/bin/zsh
HEADER="   _  __             ___             _         __\n  / |/ /__ _    __  / _ \_______    (_)__ ____/ /_\n /    / -_) |/|/ / / ___/ __/ _ \  / / -_) __/ __/\n/_/|_/\__/|__,__/ /_/  /_/  \___/_/ /\__/\__/\__/\n                               |___/              "
clear
echo -e $HEADER
echo ""

while true;
do
    read -r -p "Make new project? (y/n): " NEW
    if [[ $NEW =~ ^([yY])$ ]]
    then
        # -----------------------------------------------------------------------------
        # Install version
        # -----------------------------------------------------------------------------
        while true;
        do
            read -r -p "Install new Python version? (y/n): " INSTALL
            if [[ $INSTALL =~ ^([yY])$ ]]
            then
                while true;
                do
                    read -r -p "Select python version to install (3.8.6): " VERSION
                    echo "Version to install:" $VERSION
                    read -r -p "Is this correct? (y/n): " CORRECT
                    if [[ $CORRECT =~ ^([yY][eE][sS]|[yY])$ ]]
                    then
                        VENVVERSION=$VERSION
                        pyenv install $VENVVERSION
                        break
                    else
                        echo ""
                    fi
                done
                break
            elif [[ $INSTALL =~ ^([nN])$ ]]
            then
                # -----------------------------------------------------------------------------
                # Define virtual environment
                # -----------------------------------------------------------------------------
                while true;
                do
                    read -r -p "Select python version to use in environment (3.8.6): " VENVVERSION
                    echo "Version to use:" $VENVVERSION
                    read -r -p "Is this correct? (y/n): " CORRECT
                    if [[ $CORRECT =~ ^([yY][eE][sS]|[yY])$ ]]
                    then
                        break
                    else
                        echo ""
                    fi
                done
                break
            fi
        done
        echo ""
        echo "[STATUS] Python ready"
        echo ""
        
        while true;
        do
            read -r -p "Select name for environment (venv_name): " VENVNAME
            echo "Enviroment name:" $VENVNAME
            read -r -p "Is this correct? (y/n): " CORRECT
            if [[ $CORRECT =~ ^([yY][eE][sS]|[yY])$ ]]
            then
                break
            else
                echo ""
            fi
        done
        
        pyenv virtualenv $VENVVERSION $VENVNAME
        pyenv local $VENVNAME
        echo ""
        echo "[STATUS] Environment ready"
        echo ""
        break
    else
        break
    fi
done
# # -----------------------------------------------------------------------------
# # Pip Install
# # -----------------------------------------------------------------------------
while true;
do
    read -r -p "Install libraries with pip? (y/n): " LIB
    if [[ $LIB =~ ^([yY])$ ]]
    then
        pip install --upgrade pip
        pip install -r init_requirements.txt
        break
    else
        break
    fi
done

while true;
do
    read -r -p "Install Jupyter extensions? (y/n): " LIB
    if [[ $LIB =~ ^([yY])$ ]]
    then
        filename='init_jupyterlab_extensions.txt'
        # filename=$1
        while read line; do
            $line
        done < $filename
        jupyter lab build
        break
    else
        break
    fi
    
    cp gitignore .gitignore
    
done