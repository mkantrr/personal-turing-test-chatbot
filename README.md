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

There are many great README templates available on GitHub; however, I didn't find one that really suited my needs so I created this enhanced one. I want to create a README template so amazing that it'll be the last one you ever need -- I think this is it.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

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
