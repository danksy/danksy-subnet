# Danksy Subnet code based on Commune Subnet Templeate

Danksy Subnet built on top of [CommuneX](https://github.com/agicommies/communex).
Learn how to structure, build and deploy a subnet on [Commune AI](https://communeai.org/)!

## Subnet Objective

[danksy.ai](https://danksy.ai) is a project that aims to bring fun to the AI community via training models that can make _funny_ content. 
Our goal is to have an agentic model that can use a variety of existing content creation tools and APIs to make memes and much more.

The current implementation is aimed at incentivizing the subnet to run models that can generate data that would be fed into agent workflows.
Initially, we will be using a [fixed dataset](https://huggingface.co/datasets/dknoller/danksy-dataset) but will transition to a streaming dataset as more users are  

### Current Goals
- [x] Subnet Creation
- [x] Initial prompting
- [ ] Upload dataset
- [ ] Set up streaming
- [ ] Integrate with danksy production

As these goals are a moving target, implementation and cadence will vary over time. 

## Validator Setup


### Prerequisites

Please ensure that you have the following environment variable set:
```sh
DANKSY_WORKLOAD_URL=https://workloads.danksy.ai/workload
```

For proper monitoring, ensure you have `node` installed along with `pm2` for process management. 
Alternatively, you can use other tools such as `tmux`, as long as you can manage the validator process 

### Registering the validator
```sh
comx module register danksy-subnet::validator <your_commune_key> --netuid 4
```


### Running
1. Navigate to `src/subnet`
2. Run the following command:

```sh
pm2 start python3 -m cli <your_commune_key>
```

## Miner Setup

### Prerequisites
Please ensure that you have the following environment variables set:
```sh
# Can be any openai api compatible llm inference url
DANKSY_INFERENCE_URL 
# API Key for access
DANKSY_INFERENCE_API_KEY
```
Currently, the default miner code is set up to use inference models from [fireworks ai](https://fireworks.ai/). However, any llm inference method (hosted, locally run, etc) is possible as long as the miner code returns a generated response.

### Serving

From the root of your project, you can just call **comx module serve**. For example:

```sh
SUBNET_UID=x
PUBLIC_IP_ADDRESS=x
comx module serve src.subnet.miner.model.Miner <name-of-your-com-key> --subnets-whitelist $SUBNET_UID \
--ip $PUBLIC_IP_ADDRESS --port 8000
```

### Registration


To register the miner use:
```sh
SUBNET_UID=x
comx module register <name-of-your-miner> <name-of-your-com-key> --ip <your-ip-of-the-server> --port 8000 --netuid $SUBNET_UID  
```