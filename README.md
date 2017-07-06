# Mentor-mentee-recommender-system
-----
Prototype of a recommender system for mentor-mentee matching

## Problem description

As an input data set to be used to retrieve the mentors, infer the topics and measure mentor's expertise level, please use one of the two datasets: 

 - the Enron Email dataset available here: http://www.cs.cmu.edu/~./enron/enron_mail_20150507.tgz, where mentors will be the email senders and topics will be inferred from the email message body,
 - the DBLP Computer Science Bibliography dataset, available here: http://dblp.uni-trier.de/xml/, where mentors will be the authors and topics will be inferred from the titles of their publications.
 
In the final presentation you'll have to justify and explain the following:
 - design choices behind the prototype of your recommender system
 - methods and libraries used for topic extraction    
 - proposed metric used for measuring the level of expertise of a mentor
 - proposed recommendation method

You will need to also propose a method for quantifying the performance of your recommender system

## Solution
There are 3 notebook that do all the job:
 - 1.Preprocessing.ipynb preprocess the xml file using the class *xml_parser*
 - 2.Topics.ipynb extract the topic 
 - 3.Recommender_system.ipynb explain the recommendation part

You will find also a pdf presentation that will give more information about the prototype and everything asked for

(The data are too big to be present on the repository)