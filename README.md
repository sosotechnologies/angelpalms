## I will use my image deployment and service for this demo
create an eks cluster using the terraform folder: EKS Cluster

authenticate the cluster

```
aws eks update-kubeconfig --region us-east-1 --name AngelPalms-Prod-eks-angelpalms
```

### angel-deploy.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: angels
  name: angels
  namespace: angelnamespace
spec:
  replicas: 1
  selector:
    matchLabels:
      app: angels
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: angels
    spec:
      containers:
      - image: sosotech/angelpalms:1.0.0
        name: angelpalms
        ports:
        - containerPort: 5000
        resources: {}
status: {}
```

### angel-svc.yaml

```
k expose deploy angels --name=angel-svc -n angelnamespace --port=5000 --target-port=5000 --type=ClusterIP --dry-run=client -o yaml > service.yaml
```

```yaml
apiVersion: v1
kind: Service
metadata:
  creationTimestamp: null
  labels:
    app: angels
  name: angel-svc
  namespace: angelnamespace
spec:
  ports:
  - port: 5000
    protocol: TCP
    targetPort: 5000
  selector:
    app: angels
  type: ClusterIP
status:
  loadBalancer: {}
```

***Apply deployment and service***

```
kubectl apply -f angel-deploy.yaml
kubectl apply -f angel-ser.yaml
```

### Install Istio using HelM

Check the helm url:[Helm Link](https://helm.sh/)
Check the istio url:[Istio Helm Link](https://istio.io/latest/docs/setup/install/helm/)

```
kubectl create ns istio-system
kubectl create ns angelnamespace
```

OPTIONAL - add jenkins, minio and Sonarqube charts

```
helm install jenkins jenkins/jenkins -n jenkins
```

```
kubectl create ns minio
helm search repo bitnami
helm install minio bitnami/minio -n minio
```

```
kubectl create ns sonarqube
helm install sonarqube bitnami/sonarqube -n sonarqube
```

```
helm repo ls
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update
helm search repo istio
helm ls -A
helm install istio-base istio/base -n istio-system
helm install istio-istiod istio/istiod -n istio-system
helm install istio-gateway istio/gateway -n istio-system
helm ls -A
kubectl get po -A
```



clone this repo: [TLS Yamls](https://github.com/sosotechnologies/sosokubernetes/tree/master/ssl-cert-istio-jenkins-minio-sonarqube)

***Get istio-ingressgateway deployment labels to add to the label area in below yaml***

```
kubectl get deploy -n istio-system
kubectl get deploy istio-gateway -n istio-system --show-labels
```

### gateway.yaml

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: general-gateway
  namespace: istio-system
  labels:
    app.kubernetes.io/instance: ingressgateway
    app: ingressgateway
    istio: ingressgateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - hosts:
    - '*'
    port:
      name: http
      number: 80
      protocol: HTTP
    # Upgrade HTTP to HTTPS
    tls:
      httpsRedirect: true
  - hosts:
    - '*'
    port:
      name: https
      number: 443
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: gateway-certs

      # app.kubernetes.io/managed-by=Helm
      # app.kubernetes.io/name=ingressgateway
      # app.kubernetes.io/version=1.16.1
      # app=ingressgateway
      # helm.sh/chart=gateway-1.16.1
      # istio=ingressgateway
```

### virtualservices.yaml

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  labels:
  name: angelpalms-vir-ser
  namespace: angelnamespace
spec:
  gateways:
  - istio-system/general-gateway     # This is the name and namespace from the gateway.yaml
  hosts:
  - 'angels.angelpalmshhcare.com'
  http:
  - retries:
      attempts: 3
      perTryTimeout: 2s
    match:
    - uri:
        prefix: /
    route:
    - destination:
        host: angel-svc.angelnamespace.svc.cluster.local    #first is angelpamls service name, second is namespace
        port:
          number: 5000
```

***Apply virtualservices.yaml and gateway.yaml***

```
kubectl apply -f virtualservices.yaml
kubectl apply -f gateway.yaml
```

## Create DNS Record - Mines in GoDaddy

- Get the LoadBalancer External-IP
- Since im using docker desktop, it will be: localhost

```
kubectl get service -A
```

![angels1](photos/angels1.png)

Add an A Record

![angels2](photos/angels2.png)

Add a TXT record
 - get the record from running the certbot command below
 - you will get  a record like so: _acme-challenge.angelpalmshhcare.com


![angels3](photos/angels3.png)

![angels4](photos/angels4.png)

![angels5](photos/angels5.png)

## Install certificate in ubuntu

```
sudo apt install certbot
sudo certbot certificates
```


***use this same command to generate and update cert***

```
sudo certbot certonly --manual -d *.angelpalmshhcare.com --agree-tos --manual-public-ip-logging-ok --preferred-challenges dns-01 --server https://acme-v02.api.letsencrypt.org/directory --email=macfenty@gmail.com --rsa-key-size 4096
```

***create a cert yaml [NOTE: Will not work until below chmod and chown commands are run]***

```
kubectl create secret tls gateway-certs --cert=/etc/letsencrypt/live/angelpalmshhcare.com/fullchain.pem --key=/etc/letsencrypt/live/angelpalmshhcare.com/privkey.pem -n istio-system --dry-run=client -o yaml > soso-tls-secret.yaml
```

change file permissions and ownership

```
sudo chown macazcol:macazcol /usr/bin/certbot -R
sudo chown macazcol:macazcol /var/log/letsencrypt/ -R
sudo chown macazcol:macazcol  /etc/letsencrypt/live/angelpalmshhcare.com/ -R

cd /etc/letsencrypt/live/angelpalmshhcare.com/ 
sudo chmod +x /etc/letsencrypt/live/angelpalmshhcare.com/
sudo chmod +x /etc/letsencrypt/archive
sudo chown macazcol:macazcol  /etc/letsencrypt/live -R
sudo chown macazcol:macazcol ../../archive/angelpalmshhcare.com/privkey1.pem*
```

cd space to return to home, before running the tls yaml dry-run

```
cd
```

***Now create a cert yaml***

```
kubectl create secret tls gateway-certs --cert=/etc/letsencrypt/live/angelpalmshhcare.com/fullchain.pem --key=/etc/letsencrypt/live/angelpalmshhcare.com/privkey.pem -n istio-system --dry-run=client -o yaml > soso-tls-secret.yaml
```

***NEXT: Note***

cat the tls file and go add the content in a new file in my istio-for-angelpalms folder

***Apply the secret to the cluster***

```
kubectl apply -f tls.yaml
k get vs -A
```

copy host and place in your url

[Thats all Folks!!!]



[OPTIONAL] delete the cert

```
sudo certbot delete --cert-name collins.com
```

### IT trainers
