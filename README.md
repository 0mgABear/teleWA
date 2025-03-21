# Health Hack 2025

## Copyright & Licensing

© 2025 0mgABear and contributors. All rights reserved.

This code may only be used for **non-commercial** purposes. You are not allowed to use, modify, or distribute the code for commercial purposes unless you obtain written permission from the copyright holders, including the individual contributors.

## Contributors

- [0mgABear](https://github.com/0mgABear)
- [Jooerny](https://github.com/Jooerny)

# Project Background

1. Observed Behaviour: Older generation have an existing habit / behaviour of forwarding WhatsApp messages to each other as a means to spread and disseminate information.
2. Some insignificant part of these messages tend to be health-related.
3. Some of these messages could be misinformation such as unproven cures and/or medicine and/or remedies.
   Sources:
   - a. https://www.channelnewsasia.com/commentary/covid-19-coronavirus-forwarding-whatsapp-message-fake-news-766406
   - b. https://www.sciencedirect.com/science/article/pii/S0213911120301953
   - c. https://www.unicef.org/guineabissau/press-releases/unicef-alerts-spreading-false-messages-increase-risk-misinformation-about-corona
   - d. https://pmc.ncbi.nlm.nih.gov/articles/PMC8590927/
   - e. https://www.straitstimes.com/singapore/pandemic-of-online-misinformation-on-covid-19-takes-its-toll
4. This is not a problem confined to Singapore, but presents a serious public health problem for healthcare providers and for MOH.

# Problem Statement:

The widespread habit of forwarding misinformation—such as unverified medical advice and unproven remedies—can mislead recipients and result in potentially harmful health decisions.
For healthcare providers and local authorities (MOH), combating misinformation is a top priority, as it can create unnecessary fear and significantly hinder efforts to disseminate accurate medical information and guidance to the public.

# Proposed Solution:

Since MOH already has a Telegram Channel, whatever message is disseminated there, it can be automatically forward to a MOH WhatsApp Channel / mailing list.

## First Iteration:

Proof-of-concept to retrieve data from Telegram API - working. ✅

## Second Iteration :

Proof-of-concept to demonstrate ability to forward messages wholesale (full messages) - working. ✅

19.02.2025
Minor updates to code to include flexibility for telegram username. - working. ✅

## Third Iteration:

Elucidating project background and problem statement. - Done. ✅

## Fourth Iteration:

Proof-of-concept to connect to Whatsapp API and forward the message directly from Telegram to Whatsapp. - working. ✅

However, there are the following limitations:

1.  the message is being received from Twilio, as part of the sandbox.
2.  unable to forward image(s) yet.

Next iteration: to explore if it can forward the message directly to a specific channel.

## Fifth Iteration:

1.  able to forward messages and media to WhatsApp personal number.
2.  unable to send to a channel directly (to explore possible future solutions in next iteration).

## Future Integration (Suggestions):

1. Integration with Postman (no access due to access being limited to gov.sg personnel) - to send registered, trustworthy SMS from gov.sg.

## Limitations and Acknowledgements:

1. WhatsApp API is not free / has a limited free tier. However, WhatsApp is still the destination of choice, to directly address our problem statement - where misinformation is spreading via WhatsApp.
   Hence, the destination is by design (even though the API might be costly).
   Having forwardable content is directly piggybacking on existing human behaviour of forwarding messages to one's social groups.

2. Twilio can send to a potentially unlimited number of recipients (like a mailing list), subject to rate and cost limits.
