# MTA-UTSC FIFA Case comp

Welcome to our Group's solution to the MTA case comp! Within this repository, you shall find the answer to the prompt, *Defenders often need to be physically strong in order to compete and progress in 
the world cup.*

Our answer is that **Defenders do not need to be physically strong to progress in the worldcup**.

## Repository
Refer to ImportScripts to see the scripts used to pull data or process them
Refer to lm_wc.pdf for the regression run

## Data
To craft our answer, we used the following data.  

[Fifa 22 Dataset](https://www.kaggle.com/datasets/stefanoleone992/fifa-22-complete-player-dataset) - For player attribute data  
[Fifa 18 Results](https://en.wikipedia.org/wiki/2018_FIFA_World_Cup) - Scraped to get results of World cup

## Approach

We used multiple linear regression too see if there was a relationship between our chosen x variables and our y variables. We found that there is a weak correlation between the x variables and y, and thus there is not enough significant to 
agree that defenders need to be physically strong to progress.

## X Variables
For creativity, we used the FIFA attributes per player and determined specific attributes which we believed represented the physicality of a player. Such variables are
- movement acceleration
- movement agility
- movement balance
- power jumping
- pace
- movement reactions
- movement sprint speed
- power stamina
- power strength

## Y Variables
The Y variable we have chosen is the final position of each team of the Fifa world cup. While it is not a direct measure of "progression" (see for example belgium has more points than croatia despite placing lower), it is a fair estimate as the higher the placement of a team, the higher it's points will be.

## Result
As we can see in the lm_wc.pdf file, we can see that the regression shows a weak correlation (0.33). Thus, there is not enough evidence to support the prompt. 




