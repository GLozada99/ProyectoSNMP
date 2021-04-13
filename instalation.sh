sudo apt install mariadb-server
sudo systemctl start mariadb.service
sudo apt install python3.7
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
pip install -Iv mariadb==1.0.6
pip install -Iv beautifultable==1.0.1
pip install -Iv RPi==0.0.1
pip install -Iv pyconcrete==0.12.1

echo $"export PATH=\$PATH:$(pwd)/Bash" >> ~/.bash_profile











