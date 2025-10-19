# TDD / BDD Final Project Template

This repository contains the template to be used for the Final Project for the Coursera course **Introduction to TDD/BDD**.

## Usage

This repository is to be used as a template to create your own repository in your own GitHub account. No need to Fork it as it has been set up as a Template. This will avoid confusion when making Pull Requests in the future.

From the GitHub **Code** page, press the green **Use this template** button to create your own repository from this template. 

Name your repo: `tdd-bdd-final-project`.

## Setup

After entering the lab environment you will need to run the `setup.sh` script in the `./bin` folder to install the prerequisite software.

```bash
bash bin/setup.sh
```

Then you must exit the shell and start a new one for the Python virtual environment to be activated.

```bash
exit
```

## Tasks

In this project you will use good Test Driven Development (TDD) and Behavior Driven Development (BDD) techniques to write TDD test cases, BDD scenarios, and code, updating the following files:

```bash
tests/test_models.py
tests/test_routes.py
service/routes.py
features/products.feature
features/steps/load_steps.py
```

You will be given partial implementations in each of these files to get you started. Use those implementations as examples of the code you should write.

## Checklist
As mentioned in Exercise 1, have you updated the code in the file tests/factories.py for creating fake products and saved the GitHub URL of the same?

As mentioned in Exercise 2, have you updated the test cases in the filetests/test_models.py for all the functions including Read / Update / Delete / List All / Search by Name / Search by Category / Search by Availability?

As mentioned in Exercise 3, have you updated the test cases in the file tests/test_routes.py for all the functions including Read / Update / Delete / List All / List by Name / List by Category / List by Availability?

As mentioned in Exercise 3, have you updated the code in the file service/routes.py for all the functions including Read / Update / Delete / List All / List by Name / List by Category / List by Availability?

As mentioned in Exercise 4, have you updated the code in the file features/steps/load_steps.py for loading the BDD data?

As mentioned in Exercise 5, have you updated the code in the file features/products.feature for all the BDD scenarios including Read / Update / Delete / Search by Name / Search by Category / Search by Availability?

As mentioned in Exercise 6, have you updated the code in the file features/steps/web_steps.py for the Step Definitions?

Have you executed nosetests and confirmed that all the test cases passed with 95% code coverage?

Have you executed the honcho start and confirmed that the application is launching as expected?

Have you executed Behave and confirmed that all 7 BDD Scenarios passed?

## License

Licensed under the Apache License. See [LICENSE](/LICENSE)

## Author

John Rofrano, Senior Technical Staff Member, DevOps Champion, @ IBM Research

## <h3 align="center"> © IBM Corporation 2023. All rights reserved. <h3/>
