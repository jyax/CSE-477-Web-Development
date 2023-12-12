# [Web Application Development](https://gitlab.msu.edu/cse477-fall-2023/course-materials/): Final Exam

## Purpose
The purpose of this Final Exam is to assess your understanding of the essential elements of web application development covered this semester; these elements include: 

1. Reactive front-end design
2. Design of a data-driven backend
3. Session management
4. Asynchronous communication 
5. Web APIs

## Exam Goals
For the Final Exam, you will develop a twist on the popular word guessing game -  [Wordle](https://www.nytimes.com/games/wordle/index.html). Your implementation should be visually and functionally the same as [the standard game](https://www.nytimes.com/games/wordle/index.html), with three exceptions:

1. Users must signup and login before being able to play the game. 
2. The hidden word in your version will not be limited to 5 characters in length. Instead, players will have $n$ tries to guess a word of length $n$ (e.g. 3 tries to guess a word of length 3).  
3. At the end of a game (a win or loss), you will display a leaderboard that shows the top 5 users according to how quickly they beat that day's game. 

**NOTE:** Your implementation of the game should be accessible through the project's page of the website you've been building in Homeworks 1-3. 

## Specific Requirements
Your implementation of the exam must adhere to the following specific requirements:

1. **The Signup System:** You will develop pages that allow your users to signup with a username and password. Only logged in users should be allowed to play the game. Users must have an ability to logout as well. Make sure that all stored passwords are encrypted.

2. **The Hidden Word**: Your system's backend will source and store a new word for the user's every day. The hidden word should not be stored anywhere a user could find it (i.e. nowhere on the front-end of your interface). To generate the hidden word, you may use the [word of the day](https://www.merriam-webster.com/word-of-the-day), or some other source of your choosing.

3. **The Interface **: On the user's first sign-in, they should be prompted with the instructions for the game. Following this prompt, your users should be presented with an  $n \times n$  grid that records their guesses and a visual keyboard that they can use to enter their guesses. Users should be able to use their native keyboard to enter guesses as well.

4. **Input Validation** Before allowing a word to be submitted, you should check that it is a valid English word. You may accomplish this by using the Free Tier of the [Word API](https://www.wordsapi.com/), or [PyEnchant](https://pyenchant.github.io/pyenchant/). 

5. **Answer Check**: Following validation, you will check if a user's guess matches the hidden word and color the grid entries based on their status: 

   * grey: if the character does not show up anywhere in the hidden word; 

   * yellow: if user guessed a correct character but in an incorrect location; 

   * green: if the user guessed a correct character in a correct location.

6. **Game Conclusion** If the user guesses the word correctly or makes $n$ unsuccessful attempts at guessing the word, the game is over and the $n \times n$ grid should be replaced by a leaderboard that shows (1) the hidden word, and (2) the top 5 users according to how quickly they beat that day's game. 

## Submitting your assignment

Be sure to perform all development in the `Final-Exam` directory of your <u>Personal Course Repository</u> 

##### Submit Exam Code

1. Submit your assignment by navigating to the main directory of your <u>Personal Course Repository</u> and Pushing your repo to Gitlab; you can do this by running the following commands:

   ```bash
   git add .
   git commit -m 'submitting Final Exam'
   git push
   ```

2. You have now submitted the Final Exam; you can run the same commands to re-submit any time before the deadline. Please check that your submission was successfully uploaded by navigating to the corresponding directory in Personal Course Repository online.


**Deploy your web application to Google Cloud**

Deploy your Dockerized App to Google Cloud by running the commands below from the Final Exam directory.

```bash
gcloud builds submit --tag gcr.io/cse477-fall-2023/final-exam
gcloud run deploy --image gcr.io/cse477-fall-2023/final-exam --platform managed
```

As we did in the homework, please retain the <u>Service URL</u>; You can visit the <u>Service URL</u> above to see a live version of your web application. 


##### Submit Final Exam Survey:

[Submit the Service URL for your live web application in this Google Form]( https://docs.google.com/forms/d/e/1FAIpQLSede23XHa12B7mTjH48JtXJMGY_1Y1ArjUcDRQN3lquwzFDPA/viewform). 
