from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="TARUBOT",
    settings_files=["settings.yaml", ".secrets.yaml"],
    merge_enabled=True,
    environments=True,
    env_switcher="TARUBOT_ENV",
    env="development",
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
