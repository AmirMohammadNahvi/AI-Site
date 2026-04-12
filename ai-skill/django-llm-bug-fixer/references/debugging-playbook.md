# Debugging playbook

## Common failure zones

### 1. Wrong provider selected
Causes:
- broken default logic
- inactive provider still used
- fallback logic ignores validation

### 2. API key/config mismatch
Causes:
- wrong credential reference
- missing env var
- admin config saved with incomplete fields

### 3. Serializer passes invalid options
Causes:
- provider-specific parameters not normalized
- missing bounds on max_tokens or temperature

### 4. Timeout/retry chaos
Causes:
- no timeout configured
- retry duplicates writes/logs/messages
- synchronous endpoint doing long provider call

### 5. Conversation state corruption
Causes:
- message save order issue
- race conditions with async tasks
- conversation id misuse