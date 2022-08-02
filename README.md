# Python Scraping Project
## About
This app scraps the ladder data of Dofus players.
It can be slow to load since it scraps data from scratch every time.

## Starting with this project
Build image
```
docker build -t python-scrap .
```
Run container
```
docker run -p 8888:8080 python-scrap
```
