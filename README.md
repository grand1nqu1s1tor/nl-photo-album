# Photo Album Web Application

##### Dipesh Parwani & Naman Soni



## Features

- Upload photos

- Search photos by keywords, the utterances are:

> Show me photos of {keyword}  
> I want to see images of {keyword}
> Search for photos with {keyword}
> Look up pictures of {keyword}
> Can I see photos that have {keyword}
> Get me photos with {keyword}
> images of {keyword} 
> Find any photos of {keyword}
> I'm looking for photos of {keyword}
> I want to see images of {keyword}
> {keyword}

- Display the search results in frontend.

## Service Architecture

![architecture](https://github.com/grand1nqu1s1tor/nl-photo-album/new/main/architecture.png)


## S3

1. Create a S3 bucket to store the photos.
2. Set up a PUT trigger on S3 bucket
   - Properties -> Events -> set up a PUT trigger `uploadPhoto` and connect with lambda function.
   - Make public of the bucket to make sure we can access the photos.
3. Create a S3 bucket for your frontend .
4. Set up the bucket for static website hosting. Upload the frontend files to the bucket. Integrate the API Gateway-generated SDK (**SDK1**) into the frontend, to connect API.  


## Lambda

Two Lambda functions are inside the same VPC as ElasticSearch and all the lambda functions have the same security group as ElasticSeacrh.

- `index-photos`
  - When uploading a photo into bucket , it will send a PUT trigger.
  - Detect the labels of image sent from S3 event by Rekognition.
  - Store a JSON object in ES that references the S3 object from the PUT event ES and an array of string labels, one for each label detected by Rekognition.   
- `search-photos`
  - Get the query from API Gateway, `$GET` method.
  - Send the query to extract to Lex and Lex will disambiguate and request yields keywords. 
  - Get the keywords to seacrh from Lex and return them accordingly (as per the API spec).   


## Lex

1. Create one intent named “SearchIntent”.
2. Add training utterances to the intent, such that the bot can pick up both keyword searches (“trees”, “birds”), as well as sentence searches (“show me trees”, “show me photos with trees and birds in them”).   


## API Gateway

1. The API has two methods:  
   - `PUT /photos`
     - Set up the method as an Amazon S3 Proxy. This will allow API Gateway to forward your PUT request directly to S3. 
   - `GET /search?q={query text} `
     - Connect this method to the search Lambda function.    


## Live Link
- (http://frontend-bucket-s3.s3-website.us-east-2.amazonaws.com/)
