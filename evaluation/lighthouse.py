

import os


line  = "https://edition.cnn.com/"
# os.system('sudo lighthouse --port=9222 --output html --output json --output-path "./{1}/{0}.json" --emulated-form-factor=none --throttling.cpuSlowdownMultiplier=1 --chrome-flags="--ignore-certificate-errors" https://{0}/{2}'.format(line,test,ext))


os.system('sudo lighthouse --chrome-flags="--ignore-certificate-errors" {0}'.format(line))