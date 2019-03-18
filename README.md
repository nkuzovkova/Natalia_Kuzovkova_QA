# Natalia_Kuzovkov_QA
Ormuco QA Automation test

The frameworks that were used to solve Technical Challenge is a part of my framemork that I'm using for the last 2 years. It proves it's reliability and flexibility. Pytets framework was used to write a test cases. Chain Of Responsibility Design Pattern was used in test_login_invalid_credentials to show the different aproach to write test cases.

## The criterias that made me choose these frameworks:
* Dynamical initialisation of elements (finding elements right before the action, that solves a comon problem StaleElementReferenceException);
* Component-base model. The logic is devided between different smal components to be easier to maintain;
* Page Object Model for enhancing test maintenance and reducing code duplication;
* Using of smart explicit waits;
* Element Typing that gives quick understanding of code and manipulations that can be done with particular element;
* Pytest test cases are easy to parametrize
* Pytest has a powerful fixture that can be usede in more complicated test scenarios.

## To setup an environment:
1. install the latest Python
2. install all nessesary dependensies:
   pip install -r requirements.txt
   
## To run test cases:
You can open a project in IDE for example IntelliJ IDEA and run test cases from there or you can run a command line:
> pytest test\