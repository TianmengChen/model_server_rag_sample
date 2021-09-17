#
# Copyright (c) 2021 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from enum import IntEnum


class CallCount(IntEnum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3


# (model_name, model_version)
MODEL_SPEC_VALID = [
    ("model_name", 1),
    ("3", 17),
    ("*.-", 0),
    ("model_name", 9223372036854775806),
]

# (model_name, model_version, expected_exception, expected_message)
MODEL_SPEC_INVALID = [
    (12, 1, TypeError, "model_name type should be string, but is int"),
    (None, -1, TypeError, "model_name type should be string, but is NoneType"),
    (None, 1, TypeError, "model_name type should be string, but is NoneType"),
    ("model_name", "3", TypeError, "model_version type should be int, but is str"),
    ("model_name", None, TypeError, "model_version type should be int, but is NoneType"),
    ("model_name", -1, ValueError, f'model_version should be in range <0, {2**63-1}>'),
    ("model_name", 9223372036854775809, ValueError,
     f'model_version should be in range <0, {2**63-1}>'),
]


# (address)
ADDRESS_VALID = [
    ("localhost"),
    ("19.117.63.126"),
    ("cluster.cloud.iotg.intel.com")
]

# (address, expected_exception, expected_message)
ADDRESS_INVALID = [
    (19_117_63_126, TypeError, "address type should be string, but is int"),
    (['localhost'], TypeError, "address type should be string, but is list"),
    ("127.14", ValueError, "address is not valid"),
    ("intel.-com", ValueError, "address is not valid"),
    ("192.168.abc.4", ValueError, "address is not valid"),
    ("900.80.70.11", ValueError, "address is not valid"),
    ("....", ValueError, "address is not valid"),
    ("1000.1000.1000.1000", ValueError, "address is not valid"),
    ("19.-117.63.126", ValueError, "address is not valid"),
    ("0.0.0.0.0", ValueError, "address is not valid"),
    ("0.0.0.0.", ValueError, "address is not valid"),
]

# (port)
PORT_VALID = [
    (9000),
    (2**16-1),
]

# (port, expected_exception, expected_message)
PORT_INVALID = [
    ("9000", TypeError, "port type should be int, but is type str"),
    ([2**16-1], TypeError, "port type should be int, but is type list"),
    (2**16, ValueError, f"port should be in range <0, {2**16-1}>"),
    (-1, ValueError, f"port should be in range <0, {2**16-1}>")
]

# Special values for testing
PATH_VALID, PATH_INVALID = "valid_path", "invalid_path"

# Special values for testing
SERVER_CERT_PATH_VALID = "server_cert_path_valid"
SERVER_CERT_PATH_INVALID = "server_cert_path_invalid"
CLIENT_CERT_PATH_VALID = "client_cert_path_valid"
CLIENT_CERT_PATH_INVALID = "client_cert_path_invalid"
CLIENT_KEY_PATH_VALID = "client_key_path_valid"
CLIENT_KEY_PATH_INVALID = "client_key_path_invalid"

# (tls_config_dict, isfile_method_call_count)
TLS_CONFIG_VALID = [
    ({
        "server_cert_path": PATH_VALID
    },
     CallCount.ONE),
    ({
        "client_key_path": PATH_VALID,
        "client_cert_path": PATH_VALID,
        "server_cert_path": PATH_VALID
    },
     CallCount.THREE),
]

# (tls_config_dict,
# expected_exception, expected_message,
# isfile_method_call_count, [is_valid_client_key_path, is_valid_client_cert_path, is_valid_client_server_cert_path])  # noqa: E501
TLS_CONFIG_INVALID = [
    ({
        "client_key_path": PATH_VALID,
        "server_cert_path": PATH_VALID,
    },
     ValueError, "none or both client_key_path and client_cert_path are required in tls_config",
     CallCount.ZERO, None),
    ({
        "client_cert_path": PATH_VALID,
        "server_cert_path": PATH_VALID
    },
     ValueError, "none or both client_key_path and client_cert_path are required in tls_config",
     CallCount.ZERO, None),

    ({
        "non_client_key_path": PATH_VALID,
        "client_cert_path": PATH_VALID,
        "server_cert_path": PATH_VALID
    },
     ValueError, "none or both client_key_path and client_cert_path are required in tls_config",
     CallCount.ZERO, [True, True, True]),
    ({
        "client_key_path": PATH_VALID,
        "non_client_cert_path": PATH_VALID,
        "server_cert_path": PATH_VALID
    },
     ValueError, "none or both client_key_path and client_cert_path are required in tls_config",
     CallCount.ZERO, [True, True, True]),
    ({
        "client_key_path": PATH_VALID,
        "client_cert_path": PATH_VALID,
        "non_server_cert_path": PATH_VALID
    },
     ValueError, "server_cert_path is not defined in tls_config",
     CallCount.ZERO, [True, True, True]),
    ({
        "client_key_path": PATH_VALID,
        "client_cert_path": PATH_VALID
    },
     ValueError, "server_cert_path is not defined in tls_config",
     CallCount.ZERO, None),

    ({
        "client_key_path": 1,
        "client_cert_path": PATH_VALID,
        "server_cert_path": PATH_VALID
    },
     TypeError, 'client_key_path type should be string but is type int',
     CallCount.ZERO, [False, True, True]),
    ({
        "client_key_path": [PATH_VALID],
        "client_cert_path": PATH_VALID,
        "server_cert_path": PATH_VALID
    },
     TypeError, 'client_key_path type should be string but is type list',
     CallCount.ZERO, [False, True, True]),
    ({
        "client_key_path": 1,
        "client_cert_path": PATH_VALID,
        "server_cert_path": 1
    },
     TypeError, 'client_key_path type should be string but is type int',
     CallCount.ZERO, [False, True, False]),

    ({
        "client_key_path": PATH_VALID,
        "client_cert_path": 1,
        "server_cert_path": PATH_VALID
    },
     TypeError, 'client_cert_path type should be string but is type int',
     CallCount.ONE, [True, False, True]),
    ({
        "client_key_path": PATH_VALID,
        "client_cert_path": 1,
        "server_cert_path": 1
    },
     TypeError, 'client_cert_path type should be string but is type int',
     CallCount.ONE, [True, False, False]),
    ({
        "client_key_path": PATH_VALID,
        "client_cert_path": [PATH_VALID],
        "server_cert_path": PATH_VALID
    },
     TypeError, 'client_cert_path type should be string but is type list',
     CallCount.ONE, [True, False, True]),

    ({
        "client_key_path": PATH_VALID,
        "client_cert_path": PATH_VALID,
        "server_cert_path": 1
    },
     TypeError, 'server_cert_path type should be string but is type int',
     CallCount.TWO, [True, True, False]),
    ({
        "client_key_path": PATH_VALID,
        "client_cert_path": 1,
        "server_cert_path": [PATH_VALID]
    },
     TypeError, 'client_cert_path type should be string but is type int',
     CallCount.ONE, [True, False, False]),

    ({
        "client_key_path": PATH_INVALID,
        "client_cert_path": PATH_VALID,
        "server_cert_path": PATH_VALID
    },
     ValueError, 'invalid_path is not valid path to file',
     CallCount.ONE, [False, True, True]),
    ({
        "client_key_path": PATH_VALID,
        "client_cert_path": PATH_INVALID,
        "server_cert_path": PATH_VALID
    },
     ValueError, 'invalid_path is not valid path to file',
     CallCount.TWO, [True, False, True]),
    ({
        "client_key_path": PATH_VALID,
        "client_cert_path": PATH_VALID,
        "server_cert_path": PATH_INVALID
    },
     ValueError, 'invalid_path is not valid path to file',
     CallCount.THREE, [True, True, False]),

]

# (config_dict, method_call_count_dict= {"method_name": CallCount.NumberOfCalls})
CONFIG_VALID = [
    ({
        "address": "localhost",
        "port": 9000
    }, {"check_address": CallCount.ONE,
        "check_port": CallCount.ONE,
        "check_tls_config": CallCount.ZERO}),
    ({
        "address": "19.117.63.126",
        "port": 1
    }, {"check_address": CallCount.ONE,
        "check_port": CallCount.ONE,
        "check_tls_config": CallCount.ZERO}),
    ({
        "address": "cluster.cloud.iotg.intel.com",
        "port": 2**16-1
    }, {"check_address": CallCount.ONE,
        "check_port": CallCount.ONE,
        "check_tls_config": CallCount.ZERO}),
    ({
        "address": "localhost",
        "port": 9000,
        "tls_config": {
            "server_cert_path": "valid_path"
        }
    }, {"check_address": CallCount.ONE,
        "check_port": CallCount.ONE,
        "check_tls_config": CallCount.ONE}),
    ({
        "address": "localhost",
        "port": 9000,
        "tls_config": {
            "client_key_path": PATH_VALID,
            "client_cert_path": PATH_VALID,
            "server_cert_path": PATH_VALID
        }
    }, {"check_address": CallCount.ONE,
        "check_port": CallCount.ONE,
        "check_tls_config": CallCount.ONE})
]

# (config_dict, method_call_count_dict= {"method_name": CallCount.NumberOfCalls},
# expected_exception, expected_message,
# side_effect_dict = {"method_name": method_name_side_effect})
CONFIG_INVALID = [
    ({

    },
     {"check_address": CallCount.ZERO,
      "check_port": CallCount.ZERO,
      "check_tls_config": CallCount.ZERO},
     ValueError, 'The minimal config must contain address and port',
     {
        "check_address": None,
        "check_port": None,
        "check_tls_config": None
    }),

    ({
        "address": "localhost"
    },
     {"check_address": CallCount.ZERO,
      "check_port": CallCount.ZERO,
      "check_tls_config": CallCount.ZERO},
     ValueError, 'The minimal config must contain address and port',
     {
        "check_address": None,
        "check_port": None,
        "check_tls_config": None
    }),

    ({
        "port": 9000
    },
     {"check_address": CallCount.ZERO,
      "check_port": CallCount.ZERO,
      "check_tls_config": CallCount.ZERO},
     ValueError, 'The minimal config must contain address and port',
     {
        "check_address": None,
        "check_port": None,
        "check_tls_config": None
    }),

    ({
        "address": ["localhost"],
        "port": 9000
    },
     {"check_address": CallCount.ONE,
      "check_port": CallCount.ZERO,
      "check_tls_config": CallCount.ZERO},
     TypeError, 'address type should be string, but is list',
     {
        "check_address": TypeError('address type should be string, but is list'),
        "check_port": None,
        "check_tls_config": None
    }),

    ({
        "address": "address",
        "port": '9000'
    },
     {"check_address": CallCount.ONE,
      "check_port": CallCount.ZERO,
      "check_tls_config": CallCount.ZERO},
     ValueError, 'address is not valid',
     {
        "check_address": ValueError('address is not valid'),
        "check_port": None,
        "check_tls_config": None
    }),

    ({
        "address": "localhost",
        "port": '9000'
    },
     {"check_address": CallCount.ONE,
      "check_port": CallCount.ONE,
      "check_tls_config": CallCount.ZERO},
     TypeError, 'port type should be int, but is type str',
     {
        "check_address": None,
        "check_port": TypeError('port type should be int, but is type str'),
        "check_tls_config": None
    }),

    ({
        "address": "localhost",
        "port": 2**16
    },
     {"check_address": CallCount.ONE,
      "check_port": CallCount.ONE,
      "check_tls_config": CallCount.ZERO},
     ValueError, f"port should be in range <0, {2**16-1}>",
     {
        "check_address": None,
        "check_port": ValueError(f"port should be in range <0, {2**16-1}>"),
        "check_tls_config": None
    }),

    ({
        "address": "localhost",
        "port": 2**16,
        "tls_config": {

        }
    },
     {"check_address": CallCount.ONE,
      "check_port": CallCount.ONE,
      "check_tls_config": CallCount.ONE},
     ValueError, 'server_cert_path is not defined in tls_config',
     {
        "check_address": None,
        "check_port": None,
        "check_tls_config": ValueError('server_cert_path is not defined in tls_config')
    }),

    ({
        "address": "localhost",
        "port": 2**16,
        "tls_config": {
            "server_cert_path": PATH_VALID,
            "client_key_path": PATH_VALID
        }
    },
     {"check_address": CallCount.ONE,
      "check_port": CallCount.ONE,
      "check_tls_config": CallCount.ONE},
     ValueError, 'none or both client_key_path and client_cert_path are required in tls_config',
     {
        "check_address": None,
        "check_port": None,
        "check_tls_config": ValueError('none or both client_key_path and '
                                       'client_cert_path are required in tls_config')
    }),

    ({
        "address": "localhost",
        "port": 2**16,
        "tls_config": {
            "server_cert_path": PATH_VALID,
            "client_key_path": PATH_VALID,
            "client_cert_path": PATH_VALID,
            "invalid_key_name": PATH_VALID
        }
    },
     {"check_address": CallCount.ONE,
      "check_port": CallCount.ONE,
      "check_tls_config": CallCount.ONE},
     ValueError,  'invalid_key_name is not valid tls_config key',
     {
        "check_address": None,
        "check_port": None,
        "check_tls_config": ValueError('invalid_key_name is not valid tls_config key')
    }),

    ({
        "address": "localhost",
        "port": 2**16,
        "tls_config": {
            "server_cert_path": PATH_VALID,
            "client_key_path": PATH_VALID,
            "client_cert_path": 123,
        }
    },
     {"check_address": CallCount.ONE,
      "check_port": CallCount.ONE,
      "check_tls_config": CallCount.ONE},
     TypeError,  'client_cert_path type should be string but is type int',
     {
        "check_address": None,
        "check_port": None,
        "check_tls_config": TypeError('client_cert_path type should be string but is type int')
    }),

    ({
        "address": "localhost",
        "port": 2**16,
        "tls_config": {
            "server_cert_path": PATH_VALID,
            "client_key_path": "invalid_path",
            "client_cert_path": PATH_VALID,
        }
    },
     {"check_address": CallCount.ONE,
      "check_port": CallCount.ONE,
      "check_tls_config": CallCount.ONE},
     ValueError,  'invalid_path is not valid path to file',
     {
        "check_address": None,
        "check_port": None,
        "check_tls_config": ValueError('invalid_path is not valid path to file')
    }),
]

# (server_cert_path, client_cert_path, client_key_path,
# method_call_count_dict= {"method_name": CallCount.NumberOfCalls})
CHANNEL_CERTS_VALID = [
    (SERVER_CERT_PATH_VALID, CLIENT_CERT_PATH_VALID, CLIENT_KEY_PATH_VALID,
     {"check_certificate_valid": CallCount.TWO, "check_key_valid": CallCount.ONE}),

    (SERVER_CERT_PATH_VALID, None, None,
     {"check_certificate_valid": CallCount.ONE, "check_key_valid": CallCount.ZERO})
]

# (certificate_path)
CERTIFICATE_VALID = [
    (PATH_VALID),
]

# (key_path)
PRIVATE_KEY_VALID = [
    (PATH_VALID),
]
