## Generating Token for DC/OS enabled Authentication

### Getting Config File

On Master Node: `cat /opt/mesosphere/lib/python3.5/site-packages/dcos_auth_python.py` to check on IAM_CONFIG_PATH location

   ```
IAM_CONFIG_PATH = '/run/dcos/etc/history-service/service_account.json'
   ```

Copy the file and update `"login_endpoint": "https://<your-dcos-master-url>/acs/api/v1/auth/login"`

### Generating Token

1. Get the custom python script: `dcos_generate_token.py`

2. Install python and corresponding python script dependencies.

3. Execute `python dcos_generate_token.py <config file>`

4.  Get the AUTH TOKEN that will be displayed:

   ```
AUTH_TOKEN: <auth token output>
   ```

### Token Verification

1. Get the custom python script: `dcos_verify_token.py`

2. Execute `python dcos_verify_token.py <master url> <dcos_auth_token>`. Example:

   ```
python dcos_verify_token.py m1.dcos.com <auth token output>
   ``` 

3. Verify the token expiration from the output: `expiration is: 2017-05-01 09:06:44`. Note that DC/OS default expiration is 5 days. To increase it you might need to set the default expiration at `/opt/mesosphere/etc/bouncer-config.json` and do a `systemctl restart dcos-bouncer`

   ```
    "EXPIRATION_AUTH_TOKEN_DAYS": 5
   ```


