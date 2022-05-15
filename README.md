# Whoopbot

[![GitHub issues](https://img.shields.io/github/issues/ashwineaso/whoopbot)](https://github.com/ashwineaso/whoopbot/issues)
![GitHub](https://img.shields.io/github/license/ashwineaso/whoopbot)
[![Coverage Status](https://coveralls.io/repos/github/ashwineaso/whoopbot/badge.svg?branch=main)](https://coveralls.io/github/ashwineaso/whoopbot?branch=main)
[![Python package](https://github.com/ashwineaso/whoopbot/actions/workflows/config.yml/badge.svg?branch=main)](https://github.com/ashwineaso/whoopbot/actions/workflows/config.yml)
## Overview

Whoopbot provides a virtual lock on your resources, so that it's used by one person at a time.

This is useful in cases where multiple people are working on the same resource,
and you need to ensure that it's locked from being modified by anyone else.

For example: You are working on a service: `api-service` which has to be deployed on the `staging` environment.
To ensure that no one else would deploy their version of the service to the same environment,
you can lock the resource using `/whoop lock api-service staging`.

Please note that this is a virtual lock, does not prevent the person from actually modifying the resource.

## Usage Instructions

Whoopbot has the following functionality:

1. Add a resource for a specific environment
2. Delete a resource for a specific environment
3. List the resource and their environments
4. List the locked resources and their environments
5. Lock a resource for a specific environment
6. Unlock a resource for a specific environment

### Adding a Resource

You can add a resource using the command: `/whoop add <resource> <environment:optional>`.  
The environment is optional, if you don't specify it, will be set as `Default`.

You can add the same resource multiple times, but with different environments.
```sh
/whoop add api-service
/whoop add api-service staging
```

### Deleting a Resource

You can remove a resource using the command: `/whoop delete <resource> <environment:optional>`.  
The environment is optional, if you don't specify it, will be set as `Default`.

### Listing Resources:

Resources which have been added are listed using the command: `/whoop list resources`.

### Listing Locked Resources:

Resources which have been added are listed using the command: `/whoop list locked resources`.

### Locking a Resource 

Resources which have been added are locked using the command: `/whoop lock <resource> <environment:optional>`.  
The environment is optional, if you don't specify it, will be set as `Default`.

You can lock the same resource multiple times, but with different environments, if it has been added

```sh
/whoop add api-service
/whoop add api-service staging
```

### Unlocking a Resource

Resources which have been added are unlocked using the command: `/whoop unlock <resource> <environment:optional>`.
You can only unlock the resource which have been locked by you.

### Installation and Running

1. Install the requirements from the `requirements.txt` file
2. Run a docker container with the local version of dynamodb (`amazon/dynamodb-local`)
3. Run the command to start the server 

## Contributing

Please feel free to contribute to the project ❤️

- Give this repo a Star ⭐️
- Ask questions and share your feedback in [issues](https://github.com/ashwineaso/whoopbot/issues) 🙋🏽‍♂️
- Create a PR or issue for bugs, enhancements, ideas and suggestions 💡