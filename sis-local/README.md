# sis-local

Emulate SiS functionality in a local environment. This may not work perfectly, but it should catch many common errors
and provide a much smoother experience doing local development and porting to SiS!

- Throw warnings for commands that don't work in SiS
- (optional) Handles local Snowpark session setup

**If you find some missing compatibility issue, please file an issue and tag `@sfc-gh-jcarroll`**

## Usage

Just like Snowpark, **it requires python 3.8**

```shell
pip install "streamlit_in_snowflake @ git+https://github.com/sfc-gh-jcarroll/sis-tricks.git@sis-local#subdirectory=sis-local"
```

### Magic code block for the top of your app

```python
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.exceptions import SnowparkSessionException


def in_snowpark() -> bool:
    try:
        sess = get_active_session()
        return True
    except SnowparkSessionException:
        return False


if in_snowpark():
    import streamlit as st
    session = get_active_session()
else:
    import streamlit_in_snowflake as st
    # This part is optional, and requires secrets.toml setup
    session = st.LocalSnowparkConnection().connect()

# ...

```

### Configuring secrets.toml for `LocalSnowparkConnection`

LocalSnowparkConnection reads from `.streamlit/secrets.toml`. By default it looks for
a Snowflake connection config under the `[connections.snowflake]` heading. You can
customize this by setting `connection_name=` in the init.

- **TODO:** Add support for reading from snowsql config file.

```toml
# Example config for .streamlit/secrets.toml
[connections.snowflake]
user = "username"
warehouse = "MYWAREHOUSE"
role = "MYROLE"
account = "MYACCOUNT"
authenticator = "externalbrowser"
connection_timeout = "600"
```
