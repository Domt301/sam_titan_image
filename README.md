# AWS SAM Application - Titan Image Generator

This AWS SAM application creates an AWS Lambda function and an endpoint to interact with Titan, the AWS image generator in AWS Bedrock.

## Deployment Instructions

To deploy this application, follow these steps:

1. Install the AWS CLI and SAM CLI on your local machine.
2. Clone the repository containing this SAM application.
3. Navigate to the root directory of the cloned repository.
4. Open a terminal or command prompt.
5. Run the following command to build the SAM application:

    ```bash
    sam build
    ```

6. Run the following command to deploy the SAM application:

    ```bash
    sam deploy --guided
    ```

    This command will guide you through the deployment process, prompting for necessary information such as AWS region, stack name, and parameter values.

7. Once the deployment is complete, you will receive the endpoint URL for interacting with the Titan image generator.

## Usage

To use the Titan image generator, make a POST request to the endpoint URL provided during deployment. Include the necessary parameters in the request body to specify the image generation details.

For more information on how to use the Titan image generator, refer to the documentation.
