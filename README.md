# Campus Lost & Found Board

A Flask web app to report lost/found items, search and filter them, edit or
delete entries, and mark them as claimed.

## Run locally
```
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Run tests
```
pytest
```

## Run with Docker (example: Person A)
```
docker build -f docker/Dockerfile.a -t lostfound-a .
docker run -p 5000:5000 lostfound-a
```

## Run on Kubernetes (example: Person A)
```
kubectl apply -f k8s/k8s-a.yaml
kubectl port-forward service/lostfound-a 5000:5000
```

## Team and process
Built by a 3-member team using Scrum in Jira (2 sprints), GitHub branching with
Pull Requests, pytest + Selenium tests, GitHub Actions CI, and Docker/Kubernetes.