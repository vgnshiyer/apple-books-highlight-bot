# Apple Books - Highlight of the Day

Modified from [original](https://github.com/matttrent/ibooks-highlights).

<!-- Badges -->
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![](https://img.shields.io/badge/Follow-vgnshiyer-0A66C2?logo=linkedin)](https://www.linkedin.com/comm/mynetwork/discovery-see-all?usecase=PEOPLE_FOLLOWS&followMember=vgnshiyer)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Donate-yellow.svg?logo=buymeacoffee)](https://www.buymeacoffee.com/vgnshiyer)

## Description

A Github Actions workflow to get daily Highlight of the day from the books you read.

## Getting Started

[Fork this project.](https://github.com/vgnshiyer/apple-books-highlight-bot/fork)

### Dependencies

Install dependencies using `pip` package manager.

`pip install -r requirements.txt`

### Usage

Update your apple books data using the below command.

`python apple-books-export.py sync`

### Configure your actions.yaml

I recommend using your test email credentials.

* Go to your GitHub repository and click on the Settings tab.
* In the left sidebar, click on Secrets.
* Click on New repository secret.
* Enter the Name of the secret. For example, EMAIL or EMAILPASSWORD.
* Enter the Value of the secret. This should be the actual secret data you want to store.
* Click on Add secret to save the secret.
* Configure env variable `To` in `./github/workflows/actions.yaml` with the email you want to receive your updates.
* Change the `schedule` cron expression according to your timezone and your preferences.

#### Receive the daily highlights in your inbox every morning.

## Contributing

Thank you for considering contributing to this project! Your help is greatly appreciated.

To contribute to this project, please follow these guidelines:

### Opening Issues
If you encounter a bug, have a feature request, or want to discuss something related to the project, please open an issue on the GitHub repository. When opening an issue, please provide:

**Bug Reports**: Describe the issue in detail. Include steps to reproduce the bug if possible, along with any error messages or screenshots.

**Feature Requests**: Clearly explain the new feature you'd like to see added to the project. Provide context on why this feature would be beneficial.

**General Discussions**: Feel free to start discussions on broader topics related to the project.

### Steps

1️⃣ Fork the GitHub repository https://github.com/vgnshiyer/apple-books-highlight-bot \
2️⃣ Create a new branch for your changes (git checkout -b feature/my-new-feature). \
3️⃣ Make your changes and test them thoroughly. \
4️⃣ Push your changes and open a Pull Request to `main`.

*Please provide a clear title and description of your changes.*

## License

This project is licensed under the MIT License.

