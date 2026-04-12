# Key FaralYar flows

## Conversion flow
`/` -> `/pricing/` -> `/accounts/signup/` or `/accounts/login/` -> `/billing/checkout/<slug>/` -> `/billing/verify/`

## OTP login flow
`/accounts/otp/` -> `/accounts/otp/verify/` -> `/chat/` or intended destination

## Chat flow
`/chat/` -> first prompt -> conversation creation -> `/chat/<conversation_id>/`

## Conversation management flow
`/chat/<conversation_id>/archive/`
`/chat/<conversation_id>/restore/`
`/chat/<conversation_id>/delete/`

## Personalization flow
`/accounts/personalization/` -> `/theme/` -> `/chat/`

## Admin business flow
`/dashboard/admin-panel/` -> models/plans/texts/settings/transactions