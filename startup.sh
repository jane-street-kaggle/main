echo "****************************************************"
echo "****                                            ****"
echo "****    ---- Starting the Kaggle Team ----      ****"
echo "****                                            ****"
echo "****************************************************"
echo "****                                            ****"
echo "****    Welcome to the Grand Kaggle Setup!      ****"
echo "****    Prepare for an Exciting Journey!        ****"
echo "****                                            ****"
echo "****************************************************"

git config --global user.email "bohblue23@gmail.com" && git config --global user.name "brian bae"
echo 'eval "$(ssh-agent -s)" && ssh-add ~/.ssh/enigma_ssh_key_rsa' >> ~/.bashrc

apt-get install vim -y
apt-get install htop -y
apt-get install unzip -y
apt-get install build-essential -y
# apt-get install nvidia-opencl-dev opencl-headers -y
pip install uv

echo "****************************************************"
echo "****                                            ****"
echo "****    ---- Please Press Enter 4 Times ----    ****"
echo "****                                            ****"
echo "****************************************************"

"${SHELL}" <(curl -L micro.mamba.pm/install.sh)

bash ./setup_micromamba.sh
bash ./setup_uv.sh

