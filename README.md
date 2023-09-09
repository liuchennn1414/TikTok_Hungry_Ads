# Hungry_Ads ReadMe 

## Content: 
- Instructions
- Introduction 
- Part1: Scoring Models 
- Part 2: Matching Algorithm 
- Part 3: Result Analysis 
- Part 4: Future Work 
- Part 5: References

GitHub link: https://github.com/liuchennn1414/TikTok_Hackathon.git

## Instructions:

To run our code:
cd Matching_Algo
python run_model.py
To generate results for each category, this section of code needs to be modified accordingly:
![WechatIMG1406](https://github.com/liuchennn1414/TikTok_Hackathon/assets/77218431/9493b2f8-1fe1-4c8d-9296-94f50e7267f4)

The output could be found in 
/Matching_Algo/Results/MATCHING_RESULTS.json
And this Result_analysis.ipynb contains results analysis of key metrics, such as the score difference, market similarity score, and the task handling time.

ads.ipynb and moderstor_score.ipynb: Data processing and calculation of ads and moderators could be found in these 2 notebooks. The detailed weightage assignment and justification can also be found here. 
They process sample_data.xlsx and output 6 csv files, which are ads and moderators split into good, medium, and bad categories. 

## Introduction:

In this README file, we will provide an overview of our project, which focuses on optimising the moderation process for social media advertisements. It consists of three key components: scoring models, namely a ads content scoring model and a moderator scoring model, a matching algorithm which assigns the highest-scoring ads to top-performing moderators; and plans for Further Work to continually improve and refine the moderation process.  

Using the scoring model, we were able to split the ads and moderators into 3 categories, with high, medium, and low scores. The ads are then assigned to the moderators of the same category, as shown in Figure 1.
<img width="593" alt="Screenshot 2023-09-09 at 11 18 43 PM" src="https://github.com/liuchennn1414/TikTok_Hackathon/assets/77218431/ce0698eb-f76f-4c18-83a4-deb6d98dfdf8">

Figure 1. Overview of our algorithm

Part 1: Scoring Models 

The first part focuses on the Scoring Models for ads and moderators. The score of an advertisement reflects its priority to be reviewed, while the score of a moderator reflects his performance.

A holistic round of data exploration & engineering has been conducted to fill up/remove missing values, visualise distribution, normalise highly skewed data (e.g. handling time from moderator) and standardise the scale of attributes to prevent latent weight. Correlation analysis has also been conducted to study potential correlation among attributes. 

### 1.1 Ads Content Scoring Model
How did we determine the “priority” of an advertisement? We designed 4 metrics stemming from the information given in the dataset, which assess advertisements in 4 distinct aspects: risk, profitability, urgency, and complexity. 

a. Risk
This component evaluates the potential risk associated with the content. Risk takes into account of punish_num and the number of days after the latest punished date. The more punishments the ad supplier has and the more recent the latest punishment is, the higher the risk of this content. 

b. Profitability
Profitability assessment helps us determine the financial viability and potential returns associated with the content. It ties with the avg ads revenue and ads revenue fields of the dataset. 

c. Urgency
Urgency scoring assesses how time-sensitive the content is. It helps in prioritising and addressing content that requires immediate attention. Urgency is calculated using the start time, the earlier the ads need to be rolled out, the less time left for moderators to complete their review, and thus would be more urgent.

d. Complexity
The complexity component evaluates how intricate or involved the content is. It helps in understanding the level of effort required to deal with the content effectively. Complexity is given by the baseline_st field of the dataset.

The final scoring model for advertisement is as such: 
Y = 0.35*risk + 0.35*profitability+ 0.15*urgency + 0.15*complexity)

These 4 metrics are then assigned different weights in a linear model to co-determine the priority of the ad to be reviewed by the top-performing moderator. The higher the risk, higher the profitability, higher the urgency and higher the complexity, the better the moderator to be assigned.


### 1.2 Moderator Scoring Model
The Moderator Scoring Model is designed to evaluate the performance of moderators using a linear model based on 2 components: Accuracy and Efficiency. A justified weight is given to each component based on the business context. 

a. Accuracy
Accuracy scoring assesses how well moderators are in correctly identifying and categorising content. It depends on the original Accuracy column given in the dataset.

b. Efficiency
Efficiency scoring evaluates how efficiently moderators handle the content. It combined the effect of productivity, utilisation and handling time using a linear model with justified weights. 

The final scoring model for moderator is as such: 
Y = 0.5Accuracy + (0.33Productivity + 0.3Utilisation - 0.33HandlingTime)

Please refer to the notebook for the details on how we generate the score and how we design the weights.


## Part 2: Matching Algorithm

In order to ensure that ads are efficiently matched to a moderator with a similar score, we split the ads and moderators into 3 categories, namely the high scoring category, average scoring category and low scoring category. The assignment of ads in these batches are done in a parallel manner. This ensures that high scoring ads are not handled by low scoring moderators and vice versa. 

