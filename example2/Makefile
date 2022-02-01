run-local:
	python3 -m uvicorn server.main:app --reload

dummydb:
	docker run -d -p 27017:27017 --name mongodummy mongo 
