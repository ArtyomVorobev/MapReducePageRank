# MapReducePageRank
Map Reduce Page Rank python implementation 

# To run page rank with docker: 

``docker build -t page_rank:latest . ``

``docker run --volume="$(pwd)/data:/data" page_rank:latest``