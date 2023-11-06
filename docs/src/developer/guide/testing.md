# Testing

End-to-end testing.

## Essential reading:

* https://playwright.dev/

## Setting up a testing environment

Please follow the Kartoza [coding standards](https://kartoza.github.io/TheKartozaHandbook/development/conventions/coding_standards/#compliance).

### Testing prerequisites

The primary framework used is [playwright](https://playwright.dev/).

### Setting up playwright

Navigate to the `playwright` directory, there are two other directories present:
    
    1. ci-tests
    2. staging-tests

Navigate to `ci-tests`.

To install `playwright` ensure you have [Node.js](https://nodejs.org/en) installed.

Once `Node.js` is installed, use `npm` JavaScript package manager to install `playwright`.

To install dependencies defined in `package.json` file:

```bash
npm install
```

To install playwright browsers and OS secific depndencies:

```bash
npm playwright install --with-deps
```

**Note:**

- By default it uses TypeScript(`*.ts`).

This command will install all the required browsers and other dependencies. The [directory structure](https://playwright.dev/docs/intro#whats-installed) will be as follows:

### Running tests

By default, tests will run on three browsers in headless mode.

To run all tests:

```bash
npx playwright test
```

To run a specific test file:

```bash
npx playwright test tests/'TESTNAME'.spec.ts
```

To run it in UI mode, one can add `--ui` tag at the end.

```bash
npx playwright test --ui
```

To run a specific file in UI mode:

```bash
npx playwright test --ui tests/'TESTNAME'.spec.ts
```

### Test reports

To generate test reports:

```bash
npx playwright show-report
```

### Continuous intergration testing

Use of [continuous integration and playwright](https://playwright.dev/docs/ci-intro).

The CI  for this project is present in the directory `.github/workflows` in the `build-and-test.yml` file.

The action builds and tests for and push or a pull request is made into the main repository.

![push or pull request](./img/testing-continuous-intergration-1.png)

It uses the `template.test.env` file to set up the environment. Which is copied into a new file `.env` while setting up the containers.

![testing env](./img/testing-continuous-intergration-2.png)

Testing the django endpoint:

![testing django endpoint](./img/testing-continuous-intergration-3.png)

Running coverage tests:

![coverage tests](./img/testing-continuous-intergration-4.png)

On setting up and testing using playwright.

![testing playwright](./img/testing-continuous-intergration-5.png)

1. Updates dependencies: Installs various dependencies required
2. Installs exact dependencies for `ci`, continuous integration.
3. Installs the playwright browsers and its packages.
4. Runs the playwright tests

Reports: It will generate a report as HTML document and it will be retained for 30 days if it is present in that directory

![testing report](./img/testing-continuous-intergration-6.png)

### Staging tests

#### Setting up environment

**NixOS**

If you are a NixOS user, you can set up direnv and then cd into this directory in your shell.

When you do so the first time, you will be prompted to allow direnv which you can do using this command:


```bash
direnv allow
```

>  This may take a while the first time as NixOS builds you a sandbox environment.

**Non-NixOS**

For a non-NixOS user(Debian/Ubuntu) set up your environment by the following [commands](./testing.md/#setting-up-a-testing-environment).

#### Recording a test

There is a bash helper script that will let you quickly create a new test:

```
Usage: ./record-test.sh TESTNAME
e.g. ./record-test.sh mytest
will write a new test to tests/mytest.spec.ts
Do not use spaces in your test name.
Test files MUST END in .spec.ts

After recording your test, close the test browser.
You can then run your test by doing:
./run-tests.sh
```


>  The first time you record a test, it will store your session credentials in a file ending in ``auth.json``. This file should **NEVER** be committed to git / shared publicly. There is a gitignore rule to ensure this.

#### Running a test


```bash
./run-tests.sh
```

The report can be downloaded and shared.
