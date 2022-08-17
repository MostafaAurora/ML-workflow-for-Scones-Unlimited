# ML Workflow for Scones Unlimited  by Mostafa Mohamed # 

### This is a project showcasing a machine learning workflow for an imaginary scone-delivery-focused logistics company, this project aims to deliver a scalable and safe ML image classification model that is monitored and safeguarded against drift and degrading performance to detect the kind of vehicle delivery drivers have in order to route delivery professionals to the correct loading bay and orders based on their vehicle and give professionals with more capable vehicles farther destinations and professionals with less capable vehicles closer destinations to help optimize operations. ###

<br>
<br>
<br>

## project stages ##

<br>

### 1. Data ETL
- Image data is fetched from the CIFAR dataset
- Image data is explored and filtered based on relevant labels i.e delivery vehicle labels
- Image data is split to train and test datasets
- Image data is checked for validity and then stacked to png files
- Images are uploaded to a S3 bucket

<br>

### 2. Model training and deployment
- A model is selected for training on a powerful ml.p3.2xlarge instance which has the power of a Nvidia Tesla V100 gpu offering 15.7 TFLOPS single precision computing power and 125 TFLOPS of deep learning computing power with tensor cores
- Some hyper parameters are tuned according to is known about the image data
- Training is initialized
- Model monitor data capture configuration is made
- the model is deployed to an inference endpoint

<br>

### 3. Lambda function and step-function authoring and configuration
- 3 lambda functions are authored
  - A lambda function is made to serialize input image data
  - A lambda function to take serialized data and make an inference
  - A lambda function to take inferences and evaluate the quality and confidence of the predictions and raise an error if the confidence threshold is not met or return a specific status code depending on the project version
- A lambda step-function is authored to pass the output each function to the next one, the step-function also uses map to make multiple inferences in parallel, the step function takes the status code output of the last outcome and evaluates it in a condition to send an email to a specific email or set of emails if the inference quality does note meet the quality of the inference or if an error occurs

<br>

### 4. Reviewing data captured with visualizations
- visualizations are made to review confidence metrics of the data captured by model monitor

<br>

## Notes and conclusions
- the project has 2 versions:
  - a version using 3 vehicle classes (bicycle, motorcycle, pickup truck) for training and classification, the model in this version had poorer predictions
  - a version using just 2 classes (bicycles, motorcycles) for training and classification, this version performed significantly better and thus SNS (amazon's "simple notification service") was implemented in this version using the lambda step-function condition logic to avoid a lot of SNS emails since we use map in the step function to process multiple inputs in parallel and since the 3 vehicle classes model performed poorly

<br>

- Here is the step-function graph of the 3 vehicles classes model without SNS:
![no_sns_parallel_processing_state_machine](https://github.com/MostafaAurora/ML-workflow-for-Scones-Unlimited/blob/main/no_sns_state_mahine_screenshots/no_sns_parallel_processing_state_machine.png) 

<br>

- Here is the step-function graph of the 2 vehicles classes model with conditional logic and SNS:
![state machine with sns](.\sns_state_machine_screenshots\state_machine_with_sns.png)

<br>

- Here is an execution sample from the SNS step function:
![sns state machine with parallel success and failure](.\sns_state_machine_screenshots\sns_state_machine_parallel_success_and_failure.png)
  - NOTE : since the function runs many inferences in parallel the confidence evaluation function (confidenceFilter) succeeds many time (as indicated by the green color of the function) but also fails sometimes triggering the SNS publish event and thus leading to the failure of the block as indicated by the red color of the block, that is why it does not have a complete green color from start to finish

<br>

- Here is example of a SNS email sent on failure:
![no_sns_parallel_processing_state_machine](.\sns_subscribtion_screenshots\sns_failure_notification.png)

<br>

- Here is an example of model monitor captured data visualizations:
![model monitor captured-data visualization](.\model_monitor_output_visualizations\model_monitor_output_visualization.png)

<br>

Lastly there are more screenshots showing more details about the step-function or state machine and about SNS in their respective named folders in the project root directory.
