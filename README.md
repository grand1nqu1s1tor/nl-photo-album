# Photo Album Web Application

## Developed by Dipesh Parwani & Naman Soni

## Features

- Upload photos to an S3 bucket.
- Search photos by keywords with various utterances, such as:
  - "Show me photos of {keyword}"
  - "Can I see photos that have {keyword}"
  - ... [and so on]

- Display the search results on the frontend.

## Service Architecture

![architecture](https://github.com/grand1nqu1s1tor/nl-photo-album/blob/main/architecture.png)

## S3 Bucket Setup

1. Create an S3 bucket to store uploaded photos.
2. Configure a PUT event trigger on the S3 bucket to invoke a Lambda function upon photo upload.
3. Create another S3 bucket for the frontend application.
4. Enable static website hosting for the frontend bucket and upload the required files.

## Lambda Functions

- **index-photos**: Triggered by S3 PUT, this function uses Rekognition to label images and stores the data in ElasticSearch.
- **search-photos**: Handles search queries via API Gateway, processes them with Lex, and queries ElasticSearch.

## Lex Configuration

- Create an intent called "SearchIntent" with various training utterances for keyword and sentence searches.

## API Gateway

- Set up a `PUT /photos` method as an S3 proxy.
- Link the `GET /search?q={query text}` method to the search-photos Lambda function.

## Live Application

[Photo Album Web Application](http://frontend-bucket-s3.s3-website.us-east-2.amazonaws.com/)

## Demo link
(https://www.youtube.com/watch?v=g6ehycK2Y8s)
