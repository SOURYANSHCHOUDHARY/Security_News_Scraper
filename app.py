from scraper import get_articles, get_article_text
from parser import extract_iocs
from database import create_tables, insert_article, insert_ioc
from logger import logger


def main():

    # Create database tables
    create_tables()

    # Fetch articles from all RSS feeds
    articles = get_articles()

    logger.info(f"Fetched {len(articles)} articles from RSS feeds.")
    print(f"\nFound {len(articles)} articles.\n")

    # Process each article
    for i, article in enumerate(articles, start=1):

        print("=" * 80)
        print(f"[{i}/{len(articles)}] Processing Article")
        print("=" * 80)

        print(f"Source    : {article['source']}")
        print(f"Title     : {article['title']}")
        print(f"Published : {article['published']}")
        print(f"Link      : {article['link']}")

        logger.info(
            f"Processing article from {article['source']}: {article['title']}"
        )

        # Download article text
        text = get_article_text(article["link"])

        if not text:
            logger.error(
                f"Could not download article: {article['link']}"
            )
            print("❌ Could not download article.\n")
            continue

        print(f"Downloaded {len(text)} characters.")

        # Save article into database
        article_id = insert_article(
            article["source"],
            article["title"],
            article["published"],
            article["link"]
        )

        logger.info(f"Saved article: {article['title']}")

        # Extract IOCs
        iocs = extract_iocs(text)

        total_iocs = 0

        # Save IOCs
        for ioc_type, values in iocs.items():

            for value in values:

                insert_ioc(
                    article_id,
                    ioc_type,
                    value
                )

                total_iocs += 1

        logger.info(
            f"Saved {total_iocs} IOC(s) for article: {article['title']}"
        )

        print(f"Saved {total_iocs} IOC(s).\n")

    logger.info("Finished processing all RSS feeds.")
    print("\n✅ Finished processing all articles.")


if __name__ == "__main__":
    main()