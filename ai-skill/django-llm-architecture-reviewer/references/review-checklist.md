# Review checklist

## Models
- are provider and model config entities separated clearly?
- is audit logging present?
- are active/default rules validated?

## Services
- is provider routing centralized?
- is response normalization centralized?
- are retries controlled?

## API
- are serializers explicit?
- are error shapes consistent?
- are permissions and throttles defined?

## Admin
- is unsafe config easy to create?
- are defaults/fallbacks understandable?

## Operations
- are timeouts configurable?
- is latency tracked?
- are token/cost metrics captured?