"""
Filename: greeting_app.py
Description: A modular, object-oriented Python application that greets the user,
             uploads the name to an S3 bucket, and is designed for deployment
             to AWS EC2.
Author: Your Name (Replace with your actual name)
Date: October 27, 2023
"""

import logging
import os
import boto3  # Import the boto3 library

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# AWS S3 Configuration
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")  # Get bucket name from environment variable
S3_KEY_PREFIX = "greetings/"  # Prefix for the keys in S3
DEFAULT_REGION = "eu-north-1" # added default region


class Greeter:
    """
    A class that encapsulates the logic for greeting a user and uploading
    their name to an S3 bucket.
    """
    def __init__(self, default_name="Guest"):
        """
        Initializes the Greeter object with a default name.

        Args:
            default_name (str, optional): The default name to use if no user
                name is provided. Defaults to "Guest".
        """
        self.default_name = default_name
        self.s3_client = None # Initialize s3_client
        self.region_name = os.environ.get("AWS_REGION", DEFAULT_REGION)
        logger.debug(f"Greeter initialized with default name: {self.default_name}, region: {self.region_name}")

    def get_user_name(self):
        """
        Prompts the user to enter their name and returns the name.
        Handles input validation and errors.

        Returns:
            str: The name entered by the user, or the default name if no name
                 is entered, or "ErrorName" if an error occurs.
        """
        try:
            name = input("Please enter your name: ")
            if not name.strip():
                logger.info("No name entered. Using default name.")
                return self.default_name
            return name
        except Exception as e:
            logger.error(f"An error occurred while getting the name: {e}")
            return "ErrorName"

    def connect_to_s3(self):
        """
        Connects to AWS S3 using boto3.  Handles errors and uses
        the region name.
        """
        if not S3_BUCKET_NAME:
            logger.error("S3_BUCKET_NAME environment variable is not set.")
            print("Error: S3 bucket name is not configured.")
            return False
        try:
            #  Initialize the s3 client.
            self.s3_client = boto3.client("s3", region_name=self.region_name)
            logger.info(f"Connected to S3 bucket '{S3_BUCKET_NAME}' in region '{self.region_name}'")
            return True
        except Exception as e:
            logger.error(f"Error connecting to S3: {e}")
            print(f"Error connecting to S3: {e}")
            return False

    def upload_name_to_s3(self, user_name):
        """
        Uploads the user's name to an S3 bucket.

        Args:
            user_name (str): The name of the user to upload.
        """
        if not self.s3_client:
            logger.error("Not connected to S3. Cannot upload.")
            print("Error: Not connected to S3. Cannot upload name.")
            return False

        key = f"{S3_KEY_PREFIX}{user_name}.txt"  # Create a unique key
        try:
            self.s3_client.put_object(
                Bucket=S3_BUCKET_NAME,
                Key=key,
                Body=user_name.encode('utf-8'),
            )
            logger.info(f"Uploaded name '{user_name}' to S3 bucket '{S3_BUCKET_NAME}' with key '{key}'")
            print(f"Uploaded name to S3 bucket: {S3_BUCKET_NAME}, Key: {key}")
            return True
        except Exception as e:
            logger.error(f"Error uploading to S3: {e}")
            print(f"Error uploading to S3: {e}")
            return False

    def display_greeting(self, user_name):
        """
        Prints a greeting message to the console, incorporating the user's name.

        Args:
            user_name (str): The name of the user to greet.
        """
        try:
            if not user_name or user_name == "ErrorName":
                print(f"Hello, {self.default_name}!")
            else:
                print(f"Hello, {user_name}!")
        except TypeError as te:
            logger.error(f"TypeError in display_greeting: {te}. Check name type.")
            print(f"Hello, {self.default_name}!")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            print(f"Hello, {self.default_name}!")

class GreetingApp:
    """
    A class that represents the main application.
    """
    def __init__(self, greeter):
        """
        Initializes the GreetingApp with a Greeter object.

        Args:
            greeter (Greeter): An instance of the Greeter class.
        """
        self.greeter = greeter
        logger.debug("GreetingApp initialized.")

    def run(self):
        """
        Runs the application.
        """
        user_name = self.greeter.get_user_name()
        self.greeter.display_greeting(user_name)
        if user_name != "ErrorName":
            if self.greeter.connect_to_s3(): # connect first
                upload_successful = self.greeter.upload_name_to_s3(user_name)
                if upload_successful:
                    print("Name successfully uploaded to S3.")
                else:
                    print("Name upload to S3 failed.")
            else:
                print("Failed to connect to S3.  Upload skipped.")

        logger.info("GreetingApp run completed.")



def main():
    """
    Main function to run the application.
    """
    default_name = os.environ.get("DEFAULT_NAME", "Guest")
    greeter = Greeter(default_name)
    app = GreetingApp(greeter)
    app.run()



if __name__ == "__main__":
    main()
