
#!/bin/bash
gcloud builds submit --tag gcr.io/agile-fort-454311-j6/bingx-app
gcloud run deploy bingx-app \
  --image gcr.io/agile-fort-454311-j6/bingx-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
