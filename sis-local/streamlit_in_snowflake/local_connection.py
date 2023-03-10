from __future__ import annotations

from functools import reduce
from typing import Mapping

import pandas as pd
import streamlit as st
from snowflake.snowpark import Session


# deep_get can can iterate through nested dictionaries, used to get credentials in the
# case of a multi-level secrets.toml hierarchy
def deep_get(dictionary, keys, default={}):
    return reduce(
        lambda d, key: d.get(key, default) if isinstance(d, Mapping) else default,
        keys.split("."),
        dictionary,
    )


class LocalSnowparkConnection:
    # Initialize the connection; optionally provide the connection_name
    # (used to look up credentials in secrets.toml when run locally)
    #
    # For now this just provides a convenience connect() method to get an underlying
    # Snowpark session; it could also be extended to handle caching and other
    # functionality!
    def __init__(self, connection_name="connections.snowflake"):
        self.connection_name = connection_name

    # connect() returns a snowpark session object -
    # it checks session state for an existing object and tries to initialize
    # one if not yet created. It checks secrets.toml for credentials and provides a
    # more descriptive error if credentials are missing or path is misconfigured
    # (otherwise you get a "User is empty" error)
    def connect(self):
        if "snowpark_session" not in st.session_state:
            creds = deep_get(st.secrets, self.connection_name)

            if not creds:
                st.exception(
                    ValueError(
                        "Unable to initialize connection to Snowflake, did not "
                        "find expected credentials in secret "
                        f"{self.connection_name}. "
                        "Try updating your secrets.toml"
                    )
                )
                st.stop()
            st.session_state.snowpark_session = Session.builder.configs(creds).create()
        return st.session_state.snowpark_session
