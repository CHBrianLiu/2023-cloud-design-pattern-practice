## Problem

> Client-side code, such as browser applications, where it's difficult to provide call-back endpoints, or the use of
> long-running connections adds too much additional complexity.

## Context

While hosting a Line chatbot, Line will send webhook events to the chatbot server, along with a reply token. Line
expects the server to send an HTTP POST request with the given reply token to its API to reply to a certain message.
However, the reply token expires in 30 seconds. If the underlying logic takes longer than 30 seconds, it would be
impossible to reply to the message and the user experience drops significantly.

I'll build a Line chatbot to let me generate pictures via Line. The picture generation functionality is provided by
OpenAI through Azure OpenAI Service. However, the time it requires to generate a picture depends on the complexity of
prompts. In other words, we are at risk of losing contact with users.

## Architecture

![architecture](./architecture.png)

## Demo setup

## Run the demo

## Demo

