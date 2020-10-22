from google.cloud import language
from google.cloud.language import enums, types


def analyze_text_sentiment(text):
    client = language.LanguageServiceClient()
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    response = client.analyze_sentiment(document=document)

    sentiment = response.document_sentiment
    results = [
        ('text', text),
        ('score', sentiment.score),
        ('magnitude', sentiment.magnitude),
    ]
    for k, v in results:
        print('{:10}: {}'.format(k, v))


def analyze_text_entities(text):
    client = language.LanguageServiceClient()
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    response = client.analyze_entities(document=document)

    for entity in response.entities:
        print('=' * 79)
        results = [
            ('name', entity.name),
            ('type', enums.Entity.Type(entity.type).name),
            ('salience', entity.salience),
            ('wikipedia_url', entity.metadata.get('wikipedia_url', '-')),
            ('mid', entity.metadata.get('mid', '-')),
        ]
        for k, v in results:
            print('{:15}: {}'.format(k, v))

def analyze_text_syntax(text):
    client = language.LanguageServiceClient()
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    response = client.analyze_syntax(document=document)

    fmts = '{:10}: {}'
    print(fmts.format('sentences', len(response.sentences)))
    print(fmts.format('tokens', len(response.tokens)))
    for token in response.tokens:
        part_of_speech_tag = enums.PartOfSpeech.Tag(token.part_of_speech.tag)
        print(fmts.format(part_of_speech_tag.name, token.text.content))

def classify_text(text):
    client = language.LanguageServiceClient()
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    response = client.classify_text(document=document)

    for category in response.categories:
        print('=' * 79)
        print('category  : {}'.format(category.name))
        print('confidence: {:.0%}'.format(category.confidence))


if __name__ == "__main__":
    text = """
    roger federer è bravissimo
        """
    analyze_text_entities(text)