# Austin Bikeshare data analysis

As a part of Stream Processing and Stream Analytics project.

### Project contributers
- [Mr Philosopher](https://github.com/7ze)
- [Usama Tahir](https://github.com/Usama00004)

> **Project Disclaimer**
>Please note that this project is currently under active development. The
>information provided in this readme and associated documentation is subject to
>change without prior notice. While we strive to provide accurate and
>up-to-date details, certain aspects of the project may be modified, added, or
>removed as development progresses.

### Set up Project
---

Follow along these steps to set up the project and start the publisher and
pipeline.

#### 1. Clone and setup up requirements

```sh
git clone https://github.com/7ze/austin-bikeshare-data-analysis.git
cd austin-bikeshare-data-analysis # project's root folder

python3 -m venv env # set up virtual env
pip3 install -U pip # update pip

pip3 install -r requirements.txt # install requirements
```

#### 2. Set up environment file

```sh
touch .env
```

and add these environment variables in your `.env` file as shown

```sh
PROJECT_ID="<your project id>"
BUCKET_NAME="<your google storage bucket name>"
TOPIC_ID="<your pubsub topic id>"
BIGQUERY_DATASET="<biguery dataset name from which you wish to query>"
DATA_SOURCE="<your big query dataset name to which you wish to write results>"
DATE_COLUMN="<name of the column which has event timestamps you wish to transform>"
MAX_OFFSET_MINS="<max offset in minutes between current time and message timestamp>"
MAX_SLEEP_SECONDS="<max time to sleep between publishing messages>"
ROWS_LIMIT="<max number of rows to query at a time>"
```

At this point you can inspect around and make the changes you wish to make.

#### 3. Run the publisher

```sh
# Run with -n or --no-op option enabled to see the config options set
# helpful in case you wish to debug

python3 publisher.py
```

#### 4. Run the pipeline

```sh
./run.sh # custom run script
```

Alternatively, you could also run the pipeline manually with custom options

```sh
# Run with -n or --no-op option enabled to see the config options set
# helpful in case you wish to debug

python3 main.py
```

#### And voilà, you have the pipeline running!
