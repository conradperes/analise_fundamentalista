cd /Users/conradperes/Documents/projects/analise_fundamentalista/k8s

kubectl apply -f influxdb-deployment.yaml
kubectl apply -f stock-analysis-deployment.yaml
kubectl apply -f stock-analysis-service.yaml