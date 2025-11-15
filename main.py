from flask import Flask, render_template, request
import feedparser
app = Flask(__name__)
RSS_FEEDS = {
    'Canada News': 'https://api.io.canada.ca/io-server/gc/news/en/v2?sort=publishedDate&orderBy=desc&publishedDate%3E=2021-10-25&pick=100&format=atom&atomtitle=National%20News',
    'Business News': 'https://api.io.canada.ca/io-server/gc/news/en/v2?audience=business&sort=publishedDate&orderBy=desc&publishedDate%3E=2021-10-25&pick=100&format=atom&atomtitle=business',
    'Dominic LeBlanc': 'https://api.io.canada.ca/io-server/gc/news/en/v2?minister=hondominicleblanc&sort=publishedDate&orderBy=desc&publishedDate%3E=2021-10-25&pick=100&format=atom&atomtitle=Hon.%20Dominic%20LeBlanc',
    'Evan Solomon': 'https://api.io.canada.ca/io-server/gc/news/en/v2?minister=honevansolomon&sort=publishedDate&orderBy=desc&publishedDate%3E=2021-10-25&pick=100&format=atom&atomtitle=Hon.%20Evan%20Solomon',
    'Jobs': 'https://api.io.canada.ca/io-server/gc/news/en/v2?topic=jobsandtheworkplace&sort=publishedDate&orderBy=desc&publishedDate%3E=2021-10-25&pick=100&format=atom&atomtitle=Jobs%20and%20the%20workplace',
    'Business': 'https://api.io.canada.ca/io-server/gc/news/en/v2?topic=businessandindustry&sort=publishedDate&orderBy=desc&publishedDate%3E=2021-10-25&pick=100&format=atom&atomtitle=Business%20and%20industry',
    'One Canadian Economy': 'https://api.io.canada.ca/io-server/gc/news/en/v2?dept=onecanadianeconomy&sort=publishedDate&orderBy=desc&publishedDate%3E=2021-10-25&pick=100&format=atom&atomtitle=One%20Canadian%20Economy%20',
    'Public Health Canada': 'https://api.io.canada.ca/io-server/gc/news/en/v2?dept=publichealthagencyofcanada&sort=publishedDate&orderBy=desc&publishedDate%3E=2021-07-23&pick=50&format=atom&atomtitle=Public%20Health%20Agency%20of%20Canada'
}
@app.route('/')
def index():
    articles = []
    for source, feed in RSS_FEEDS.items():
        parsed_feed = feedparser.parse(feed)
        entries = [(source, entry) for entry in parsed_feed.entries]
        articles.extend(entries)
    articles = sorted(articles, key=lambda x: x[1].updated_parsed, reverse=True)
    page = request.args.get('page', 1, type=int)
    per_page = 10
    total_articles = len(articles)
    start = (page-1) * per_page
    end = start + per_page
    paginated_articles = articles[start:end]
    return render_template('index.html', articles=paginated_articles, page=page, total_pages = total_articles // per_page + 1)
@app.route('/search')
def search():
    query = request.args.get('q')
    articles = []
    for source, feed in RSS_FEEDS.items():
        parsed_feed = feedparser.parse(feed)
        entries = [(source, entry) for entry in parsed_feed.entries]
        articles.extend(entries)
    results = [article for article in articles if query.lower() in article[1].title.lower()]
    return render_template('search_results.html', articles=results, query=query)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
