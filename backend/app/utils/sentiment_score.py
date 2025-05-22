from sqlmodel import Session, create_engine, text
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

# À adapter selon ta config
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
sia = SentimentIntensityAnalyzer()

BATCH_SIZE = 10000

with Session(engine) as session:
    offset = 0
    while True:
        # Récupère les commentaires sans score
        stmt = text(f"""
            SELECT id, comments
            FROM reviews
            WHERE comments IS NOT NULL AND (sentiment_score IS NULL OR sentiment_score = 0)
            LIMIT {BATCH_SIZE} OFFSET {offset}
        """)
        results = session.exec(stmt).all()
        if not results:
            break

        update_data = []
        for row in results:
            review_id = row[0]
            comment = row[1]
            score = sia.polarity_scores(comment)["compound"]
            update_data.append({'score': score, 'review_id': review_id})

        if update_data:
            update_stmt = text("""
                UPDATE reviews
                SET sentiment_score = :score
                WHERE id = :review_id
            """)
            session.execute(update_stmt, update_data)  # executemany

        session.commit()
        print(f"Traitement du batch à partir de l'offset {offset}")
        offset += BATCH_SIZE

print("Mise à jour terminée !")