# Load tests hub

This project is a demo for sending load test results to
the [load-testing-hub](https://github.com/Nikita-Filonov/load-testing-hub-panel) service. It reads load test results
from `locust_stats.json`, `locust_stats_history.json`, `locust_exceptions.json`, `locust_ratio.json` files and sends
them to the [load-testing-hub API](https://github.com/Nikita-Filonov/load-testing-hub-api) using its endpoints. The
example is written in Python and uses Locust, but it can be adapted to any language; it is just a demonstration.

If you have any questions, you can ask [@Nikita Filonov](https://t.me/sound_right)

## Project setup

```shell
git clone https://github.com/Nikita-Filonov/load-tests-hub.git
cd load-tests-hub

pip install -r requirements.txt
python -m reports.script
```
