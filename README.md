# kudumisto
GitHub Issue to GPT; GPT's Response as a Pull Request

Code: https://github.com/busse/kodumisto
Playground: https://github.com/busse/kodumisto-playground
MIT License: https://github.com/busse/kodumisto/blob/main/LICENSE

> Kodumisto (Esperanto): Derived from the Esperanto words 
> "kodo" meaning "code" and "umisto" meaning "skilled person"
> this name suggests the bot's expertise and competence in editing software code.
>   -- ChatGPT-4

Supports:

NEW FILE: Write Issue to create new file. 
 First line MUST be just a file extension including the '.'
 The rest of the issue is the prompt to send to GPT.
   
 Examples:

   Make a cool python script (issue title is ignored)
   |  .py
   |  Create a python script that writes "hello world" to the console.
   |  It should also append one of ten random emojis to the end of the output.

   Test data: The Simpsons did it first (issue title is ignored)
   |  .csv
   |  Create a csv file with sample transaction data for a credit card company.
   |  The file should have a header row and fifty rows of data. The data should
   |  represent credit card transactions for characters from the TV show The
   |  Simpsons, mixed with transactions for characters from the TV show
   |  Family Guy. Make the data similar, but similar transactions for The Simpsons
   |  should have earlier timestamps than those for the Family Guy characters.

   Write me a blog post (issue title is ignored)
   |  .md
   |  Write a post for my Jekyll / GitHub pages blog on what it means for AI to be
   |  self-aware, but give wrong answers only.

CHANGE FILE: Write Issue to create new file. 
 First line of the Issue body MUST be the GitHub URL to the FILE to edit and return PR for.
   Note: This is the same format that the GitHub Web UI uses when it creates an Issue from 
   a file line number using "Reference in new issue"

 Both github.com and raw.githubusercontent.com are supported

 The rest of the issue is the prompt to send to GPT.
   
 Examples:

   Let's go to Mars (issue title is ignored)
   |  https://github.com/busse/kodumisto-playground/blob/main/directory1/hellomars.py
   |  The output of this file should be the red planet, not world.

   Test data: Migrate Legacy Simpsons data
   |  https://github.com/busse/kodumisto-playground/blob/main/simpsons.csv
   |  Refactor this csv file to represent The Family Guy instead of The Simpsons.

   Add a new test to draw triangles (issue title is ignored)
   |  https://raw.githubusercontent.com/busse/AI-Functions/master/test_ai_function.py
   |  Add an additional test function to the script that generates a drawing of a triangle 
   |  in SVG format with style infromation, and runs an appropriate test against it.
   |  Take care to disturb what is already there as little as possible

   TODO(busse): on the triangle test example above, I think it might not work with this latest
                version of kodumisto due to the outdated 'master' taxonomy, 
                but I have it working in an earlier dev version of this script.
USAGE:
 
`kodumisto.py issue_number repo_owner repo_name [gpt_model defaults to gpt-3.5-turbo]`
`kodumisto.py 38 busse kodumisto-playground gpt-4`