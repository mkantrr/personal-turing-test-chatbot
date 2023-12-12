<a name="readme-top"></a>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Project Image][project-image]](https://www.omni-chatbot.com/wp-content/uploads/2019/12/test_turinga.jpg)

This project was a final project resulting from a semester of work in a class at the University of Mary Washington (UMW)
in a class called ChatGPT and Generative AI (DGST301N). In an effort to test some hypotheses that current chatbot LLM models
where becoming more advanced at a rate unheard of in an ever-expanding AI field, I developed this chatbot program to perform a
series of turing tests personalized to my own "life" data to allow it to mimic how I might respond to people who know me and 
who have had close communication with me a good portion of my life over text messaging (SMS) as much as possible.

A turing test, which was proposed as a measure of machine-human likeness (and often confused primarily as a measure of 
machine intelligence due to our nature as humans to measure intelligence) is a test in which the subject asks a series of questions
in a text-based console. The questions are given responses, and either the human or computer component of the experiement responds.
The subject is then prompted to indicate whether the questions they ask or have asked either originate from a human or a computer
solely based on those text responses, controlling any constants.

This turing test, which was personalized by nature, was a specific measure of how well an LLM model like GPT-4 from OpenAI could be
instructed to be able to simulate human-likeness, most specifically my likeness. In doing so, I do not believe that this type of test
on an LLM model of this nature would be a test of machine intelligence or evolution toward sentient AI. The LLM model, being predictive text,
can only operate effectively on the instructions and information it is given, however it's hallucinations and made up information for data it
does not know or cannot perceive are mostly believable for someone who may not personally know me in a personalized test. 

Acting on only the information that it was given, the issue that arose was the scalability of data. For subjects who have known me for my entire life
or know me very well, there will never be enough data I can feed to the model that would encompass my entire life memories, experiences, emotions, values,
belief systems, etc. that would completely and accurate depict me to be able to completely mimic me, as a human. As such, I believe the results to this experiement
were indicative in and of themselves considering the nature of data to act upon.

While lacking in sample size, the results were surprising:

* Out of 10 questions prompted by the subject in which 5 responses were of my own responses and 5 responses were that of the
chatbot's, my girlfriend of three years (the subject) incorrectly indicated the origin of the response to 2 of the responses.
* Out of 10 questions prompted by the subject in which 6 responses were of my own responses and 4 responses were that of the
chatbot's, my mother (the subject) incorrectly indicated the origin of the response to 2 of the responses as well.
* Out of 7 questions prompted by the subject in which 4 responses were of my own responses and 3 responses were that of the
chatbot's, my best friend of three years (the subject) incorrectly indicated the origin of the response to 4 of the responses.

If you would like to learn more about this experiment I conducted or the intricacies of creating a chatbot program like this,
I refer you to [the presentation](https://youtu.be/QuBjjlUYBsM) on this project.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

This project was built with the following language and packages for ease of use and understanding.

* [![Python][Python]][Python-url]
* [![OpenAI][OpenAI]][OpenAI-url]
* [![Langchain][Langchain]][Langchain-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

You will need to use the [command line interface (CLI)](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Understanding_client-side_tools/Command_line) to use this repo.
Make sure, of course, that you have [Python](https://www.python.org/downloads/) and the Pip package manager installed (which usually comes with Python installation).
1. If you can run the following commands you are ready to go:
* python or python3
  ```sh
  python --version
  ```
  ```sh
  python3 --version
  ```
* pip or pip3
   ```sh
  pip --version
  ```
  ```sh
  pip3 --version
  ```

2. Unfortunately, in order to use OpenAI's API endpoints to query their LLM models, there is a slight fee that accumulates each time you embed information (such as your own data) or each time you query the model
and receive a response. Make sure you have added a small amount to your OpenAI account balance to account for these small fees.

### Installation

_You may find the instructions to set up this chatbot locally on your computer here._

1. Get an [OpenAPI](https://platform.openai.com/account/api-keys) key from your already made OpenAI account or by signing up at [OpenAI](https://openai.com/).
2. Clone the repo
   ```sh
   https://github.com/mkantrr/personal-turing-test-chatbot.git
   ```
3. Install [Langchain][Langchain-url] and other required packages such as OpenAI's API for their chat models.
   ```sh
   pip install langchain openai chromadb tiktoken unstructured
   ```
4. Enter your API in `chatbot/constants.txt`
   ```py
   APIKEY = "ENTER YOUR API"
   ```
   And rename `chatbot/constants.txt` to `chatbot/constants.py`

5. Make a directory within `chatbot/` called `data/`. Place your own data for the LLM model to be trained on in this directory.

   An example file would be `data/data.txt` or `data/data.pdf`.

6. Edit `chatbot/turing_gpt.py` from these lines:
   ```py
   template = """  ***Your instructions to give the bot for responses to each question are given here.***

    Question: {question}
    =========
    {context}
    =========
    Answer in Markdown:"""
   ```
   to be something like:
   ```py
   template = """  Act like a really annoying car salesperson with every response you give.

    Question: {question}
    =========
    {context}
    =========
    Answer in Markdown:"""
    ```

   You may include any amount of instructions to this bot, and there is no specific block indentation or syntax required.
   You must, however, be very specific with your instructions, as whatever you do not tell it that you might expect it to do will not always be the actual outcome.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact


[![LinkedIn][linkedin-shield]][linkedin-url]

Matthew Kanter - mkanter@umw.edu

Project Link: [https://github.com/mkantrr/personal-turing-test-chatbot](https://github.com/mkantrr/personal-turing-test-chatbot.git)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Some helpful resources used to complete this project and some inspiration:

* [Choose an Open Source License](https://choosealicense.com)
* [ChatGPT Retrieval](https://github.com/techleadhd/chatgpt-retrieval)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/mkanter124/
[Python-url]: https://www.python.org
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[OpenAI]: https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white
[OpenAI-url]: https://platform.openai.com/docs/overview
[Langchain-url]: https://github.com/langchain-ai/langchain
[Langchain]: https://img.shields.io/badge/Langchain-0081A5?style=for-the-badge&logo=openaigym&logoColor=white 
[project-image]: https://www.omni-chatbot.com/wp-content/uploads/2019/12/test_turinga.jpg
