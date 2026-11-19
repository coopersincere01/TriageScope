#!/usr/bin/env bash
set -euo pipefail

# Deploy a tested image without immediately changing live traffic.
IMAGE="${1:?A Docker image URL is required}"
PROJECT="triagescope"
REGION="us-central1"
SERVICE="triagescope"
RUNTIME_ACCOUNT="168374564156-compute@developer.gserviceaccount.com"
LIVE_URL="https://triagescope-168374564156.us-central1.run.app"

service_details() {
  gcloud run services describe "$SERVICE" \
    --project="$PROJECT" --region="$REGION" --format=json
}

check_health() {
  curl --fail --silent --show-error \
    --retry 5 --retry-delay 3 --retry-all-errors \
    "$1/health" |
    python3 -c 'import json,sys; assert json.load(sys.stdin).get("status") == "ok"'
}

# Save the revision currently receiving all production traffic.
PREVIOUS_REVISION="$(
  service_details | python3 -c '
import json, sys
traffic = json.load(sys.stdin)["status"]["traffic"]
active = [item["revisionName"] for item in traffic
          if item.get("percent") == 100]
print(active[0] if len(active) == 1 else "")
'
)"

if [[ -z "$PREVIOUS_REVISION" ]]; then
  echo "Cannot determine the previous live revision safely."
  exit 1
fi

echo "Current production revision: $PREVIOUS_REVISION"

# Create a candidate revision with zero production traffic.
gcloud run deploy "$SERVICE" \
  --image="$IMAGE" \
  --project="$PROJECT" \
  --region="$REGION" \
  --service-account="$RUNTIME_ACCOUNT" \
  --no-traffic \
  --tag=candidate \
  --quiet

DETAILS="$(service_details)"

NEW_REVISION="$(
  printf '%s' "$DETAILS" |
    python3 -c '
import json, sys
status = json.load(sys.stdin)["status"]
matches = [item.get("revisionName") for item in status["traffic"]
           if item.get("tag") == "candidate"]
if (len(matches) != 1 or not matches[0]
        or matches[0] != status.get("latestReadyRevisionName")):
    sys.exit("Candidate revision is not ready or uniquely tagged")
print(matches[0])
'
)"

CANDIDATE_URL="$(
  printf '%s' "$DETAILS" |
    python3 -c '
import json, sys
traffic = json.load(sys.stdin)["status"]["traffic"]
print(next((item.get("url", "") for item in traffic
            if item.get("tag") == "candidate"), ""))
'
)"

if [[ -z "$NEW_REVISION" || -z "$CANDIDATE_URL" ]]; then
  echo "Cannot verify the candidate revision. Production traffic was not changed."
  exit 1
fi

echo "Testing candidate revision: $NEW_REVISION"
check_health "$CANDIDATE_URL"

# Promote only after the candidate health check succeeds.
gcloud run services update-traffic "$SERVICE" \
  --project="$PROJECT" \
  --region="$REGION" \
  --to-revisions="${NEW_REVISION}=100" \
  --quiet

if check_health "$LIVE_URL"; then
  echo "Deployment successful: $NEW_REVISION"
else
  echo "Production verification failed. Restoring $PREVIOUS_REVISION"
  gcloud run services update-traffic "$SERVICE" \
    --project="$PROJECT" \
    --region="$REGION" \
    --to-revisions="${PREVIOUS_REVISION}=100" \
    --quiet
  exit 1
fi
