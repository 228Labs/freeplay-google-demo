# Agent Observability with Freeplay

[Freeplay](https://freeplay.ai/) is an end-to-end platform for building and optimizing AI agents. Manage prompts, run experiments & evals, monitor production, and review data—all in one enterprise-ready platform.

Freeplay and Google ADK complement one another. The Google ADK gives you a powerful and expressive agent orchestration framework while Freeplay plugs in for observability, prompt management, evaluation and testing. 

Below is a guide for getting started with Freeplay and ADK. You can also find a full sample agent repo [here](https://github.com/228Labs/freeplay-google-demo).

## Basic Set up
**Create a Freeplay Account**

Sign up for a free [Freeplay account](https://freeplay.ai/signup).

After creating an account, you'll want to add the following environment variables to your code. 
```
FREEPLAY_PROJECT_ID=
FREEPLAY_API_KEY=
FREEPLAY_API_URL=

```

**Integrate using the Freeplay ADK Library**

Install the Freeplay ADK library

```pip install freeplay-python-adk```

Freeplay will automatically capture OTel logs from your ADK application when initialize observability 

```
from freeplay_python_adk.client import FreeplayADK
FreeplayADK.initialize_observability()
```

You can now use the ADK just as you normally would and you will see logs flowing to Freeplay in the Observability section.

## Observability
Freeplay's Observability gives you a clear view into how your agent is performing in production.
You can dig into to individual agent traces to understand each step and diagnose issues. 

<img src="https://228labs.com/freeplay-google-demo/images/trace_detail.png" width="600" alt="Trace detail">

You can also use Freeplay's comprehensive filtering functionality to slice and dice the data across any segment of interest. 

<img src="https://228labs.com/freeplay-google-demo/images/filter.png" width="600" alt="Filter">

## Prompt Management
Freeplay offers [native prompt management](https://docs.freeplay.ai/docs/managing-prompts) which simplifies the process of version and testing different prompt versions.

To leverage Freeplay's prompt management capabilities alongside the Google ADK you'll want to use Freeplay ADK agent wrapper.
The FreeplayLLMAgent extends the ADK's base LlmAgent class but instead of having to hard code the prompt you can version prompts in the Freeplay application. 
First define a prompt in Freeplay by going to Prompts -> Create prompt template. 

<img src="https://228labs.com/freeplay-google-demo/images/filter.png" width="600" alt="Prompt">

In code simply use the ```FreeplayLLMAgent```

```
from freeplay_python_adk.client import FreeplayADK
from freeplay_python_adk.freeplay_llm_agent import (
    FreeplayLLMAgent,
)

FreeplayADK.initialize_observability()

root_agent = FreeplayLLMAgent(
    name="social_product_researcher",
    tools=[tavily_search],
)
```

When the ```social_product_researcher``` is invoked the prompt will be retrieved from Freeplay and formatted with the proper input variables. 

## Evaluation
[Freeplay](https://docs.freeplay.ai/docs/evaluations) enables you to define, version, and run evaluations right from the web application.
You can define evaluations for any of your prompts or agents by going to Evaluations -> "New evaluation". 

<img src="https://228labs.com/freeplay-google-demo/images/eval_create.png" width="600" alt="Creating a new evaluation in Freeplay">

These evaluations can be run for both online monitoring and offline evaluation. 
