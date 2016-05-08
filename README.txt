mkdir squid
cd squid
virtualenv .
. bin/activate
mkdir squid
cd squid
pip install -r requirements.txt
cd squid
scrapy crawl yahoo.AAPL -o items.json
less items.json