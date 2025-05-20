# Greeting App - AWS S3 Integration with Docker

> **Practice Project**  
> This is a practice project developed to learn and experiment with Python, AWS S3, and Docker.  
> **Not intended for production use.**

##  Description

This is a modular, object-oriented Python application that:

- Prompts the user to input their name.
- Greets the user with their name.
- Uploads the name as a `.txt` file to an AWS S3 bucket.
- Is designed to be run locally or deployed to an AWS EC2 instance.
- Includes Docker support for containerization.


##  Technologies Used

- Python 3.x
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) (AWS SDK for Python)
- AWS S3
- Docker (for packaging and running the app in a container)
- Logging module for error handling and info tracking

##  Features

- Uses environment variables for AWS configuration (bucket name, region, default name).
- Uploads user input as `.txt` to S3 under a `greetings/` prefix.
- Implements error handling and logging throughout.
- Fully modular and testable class-based design.

##  Environment Variables

Set the following environment variables before running the app:

| Variable        | Description                      |
|----------------|----------------------------------|
| `S3_BUCKET_NAME` | Name of the target S3 bucket     |
| `AWS_REGION`     | (Optional) AWS region to use. Defaults to `eu-north-1` |
| `DEFAULT_NAME`   | (Optional) Default name if user doesn't input anything |

Set them in your terminal before running the script:

```bash
export S3_BUCKET_NAME=your-bucket-name
export AWS_REGION=eu-north-1
export DEFAULT_NAME=Friend
```

##  Docker Build and Run

```bash
docker build -t greeting-app .
docker run -e S3_BUCKET_NAME=your-bucket-name -e AWS_REGION=eu-north-1 greeting-app
```
## 📌 Notes
- **This application is strictly for educational and practice purposes.**

- **It is not optimized or secured for production deployment.**


