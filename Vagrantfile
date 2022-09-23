$script = <<-SCRIPT
  
  echo "-- Installing Docker..."
  sudo apt-get update
  sudo apt-get -y install apt-transport-https ca-certificates curl gnupg lsb-release resolvconf
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
  echo \ "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update
  sudo apt-get -y install docker-ce docker-ce-cli containerd.io
  sudo usermod -aG docker vagrant
  
  echo "-- Installing Docker Compose..."
  sudo curl -kL "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  
  echo "-- Installing Git..."
  sudo apt-get -y install git
  SCRIPT
  
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.provider "virtualbox" do |v|
    v.memory = 6128
    v.name = "birthday-api"
end

config.vm.provision "shell", inline: $script
  
# Sync folder
config.vm.synced_folder "C:\\Users\\jijz\\Documents\\gssacgms\\revolut-devops-test\\Birthday-API\\shared_folder", "/home/vagrant/shared_folder"
end
  