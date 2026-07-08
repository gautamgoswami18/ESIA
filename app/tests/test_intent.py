from app.ai.intent_classifier import IntentClassifier

classifier = IntentClassifier()

print(
    classifier.classify(
        "Find Java developer with Kafka"
    )
)

print(
    classifier.classify(
        "Compare employee 1035 and 1042"
    )
)

print(
    classifier.classify(
        "Summarize employee 1035"
    )
)

print(
    classifier.classify(
        "Recommend training for employee 1035"
    )
)

print(
    classifier.classify(
        "Generate interview questions for employee 1035"
    )
)