## Problem

> A migration is planned to happen over multiple stages, but integration between new and legacy systems needs to be
> maintained.

## Context

A company stores all the customer data in a relational database. However, they would like to develop a social media
platform that allows users to share thoughts. Moreover, they want to store post data in a non-relational database, but
do not want to migrate the existing data to the new non-relational database due to the complexity.

## Architecture

Instead of letting applications query user metadata and post data from each database respectively, we can add a service
to perform data operations.

![architecture](./architecture.png)

## Demo setup

## Run the demo

## Demo