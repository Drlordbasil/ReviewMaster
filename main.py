import requests
from bs4 import BeautifulSoup
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import pandas as pd

class ECommerceReviewAnalyzer:
    def __init__(self, urls):
        self.urls = urls
        self.reviews = []

    def scrape_reviews(self):
        for url in self.urls:
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')

                reviews = soup.find_all('div', class_='review')
                for review in reviews:
                    rating = review.find('span', class_='rating').text
                    text = review.find('p', class_='review-text').text
                    date = review.find('span', class_='review-date').text

                    self.reviews.append({
                        'Rating': rating,
                        'Text': text,
                        'Date': date
                    })
            except requests.exceptions.RequestException as e:
                print(f"Error scraping reviews from {url}: {e}")

    def perform_sentiment_analysis(self):
        sid = SentimentIntensityAnalyzer()
        sentiment_scores = []

        for review in self.reviews:
            sentiment_score = sid.polarity_scores(review['Text'])
            sentiment_scores.append(sentiment_score['compound'])

        sentiment_df = pd.DataFrame({'Sentiment Score': sentiment_scores})
        sentiment_df['Sentiment'] = sentiment_df['Sentiment Score'].apply(
            lambda score: 'Positive' if score > 0 else 'Negative' if score < 0 else 'Neutral'
        )

        return sentiment_df

    def extract_keywords(self):
        keywords = {}
        for review in self.reviews:
            text = review['Text']
            words = text.split()

            for word in words:
                if len(word) > 2:
                    if word.lower() in keywords:
                        keywords[word.lower()] += 1
                    else:
                        keywords[word.lower()] = 1

        sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
        return sorted_keywords

    def visualize_sentiment_distribution(self, sentiment_df):
        sentiment_counts = sentiment_df['Sentiment'].value_counts()

        plt.bar(sentiment_counts.index, sentiment_counts.values)
        plt.xlabel('Sentiment')
        plt.ylabel('Count')
        plt.title('Sentiment Distribution')
        plt.show()

    def generate_report(self, sentiment_df, keywords):
        report = "E-commerce Review Analysis Report\n\n"
        report += "Sentiment Analysis:\n"
        sentiment_counts = sentiment_df['Sentiment'].value_counts()
        report += str(sentiment_counts) + "\n\n"

        report += "Top Keywords:\n"
        for keyword, count in keywords[:10]:
            report += f"{keyword}: {count}\n"

        return report


if __name__ == "__main__":
    urls = [
        "https://www.example-ecommerce.com/reviews",
        "https://www.another-ecommerce-website.com/reviews"
    ]

    analyzer = ECommerceReviewAnalyzer(urls)
    analyzer.scrape_reviews()
    sentiment_df = analyzer.perform_sentiment_analysis()
    keywords = analyzer.extract_keywords()

    analyzer.visualize_sentiment_distribution(sentiment_df)

    report = analyzer.generate_report(sentiment_df, keywords)
    print(report)