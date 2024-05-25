# Danksy Subnet code based on Commune Subnet Templeate

Danksy Subnet built on top of [CommuneX](https://github.com/agicommies/communex).
Learn how to structure, build and deploy a subnet on [Commune AI](https://communeai.org/)!

## Subnet Objective

[danksy.ai](https://danksy.ai) is a project that aims to bring fun to the AI community via encouraging the training of models that can make _funny_ content. 
Our goal is to have an agentic model that can use a variety of existing content creation tools and APIs to make memes and much more.

The current implementation is aimed at incentivizing the subnet to run models that can generate data that would be fed into agent workflows.
Initially, we will be using a [fixed dataset](https://huggingface.co/datasets/dknoller/danksy-dataset) but will transition to a streaming dataset over time.

### Current Goals
- [x] Subnet Creation
- [x] Upload dataset
- [x] Set up streaming
- [ ] Image macro captioning and generation with multimodal models (the fun part)
- [ ] Integrate with danksy production

As these goals are a moving target, implementation and cadence will vary over time. 

## Validator and Miner Notes
When running either a validator or a miner, you need to keep this process alive, running in the background. 
Some options are [tmux](https://www.tmux.org/](https://ioflood.com/blog/install-tmux-command-linux/)), [pm2](https://pm2.io/docs/plus/quick-start/) or [nohup](https://en.wikipedia.org/wiki/Nohup).
We will use `tmux` for examples.

For subnet uid, on mainnet the netuid is `4` and on testnet the netuid is `24`

## Validator Setup

### Prerequisites

Please ensure that you have the following environment variable set:
```sh
DANKSY_WORKLOAD_URL=https://workloads.danksy.ai/workload
```

In the root directory, run the following command:
```shell
pip install -e .
```

### Registering the validator

You must first register before running the validator:

```sh
comx module register danksy-subnet::validator <name-of-commune-key> --netuid <danksy-netuid>
```

### Running
Run the following command:

```sh
pm2 start "python -m validator.cli" --name <validator-instance-name>
```

## Miner Setup

### Prerequisites

Please ensure that you have the following environment variables set (assuming you are using [fireworks ai](https://fireworks.ai)):
```sh
# API Key for access
DANKSY_INFERENCE_API_KEY=<api-key>
```
Optionally, you can also set the following in order to use a different provider such as openAI
```shell
# Can be any openai api compatible llm inference url
DANKSY_INFERENCE_URL="website.com"
DANKSY_INFERENCE_MODEL_NAME="llama-v3-70b"
DANKSY_INFERENCE_API_KEY="<api-key>"
```

In the root directory, run the following command:
```shell
pip install -e .
```

Currently, the default miner code is set up to use inference models from [fireworks ai](https://fireworks.ai). 
However, any llm inference method (hosted, locally run, etc) is possible as long as the miner code returns a generated response.
Feel free to modify the `Miner` instantiation and `generate` methods as needed.

By default, the miner instance will listen on port `8000`. Please ensure this port is available and open for connections.

### Serving

Run the following command:

```shell
pm2 start "comx module serve miner.model.Miner <name-of-commune-key> --subnets-whitelist <danksy-netuid> --ip 0.0.0.0" --name <miner-instance-name>
```
By default, this will run the miner instance on port 8000. You can modify via adding the argument `--port `. Keep this port value in mind when registering.

### Registration

To register the miner use:
```shell
SUBNET_UID=x
comx module register <miner-instance-name> <name-of-commune-key> --ip <ip-of-the-miner> --netuid <danksy-netuid>  
```

## Testnet Instructions

### Running a Miner
The instructions are nearly similar with the addition of the `--testnet` flag after invoking `comx` and using the testnet id `24`.

Register the miner on testnet 24 (ensure the port specified is open):

```shell
comx --testnet module register danksy-subnet::miner <name-of-commune-key> --ip <ip-of-the-miner> --netuid 24
```
To run:
```shell
comx --testnet module serve miner.model.Miner miner1 --subnets-whitelist 24 --ip 0.0.0.0
```

### Running a Validator
To register:
```shell
comx --testnet module register danksy-subnet::validator <name-of-commune-key> --ip <ip-of-the-miner> --netuid 24
```
To run the validator:
```shell
python -m validator.cli vali1 --netuid 24 --testnet
```
