# DevOps-Bitirme-Ödevi
TBB DevOps Uzmanlık Eğitimi Bitirme Ödevi

# FATİH GEDİK                    07.05.2021

Bu proje Türkiye Bankalar Birliği'nin düzenlemiş olduğu 42 gün süre boyunca Bilge Adam tarafından verilen DevOps Eğitim Programı bitirme projesidir.

# 1. APP.PY uygulamasının dockerize edilme komutları aşağıda ki gibidir:
  
```
docker build -t tbbpython .
docker volume create mysql_volume
docker network create -d bridge mynet
docker run --network=mynet -d -h=mydb --name=mydb -e MYSQL_ROOT_PASSWORD=12345 -p 3306:3306 -v mysql_volume:/var/lib/mysql mysql
docker run --network=mynet -d -h=myapp --name=myapp -p 5001:5001 tbbpython

```





# 3. Yapılan uygulamanın Deployment klasörleri aşağıda ki gibidir: 
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
