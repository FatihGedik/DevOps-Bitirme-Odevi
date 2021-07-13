# DevOps-Bitirme-Ödevi
TBB DevOps Uzmanlık Eğitimi Bitirme Ödevi

# FATİH GEDİK                    07.05.2021

Bu proje Türkiye Bankalar Birliği'nin düzenlemiş olduğu 42 gün süre boyunca Bilge Adam tarafından verilen DevOps Eğitim Programı bitirme projesidir.

# 1. Docker Install:
```
 $ sudo apt-get update
 
 $ sudo apt-get install \
      apt-transport-https \
      ca-certificates \
      curl \
      gnupg \
      lsb-release
      
 $ echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  
 $ sudo apt-get update
 $ sudo apt-get install docker-ce docker-ce-cli containerd.io
```

# 2. APP.PY Uygulamasının Dockerize Edilme Komutları:
  
```
docker build -t tbbpython .
docker volume create mysql_volume
docker network create -d bridge mynet
docker run --network=mynet -d -h=mydb --name=mydb -e MYSQL_ROOT_PASSWORD=12345 -p 3306:3306 -v mysql_volume:/var/lib/mysql mysql
docker run --network=mynet -d -h=myapp --name=myapp -p 5001:5001 tbbpython

```
# 3. HAProxy Kurulumu: 

```
apt-get update
apt-get upgrade -y
apt-get install haproxy
mv /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.org
vi /etc/haproxy/haproxy.cfg
```
[Haproxy.txt](https://github.com/FatihGedik/DevOps-Bitirme-Odevi/files/6806474/Haproxy.txt)

Haproxy.txt dosyasındaki konfigürasyonları uyarlayarak haproxy.cfg içine yapıştırıyoruz.
```
cd /etc/haproxy
haproxy -c -V -f haproxy.cfg
systemctl enable haproxy --now
shutdown -r now
```
# 4. Kubernetes Cluster Kurulumu:
```
sudo -i # change user to root
ssh-keygen  #select defaults values
ssh-copy-id ged2@192.168.1.105
git clone https://github.com/kubernetes-sigs/kubespray.git
cd kubespray
apt install python3-pip -y
pip3 install -r requirements.txt
cp -rfp inventory/sample inventory/mycluster

vi inventory/mycluster/inventory.ini
[all]
master ansible_host="192.168.1.105"
[kube_control_plane]
master ansible_host="192.168.1.105"
[etcd]
master ansible_host="192.168.1.105"
[kube_node]
master ansible_host="192.168.1.105"
[calico_rr]
[k8s_cluster:children]
kube_control_plane
kube_node
calico_rr

:wq
vi inventory/mycluster/group_vars/k8s_cluster/k8s-cluster.yml 
  kube_version: v1.20.4
  kube_network_plugin: 'weave'
:wq
vi inventory/mycluster/group_vars/k8s_cluster/addons.yml
helm_enabled: true
metrics_server_enabled: true
:wq
vi inventory/mycluster/group_vars/all/all.yml
## External LB example config
apiserver_loadbalancer_domain_name: "k8s.ged2.local"
loadbalancer_apiserver:
   address: 192.168.1.105
   port: 8543
:wq!
vi inventory/mycluster/group_vars/k8s_cluster/k8s-cluster.yml
cluster_name: ged2.local
:wq!
# declare -a IPS=(192.168.1.201 192.168.1.202 192.168.1.203)
declare -a IPS=(192.168.1.201)  
# Single node oldugundan asagidaki gibi
CONFIG_FILE=inventory/mycluster/hosts.yaml python3 contrib/inventory_builder/inventory.py $IPS
sed -i -e "s/node1/master/g" inventory/mycluster/hosts.yaml
ansible-playbook -i inventory/mycluster/hosts.yaml  --become -b -u ged2  cluster.yml -K
```
# 5. Jenkins Kurulumu:
```
sudo apt-get install openjdk-8-jdk
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt update
sudo apt upgrade
sudo apt install jenkins
sudo systemctl start jenkins
sudo ufw allow 8080
sudo ufw allow 22/tcp

sudo ufw status : Status: inactive ise
sudo ufw enable
sudo ufw default deny
sudo ufw allow 22/tcp
sudo ufw allow 8443/tcp
```
# Jenkins IP and Default Pasword
```
http://localhost:8080

cat /var/lib/jenkins/secrets/initialAdminPassword
```

# 6. Yapılan uygulamanın Deployment klasörleri aşağıdaki komutlar ile deploy edilmiştir. 
```
kubectl apply -f 
```
1. mysql-pv.yaml
2. mysql-pvc.yaml
3. mysql-secret.yaml
4. mysql-service.yaml
5. mysql-deploy.yaml
6. app-deployment.yaml
7. app-service.yaml

# 7. Zabbix Agent Kurulumu:
```
sudo wget https://repo.zabbix.com/zabbix/5.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_5.0-1+$(lsb_release -sc)_all.deb 
sudo dpkg -i zabbix-release_5.0-1+$(lsb_release -sc)_all.deb
sudo apt update
sudo apt-get install zabbix-agent -y
```
