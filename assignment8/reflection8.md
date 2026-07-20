# Reflection 8
### Ben Branta

## How much did you need to update your word_counts_from_file function? Did you make any other changes beyond returning a DataFrame instead of a dictionary?

I had to update the return value and adjust the pd.DataFrame method to create the columns and name them. Overall, it was a small change.

## What is the value in removing stopwords from text before computing the Scrabble scores or sentiment scores?

Stopwords are normally removed because they don't add meaning to the text. They are filler words. In the Scrabble context this translates to points: stopwords like "a", "the", and "is" are short, common words made of low-scoring letters. By removing the words for scrabble we focus on scores for meaningful words. For sentiment, stopwords carry no positive or negative signal, so removing them lets the sentiment analyzer focus on the words that actually express opinion.

## Discuss your experience writing the wikipedia_page_content function in collaboration with an AI tool.

For this task I chose to work with Claude. Using AI tools can complete a task quickly, but they can also create a lot of content quickly, so it's important to understand what the code is actually doing rather than just accepting it. A good example from this assignment: the first version of the function worked when I tested the URL in my browser but returned a 403 Forbidden error in Python. Working through it with the AI, I learned that Wikipedia rejects requests using the default python requests User-Agent, and the fix was to send a descriptive User-Agent header identifying the project. I would not have understood that fix if I had not read through the code and the error instead of just re-generating it.

## A few of the interstates have very negative compound sentiment scores. Any thoughts on what might be special about those interstates?

The very negative articles tend to be about interstates whose histories involve disasters, deaths, and controversy. VADER scores words like "killed", "crash", "collapse", "destroyed", "protest", and "demolished" as strongly negative, and some interstate articles are full of that vocabulary. So the negative scores are not really saying the highway is "bad" — they are picking up that the article spends a lot of its text on crashes, disasters, and controversies rather than neutral route description. It is a good reminder that sentiment analysis measures the language of the article, not the quality of the thing the article is about.

## What did you find interesting or useful in this Lesson, and how might you use it in your future work?

I think the NLTK library has a lot of interesting tools — tokenizing, stopword lists, and sentiment analysis all took only a few lines each once the data was cleaned. With the rise of LLMs, I think mastering NLP fundamentals like the ones in NLTK will become more and more important, both for preprocessing text before feeding it to larger models and for understanding what those models are doing under the hood. From this assignment though I'm left wondering why does sentiment matter? What other tools in NLTK are used to evaluate LLMs and why? Regarding sentiment - some of my research shows that it could be useful for escalating service tickets. This is an interesting application for LLMs that doesn't jump out because I typically use it as a research tool. I'm interested in finding use cases for LLMs (where they shine) and I think NLTK was an interesting introduction into those use cases.
