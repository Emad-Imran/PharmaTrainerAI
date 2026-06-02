# ML Recommendation Microservice

## Purpose

The ML Recommendation Service predicts the next suitable training level for a user.

The target levels are:

- Beginner
- Intermediate
- Advanced

The service is separated from the main application so that the machine learning logic can be updated independently.

---

## Model

The service uses:

```text
RandomForestClassifier