# kudumisto
GitHub Issue as ChatGPT Prompt; ChatGPT's Response as a Pull Request

Kodumisto is a Python script that reads a GitHub Issue then calls the OpenAI ChatGPT API with the body of the Issue as a ChatCompletion prompt to the GPT model. It then writes the contents of ChatGPT's response as a Pull Request associated with the Issue.

Kudimisto currently supports the creation of new files, and the editing of a single file. It can be called either via the command line, or can be triggered by GitHub Actions, examples of which are provided in this repository.

> Kodumisto (Esperanto): Derived from the Esperanto words 
> "kodo" meaning "code" and "umisto" meaning "skilled person"
> this name suggests the bot's expertise and competence in editing software code.
>   -- ChatGPT-4

**Kodumisto was created for three main reasons:**

1. To get ChatGPT closer to a "regular" developer workflow with minumum dependencies. Once setup, a user only needs to work with the GitHub Issues if they want to, choosing which Issues they want kodumisto to attempt, and choosing whether to accept the Pull Requests as-is, modify them further, or trash them all together.

2. To see what kind of coding ChatGPT can do in real world scenarios. See the `kodumisto-playground` Issues for examples from my testing (note that labels in that repo may be misleading): https://github.com/busse/kodumisto-playground/issues

3. To start teach myself Python by making something real for others to use.

## Installation

A future version of this README should have more robust installation instructions, but basically get `kodumisto.py` in a Python environment and make sure you have set the `.env` variables for `OPENAI_ACCESS_TOKEN` and `GITHUB_ACCESS_TOKEN`.

Instructions on using GitHub Actions to trigger kodumisto on an Issue when it is assigned a specific label is covered after the Usage secton below.

## Usage

1. Create a GitHub Issue. 

If you intend for the Issue to create a new file, make the first line of the Issue be the file type extension you would like the new file to have, then write the prompt instructions in the rest of the Issue body. Examples:

>  Make a cool python script (issue title is ignored)
>   |  .py
>   |  Create a python script that writes "hello world" to the console.
>   |  It should also append one of ten random emojis to the end of the output.
>
>   Test data: The Simpsons did it first (issue title is ignored)
>   |  .csv
>   |  Create a csv file with sample transaction data for a credit card company.
>   |  The file should have a header row and fifty rows of data. The data should
>   |  represent credit card transactions for characters from the TV show The
>   |  Simpsons, mixed with transactions for characters from the TV show
>   |  Family Guy. Make the data similar, but similar transactions for The Simpsons
>   |  should have earlier timestamps than those for the Family Guy characters.
>
>   Write me a blog post (issue title is ignored)
>   |  .md
>   |  Write a post for my Jekyll / GitHub pages blog on what it means for AI to be
>   |  self-aware, but give wrong answers only.

If you intend for the Issue to make changes to an exsiting file, make the first line of the Issue body be the URL to the file in the repo that you want ChatGPT to edit (Both github.com and raw.githubusercontent.com are supported), then write the prompt instructions in the rest of the Issue body. Examples:

>   Let's go to Mars (issue title is ignored)
>   |  https://github.com/busse/kodumisto-playground/blob/main/directory1/hellomars.py
>   |  The output of this file should be the red planet, not world.
>
>   Test data: Migrate Legacy Simpsons data
>   |  https://github.com/busse/kodumisto-playground/blob/main/simpsons.csv
>   |  Refactor this csv file to represent The Family Guy instead of The Simpsons.
>
>   Add a new test to draw triangles (issue title is ignored)
>   |  https://raw.githubusercontent.com/busse/AI-Functions/master/test_ai_function.py
>   |  Add an additional test function to the script that generates a drawing of a triangle 
>   |  in SVG format with style infromation, and runs an appropriate test against it.
>   |  Take care to disturb what is already there as little as possible
>
>   TODO(busse): on the triangle test example above, I think it might not work with this latest
>                version of kodumisto due to the outdated 'master' taxonomy from that repo when I forked it, 
>                but I have it working in an earlier dev version of this script.

2. Run kodumisto

```sh
kodumisto.py issue_number repo_owner repo_name [model]
```
Note: `model` defaults to `gpt-3.5-turbo`

```sh
kodumisto.py 38 busse kodumisto-playground
```

```sh
kodumisto.py 38 kodumisto-playground busse gpt-4
```

3. After running successfully you will have a PR to review on the Issue.

## Kodumisto with GitHub Actions

Kodumisto can run as a GitHub Action. One action can handle both file add and file edit use cases.

An example action is provided here as `.github/workflows/kodumisto_by_label.yml`, which is written to trigger when the label `kodumisto` is added to an Issue. Similarly, `.github/workflows/kodumisto_by_label_gpt_4.yml` uses the GPT-4 model, triggered by the label `kodumisto-gpt-4`

Note that for these to run as provided here, you must set two environment secrets as follows:

1. In GitHub for the repo you want kodumisto to have Issues trigger actions, navigate to:

> Settings -> Secrets and variables -> Actions

2. Add an environment called `env-secrets`

3. Create new Environment secrets for `GH_ACCESS_TOKEN` and `OPENAI_ACCESS_TOKEN`

Note: Due to a known limition in GitHub Actions working with Issues, we aren't using the Action's runtime-generated temporary GitHub token.

Also, from a repo/code perspective, it may make sense to have `kodumisto.py` running in a separate repo than the code it is affecting. Future versions of kodumisto may support this more robustly "out of the box".

## Contributing

Issues & Pull Requests are welcomed!

