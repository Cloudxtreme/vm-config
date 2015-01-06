from util import *

call('curl -s get.gvmtool.net | bash')

config = """
gvm_auto_answer=true
gvm_suggestive_selfupdate=false
gvm_auto_selfupdate=true
"""

with open('/root/.gvm/etc/config', 'w+') as conf_file:
    conf_file.write(config)