Within each category, ads are sorted according to the score, so that high priority ads are moderated first. They are then assigned to moderators in batches. A one-to-one assignment is done in each batch, and we aim to minimise the overall cost of assignment in each batch. The overall cost is defined by the loss function, described in details below. 

The loss function comprises of 3 components: 
The absolute difference between the scores given a pair of ad and moderator.
This measures the fitness between the ad and moderator in terms of scores
The maximum similarity between the ad’s country and moderator’s scope of countries:
In order to assign ads to the moderator with similar cultural and language context, we prompted ChatGPT to generate the similarity between each pair of distinct countries based on their official language used as well as the similarity of their cultural background. The similarity score varies from 0 to 1, and the closer to 1, the more suitable the moderator to review this ad.
As a moderator can review ads from more than 1 country, we only consider the country in a moderator’s scope that is the most similar to the country the ad came from.
This ensures that moderators handle ads that he/she is more familiar with
The length of task at hand of a moderator after he/she is assigned an ad.
By minimising the time taken for a moderator to finish reviewing all ads assigned after each batch, we shorten the time taken to finish reviewing all the ads.

The 3 losses are normalised in each batch and assigned an individual weight, with the weight of the second cost being negative and the rest being positive. These values then sum up to be the overall loss of assignment in each batch.

The min-cost-assignment problem for each batch is handled with the Hungarian algorithm, also known as the Kuhn-Munkres algorithm, which is an optimization algorithm used for solving the assignment problem.

## Part 3: Model Result 
We will evaluate our matching model’s result via 3 perspectives: Score Difference, Market Similarity and Task Handling Time. 

### 3.1 Score Difference
<img width="597" alt="Screenshot 2023-09-09 at 11 19 33 PM" src="https://github.com/liuchennn1414/TikTok_Hackathon/assets/77218431/b93aee92-fa2e-42d9-b227-c4c1f0c0b270">



Based on the optimised distribution of score difference between moderator and ads, the distribution has shifted left as compared with the random mean & distribution. It is a good indicator that our matching model reduces the score difference between moderator and ads, and good content is moderated by good moderators to make sure that those risky and highly profitable materials are handled appropriately. 

### 3.2 Market Similarity 
<img width="596" alt="Screenshot 2023-09-09 at 11 19 49 PM" src="https://github.com/liuchennn1414/TikTok_Hackathon/assets/77218431/c74e4678-e7fd-4a64-bd69-997513b0340c">


The improved market similarity score has been shifted to the right, and the median of average score has increased from 0.4 to 0.75 (a 90 percent increase). As a result of our model, moderators are able to focus on moderating content which they are familiar with (from a linguistic and cultural perspective), which would improve their efficiency and accuracy, which has resulted in the optimization of both revenue and review time. 

### 3.3 Task Handling Time 
<img width="601" alt="Screenshot 2023-09-09 at 11 19 56 PM" src="https://github.com/liuchennn1414/TikTok_Hackathon/assets/77218431/55c5d60a-c7ca-477b-9621-0223fa9f4366">

Our model was able to reduce the median task handling time from 90 to 25 (a 72% reduction). A shorter handling time per task indicates that moderators will be able to review each advertisement more quickly, which will ultimately improve their efficiency. However, we noticed a pattern with higher handling time, and we found out that this is contributed by the good moderator (i.e. the high score category).

The root cause is likely that high-score tasks are generally more complex, thus requiring a longer duration to moderate effectively. Despite this, we remain convinced that assigning complex tasks to high-score moderators is essential. We prioritise this approach because the risks associated with allowing potentially harmful content to pass or wrongly rejecting high-value content are considerably greater than the inconvenience of slightly longer wait times for advertisers. We have undertaken efforts to optimise both facets to the best of our ability.

## Part 4: Future Work

<img width="624" alt="Screenshot 2023-09-09 at 11 20 03 PM" src="https://github.com/liuchennn1414/TikTok_Hackathon/assets/77218431/4cc333a3-fab4-4316-9d98-c05a28cfb712">


While we don't have access to the actual content of the advertisement, we believe it's crucial to review it to determine if the ad poses any risk, beyond just relying on historical data. As such, we've developed a framework that can analyse video content and enhance our ability to assess the risk level of an advertisement.

Our framework essentially transforms video into several images, which are then examined using traditional image classifiers like CLIP to identify any potentially illegal products featured in the advertisement. Similarly, we can convert audio into text and use a text classifier (like BERT) to detect any references to illegal products. If any are found, the advertisement would be deemed riskier.

By understanding the content of the advertisement, we're confident that our advertisement scoring model will yield more accurate results.

## Part 5: Resources
Stochastic dynamic matching: A mixed graph-theory and linear-algebra approach
A framework for dynamic matching in weighted graphs





