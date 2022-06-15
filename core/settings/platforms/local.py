import os


def read_env(base_dir, path=None):
    if path:
        local_env = open(os.path.join(base_dir, path))
    else:
        local_env = open(os.path.join(base_dir, '.env'))

    env_list = dict()

    while True:
        line = local_env.readline()
        if not line:
            break
        if line.count("=") == 0:
            raise SyntaxError(".env file MUST HAVE `=` delimiter in each line.")

        line = line.replace('\n', '')
        line = line.split('=')
        key = line[0]
        value = line[1]
        env_list[key] = value

    return env_list