# Deploymenyt on K8s

## Kubectl

```bash
aws ecr get-login-password --region us-east-1 --profile xxx-xxx | docker login --username AWS --password-stdin xxxxxxx.dkr.ecr.us-east-1.amazonaws.com 

kubectl apply -f epsilla-deployment.yaml
kubectl apply -f lang-service-deployment.yaml
kubectl apply -f frontend-deployment.yaml

kubectl delete -f epsilla-deployment.yaml
kubectl delete -f lang-service-deployment.yaml
kubectl delete -f frontend-deployment.yaml

```
